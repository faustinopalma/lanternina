"""Invitation and membership records for the separate adolescent portal."""

from __future__ import annotations

import copy
import json
import threading
from collections.abc import Callable
from typing import Any, TypeVar

Result = TypeVar("Result")


class MemoryPortalStore:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {"invitations": {}, "members": {}}
        self._lock = threading.Lock()

    def read(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._data)

    def change(self, operation: Callable[[dict[str, Any]], Result]) -> Result:
        with self._lock:
            updated = copy.deepcopy(self._data)
            result = operation(updated)
            self._data = updated
            return result

    def known_subject(self, subject: str) -> bool:
        return subject in self.read()["members"]


class BlobPortalStore(MemoryPortalStore):
    def __init__(self, container: Any) -> None:
        self.blob = container.get_blob_client("portal/access.json")

    def _load(self) -> tuple[dict[str, Any], str | None]:
        from azure.core.exceptions import ResourceNotFoundError

        try:
            download = self.blob.download_blob()
            return json.loads(download.readall()), download.properties.etag
        except ResourceNotFoundError:
            return {"invitations": {}, "members": {}}, None

    def read(self) -> dict[str, Any]:
        return self._load()[0]

    def change(self, operation: Callable[[dict[str, Any]], Result]) -> Result:
        from azure.core import MatchConditions
        from azure.core.exceptions import ResourceExistsError, ResourceModifiedError

        for _attempt in range(8):
            data, etag = self._load()
            result = operation(data)
            try:
                options = {"etag": etag, "match_condition": MatchConditions.IfNotModified}
                self.blob.upload_blob(
                    json.dumps(data).encode(), overwrite=etag is not None,
                    **(options if etag is not None else {}),
                )
                return result
            except (ResourceExistsError, ResourceModifiedError):
                continue
        raise RuntimeError("portal access changed concurrently")
