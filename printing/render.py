"""Draw a :class:`~shared.sheet.SheetSpec` onto paper.

The reader and this module have to agree on where a cell is, so both derive every
rectangle from ``shared.sheet``. Nothing here decides content: it draws only the scaffold
that lets a sheet be found again — four ArUco markers, a QR that identifies it, and the
outlines the learner writes inside.

Output is vector SVG at exact millimetre sizes. Vector matters here: an ArUco module at a
15 mm marker is 2.5 mm across, and letting a printer driver resample a bitmap softens
precisely the edges the detector measures. The raster backend exists so tests can decode
what was drawn; both backends consume the same :class:`Drawing`, so they cannot disagree.

Page size lives here rather than in the spec because ``SheetSpec`` is deliberately
paper-independent: its coordinates are normalised over the marker quadrilateral.
"""

from __future__ import annotations

import base64
import zlib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Final

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.sheet import (
    ARUCO_DICT_NAME,
    MARKER_ID_BOTTOM_LEFT,
    MARKER_ID_BOTTOM_RIGHT,
    MARKER_ID_TOP_LEFT,
    MARKER_ID_TOP_RIGHT,
    MARKER_SIZE_MM,
    QUIET_ZONE_MM,
    CellKind,
    QrPayload,
    Rect,
    SheetSpec,
)

# A 4x4 ArUco is 4 data modules plus a one-module black border on each side.
MARKER_MODULES: Final = 6

# The QR standard asks for four clear modules around the symbol. Reserving them inside the
# declared rectangle keeps the code readable regardless of what a caller puts next to it.
QR_QUIET_MODULES: Final = 4

# Printed at 100% scale this measures exactly 50 mm, which is how the parent can tell that
# "fit to page" did not silently shrink the geometry the reader depends on.
RULER_LENGTH_MM: Final = 50.0

# The size a cell's label is drawn at, in both backends, so the width computed below is the
# width that gets printed.
LABEL_SIZE_MM: Final = 3.0

# Helvetica advance widths, in thousandths of an em, for the characters a label is made of:
# digits, the arithmetic signs, and the letters of a short Italian word. Anything else uses
# the default. Taken from the Adobe Helvetica metrics, so a label's width on paper is known
# rather than guessed — which is what lets a writing line start exactly after its label.
_HELVETICA_WIDTHS: Final[dict[str, int]] = {
    " ": 278, ".": 278, ",": 278, ":": 278, ";": 278, "!": 278, "'": 191,
    "(": 333, ")": 333, "-": 333, "/": 278, "?": 556,
    "=": 584, "+": 584, "\u00d7": 584, "<": 584, ">": 584,
    "i": 222, "l": 222, "j": 222, "f": 278, "t": 278, "r": 333,
    "m": 833, "w": 722, "M": 833, "W": 944,
}
_HELVETICA_DIGIT: Final = 556
_HELVETICA_DEFAULT: Final = 556
_HELVETICA_UPPER: Final = 722

_MM_PER_INCH: Final = 25.4


def _text_width_mm(text: str, size_mm: float) -> float:
    """How wide this text prints in Helvetica at this size."""
    thousandths = 0
    for character in text:
        if character in _HELVETICA_WIDTHS:
            thousandths += _HELVETICA_WIDTHS[character]
        elif character.isdigit():
            thousandths += _HELVETICA_DIGIT
        elif character.isupper():
            thousandths += _HELVETICA_UPPER
        else:
            thousandths += _HELVETICA_DEFAULT
    return thousandths / 1000.0 * size_mm


class SheetLayoutError(ValueError):
    """The spec cannot be drawn on this page without breaking detection."""


@dataclass(frozen=True, slots=True)
class MmRect:
    """A rectangle in page millimetres, origin at the top-left corner of the paper."""

    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    def grown(self, by: float) -> MmRect:
        return MmRect(self.x - by, self.y - by, self.w + 2 * by, self.h + 2 * by)

    def overlaps(self, other: MmRect) -> bool:
        return not (
            other.x >= self.right
            or other.right <= self.x
            or other.y >= self.bottom
            or other.bottom <= self.y
        )


