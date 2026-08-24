"""The two routes where the panel actually asks a model something.

Both are called by the house and by nothing else: a picture when it wants one, a reading
when a page comes off the glass. Neither is scheduled here — the cadence belongs to the
house, which is the only place that knows what is happening in the room.

Both are counted, and both refuse once the household's monthly cap is reached. A path that
counts against a cap without checking it can only be stopped by whichever path does check.
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked

from ..config import Settings
from ..gate import DeviceKey
from ..pictures import PictureArchive, PictureRecord
from ..themes import ThemeStore
from ..usage import (
    FAILED,
    KIND_IMAGE,
    REFUSED,
    SERVED,
    UsageStore,
    event_from,
    over_cap,
)

router = APIRouter()





@router.post("/api/device/{household_id}/paint")
async def paint_picture(
    household_id: str, _: DeviceKey, request: Request, theme: str = ""
) -> Any:
    """Paint one picture now, and hand back the bitmap ready for the panel.

    The home server calls this when it wants a new picture. Nothing here is scheduled:
    the cadence belongs to the house, which is the only place that knows what is
    happening in the room.
    """
    from devices.epaper import render_picture_bytes
    from shared.ids import new_id

    from ..painting import choose_theme, paint

    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if over_cap(counter, household_id, settings.monthly_call_cap):
        # Reaching the cap is a decision, not a fault: the display keeps its picture.
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    themes: ThemeStore = request.app.state.themes
    chosen = theme or choose_theme([row.label for row in themes.list(household_id)])

    reported: list[Any] = []
    outcome = FAILED
    try:
        picture_id, image_b64, _ = await paint(chosen, on_usage=reported.append)
        outcome = SERVED
    except SafetyBlocked as exc:
        # A refused picture is a normal outcome: the display keeps what it has.
        outcome = REFUSED
        raise HTTPException(status_code=409, detail=f"refused: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        try:
            counter.record(
                event_from(
                    household_id,
                    KIND_IMAGE,
                    outcome,
                    reported[0] if reported else None,
                    event_id=str(new_id("use")),
                )
            )
        except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a picture
            # The call was already made and paid for; failing here would spend the
            # money and deliver nothing. Loud in the log, silent to the house.
            logging.getLogger(__name__).warning("usage not recorded: %s", exc)

    bitmap = render_picture_bytes(image_b64)
    archive: PictureArchive = request.app.state.pictures
    archive.save(
        PictureRecord(
            id=picture_id,
            household_id=household_id,
            theme=chosen,
            created_at=time.time(),
        ),
        bitmap,
    )
    return {
        "id": picture_id,
        "theme": chosen,
        "imageBase64": base64.b64encode(bitmap).decode(),
    }
