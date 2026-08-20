"""The one channel from the panel into the house, and the shape every later one copies.

The parent presses; a row is written; the hub finds it when it next asks and decides what
to do with it. Nothing here calls a model, wakes a machine or schedules anything — a write
from the panel persists state and stops. That is what keeps "the panel writes, the house
decides" true in code rather than only in a document.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request

from ..gate import CurrentAccount, DeviceKey
from ..pictures import PictureArchive
from ..requests import KIND_SHOW_AGAIN, RequestStore, clean_request

router = APIRouter()


@router.post("/api/pictures/{picture_id}/again")
def ask_for_picture_again(picture_id: str, account: CurrentAccount, request: Request) -> Any:
    """Ask that this picture go back on the display. It records and returns.

    The picture is not fetched, sent or scheduled here. The hub reads the request on its
    next run and puts the picture back itself, which means the wait is up to one spacing
    between pictures — the panel has no way to shorten that and is not given one.
    """
    archive: PictureArchive = request.app.state.pictures
    try:
        archive.get(str(account.household_id), picture_id)
    except Exception as exc:  # storage SDKs raise their own not-found types
        raise HTTPException(status_code=404, detail="unknown_picture") from exc

    store: RequestStore = request.app.state.requests
    asked = clean_request(
        str(account.household_id),
        kind=KIND_SHOW_AGAIN,
        subject=picture_id,
        asked_by=str(account.id),
    )
    return store.put(asked).to_public()


@router.get("/api/request")
def read_own_request(account: CurrentAccount, request: Request) -> Any:
    """What the house has not yet come to collect, so the panel can say "asked for"."""
    store: RequestStore = request.app.state.requests
    standing = store.get(str(account.household_id))
    return {"request": standing.to_public() if standing else None}


@router.get("/api/device/{household_id}/request")
def device_request(household_id: str, _: DeviceKey, request: Request) -> Any:
    """What the parent has asked for, or nothing. The house decides whether to act."""
    store: RequestStore = request.app.state.requests
    standing = store.get(household_id)
    return {"request": standing.to_public() if standing else None}


@router.post("/api/device/{household_id}/request/{request_id}/done")
def device_request_done(
    household_id: str, request_id: str, _: DeviceKey, request: Request
) -> Any:
    """The house has acted on this request. Cleared by id, so a press that landed while
    the house was busy with the previous one is still there afterwards."""
    store: RequestStore = request.app.state.requests
    return {"cleared": store.clear(household_id, request_id)}
