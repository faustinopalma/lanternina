"""Read a scanned or photographed sheet back and report what was actually found.

This is the measuring instrument for the print-and-scan loop: it answers whether ink on
real paper still yields four markers, a decodable QR, and cell rectangles that land where
the spec says they do.

    python -m tools.check_scan build/scan.png

Everything it prints describes marks on paper. A cell is reported as covered or empty;
nothing here decides whether an answer is right, and nothing describes the person who
wrote it. Only the rectified page is written out — the region inside the marker quad.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.sheet import (
    ARUCO_DICT_NAME,
    LOCALLY_READABLE,
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

# Corners come back clockwise from each marker's own top-left, so the corner facing the
# centre of the page sits at a different index for each of the four.
INNER_CORNER_INDEX = {
    MARKER_ID_TOP_LEFT: 2,
    MARKER_ID_TOP_RIGHT: 3,
    MARKER_ID_BOTTOM_RIGHT: 0,
    MARKER_ID_BOTTOM_LEFT: 1,
}

# Below this fraction of dark pixels a cell is reported empty rather than guessed at.
INK_PRESENT = 0.04
INK_UNCERTAIN = 0.02


def detect_markers(image: NDArray[np.uint8]) -> dict[int, NDArray[np.float32]]:
    dictionary = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, ARUCO_DICT_NAME))
    detector = cv2.aruco.ArucoDetector(dictionary, cv2.aruco.DetectorParameters())
    corners, ids, _ = detector.detectMarkers(image)
    if ids is None:
        return {}
    return {int(i): c.reshape(4, 2) for c, i in zip(corners, ids.flatten(), strict=True)}


def rectify(image: NDArray[np.uint8], found: dict[int, NDArray[np.float32]]) -> NDArray[np.uint8]:
    """Warp the marker quadrilateral onto the fixed canvas the spec's coordinates assume."""
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
    return cv2.warpPerspective(image, matrix, (RECTIFIED_WIDTH, RECTIFIED_HEIGHT))


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


def report(image_path: Path, spec: SheetSpec | None, out_path: Path | None) -> int:
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"cannot read {image_path}")
        return 2
    print(f"scan: {image.shape[1]}x{image.shape[0]} px")

    found = detect_markers(image)
    missing = [i for i in REQUIRED_MARKER_IDS if i not in found]
    print(f"markers found: {sorted(found)}" + (f"  MISSING {missing}" if missing else ""))
    if missing:
        print("cannot rectify without all four markers; refusing to guess the page outline")
        return 1

    for marker_id in REQUIRED_MARKER_IDS:
        points = found[marker_id]
        side = float(np.linalg.norm(points[0] - points[1]))
        print(f"  marker {marker_id}: side {side:6.1f} px")

    decoded, _, _ = cv2.QRCodeDetector().detectAndDecode(image)
    if decoded:
        try:
            payload = QrPayload.decode(decoded)
            print(f"QR: sheet={payload.sheet_id} exercise={payload.exercise_id} "
                  f"spec_version={payload.spec_version}")
        except ValueError as exc:
            print(f"QR decoded but not ours: {exc}")
    else:
        print("QR: not decoded")

    rectified = rectify(image, found)
    if out_path is not None:
        cv2.imwrite(str(out_path), rectified)
        print(f"rectified page written to {out_path}")

    if spec is not None:
        threshold = page_ink_threshold(rectified)
        print(f"cells (marks on paper, not judgements) — page threshold {threshold}:")
        for cell in spec.cells:
            box = cell.rect.to_pixels(RECTIFIED_WIDTH, RECTIFIED_HEIGHT)
            fraction = ink_fraction(rectified, box, threshold)
            if fraction is None:
                print(f"  {cell.id:<12} {cell.kind:<12}    n/a  cannot sample this cell")
                continue
            if cell.kind not in LOCALLY_READABLE:
                state = "needs review (not locally readable)"
            elif fraction >= INK_PRESENT:
                state = "covered"
            elif fraction <= INK_UNCERTAIN:
                state = "empty"
            else:
                state = "needs review (between thresholds)"
            print(f"  {cell.id:<12} {cell.kind:<12} ink {fraction:5.1%}  {state}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan", type=Path)
    parser.add_argument("--rectified", type=Path, default=None)
    parser.add_argument("--no-cells", action="store_true", help="skip the cell report")
    args = parser.parse_args()

    spec = None
    if not args.no_cells:
        from printing.render import PageGeometry
        from tools.make_test_sheet import DEFAULT_EXERCISE_ID, DEFAULT_SHEET_ID, build_test_spec

        spec = build_test_spec(PageGeometry(), DEFAULT_SHEET_ID, DEFAULT_EXERCISE_ID)
    return report(args.scan, spec, args.rectified)


if __name__ == "__main__":
    raise SystemExit(main())
