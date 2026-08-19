"""The paper loop, without the paper.

The sheet is laid out, drawn at print resolution, marked in one box, and read back through
the same path a scanned page takes: find the markers, flatten, decode the code, look at
every declared cell. It is the only test that can fail when the layout and the reader
disagree about where a box is, which is the failure that would otherwise show up as an
answer attributed to the wrong question.

What it cannot cover is the paper itself — ink bleed, a page lying askew, a printer that
scaled. The ruler on the sheet and a real scan cover those, and neither belongs in a test.
"""

from __future__ import annotations

import numpy as np
import pytest

from printing.layout import sheet_for
from printing.render import PageGeometry, build_drawing, drawing_to_array
from shared.ids import ExerciseId, SheetId
from shared.sheet import SheetSpec
from vision.read_sheet import (
    MarkersNotFound,
    detect_markers,
    read_cells,
    read_qr,
    rectify,
)

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


def test_the_code_on_the_page_says_which_sheet_it_is() -> None:
    spec = sheet_for(BODY, sheet_id=SheetId("sh_loop"), exercise_id=ExerciseId("ex_loop"))
    page = _printed(spec)

    payload = read_qr(rectify(page, detect_markers(page)))
    assert payload.sheet_id == "sh_loop"
    assert payload.exercise_id == "ex_loop"


def test_a_page_missing_a_marker_is_refused_rather_than_read() -> None:
    """Three corners are enough to warp something. What comes out is not this page."""
    spec = sheet_for(BODY, sheet_id=SheetId("sh_loop"), exercise_id=ExerciseId("ex_loop"))
    page = _printed(spec)
    page[:400, :400] = 255  # a thumb over the top-left marker

    with pytest.raises(MarkersNotFound):
        rectify(page, detect_markers(page))


def test_a_stored_sheet_comes_back_the_same() -> None:
    """The page returns days later, so the spec has to survive being written down."""
    spec = sheet_for(BODY, sheet_id=SheetId("sh_loop"), exercise_id=ExerciseId("ex_loop"))
    again = SheetSpec.from_dict(spec.to_dict())
    assert [c.rect for c in again.cells] == [c.rect for c in spec.cells]
    assert [c.id for c in again.cells] == [c.id for c in spec.cells]
    assert again.title == spec.title
