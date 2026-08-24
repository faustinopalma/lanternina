"""From a design to paper: what gets refused, and what the reader is handed.

The claims here are the ones that only appear once millimetres are involved. A design is
paper-independent and a page is not, so this is where a drawing can be too heavy, a mark
can land in a marker's quiet zone, and a line to write on stops being a box.
"""

from __future__ import annotations

import pytest

from printing.compose import InkTooHeavy, compose, ink_coverage
from printing.render import Drawing, PageGeometry, SheetLayoutError, StrokePath
from shared.ids import ExerciseId, SheetId
from shared.pagedesign import PageDesign, Stroke, TickBox, WriteLine
from shared.sheet import Rect

PAGE = PageGeometry()
QUAD = PAGE.quad
AREA = PAGE.width_mm * PAGE.height_mm


def a_design(*extra: object) -> PageDesign:
    return PageDesign(
        title="Un foglio",
        instructions="Fai quello che vuoi.",
        marks=(
            TickBox("q1a", Rect(0.1, 0.2, 0.04, 0.03), "sole", "q1"),
            WriteLine("ask", Rect(0.1, 0.9, 0.7, 0.03)),
            *extra,
        ),
    )


def composed(design: PageDesign, **kwargs: object) -> object:
    return compose(
        design,
        sheet_id=SheetId("sh_00000001"),
        exercise_id=ExerciseId("ex_00000001"),
        page=PAGE,
        **kwargs,  # type: ignore[arg-type]
    )


def test_a_drawing_over_the_budget_is_refused_before_it_is_rendered() -> None:
    """The refusal says what was spent against what was allowed, because the caller's next
    move is to ask for a lighter page and it has to be able to say by how much."""
    heavy = tuple(
        Stroke(((0.0, y / 200), (1.0, y / 200)), 0.6) for y in range(1, 60)
    )
    with pytest.raises(InkTooHeavy, match="allowed"):
        composed(a_design(*heavy))


def test_the_budget_is_the_physical_figure_and_not_the_raster() -> None:
    """A budget that moved with the resolution somebody rendered at would not be a budget.
    Measured, 20 August 2026: rounding a stroke width to whole pixels moves the rasterised
    figure to between 0.85 and 1.70 times the arithmetic one."""
    across = Stroke(((0.0, 0.5), (1.0, 0.5)), 0.3)
    sheet = composed(a_design(across))

    assert sheet.stroke_ink_mm2 == pytest.approx(QUAD.w * 0.3)

    only_the_stroke = Drawing(
        PAGE, (), (), (), (), (StrokePath(((QUAD.x, 100.0), (QUAD.x + QUAD.w, 100.0)), 0.3),)
    )
    rastered = ink_coverage(only_the_stroke) * AREA
    assert 0.85 <= rastered / sheet.stroke_ink_mm2 <= 1.70


def test_a_line_to_write_on_is_a_rule_and_not_a_box() -> None:
    """Three sides of ink saved on every one, and it looks like somewhere to write rather
    than a field on a form."""
    sheet = composed(a_design())

    assert len(sheet.drawing.outlined) == 1  # the tick box, and nothing else
    assert any(len(s.vertices) == 2 for s in sheet.drawing.strokes)


def test_a_mark_in_a_marker_quiet_zone_is_refused() -> None:
    """Rectification drifts without failing loudly when a corner is obstructed, so this is
    caught while it is still an object rather than after a scan."""
    with pytest.raises(SheetLayoutError, match="quiet zone"):
        composed(a_design(Stroke(((0.0, 0.0), (0.02, 0.01)), 0.3)))


def test_the_sheet_that_comes_out_is_the_one_the_reader_reads() -> None:
    sheet = composed(a_design())

    assert [str(c.id) for c in sheet.spec.cells] == ["q1a", "ask"]
    assert sheet.spec.title == "Un foglio"
    assert sheet.spec.qr_rect.x > 0.5  # the top-right corner, below the marker


def test_a_designed_sheet_is_lighter_than_the_form_it_replaces() -> None:
    """Measured on the sheet this format replaces: four markers, a QR, the ruler and
    sixteen tick boxes is 2.78% of an A4 page. A designed page with a drawing on it has to
    come in under that, or the whole frugality claim is decoration."""
    drawing = tuple(
        Stroke(((0.15 + i * 0.01, 0.30), (0.18 + i * 0.01, 0.36), (0.15 + i * 0.01, 0.42)), 0.3)
        for i in range(12)
    )
    sheet = composed(a_design(*drawing))

    assert sheet.coverage < 0.0278


def test_the_scaffold_is_what_every_sheet_pays() -> None:
    """940 mm² of markers, QR and ruler, measured. Worth pinning because it is the floor
    every budget is set above, and it moves if a marker size changes."""
    sheet = composed(a_design())
    bare = Drawing(PAGE, sheet.drawing.filled, (), (), (), ())

    assert ink_coverage(bare) * AREA == pytest.approx(940.0, abs=15.0)
