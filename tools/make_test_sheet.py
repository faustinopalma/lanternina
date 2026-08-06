"""Generate a printable test sheet, so the vision path can be exercised on real paper.

The layout here is synthetic scaffolding — numbered boxes and nothing else. It exists to
answer measurable questions: do four markers survive this printer, does the QR decode from
a photograph, does a rectified cell land where the spec says it does.

    python tools/make_test_sheet.py --out build/test-sheet.svg --png

Print it at **100% scale**, never "fit to page". The ruler along the bottom edge is there
to be checked against a real ruler: if it does not measure 50 mm, every cell rectangle on
the page is wrong and readings would be silently misplaced.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from PIL import Image

from printing.render import PageGeometry, build_drawing, drawing_to_array, drawing_to_svg
from shared.ids import CellId, ExerciseId, SheetId
from shared.sheet import CellKind, CellSpec, Rect, SheetSpec

DEFAULT_SHEET_ID = SheetId("sh_testcard")
DEFAULT_EXERCISE_ID = ExerciseId("ex_testcard")


def square(page: PageGeometry, x_norm: float, y_norm: float, size_mm: float) -> Rect:
    """A rectangle that is square on paper, expressed in the spec's normalised frame."""
    quad = page.quad
    return Rect(x=x_norm, y=y_norm, w=size_mm / quad.w, h=size_mm / quad.h)


def build_test_spec(page: PageGeometry, sheet_id: SheetId, exercise_id: ExerciseId) -> SheetSpec:
    quad = page.quad
    cells: list[CellSpec] = []

    box_mm = 12.0
    gap_mm = 10.0
    for row in range(2):
        for column in range(4):
            index = row * 4 + column + 1
            x_mm = 10.0 + column * (box_mm + gap_mm)
            y_mm = 45.0 + row * (box_mm + gap_mm)
            cells.append(
                CellSpec(
                    id=CellId(f"box{index}"),
                    kind=CellKind.CHECKBOX,
                    rect=square(page, x_mm / quad.w, y_mm / quad.h, box_mm),
                    label=str(index),
                )
            )

    for option, letter in enumerate("abc"):
        x_mm = 10.0 + option * (box_mm + gap_mm)
        cells.append(
            CellSpec(
                id=CellId(f"choice_{letter}"),
                kind=CellKind.CHOICE_BOX,
                rect=square(page, x_mm / quad.w, 100.0 / quad.h, box_mm),
                label=letter,
                group="choice",
            )
        )

    cells.append(
        CellSpec(
            id=CellId("word"),
            kind=CellKind.WORD_LINE,
            rect=Rect(x=10.0 / quad.w, y=130.0 / quad.h, w=120.0 / quad.w, h=14.0 / quad.h),
            label="word",
        )
    )
    cells.append(
        CellSpec(
            id=CellId("drawing"),
            kind=CellKind.DRAWING_AREA,
            rect=Rect(x=10.0 / quad.w, y=160.0 / quad.h, w=140.0 / quad.w, h=60.0 / quad.h),
            label="drawing",
        )
    )

    qr_mm = 22.0
    qr_x_norm = (quad.w - qr_mm) / 2 / quad.w
    return SheetSpec(
        sheet_id=sheet_id,
        exercise_id=exercise_id,
        title="Test card",
        cells=tuple(cells),
        qr_rect=square(page, qr_x_norm, 2.0 / quad.h, qr_mm),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("build/test-sheet.svg"))
    parser.add_argument("--sheet-id", default=str(DEFAULT_SHEET_ID))
    parser.add_argument("--exercise-id", default=str(DEFAULT_EXERCISE_ID))
    parser.add_argument("--marker-size-mm", type=float, default=None)
    parser.add_argument("--png", action="store_true", help="also write a raster preview")
    parser.add_argument("--pdf", action="store_true", help="also write a PDF sized in mm")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    page = (
        PageGeometry(marker_size_mm=args.marker_size_mm)
        if args.marker_size_mm is not None
        else PageGeometry()
    )
    spec = build_test_spec(page, SheetId(args.sheet_id), ExerciseId(args.exercise_id))
    drawing = build_drawing(spec, page)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(drawing_to_svg(drawing), encoding="utf-8", newline="\n")
    print(f"wrote {args.out}  ({len(spec.cells)} cells, markers {page.marker_size_mm} mm)")

    if args.png:
        png_path = args.out.with_suffix(".png")
        cv2.imwrite(str(png_path), drawing_to_array(drawing, dpi=args.dpi))
        print(f"wrote {png_path}  ({args.dpi} dpi preview, not the print path)")

    if args.pdf:
        pdf_path = args.out.with_suffix(".pdf")
        raster = drawing_to_array(drawing, dpi=args.dpi)
        # Embedding the resolution makes the PDF page a physical size, so a print queue has
        # no reason to rescale it and the ruler on the page still measures 50 mm.
        Image.fromarray(raster).save(pdf_path, "PDF", resolution=float(args.dpi))
        points_w = raster.shape[1] / args.dpi * 72
        points_h = raster.shape[0] / args.dpi * 72
        print(f"wrote {pdf_path}  (page {points_w:.1f}x{points_h:.1f} pt, A4 is 595.3x841.9)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
