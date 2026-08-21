"""When the display may change, and how often.

Three routes and one shape: the parent writes it, the hub reads it on its next run. Saving
it reaches into nothing.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..gate import CurrentAccount, DeviceKey
from ..rhythm import RhythmStore, clean_rhythm

router = APIRouter()


class NewRhythm(BaseModel):
    """When the house may do something, and how often. Saving it starts nothing."""

    quietFrom: str
    quietUntil: str
    cadenceMinutes: int
    # Which days an afternoon may begin on, and from what hour. Absent means no day, so a
    # panel that has not been rebuilt cannot switch afternoons on by omission.
    afternoonDays: list[str] = []
    afternoonFrom: str = ""


@router.get("/api/rhythm")
def read_rhythm(account: CurrentAccount, request: Request) -> Any:
    store: RhythmStore = request.app.state.rhythm
    return store.get(str(account.household_id)).to_public()


@router.post("/api/rhythm")
def write_rhythm(new: NewRhythm, account: CurrentAccount, request: Request) -> Any:
    """Record when the display may change. It persists and returns: the hub reads it
    on its next run, and nothing here reaches into the house."""
    store: RhythmStore = request.app.state.rhythm
    try:
        chosen = clean_rhythm(
            str(account.household_id),
            quiet_from=new.quietFrom,
            quiet_until=new.quietUntil,
            cadence_minutes=new.cadenceMinutes,
            afternoon_days=new.afternoonDays,
            afternoon_from=new.afternoonFrom or None,
            updated_by=str(account.id),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.set(chosen).to_public()


@router.get("/api/device/{household_id}/rhythm")
def device_rhythm(household_id: str, _: DeviceKey, request: Request) -> Any:
    """The hours and the spacing the hub applies, as the parent last left them."""
    store: RhythmStore = request.app.state.rhythm
    return store.get(household_id).to_public()
