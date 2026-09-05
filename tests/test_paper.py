"""One image, one sheet of paper — and the blank that is the only thing kept.

`printing/paper.py` is what is left of printing now that a page arrives drawn: fit it on A4
without stretching it, write a PDF whose page is the paper, and count the ink.
`devices/print_page.py` is the half that touches the disk, and what it holds is the blank —
`ideas/10 §3` reads a page by comparing it to the sheet that was handed over, so that sheet
has to exist and nothing else has to.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
import pytest

from devices import print_page as print_page_module
from devices.print_page import (
    PRINT_OPTIONS,
    PageNotPrinted,
    blank_path,
    make_sheet,
    print_page,
    recall,
    waiting,
)
from printing.paper import (
    A4_HEIGHT_MM,
    A4_WIDTH_MM,
    BLANK_DPI,
    SAFE_MARGIN_MM,
    ink_fraction,
    placed,
    to_paper,
    to_pdf,
)
from shared.ids import SheetId

SHEET = SheetId("sh_page_test")


def a_drawing(rows: int = 1536, cols: int = 1024, grey: int = 255) -> np.ndarray:
    return np.full((rows, cols), grey, dtype=np.uint8)


# ── Onto the paper ───────────────────────────────────────────────────────────────────


def test_a_page_is_fitted_and_never_stretched() -> None:
    """A page drawn 2:3 and squeezed onto A4's 1:1.414 is a page whose lettering leans, and
    nobody would be able to say why it looked wrong."""
    where = placed(a_drawing(1536, 1024))

    assert where.w / where.h == pytest.approx(1024 / 1536, abs=0.001)
    assert where.w <= A4_WIDTH_MM - 2 * SAFE_MARGIN_MM + 0.001
    assert where.h <= A4_HEIGHT_MM - 2 * SAFE_MARGIN_MM + 0.001


def test_a_page_is_centred_on_the_printable_area() -> None:
    where = placed(a_drawing())

    assert where.x == pytest.approx(A4_WIDTH_MM - where.x - where.w, abs=0.001)
    assert where.y == pytest.approx(A4_HEIGHT_MM - where.y - where.h, abs=0.001)


def test_a_wide_drawing_is_fitted_by_its_width_instead() -> None:
    """Nothing says a model returns the shape that was asked for."""
    where = placed(a_drawing(rows=600, cols=1600))

    assert where.w == pytest.approx(A4_WIDTH_MM - 2 * SAFE_MARGIN_MM, abs=0.001)
    assert where.h < A4_HEIGHT_MM - 2 * SAFE_MARGIN_MM


def test_the_sheet_is_the_paper_and_not_the_picture() -> None:
    """A scan arrives as a sheet, margins and all, so the blank it is compared to has to be
    a sheet too. Handing the reader the picture alone would be comparing two different things.
    """
    sheet = to_paper(a_drawing())

    assert sheet.shape == (
        round(A4_HEIGHT_MM * BLANK_DPI / 25.4),
        round(A4_WIDTH_MM * BLANK_DPI / 25.4),
    )
    assert sheet[0, 0] == 255, "the margin is paper"


def test_the_pdf_page_is_a4_to_the_point() -> None:
    """A print queue given a page at its physical size has no reason to rescale it."""
    pdf = to_pdf(a_drawing())

    assert pdf.startswith(b"%PDF")
    assert b"/MediaBox [0 0 595.276 841.890]" in pdf


def test_the_drawing_is_embedded_in_the_pdf_that_goes_to_the_printer() -> None:
    """A page that renders in a preview and not in the PDF is a defect nobody sees until a
    sheet comes out of the printer blank."""
    pdf = to_pdf(a_drawing(64, 64))

    assert b"/Subtype /Image" in pdf
    assert b"/ColorSpace /DeviceGray" in pdf
    assert b"/Im0 Do" in pdf


def test_ink_is_counted_by_tone_and_not_by_dark_pixels() -> None:
    """An inkjet laying a mid-grey pixel spends about half the ink of a black one, and a
    drawing is where the ink goes. A threshold would call a page 100 % or 0 %."""
    assert ink_fraction(np.full((100, 100), 128, dtype=np.uint8)) == pytest.approx(
        0.498, abs=0.005
    )
    assert ink_fraction(np.full((10, 10), 255, dtype=np.uint8)) == 0.0
    assert ink_fraction(np.zeros((10, 10), dtype=np.uint8)) == 1.0


def test_the_print_queue_is_told_not_to_rescale() -> None:
    """Nothing is read back by position any more, so a rescale no longer breaks the reading
    — but a page printed at 94 % has margins nobody chose, and its blank is no longer its
    twin."""
    assert "print-scaling=none" in PRINT_OPTIONS
    assert "media=A4" in PRINT_OPTIONS


# ── The blank, which is the only thing kept ──────────────────────────────────────────


def test_the_blank_is_kept_and_comes_back_the_same(tmp_path: Path) -> None:
    blank, pdf = make_sheet(a_drawing(), sheets_dir=tmp_path, sheet_id=SHEET)

    assert blank_path(tmp_path, SHEET).exists()
    assert np.array_equal(recall(tmp_path, SHEET), blank)
    assert pdf.startswith(b"%PDF")


def test_the_blank_is_the_only_thing_the_folder_holds(tmp_path: Path) -> None:
    """No spec, no cells, no code printed on the paper: a page carries nothing but what it
    is for, so there is nothing else to write down."""
    make_sheet(a_drawing(), sheets_dir=tmp_path, sheet_id=SHEET)

    assert [path.name for path in sorted(tmp_path.iterdir())] == [f"{SHEET}.png"]


def test_a_page_that_was_never_printed_is_an_error_and_not_an_empty_one(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="sh_page_test"):
        recall(tmp_path, SHEET)


def test_the_sheets_handed_out_come_back_newest_last(tmp_path: Path) -> None:
    """By when it came out and not by its name. A sheet id is a random hex string, and
    sorting those alphabetically once gave the second half of an afternoon the first half's
    page — which read as a page that had already been read."""
    import os
    import time

    make_sheet(a_drawing(), sheets_dir=tmp_path, sheet_id=SheetId("sh_ffff0000"))
    time.sleep(0.01)
    make_sheet(a_drawing(), sheets_dir=tmp_path, sheet_id=SheetId("sh_0000ffff"))
    # Nudged apart explicitly: a filesystem whose timestamps are coarse would otherwise
    # decide this test's answer for it.
    os.utime(blank_path(tmp_path, SheetId("sh_0000ffff")), (time.time(), time.time() + 5))

    assert [str(one) for one in waiting(tmp_path)] == ["sh_ffff0000", "sh_0000ffff"]


def test_a_house_that_has_handed_nothing_out_is_waiting_for_nothing(tmp_path: Path) -> None:
    assert waiting(tmp_path / "never-made") == []


# ── Accepted by the queue is not out of the printer ──────────────────────────────────
#
# On 5 September 2026 an afternoon ran for an hour and forty asking for a page that was
# sitting in the CUPS queue the whole time, because `lp` returns as soon as the queue takes
# the file. The display went to the last rung of help for a sheet nobody could fetch. These
# fix the difference between "the queue has it" and "the printer took it".


class _Cups:
    """A printer that answers the two commands, without one being in the room."""

    def __init__(self, *, leaves_after: int, accepts: bool = True) -> None:
        self.leaves_after = leaves_after
        self.accepts = accepts
        self.asked = 0
        self.cancelled: list[str] = []
        self.sent: list[list[str]] = []

    def __call__(self, argv: list[str], **kw: object) -> subprocess.CompletedProcess[bytes]:
        if argv[0] == "lp":
            self.sent.append(argv)
            if not self.accepts:
                raise subprocess.CalledProcessError(1, argv)
            return subprocess.CompletedProcess(
                argv, 0, b"request id is Lanternina-19 (1 file(s))\n", b""
            )
        if argv[0] == "lpstat":
            self.asked += 1
            gone = self.asked > self.leaves_after
            out = b"" if gone else b"Lanternina-19  fausto  100352  Sat 05 Sep 2026\n"
            return subprocess.CompletedProcess(argv, 0, out, b"")
        if argv[0] == "cancel":
            self.cancelled.append(argv[1])
            return subprocess.CompletedProcess(argv, 0, b"", b"")
        raise AssertionError(f"unexpected command: {argv}")


def _cups(monkeypatch: pytest.MonkeyPatch, fake: _Cups) -> None:
    monkeypatch.setattr(print_page_module.subprocess, "run", fake)
    monkeypatch.setattr(print_page_module.time, "sleep", lambda _: None)


def test_a_page_that_leaves_the_queue_is_a_page_that_printed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake = _Cups(leaves_after=2)
    _cups(monkeypatch, fake)

    blank = print_page(a_drawing(), sheets_dir=tmp_path, sheet_id=SHEET, printer="Lanternina")

    assert blank_path(tmp_path, SHEET).exists()
    assert np.array_equal(recall(tmp_path, SHEET), blank)
    assert fake.cancelled == [], "a page that printed must not be cancelled"


def test_a_page_the_printer_never_takes_is_refused_rather_than_reported_as_printed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The defect of 5 September, stated. It never leaves the queue, so it never printed."""
    fake = _Cups(leaves_after=10_000)
    _cups(monkeypatch, fake)

    with pytest.raises(PageNotPrinted, match="did not take the page"):
        print_page(
            a_drawing(),
            sheets_dir=tmp_path,
            sheet_id=SHEET,
            printer="Lanternina",
            wait_seconds=0.0,
        )

    assert fake.cancelled == ["Lanternina-19"], (
        "a page left in the queue arrives after the afternoon has moved on"
    )
    assert not blank_path(tmp_path, SHEET).exists(), (
        "a kept blank is a sheet `waiting` believes is on the table"
    )


