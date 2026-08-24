"""Four ways of laying out a page, because four kinds of object were chosen.

`shared/page.py` says what a page is: a kind, a title, a note, some labelled places to
write, and a picture described in words. This is where that becomes millimetres.

**The layout is ours and the composition is the model's.** The model chose the kind, wrote
the words and said what the picture shows; this file decides where any of it lands. That
division is not tidiness — it is `ideas/10 §5`: words drawn into pixels by an image model
reach a person having passed no safety gate, so the words are set here, from strings that
came through it.

**Nothing here has an identity and nothing is read back by position.** There are no cells,
no ids and no normalised rectangles: a page is read by handing a model the blank and what
came back off the glass. So a layout may change between one afternoon and the next without
anything downstream needing to hear about it.

**A picture that did not arrive leaves a page, not a hole.** Each layout is written so that
the room the illustration would have taken is given back — the words move up, the writing
lines grow — because a cloud that is down should cost a plainer page and not the afternoon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import numpy as np
from numpy.typing import NDArray

from shared.page import Page, PageKind, Room, Space

from .render import Drawing, MmRect, PageGeometry, PageImage, StrokePath, _text_width_mm

# A4, and the margin a home printer can be trusted with. The ET-2870 prints borderless on
# photo paper only; on plain A4 its unprintable edge is a few millimetres, so 14 mm is
# comfortable rather than tight. Chosen, not measured.
PAPER: Final = PageGeometry(
    width_mm=210.0, height_mm=297.0, margin_mm=14.0, marker_size_mm=0.0, quiet_zone_mm=0.0
)

TITLE_MM: Final = 8.0
NOTE_MM: Final = 4.2
LABEL_MM: Final = 3.6
# A rule to write on, and the gap under it that the writing actually occupies.
RULE_MM: Final = 0.3
WRITING_MM: Final = 9.0
# What each amount of room turns into here. A box is for drawing in and the other two are
# for words, so they differ by more than a number of lines.
ROWS: Final[dict[Room, int]] = {Room.A_LINE: 1, Room.SOME_LINES: 3, Room.A_BOX: 0}
BOX_MM: Final = 34.0


class PageTooFull(ValueError):
    """The words asked for more paper than the paper has."""


@dataclass
class _Sheet:
    """A drawing being built, in page millimetres, with a cursor going down the page."""

    filled: list[MmRect]
    outlined: list[MmRect]
    headings: list[tuple[float, float, float, str]]
    strokes: list[StrokePath]
    images: list[PageImage]
    y: float

    def done(self) -> Drawing:
        return Drawing(
            page=PAPER,
            filled=tuple(self.filled),
            outlined=tuple(self.outlined),
            labels=(),
            headings=tuple(self.headings),
            strokes=tuple(self.strokes),
            images=tuple(self.images),
        )


def compose(page: Page, picture: NDArray[np.uint8] | None = None) -> Drawing:
    """One page, ready to print. ``picture`` is grey, or absent because none arrived."""
    sheet = _Sheet(filled=[], outlined=[], headings=[], strokes=[], images=[], y=PAPER.margin_mm)
    layout = _LAYOUTS[page.kind]
    layout(sheet, page, picture)
    if sheet.y > PAPER.height_mm - PAPER.margin_mm:
        raise PageTooFull(
            f"a {page.kind} of this length needs {sheet.y:.0f} mm and the paper has "
            f"{PAPER.height_mm - PAPER.margin_mm:.0f}"
        )
    return sheet.done()


# ── The pieces every layout is made of ───────────────────────────────────────────────


def _text_area() -> tuple[float, float]:
    """Left edge and width of the column everything is set in."""
    return PAPER.margin_mm, PAPER.width_mm - 2 * PAPER.margin_mm


def _wrapped(text: str, width_mm: float, size_mm: float) -> list[str]:
    """Break a line so it fits the column, measuring in the font the PDF actually sets."""
    lines: list[str] = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and _text_width_mm(candidate, size_mm) > width_mm:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def _write(
    sheet: _Sheet, text: str, size_mm: float, *, x: float, width_mm: float, centred: bool = False
) -> None:
    """Set one string, wrapped, moving the cursor past it."""
    for line in _wrapped(text, width_mm, size_mm):
        left = x
        if centred:
            left = x + (width_mm - _text_width_mm(line, size_mm)) / 2
        sheet.y += size_mm
        sheet.headings.append((left, sheet.y, size_mm, line))
        sheet.y += size_mm * 0.35


def _rule(sheet: _Sheet, x: float, width_mm: float, thickness_mm: float = RULE_MM) -> None:
    sheet.filled.append(MmRect(x, sheet.y, width_mm, thickness_mm))
    sheet.y += thickness_mm


def _space(sheet: _Sheet, space: Space, *, x: float, width_mm: float) -> None:
    """A label, and the room to answer it. The label is set above what it names."""
    if space.label:
        _write(sheet, space.label, LABEL_MM, x=x, width_mm=width_mm)
    if space.room is Room.A_BOX:
        sheet.outlined.append(MmRect(x, sheet.y + 1.0, width_mm, BOX_MM))
        sheet.y += BOX_MM + 4.0
        return
    for _ in range(ROWS[space.room]):
        sheet.y += WRITING_MM
        _rule(sheet, x, width_mm)
    sheet.y += 3.0


def _picture(
    sheet: _Sheet, picture: NDArray[np.uint8] | None, rect: MmRect, *, framed: bool = False
) -> float:
    """Place the picture and say how much height it used, which is none when there is none."""
    if picture is None:
        return 0.0
    sheet.images.append(PageImage(rect=rect, grey=picture))
    if framed:
        sheet.outlined.append(rect)
    return rect.h


# ── The four kinds ───────────────────────────────────────────────────────────────────


def _map(sheet: _Sheet, page: Page, picture: NDArray[np.uint8] | None) -> None:
    """A border, the country inside it, and a legend along the bottom.

    The border is what makes it read as a map rather than as a picture with writing under
    it, and it costs about 900 mm² of ink — a line 0.5 mm wide around a 182 by 269 box.
    """
    x, width = _text_area()
    sheet.outlined.append(MmRect(x, sheet.y, width, PAPER.height_mm - 2 * PAPER.margin_mm))
    inner_x = x + 6.0
    inner_w = width - 12.0
    sheet.y += 8.0

    _write(sheet, page.title, TITLE_MM, x=inner_x, width_mm=inner_w, centred=True)
    sheet.y += 2.0
    for line in page.note:
        _write(sheet, line, NOTE_MM, x=inner_x, width_mm=inner_w, centred=True)

    sheet.y += 3.0
    sheet.y += _picture(
        sheet, picture, MmRect(inner_x, sheet.y, inner_w, inner_w * 0.72), framed=True
    )
    sheet.y += 6.0

    _rule(sheet, inner_x, inner_w, 0.5)
    sheet.y += 4.0
    for space in page.spaces:
        _space(sheet, space, x=inner_x, width_mm=inner_w)


def _dossier(sheet: _Sheet, page: Page, picture: NDArray[np.uint8] | None) -> None:
    """A heading with a rule under it, the picture filed to the right, fields below.

    The picture is beside the note rather than above it, which is what makes this look
    like something taken out of a folder instead of an article.
    """
    x, width = _text_area()
    picture_w = 52.0
    column = width - picture_w - 8.0 if picture is not None else width

    top = sheet.y
    _write(sheet, page.title, TITLE_MM, x=x, width_mm=column)
    sheet.y += 1.5
    _rule(sheet, x, width, 0.8)
    sheet.y += 4.0
    for line in page.note:
        _write(sheet, line, NOTE_MM, x=x, width_mm=column)

    used = _picture(
        sheet,
        picture,
        MmRect(x + width - picture_w, top + TITLE_MM + 8.0, picture_w, picture_w),
        framed=True,
    )
    sheet.y = max(sheet.y, top + TITLE_MM + 8.0 + used) + 6.0

    for space in page.spaces:
        _space(sheet, space, x=x, width_mm=width)


def _label(sheet: _Sheet, page: Page, picture: NDArray[np.uint8] | None) -> None:
    """The picture large, the words few and centred under it, and a great deal of white.

    This is the kind that spends its paper on nothing, on purpose. It is also the one most
    likely to be refused by the ink budget, because a big picture is where the ink goes.
    """
    x, width = _text_area()
    sheet.y += 6.0
    sheet.y += _picture(sheet, picture, MmRect(x + width * 0.1, sheet.y, width * 0.8, width * 0.6))
    sheet.y += 10.0

    _write(sheet, page.title, TITLE_MM, x=x, width_mm=width, centred=True)
    sheet.y += 1.0
    _rule(sheet, x + width * 0.35, width * 0.3, 0.4)
    sheet.y += 5.0
    for line in page.note:
        _write(sheet, line, NOTE_MM, x=x + width * 0.1, width_mm=width * 0.8, centred=True)

    sheet.y += 8.0
    for space in page.spaces:
        _space(sheet, space, x=x + width * 0.1, width_mm=width * 0.8)


def _notebook(sheet: _Sheet, page: Page, picture: NDArray[np.uint8] | None) -> None:
    """A margin rule down the left, the picture small in the corner, and ruled rows.

    The margin rule runs the height of the paper whatever the words do, which is what makes
    the page look like a leaf out of something rather than a printout of a list.
    """
    x, width = _text_area()
    margin_x = x + 12.0
    sheet.filled.append(
        MmRect(margin_x, PAPER.margin_mm, 0.3, PAPER.height_mm - 2 * PAPER.margin_mm)
    )
    column_x = margin_x + 5.0
    column_w = x + width - column_x

    picture_w = 40.0
    top = sheet.y
    used = _picture(
        sheet, picture, MmRect(x + width - picture_w, top, picture_w, picture_w * 0.75)
    )
    words_w = column_w - (picture_w + 6.0 if picture is not None else 0.0)

    _write(sheet, page.title, TITLE_MM, x=column_x, width_mm=words_w)
    sheet.y += 2.0
    for line in page.note:
        _write(sheet, line, NOTE_MM, x=column_x, width_mm=words_w)
    sheet.y = max(sheet.y, top + used) + 6.0

    for space in page.spaces:
        _space(sheet, space, x=column_x, width_mm=column_w)


_LAYOUTS: Final = {
    PageKind.MAP: _map,
    PageKind.DOSSIER: _dossier,
    PageKind.LABEL: _label,
    PageKind.NOTEBOOK: _notebook,
}
