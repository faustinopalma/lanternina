"""The hub's half of the reminders: deciding the moment, and putting it on a display.

The panel's half was tested on 19 August 2026 — a sentence stored, read once, placed in
the day or turned into a question. What is tested here is what happens next, and the part
that needed care is not the arithmetic on the clock. It is that nothing in this path can
say whether anybody pressed anything.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pytest

from devices import show_reminders
from devices.inventory import save_jobs
from devices.trmnl_byos import reminder_for, validate_screen

FRIENDLY = "CF7D04"
OTHER = "FB9F18"


def clock(wall: str) -> time.struct_time:
    return time.strptime(wall, "%Y-%m-%d %H:%M")


def epoch_of(wall: str) -> float:
    """The same wall time as a timestamp, so a test reads the same on any machine."""
    return time.mktime(clock(wall))


def reminder(at: str, text: str, days: list[str] | None = None, **rest: Any) -> dict[str, Any]:
    return {
        "id": rest.get("id", f"rm_{at.replace(':', '')}"),
        "text": text,
        "at": at,
        "days": days or [],
        "words": rest.get("words", []),
    }


TEETH = reminder("13:30", "lavarsi i denti dopo pranzo")
MEDICINE = reminder("07:00", "lavarsi i denti e prendere la medicina prima di uscire")


def test_the_days_agree_with_the_panel() -> None:
    """Two copies of the same seven words, because the hub cannot import the panel.

    The panel decides which days a sentence applies to and writes them; the hub reads
    them against its own calendar. A disagreement would silently show every reminder on
    the wrong days, which is exactly the kind of fault nobody reports.
    """
    from panel.reminders import DAYS

    assert show_reminders.DAYS == DAYS


def test_a_reminder_is_due_from_its_hour_until_its_window_closes() -> None:
    assert show_reminders.due_now([TEETH], clock("2026-08-20 13:29")) is None
    assert show_reminders.due_now([TEETH], clock("2026-08-20 13:30")) == TEETH
    assert show_reminders.due_now([TEETH], clock("2026-08-20 13:59")) == TEETH
    assert show_reminders.due_now([TEETH], clock("2026-08-20 14:00")) is None


def test_a_reminder_for_some_days_only_is_left_alone_on_the_others() -> None:
    # 20 August 2026 is a Thursday.
    only_wednesday = reminder("13:30", "porta fuori il bidone", ["wed"])
    assert show_reminders.due_now([only_wednesday], clock("2026-08-20 13:35")) is None
    assert show_reminders.due_now([only_wednesday], clock("2026-08-19 13:35")) == only_wednesday


def test_the_hour_that_has_just_come_wins_over_one_still_inside_its_window() -> None:
    """At 13:35 a reminder for 13:30 is more of this moment than one for 13:10."""
    earlier = reminder("13:10", "prima cosa")
    assert show_reminders.due_now([earlier, TEETH], clock("2026-08-20 13:35")) == TEETH
    assert show_reminders.due_now([TEETH, earlier], clock("2026-08-20 13:35")) == TEETH


def test_an_hour_that_is_not_an_hour_is_left_out_rather_than_raising() -> None:
    noon = clock("2026-08-20 13:35")
    assert show_reminders.due_now([reminder("half past one", "x")], noon) is None
    assert show_reminders.due_now([{"id": "r", "text": "x"}], noon) is None


@pytest.fixture
def house(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A hub with one display told to show reminders and one told to show pictures."""
    screen = tmp_path / "screen.bmp"
    jobs = tmp_path / "jobs.json"
    save_jobs(
        jobs,
        [
            {"id": "94:A9:90:CF:7D:04", "label": FRIENDLY, "jobs": ["picture", "remind"]},
            {"id": "E8:3D:C1:FB:9F:18", "label": OTHER, "jobs": ["picture"]},
        ],
    )
    monkeypatch.setenv("LANTERNINA_PANEL_URL", "http://panel.invalid")
    monkeypatch.setenv("LANTERNINA_HOUSEHOLD", "hh_test")
    monkeypatch.setenv("LANTERNINA_DEVICE_KEY", "k")
    monkeypatch.setenv("TRMNL_SCREEN_FILE", str(screen))
    monkeypatch.setenv("LANTERNINA_JOBS_FILE", str(jobs))
    return screen


