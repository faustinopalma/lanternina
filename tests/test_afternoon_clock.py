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
    fits_inside_the_band,
    its_moment,
    looked_today,
    mark_looked,
)
from devices.house import House
from devices.run_experience import conclude_what_is_over, load_experience, waiting_runs
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
        "afternoonUntil": "22:00",
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


def test_an_afternoon_may_begin_only_if_the_whole_of_it_is_over_before_the_band_closes() -> None:
    """The band the parent chose is the end, and the afternoon's own length says whether
    it fits. A shorter one may still fit when a longer one does not."""
    opens, closes = 15 * 60, 19 * 60
    assert fits_inside_the_band(15 * 60, 180, opens, closes)
    assert not fits_inside_the_band(17 * 60, 180, opens, closes)
    # A short one still fits in the same gap the long one did not.
    assert fits_inside_the_band(17 * 60, 90, opens, closes)
    # Before it opens and after it closes, nothing begins.
    assert not fits_inside_the_band(14 * 60, 30, opens, closes)
    assert not fits_inside_the_band(19 * 60, 30, opens, closes)


def test_the_stamp_holds_a_date_and_not_a_tally(tmp_path: Path) -> None:
    stamp = tmp_path / "looked.stamp"
    assert not looked_today(stamp, WHEN)
    mark_looked(stamp, WHEN)

    assert looked_today(stamp, WHEN)
    assert not looked_today(stamp, WHEN + 26 * 3600)
    assert stamp.read_text(encoding="utf-8").strip() == "2026-08-19"


def test_a_run_that_found_nothing_to_do_still_begins_one_approved_later(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """An afternoon approved at four o'clock begins at ten past, not tomorrow."""
    offered: list[dict[str, Any]] = []
    calls = a_panel(monkeypatch, offered=offered, waiting=1)

    a_turn(monkeypatch, house, WHEN)

    offered.append(offered_row())
    a_turn(monkeypatch, house, WHEN + 600)

    assert calls["looked"] == 2
    assert calls["begun"] == ["aftn-1"]
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


def test_a_run_whose_hour_has_come_reaches_its_ending_rather_than_being_deleted(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The defect this replaced, and the reason the test is written this way round.

    Until 23 August 2026 a run whose hours had passed was unlinked and nothing was said to
    anybody — measured on the house at 14:02 on 21 August, on `aft_5ec79e85`. That is an
    afternoon that stops without ending, which is the failure the whole project exists to
    prevent. So this asserts what went on the display, in order, and it fails on the old
    behaviour rather than merely passing on the new one.
    """
    said: list[str] = []
    monkeypatch.setattr(
        "devices.hands.show", lambda _h, heading, _lines: said.append(heading)
    )
    experience = an_experience()
    # Twenty minutes left, so the ending has already been due for ten.
    a_run(house, "aft_old", WHEN - (experience.minutes - 20) * 60)
    notes = house.sheets_dir / "afternoons" / "pages"
    notes.mkdir(parents=True)
    (notes / "sh_1.json").write_text(json.dumps({"run_id": "aft_old"}), encoding="utf-8")

    assert waiting_runs(house.sheets_dir) == ["aft_old"]

    # First pass: the way out of wherever it got to, and the run is still there.
    assert conclude_what_is_over(house, WHEN, send=False) == []
    assert said == [experience.moment("come-e-tornato").way_out.heading]
    assert waiting_runs(house.sheets_dir) == ["aft_old"]

    # Second pass, once the way out has had its own minutes: the ending, then nothing left.
    out = experience.moment("come-e-tornato").way_out
    assert conclude_what_is_over(house, WHEN + out.minutes * 60, send=False) == ["aft_old"]
    assert said[-1] == experience.moment("basta-cosi").heading
    assert waiting_runs(house.sheets_dir) == []
    assert not (notes / "sh_1.json").exists()


def test_a_run_still_inside_its_hours_is_left_alone(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    said: list[str] = []
    monkeypatch.setattr(
        "devices.hands.show", lambda _h, heading, _lines: said.append(heading)
    )
    a_run(house, "aft_now", WHEN - 600)

    assert conclude_what_is_over(house, WHEN, send=False) == []
    assert said == [], "nothing was said to anybody about an afternoon still under way"
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
        # The real panel stops offering what has begun, and the runner leans on that to
        # move on to the next one. A fake that kept offering it would show a house
        # beginning the same afternoon twice and call it a pass.
        offered[:] = [row for row in offered if row.get("id") != offered_id]

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


def offered_row(offered_id: str = "aftn-1") -> dict[str, Any]:
    return {"id": offered_id, "experience": an_experience().to_dict()}


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


def test_it_does_not_begin_a_second_while_the_first_is_still_going(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """The next run of the timer must not print a second sheet on top of the first."""
    calls = a_panel(monkeypatch, offered=[offered_row()])

    a_turn(monkeypatch, house, WHEN)
    running = waiting_runs(house.sheets_dir)
    a_turn(monkeypatch, house, WHEN + 600)

    assert calls["looked"] == 1
    assert waiting_runs(house.sheets_dir) == running


def test_a_second_approved_afternoon_begins_when_the_first_has_finished(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """Two approved, the first over by half past four, three hours of band left.

    Until 25 August 2026 the day's stamp meant one afternoon a day whatever else was true,
    so the second waited until tomorrow. A parent watching that happen is the reason this
    test exists; the stamp now gates only the expensive half, asking a model for a new one.
    """
    calls = a_panel(monkeypatch, offered=[offered_row("aftn-1"), offered_row("aftn-2")])

    a_turn(monkeypatch, house, WHEN)
    assert calls["begun"] == ["aftn-1"]

    # The first is over: nothing is waiting on paper any more.
    for left in house.sheets_dir.rglob("*"):
        if left.is_file():
            left.unlink()
    assert waiting_runs(house.sheets_dir) == []

    a_turn(monkeypatch, house, WHEN + 3600)

    assert calls["begun"] == ["aftn-1", "aftn-2"]


def test_it_asks_for_one_when_there_is_nothing_approved_and_nothing_with_the_parent(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    calls = a_panel(monkeypatch, offered=[], waiting=0)

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["devised"] == 1
    # Devised is not begun. What comes back is pending, so nothing runs today.
    assert waiting_runs(house.sheets_dir) == []


def test_it_keeps_a_stock_rather_than_one_at_a_time(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """One unread afternoon used to stop the house devising anything at all, so a parent
    away for a week came back to a single card. It tops up to `STOCK` instead, one a day."""
    calls = a_panel(monkeypatch, offered=[], waiting=1)

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["devised"] == 1


def test_a_full_stock_is_not_topped_up(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """The stock is a ceiling, not a target to keep hitting."""
    calls = a_panel(monkeypatch, offered=[], waiting=clock.STOCK)

    assert a_turn(monkeypatch, house, WHEN) == 0

    assert calls["devised"] == 0


def test_it_asks_for_one_more_only_once_a_day(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    """The timer fires sixty times an hour and devising is a model writing a dozen moments."""
    calls = a_panel(monkeypatch, offered=[], waiting=0)

    a_turn(monkeypatch, house, WHEN)
    a_turn(monkeypatch, house, WHEN + 600)
    a_turn(monkeypatch, house, WHEN + 1200)

    assert calls["devised"] == 1


def test_an_afternoon_that_would_run_past_the_band_does_not_begin(
    monkeypatch: pytest.MonkeyPatch, house: House
) -> None:
    calls = a_panel(
        monkeypatch, offered=[offered_row()], rhythm=a_rhythm(afternoonUntil="16:00")
    )

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
