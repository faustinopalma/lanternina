"""What survives of the paper loop when nothing offline reads the page.

A designed sheet is composed, drawn at print resolution, and put back through the two
things the house still does for itself: find the four markers and flatten the page, then
decode the code that says which sheet this is. Both are geometry and identity, not
reading — reading is a model's job and cannot be checked without a network.

The markers are here for the flatbed today and for the camera of `ideas/06 §1` tomorrow.
What this cannot cover is the paper itself — ink bleed, a page lying askew, a printer that
scaled — and none of that belongs in a test.
"""

from __future__ import annotations

import numpy as np
import pytest

from printing.compose import compose
from printing.render import PageGeometry, build_drawing, drawing_to_array
from shared.ids import ExerciseId, SheetId
from shared.pagedesign import PageDesign, TickBox, Words
from shared.sheet import Rect, SheetSpec
from vision.read_sheet import MarkersNotFound, detect_markers, read_qr, rectify

DPI = 300
# Clear of the corner markers' quiet zones: a full-width line at the very top of the frame
# runs through the two upper ones and the renderer refuses it.
DESIGN = PageDesign(
    title="Le stagioni",
    instructions="Barra una scelta per ogni riga.",
    marks=(
        Words(Rect(0.05, 0.07, 0.90, 0.04), "In che stagione cadono le foglie?"),
        TickBox("q1c1", Rect(0.05, 0.14, 0.40, 0.05), label="estate", group="q1"),
        TickBox("q1c2", Rect(0.55, 0.14, 0.40, 0.05), label="autunno", group="q1"),
        Words(Rect(0.05, 0.28, 0.90, 0.04), "Quando fiorisce il ciliegio?"),
        TickBox("q2c1", Rect(0.05, 0.35, 0.40, 0.05), label="primavera", group="q2"),
        TickBox("q2c2", Rect(0.55, 0.35, 0.40, 0.05), label="inverno", group="q2"),
    ),
)


def _spec() -> SheetSpec:
    return compose(
        DESIGN, sheet_id=SheetId("sh_loop"), exercise_id=ExerciseId("ex_loop")
    ).spec


def _printed(spec: SheetSpec) -> np.ndarray:
    return drawing_to_array(build_drawing(spec, PageGeometry()), dpi=DPI)


def test_the_code_on_the_page_says_which_sheet_it_is() -> None:
    spec = _spec()
    page = _printed(spec)

    payload = read_qr(rectify(page, detect_markers(page)))
    assert payload.sheet_id == "sh_loop"
    assert payload.exercise_id == "ex_loop"


def test_a_page_missing_a_marker_is_refused_rather_than_read() -> None:
    """Three corners are enough to warp something. What comes out is not this page."""
    page = _printed(_spec())
    page[:400, :400] = 255  # a thumb over the top-left marker

    with pytest.raises(MarkersNotFound):
        rectify(page, detect_markers(page))


def test_a_stored_sheet_comes_back_the_same() -> None:
    """The page returns days later, so the spec has to survive being written down."""
    spec = _spec()
    again = SheetSpec.from_dict(spec.to_dict())
    assert [c.rect for c in again.cells] == [c.rect for c in spec.cells]
    assert [c.id for c in again.cells] == [c.id for c in spec.cells]
    assert again.title == spec.title