def run_at(
    monkeypatch: pytest.MonkeyPatch, wall: str, answer: list[dict[str, Any]] | None
) -> int:
    monkeypatch.setattr(show_reminders.time, "time", lambda: epoch_of(wall))
    monkeypatch.setattr(
        show_reminders, "ask_panel", lambda *_args, **_kwargs: answer
    )
    return show_reminders.main()


def test_the_reminder_reaches_the_display_that_holds_the_job_and_no_other(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert run_at(monkeypatch, "2026-08-20 13:35", [TEETH, MEDICINE]) == 0

    drawn = reminder_for(house, FRIENDLY)
    assert validate_screen(drawn), "the display cannot render what it was given"
    assert not reminder_for(house, OTHER).exists(), "this one only shows the pictures"


def test_the_window_closing_takes_it_down_and_nothing_replaces_it(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A reminder nobody pressed is shown until its window closes and is then simply not
    shown. It is not repeated, not made louder, and nobody is told."""
    run_at(monkeypatch, "2026-08-20 13:35", [TEETH])
    assert reminder_for(house, FRIENDLY).exists()

    run_at(monkeypatch, "2026-08-20 14:05", [TEETH])
    assert not reminder_for(house, FRIENDLY).exists()


def test_a_reminder_that_was_seen_does_not_come_back(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The press takes the file away. Putting it back would make the press mean nothing,
    and would be indistinguishable from nagging somebody who already did the thing."""
    run_at(monkeypatch, "2026-08-20 13:35", [TEETH])
    reminder_for(house, FRIENDLY).unlink()  # what a press does

    run_at(monkeypatch, "2026-08-20 13:36", [TEETH])
    assert not reminder_for(house, FRIENDLY).exists()

    # And the next day is a new moment, not a repeat of the one that was dealt with.
    run_at(monkeypatch, "2026-08-21 13:35", [TEETH])
    assert reminder_for(house, FRIENDLY).exists()


def test_nothing_kept_can_tell_a_dismissed_reminder_from_one_still_standing(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The guarantee the whole feature is judged on, and it is structural rather than
    careful: after a press and after no press, what the hub has written down is the same
    bytes. There is nowhere an adherence score could accumulate even by accident.
    """
    state = house.with_name("reminders-shown.json")
    run_at(monkeypatch, "2026-08-20 13:35", [TEETH])
    untouched = state.read_bytes()

    reminder_for(house, FRIENDLY).unlink()  # somebody pressed the button
    run_at(monkeypatch, "2026-08-20 13:40", [TEETH])
    assert state.read_bytes() == untouched

    kept = json.loads(state.read_text(encoding="utf-8"))
    assert set(kept) == {"displays"}
    assert set(kept["displays"]) == {FRIENDLY}


def test_a_panel_that_cannot_be_reached_leaves_the_house_working(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reduced capability, not a stopped house: the reminders already known still appear,
    and only a sentence written since is missed."""
    run_at(monkeypatch, "2026-08-20 13:35", [TEETH])
    reminder_for(house, FRIENDLY).unlink()

    assert run_at(monkeypatch, "2026-08-20 13:45", None) == 0
    # The cache is more than five minutes old, the panel refused, and the reminder the
    # house already had is still the one it is working from.
    assert show_reminders.load_cache(house.with_name("reminders.json"))[0] == [TEETH]


def test_a_house_where_nobody_shows_reminders_asks_nothing_and_touches_nothing(
    tmp_path: Path, house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A job nobody has handed out costs nothing, which is what makes it safe to install
    this before the parent has been to the panel."""
    save_jobs(tmp_path / "jobs.json", [{"id": "x", "label": OTHER, "jobs": ["picture"]}])
    asked: list[str] = []

    monkeypatch.setattr(show_reminders.time, "time", lambda: epoch_of("2026-08-20 13:35"))
    monkeypatch.setattr(
        show_reminders, "ask_panel", lambda *a, **k: asked.append("asked") or []
    )
    assert show_reminders.main() == 0
    assert asked == [], "the panel must not be woken for a job nobody handed out"
    assert not house.with_name("reminders-shown.json").exists()


def test_the_hub_never_hears_of_a_sentence_it_could_not_place(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The panel sends only reminders with an hour. A sentence it could not place stays a
    question for the parent, and never becomes something shown to somebody at a guess."""
    run_at(monkeypatch, "2026-08-20 13:35", [TEETH])
    kept, _at = show_reminders.load_cache(house.with_name("reminders.json"))
    assert all(row["at"] for row in kept)


# ── The words on the screen ──────────────────────────────────────────────────────────

WORDED = reminder(
    "13:30",
    "lavarsi i denti dopo pranzo",
    words=["È ora dei denti.", "Un minuto per i denti.", "I denti, quando ti va."],
)


def test_the_screen_carries_a_generated_wording_and_not_the_parents_sentence() -> None:
    occurrence = show_reminders.occurrence_of(WORDED, clock("2026-08-20 13:35"))
    assert show_reminders.words_of(WORDED, occurrence) in WORDED["words"]


def test_a_reminder_with_no_wordings_is_shown_as_the_parent_wrote_it() -> None:
    """Which is what this did before any wording existed, so a cloud that would not word
    it and a gate that refused it both cost the variety and nothing else."""
    occurrence = show_reminders.occurrence_of(TEETH, clock("2026-08-20 13:35"))
    assert show_reminders.words_of(TEETH, occurrence) == "lavarsi i denti dopo pranzo"
    assert show_reminders.words_of({"text": "x", "words": []}, occurrence) == "x"


def test_one_showing_keeps_one_wording_from_one_minute_to_the_next() -> None:
    """The timer fires every minute in a fresh process. Picking from the occurrence rather
    than at random is what stops the words changing under somebody who is reading them."""
    at_thirty = show_reminders.occurrence_of(WORDED, clock("2026-08-20 13:30"))
    at_forty = show_reminders.occurrence_of(WORDED, clock("2026-08-20 13:40"))
    assert at_thirty == at_forty
    assert show_reminders.words_of(WORDED, at_thirty) == show_reminders.words_of(
        WORDED, at_forty
    )


def test_the_wording_is_the_same_in_any_process() -> None:
    """The built-in hash is salted per process, so a digest is not a preference here."""
    occurrence = show_reminders.occurrence_of(WORDED, clock("2026-08-20 13:35"))
    assert show_reminders.words_of(WORDED, occurrence) == "I denti, quando ti va."


def test_the_days_do_not_all_get_the_same_words() -> None:
    """Three wordings and a fortnight: the point of generating them is that a reminder is
    not the same screen for the two hundredth time."""
    chosen = {
        show_reminders.words_of(
            WORDED, show_reminders.occurrence_of(WORDED, clock(f"2026-08-{day:02d} 13:35"))
        )
        for day in range(1, 15)
    }
    assert len(chosen) == 3


def test_the_wordings_change_nothing_about_what_the_hub_writes_down(
    house: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The guarantee is structural and it has to survive the words getting richer: after
    a press and after no press, the bytes are still the same."""
    state = house.with_name("reminders-shown.json")
    run_at(monkeypatch, "2026-08-20 13:35", [WORDED])
    untouched = state.read_bytes()

    reminder_for(house, FRIENDLY).unlink()  # somebody pressed the button
    run_at(monkeypatch, "2026-08-20 13:40", [WORDED])
    assert state.read_bytes() == untouched

    kept = json.loads(state.read_text(encoding="utf-8"))
    assert set(kept) == {"displays"}
    assert set(kept["displays"]) == {FRIENDLY}