def test_a_queue_that_will_not_take_the_page_is_the_same_answer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _cups(monkeypatch, _Cups(leaves_after=0, accepts=False))

    with pytest.raises(PageNotPrinted, match="would not take"):
        print_page(a_drawing(), sheets_dir=tmp_path, sheet_id=SHEET, printer="Lanternina")


def test_a_printer_that_cannot_be_asked_is_not_taken_for_a_printer_that_finished(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`lpstat` failing must not read as "the job is gone, so it printed"."""

    def broken(argv: list[str], **kw: object) -> subprocess.CompletedProcess[bytes]:
        if argv[0] == "lp":
            return subprocess.CompletedProcess(argv, 0, b"request id is Lanternina-19\n", b"")
        if argv[0] == "cancel":
            return subprocess.CompletedProcess(argv, 0, b"", b"")
        raise OSError("lpstat is not here")

    monkeypatch.setattr(print_page_module.subprocess, "run", broken)
    monkeypatch.setattr(print_page_module.time, "sleep", lambda _: None)

    with pytest.raises(PageNotPrinted):
        print_page(
            a_drawing(),
            sheets_dir=tmp_path,
            sheet_id=SHEET,
            printer="Lanternina",
            wait_seconds=0.0,
        )


def test_nothing_is_sent_and_nothing_is_waited_for_when_the_paper_is_off(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`--no-paper` lays the sheet out without a printer being involved at all."""
    fake = _Cups(leaves_after=0)
    _cups(monkeypatch, fake)

    print_page(
        a_drawing(), sheets_dir=tmp_path, sheet_id=SHEET, printer="Lanternina", send=False
    )

    assert fake.sent == []
    assert blank_path(tmp_path, SHEET).exists()
