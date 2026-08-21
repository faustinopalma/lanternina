"""Turn an approved exercise into a sheet that can be printed and read back.

Retired 21 August 2026. It laid out four questions of four boxes, always in the same
places, and that fixed shape is what a page stopped being: `shared/pagedesign.py` and
`printing/compose.py` took over, where a model designs the page and the ink it may spend
is bounded by the vocabulary rather than by arithmetic. `attic/README.md` holds the rest.

Nothing was wrong with it. The two catalogue experiences it drew were converted to designs
by running this module one last time and freezing what came out, and every cell and every
heading came out in exactly the same place — checked on 21 August 2026, both sheets, cells
and headings identical.

This is the missing half of the paper loop: the content agent writes the words, the
renderer draws millimetres, and nothing until now decided where a box goes. The decision is
arithmetic, not judgement, so there is no model here and nothing to approve — the words
were approved as words, and this only chooses where they land.

Only `CHOICE_BOX` cells are produced, because they are one of the two kinds readable
without the network. A sheet made of them keeps working when the cloud does not, which is
the whole reason the paper path exists.

Positions are normalised over the marker quadrilateral, so they carry no millimetres and
no paper size. The renderer refuses a layout that would sit in a marker's quiet zone; the
tests here check the weaker thing the renderer cannot see — that every declared cell is
inside the page and no two of them overlap.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final

from shared.exercise import CHOICES, EXERCISES, INSTRUCTIONS, QUESTION, TITLE, field
from shared.ids import CellId, ExerciseId, SheetId
from shared.sheet import CellKind, CellSpec, Heading, Rect, SheetSpec

# The band each part of the sheet lives in, as a fraction of the marker quadrilateral.
# The top band is the only one that has to dodge anything: a full-width line there runs
# through the two upper markers' quiet zones and rectification drifts without failing
# loudly. Hence the inset, and hence the QR sitting below the corner rather than in it.
TITLE_LEFT: Final = 0.04
TITLE_WIDTH: Final = 0.92
TITLE_TOP: Final = 0.005
INSTRUCTIONS_TOP: Final = 0.065
QR_RECT: Final = Rect(0.78, 0.025, 0.18, 0.118)
QUESTIONS_TOP: Final = 0.19
QUESTION_HEIGHT: Final = 0.135
# Far enough below the question that the choice printed above each box does not land on
# it: at 251 mm of usable height these two lines were a millimetre apart at 0.045.
BOX_TOP_OFFSET: Final = 0.065
BOX_HEIGHT: Final = 0.042
BOX_GAP: Final = 0.02

# Four questions of four choices is what fits with the boxes still big enough to tick.
MAX_QUESTIONS: Final = 4
MAX_CHOICES: Final = 4


class SheetTooFull(ValueError):
    """The exercise does not fit on one sheet, and shrinking it is not this module's call."""


def sheet_for(
    body: Mapping[str, Any],
    *,
    sheet_id: SheetId,
    exercise_id: ExerciseId,
    created_at: float = 0.0,
) -> SheetSpec:
    """Lay one exercise body out as a printable, readable sheet."""
    questions = _questions(body)
    if not questions:
        raise SheetTooFull("an exercise with no question has nothing to lay out")
    if len(questions) > MAX_QUESTIONS:
        raise SheetTooFull(
            f"{len(questions)} questions do not fit on one sheet; at most {MAX_QUESTIONS}"
        )

    headings = [
        Heading(
            Rect(TITLE_LEFT, TITLE_TOP, TITLE_WIDTH, 0.04),
            str(field(body, TITLE, "")),
            size_mm=6.5,
        )
    ]
    instructions = str(field(body, INSTRUCTIONS, ""))
    if instructions:
        headings.append(
            Heading(Rect(TITLE_LEFT, INSTRUCTIONS_TOP, 0.70, 0.032), instructions, 4.0)
        )

    cells: list[CellSpec] = []
    for index, question in enumerate(questions):
        top = QUESTIONS_TOP + index * QUESTION_HEIGHT
        headings.append(
            Heading(Rect(0.0, top, 1.0, 0.035), f"{index + 1}. {_question_text(question)}", 4.5)
        )
        cells.extend(_choice_cells(question, index, top + BOX_TOP_OFFSET))

    return SheetSpec(
        sheet_id=sheet_id,
        exercise_id=exercise_id,
        title=str(field(body, TITLE, "")),
        cells=tuple(cells),
        qr_rect=QR_RECT,
        created_at=created_at,
        headings=tuple(headings),
    )


def _questions(body: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    entries = field(body, EXERCISES, []) or []
    if not isinstance(entries, Sequence):
        return []
    return [entry for entry in entries if isinstance(entry, Mapping)]


def _question_text(question: Mapping[str, Any]) -> str:
    return str(field(question, QUESTION, ""))


def _choice_cells(
    question: Mapping[str, Any], index: int, top: float
) -> list[CellSpec]:
    choices = [str(choice) for choice in (field(question, CHOICES, []) or [])]
    if not 2 <= len(choices) <= MAX_CHOICES:
        raise SheetTooFull(
            f"question {index + 1} has {len(choices)} choices; a sheet holds 2 to {MAX_CHOICES}"
        )

    width = (1.0 - BOX_GAP * (len(choices) - 1)) / len(choices)
    group = f"q{index + 1}"
    return [
        CellSpec(
            id=CellId(f"{group}c{position + 1}"),
            kind=CellKind.CHOICE_BOX,
            rect=Rect(position * (width + BOX_GAP), top, width, BOX_HEIGHT),
            label=choice,
            group=group,
        )
        for position, choice in enumerate(choices)
    ]
