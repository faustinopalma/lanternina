"""Print a page, and keep the blank so that what comes back can be compared to it.

The keeping is the point, and it is the only thing kept. `ideas/10 §3` reads a page by
handing a model two images — the blank that was printed and what came off the glass — and
asking what is different. So the house has to be able to produce the blank again hours
later, and there is nothing else it needs: no spec, no cells, no id printed on the paper.

**What is on disk is the blank, and never what somebody wrote.** A run keeps a PNG of the
page as it was handed over; the scan that comes back is compared to it and is not stored.
When the afternoon ends, ``_forget`` takes the folder and the blank goes with it.

The picture is composed in, or is absent. A page whose illustration did not arrive prints
anyway, because a cloud that is down should cost a plainer page and not the afternoon.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from printing.ink import check_ink
from printing.page_layout import compose
from printing.render import drawing_to_array, drawing_to_pdf
from shared.experience_checks import Complaint
from shared.ids import SheetId
from shared.page import Page

# CUPS scales to fit by default. Nothing on this page is read back by position any more, so
# a rescale no longer breaks the reading — but a page printed at 94 % is a page whose margins
# are not the margins somebody chose, and the blank kept here would no longer be its twin.
PRINT_OPTIONS = ("-o", "media=A4", "-o", "print-scaling=none", "-o", "sides=one-sided")

# What the blank is kept at. The reader looks at handwriting, and 150 dpi is what the scanner
# path already rectifies to, so the two images arrive at the model the same size.
BLANK_DPI = 150


class TooMuchInk(ValueError):
    """The page would cost more ink than the budget allows, and was not printed."""

    def __init__(self, complaints: tuple[Complaint, ...]) -> None:
        super().__init__("; ".join(str(one) for one in complaints))
        self.complaints = complaints


def blank_path(directory: Path, sheet_id: SheetId) -> Path:
    return directory / f"{sheet_id}.png"


def remember(directory: Path, sheet_id: SheetId, blank: NDArray[np.uint8]) -> Path:
    """Store the page as it was handed over, which is the only copy that ever exists."""
    directory.mkdir(parents=True, exist_ok=True)
    path = blank_path(directory, sheet_id)
    temporary = path.with_suffix(".png.tmp")
    ok, encoded = cv2.imencode(".png", blank)
    if not ok:
        raise ValueError("the page could not be encoded")
    temporary.write_bytes(encoded.tobytes())
    temporary.replace(path)
    return path


def recall(directory: Path, sheet_id: SheetId) -> NDArray[np.uint8]:
    """The blank a page came from. Missing is an error, not an empty page."""
    path = blank_path(directory, sheet_id)
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"no blank was kept for {sheet_id}")
    return np.asarray(image, dtype=np.uint8)


def compose_page(
    page: Page,
    picture: NDArray[np.uint8] | None,
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
) -> tuple[NDArray[np.uint8], bytes]:
    """Compose, measure, remember, and return the blank raster and the PDF.

    Raises :class:`TooMuchInk` before anything is written, so a page over the budget costs
    no paper and leaves nothing behind to explain later.
    """
    drawing = compose(page, picture)
    complaints = check_ink(page, drawing)
    if complaints:
        raise TooMuchInk(complaints)
    blank = drawing_to_array(drawing, dpi=BLANK_DPI, text=True)
    remember(sheets_dir, sheet_id, blank)
    return blank, drawing_to_pdf(drawing)


def compose_and_print(
    page: Page,
    picture: NDArray[np.uint8] | None,
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
    printer: str,
    send: bool = True,
) -> NDArray[np.uint8]:
    """Put the page on paper, and hand back the blank it was printed from."""
    blank, pdf = compose_page(page, picture, sheets_dir=sheets_dir, sheet_id=sheet_id)
    if send:
        subprocess.run(
            ["lp", "-d", printer, *PRINT_OPTIONS, "-t", f"lanternina-{sheet_id}", "-"],
            input=pdf,
            check=True,
        )
    return blank
