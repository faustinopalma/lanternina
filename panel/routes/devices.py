"""Everything in the house, and what the parent decided each thing is for.

The hub reports what it found and is told what each thing is for in the same answer. The
parent names things and hands out jobs. Neither side can undo the other: a discovery pass
never carries a job or a name, and an assignment never claims a thing was seen.
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from shared.capabilities import KIND_DISPLAY

from ..devices import (
    MAX_NAME_LENGTH,
    DeviceStatus,
    DeviceStatusStore,
    InventoryStore,
    Thing,
    clean_jobs,
    clean_name,
    merged,
)
from ..gate import CurrentAccount, DeviceKey
from ..requests import KIND_IDENTIFY, KIND_LOOK_NOW, RequestStore, clean_request

router = APIRouter()


class ReportedDevice(BaseModel):
    """What the hub says about one thing in the house. The hub decides a display's level:
    it holds the thresholds and knows whether the display is declared mains powered.

    A printer or a scanner arrives here too, found over mDNS, carrying nothing but its
    identity — which is why everything except the id has a default.
    """

    id: str
    kind: str = KIND_DISPLAY
    name: str = ""
    address: str = ""
    lastSeen: float = 0.0
    level: str = "ok"
    voltage: float | None = None
    rssi: float | None = None
    firmware: str = ""
    model: str = ""
    # The house would not use the name the parent wrote: it carries a person's name. Only
    # the house can say so, and only it knows why.
    nameRefused: bool = False


class NewAssignment(BaseModel):
    """What the parent decided about one thing. Both parts are optional: naming a printer
    and giving it the job are two moments, and neither should undo the other.

    Unknown fields are refused rather than dropped, so a body carrying something we do not
    store cannot look as though it was saved.
    """

    model_config = ConfigDict(extra="forbid")

    jobs: list[str] | None = None
    name: str | None = None


@router.post("/api/device/{household_id}/devices")
def report_devices(
    household_id: str, reported: list[ReportedDevice], _: DeviceKey, request: Request
) -> Any:
    """The hub says what it found, and is told what each thing is for.

    State, not history. The report never carries a job or a name: those are the
    parent's, and a discovery pass that overwrote them would undo a choice made in the
    panel every five minutes.
    """
    store: DeviceStatusStore = request.app.state.devices
    inventory: InventoryStore = request.app.state.inventory
    recorded: list[str] = []
    for item in reported:
        seen = item.lastSeen or time.time()
        if item.kind == KIND_DISPLAY:
            store.record(
                DeviceStatus(
                    id=item.id,
                    household_id=household_id,
                    name=item.name or item.id,
                    last_seen=seen,
                    level=item.level,
                    voltage=item.voltage,
                    rssi=item.rssi,
                    firmware=item.firmware,
                    model=item.model,
                )
            )
        inventory.see(
            Thing(
                id=item.id,
                household_id=household_id,
                kind=item.kind,
                label=item.name,
                model=item.model,
                address=item.address,
                name_refused=item.nameRefused,
                last_seen=seen,
            )
        )
        recorded.append(item.id)
    # The whole inventory comes back, not only what was just reported: the hub caches
    # it, and a printer that was switched off this minute still has a job. What the parent
    # took off the list is left out, so a forgotten display stops being served without the
    # row -- and the job and the name on it -- having to be destroyed.
    return {
        "recorded": recorded,
        "things": [
            row.to_public()
            for row in inventory.list(household_id)
            if row.forgotten_at == 0.0
        ],
    }


@router.get("/api/device/{household_id}/whoami")
def whoami(household_id: str, _: DeviceKey) -> Any:
    """Which identity this container authenticates as. Claims only, never the token."""
    from ..painting import identity_claims

    try:
        return identity_claims()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"no token: {exc}") from exc


@router.get("/api/devices")
def list_devices(account: CurrentAccount, request: Request) -> Any:
    """Everything in the house, in one list, with whatever the hub last said about it."""
    store: DeviceStatusStore = request.app.state.devices
    inventory: InventoryStore = request.app.state.inventory
    household = str(account.household_id)
    everything = inventory.list(household)
    seen = store.list(household)
    here = [row for row in everything if row.forgotten_at == 0.0]
    gone = [row for row in everything if row.forgotten_at > 0.0]
    # Only the statuses of the things being listed. `merged` invents a row for a status it
    # has no thing for — which is right for the house and wrong here: handed every status,
    # the second list grew a row for every display that reports, and the panel said things
    # had been taken off the list that nobody had touched.
    forgotten_ids = {row.id for row in gone}
    return {
        "devices": merged(here, seen),
        # Kept apart rather than mixed in. What was taken off the list is not part of the
        # house any more, and the only thing to do with it is put it back.
        "forgotten": merged(gone, [row for row in seen if row.id in forgotten_ids]),
        # Stated while the parent types rather than enforced afterwards by truncation.
        "nameLimit": MAX_NAME_LENGTH,
    }


@router.post("/api/devices/{thing_id}")
def assign_device(
    thing_id: str, new: NewAssignment, account: CurrentAccount, request: Request
) -> Any:
    """Give a thing its job and its name. Nothing happens: choosing a printer prints
    nothing, and the hub finds out on its next run."""
    inventory: InventoryStore = request.app.state.inventory
    household = str(account.household_id)
    known = {row.id: row for row in inventory.list(household)}.get(thing_id)
    if known is None:
        raise HTTPException(status_code=404, detail="unknown_device")
    try:
        jobs = None if new.jobs is None else clean_jobs(known.kind, new.jobs)
        name = None if new.name is None else clean_name(new.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return inventory.assign(household, thing_id, jobs=jobs, name=name).to_public()


@router.post("/api/devices/{thing_id}/remove")
def forget_device(thing_id: str, account: CurrentAccount, request: Request) -> Any:
    """Take a thing off the list. Nothing leaves on its own for going quiet, so this
    is the only way out, and it is a decision somebody took.

    Marked rather than destroyed. The hub finds it on the network again within minutes and
    reports it, and a report carries no job and no name -- so before 25 August 2026 a press
    made by mistake put the row back stripped of both, which read as the panel losing a
    setting rather than as the removal being undone.
    """
    inventory: InventoryStore = request.app.state.inventory
    inventory.forget(str(account.household_id), thing_id)
    return {"removed": thing_id}


@router.post("/api/devices/look")
def look_now(account: CurrentAccount, request: Request) -> Any:
    """Ask the house to look at the network for printers and scanners now.

    A row written and nothing else, like everything else the parent asks for. The house
    looks on its own every minute; this exists because somebody who has just plugged a
    printer in is standing there, and what it buys them is the difference between waiting
    and knowing they have been heard.
    """
    store: RequestStore = request.app.state.requests
    asked = clean_request(
        household_id=str(account.household_id),
        kind=KIND_LOOK_NOW,
        # Nothing to name: the question is about the network, not about a thing.
        subject=KIND_LOOK_NOW,
        asked_by=str(account.id),
    )
    return store.put(asked).to_public()


@router.post("/api/devices/{thing_id}/recall")
def recall_device(thing_id: str, account: CurrentAccount, request: Request) -> Any:
    """Put a thing back on the list, with the job and the name it had."""
    inventory: InventoryStore = request.app.state.inventory
    try:
        return inventory.recall(str(account.household_id), thing_id).to_public()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="unknown_thing") from exc


@router.post("/api/devices/{thing_id}/identify")
def identify_device(thing_id: str, account: CurrentAccount, request: Request) -> Any:
    """Ask one display to say which one it is, so a row can be matched to a box on a wall.

    A row written and nothing else, like every other thing the parent asks for: the house
    collects it when it next looks, and the display changes at its own next refresh. The
    panel says both of those rather than implying the wall has already changed.
    """
    store: RequestStore = request.app.state.requests
    asked = clean_request(
        household_id=str(account.household_id),
        kind=KIND_IDENTIFY,
        subject=thing_id,
        asked_by=str(account.id),
    )
    return store.put(asked).to_public()
