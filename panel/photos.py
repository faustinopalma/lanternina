"""Family photographs, stored separately from generated pictures."""

from __future__ import annotations

import hashlib
import threading
from dataclasses import asdict, dataclass, replace
from typing import Any, Protocol


@dataclass(frozen=True)
class Photo:
    id: str
    camera: str
    capturedAt: float | None
    receivedAt: float
    width: int
    height: int
    state: str
    digest: str
    deleted: bool = False

    @property
    def date(self) -> float:
        return self.capturedAt if self.capturedAt is not None else self.receivedAt

    def public(self) -> dict[str, Any]:
        return {**asdict(self), "date": self.date}


class PhotoArchive(Protocol):
    def save(self, household: str, record: Photo, image: bytes) -> Photo: ...
    def list(self, household: str) -> list[Photo]: ...
    def get(self, household: str, photo_id: str) -> bytes: ...
    def delete(self, household: str, photo_id: str) -> None: ...
    def report(self, household: str, status: dict[str, Any]) -> None: ...
    def status(self, household: str) -> dict[str, Any] | None: ...


class MemoryPhotoArchive:
    def __init__(self) -> None:
        self.rows: dict[tuple[str, str], tuple[Photo, bytes]] = {}
        self.lock = threading.Lock()
        self.reports: dict[str, dict[str, Any]] = {}

    def report(self, household: str, status: dict[str, Any]) -> None:
        with self.lock:
            self.reports[household] = status

    def status(self, household: str) -> dict[str, Any] | None:
        with self.lock:
            return self.reports.get(household)

    def save(self, household: str, record: Photo, image: bytes) -> Photo:
        with self.lock:
            key = household, record.id
            old = self.rows.get(key)
            if old:
                if old[0].digest != record.digest or old[0].camera != record.camera:
                    raise ValueError("conflicting photograph")
                record = replace(old[0], state=record.state) if not old[0].deleted else old[0]
            self.rows[key] = record, b"" if record.deleted else image
            return record

    def list(self, household: str) -> list[Photo]:
        with self.lock:
            return [record for (family, _), (record, _) in self.rows.items() if family == household]

    def get(self, household: str, photo_id: str) -> bytes:
        with self.lock:
            record, image = self.rows[household, photo_id]
            if record.deleted:
                raise KeyError(photo_id)
            return image

    def delete(self, household: str, photo_id: str) -> None:
        with self.lock:
            old = self.rows.get((household, photo_id))
            if old:
                self.rows[household, photo_id] = replace(old[0], deleted=True), b""


def metadata(record: Photo) -> dict[str, str]:
    import json

    return {"record": json.dumps(asdict(record), ensure_ascii=True)}


def from_metadata(values: dict[str, str]) -> Photo:
    import json

    return Photo(**json.loads(values["record"]))


class BlobPhotoArchive:
    def __init__(self, endpoint: str, container: str) -> None:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient

        self.container = BlobServiceClient(
            endpoint,
            credential=DefaultAzureCredential(),
            connection_timeout=10,
            read_timeout=30,
        ).get_container_client(container)

    def prefix(self, household: str) -> str:
        return "camera/" + hashlib.sha256(household.encode()).hexdigest() + "/"

    def report(self, household: str, status: dict[str, Any]) -> None:
        import json

        self.container.upload_blob(
            name=self.prefix(household).rstrip("/") + ".status",
            data=json.dumps(status).encode(),
            overwrite=True,
        )

    def status(self, household: str) -> dict[str, Any] | None:
        import json

        from azure.core.exceptions import ResourceNotFoundError

        try:
            return json.loads(
                self.container.get_blob_client(self.prefix(household).rstrip("/") + ".status")
                .download_blob()
                .readall()
            )
        except ResourceNotFoundError:
            return None

    def save(self, household: str, record: Photo, image: bytes) -> Photo:
        from azure.core import MatchConditions
        from azure.core.exceptions import ResourceExistsError, ResourceModifiedError
        from azure.storage.blob import ContentSettings

        blob = self.container.get_blob_client(self.prefix(household) + record.id)
        try:
            blob.upload_blob(
                image,
                overwrite=False,
                metadata=metadata(record),
                content_settings=ContentSettings(content_type="image/jpeg"),
            )
            return record
        except ResourceExistsError:
            pass
        for _attempt in range(4):
            properties = blob.get_blob_properties()
            old = from_metadata(properties.metadata)
            if old.digest != record.digest or old.camera != record.camera:
                raise ValueError("conflicting photograph")
            if old.deleted or old.state == record.state:
                return old
            updated = replace(old, state=record.state)
            try:
                blob.set_blob_metadata(
                    metadata(updated),
                    etag=properties.etag,
                    match_condition=MatchConditions.IfNotModified,
                )
                return updated
            except ResourceModifiedError:
                continue
        raise RuntimeError("photograph changed concurrently")

    def list(self, household: str) -> list[Photo]:
        return [
            from_metadata(blob.metadata)
            for blob in self.container.list_blobs(
                name_starts_with=self.prefix(household), include=["metadata"]
            )
        ]

    def get(self, household: str, photo_id: str) -> bytes:
        from azure.core import MatchConditions
        from azure.core.exceptions import ResourceNotFoundError

        blob = self.container.get_blob_client(self.prefix(household) + photo_id)
        try:
            properties = blob.get_blob_properties()
            if from_metadata(properties.metadata).deleted:
                raise KeyError(photo_id)
            return bytes(
                blob.download_blob(
                    etag=properties.etag, match_condition=MatchConditions.IfNotModified
                ).readall()
            )
        except ResourceNotFoundError as exc:
            raise KeyError(photo_id) from exc

    def delete(self, household: str, photo_id: str) -> None:
        from azure.core import MatchConditions
        from azure.core.exceptions import ResourceModifiedError, ResourceNotFoundError

        blob = self.container.get_blob_client(self.prefix(household) + photo_id)
        for _attempt in range(4):
            try:
                properties = blob.get_blob_properties()
                record = from_metadata(properties.metadata)
                if record.deleted:
                    return
                blob.upload_blob(
                    b"",
                    overwrite=True,
                    metadata=metadata(replace(record, deleted=True)),
                    etag=properties.etag,
                    match_condition=MatchConditions.IfNotModified,
                )
                return
            except ResourceNotFoundError:
                return
            except ResourceModifiedError:
                continue
        raise RuntimeError("photograph changed concurrently")
