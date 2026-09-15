"""Scanner originals share archive guarantees, with a separate storage namespace."""

from __future__ import annotations

from panel.photos import BlobPhotoArchive


class BlobScanArchive(BlobPhotoArchive):
    namespace = "scans"
    media_type = "image/png"