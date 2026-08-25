"""What this household's model calls consumed, and where its fuse sits.

Numbers about machines, never about a person, and never a target to hit.

The fuse is not a budget the parent was given: it is what stops a loop that has lost its
mind, and an ordinary month passes nowhere near it. The only time anybody needs to see it
is when it has gone, and the only useful thing to do then is move it and carry on.
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..config import Settings
from ..gate import CurrentAccount
from ..usage import (
    MAX_MONTHLY_CALL_CAP,
    Fuse,
    FuseStore,
    UsageStore,
    cap_of,
    clean_cap,
    month_of,
)

router = APIRouter()


class RaisedFuse(BaseModel):
    """Where the parent wants the fuse. Moving it starts nothing on its own."""

    calls: int


def _state(request: Request, household_id: str, period: str) -> dict[str, Any]:
    counter: UsageStore = request.app.state.usage
    fuses: FuseStore = request.app.state.fuse
    settings: Settings = request.app.state.settings
    summary = counter.summary(household_id, period)
    cap = cap_of(fuses, household_id, settings.monthly_call_cap)
    moved = fuses.get(household_id)
    return {
        "usage": summary.to_public(),
        "cap": cap,
        "maxCap": MAX_MONTHLY_CALL_CAP,
        "spent": summary.total.billed_calls,
        # Whether the house is being refused right now. Said plainly, because until this
        # existed the only sign was that nothing happened.
        "reached": cap > 0 and summary.total.billed_calls >= cap,
        # Zero when nobody has moved it, which is not the same as a fuse deliberately set
        # to the number the default happens to be.
        "raisedAt": 0.0 if moved is None else moved.raised_at,
        "raisedBy": "" if moved is None else moved.raised_by,
    }


@router.get("/api/usage")
def read_usage(account: CurrentAccount, request: Request, period: str = "") -> Any:
    """What this household's model calls consumed this month, split by kind.

    The split is the point: pictures and generated text are counted together by the cap
    and apart by everything else, so a figure never has to stand for a kind it does not
    describe. Numbers about machines, never about a person, and never a target to hit.
    """
    return _state(request, str(account.household_id), period or month_of(time.time()))


@router.post("/api/usage/fuse")
def raise_fuse(moved: RaisedFuse, account: CurrentAccount, request: Request) -> Any:
    """Move this household's fuse, so work it refused can carry on.

    Recorded with who and when, and reported by the route above, so a fuse somebody moved
    never looks like one that was always there.
    """
    household_id = str(account.household_id)
    period = month_of(time.time())
    counter: UsageStore = request.app.state.usage
    fuses: FuseStore = request.app.state.fuse
    spent = counter.summary(household_id, period).total.billed_calls
    try:
        calls = clean_cap(moved.calls, spent)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    fuses.set(
        Fuse(
            household_id=household_id,
            calls=calls,
            raised_at=time.time(),
            raised_by=str(account.id),
        )
    )
    return _state(request, household_id, period)
