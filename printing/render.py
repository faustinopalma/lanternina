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

from dataclasses import dataclass
from typing import Final

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

_MM_PER_INCH: Final = 25.4


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
class Drawing:
    """A resolution-independent description of one printable sheet."""

    page: PageGeometry
    filled: tuple[MmRect, ...]
    outlined: tuple[MmRect, ...]
    labels: tuple[tuple[float, float, str], ...]
    # (x, y, size in mm, text): the words on the sheet, which carry no geometry.
    headings: tuple[tuple[float, float, float, str], ...] = ()


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


def build_drawing(spec: SheetSpec, page: PageGeometry | None = None) -> Drawing:
    """Lay ``spec`` out on paper, refusing layouts the reader could not decode."""
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
    for cell in spec.cells:
        area = page.to_page(cell.rect)
        _refuse_if_obstructed(page, area, f"cell {cell.id!r}")
        outlined.append(area)
        if cell.label:
            labels.append((area.x, area.y - 1.5, cell.label))

    filled.extend(_ruler_rects(page))
    ruler_x = (page.width_mm - RULER_LENGTH_MM) / 2
    labels.append(
        (ruler_x, page.height_mm - page.margin_mm - 1.0, f"{RULER_LENGTH_MM:.0f} mm")
    )

    headings: list[tuple[float, float, float, str]] = []
    for heading in spec.headings:
        area = page.to_page(heading.rect)
        _refuse_if_obstructed(page, area, "a printed line")
        headings.append((area.x, area.bottom, heading.size_mm, heading.text))
    return Drawing(page, tuple(filled), tuple(outlined), tuple(labels), tuple(headings))


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
            f'font-size="3" fill="#000000">{_escape(text)}</text>'
        )
    for x, y, size, text in drawing.headings:
        parts.append(
            f'<text x="{x:.4f}" y="{y:.4f}" font-family="DejaVu Sans, sans-serif" '
            f'font-size="{size:.2f}" fill="#000000">{_escape(text)}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def drawing_to_array(drawing: Drawing, dpi: int = 300) -> NDArray[np.uint8]:
    """Rasterise for tests and previews. Never the print path — printing uses the SVG.

    Labels are omitted: they carry no geometry, and text near a cell only adds noise to
    detection tests. Every rectangle comes from the same ``Drawing`` the SVG uses, so the
    two backends cannot disagree about where anything is.
    """
    page = drawing.page
    scale = dpi / _MM_PER_INCH
    width = round(page.width_mm * scale)
    height = round(page.height_mm * scale)
    canvas: NDArray[np.uint8] = np.full((height, width), 255, dtype=np.uint8)

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
    return canvas


def drawing_to_pdf(drawing: Drawing) -> bytes:
    """Write the sheet as a PDF whose page is the paper, one unit per point.

    Written by hand rather than through a converter, because every converter in the path
    is another chance for "fit to page" to shrink the geometry the reader measures. Here
    a millimetre becomes 72/25.4 points and nothing else touches it. CUPS still rasterises
    for the printer, at 360 dpi, which leaves an ArUco module about 35 pixels across.

    Text is Helvetica in WinAnsi, so it carries Italian accents and nothing wider. A
    character outside that set is dropped rather than shifting the bytes after it.
    """
    page = drawing.page
    scale = 72.0 / _MM_PER_INCH
    height = page.height_mm * scale

    body = ["0 0 0 rg", "0 0 0 RG", "0.85 w"]
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
        body.append(_pdf_text(x * scale, height - y * scale, 3.0 * scale, text))
    for x, y, size, text in drawing.headings:
        body.append(_pdf_text(x * scale, height - y * scale, size * scale, text))

    content = "\n".join(body).encode("ascii", "replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page.width_mm * scale:.3f} "
        f"{height:.3f}] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>".encode(),
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
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


def _pdf_text(x: float, y: float, size: float, text: str) -> str:
    body = text.encode("cp1252", "ignore").decode("cp1252")
    escaped = body.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    return f"BT /F1 {size:.2f} Tf {x:.3f} {y:.3f} Td ({escaped}) Tj ET"


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )
