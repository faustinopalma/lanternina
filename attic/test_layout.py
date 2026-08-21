"""Where a box lands on the sheet, and whether the reader will find it there.

Retired 21 August 2026 with the module it tests. Run from the repository root with
`pytest attic`; the ordinary run does not collect it.

The renderer already refuses a layout that would sit in a marker's quiet zone. What it
cannot see is the weaker thing that matters just as much: that two boxes never overlap,
because a mark inside an overlap belongs to two questions at once and there is no honest
way to attribute it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from layout import MAX_QUESTIONS, SheetTooFull, sheet_for  # noqa: E402

from printing.render import PageGeometry, build_drawing, drawing_to_svg  # noqa: E402
from shared.ids import ExerciseId, SheetId  # noqa: E402
from shared.sheet import CellKind  # noqa: E402

BODY = {
    "title": "Le stagioni",
    "instructions": "Barra una scelta per ogni riga.",
    "exercises": [
        {"question": "In che stagione cadono le foglie?", "choices": ["estate", "autunno"]},
        {"question": "Quando fiorisce il ciliegio?", "choices": ["primavera", "inverno"]},
    ],
}


def _sheet(body: dict[str, object] = BODY):  # type: ignore[no-untyped-def]
    return sheet_for(body, sheet_id=SheetId("sh_1"), exercise_id=ExerciseId("ex_1"))


def test_every_choice_becomes_a_box_the_reader_can_read_offline() -> None:
    sheet = _sheet()
    assert [cell.kind for cell in sheet.cells] == [CellKind.CHOICE_BOX] * 4
    assert [cell.label for cell in sheet.cells] == [
        "estate",
        "autunno",
        "primavera",
        "inverno",
    ]
    # One group per question, so a mark can be attributed to the question it answers.
    assert {cell.group for cell in sheet.cells} == {"q1", "q2"}


def test_no_two_boxes_overlap() -> None:
    boxes = [cell.rect for cell in _sheet().cells]
    for first in range(len(boxes)):
        for second in range(first + 1, len(boxes)):
            a, b = boxes[first], boxes[second]
            apart = (
                b.x >= a.x + a.w
                or b.x + b.w <= a.x
                or b.y >= a.y + a.h
                or b.y + b.h <= a.y
            )
            assert apart, f"{a} and {b} overlap: a mark there answers two questions"


def test_the_sheet_draws_without_obstructing_a_marker() -> None:
    """The QR and every box have to clear the quiet zones, or rectification drifts."""
    drawing = build_drawing(_sheet(), PageGeometry())
    svg = drawing_to_svg(drawing)
    assert svg.startswith("<?xml")
    assert "Le stagioni" in svg
    assert "In che stagione cadono le foglie?" in svg
    assert "estate" in svg
    # The ruler is what tells the parent the printer did not scale the page.
    assert "50 mm" in svg


def test_the_words_are_headings_and_never_cells() -> None:
    """A cell is a place an answer can be. The question is not one."""
    sheet = _sheet()
    printed = " ".join(heading.text for heading in sheet.headings)
    assert "Le stagioni" in printed
    assert "1. In che stagione cadono le foglie?" in printed
    assert all(cell.label in {"estate", "autunno", "primavera", "inverno"} for cell in sheet.cells)


def test_an_exercise_too_big_for_a_sheet_is_refused_rather_than_squeezed() -> None:
    too_many = {
        "title": "T",
        "exercises": [
            {"question": f"q{n}", "choices": ["a", "b"]} for n in range(MAX_QUESTIONS + 1)
        ],
    }
    with pytest.raises(SheetTooFull):
        _sheet(too_many)

    with pytest.raises(SheetTooFull):
        _sheet({"title": "T", "exercises": [{"question": "q", "choices": ["only one"]}]})

    with pytest.raises(SheetTooFull):
        _sheet({"title": "T", "exercises": []})


def test_a_sheet_written_before_the_rename_still_lays_out() -> None:
    """The old Italian keys reach here too: approval outlived the field names."""
    legacy = {
        "titolo": "Le stagioni",
        "istruzioni": "Barra una scelta.",
        "esercizi": [{"domanda": "Chi ha gli aculei?", "scelte": ["riccio", "volpe"]}],
    }
    sheet = _sheet(legacy)
    assert sheet.title == "Le stagioni"
    assert [cell.label for cell in sheet.cells] == ["riccio", "volpe"]
