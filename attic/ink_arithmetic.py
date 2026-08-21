"""Read a sheet by counting dark pixels inside the rectangles a template declared.

Retired 21 August 2026. It was the reader of the paper loop until 19 August, then the
answer the house gave when the cloud could not be reached, and now neither. `attic/README`
holds why; the short version is that it can only read a page made of boxes in known
places, and that shape is what the sheet stopped being.

What it did well is worth keeping in view: it needed no network, it described ink and
never a person, and it handed anything doubtful to the parent instead of choosing. What it
could not do is read a light pencil mark, and no threshold fixes that.

The two constants below are measured, not chosen. On 19 August 2026 the first pair
reported four ticked boxes as empty — with `ReadConfidence.CERTAIN`, which the reading
contract forbids. Three sheets marked by hand in pen then measured 0.0121 to 0.0196 of the
cell dark, and an empty cell measured exactly 0.0000: the 10% inset per side keeps the
printed border out of the sample, so there is no noise floor to clear.
"""

from __future__ import annotations

import time

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.ids import CellId
from shared.sheet import SheetSpec
from shared.vision_contracts import CellReading, PageReading, ReadConfidence

INK_PRESENT = 0.010
INK_UNCERTAIN = 0.003


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
