"""The archive of pictures a display has shown, and the way to put one back.

Blobs rather than the database: a picture is 48 KB of bitmap, which is the wrong shape for
a document store and the right shape for object storage. What is kept is the **rendered**
1-bit image, not the model's original — the record is of what she actually saw.

The storage account refuses public access and shared keys, both forced by tenant policy,
so this reaches it over a private endpoint with the container's managed identity. That is
also why the archive is written through the panel: the server in the home cannot see the
storage account, and should not have a key that would let it.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class PictureRecord:
    id: str
    household_id: str
    theme: str
    created_at: float
    # "ok", "low" or "critical": pictures the panel showed about its own battery are kept
    # too, so the history explains itself.
    kind: str = "ok"

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "theme": self.theme,
            "createdAt": self.created_at,
            "kind": self.kind,
        }


@runtime_checkable
class PictureArchive(Protocol):
    def save(self, record: PictureRecord, image: bytes) -> PictureRecord: ...

    def list(self, household_id: str, limit: int = 50) -> list[PictureRecord]: ...

    def get(self, household_id: str, picture_id: str) -> tuple[PictureRecord, bytes]: ...


@dataclass
class InMemoryPictureArchive:
    _rows: dict[tuple[str, str], tuple[PictureRecord, bytes]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def save(self, record: PictureRecord, image: bytes) -> PictureRecord:
        with self._lock:
            self._rows[(record.household_id, record.id)] = (record, image)
        return record

    def list(self, household_id: str, limit: int = 50) -> list[PictureRecord]:
        with self._lock:
            rows = [
                record
                for (household, _), (record, _image) in self._rows.items()
                if household == household_id
            ]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)[:limit]

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
        self._container.upload_blob(
            name=self._name(record.household_id, record.id),
            data=image,
            overwrite=True,
            metadata={
                "theme": record.theme,
                "createdAt": str(record.created_at),
                "kind": record.kind,
            },
            content_type="image/bmp",
        )
        return record

    def list(self, household_id: str, limit: int = 50) -> list[PictureRecord]:
        rows = [
            _to_record(household_id, blob)
            for blob in self._container.list_blobs(
                name_starts_with=f"{household_id}/", include=["metadata"]
            )
        ]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)[:limit]

    def get(self, household_id: str, picture_id: str) -> tuple[PictureRecord, bytes]:
        blob = self._container.get_blob_client(self._name(household_id, picture_id))
        properties = blob.get_blob_properties()
        image = blob.download_blob().readall()
        metadata = properties.metadata or {}
        return (
            PictureRecord(
                id=picture_id,
                household_id=household_id,
                theme=str(metadata.get("theme") or ""),
                created_at=float(metadata.get("createdAt") or 0.0),
                kind=str(metadata.get("kind") or "ok"),
            ),
            bytes(image),
        )


def _to_record(household_id: str, blob: Any) -> PictureRecord:
    metadata = getattr(blob, "metadata", None) or {}
    name = str(blob.name).rsplit("/", 1)[-1]
    return PictureRecord(
        id=name[:-4] if name.endswith(".bmp") else name,
        household_id=household_id,
        theme=str(metadata.get("theme") or ""),
        created_at=float(metadata.get("createdAt") or 0.0),
        kind=str(metadata.get("kind") or "ok"),
    )
