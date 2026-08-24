"""A sheet whose only purpose is to be measured, so the ink thresholds stop being guesses.

Three things are being separated here, and one sheet answers all three.

*The floor.* Boxes left empty in different places on the page. One scan of one sheet put
every untouched box at exactly 0.0000, which is a suspiciously good number; spread out over
the glass they will say whether that holds at the edges too.

*The instrument.* Boxes carrying a printed square of known area — 1% of the box up to 32%.
Printed rather than shaded, because a halftone grey measures the printer's dithering and a
solid square measures what we mean. These say how a measured fraction relates to a real
one, including whatever the reader's inset does to it.

*The hand.* Boxes for somebody to mark the way it will actually happen: a light tick, a
firm one, a cross, a filled box, a circle. That is the distribution the threshold has to
separate, and it is the only part that cannot be printed.

The last box asks for a mark just outside the lines. If that one reads as ink, the reader
is counting the printed outline or a stray, and the inset needs to grow.

    python -m tools.make_calibration_sheet --out build/taratura.pdf
"""

from __future__ import annotations

import argparse
import math
from dataclasses import replace
from pathlib import Path

from printing.render import Drawing, MmRect, PageGeometry, build_drawing, drawing_to_pdf
from shared.ids import CellId, ExerciseId, SheetId
from shared.sheet import CellKind, CellSpec, Heading, Rect, SheetSpec

SHEET_ID = SheetId("sh_taratura")
EXERCISE_ID = ExerciseId("ex_taratura")

BOX_H = 0.052
GAP_X = 0.025
ROW_STEP = 0.115
FIRST_ROW = 0.16

# Printed area as a fraction of the box, drawn as one centred square.
PRINTED_FILLS = (0.01, 0.02, 0.04, 0.08, 0.16, 0.32)

BY_HAND = (
    ("leggero", "un segno leggerissimo"),
    ("normale", "un segno come al solito"),
    ("crocetta", "una crocetta"),
    ("pieno", "riempi tutta la casella"),
    ("cerchio", "un cerchio dentro"),
    ("fuori", "un segno FUORI, accanto"),
)


def _row(cells: list[CellSpec], names: list[tuple[str, str]], top: float) -> None:
    width = (1.0 - GAP_X * (len(names) - 1)) / len(names)
    for column, (cell_id, label) in enumerate(names):
        cells.append(
            CellSpec(
                id=CellId(cell_id),
                kind=CellKind.CHECKBOX,
                rect=Rect(column * (width + GAP_X), top, width, BOX_H),
                label=label,
            )
        )


def build_spec() -> SheetSpec:
    cells: list[CellSpec] = []
    headings = [
        Heading(Rect(0.04, 0.005, 0.92, 0.04), "Foglio di taratura", size_mm=6.5),
        Heading(
            Rect(0.04, 0.062, 0.70, 0.03),
            "Prima riga: non toccare. Seconda: gia stampata. Poi segna come dice l'etichetta.",
            3.6,
        ),
    ]

    _row(cells, [(f"vuota{n}", "lascia vuota") for n in range(1, 6)], FIRST_ROW)
    _row(
        cells,
        [(f"stampata{int(f * 100):02d}", f"{f * 100:.0f}% stampato") for f in PRINTED_FILLS],
        FIRST_ROW + ROW_STEP,
    )
    _row(cells, list(BY_HAND[:3]), FIRST_ROW + 2 * ROW_STEP)
    _row(cells, list(BY_HAND[3:]), FIRST_ROW + 3 * ROW_STEP)
    _row(cells, [(f"vuota{n}", "lascia vuota") for n in range(6, 9)], FIRST_ROW + 4 * ROW_STEP)

    return SheetSpec(
        sheet_id=SHEET_ID,
        exercise_id=EXERCISE_ID,
        title="Foglio di taratura",
        cells=tuple(cells),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
        headings=tuple(headings),
    )


def with_printed_fills(drawing: Drawing, spec: SheetSpec, page: PageGeometry) -> Drawing:
    """Put a centred square of known area inside each of the printed boxes."""
    extra: list[MmRect] = []
    for fraction in PRINTED_FILLS:
        area = page.to_page(spec.cell(CellId(f"stampata{int(fraction * 100):02d}")).rect)
        side = math.sqrt(fraction * area.w * area.h)
        extra.append(
            MmRect(
                area.x + (area.w - side) / 2,
                area.y + (area.h - side) / 2,
                side,
                side,
            )
        )
    return replace(drawing, filled=drawing.filled + tuple(extra))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("build/taratura.pdf"))
    args = parser.parse_args()

    page = PageGeometry()
    spec = build_spec()
    drawing = with_printed_fills(build_drawing(spec, page), spec, page)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(drawing_to_pdf(drawing))
    print(f"{args.out}: {len(spec.cells)} caselle")


if __name__ == "__main__":
    main()
