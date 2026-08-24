"""Printing a page and keeping its blank, which is the only thing a page leaves behind.

The claims here are about what is on disk. A run keeps the blank it printed, because
`ideas/10 §3` reads a page by comparing it to what came off the glass. It keeps nothing
else: no spec, no cells, no copy of what anybody wrote.

`compose_page` is also where the ink budget stops a page, and it stops it before any paper
or any file exists — a page refused after printing would have cost the thing the budget is
about.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from devices.print_page import (
    BLANK_DPI,
    PRINT_OPTIONS,
    TooMuchInk,
    blank_path,
    compose_page,
    recall,
)
from shared.ids import SheetId
from shared.page import Page, PageKind, Room, Space

SHEET = SheetId("sh_page_test")

A_PAGE = Page(
    kind=PageKind.NOTEBOOK,
    title="Il cielo di oggi",
    illustration="clouds over rooftops",
    note=("Guarda fuori, poi riempi quello che vuoi.",),
    spaces=(Space(label="Che forma aveva", room=Room.A_LINE),),
)


def a_picture(side: int = 128, grey: int = 250) -> np.ndarray:
    return np.full((side, side), grey, dtype=np.uint8)


def test_the_blank_is_kept_and_comes_back_the_same_size(tmp_path: Path) -> None:
    """Hours later, the reader wants the page as it was handed over, at the size the scan
    arrives at, so that the two images reach the model alike."""
    blank, pdf = compose_page(A_PAGE, a_picture(), sheets_dir=tmp_path, sheet_id=SHEET)

    assert blank_path(tmp_path, SHEET).exists()
    assert recall(tmp_path, SHEET).shape == blank.shape
    assert blank.shape == (round(297 * BLANK_DPI / 25.4), round(210 * BLANK_DPI / 25.4))
    assert pdf.startswith(b"%PDF")


def test_the_blank_is_the_only_thing_the_folder_holds(tmp_path: Path) -> None:
    """No spec, no cells, no id: a page carries nothing but what it is for, so there is
    nothing else to write down."""
    compose_page(A_PAGE, a_picture(), sheets_dir=tmp_path, sheet_id=SHEET)

    assert [path.name for path in sorted(tmp_path.iterdir())] == [f"{SHEET}.png"]


def test_a_page_whose_picture_never_arrived_is_still_printed(tmp_path: Path) -> None:
    """A cloud that is down costs a plainer page, not the afternoon."""
    blank, pdf = compose_page(A_PAGE, None, sheets_dir=tmp_path, sheet_id=SHEET)

    assert blank_path(tmp_path, SHEET).exists()
    assert b"/Subtype /Image" not in pdf


def test_a_page_over_the_budget_costs_no_paper_and_leaves_no_file(tmp_path: Path) -> None:
    """Refused before anything exists. A page stopped after printing would have spent the
    thing the budget is about."""
    heavy = Page(
        kind=PageKind.LABEL, title="Troppo", illustration="a dark thing", note=("Nera.",)
    )

    with pytest.raises(TooMuchInk, match="%"):
        compose_page(heavy, a_picture(grey=10), sheets_dir=tmp_path, sheet_id=SHEET)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_a_page_that_was_never_printed_is_an_error_and_not_an_empty_one(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="sh_page_test"):
        recall(tmp_path, SHEET)


def test_the_print_queue_is_told_not_to_rescale() -> None:
    """Nothing is read back by position any more, so a rescale no longer breaks the reading
    — but a page printed at 94 % has margins nobody chose, and its blank is no longer its
    twin."""
    assert "print-scaling=none" in PRINT_OPTIONS
    assert "media=A4" in PRINT_OPTIONS
