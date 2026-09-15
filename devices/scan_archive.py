"""Keep acquired scanner pixels independently of activity reading and continuation."""

from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from devices.photo_store import PhotoStore


class ScanStore(PhotoStore):
    image_format = "PNG"
    max_image_bytes = 12_000_000
    initial_state = "done"


def keep_scan(image: NDArray[np.uint8], scanner: str) -> str | None:
    database = os.environ.get("LANTERNINA_SCAN_DATABASE", "")
    if not database:
        return None
    encoded, png = cv2.imencode(".png", image)
    if not encoded:
        raise ValueError("the scan could not be archived")
    scan_id = uuid.uuid4().hex
    ScanStore(Path(database)).accept(
        scan_id, scanner[:64], png.tobytes(), captured=time.time(), target=None,
    )
    return scan_id