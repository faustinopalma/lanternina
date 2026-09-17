"""The parent saying something to an afternoon that is already running.

Four routes and the shape is `panel/routes/requests.py`'s, because the rule is the same
one: the parent writes a row, and the house finds it when it next asks. What is different
is only what may be written. This route accepts deadline and termination commands from
`shared/message.py`; photograph assignments use the route that validates their candidates.

Nothing here reaches a house, and nothing here reads a message aloud. The house applies it
in `devices/run_experience.hear`, which draws nothing: an afternoon whose end hour moved
looks like an afternoon, which is the whole point.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from shared.message import MessageError

from ..gate import CurrentAccount, DeviceKey
from ..messages import MessageStore, clean_message

router = APIRouter()


class WhatIsSaid(BaseModel):
    """A deadline or termination command, optionally addressed to a reported open run.

    ``extra="forbid"`` is doing work rather than tidying: a body that carries a note is
    refused here as well as in `shared/message.py`, so the field cannot be added by
    accident on one side of the API and quietly accepted on the other.
    """

    model_config = ConfigDict(extra="forbid")

    says: str
    at: str = ""
    runId: str = ""


@router.post("/api/message")
def say_something(what: WhatIsSaid, account: CurrentAccount, request: Request) -> Any:
    """Say it. One row is written and that is the whole effect.

    No model is called, nothing is queued, and no display is touched. The afternoon in the
    house changes when the house next looks; an offline hub can delay delivery.
    """
    store: MessageStore = request.app.state.messages
    if what.says == "assign_photo":
        raise HTTPException(status_code=400, detail="use_photo_assignment")
    if what.runId and not any(
        run["runId"] == what.runId
        for run in request.app.state.trail.current(str(account.household_id)).runs
    ):
        raise HTTPException(status_code=404, detail="unknown_open_activity")
    try:
        pending = clean_message(
            str(account.household_id),
            says=what.says,
            at=what.at,
            written_by=str(account.id),
            run_id=what.runId,
        )
    except MessageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.add(pending).to_public()


@router.get("/api/messages")
def read_own_messages(account: CurrentAccount, request: Request) -> Any:
    """What the house has not yet come for, so the panel can say so rather than guess."""
    store: MessageStore = request.app.state.messages
    return {
        "messages": [row.to_public() for row in store.pending(str(account.household_id))]
    }


@router.get("/api/device/{household_id}/messages")
def device_messages(household_id: str, _: DeviceKey, request: Request) -> Any:
    """What the parent said, oldest first. The house decides what to do with it."""
    store: MessageStore = request.app.state.messages
    return {"messages": [row.to_public() for row in store.pending(household_id)
                         if str(row.said.says) != "assign_photo"]}


@router.post("/api/device/{household_id}/messages/{message_id}/heard")
def device_message_heard(
    household_id: str, message_id: str, _: DeviceKey, request: Request
) -> Any:
    """The house has heard this one. Cleared by id, so a message the parent wrote while
    the house was busy with the one before it is still there afterwards."""
    store: MessageStore = request.app.state.messages
    return {"heard": store.heard(household_id, message_id)}