@dataclass(frozen=True, slots=True)
class PageGeometry:
    """Where the markers sit on a physical sheet of paper."""

    width_mm: float = 210.0
    height_mm: float = 297.0
    margin_mm: float = 8.0
    marker_size_mm: float = MARKER_SIZE_MM
    quiet_zone_mm: float = QUIET_ZONE_MM

    def __post_init__(self) -> None:
        if self.quad.w <= 0 or self.quad.h <= 0:
            raise SheetLayoutError("markers and margins leave no readable area")

    @property
    def marker_rects(self) -> dict[int, MmRect]:
        size = self.marker_size_mm
        near = self.margin_mm
        far_x = self.width_mm - self.margin_mm - size
        far_y = self.height_mm - self.margin_mm - size
        return {
            MARKER_ID_TOP_LEFT: MmRect(near, near, size, size),
            MARKER_ID_TOP_RIGHT: MmRect(far_x, near, size, size),
            MARKER_ID_BOTTOM_RIGHT: MmRect(far_x, far_y, size, size),
            MARKER_ID_BOTTOM_LEFT: MmRect(near, far_y, size, size),
        }

    @property
    def quad(self) -> MmRect:
        """The region normalised page coordinates map onto: the markers' *inner* corners."""
        inset = self.margin_mm + self.marker_size_mm
        return MmRect(
            inset,
            inset,
            self.width_mm - 2 * inset,
            self.height_mm - 2 * inset,
        )

    def to_page(self, rect: Rect) -> MmRect:
        """Map a normalised spec rectangle into page millimetres."""
        quad = self.quad
        return MmRect(
            quad.x + rect.x * quad.w,
            quad.y + rect.y * quad.h,
            rect.w * quad.w,
            rect.h * quad.h,
        )

    @property
    def keep_out_rects(self) -> tuple[MmRect, ...]:
        """Regions that must stay free of ink, quiet zones included."""
        return tuple(r.grown(self.quiet_zone_mm) for r in self.marker_rects.values())


@dataclass(frozen=True, slots=True)
class StrokePath:
    """A run of straight segments in page millimetres.

    One primitive rather than lines, curves and circles, because the three backends have
    to agree about where ink lands and the cheapest way to guarantee that is to give them
    one thing to draw. A circle arrives here already expanded into short chords.
    """

    vertices: tuple[tuple[float, float], ...]
    width_mm: float = 0.3


@dataclass(frozen=True, slots=True)
class PageImage:
    """A grey picture placed on the paper, in page millimetres.

    Grey and not colour, because the two things this ever goes to are an inkjet asked not
    to spend much and an ink-coverage measurement, and both of them are about tone. The
    array is what the backends resample; nothing here decides how big it was when it
    arrived.
    """

    rect: MmRect
    grey: NDArray[np.uint8]


@dataclass(frozen=True, slots=True)
class Drawing:
    """A resolution-independent description of one printable sheet."""

    page: PageGeometry
    filled: tuple[MmRect, ...]
    outlined: tuple[MmRect, ...]
    labels: tuple[tuple[float, float, str], ...]
    # (x, y, size in mm, text): the words on the sheet, which carry no geometry.
    headings: tuple[tuple[float, float, float, str], ...] = ()
    # Line art, and the rules a writing line is drawn as.
    strokes: tuple[StrokePath, ...] = ()
    # Drawn first, so words and rules land on top of a picture rather than under it.
    images: tuple[PageImage, ...] = ()


def _bitmap_to_rects(bitmap: NDArray[np.uint8], origin: MmRect, quiet_modules: int) -> list[MmRect]:
    """Turn a black-and-white module grid into one rectangle per dark module.

    Drawing modules as rectangles rather than scaling an image keeps every edge exactly on
    a module boundary, which is what the detectors measure.
    """
    rows, cols = bitmap.shape
    total_cols = cols + 2 * quiet_modules
    total_rows = rows + 2 * quiet_modules
    module_w = origin.w / total_cols
    module_h = origin.h / total_rows
    left = origin.x + quiet_modules * module_w
    top = origin.y + quiet_modules * module_h

    rects: list[MmRect] = []
    for row in range(rows):
        for col in range(cols):
            if bitmap[row, col] == 0:
                rects.append(
                    MmRect(left + col * module_w, top + row * module_h, module_w, module_h)
                )
    return rects


