"""The sentences the parent wrote, and the house asking what they mean.

Both halves of the feature meet here and they are different in kind. The parent's routes
persist words and nothing else — no model is asked, nothing is queued. The house's route
is the one place the interpreting is allowed to happen, because it happens inside the
answer to a request the house made.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from shared.errors import CloudUnavailable, NoCapacityError

from ..gate import CurrentAccount, DeviceKey
from ..reminders import (
    MAX_SENTENCE_LENGTH,
    SentenceStore,
    clean_reading,
    clean_sentence,
    make_sentence,
)

router = APIRouter()


class NewSentence(BaseModel):
    """One thing the parent wants remembered, in their own words. Saving it starts
    nothing: the house reads it when it next asks, and not before."""

    model_config = ConfigDict(extra="forbid")

    text: str


@router.get("/api/reminders")
def list_reminders(account: CurrentAccount, request: Request) -> Any:
    """The sentences the parent wrote, and whether the house has read each one."""
    store: SentenceStore = request.app.state.reminders
    return {
        "reminders": [row.to_public() for row in store.list(str(account.household_id))],
        # Stated while the parent types rather than enforced afterwards by truncation.
        "textLimit": MAX_SENTENCE_LENGTH,
    }


@router.post("/api/reminders")
def add_reminder(new: NewSentence, account: CurrentAccount, request: Request) -> Any:
    """Write down something to be remembered. It is stored and marked unread, and
    that is the entire effect: no model is asked what it means, nothing is queued,
    and the house does not find out until it next asks."""
    store: SentenceStore = request.app.state.reminders
    try:
        sentence = make_sentence(str(account.household_id), new.text, str(account.id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.add(sentence).to_public()


@router.post("/api/reminders/{reminder_id}")
def rewrite_reminder(
    reminder_id: str, new: NewSentence, account: CurrentAccount, request: Request
) -> Any:
    """Change a sentence. The parent's words stay the only copy, so answering a
    question the house asked is an edit here rather than a field somewhere else."""
    store: SentenceStore = request.app.state.reminders
    household = str(account.household_id)
    try:
        text = clean_sentence(new.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if reminder_id not in {row.id for row in store.list(household)}:
        raise HTTPException(status_code=404, detail="unknown_reminder")
    return store.rewrite(household, reminder_id, text).to_public()


@router.post("/api/reminders/{reminder_id}/remove")
def remove_reminder(reminder_id: str, account: CurrentAccount, request: Request) -> Any:
    """Stop remembering this. Nothing is kept: there is no artefact pointing back at
    a sentence, and how long it stood is not something worth recording."""
    store: SentenceStore = request.app.state.reminders
    store.remove(str(account.household_id), reminder_id)
    return {"removed": reminder_id}


@router.post("/api/device/{household_id}/reminders")
async def device_reminders(household_id: str, _: DeviceKey, request: Request) -> Any:
    """What the house should remind about, with the reading done inside this answer.

    This is the whole shape of the feature. A write from the panel is inert, so the
    parent's sentences sit unread until the house asks — and the asking is this call,
    on the timer the hub already has. What comes back is the reminders that have an
    hour; the house owns the clock and decides when a moment has come.

    A sentence the model cannot place gets a question instead, which the parent sees
    the next time they open the panel and answers by editing their own words.

    Nothing here records whether a reminder was ever shown or pressed. There is no
    field for it, which is the only way that stays true.
    """
    store: SentenceStore = request.app.state.reminders
    rows = store.list(household_id)
    unread = [(row.id, row.text) for row in rows if row.read_at <= 0.0]

    degraded = False
    if unread:
        from ..reading import read_sentences

        now = time.time()
        try:
            placements = await read_sentences(unread, now=now)
        except (NoCapacityError, CloudUnavailable, ValueError) as exc:
            # Reduced capability, not a stopped house: the sentences stay unread and
            # the reminders already placed are still handed over.
            logging.getLogger(__name__).warning("reminders not read: %s", exc)
            degraded = True
        else:
            for sentence_id, _text in unread:
                said = placements.get(sentence_id, (None, None, None))
                at, days, question = clean_reading(*said)
                store.record_reading(
                    household_id,
                    sentence_id,
                    read_at=now,
                    at=at,
                    days=days,
                    question=question,
                )
            rows = store.list(household_id)

    return {
        "reminders": [
            {"id": row.id, "text": row.text, "at": row.at, "days": list(row.days)}
            for row in rows
            if row.at
        ],
        "degraded": degraded,
    }
