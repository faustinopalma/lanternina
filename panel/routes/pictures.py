"""The pictures a display has shown, kept so they can be put back later.

The house archives; the parent browses. Both sides read the same rows, and the image
itself is handed over as bytes on a route of its own rather than inside a listing.
"""

from __future__ import annotations

import base64
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from ..gate import CurrentAccount, DeviceKey
from ..pictures import DEFAULT_PAGE_SIZE, PAGE_SIZES, PictureArchive, PictureRecord

router = APIRouter()


class ShownPicture(BaseModel):
    """A picture a display has shown, archived so it can be put back later."""

    id: str
    theme: str = ""
    kind: str = "ok"
    display: str = ""
    createdAt: float = 0.0
    imageBase64: str


@router.post("/api/device/{household_id}/pictures")
def archive_picture(
    household_id: str, shown: ShownPicture, _: DeviceKey, request: Request
) -> Any:
    """Keep a picture that was shown, so it can be put back on a display later."""
    archive: PictureArchive = request.app.state.pictures
    record = archive.save(
        PictureRecord(
            id=shown.id,
            household_id=household_id,
            theme=shown.theme,
            created_at=shown.createdAt or time.time(),
            kind=shown.kind,
            display=shown.display,
        ),
        base64.b64decode(shown.imageBase64),
    )
    return record.to_public()


@router.get("/api/device/{household_id}/pictures")
def device_pictures(household_id: str, _: DeviceKey, request: Request) -> Any:
    archive: PictureArchive = request.app.state.pictures
    return {"pictures": [row.to_public() for row in archive.list(household_id)]}


@router.get("/api/device/{household_id}/pictures/{picture_id}")
def device_picture(household_id: str, picture_id: str, _: DeviceKey, request: Request) -> Any:
    """Hand back one archived picture, so the home server can show it again."""
    archive: PictureArchive = request.app.state.pictures
    try:
        record, image = archive.get(household_id, picture_id)
    except Exception as exc:  # storage SDKs raise their own not-found types
        raise HTTPException(status_code=404, detail="unknown_picture") from exc
    return {**record.to_public(), "imageBase64": base64.b64encode(image).decode()}


@router.get("/api/pictures")
def list_pictures(
    account: CurrentAccount,
    request: Request,
    page: int = 1,
    perPage: int = DEFAULT_PAGE_SIZE,
) -> Any:
    archive: PictureArchive = request.app.state.pictures
    size = perPage if perPage in PAGE_SIZES else DEFAULT_PAGE_SIZE
    household = str(account.household_id)
    wanted = max(1, page)
    rows, total = archive.page(household, offset=(wanted - 1) * size, limit=size)
    pages = max(1, -(-total // size))
    if wanted > pages:
        # A larger page size can leave the parent standing past the end. Show the last
        # page rather than an empty one.
        wanted = pages
        rows, total = archive.page(household, offset=(wanted - 1) * size, limit=size)
    return {
        "pictures": [row.to_public() for row in rows],
        "page": wanted,
        "perPage": size,
        "pages": pages,
        "total": total,
        "pageSizes": list(PAGE_SIZES),
    }


@router.get("/api/pictures/{picture_id}/content")
def picture_content(picture_id: str, account: CurrentAccount, request: Request) -> Response:
    archive: PictureArchive = request.app.state.pictures
    try:
        _record, image = archive.get(str(account.household_id), picture_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail="unknown_picture") from exc
    return Response(content=image, media_type="image/bmp")
