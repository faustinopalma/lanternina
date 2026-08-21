"""The house's own clock for afternoons: when it looks, when it begins one, when it asks.

No network and no hardware. The panel is four functions this module replaces, the display
is a file, and the printer is a name nothing is sent to. What is checked is the decision —
which is the part that is new, and the part where a rule gets bent if nobody looks.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pytest

from devices import afternoon as clock
from devices.afternoon import (
    DAYS,
    fits_before_the_pause,
    its_moment,
    looked_today,
    mark_looked,
)
from devices.house import House
from devices.run_experience import forget_what_is_over, load_experience, waiting_runs
from shared.experience import Experience

THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")

# Half past three in the afternoon, local time, on a day the calendar names for us rather
# than one this file asserts the weekday of.
WHEN = time.mktime((2026, 8, 19, 15, 30, 0, 0, 0, -1))
THAT_DAY = DAYS[time.localtime(WHEN).tm_wday]
SOME_OTHER_DAY = DAYS[(time.localtime(WHEN).tm_wday + 1) % 7]


def an_experience() -> Experience:
    return load_experience(THE_AFTERNOON)


@pytest.fixture
def house(tmp_path: Path) -> House:
    return House(
        printer="paper",
        scanner="glass",
        screen=tmp_path / "screen.bmp",
        sheets_dir=tmp_path / "sheets",
        panel="https://panel.example",
        household="hh_1",
        device_key="k",
    )


def a_rhythm(**changes: Any) -> dict[str, Any]:
    rhythm: dict[str, Any] = {
        "afternoonDays": [THAT_DAY],
        "afternoonFrom": "15:00",
        "quietFrom": "22:00",
        "quietUntil": "07:00",
    }
    rhythm.update(changes)
    return rhythm


# ── When the house may begin one at all ──────────────────────────────────────────────


def test_a_house_told_nothing_begins_nothing() -> None:
    """The default is no day. A feature that arrives switched on has decided something the
    parent has not."""
    assert not its_moment(a_rhythm(afternoonDays=[]), time.localtime(WHEN))


def test_it_is_the_day_and_the_hour_or_it_is_neither() -> None:
    assert its_moment(a_rhythm(), time.localtime(WHEN))
    assert not its_moment(a_rhythm(afternoonDays=[SOME_OTHER_DAY]), time.localtime(WHEN))
    assert not its_moment(a_rhythm(afternoonFrom="16:00"), time.localtime(WHEN))


def test_an_afternoon_may_begin_only_if_the_whole_of_it_is_over_before_the_pause() -> None:
    """This is why there is no second hour to set. The pause the parent already chose is
    the end, and the afternoon's own length says whether it fits."""
    pause, until = 22 * 60, 7 * 60
    assert fits_before_the_pause(15 * 60, 180, pause, until)
    assert not fits_before_the_pause(20 * 60 + 30, 180, pause, until)
    # Inside the pause already: nothing begins, whatever the day says.
    assert not fits_before_the_pause(23 * 60, 30, pause, until)
    # Equal ends mean the parent turned the pause off, so nothing is in the way.
    assert fits_before_the_pause(23 * 60, 300, 60, 60)


def test_the_stamp_holds_a_date_and_not_a_tally(tmp_path: Path) -> None:
    stamp = tmp_path / "looked.stamp"
    assert not looked_today(stamp, WHEN)
    mark_looked(stamp, WHEN)

    assert looked_today(stamp, WHEN)
    assert not looked_today(stamp, WHEN + 26 * 3600)
    assert stamp.read_text(encoding="utf-8").strip() == "2026-08-19"


