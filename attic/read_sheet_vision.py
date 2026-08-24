"""Find the four markers on a page, flatten it, and say which sheet it is.

The functions here were proven in `tools/check_scan.py` on a real scanned page before they
were a package; this is the same arithmetic in the place the architecture says it belongs.
Nothing writes a file and nothing looks at anything but the quadrilateral the four markers
enclose — if they are not all found the page is refused rather than guessed at.

What used to be here as well, and is not any more: the arithmetic that counted dark pixels
inside a declared rectangle and called the result a reading. It went to `attic/` on
21 August 2026 with the template that drew those rectangles. Reading a page is a model's
job now, and the consequence is stated rather than worked around — no cloud, no reading.

The markers stay, and not out of sentiment. A flatbed hands back a flat image at a known
scale and needs no help; a camera does not, and `ideas/06 §1` is where four corners in a
photograph earn their keep.
"""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.sheet import (
    ARUCO_DICT_NAME,
    MARKER_ID_BOTTOM_LEFT,
    MARKER_ID_BOTTOM_RIGHT,
    MARKER_ID_TOP_LEFT,
    MARKER_ID_TOP_RIGHT,
    RECTIFIED_HEIGHT,
    RECTIFIED_WIDTH,
    REQUIRED_MARKER_IDS,
    QrPayload,
)

# OpenCV returns a marker's corners clockwise from its own top-left, so which of the four
# is the *inner* one depends on which corner of the page the marker sits in.
INNER_CORNER_INDEX = {
    MARKER_ID_TOP_LEFT: 2,
    MARKER_ID_TOP_RIGHT: 3,
    MARKER_ID_BOTTOM_RIGHT: 0,
    MARKER_ID_BOTTOM_LEFT: 1,
}


class MarkersNotFound(ValueError):
    """Fewer than four markers. The page is refused rather than partially trusted."""


def detect_markers(image: NDArray[np.uint8]) -> dict[int, NDArray[np.float32]]:
    dictionary = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, ARUCO_DICT_NAME))
    detector = cv2.aruco.ArucoDetector(dictionary, cv2.aruco.DetectorParameters())
    corners, ids, _ = detector.detectMarkers(image)
    if ids is None:
        return {}
    return {int(i): c.reshape(4, 2) for c, i in zip(corners, ids.flatten(), strict=True)}


def rectify(image: NDArray[np.uint8], found: dict[int, NDArray[np.float32]]) -> NDArray[np.uint8]:
    """Warp the marker quadrilateral onto the fixed canvas the spec's coordinates assume."""
    missing = [marker for marker in REQUIRED_MARKER_IDS if marker not in found]
    if missing:
        raise MarkersNotFound(f"markers {missing} are not on this page")
    source = np.array(
        [found[i][INNER_CORNER_INDEX[i]] for i in REQUIRED_MARKER_IDS], dtype=np.float32
    )
    target = np.array(
        [
            [0, 0],
            [RECTIFIED_WIDTH, 0],
            [RECTIFIED_WIDTH, RECTIFIED_HEIGHT],
            [0, RECTIFIED_HEIGHT],
        ],
        dtype=np.float32,
    )
    matrix = cv2.getPerspectiveTransform(source, target)
    warped = cv2.warpPerspective(image, matrix, (RECTIFIED_WIDTH, RECTIFIED_HEIGHT))
    return np.asarray(warped, dtype=np.uint8)


def read_qr(rectified: NDArray[np.uint8]) -> QrPayload:
    """Decode the code that says which sheet this is. Unreadable is refused, not guessed.

    Searched over the whole flattened page rather than at a known rectangle, because where
    the code sits is a property of the sheet and the sheet is what we are trying to learn.
    """
    raw, _, _ = cv2.QRCodeDetector().detectAndDecode(rectified)
    if not raw:
        raise ValueError("no sheet code found on this page")
    return QrPayload.decode(raw)
