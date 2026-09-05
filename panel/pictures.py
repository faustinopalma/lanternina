"""The archive of pictures a display has shown, and the way to put one back.

Blobs rather than the database: a picture is 48 KB of bitmap, which is the wrong shape for
a document store and the right shape for object storage. What is kept is the **rendered**
1-bit image, not the model's original — the record is of what was actually on the display.

The storage account refuses public access and shared keys, both forced by tenant policy,
so this reaches it over a private endpoint with the container's managed identity. That is
also why the archive is written through the panel: the server in the home cannot see the
storage account, and should not have a key that would let it.
"""

from __future__ import annotations

import threading
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable
from urllib.parse import quote, unquote

# How many pictures the gallery shows at once. The parent picks one of these; anything
# else is refused rather than rounded, so a hand-typed URL cannot ask for the whole
# archive in one page.
PAGE_SIZES = (10, 20, 30, 50)
DEFAULT_PAGE_SIZE = 20


@dataclass(frozen=True, slots=True)
class PictureRecord:
    id: str
    household_id: str
    theme: str
    created_at: float
    # "ok", "low" or "critical": pictures the panel showed about its own battery are kept
    # too, so the history explains itself.
    kind: str = "ok"
    # Which display this went to, as the house names it. Empty when the house cannot say,
    # which is the state of every row written before 1 September 2026.
    display: str = ""
    # What the bytes are. Pictures for a display are 1-bit BMP; a sheet drawn for the
    # printer is a PNG, and serving one as the other gives a parent a broken image.
    media: str = "image/bmp"

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "theme": self.theme,
            "createdAt": self.created_at,
            "kind": self.kind,
            "display": self.display,
            "media": self.media,
        }


def on_other_displays(records: Sequence[PictureRecord], display: str) -> list[str]:
    """The subjects hanging on the other displays right now: the newest row of each.

    Rows that do not name a display say nothing about any of them and are left out, so a
    household whose archive predates this simply has nothing to avoid.
    """
    newest: dict[str, PictureRecord] = {}
    for record in records:
        if record.kind != "ok" or not record.display or record.display == display:
            continue
        held = newest.get(record.display)
        if held is None or record.created_at > held.created_at:
            newest[record.display] = record
    return [record.theme for record in newest.values() if record.theme]


def last_used(records: Sequence[PictureRecord]) -> dict[str, float]:
    """When each subject was last painted, anywhere in the house.

    This is what makes subjects come round in turn, so it only works while every picture
    that reaches a display also reaches the archive: a subject that fails to be recorded
    stays "never used" and is therefore chosen again, and again.
    """
    when: dict[str, float] = {}
    for record in records:
        if record.kind != "ok" or not record.theme:
            continue
        when[record.theme] = max(when.get(record.theme, 0.0), record.created_at)
    return when


def _as_metadata(value: str) -> str:
    """Blob metadata travels as an HTTP header, and a header is latin-1.

    A subject the parent typed with a typographic apostrophe raised UnicodeEncodeError
    inside the storage SDK on 1 September 2026 — after the picture had been generated and
    paid for. Percent-encoding lets the subject keep its punctuation instead of being
    flattened to something the parent did not write.
    """
    return quote(value, safe=" ")


def _from_metadata(value: str) -> str:
    # ASCII rows written before this are unchanged by decoding, so they read back as they
    # were. The one exception is a subject holding a literal % before two hex digits.
    return unquote(value)


@runtime_checkable
class PictureArchive(Protocol):
    def save(self, record: PictureRecord, image: bytes) -> PictureRecord: ...

    def list(self, household_id: str, limit: int = 50) -> list[PictureRecord]: ...

    def page(
        self, household_id: str, *, offset: int, limit: int
    ) -> tuple[list[PictureRecord], int]: ...

    def get(self, household_id: str, picture_id: str) -> tuple[PictureRecord, bytes]: ...


