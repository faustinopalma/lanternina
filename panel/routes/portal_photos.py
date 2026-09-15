"""Bounded mobile uploads and the home's authenticated pull of pending photographs."""

from __future__ import annotations

import base64
import hashlib
import io
import re
import time

from fastapi import APIRouter, HTTPException, Request, Response
from PIL import Image, ImageOps, UnidentifiedImageError

from panel.gate import DeviceKey
from panel.photos import Photo
from panel.routes.adolescents import Member

router = APIRouter()
MAX_UPLOAD = 12_000_000


def valid_id(photo_id: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{32}", photo_id):
        raise HTTPException(404, "unknown_photo")


def own_photo(request: Request, member: dict, photo_id: str) -> Photo:
    valid_id(photo_id)
    for row in request.app.state.photos.list(member["household"]):
        if row.id == photo_id and row.camera == "portal:" + member["id"] and not row.deleted:
            return row
    raise HTTPException(404, "unknown_photo")


def normalize(raw: bytes) -> tuple[bytes, int, int]:
    try:
        with Image.open(io.BytesIO(raw)) as source:
            if source.format not in {"JPEG", "PNG", "WEBP"} or (
                source.width * source.height > 12_000_000
            ):
                raise ValueError("unsupported image")
            source.load()
            image = ImageOps.exif_transpose(source).convert("RGB")
            image.thumbnail((1600, 1200))
            image.info.clear()
            for quality in (85, 70, 50):
                output = io.BytesIO()
                image.save(output, "JPEG", quality=quality)
                jpeg = output.getvalue()
                if len(jpeg) <= 750000:
                    return jpeg, image.width, image.height
            raise ValueError("image too large")
    except (ValueError, OSError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise HTTPException(400, "invalid_photo") from exc


@router.post("/api/portal/photos/{photo_id}")
async def upload(photo_id: str, member: Member, request: Request) -> dict:
    from starlette.concurrency import run_in_threadpool

    valid_id(photo_id)
    raw = bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw) > MAX_UPLOAD:
            raise HTTPException(413, "photo_too_large")
    image, width, height = await run_in_threadpool(normalize, bytes(raw))

    def save() -> dict:
        archive = request.app.state.photos
        rows = archive.list(member["household"])
        source = "portal:" + member["id"]
        digest = hashlib.sha256(image).hexdigest()
        for old in rows:
            if old.id == photo_id:
                if old.camera != source or old.digest != digest:
                    raise HTTPException(409, "conflicting_photo")
                if old.deleted:
                    raise HTTPException(410, "photo_deleted")
                return old.public()
        now = time.time()
        retained = {row.id for row in rows if row.camera == source and not row.deleted}
        deleted = {row.id for row in rows if row.camera == source and row.deleted}

        def reserve(data: dict) -> None:
            current = next((entry for entry in data["members"].values()
                            if entry["id"] == member["id"] and entry["active"]), None)
            if current is None:
                raise HTTPException(403, "portal_access_required")
            uploads = {key: stamp for key, stamp in current.get("uploads", {}).items()
                       if stamp > now - 86400}
            reserved = {key for key, stamp in uploads.items()
                        if stamp > now - 120 and key not in deleted}
            if photo_id not in uploads and len(uploads) >= 1000:
                raise HTTPException(429, "photo_daily_limit")
            if photo_id not in retained | reserved and len(retained | reserved) >= 200:
                raise HTTPException(429, "photo_limit")
            uploads[photo_id] = now
            current["uploads"] = uploads

        request.app.state.portal.change(reserve)
        row = Photo(photo_id, source, now, now, width, height, "pending", digest)
        try:
            saved = archive.save(member["household"], row, image, preserve_state=True)
            if saved.deleted:
                raise HTTPException(410, "photo_deleted")
            return saved.public()
        except Exception as exc:
            request.app.state.portal.change(
                lambda data: next(entry for entry in data["members"].values()
                                  if entry["id"] == member["id"])["uploads"].pop(photo_id, None)
            )
            if isinstance(exc, ValueError):
                raise HTTPException(409, "conflicting_photo") from exc
            raise

    return await run_in_threadpool(save)


@router.get("/api/portal/photos")
def listing(member: Member, request: Request, page: int = 1) -> dict:
    rows = sorted(
        (row for row in request.app.state.photos.list(member["household"])
         if row.camera == "portal:" + member["id"] and not row.deleted),
        key=lambda row: (row.receivedAt, row.id), reverse=True,
    )
    pages = max(1, (len(rows) + 19) // 20)
    page = min(max(1, page), pages)
    return {"photos": [row.public() for row in rows[(page - 1) * 20:page * 20]],
            "total": len(rows), "page": page, "pages": pages}


@router.get("/api/portal/photos/{photo_id}/content")
def content(photo_id: str, member: Member, request: Request) -> Response:
    own_photo(request, member, photo_id)
    try:
        image = request.app.state.photos.get(member["household"], photo_id)
    except KeyError as exc:
        raise HTTPException(404, "unknown_photo") from exc
    return Response(image, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@router.delete("/api/portal/photos/{photo_id}")
def delete(photo_id: str, member: Member, request: Request) -> dict:
    own_photo(request, member, photo_id)
    request.app.state.photos.delete(member["household"], photo_id)
    return {"deleted": True}


@router.post("/api/device/{household_id}/portal-photos/pull")
def pull(household_id: str, _: DeviceKey, request: Request) -> dict:
    active = {
        "portal:" + member["id"]
        for member in request.app.state.portal.read()["members"].values()
        if member["household"] == household_id and member["active"]
        and (parent := request.app.state.store.by_subject(member["parent"])) is not None
        and parent.status == "active"
    }
    archive = request.app.state.photos
    pending = sorted(
        (row for row in archive.list(household_id)
         if row.camera in active and row.state == "pending" and not row.deleted),
        key=lambda row: (row.receivedAt, row.id),
    )[:10]
    answer = []
    for row in pending:
        try:
            image = archive.get(household_id, row.id)
        except KeyError:
            continue
        answer.append({**row.public(), "imageBase64": base64.b64encode(image).decode()})
    return {"photos": answer}