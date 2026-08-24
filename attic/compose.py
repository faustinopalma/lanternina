"""From a design a model made to a sheet that can be printed and read back.

Two things happen here and they are deliberately in one place, because they are the same
decision seen twice: a design becomes the ``SheetSpec`` the reader has always taken, and
the ink it spends is measured against a budget before any of it reaches paper.

The budget is applied to :meth:`PageDesign.stroke_ink_mm2`, which is length times width
over the marks — the area a pen would wet, and a figure that does not move with the
resolution anybody happens to render at. :func:`ink_coverage` is the other number: it
rasterises the page and counts dark pixels, which catches a whole page of boxes that the
stroke figure knows nothing about. The two are not interchangeable and this module does
not pretend they are — rounding a stroke width to whole pixels moves the rasterised
figure by up to 70%, measured, so it is reported and never used to refuse.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

from shared.ids import ExerciseId, SheetId
from shared.pagedesign import MAX_STROKE_INK_MM2, Circle, PageDesign, Stroke
from shared.sheet import Rect, SheetSpec

from .render import (
    Drawing,
    MmRect,
    PageGeometry,
    StrokePath,
    build_drawing,
    drawing_to_array,
)

# Where the QR sits on every designed sheet. Fixed rather than left to the model: it is the
# only thing on the page that says which sheet this is, and a design that put it somewhere
# a marker's quiet zone reaches would be refused after the model had been paid.
QR_RECT: Final = Rect(0.78, 0.025, 0.18, 0.118)

# A circle becomes chords this long. At 0.5 mm the corners are under the dot pitch of any
# printer this reaches, so the polygon is a circle on paper; the cap keeps a large circle
# from spending a hundred vertices on smoothness nobody can see.
CHORD_MM: Final = 0.5
MAX_CHORD_SEGMENTS: Final = 180

# The raster the reported figure is measured on. 150 dpi puts a 0.2 mm stroke — the
# thinnest the format allows — at 1.2 pixels, so the thinnest line is still counted.
INK_DPI: Final = 150


class InkTooHeavy(ValueError):
    """The design spends more ink than a sheet is allowed to."""


@dataclass(frozen=True, slots=True)
class ComposedSheet:
    """What a design becomes: the reader's contract, the drawing, and what it will cost."""

    spec: SheetSpec
    drawing: Drawing
    stroke_ink_mm2: float
    coverage: float

    @property
    def ink_mm2(self) -> float:
        page = self.drawing.page
        return self.coverage * page.width_mm * page.height_mm


def compose(
    design: PageDesign,
    *,
    sheet_id: SheetId,
    exercise_id: ExerciseId,
    page: PageGeometry | None = None,
    created_at: float = 0.0,
    budget_mm2: float = MAX_STROKE_INK_MM2,
) -> ComposedSheet:
    """Turn a design into a printable sheet, or refuse it.

    The refusal comes before rendering and says what was spent against what was allowed,
    because the caller's next move is to ask the model for a lighter page and it needs to
    be able to say by how much.
    """
    page = page or PageGeometry()
    quad = page.quad
    spent = design.stroke_ink_mm2(quad.w, quad.h)
    if spent > budget_mm2:
        raise InkTooHeavy(
            f"the drawing would put {spent:.0f} mm² of ink on the page; "
            f"a sheet is allowed {budget_mm2:.0f} mm²"
        )

    spec = design.to_sheet_spec(
        sheet_id=sheet_id,
        exercise_id=exercise_id,
        qr_rect=QR_RECT,
        created_at=created_at,
    )
    drawing = build_drawing(spec, page, strokes=_strokes_in_mm(design, page))
    return ComposedSheet(
        spec=spec,
        drawing=drawing,
        stroke_ink_mm2=spent,
        coverage=ink_coverage(drawing),
    )


def ink_coverage(drawing: Drawing, dpi: int = INK_DPI) -> float:
    """The fraction of the page that is dark, on the raster the renderer produces.

    Reported, never used to refuse. Two things are absent from it and both are said here
    rather than discovered: text is not drawn unless a caller asks for it, so a page of
    long sentences costs more than this reports; and a stroke width is rounded to whole
    pixels, which at 0.3 mm and 150 dpi is 1.77 pixels drawn as 2.
    """
    canvas = drawing_to_array(drawing, dpi=dpi)
    return float((canvas < 128).sum()) / float(canvas.size)


def _strokes_in_mm(design: PageDesign, page: PageGeometry) -> list[StrokePath]:
    """Every stroke converted from the marker frame to page millimetres."""
    quad = page.quad
    out: list[StrokePath] = []
    for mark in design.strokes:
        if isinstance(mark, Stroke):
            vertices = tuple(
                (quad.x + x * quad.w, quad.y + y * quad.h) for x, y in mark.vertices
            )
        else:
            vertices = _chords(mark, quad)
        out.append(StrokePath(vertices, mark.width_mm))
    return out


def _chords(circle: Circle, quad: MmRect) -> tuple[tuple[float, float], ...]:
    """A circle as a closed run of short segments, in page millimetres.

    The radius is a fraction of the frame's width in both directions, which is what keeps
    it a circle on paper: the frame is not square, so scaling y by the height would draw
    an ellipse.
    """
    radius_mm = circle.r * quad.w
    circumference = 2.0 * math.pi * radius_mm
    segments = min(MAX_CHORD_SEGMENTS, max(24, int(circumference / CHORD_MM)))
    cx = quad.x + circle.cx * quad.w
    cy = quad.y + circle.cy * quad.h
    return tuple(
        (
            cx + radius_mm * math.cos(2.0 * math.pi * i / segments),
            cy + radius_mm * math.sin(2.0 * math.pi * i / segments),
        )
        for i in range(segments + 1)
    )
