"""The sentences the parent wrote, and the house asking what they mean.

Both halves of the feature meet here and they are different in kind. The parent's routes
persist words and nothing else — no model is asked, nothing is queued. The house's route
is the one place the interpreting is allowed to happen, because it happens inside the
answer to a request the house made.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked

from ..config import Settings
from ..gate import CurrentAccount, DeviceKey
from ..reminders import (
    MAX_SENTENCE_LENGTH,
    SentenceStore,
    clean_reading,
    clean_sentence,
    clean_wordings,
    make_sentence,
)
from ..usage import (
    FAILED,
    KIND_IMAGE,
    KIND_READ,
    KIND_TEXT,
    REFUSED,
    SERVED,
    UsageStore,
    at_the_limit,
    event_from,
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
    the next time they open the panel and answers by editing their own words. One that
    is placed is also given a few ways of saying it, in the same breath and once in its
    life — that is content, so it goes out through the gate, and if the gate or the
    cloud refuses it the reminder simply carries the parent's own sentence.

    Nothing here records whether a reminder was ever shown or pressed. There is no
    field for it, which is the only way that stays true.

    At the monthly cap the sentences are left unread and the answer comes back degraded,
    rather than refused: a refusal would take the reminders already placed with it.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    store: SentenceStore = request.app.state.reminders
    rows = store.list(household_id)
    unread = [(row.id, row.text) for row in rows if row.read_at <= 0.0]

    degraded = False
    if unread and at_the_limit(
        counter, request.app.state.limit, household_id, settings.monthly_limit
    ):
        # Reaching the cap says the same thing to the house as a cloud that will not
        # answer: the sentences stay unread, and the reminders already placed still go
        # out. A 429 for the whole call would take those with it.
        logging.getLogger(__name__).info("reminders not read: the monthly cap is reached")
        degraded = True
    elif unread:
        from ..reading import read_sentences

        now = time.time()
        placements: Mapping[str, tuple[Any, Any, Any]] = {}
        spent: Any = None
        outcome = FAILED
        try:
            placements, spent = await read_sentences(unread, now=now)
            outcome = SERVED
        except (NoCapacityError, CloudUnavailable, ValueError) as exc:
            # Reduced capability, not a stopped house: the sentences stay unread and
            # the reminders already placed are still handed over.
            logging.getLogger(__name__).warning("reminders not read: %s", exc)
            degraded = True
        # Written down before the wordings are asked for, so that a batch large enough to
        # pass the cap is stopped by the call it has already made.
        _count(counter, household_id, KIND_READ, outcome, spent)
        if outcome == SERVED:
            for sentence_id, text in unread:
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
                if at:
                    await _word(request, household_id, sentence_id, text, at, now=now)
            rows = store.list(household_id)

    return {
        "reminders": [
            {
                "id": row.id,
                "text": row.text,
                "at": row.at,
                "days": list(row.days),
                "words": list(row.words),
            }
            for row in rows
            if row.at
        ],
        "degraded": degraded,
    }


async def _word(
    request: Request, household_id: str, sentence_id: str, text: str, at: str, *, now: float
) -> None:
    """Give one placed sentence a few ways of saying it. Never raises.

    Called once per sentence, in the call that read it, and not again: the hub asks every
    five minutes, so retrying a sentence the cloud will not word would pay for it about
    two hundred and eighty times a day. A sentence that got no wordings keeps the parent's
    own, and the way to ask again is the way the parent already has — editing it, which
    makes it unread.

    The cap is checked here and not only where the reading is, because the reading of a
    batch is one call and the wording is one per sentence in it: a household writing forty
    sentences at once passes the cap in the middle of the batch, and the sentences after
    that point would otherwise be paid for anyway.
    """
    from ..wording import word_sentence

    settings: Settings = request.app.state.settings
    store: SentenceStore = request.app.state.reminders
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        logging.getLogger(__name__).info("reminder not worded: the monthly cap is reached")
        return
    spent: Any = None
    outcome = FAILED
    try:
        words, spent = await word_sentence(text, at, now=now)
    except SafetyBlocked as exc:
        # A refused wording is a normal outcome: the parent's own sentence is shown.
        outcome = REFUSED
        logging.getLogger(__name__).info("wording refused: %s", exc)
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("reminder not worded: %s", exc)
    else:
        outcome = SERVED
        store.record_wording(household_id, sentence_id, words=clean_wordings(words))
    _count(counter, household_id, KIND_TEXT, outcome, spent)


@router.post("/api/device/{household_id}/reminders/{sentence_id}/words")
async def say_it_now(
    household_id: str, sentence_id: str, _: DeviceKey, request: Request
) -> Any:
    """One way of saying this reminder, for the showing about to happen, and a drawing.

    Asked for by the house at the moment a reminder comes due, and not before: this is
    the only route here that generates because a moment arrived rather than because a
    batch was read. The house asks once per occurrence, which is about once a day per
    reminder — `panel/usage.py` adds that into the ordinary month.

    Nothing about the showing is written down. Not that it happened, not which words went
    up, not when: the wording is generated, handed over and forgotten, which is what keeps
    this from becoming a record of how often somebody was reminded of something.

    Never refuses for the cloud's sake. An empty answer means the house shows what it
    already has — one of the wordings made when the sentence was read, or the parent's own
    sentence — so a reminder still goes up when nothing here can be reached.
    """
    store: SentenceStore = request.app.state.reminders
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    known = {row.id: row for row in store.list(household_id)}.get(sentence_id)
    if known is None or not known.at:
        raise HTTPException(status_code=404, detail="unknown_reminder")
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        logging.getLogger(__name__).info("reminder not said: the monthly limit is reached")
        return {"words": "", "decorationBase64": ""}

    from ..wording import say_sentence_now

    said = ""
    subject = ""
    spent: Any = None
    outcome = FAILED
    try:
        said, subject, spent = await say_sentence_now(known.text, known.at, now=time.time())
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("wording refused: %s", exc)
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("reminder not said: %s", exc)
    _count(counter, household_id, KIND_TEXT, outcome, spent)
    words = next(iter(clean_wordings([said])), "")
    return {
        "words": words,
        "decorationBase64": await _decoration(request, household_id, subject),
    }


async def _decoration(request: Request, household_id: str, subject: str) -> str:
    """A small drawing of what the sentence is about, or nothing. Never raises.

    Nothing is the ordinary answer for a sentence that names no drawable thing, and it is
    also what a refusal or an unreachable cloud comes to: the words go up either way, and
    a reminder that did not appear because its ornament could not be drawn would be the
    wrong failure.
    """
    if not subject:
        return ""
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        return ""

    from ..painting import decorate

    reported: list[Any] = []
    outcome = FAILED
    drawn = ""
    try:
        drawn = await decorate(subject, on_usage=reported.append)
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("decoration refused: %s", exc)
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("reminder not decorated: %s", exc)
    _count(
        counter,
        household_id,
        KIND_IMAGE,
        outcome,
        reported[0] if reported else None,
    )
    return drawn


def _count(
    counter: UsageStore, household_id: str, kind: str, outcome: str, spent: Any
) -> None:
    """Write down what a call consumed. Never raises: the call was already made and paid
    for, so failing here would spend the money and deliver nothing."""
    from shared.ids import new_id

    try:
        counter.record(
            event_from(household_id, kind, outcome, spent, event_id=str(new_id("use")))
        )
    except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a reminder
        logging.getLogger(__name__).warning("usage not recorded: %s", exc)