def marker_bitmap(marker_id: int, dictionary_name: str = ARUCO_DICT_NAME) -> NDArray[np.uint8]:
    """The exact module pattern OpenCV will later look for. Same library both ways."""
    dictionary = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dictionary_name))
    # OpenCV's stubs promise only a generic ndarray, so narrow it where it enters our code.
    bitmap = cv2.aruco.generateImageMarker(dictionary, marker_id, MARKER_MODULES)
    return np.asarray(bitmap, dtype=np.uint8)


def qr_bitmap(payload: str) -> NDArray[np.uint8]:
    return np.asarray(cv2.QRCodeEncoder.create().encode(payload), dtype=np.uint8)


def build_drawing(
    spec: SheetSpec,
    page: PageGeometry | None = None,
    strokes: Sequence[StrokePath] = (),
) -> Drawing:
    """Lay ``spec`` out on paper, refusing layouts the reader could not decode.

    ``strokes`` is line art already converted to millimetres. It is passed in rather than
    read off the spec because ``SheetSpec`` is the reader's contract and the reader never
    looks at a drawing.
    """
    page = page or PageGeometry()

    filled: list[MmRect] = []
    for marker_id, rect in page.marker_rects.items():
        filled.extend(_bitmap_to_rects(marker_bitmap(marker_id), rect, quiet_modules=0))

    payload = QrPayload(
        sheet_id=spec.sheet_id, exercise_id=spec.exercise_id, spec_version=spec.spec_version
    ).encode()
    qr_area = page.to_page(spec.qr_rect)
    _refuse_if_obstructed(page, qr_area, "the QR code")
    filled.extend(_bitmap_to_rects(qr_bitmap(payload), qr_area, QR_QUIET_MODULES))

    outlined: list[MmRect] = []
    labels: list[tuple[float, float, str]] = []
    rules: list[StrokePath] = []
    for cell in spec.cells:
        area = page.to_page(cell.rect)
        _refuse_if_obstructed(page, area, f"cell {cell.id!r}")
        if cell.kind is CellKind.WORD_LINE:
            # A line to write on is its baseline. A box around it costs three more sides of
            # ink and looks like a form rather than somewhere to write.
            #
            # Its label sits at the start of the line and the rule begins after it, which
            # is how `6 × 2 = ______` is read. Drawn under the rule instead, it printed as
            # a caption under an empty line and nothing joined the two.
            start = area.x
            if cell.label:
                start += _text_width_mm(cell.label, LABEL_SIZE_MM) + 1.5
            rules.append(StrokePath(((start, area.bottom), (area.right, area.bottom)), 0.3))
        else:
            outlined.append(area)
        if cell.label:
            if cell.kind is CellKind.WORD_LINE:
                # On the line's own baseline, at its start: the rule was shortened above
                # to leave exactly this room.
                labels.append((area.x, area.bottom, cell.label))
            elif cell.kind is CellKind.DRAWING_AREA:
                # Just inside the frame. Above it collided with the heading a model had
                # already put there, and a drawing area is empty by definition, so inside
                # is the one place nothing else can be.
                labels.append((area.x + 1.5, area.y + LABEL_SIZE_MM + 1.0, cell.label))
            else:
                # Beside the box, in the order a choice is read — unless it would run off
                # the paper, which is what a wide box does with a long label beside it.
                width = _text_width_mm(cell.label, LABEL_SIZE_MM)
                if area.right + 1.5 + width <= page.width_mm - page.margin_mm:
                    labels.append(
                        (area.right + 1.5, area.bottom - area.h * 0.25, cell.label)
                    )
                else:
                    labels.append((area.x, area.bottom + LABEL_SIZE_MM + 1.0, cell.label))

    filled.extend(_ruler_rects(page))
    ruler_x = (page.width_mm - RULER_LENGTH_MM) / 2
    # Above the ticks rather than across the bar, which is where it used to land.
    labels.append(
        (ruler_x, page.height_mm - page.margin_mm - 5.5, f"{RULER_LENGTH_MM:.0f} mm")
    )

    headings: list[tuple[float, float, float, str]] = []
    for heading in spec.headings:
        area = page.to_page(heading.rect)
        _refuse_if_obstructed(page, area, "a printed line")
        headings.append((area.x, area.bottom, heading.size_mm, heading.text))

    drawn = [*rules, *strokes]
    for stroke in strokes:
        for x, y in stroke.vertices:
            _refuse_if_obstructed(page, MmRect(x, y, 0.01, 0.01), "a stroke")
    return Drawing(
        page,
        tuple(filled),
        tuple(outlined),
        tuple(labels),
        tuple(headings),
        tuple(drawn),
    )


