"""The parent may say "now", and what that does not mean.

A press writes one row. The house finds it on its next look and begins an afternoon
whatever the hour says. Nothing is pushed, nothing is woken, and the panel cannot reach
into the house — which is why "now" means "at the next look" and the panel is written to
say so rather than to imply the afternoon has started.

What a press overrides is the day and the hour, and that is the whole list. These tests
exist mostly for the rest of the list: the evening pause still holds, an afternoon already
under way is still not interrupted, and a house with nothing approved still has nothing to
begin. Each of those is a way a "start now" button turns into a system that surprises
somebody in their own house.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from devices import afternoon as clock
from devices.afternoon import BEGIN_NOW, the_standing_request


def _answering(monkeypatch: pytest.MonkeyPatch, standing: dict[str, Any] | None) -> list[str]:
    asked_for: list[str] = []

    def _get(url: str, key: str, timeout: float) -> dict[str, Any]:
        asked_for.append(url)
        if url.endswith("/request"):
            return {"request": standing}
        raise AssertionError(f"nothing should ask for {url}")

    monkeypatch.setattr(clock, "_get", _get)
    return asked_for


def test_a_waiting_press_is_found_and_named_by_its_id(monkeypatch: pytest.MonkeyPatch) -> None:
    _answering(monkeypatch, {"id": "ask_2f9c", "kind": BEGIN_NOW, "subject": "any"})

    assert the_standing_request("https://panel.invalid", "hh_1", "k") == "ask_2f9c"


def test_a_request_of_another_kind_is_not_a_press(monkeypatch: pytest.MonkeyPatch) -> None:
    """The picture channel and this one share a row. Acting on the wrong kind would begin
    an afternoon because somebody asked for a picture back."""
    _answering(monkeypatch, {"id": "ask_2f9c", "kind": "showAgain", "subject": "pic_7"})

    assert the_standing_request("https://panel.invalid", "hh_1", "k") == ""


def test_no_request_is_not_a_press(monkeypatch: pytest.MonkeyPatch) -> None:
    _answering(monkeypatch, None)

    assert the_standing_request("https://panel.invalid", "hh_1", "k") == ""


def test_a_panel_that_will_not_answer_is_the_same_as_no_press(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It must not raise. A house that cannot reach the panel still has its own hours, and
    an exception here would stop the afternoon that was going to begin on time."""

    def _get(url: str, key: str, timeout: float) -> dict[str, Any]:
        raise OSError("no route to host")

    monkeypatch.setattr(clock, "_get", _get)

    assert the_standing_request("https://panel.invalid", "hh_1", "k") == ""


def test_a_press_does_not_reach_past_the_evening_pause() -> None:
    """The hour is overridden; the pause is not.

    `fits_before_the_pause` is what the runner asks after a press as well as before one,
    so an afternoon of ninety minutes at half past nine is still not begun.
    """
    at_2130 = 21 * 60 + 30
    quiet_from, quiet_until = 22 * 60, 7 * 60

    assert clock.fits_before_the_pause(at_2130, 20, quiet_from, quiet_until) is True
    assert clock.fits_before_the_pause(at_2130, 90, quiet_from, quiet_until) is False


def test_a_press_inside_the_pause_begins_nothing() -> None:
    """Half past eleven at night is not a time to start printing."""
    at_2330 = 23 * 60 + 30

    assert clock.fits_before_the_pause(at_2330, 5, 22 * 60, 7 * 60) is False


def test_the_press_is_cleared_by_its_own_id(monkeypatch: pytest.MonkeyPatch) -> None:
    """Cleared by id, so a second press landing while the house was busy survives."""
    posted: list[str] = []

    def _post(url: str, key: str, body: Any, timeout: float) -> dict[str, Any]:
        posted.append(url)
        return {"cleared": True}

    monkeypatch.setattr(clock, "_post", _post)
    clock.the_request_is_done("https://panel.invalid", "hh_1", "k", "ask_2f9c")

    assert posted == ["https://panel.invalid/api/device/hh_1/request/ask_2f9c/done"]


def test_a_press_that_could_not_be_cleared_does_not_undo_the_afternoon(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The afternoon has begun. Raising here would report a failure that did not happen."""

    def _post(url: str, key: str, body: Any, timeout: float) -> dict[str, Any]:
        raise OSError("connection reset")

    monkeypatch.setattr(clock, "_post", _post)
    clock.the_request_is_done("https://panel.invalid", "hh_1", "k", "ask_2f9c")

    assert "not cleared" in capsys.readouterr().out


def test_the_stamp_is_not_what_a_press_has_to_get_past(tmp_path: Path) -> None:
    """A press means "today, again", so the once-a-day stamp cannot be the thing that
    refuses it. This pins the stamp's own behaviour, which the runner then chooses to
    skip; the skipping itself is one `if` in `main` and is read there."""
    stamp = tmp_path / "looked"
    when = 1787654321.0
    clock.mark_looked(stamp, when, "Europe/Rome")

    assert clock.looked_today(stamp, when, "Europe/Rome") is True


def test_a_house_with_nothing_approved_has_nothing_to_begin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A press cannot conjure an afternoon. Approval is still the parent's, made earlier."""
    from devices.house import House

    empty: list[Any] = []
    assert clock.choose(empty, House(printer="p", scanner="s", screen=Path("x"))) is None


def test_the_wire_word_matches_what_the_panel_writes() -> None:
    """The hub does not import the panel, so the two spell this constant separately and a
    test is what keeps them the same word. A mismatch is a button that does nothing."""
    kinds = json.loads(
        json.dumps(
            [
                line.split("=")[1].strip().strip('"')
                for line in Path("panel/requests.py").read_text(encoding="utf-8").splitlines()
                if line.startswith("KIND_BEGIN_NOW")
            ]
        )
    )

    assert kinds == [BEGIN_NOW]