@dataclass
class InMemoryPictureArchive:
    _rows: dict[tuple[str, str], tuple[PictureRecord, bytes]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def save(self, record: PictureRecord, image: bytes) -> PictureRecord:
        with self._lock:
            self._rows[(record.household_id, record.id)] = (record, image)
        return record

    def _newest_first(self, household_id: str) -> list[PictureRecord]:
        with self._lock:
            rows = [
                record
                for (household, _), (record, _image) in self._rows.items()
                if household == household_id
            ]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)

    def list(self, household_id: str, limit: int = 50) -> list[PictureRecord]:
        return self._newest_first(household_id)[:limit]

    def page(
        self, household_id: str, *, offset: int, limit: int
    ) -> tuple[list[PictureRecord], int]:
        rows = self._newest_first(household_id)
        return rows[offset : offset + limit], len(rows)

    def get(self, household_id: str, picture_id: str) -> tuple[PictureRecord, bytes]:
        with self._lock:
            return self._rows[(household_id, picture_id)]


class BlobPictureArchive:
    """Conforms to :class:`PictureArchive`, backed by one container in Blob Storage."""

    def __init__(self, endpoint: str, container: str, credential: Any | None = None) -> None:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient

        self._container = BlobServiceClient(
            account_url=endpoint, credential=credential or DefaultAzureCredential()
        ).get_container_client(container)

    def _name(self, household_id: str, picture_id: str) -> str:
        # Household first, so a prefix listing cannot cross a family boundary.
        return f"{household_id}/{picture_id}.bmp"

    def save(self, record: PictureRecord, image: bytes) -> PictureRecord:
        metadata = {
            "theme": _as_metadata(record.theme),
            "createdAt": str(record.created_at),
            "kind": record.kind,
            "media": record.media,
        }
        # Left out rather than written empty: whether the service takes an empty metadata
        # value has not been measured here, and a refusal would cost the picture itself.
        if record.display:
            metadata["display"] = _as_metadata(record.display)
        self._container.upload_blob(
            name=self._name(record.household_id, record.id),
            data=image,
            overwrite=True,
            metadata=metadata,
            content_type=record.media,
        )
        return record

    def _newest_first(self, household_id: str) -> list[PictureRecord]:
        # Blob listing has no ordering and no count, so the prefix is read whole and
        # sorted here. One household's pictures are the unit, which bounds it.
        rows = [
            _to_record(household_id, blob)
            for blob in self._container.list_blobs(
                name_starts_with=f"{household_id}/", include=["metadata"]
            )
        ]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)

    def list(self, household_id: str, limit: int = 50) -> list[PictureRecord]:
        return self._newest_first(household_id)[:limit]

    def page(
        self, household_id: str, *, offset: int, limit: int
    ) -> tuple[list[PictureRecord], int]:
        rows = self._newest_first(household_id)
        return rows[offset : offset + limit], len(rows)

    def get(self, household_id: str, picture_id: str) -> tuple[PictureRecord, bytes]:
        blob = self._container.get_blob_client(self._name(household_id, picture_id))
        properties = blob.get_blob_properties()
        image = blob.download_blob().readall()
        metadata = properties.metadata or {}
        return (
            PictureRecord(
                id=picture_id,
                household_id=household_id,
                theme=_from_metadata(str(metadata.get("theme") or "")),
                created_at=float(metadata.get("createdAt") or 0.0),
                kind=str(metadata.get("kind") or "ok"),
                display=_from_metadata(str(metadata.get("display") or "")),
            ),
            bytes(image),
        )


def _to_record(household_id: str, blob: Any) -> PictureRecord:
    metadata = getattr(blob, "metadata", None) or {}
    name = str(blob.name).rsplit("/", 1)[-1]
    return PictureRecord(
        id=name[:-4] if name.endswith(".bmp") else name,
        household_id=household_id,
        theme=_from_metadata(str(metadata.get("theme") or "")),
        created_at=float(metadata.get("createdAt") or 0.0),
        kind=str(metadata.get("kind") or "ok"),
        display=_from_metadata(str(metadata.get("display") or "")),
        # A row written before pages were kept here holds a BMP for a display.
        media=str(metadata.get("media") or "image/bmp"),
    )