def _refuse_if_obstructed(page: PageGeometry, area: MmRect, what: str) -> None:
    for zone in page.keep_out_rects:
        if zone.overlaps(area):
            raise SheetLayoutError(
                f"{what} overlaps a marker quiet zone; the page would not rectify reliably"
            )


def _ruler_rects(page: PageGeometry) -> list[MmRect]:
    """A 50 mm bar with 10 mm ticks, so a wrongly scaled printout is visible with a ruler.

    Centred between the bottom markers: an earlier version started at the left margin and
    ran straight through the bottom-left marker, which still decoded but reported corners
    several pixels off — a quietly wrong rectification rather than an obvious failure.
    """
    baseline = page.height_mm - page.margin_mm - 3.0
    left = (page.width_mm - RULER_LENGTH_MM) / 2
    rects = [MmRect(left, baseline, RULER_LENGTH_MM, 0.4)]
    step = 10.0
    for index in range(int(RULER_LENGTH_MM / step) + 1):
        rects.append(MmRect(left + index * step, baseline - 1.5, 0.4, 1.5))
    for rect in rects:
        _refuse_if_obstructed(page, rect, "the calibration ruler")
    return rects


def drawing_to_svg(drawing: Drawing) -> str:
    """Render to SVG with explicit millimetre units, so 1 mm on screen is 1 mm on paper."""
    page = drawing.page
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{page.width_mm}mm" '
        f'height="{page.height_mm}mm" viewBox="0 0 {page.width_mm} {page.height_mm}">',
        f'<rect x="0" y="0" width="{page.width_mm}" height="{page.height_mm}" fill="#ffffff"/>',
    ]
    for image in drawing.images:
        ok, encoded = cv2.imencode(".png", image.grey)
        if not ok:
            raise SheetLayoutError("the picture could not be encoded")
        data = base64.b64encode(encoded.tobytes()).decode("ascii")
        parts.append(
            f'<image x="{image.rect.x:.4f}" y="{image.rect.y:.4f}" '
            f'width="{image.rect.w:.4f}" height="{image.rect.h:.4f}" '
            f'href="data:image/png;base64,{data}"/>'
        )
    for rect in drawing.filled:
        parts.append(
            f'<rect x="{rect.x:.4f}" y="{rect.y:.4f}" width="{rect.w:.4f}" '
            f'height="{rect.h:.4f}" fill="#000000"/>'
        )
    for rect in drawing.outlined:
        parts.append(
            f'<rect x="{rect.x:.4f}" y="{rect.y:.4f}" width="{rect.w:.4f}" '
            f'height="{rect.h:.4f}" fill="none" stroke="#000000" stroke-width="0.3"/>'
        )
    for x, y, text in drawing.labels:
        parts.append(
            f'<text x="{x:.4f}" y="{y:.4f}" font-family="DejaVu Sans, sans-serif" '
            f'font-size="{LABEL_SIZE_MM:g}" fill="#000000">{_escape(text)}</text>'
        )
    for x, y, size, text in drawing.headings:
        parts.append(
            f'<text x="{x:.4f}" y="{y:.4f}" font-family="DejaVu Sans, sans-serif" '
            f'font-size="{size:.2f}" fill="#000000">{_escape(text)}</text>'
        )
    for stroke in drawing.strokes:
        vertices = " ".join(f"{x:.4f},{y:.4f}" for x, y in stroke.vertices)
        parts.append(
            f'<polyline vertices="{vertices}" fill="none" stroke="#000000" '
            f'stroke-width="{stroke.width_mm:.3f}" stroke-linecap="round" '
            'stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def drawing_to_array(
    drawing: Drawing, dpi: int = 300, text: bool = False
) -> NDArray[np.uint8]:
    """Rasterise for tests and previews. Never the print path — printing uses the SVG.

    Text is off by default: it carries no geometry, and words near a cell only add noise
    to detection tests. A preview wants it, and asks. The raster font is OpenCV's Hershey
    and the print font is Helvetica, so a preview shows where the words are and roughly
    how much room they take, not what they will look like.

    Every rectangle comes from the same ``Drawing`` the SVG uses, so the two backends
    cannot disagree about where anything is.
    """
    page = drawing.page
    scale = dpi / _MM_PER_INCH
    width = round(page.width_mm * scale)
    height = round(page.height_mm * scale)
    canvas: NDArray[np.uint8] = np.full((height, width), 255, dtype=np.uint8)

    for image in drawing.images:
        x0 = round(image.rect.x * scale)
        y0 = round(image.rect.y * scale)
        x1 = round(image.rect.right * scale)
        y1 = round(image.rect.bottom * scale)
        if x1 <= x0 or y1 <= y0:
            continue
        canvas[y0:y1, x0:x1] = cv2.resize(
            image.grey, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA
        )
    for rect in drawing.filled:
        x0 = round(rect.x * scale)
        y0 = round(rect.y * scale)
        x1 = round(rect.right * scale)
        y1 = round(rect.bottom * scale)
        canvas[y0:y1, x0:x1] = 0
    for rect in drawing.outlined:
        cv2.rectangle(
            canvas,
            (round(rect.x * scale), round(rect.y * scale)),
            (round(rect.right * scale), round(rect.bottom * scale)),
            color=0,
            thickness=max(1, round(0.3 * scale)),
        )
    for stroke in drawing.strokes:
        vertices = np.array(
            [[round(x * scale), round(y * scale)] for x, y in stroke.vertices], dtype=np.int32
        )
        cv2.polylines(
            canvas,
            [vertices],
            isClosed=False,
            color=0,
            thickness=max(1, round(stroke.width_mm * scale)),
            lineType=cv2.LINE_AA,
        )
    if text:
        _draw_text(canvas, drawing, scale)
    return canvas