def test_a_run_that_found_nothing_to_do_does_not_use_up_the_day(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """An afternoon approved at four o'clock begins at ten past, not tomorrow. Nothing was
    spent on a run that only found the parent had not decided yet."""
    offered: list[dict[str, Any]] = []
    calls = a_panel(monkeypatch, offered=offered, waiting=1)

    a_turn(monkeypatch, house, WHEN)
    assert not (house.sheets_dir / "afternoon-looked.stamp").exists()

    offered.append(offered_row())
    a_turn(monkeypatch, house, WHEN + 600)

    assert calls["looked"] == 2
    assert calls["begun"] == ["aftn-1"]


# ── What the runner leaves behind, and who clears it ─────────────────────────────────


def a_run(house: House, run_id: str, started_at: float) -> Path:
    runs = house.sheets_dir / "afternoons"
    runs.mkdir(parents=True, exist_ok=True)
    path = runs / f"{run_id}.json"
    path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "started_at": started_at,
                "waiting_at": "come-e-tornato",
                "experience": an_experience().to_dict(),
                "segment": [],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_a_run_whose_hours_have_passed_is_forgotten_along_with_its_paper(
    house: House,
) -> None:
    """The runner notices the hours when a page arrives, which is the only moment it is
    awake. A run nobody ever brought a page back to would otherwise sit there for good."""
    a_run(house, "aft_old", WHEN - 10 * 3600)
    notes = house.sheets_dir / "afternoons" / "pages"
    notes.mkdir(parents=True)
    (notes / "sh_1.json").write_text(json.dumps({"run_id": "aft_old"}), encoding="utf-8")

    assert waiting_runs(house.sheets_dir) == ["aft_old"]
    assert forget_what_is_over(house.sheets_dir, WHEN) == ["aft_old"]
    assert waiting_runs(house.sheets_dir) == []
    assert not (notes / "sh_1.json").exists()


def test_a_run_still_inside_its_hours_is_left_alone(house: House) -> None:
    a_run(house, "aft_now", WHEN - 600)

    assert forget_what_is_over(house.sheets_dir, WHEN) == []
    assert waiting_runs(house.sheets_dir) == ["aft_now"]


# ── The whole turn ───────────────────────────────────────────────────────────────────


def a_panel(
    monkeypatch: pytest.MonkeyPatch,
    *,
    offered: list[dict[str, Any]],
    waiting: int = 0,
    rhythm: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Stand in for the cloud, and write down every call the house made."""
    calls: dict[str, Any] = {"looked": 0, "devised": 0, "begun": []}

    def _rhythm(panel: str, household: str, key: str) -> dict[str, Any]:
        return a_rhythm() if rhythm is None else rhythm

    def _look(panel: str, household: str, key: str) -> tuple[list[Any], int]:
        calls["looked"] += 1
        return offered, waiting

    def _devise(panel: str, household: str, key: str, house: House) -> str:
        calls["devised"] += 1
        return "something new"

    def _begun(panel: str, household: str, key: str, offered_id: str) -> None:
        calls["begun"].append(offered_id)

    monkeypatch.setattr(clock, "read_rhythm", _rhythm)
    monkeypatch.setattr(clock, "what_the_house_may_run", _look)
    monkeypatch.setattr(clock, "ask_for_one", _devise)
    monkeypatch.setattr(clock, "say_it_began", _begun)
    return calls


def a_turn(monkeypatch: pytest.MonkeyPatch, house: House, when: float) -> int:
    """One run of the timer, with the environment the unit file sets."""
    monkeypatch.setattr(clock.time, "time", lambda: when)
    for name, value in {
        "LANTERNINA_PANEL_URL": house.panel,
        "LANTERNINA_HOUSEHOLD": house.household,
        "LANTERNINA_DEVICE_KEY": house.device_key,
        "LANTERNINA_SHEETS_DIR": str(house.sheets_dir),
        "LANTERNINA_PRINTER": house.printer,
        "LANTERNINA_SCANNER": house.scanner,
        "TRMNL_SCREEN_FILE": str(house.screen),
    }.items():
        monkeypatch.setenv(name, value)
    return clock.main(["--no-paper"])


def offered_row() -> dict[str, Any]:
    return {"id": "aftn-1", "experience": an_experience().to_dict()}


def test_it_begins_the_approved_afternoon_and_tells_the_panel_it_did(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    calls = a_panel(monkeypatch, offered=[offered_row()])

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["begun"] == ["aftn-1"]
    assert len(waiting_runs(house.sheets_dir)) == 1
    assert house.screen.exists()


def test_nothing_happens_on_a_day_nobody_chose(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """Not even the look. A house with no day chosen never touches the network."""
    calls = a_panel(monkeypatch, offered=[offered_row()], rhythm=a_rhythm(afternoonDays=[]))

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["looked"] == 0
    assert waiting_runs(house.sheets_dir) == []


def test_it_looks_once_a_day_and_begins_one_afternoon(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """The next run of the timer must not print a second sheet."""
    calls = a_panel(monkeypatch, offered=[offered_row()])

    a_turn(monkeypatch, house, WHEN)
    running = waiting_runs(house.sheets_dir)
    a_turn(monkeypatch, house, WHEN + 600)

    assert calls["looked"] == 1
    assert waiting_runs(house.sheets_dir) == running


def test_it_asks_for_one_when_there_is_nothing_approved_and_nothing_with_the_parent(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    calls = a_panel(monkeypatch, offered=[], waiting=0)

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["devised"] == 1
    # Devised is not begun. What comes back is pending, so nothing runs today.
    assert waiting_runs(house.sheets_dir) == []


def test_it_does_not_ask_while_one_is_still_with_the_parent(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """A parent who has not read the first one is not handed a second to refuse."""
    calls = a_panel(monkeypatch, offered=[], waiting=1)

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["devised"] == 0


def test_an_afternoon_that_would_run_past_the_pause_does_not_begin(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    calls = a_panel(monkeypatch, offered=[offered_row()], rhythm=a_rhythm(quietFrom="16:00"))

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["begun"] == []
    assert waiting_runs(house.sheets_dir) == []


def test_no_second_afternoon_begins_while_one_is_under_way(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """Even with the day's stamp gone, which is the only other thing holding it back."""
    calls = a_panel(monkeypatch, offered=[offered_row()])
    a_turn(monkeypatch, house, WHEN)
    (house.sheets_dir / "afternoon-looked.stamp").unlink()

    a_turn(monkeypatch, house, WHEN + 600)

    assert calls["looked"] == 1
    assert len(waiting_runs(house.sheets_dir)) == 1


def test_a_parent_who_turns_afternoons_on_is_honoured_by_the_next_run(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """There was a copy of the rhythm on disk here, kept for six hours. The days were
    saved at 15:21 on 21 August 2026 and the house was still deciding on a rhythm read at
    14:02 — nothing happened, and nothing said why."""
    chosen: dict[str, Any] = a_rhythm(afternoonDays=[])
    calls = a_panel(monkeypatch, offered=[offered_row()], rhythm=chosen)

    a_turn(monkeypatch, house, WHEN)
    assert waiting_runs(house.sheets_dir) == []

    chosen["afternoonDays"] = [THAT_DAY]
    a_turn(monkeypatch, house, WHEN + 600)

    assert calls["begun"] == ["aftn-1"]
    assert len(waiting_runs(house.sheets_dir)) == 1
