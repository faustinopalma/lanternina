"""What the house tells the panel when an afternoon is over, and what it says about paper.

Until 4 September 2026 it told it nothing. The route
``POST /api/device/{h}/what-happened/{run}`` had existed since 28 August, `panel/what_happened.py`
was written and tested behind it, and the string ``what-happened/`` appeared exactly once in
the repository: on the line that defines the route. So both prompt blocks that read those
rows — the last few afternoons, and which way to move on how much to ask for — were
conditional on a store that nothing ever wrote to, and every afternoon devised in production
was written with no history at all.

These are the guarantees for the call that was missing, and the one that matters most is the
last: a sheet handed over and never brought back is reported, and reported as its own thing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from devices import run_experience
from devices.house import House
from devices.run_experience import Afternoon, begin, conclude_what_is_over
from shared.capabilities import ENDED_WAY_OUT, NEVER_CAME_BACK
from shared.experience import Experience

THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")
HOURS = 60.0 * 60.0


@pytest.fixture
def where(tmp_path: Path) -> Path:
    return tmp_path / "pretend"


@pytest.fixture
def house(where: Path) -> House:
    # A panel it can name, so the report is attempted rather than skipped. Nothing reaches
    # the network: the posting function is the thing under test and is replaced.
    return House(
        sheets_dir=where / "state",
        pretend=where,
        panel="https://panel.invalid",
        household="hh_test",
        device_key="k",
    )


def an_experience() -> Experience:
    return Experience.from_dict(json.loads(THE_AFTERNOON.read_text(encoding="utf-8")))


def waiting(house: House) -> Afternoon:
    return Afternoon.from_dict(
        json.loads(sorted((house.sheets_dir / "afternoons").glob("*.json"))[0].read_text("utf-8"))
    )


def over(house: House, experience: Experience) -> list[str]:
    """The two steps of an ending: the way out at T-30, then the close when its own minutes
    are up. Both are needed, which is `conclude_what_is_over`'s own design and not a detail
    of this test — a way out is something somebody does, not something a display finishes."""
    late = experience.minutes * 60.0 + HOURS
    conclude_what_is_over(house, now=late, send=False)
    return conclude_what_is_over(house, now=late + HOURS, send=False)


@pytest.fixture
def filed(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Everything the house would have posted to the what-happened route."""
    posted: list[dict[str, Any]] = []
    real = run_experience.urllib.request.Request

    def _caught(url: str, *args: Any, **kwargs: Any) -> Any:
        if "/what-happened/" in url:
            posted.append(json.loads(kwargs["data"].decode()))
            raise OSError("caught by the test rather than sent")
        return real(url, *args, **kwargs)

    monkeypatch.setattr(run_experience.urllib.request, "Request", _caught)
    return posted


def _a_printer_that_works(monkeypatch: pytest.MonkeyPatch) -> None:
    """A page that draws. Without this the hand_over plays its ``instead`` and the afternoon
    hands over nothing, which is a real path and not the one under test here."""
    import numpy as np

    monkeypatch.setattr(
        "devices.hands.draw_page",
        lambda *_args, **_kwargs: np.full((64, 64), 255, dtype=np.uint8),
    )


def test_an_afternoon_that_ends_is_reported(house: House, filed: list[dict[str, Any]]) -> None:
    """The call that did not exist. Without it the store behind two prompt blocks is empty
    for every real household, for ever, and nothing anywhere says so."""
    experience = an_experience()
    begin(house, experience, now=0.0, send=False)

    over(house, experience)

    assert len(filed) == 1, "the panel was told once, when the afternoon ended"
    said = filed[0]
    assert said["ending"] == ENDED_WAY_OUT
    assert said["experience"]["experience_id"] == experience.experience_id
    assert said["minutes"] > 0
    assert said["reached"]


def test_a_sheet_that_was_handed_over_and_never_came_back_is_reported_as_that(
    house: House, filed: list[dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The parent's own instruction on 4 September 2026: a sheet not returned counts.

    It counts as its own word and not as a blank page, because blank is an act — somebody
    carried the sheet to the glass. ``never`` covers the sheet still on the table, the sheet
    in the bin, the afternoon walked away from, and a scanner nobody has plugged in.
    `shared/profile.py` is where the last of those is guarded against.

    Broken to check: making `_sheets_of` report only ``run.answered`` leaves this afternoon
    reporting no sheets at all, and the whole of the ink axis with nothing behind it.
    """
    experience = an_experience()
    _a_printer_that_works(monkeypatch)
    begin(house, experience, now=0.0, send=False)
    handed_over = waiting(house).printed
    assert handed_over, "this afternoon hands over a sheet before its first collect"

    over(house, experience)

    sheets = filed[0]["sheets"]
    assert len(sheets) == len(handed_over)
    assert [one["came"] for one in sheets] == [NEVER_CAME_BACK] * len(handed_over)


def test_a_house_with_no_panel_still_ends_its_afternoon(
    where: Path, filed: list[dict[str, Any]]
) -> None:
    """A bench house has no panel to name, and reporting must not be able to stop an ending.

    An afternoon that stops without ending is the failure `devices/run_experience.py` calls
    impossible, and it would be an ugly way to reintroduce it: a diagnostic taking down the
    thing it measures.
    """
    bench = House(sheets_dir=where / "state", pretend=where)
    experience = an_experience()
    begin(bench, experience, now=0.0, send=False)

    ended = over(bench, experience)

    assert ended, "the afternoon reached its ending"
    assert filed == []
