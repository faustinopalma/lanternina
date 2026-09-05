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

import re
import subprocess
import time
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

# How long the printer has to take the page before the afternoon stops waiting for it.
# Measured on this house's ET-2870: an A4 sheet is out well inside a minute once the job
# reaches the printer, so this is a backstop and not a target. It is spent only when
# something is wrong, because a job that prints leaves the queue and stops the wait early.
TOOK_THE_PAGE_SECONDS = 120
_ASK_EVERY_SECONDS = 2.0

# `lp` says `request id is Lanternina-19 (1 file(s))` and that id is the only handle there
# is on the job afterwards.
_JOB_ID = re.compile(r"request id is (\S+)")


class PageNotPrinted(RuntimeError):
    """The queue took the page and the printer did not.

    Its own type because it is not a broken house: the printer may be off, asleep or on a
    different network, and the afternoon has words written for a page that never arrives.
    """


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


def _hand_to_cups(pdf: bytes, printer: str, sheet_id: SheetId) -> str:
    """Put the page in the queue and hand back the job id CUPS gave it."""
    try:
        done = subprocess.run(
            ["lp", "-d", printer, *PRINT_OPTIONS, "-t", f"lanternina-{sheet_id}", "-"],
            input=pdf,
            capture_output=True,
            check=True,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        raise PageNotPrinted(f"the queue would not take the page: {exc}") from exc
    found = _JOB_ID.search(done.stdout.decode(errors="replace"))
    if found is None:
        raise PageNotPrinted("the queue took the page without saying which job it is")
    return found.group(1)


def _still_queued(job: str, printer: str) -> bool:
    """Whether the job is still waiting or printing. Unreadable counts as still waiting.

    An error from `lpstat` must not read as "it printed": the whole point here is that
    only positive evidence of leaving the queue is allowed to end the wait.
    """
    try:
        done = subprocess.run(
            ["lpstat", "-W", "not-completed", "-o", printer],
            capture_output=True,
            check=False,
            timeout=15,
        )
    except (subprocess.SubprocessError, OSError):
        return True
    return any(
        line.split(" ", 1)[0] == job
        for line in done.stdout.decode(errors="replace").splitlines()
    )


def _give_up_on(job: str) -> None:
    """Take the job out of the queue, so no page arrives after the afternoon moved on.

    This is the half that is easy to leave out, and leaving it out is what happened on 5
    September 2026: two pages printed 82 minutes late, for an afternoon that had long since
    said they were not coming and was nearly over.
    """
    try:
        subprocess.run(["cancel", job], capture_output=True, check=False, timeout=15)
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"the page could not be taken out of the queue ({exc})")


def print_page(
    drawn: NDArray[np.uint8],
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
    printer: str,
    send: bool = True,
    wait_seconds: float | None = None,
) -> NDArray[np.uint8]:
    """Put the page on paper, and hand back the blank it was printed from.

    **Accepted by the queue is not out of the printer**, and reading the first as the second
    is the defect this waits out. `lp` returns as soon as CUPS has the file, so a printer
    that is off, asleep or on another network leaves the house believing paper is on the
    table: on 5 September 2026 an afternoon ran for an hour and forty asking for a sheet
    that was sitting in the queue the whole time, and the display went up to the last rung
    of help for it. Raises :class:`PageNotPrinted` instead, which the hand above turns into
    the words the afternoon already has for a page that does not arrive.

    The blank goes with it. `waiting` reads the blanks on disk as sheets on the table, so
    one kept for a page nobody has would be a sheet the house waits to see come back.
    """
    blank, pdf = make_sheet(drawn, sheets_dir=sheets_dir, sheet_id=sheet_id)
    if not send:
        return blank
    # Read here rather than bound as a default, so the ceiling is one value and not a copy
    # taken when this module was imported.
    waits = TOOK_THE_PAGE_SECONDS if wait_seconds is None else wait_seconds
    job = _hand_to_cups(pdf, printer, sheet_id)
    give_up_at = time.monotonic() + waits
    while _still_queued(job, printer):
        if time.monotonic() >= give_up_at:
            _give_up_on(job)
            blank_path(sheets_dir, sheet_id).unlink(missing_ok=True)
            raise PageNotPrinted(
                f"the printer did not take the page within {waits:.0f} seconds"
            )
        time.sleep(_ASK_EVERY_SECONDS)
    return blank


def ink_on(sheet: NDArray[np.uint8]) -> float:
    """What the page costs, for the log. Measured and never refused — `ideas/10 §4`."""
    return ink_fraction(sheet)
