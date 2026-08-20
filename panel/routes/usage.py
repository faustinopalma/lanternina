"""What this household's model calls consumed, as the backend reported it.

Numbers about machines, never about a person, and never a target to hit.
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, Request

from ..config import Settings
from ..gate import CurrentAccount
from ..usage import UsageStore, month_of

router = APIRouter()


@router.get("/api/usage")
def read_usage(account: CurrentAccount, request: Request, period: str = "") -> Any:
    """What this household's model calls consumed this month, split by kind.

    The split is the point: pictures and generated text are counted together by the cap
    and apart by everything else, so a figure never has to stand for a kind it does not
    describe. Numbers about machines, never about a person, and never a target to hit.
    """
    counter: UsageStore = request.app.state.usage
    settings: Settings = request.app.state.settings
    summary = counter.summary(str(account.household_id), period or month_of(time.time()))
    return {"usage": summary.to_public(), "cap": settings.monthly_call_cap}
