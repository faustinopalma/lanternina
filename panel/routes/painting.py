"""The two routes where the panel actually asks a model something.

Both are called by the house and by nothing else: a picture when it wants one, a reading
when a page comes off the glass. Neither is scheduled here — the cadence belongs to the
house, which is the only place that knows what is happening in the room.
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked

from ..config import Settings
from ..gate import DeviceKey
from ..pictures import PictureArchive, PictureRecord
from ..themes import ThemeStore
from ..usage import FAILED, KIND_IMAGE, REFUSED, SERVED, UsageStore, event_from, over_cap

router = APIRouter()


class PageToRead(BaseModel):
    """One rectified page and the sheet that says where its boxes are.

    The image is the crop inside the four corner markers and nothing else. The sheet is
    what ``SheetSpec.to_dict()`` produces, which carries no expected answer: there is no
    field on the wire for what a mark should have been.
    """

    model_config = ConfigDict(extra="forbid")

    imageBase64: str
    width: int = 0
    height: int = 0
    sheet: dict[str, Any] = Field(default_factory=dict)


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


@router.post("/api/device/{household_id}/read-sheet")
async def read_sheet_page(
    household_id: str, page: PageToRead, _: DeviceKey, request: Request
) -> Any:
    """Read one filled-in sheet and hand back what is in each box.

    The house calls this when a page comes off the glass. What comes back describes
    ink — this box has a mark, this one does not, this one I could not tell — and the
    house turns it into a sentence. Nothing here says anything about who filled it in,
    and there is no field in which it could.

    A refusal leaves the house to fall back on its own arithmetic and say so, which is
    the whole of what "reduced capability, not a stopped system" means on this path.
    """
    from shared.sheet import SheetSpec
    from shared.vision_contracts import RectifiedPage

    from ..reading import read_sheet

    try:
        spec = SheetSpec.from_dict(page.sheet)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"not a sheet: {exc}") from exc

    png = base64.b64decode(page.imageBase64)
    rectified = RectifiedPage(
        sheet_id=spec.sheet_id,
        exercise_id=spec.exercise_id,
        png=png,
        width=page.width,
        height=page.height,
        captured_at=time.time(),
        spec_version=spec.spec_version,
    )
    try:
        reading = await read_sheet(rectified, spec, now=time.time())
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    return reading.to_dict()
