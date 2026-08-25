"""What this household's model calls consumed, and where its limit sits.

Numbers about machines, never about a person, and never a target to hit.

The limit is not a budget the parent was given: it is what stops a loop that has lost its
mind, and an ordinary month passes nowhere near it. It can be read and moved at any time,
because a limit nobody can see or change is one that stops the house without explaining
itself, which is what this one did until 25 August 2026.
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..config import Settings
from ..gate import CurrentAccount
from ..usage import (
    MAX_MONTHLY_LIMIT,
    Limit,
    LimitStore,
    UsageStore,
    clean_limit,
    limit_of,
    month_of,
)

router = APIRouter()


class ChosenLimit(BaseModel):
    """Where the parent wants the limit. Saving it starts nothing on its own."""

    calls: int


def _state(request: Request, household_id: str, period: str) -> dict[str, Any]:
    counter: UsageStore = request.app.state.usage
    limits: LimitStore = request.app.state.limit
    settings: Settings = request.app.state.settings
    summary = counter.summary(household_id, period)
    limit = limit_of(limits, household_id, settings.monthly_limit)
    chosen = limits.get(household_id)
    return {
        "usage": summary.to_public(),
        "limit": limit,
        "maxLimit": MAX_MONTHLY_LIMIT,
        "spent": summary.total.billed_calls,
        # Whether the house is being refused right now. Said plainly, because until this
        # existed the only sign was that nothing happened.
        "reached": limit > 0 and summary.total.billed_calls >= limit,
        # Zero when nobody has set it, which is not the same as a limit deliberately set to
        # the number the default happens to be.
        "changedAt": 0.0 if chosen is None else chosen.changed_at,
        "changedBy": "" if chosen is None else chosen.changed_by,
    }


@router.get("/api/usage")
def read_usage(account: CurrentAccount, request: Request, period: str = "") -> Any:
    """What this household's model calls consumed this month, split by kind.

    The split is the point: pictures and generated text are counted together by the limit
    and apart by everything else, so a figure never has to stand for a kind it does not
    describe. Numbers about machines, never about a person, and never a target to hit.
    """
    return _state(request, str(account.household_id), period or month_of(time.time()))


@router.post("/api/usage/limit")
def set_limit(chosen: ChosenLimit, account: CurrentAccount, request: Request) -> Any:
    """Set this household's limit, so work it refused can carry on.

    Recorded with who and when, and reported by the route above, so a limit somebody chose
    never looks like one that was always there.
    """
    household_id = str(account.household_id)
    period = month_of(time.time())
    counter: UsageStore = request.app.state.usage
    limits: LimitStore = request.app.state.limit
    spent = counter.summary(household_id, period).total.billed_calls
    try:
        calls = clean_limit(chosen.calls, spent)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    limits.set(
        Limit(
            household_id=household_id,
            calls=calls,
            changed_at=time.time(),
            changed_by=str(account.id),
        )
    )
    return _state(request, household_id, period)
