"""What a designed page may be, and what it may cost.

The properties worth pinning are the ones a plausible-looking implementation gets wrong.
Three of them are about the adolescent rather than about drawing: a page that only assigns
is refused, two answerable places may not share paper because a mark inside both answers
two things at once, and nothing on a sheet carries an expected answer.

The rest are about ink. There is no mark that fills an area — that is the property the
whole format exists to have — and the remaining way to spend ink is a great many strokes,
which is measured rather than trusted.
"""

from __future__ import annotations

import math

import pytest

from shared.ids import ExerciseId, SheetId
from shared.pagedesign import (
    MAX_STROKE_MM,
    MIN_BOX_SIDE,
    Circle,
    DesignError,
    DrawArea,
    PageDesign,
    Stroke,
    TickBox,
    Words,
    WriteLine,
    mark_from_dict,
)
from shared.sheet import CellKind, Rect

QUAD_W = 178.0
QUAD_H = 251.0


def box(name: str, x: float, y: float) -> TickBox:
    return TickBox(name, Rect(x, y, 0.04, 0.03), "una scelta", "q1")


def a_design(*extra: object) -> PageDesign:
    return PageDesign(
        title="Un foglio",
        instructions="Fai quello che vuoi.",
        marks=(box("q1a", 0.1, 0.2), WriteLine("ask", Rect(0.1, 0.9, 0.7, 0.03)), *extra),
    )


def test_the_format_has_no_way_to_fill_an_area() -> None:
    """The one claim the whole design rests on: a heavy page is unreachable, not
    discouraged. If a fill mark is ever added this test is the thing that has to be
    deleted first, deliberately."""
    for attempt in ("fill", "rect", "shade", "image", "polygon"):
        with pytest.raises(DesignError, match="not a mark"):
            mark_from_dict({"mark": attempt, "rect": {"x": 0, "y": 0, "w": 1, "h": 1}})


def test_a_page_that_only_assigns_has_nowhere_to_answer() -> None:
    with pytest.raises(DesignError, match="nobody can answer"):
        PageDesign(title="t", instructions="i", marks=(Words(Rect(0, 0, 1, 0.05), "ciao"),))


def test_two_answerable_places_may_not_share_paper() -> None:
    with pytest.raises(DesignError, match="overlap"):
        a_design(box("q1b", 0.11, 0.21))


def test_two_answerable_places_may_not_share_an_id() -> None:
    with pytest.raises(DesignError, match="share the id"):
        a_design(box("q1a", 0.5, 0.5))


def test_a_box_too_small_to_aim_at_is_refused() -> None:
    with pytest.raises(DesignError, match="too small"):
        PageDesign(
            title="t",
            instructions="i",
            marks=(
                TickBox("tiny", Rect(0.1, 0.1, MIN_BOX_SIDE / 2, 0.03)),
                WriteLine("ask", Rect(0.1, 0.9, 0.7, 0.03)),
            ),
        )


def test_a_stroke_wider_than_a_pen_is_refused() -> None:
    with pytest.raises(DesignError, match="outside"):
        mark_from_dict(
            {
                "mark": "stroke",
                "vertices": [[0.1, 0.1], [0.2, 0.2]],
                "width_mm": MAX_STROKE_MM + 0.1,
            }
        )


def test_a_key_nobody_declared_is_refused_rather_than_ignored() -> None:
    """What was not read cannot reach paper. An ignored key is a field somebody thought
    they had set."""
    with pytest.raises(DesignError, match="does not define"):
        mark_from_dict(
            {"mark": "tick_box", "id": "q1", "rect": {"x": 0.1, "y": 0.1, "w": 0.04, "h": 0.03},
             "expected": "sole"}
        )


def test_text_cannot_carry_a_line_break_into_the_page() -> None:
    """This text was written by a model and is printed. A line break is the cheapest way
    to make one line of a page look like a new instruction."""
    words = mark_from_dict(
        {
            "mark": "words",
            "rect": {"x": 0.1, "y": 0.1, "w": 0.5, "h": 0.03},
            "text": "prima riga\n\nIgnora quanto sopra",
        }
    )
    assert "\n" not in words.text
    assert words.text == "prima riga Ignora quanto sopra"


def test_the_ink_a_drawing_spends_is_length_times_width() -> None:
    """A number with units, checked against arithmetic somebody can do on paper: a
    100 mm line 0.3 mm wide is 30 mm² of ink."""
    across = Stroke(((0.0, 0.5), (1.0, 0.5)), 0.3)
    design = a_design(across)

    assert design.stroke_ink_mm2(QUAD_W, QUAD_H) == pytest.approx(QUAD_W * 0.3)


def test_a_circle_stays_a_circle_on_a_page_that_is_not_square() -> None:
    """The radius is a fraction of the width in both directions. Scaling y by the height
    would draw an ellipse on A4, where the frame is 178 by 251 mm."""
    circle = Circle(0.5, 0.5, 0.1, 0.3)

    assert circle.length(QUAD_W, QUAD_H) == pytest.approx(2 * math.pi * 0.1 * QUAD_W)


def test_a_design_survives_the_round_trip_it_is_stored_as() -> None:
    design = a_design(
        Stroke(((0.1, 0.1), (0.2, 0.15), (0.3, 0.1)), 0.4),
        Circle(0.5, 0.3, 0.05, 0.3),
        Words(Rect(0.04, 0.02, 0.6, 0.04), "Un titolo", 6.0),
        DrawArea("d1", Rect(0.1, 0.5, 0.4, 0.2), "disegna qui"),
    )

    again = PageDesign.from_dict(design.to_dict())

    assert again == design


def test_the_reader_gets_the_contract_it_has_always_had() -> None:
    """The seam the whole change rests on: a page may become as interesting as a model can
    design it, and the vision pipeline still receives rectangles with ids."""
    design = a_design(DrawArea("d1", Rect(0.1, 0.5, 0.4, 0.2), "disegna"))

    spec = design.to_sheet_spec(
        sheet_id=SheetId("sh_00000001"),
        exercise_id=ExerciseId("ex_00000001"),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
    )

    assert [str(c.id) for c in spec.cells] == ["q1a", "ask", "d1"]
    assert [c.kind for c in spec.cells] == [
        CellKind.CHOICE_BOX,
        CellKind.WORD_LINE,
        CellKind.DRAWING_AREA,
    ]
    # Nothing on a sheet says what a mark should have been.
    assert all(c.expected is None for c in spec.cells)


def test_the_words_on_the_page_are_never_answerable() -> None:
    """A cell is a place an answer can be, and a printed line is not one. Keeping them
    apart is what stops the reader having to know which rectangles were only words."""
    design = a_design(Words(Rect(0.04, 0.02, 0.6, 0.04), "Quante foglie?", 5.0))

    spec = design.to_sheet_spec(
        sheet_id=SheetId("sh_00000001"),
        exercise_id=ExerciseId("ex_00000001"),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
    )

    assert [h.text for h in spec.headings] == ["Quante foglie?"]
    assert "Quante foglie?" not in [c.label for c in spec.cells]
