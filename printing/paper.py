"""One image, one sheet of paper. This is the whole of what printing does now.

`printing/render.py` used to be here: page geometry, markers, a QR, rectangles for fields,
text set from strings, three backends that had to agree about where ink landed. It is in
`attic/` with the rest of the machinery that laid pages out, because the page is drawn whole
by a model now and nothing on this side decides where anything goes.

What is left is arithmetic nobody can argue with: fit a picture onto A4 without stretching
it, and write a PDF whose page is the paper so no queue has a reason to rescale.
"""

from __future__ import annotations

import zlib
from dataclasses import dataclass
from typing import Final

import cv2
import numpy as np
from numpy.typing import NDArray

A4_WIDTH_MM: Final = 210.0
A4_HEIGHT_MM: Final = 297.0

# The ET-2870 cannot print to the edge of plain paper, and a page pushed into the unprintable
# strip loses whatever the model drew there. Three millimetres is the usual margin on this
# class of printer; it is chosen from the specification and not measured on the paper.
SAFE_MARGIN_MM: Final = 3.0

# What the blank is kept and compared at. The reader is shown two images — the page as it was
# handed over and what came off the glass — and the scanner path already works at 150 dpi.
BLANK_DPI: Final = 150

_MM_PER_INCH: Final = 25.4


@dataclass(frozen=True, slots=True)
class Placed:
    """Where the picture lands on the paper, in millimetres from the top left."""

    x: float
    y: float
    w: float
    h: float


def placed(picture: NDArray[np.uint8]) -> Placed:
    """The largest upright rectangle the picture fits in, centred on the printable area.

    Fitted rather than stretched. A page drawn 2:3 and squeezed onto A4's 1:1.414 is a page
    whose lettering leans, and nobody would be able to say why it looked wrong.
    """
    rows, cols = picture.shape[:2]
    width = A4_WIDTH_MM - 2 * SAFE_MARGIN_MM
    height = A4_HEIGHT_MM - 2 * SAFE_MARGIN_MM
    scale = min(width / cols, height / rows)
    return Placed(
        x=(A4_WIDTH_MM - cols * scale) / 2,
        y=(A4_HEIGHT_MM - rows * scale) / 2,
        w=cols * scale,
        h=rows * scale,
    )


def to_paper(picture: NDArray[np.uint8], dpi: int = BLANK_DPI) -> NDArray[np.uint8]:
    """The whole sheet as it will print: the picture on A4, the rest white paper.

    This is what is kept as the blank and what the reader is shown, so it has to be the
    sheet and not the picture — a scan arrives as a sheet, margins and all.
    """
    scale = dpi / _MM_PER_INCH
    sheet: NDArray[np.uint8] = np.full(
        (round(A4_HEIGHT_MM * scale), round(A4_WIDTH_MM * scale)), 255, dtype=np.uint8
    )
    where = placed(picture)
    x0, y0 = round(where.x * scale), round(where.y * scale)
    x1, y1 = round((where.x + where.w) * scale), round((where.y + where.h) * scale)
    sheet[y0:y1, x0:x1] = cv2.resize(picture, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
    return sheet


def to_pdf(picture: NDArray[np.uint8]) -> bytes:
    """An A4 PDF holding the picture at its physical size, written by hand.

    By hand rather than through a converter because every converter in the path is another
    chance for "fit to page" to change the size of what somebody drew. Here a millimetre
    becomes 72/25.4 units and nothing else touches it. The image goes in raw and deflated,
    grey, so no decoder is being guessed at either.
    """
    scale = 72.0 / _MM_PER_INCH
    height = A4_HEIGHT_MM * scale
    where = placed(picture)
    rows, cols = picture.shape[:2]
    pixels = zlib.compress(np.ascontiguousarray(picture, dtype=np.uint8).tobytes(), 6)

    content = (
        f"q {where.w * scale:.3f} 0 0 {where.h * scale:.3f} {where.x * scale:.3f} "
        f"{height - (where.y + where.h) * scale:.3f} cm /Im0 Do Q"
    ).encode("ascii")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {A4_WIDTH_MM * scale:.3f} "
        f"{height:.3f}] /Resources << /XObject << /Im0 5 0 R >> >> /Contents 4 0 R >>".encode(),
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /XObject /Subtype /Image /Width "
        + str(cols).encode()
        + b" /Height "
        + str(rows).encode()
        + b" /ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode /Length "
        + str(len(pixels)).encode()
        + b" >>\nstream\n"
        + pixels
        + b"\nendstream",
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


def ink_fraction(sheet: NDArray[np.uint8]) -> float:
    """The share of the paper covered, counting a grey pixel as the ink it actually is.

    Measured and reported, never refused. `ideas/10 §4` records why: the parent has printed
    pages made this way and they are fine, and a page nobody objected to should not be thrown
    away by arithmetic. The number stays because it is the only measurable thing in the brief.
    """
    return float(np.mean(255.0 - sheet.astype(np.float64)) / 255.0)