# Arial and Liberation Sans carry the same character widths as Helvetica, which is the font
# `drawing_to_pdf` sets. So a preview drawn in one of these puts the words where the print
# will put them, and — the reason this matters more than looks — the ink measured on the
# raster is the ink the page will actually spend. Hershey, the fallback, is a stroke font
# and runs about a third wider and heavier, which overstates both.
_FONT_CANDIDATES: Final = (
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)


def metric_font_path() -> str:
    """The first font on this machine whose widths match the print, or "" for none."""
    from pathlib import Path

    for candidate in _FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return ""


def _draw_text(canvas: NDArray[np.uint8], drawing: Drawing, scale: float) -> None:
    """Set every word on the raster, in one pass, in the closest font this machine has."""
    path = metric_font_path()
    if not path:
        for x, y, label in drawing.labels:
            _put_text(canvas, x, y, LABEL_SIZE_MM, label, scale)
        for x, y, size, heading in drawing.headings:
            _put_text(canvas, x, y, size, heading, scale)
        return

    from PIL import Image, ImageDraw, ImageFont

    sheet = Image.fromarray(canvas)
    pen = ImageDraw.Draw(sheet)
    fonts: dict[int, Any] = {}

    def font_for(size_mm: float) -> Any:
        pixels = max(1, round(size_mm * scale))
        if pixels not in fonts:
            fonts[pixels] = ImageFont.truetype(path, pixels)
        return fonts[pixels]

    for x, y, label in drawing.labels:
        if label:
            pen.text(
                (x * scale, y * scale), label, font=font_for(LABEL_SIZE_MM), fill=0, anchor="ls"
            )
    for x, y, size, heading in drawing.headings:
        if heading:
            pen.text((x * scale, y * scale), heading, font=font_for(size), fill=0, anchor="ls")
    canvas[:, :] = np.asarray(sheet, dtype=np.uint8)


def _put_text(
    canvas: NDArray[np.uint8], x: float, y: float, size_mm: float, text: str, scale: float
) -> None:
    """Hershey at roughly the millimetre height asked for. 21.0 is the divisor that makes
    OpenCV's nominal cap height match a millimetre size, measured with getTextSize."""
    if not text:
        return
    cv2.putText(
        canvas,
        text,
        (round(x * scale), round(y * scale)),
        cv2.FONT_HERSHEY_SIMPLEX,
        size_mm * scale / 21.0,
        color=0,
        thickness=max(1, round(size_mm * scale / 12.0)),
        lineType=cv2.LINE_AA,
    )


