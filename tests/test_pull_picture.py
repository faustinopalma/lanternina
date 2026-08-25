"""When the hub decides to paint, and what that decision costs in cloud calls.

The tests worth having here are the ones that hold a shape rather than a behaviour: the
spacing the parent chose is honoured to the minute, and the panel is woken only when a
picture is actually being asked for. The second is not a nicety — the panel's API scales
to zero, so a run that touches the network every minute holds a replica awake all day.
"""

from __future__ import annotations

import json
import time
import urllib.error
from pathlib import Path

import pytest

from devices import pull_picture
from devices.pull_picture import (
    CADENCE_GRACE_SECONDS,
    due,
    inside_band,
    load_rhythm,
    minutes_of,
    save_rhythm,
)

FALLBACK = (22 * 60, 7 * 60, 60)


def _environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, screen: Path) -> None:
    for name, value in {
        "LANTERNINA_PANEL_URL": "https://panel.invalid",
        "LANTERNINA_HOUSEHOLD": "h1",
        "LANTERNINA_DEVICE_KEY": "k",
        "TRMNL_SCREEN_FILE": str(screen),
        "LANTERNINA_RHYTHM_FILE": str(tmp_path / "rhythm.json"),
    }.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(
        pull_picture.time, "localtime", lambda: time.struct_time((2026, 8, 19, 12, 0, 0, 0, 0, 0))
    )


def test_the_spacing_is_honoured_to_the_minute(tmp_path: Path) -> None:
    screen = tmp_path / "screen.bmp"
    screen.write_bytes(b"x")
    painted = screen.stat().st_mtime

    assert not due(screen, 15, painted + 10 * 60)
    # The grace is what keeps thirteen minutes from becoming fourteen on a minute timer.
    assert due(screen, 15, painted + 15 * 60 - CADENCE_GRACE_SECONDS)
    assert due(screen, 15, painted + 16 * 60)


def test_nothing_on_the_display_is_always_due(tmp_path: Path) -> None:
    assert due(tmp_path / "never-written.bmp", 1440, time.time())


def test_the_rhythm_survives_between_runs(tmp_path: Path) -> None:
    path = tmp_path / "rhythm.json"
    save_rhythm(path, minutes_of("21:30"), minutes_of("07:15"), 15)
    assert load_rhythm(path) == (21 * 60 + 30, 7 * 60 + 15, 15)


def test_a_damaged_or_missing_copy_reads_as_nothing_known(tmp_path: Path) -> None:
    """Not an error, and not a default either: the caller has to go and ask."""
    path = tmp_path / "rhythm.json"
    path.write_text("{ not json", encoding="utf-8")
    assert load_rhythm(path) is None

    path.write_text(json.dumps({"picturesFrom": 0}), encoding="utf-8")
    assert load_rhythm(path) is None

    assert load_rhythm(tmp_path / "absent.json") is None


def test_the_pause_wraps_around_midnight() -> None:
    start, end = minutes_of("22:00"), minutes_of("07:00")
    assert inside_band(time.struct_time((2026, 8, 19, 23, 30, 0, 0, 0, 0)), start, end)
    assert inside_band(time.struct_time((2026, 8, 19, 3, 0, 0, 0, 0, 0)), start, end)
    assert not inside_band(time.struct_time((2026, 8, 19, 12, 0, 0, 0, 0, 0)), start, end)


def test_a_run_that_is_not_due_never_touches_the_panel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The minute timer must be free. A replica held awake for this would cost all day."""
    screen = tmp_path / "screen.bmp"
    screen.write_bytes(b"x")  # just painted, so nothing is due
    save_rhythm(tmp_path / "rhythm.json", minutes_of("22:00"), minutes_of("07:00"), 15)
    _environment(monkeypatch, tmp_path, screen)

    def refuse(*args: object, **kwargs: object) -> None:
        raise AssertionError("the panel was contacted on a run that had nothing to ask")

    monkeypatch.setattr(pull_picture.urllib.request, "urlopen", refuse)
    assert pull_picture.main() == 0


def test_a_hub_that_knows_no_rhythm_asks_before_deciding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Otherwise the first period after a rebuild runs on a spacing nobody chose."""
    screen = tmp_path / "screen.bmp"
    screen.write_bytes(b"x")
    _environment(monkeypatch, tmp_path, screen)

    asked: list[str] = []

    def answer(request: object, timeout: int = 0) -> object:
        asked.append(str(getattr(request, "full_url", "")))
        raise urllib.error.URLError("no panel reachable in a test")

    monkeypatch.setattr(pull_picture.urllib.request, "urlopen", answer)
    assert pull_picture.main() == 0
    assert asked and asked[0].endswith("/rhythm")


def test_the_picture_goes_to_the_display_that_holds_the_job(tmp_path: Path) -> None:
    """The defect of 19 August 2026, closed at its cause.

    One press created `screen-FB9F18.bmp`, that file took the display over for good, and
    the pictures — written only to the shared file — never reached it again. Addressing the
    display that holds the job is what fixed it.

    It goes to a layer of the picture's own, which is the second half of the same lesson:
    written into the display's shared file, a picture outlived the job that made it.
    """
    from devices.inventory import save_jobs
    from devices.pull_picture import picture_file

    shared = tmp_path / "screen.bmp"
    jobs = tmp_path / "jobs.json"
    save_jobs(
        jobs,
        [
            {"id": "94:A9:90:CF:7D:04", "label": "CF7D04", "job": "picture"},
            {"id": "E8:3D:C1:FB:9F:18", "label": "FB9F18", "job": "sheet"},
        ],
    )

    assert picture_file(shared, jobs) == shared.with_name("screen-CF7D04-picture.bmp")


def test_with_nobody_holding_the_job_the_picture_goes_where_it_always_did(
    tmp_path: Path,
) -> None:
    """An unreachable panel leaves the house working to what it knew, and a house that has
    never reached the panel keeps behaving as it did before there was one."""
    from devices.inventory import save_jobs
    from devices.pull_picture import picture_file

    shared = tmp_path / "screen.bmp"
    assert picture_file(shared, tmp_path / "absent.json") == shared

    jobs = tmp_path / "jobs.json"
    save_jobs(jobs, [{"id": "94:A9:90:CF:7D:04", "label": "CF7D04", "job": ""}])
    assert picture_file(shared, jobs) == shared
