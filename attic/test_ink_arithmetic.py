"""The paper loop as it was read without a network, kept with the arithmetic it tested.

Retired 21 August 2026. Run from the repository root with `pytest attic`; the ordinary run
does not collect it.

The sheet is laid out, drawn at print resolution, marked in one box, and read back through
the path a scanned page took: find the markers, flatten, look at every declared cell. It
was the only test that could fail when the layout and the reader disagreed about where a
box is, and that guarantee went with them — a model reading a page cannot be checked
offline, which is part of what "no cloud, no reading" costs.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ink_arithmetic import read_cells  # noqa: E402
from layout import sheet_for  # noqa: E402

from printing.render import PageGeometry, build_drawing, drawing_to_array  # noqa: E402
from shared.ids import ExerciseId, SheetId  # noqa: E402
from shared.sheet import SheetSpec  # noqa: E402
from vision.read_sheet import detect_markers, rectify  # noqa: E402

DPI = 300
BODY = {
    "title": "Le stagioni",
    "instructions": "Barra una scelta per ogni riga.",
    "exercises": [
        {"question": "In che stagione cadono le foglie?", "choices": ["estate", "autunno"]},
        {"question": "Quando fiorisce il ciliegio?", "choices": ["primavera", "inverno"]},
    ],
}


def _printed(spec: SheetSpec) -> np.ndarray:
    return drawing_to_array(build_drawing(spec, PageGeometry()), dpi=DPI)


def _mark(page: np.ndarray, spec: SheetSpec, cell_id: str) -> np.ndarray:
    """Scribble inside one box, the way a pencil would."""
    geometry = PageGeometry()
    area = geometry.to_page(spec.cell(cell_id).rect)  # type: ignore[arg-type]
    scale = DPI / 25.4
    x0, y0 = round(area.x * scale), round(area.y * scale)
    x1, y1 = round(area.right * scale), round(area.bottom * scale)
    inset_x, inset_y = (x1 - x0) // 4, (y1 - y0) // 4
    marked = page.copy()
    marked[y0 + inset_y : y1 - inset_y, x0 + inset_x : x1 - inset_x] = 0
    return marked


def test_a_marked_box_is_read_as_marked_and_the_others_are_not() -> None:
    spec = sheet_for(BODY, sheet_id=SheetId("sh_loop"), exercise_id=ExerciseId("ex_loop"))
    page = _mark(_printed(spec), spec, "q1c2")

    flat = rectify(page, detect_markers(page))
    reading = read_cells(flat, spec)

    marked = {str(cell.cell_id) for cell in reading.cells if cell.value}
    assert marked == {"q1c2"}, "the mark landed in a box the reader does not look at"
    assert not reading.degraded, "a clean page should need nobody to look at it"
