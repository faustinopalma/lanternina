"""No cloud, no reading.

The house used to have a second reader underneath the model: arithmetic that counted dark
pixels inside declared rectangles, used when the panel could not be reached and marked
``degraded``. It is in `attic/` since 21 August 2026, and what replaces it is a refusal.

These are the two ways that refusal can be quietly undone — a fallback that returns
something, or a half-parsed answer that looks whole by the time it reaches a display — and
one test each.
"""

from __future__ import annotations

import urllib.error
import urllib.request
from typing import Any

import numpy as np
import pytest

from devices import read_page as module
from devices.read_page import PanelUnreachable, read_page
from shared.ids import CellId, ExerciseId, SheetId
from shared.sheet import CellKind, CellSpec, Rect, SheetSpec

SPEC = SheetSpec(
    sheet_id=SheetId("sh_test"),
    exercise_id=ExerciseId("ex_test"),
    title="Una cosa",
    cells=(
        CellSpec(
            id=CellId("c1"),
            kind=CellKind.CHOICE_BOX,
            rect=Rect(0.1, 0.1, 0.2, 0.05),
            label="sole",
        ),
    ),
    qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
)


def a_page() -> np.ndarray:
    return np.full((40, 40), 255, dtype=np.uint8)


def test_a_house_with_no_panel_does_not_read_the_page() -> None:
    with pytest.raises(PanelUnreachable):
        read_page(a_page(), SPEC, panel="", household="", key="")


def test_a_panel_that_does_not_answer_produces_a_refusal_and_not_a_reading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The failure that matters: a reading arriving from somewhere other than the model."""

    def refuse(*_args: Any, **_kwargs: Any) -> Any:
        raise urllib.error.URLError("no route to host")

    monkeypatch.setattr(urllib.request, "urlopen", refuse)
    with pytest.raises(PanelUnreachable, match="did not answer"):
        read_page(
            a_page(), SPEC, panel="https://panel.invalid", household="hh_1", key="k"
        )


def test_an_answer_that_is_not_a_reading_is_thrown_away_whole(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A half-parsed reading looks exactly like a whole one by the time it is on a display."""

    class Answer:
        def read(self) -> bytes:
            return b'{"cells": [{"nonsense": true}]}'

        def __enter__(self) -> Answer:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: Answer())
    with pytest.raises(PanelUnreachable):
        read_page(
            a_page(), SPEC, panel="https://panel.invalid", household="hh_1", key="k"
        )


def test_there_is_nothing_underneath_that_reads_a_page_from_pixels() -> None:
    """The fallback is gone by absence, not by a flag somebody could set back."""
    assert not hasattr(module, "read_cells")
    assert "vision.read_sheet" not in getattr(module, "__dict__", {})