def drawing_to_pdf(drawing: Drawing) -> bytes:
    """Write the sheet as a PDF whose page is the paper, one unit per vertex.

    Written by hand rather than through a converter, because every converter in the path
    is another chance for "fit to page" to shrink the geometry the reader measures. Here
    a millimetre becomes 72/25.4 vertices and nothing else touches it. CUPS still rasterises
    for the printer, at 360 dpi, which leaves an ArUco module about 35 pixels across.

    Text is Helvetica in WinAnsi, so it carries Italian accents and nothing wider. A
    character outside that set is dropped rather than shifting the bytes after it.
    """
    page = drawing.page
    scale = 72.0 / _MM_PER_INCH
    height = page.height_mm * scale

    body = ["0 0 0 rg", "0 0 0 RG", "0.85 w"]
    # Pictures first, so a rule or a word drawn over one is on top of it and not under.
    pictures: list[bytes] = []
    for number, image in enumerate(drawing.images):
        rows, cols = image.grey.shape
        pixels = _deflated(image.grey)
        pictures.append(
            b"<< /Type /XObject /Subtype /Image /Width "
            + str(cols).encode()
            + b" /Height "
            + str(rows).encode()
            + b" /ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode /Length "
            + str(len(pixels)).encode()
            + b" >>\nstream\n"
            + pixels
            + b"\nendstream"
        )
        rect = image.rect
        # cm maps the unit square onto the rectangle; q/Q keeps it off everything after.
        body.append(
            f"q {rect.w * scale:.3f} 0 0 {rect.h * scale:.3f} {rect.x * scale:.3f} "
            f"{height - rect.bottom * scale:.3f} cm /Im{number} Do Q"
        )
    for rect in drawing.filled:
        body.append(
            f"{rect.x * scale:.3f} {height - rect.bottom * scale:.3f} "
            f"{rect.w * scale:.3f} {rect.h * scale:.3f} re f"
        )
    for rect in drawing.outlined:
        body.append(
            f"{rect.x * scale:.3f} {height - rect.bottom * scale:.3f} "
            f"{rect.w * scale:.3f} {rect.h * scale:.3f} re S"
        )
    for x, y, text in drawing.labels:
        body.append(_pdf_text(x * scale, height - y * scale, LABEL_SIZE_MM * scale, text))
    for x, y, size, text in drawing.headings:
        body.append(_pdf_text(x * scale, height - y * scale, size * scale, text))
    for stroke in drawing.strokes:
        # Round caps and joins: a chorded circle drawn with butt caps shows its corners.
        body.append(f"{stroke.width_mm * scale:.3f} w 1 J 1 j")
        first_x, first_y = stroke.vertices[0]
        body.append(f"{first_x * scale:.3f} {height - first_y * scale:.3f} m")
        for x, y in stroke.vertices[1:]:
            body.append(f"{x * scale:.3f} {height - y * scale:.3f} l")
        body.append("S")

    # WinAnsi, not ASCII. The font below is declared /WinAnsiEncoding, which is cp1252, so
    # bytes 0x80–0xFF are exactly what it expects. Encoding the stream as ASCII "replace"
    # is what printed `6 ? 2 =` for `6 × 2 =` and `attivit?` for `attività`: the filtering
    # in `_pdf_text` was already correct and this line undid it.
    content = "\n".join(body).encode("cp1252", "replace")
    xobjects = " ".join(f"/Im{number} {6 + number} 0 R" for number in range(len(pictures)))
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page.width_mm * scale:.3f} "
        f"{height:.3f}] /Resources << /Font << /F1 5 0 R >> /XObject << {xobjects} >> >> "
        f"/Contents 4 0 R >>".encode(),
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        *pictures,
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + obj + b"\nendobj\n"
    start = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n"
    ).encode()
    return bytes(out)


def _deflated(grey: NDArray[np.uint8]) -> bytes:
    """Grey rows as a PDF image stream. Raw and deflated, so no decoder is guessed at."""
    return zlib.compress(np.ascontiguousarray(grey, dtype=np.uint8).tobytes(), 6)


def _pdf_text(x: float, y: float, size: float, text: str) -> str:
    body = text.encode("cp1252", "ignore").decode("cp1252")
    escaped = body.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    return f"BT /F1 {size:.2f} Tf {x:.3f} {y:.3f} Td ({escaped}) Tj ET"


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )
