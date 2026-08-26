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

    picturesFrom: str
    picturesUntil: str
    cadenceMinutes: int
    # Which days an afternoon may begin on, and between which hours. Absent means no day,
    # so a panel that has not been rebuilt cannot switch afternoons on by omission.
    afternoonDays: list[str] = []
    afternoonFrom: str = ""
    afternoonUntil: str = ""
    # Where the house is. Absent leaves whatever was saved before untouched by a panel
    # that has not been rebuilt, which is not the same as choosing to have none.
    timeZone: str | None = None
    # How many devised afternoons to keep waiting for a decision. Absent leaves what was
    # saved, for the same reason.
    scriptsWanted: int | None = None


@router.get("/api/rhythm")
def read_rhythm(account: CurrentAccount, request: Request) -> Any:
    store: RhythmStore = request.app.state.rhythm
    return store.get(str(account.household_id)).to_public()


@router.post("/api/rhythm")
def write_rhythm(new: NewRhythm, account: CurrentAccount, request: Request) -> Any:
    """Record when the display may change. It persists and returns: the hub reads it
    on its next run, and nothing here reaches into the house."""
    store: RhythmStore = request.app.state.rhythm
    kept = store.get(str(account.household_id))
    try:
        chosen = clean_rhythm(
            str(account.household_id),
            pictures_from=new.picturesFrom,
            pictures_until=new.picturesUntil,
            cadence_minutes=new.cadenceMinutes,
            afternoon_days=new.afternoonDays,
            afternoon_from=new.afternoonFrom or None,
            afternoon_until=new.afternoonUntil or None,
            # A panel that does not send the field leaves the zone as it was, so an older
            # browser cannot quietly move the house back onto the machine's own clock.
            time_zone=kept.time_zone if new.timeZone is None else new.timeZone,
            scripts_wanted=(
                kept.scripts_wanted if new.scriptsWanted is None else new.scriptsWanted
            ),
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
