"""Authenticated camera archive and explicit, bounded deletion selections."""

from __future__ import annotations

import base64
import hashlib
import io
import time
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Request, Response
from PIL import Image
from pydantic import BaseModel, Field, model_validator

from panel.gate import CurrentAccount, DeviceKey
from panel.photos import Photo, PhotoArchive

router = APIRouter()
PhotoId = Annotated[str, Field(pattern=r"^[0-9a-f]{32}$")]
Timestamp = Annotated[float, Field(ge=0, allow_inf_nan=False)]


class UploadedPhoto(BaseModel):
    id: PhotoId
    camera: str = Field(min_length=1, max_length=64)
    capturedAt: Timestamp | None = None
    receivedAt: Timestamp
    state: Literal["pending", "processing", "done", "failed"] = "pending"
    imageBase64: str = Field(max_length=1_000_000)


class DeleteSelection(BaseModel):
    mode: Literal["single", "range", "all"]
    id: PhotoId | None = None
    start: Timestamp | None = None
    end: Timestamp | None = None

    @model_validator(mode="after")
    def selection(self) -> DeleteSelection:
        if self.mode == "single":
            valid = self.id is not None and self.start is None and self.end is None
        elif self.mode == "range":
            valid = self.id is None and self.start is not None and self.end is not None
            valid = valid and self.start < self.end
        else:
            valid = self.id is None and self.start is None and self.end is None
        if not valid:
            raise ValueError("invalid photograph selection")
        return self


class DeleteConfirmed(DeleteSelection):
    ids: list[PhotoId] = Field(max_length=10000)


class SyncReport(BaseModel):
    pending: int = Field(ge=0)
    localPhotos: int = Field(ge=0)
    lastReceivedAt: Timestamp | None = None


@router.post("/api/device/{household_id}/photos/sync")
def sync_report(household_id: str, body: SyncReport, _: DeviceKey, request: Request) -> dict:
    archive: PhotoArchive = request.app.state.photos
    archive.report(household_id, {**body.model_dump(), "contactAt": time.time()})
    return {"ids": [row.id for row in archive.list(household_id) if row.deleted]}


@router.post("/api/device/{household_id}/photos/{photo_id}/delete")
def device_delete(household_id: str, photo_id: str, _: DeviceKey, request: Request) -> dict:
    if len(photo_id) != 32 or any(char not in "0123456789abcdef" for char in photo_id):
        raise HTTPException(400, "invalid_photo_id")
    request.app.state.photos.delete(household_id, photo_id)
    return {"id": photo_id, "deleted": True}


def selected(rows: list[Photo], choice: DeleteSelection) -> list[str]:
    return [
        row.id
        for row in rows
        if not row.deleted
        and (
            choice.mode == "all"
            or (choice.mode == "single" and row.id == choice.id)
            or (choice.mode == "range" and choice.start <= row.date < choice.end)
        )
    ]


@router.post("/api/device/{household_id}/photos")
def upload(household_id: str, body: UploadedPhoto, _: DeviceKey, request: Request) -> dict:
    try:
        image = base64.b64decode(body.imageBase64, validate=True)
        if not 0 < len(image) <= 750000:
            raise ValueError("invalid image size")
        with Image.open(io.BytesIO(image)) as decoded:
            if decoded.format != "JPEG" or decoded.width * decoded.height > 12_000_000:
                raise ValueError("invalid JPEG")
            decoded.load()
            width, height = decoded.size
    except (ValueError, OSError) as exc:
        raise HTTPException(400, "invalid_photo") from exc
    archive: PhotoArchive = request.app.state.photos
    try:
        record = archive.save(
            household_id,
            Photo(
                body.id,
                body.camera,
                body.capturedAt,
                body.receivedAt,
                width,
                height,
                body.state,
                hashlib.sha256(image).hexdigest(),
            ),
            image,
        )
    except ValueError as exc:
        raise HTTPException(409, "conflicting_photo") from exc
    return {"id": record.id, "stored": not record.deleted, "deleted": record.deleted}


@router.get("/api/device/{household_id}/photos/deleted")
def deleted(household_id: str, _: DeviceKey, request: Request) -> dict:
    archive: PhotoArchive = request.app.state.photos
    return {"ids": [row.id for row in archive.list(household_id) if row.deleted]}


@router.get("/api/photos")
def listing(account: CurrentAccount, request: Request, page: int = 1) -> dict:
    archive: PhotoArchive = request.app.state.photos
    rows = sorted(
        (row for row in archive.list(str(account.household_id)) if not row.deleted),
        key=lambda row: (row.date, row.id),
        reverse=True,
    )
    pages = max(1, (len(rows) + 19) // 20)
    page = max(1, min(page, pages))
    return {
        "photos": [row.public() for row in rows[(page - 1) * 20 : page * 20]],
        "total": len(rows),
        "page": page,
        "pages": pages,
        "lastReceivedAt": max((row.receivedAt for row in rows), default=None),
        "hub": archive.status(str(account.household_id)),
    }


@router.get("/api/photos/{photo_id}/content")
def content(photo_id: str, account: CurrentAccount, request: Request) -> Response:
    if len(photo_id) != 32 or any(char not in "0123456789abcdef" for char in photo_id):
        raise HTTPException(404, "unknown_photo")
    try:
        image = request.app.state.photos.get(str(account.household_id), photo_id)
    except KeyError as exc:
        raise HTTPException(404, "unknown_photo") from exc
    return Response(image, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@router.post("/api/photos/delete-preview")
def preview(body: DeleteSelection, account: CurrentAccount, request: Request) -> dict:
    return {"ids": selected(request.app.state.photos.list(str(account.household_id)), body)}


@router.post("/api/photos/delete")
def delete(body: DeleteConfirmed, account: CurrentAccount, request: Request) -> dict:
    household = str(account.household_id)
    archive: PhotoArchive = request.app.state.photos
    allowed = set(selected(archive.list(household), body))
    removed, failed = [], []
    for photo_id in dict.fromkeys(body.ids):
        if photo_id not in allowed:
            continue
        try:
            archive.delete(household, photo_id)
            removed.append(photo_id)
        except Exception:
            failed.append(photo_id)
    return {"deleted": removed, "failed": failed}
