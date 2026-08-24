"""Print a page, and keep the blank so that what comes back can be compared to it.

The keeping is the point, and it is the only thing kept. `ideas/10 §3` reads a page by
handing a model two images — the page as it was handed over and what came off the glass —
and asking what is different. So the house has to be able to produce the blank again hours
later, and there is nothing else it needs: no spec, no cells, no code printed on the paper.

**What is on disk is the blank, and never what somebody wrote.** A run keeps a PNG of the
sheet as it was handed over; the scan that comes back is compared to it and is not stored.
When the afternoon ends, ``_forget`` takes the folder and the blank goes with it.

Nothing here lays anything out. The page arrives drawn.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from printing.paper import BLANK_DPI, ink_fraction, to_paper, to_pdf
from shared.ids import SheetId

# CUPS scales to fit by default. Nothing is read back by position any more, so a rescale no
# longer breaks the reading — but a page printed at 94 % has margins nobody chose, and the
# blank kept here would no longer be its twin.
PRINT_OPTIONS = ("-o", "media=A4", "-o", "print-scaling=none", "-o", "sides=one-sided")


def blank_path(directory: Path, sheet_id: SheetId) -> Path:
    return directory / f"{sheet_id}.png"


def remember(directory: Path, sheet_id: SheetId, blank: NDArray[np.uint8]) -> Path:
    """Store the sheet as it was handed over, which is the only copy that ever exists."""
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


def waiting(directory: Path) -> list[SheetId]:
    """The sheets this house has handed out and not yet seen come back, newest last.

    Ordered by when the file was written and not by name: a sheet id is hexadecimal, and
    sorting those alphabetically once gave the second half of an afternoon the first half's
    page.
    """
    if not directory.exists():
        return []
    pages = sorted(directory.glob("*.png"), key=lambda path: path.stat().st_mtime)
    return [SheetId(path.stem) for path in pages]


def make_sheet(
    drawn: NDArray[np.uint8], *, sheets_dir: Path, sheet_id: SheetId
) -> tuple[NDArray[np.uint8], bytes]:
    """Put the drawn page on A4, remember it, and return the blank and the PDF."""
    blank = to_paper(drawn, dpi=BLANK_DPI)
    remember(sheets_dir, sheet_id, blank)
    return blank, to_pdf(drawn)


def print_page(
    drawn: NDArray[np.uint8],
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
    printer: str,
    send: bool = True,
) -> NDArray[np.uint8]:
    """Put the page on paper, and hand back the blank it was printed from."""
    blank, pdf = make_sheet(drawn, sheets_dir=sheets_dir, sheet_id=sheet_id)
    if send:
        subprocess.run(
            ["lp", "-d", printer, *PRINT_OPTIONS, "-t", f"lanternina-{sheet_id}", "-"],
            input=pdf,
            check=True,
        )
    return blank


def ink_on(sheet: NDArray[np.uint8]) -> float:
    """What the page costs, for the log. Measured and never refused — `ideas/10 §4`."""
    return ink_fraction(sheet)
