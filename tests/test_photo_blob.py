from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest
from azure.core import MatchConditions
from azure.core.exceptions import ResourceExistsError, ResourceModifiedError

from panel.photos import BlobPhotoArchive, Photo, from_metadata, metadata


class Blob:
    def __init__(self):
        self.metadata = None
        self.data = b""
        self.etag = 0
        self.race = False

    def upload_blob(self, data, *, overwrite, metadata, **kwargs):
        if self.metadata is not None and not overwrite:
            raise ResourceExistsError("exists")
        if overwrite:
            assert kwargs["match_condition"] == MatchConditions.IfNotModified
            if kwargs["etag"] != self.etag:
                raise ResourceModifiedError("changed")
        self.metadata, self.data = metadata, data
        self.etag += 1

    def get_blob_properties(self):
        return SimpleNamespace(metadata=self.metadata, etag=self.etag)

    def set_blob_metadata(self, values, **kwargs):
        assert kwargs["match_condition"] == MatchConditions.IfNotModified
        if self.race:
            self.metadata = metadata(replace(from_metadata(self.metadata), deleted=True))
            self.data = b""
            self.etag += 1
            self.race = False
        if kwargs["etag"] != self.etag:
            raise ResourceModifiedError("changed")
        self.metadata = values
        self.etag += 1


def test_blob_delete_wins_over_concurrent_processing_status_update():
    blob = Blob()
    archive = object.__new__(BlobPhotoArchive)
    archive.container = SimpleNamespace(get_blob_client=lambda _: blob)
    photo = Photo("a"*32, "camera", 100, 101, 1600, 1200, "pending", "digest")
    archive.save("family", photo, b"jpeg")
    blob.race = True
    result = archive.save("family", replace(photo, state="done"), b"jpeg")
    assert result.deleted
    assert blob.data == b""
    with pytest.raises(KeyError):
        archive.get("family", photo.id)
    assert archive.save("family", photo, b"jpeg").deleted


def test_blob_delete_replaces_bytes_with_tombstone_in_one_conditional_write():
    blob = Blob()
    archive = object.__new__(BlobPhotoArchive)
    archive.container = SimpleNamespace(get_blob_client=lambda _: blob)
    photo = Photo("a"*32, "camera", None, 101, 1600, 1200, "done", "digest")
    archive.save("family", photo, b"jpeg")
    archive.delete("family", photo.id)
    assert blob.data == b""
    assert from_metadata(blob.metadata).deleted
    archive.delete("family", photo.id)