"""Read a sheet back: find the markers, flatten the page, and say what ink is where.

The functions here were proven in `tools/check_scan.py` on a real scanned page before they
were a package; this is the same arithmetic in the place the architecture says it belongs.
Nothing writes a file and nothing looks at anything but the quadrilateral the four markers
enclose — if they are not all found the page is refused rather than guessed at.

What comes out describes ink: this cell is dark, this one is not. Whether a mark is the
right one is not decided here and is not decided anywhere.
"""

from __future__ import annotations

import time

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.ids import CellId
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
    SheetSpec,
)
from shared.vision_contracts import CellReading, PageReading, ReadConfidence

# OpenCV returns a marker's corners clockwise from its own top-left, so which of the four
# is the *inner* one depends on which corner of the page the marker sits in.
INNER_CORNER_INDEX = {
    MARKER_ID_TOP_LEFT: 2,
    MARKER_ID_TOP_RIGHT: 3,
    MARKER_ID_BOTTOM_RIGHT: 0,
    MARKER_ID_BOTTOM_LEFT: 1,
}

# Below this fraction of dark pixels a cell is reported empty rather than guessed at. The
# band between the two is where the page is handed to the parent instead.
INK_PRESENT = 0.04
INK_UNCERTAIN = 0.02


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


def page_ink_threshold(rectified: NDArray[np.uint8]) -> int:
    """One threshold for the whole page, computed once.

    Otsu needs a bimodal histogram. The page has one — paper plus printed lines — but an
    empty cell does not, so thresholding a cell on its own splits paper texture down the
    middle and reports scanner noise as ink.
    """
    value, _ = cv2.threshold(rectified, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return int(value)


def ink_fraction(
    rectified: NDArray[np.uint8], box: tuple[int, int, int, int], threshold: int
) -> float | None:
    """Dark fraction strictly inside a cell, or None when the cell is too small to sample.

    The inset is per-axis: derived from the width alone it swallowed the whole height of a
    wide, flat cell, leaving an empty patch that used to be reported as clean.
    """
    x0, y0, x1, y1 = box
    inset_x = max(2, (x1 - x0) // 10)
    inset_y = max(2, (y1 - y0) // 10)
    patch = rectified[y0 + inset_y : y1 - inset_y, x0 + inset_x : x1 - inset_x]
    if patch.size == 0:
        return None
    return float(np.count_nonzero(patch < threshold)) / float(patch.size)


def read_qr(rectified: NDArray[np.uint8]) -> QrPayload:
    """Decode the code that says which sheet this is. Unreadable is refused, not guessed.

    Searched over the whole flattened page rather than at a known rectangle, because where
    the code sits is a property of the sheet and the sheet is what we are trying to learn.
    """
    raw, _, _ = cv2.QRCodeDetector().detectAndDecode(rectified)
    if not raw:
        raise ValueError("no sheet code found on this page")
    return QrPayload.decode(raw)


def read_cells(rectified: NDArray[np.uint8], spec: SheetSpec) -> PageReading:
    """Report the ink in every declared cell, and hand the doubtful ones to the parent."""
    threshold = page_ink_threshold(rectified)
    readings: list[CellReading] = []
    for cell in spec.cells:
        fraction = ink_fraction(rectified, cell.rect.to_pixels(), threshold)
        if fraction is None:
            readings.append(
                CellReading(
                    cell_id=CellId(str(cell.id)),
                    kind=cell.kind,
                    value=None,
                    confidence=ReadConfidence.UNSURE,
                    needs_review=True,
                    note="the cell is too small to sample",
                )
            )
            continue
        if fraction >= INK_PRESENT:
            readings.append(
                CellReading(
                    cell_id=CellId(str(cell.id)),
                    kind=cell.kind,
                    value=cell.label,
                    confidence=ReadConfidence.CERTAIN,
                )
            )
        elif fraction >= INK_UNCERTAIN:
            readings.append(
                CellReading(
                    cell_id=CellId(str(cell.id)),
                    kind=cell.kind,
                    value=None,
                    confidence=ReadConfidence.UNSURE,
                    needs_review=True,
                    note=f"{fraction:.3f} of the cell is dark, between empty and marked",
                )
            )
        else:
            readings.append(
                CellReading(
                    cell_id=CellId(str(cell.id)),
                    kind=cell.kind,
                    value=None,
                    confidence=ReadConfidence.CERTAIN,
                )
            )
    return PageReading(
        sheet_id=spec.sheet_id,
        exercise_id=spec.exercise_id,
        cells=tuple(readings),
        read_at=time.time(),
        degraded=any(reading.needs_review for reading in readings),
    )
