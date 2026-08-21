"""When the display may change, and how often.

Two things used to be constants: the quiet window and the spacing between pictures. The
tests worth having are the ones about what happens at the edges — a window that wraps past
midnight, a window turned off, and a hub that cannot reach the panel at all. The last one
matters most: an unreachable panel must leave the house working, not stopped.

Both are minutes now rather than whole hours, which adds one claim worth holding down: a
spacing the panel accepts has to be a spacing the timer can actually deliver.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from devices.pull_picture import due, read_rhythm
from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.rhythm import (
    MAX_CADENCE_MINUTES,
    MIN_CADENCE_MINUTES,
    InMemoryRhythmStore,
    clean_rhythm,
    in_quiet_window,
)
from panel.store import InMemoryAccountStore

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
REPO = Path(__file__).resolve().parent.parent


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            rhythm=InMemoryRhythmStore(),
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def test_a_household_that_never_chose_still_has_a_rhythm() -> None:
    """The hub has to be able to run before anyone has opened the panel."""
    client = client_for()
    answer = client.get("/api/rhythm", headers=headers()).json()
    assert answer["quietFrom"] == "22:00"
    assert answer["quietUntil"] == "07:00"
    assert answer["cadenceMinutes"] == 60


def test_what_the_parent_chose_is_what_the_hub_is_told() -> None:
    """Thirteen minutes, and a pause that starts at half past. Neither is a round number
    and neither may be rounded into one."""
    client = client_for()
    household = str(client.get("/api/me", headers=headers()).json()["householdId"])

    written = client.post(
        "/api/rhythm",
        json={"quietFrom": "21:30", "quietUntil": "07:45", "cadenceMinutes": 13},
        headers=headers(),
    )
    assert written.status_code == 200

    device = client.get(
        f"/api/device/{household}/rhythm", headers={"X-Device-Key": DEVICE_KEY}
    ).json()
    assert (device["quietFrom"], device["quietUntil"], device["cadenceMinutes"]) == (
        "21:30",
        "07:45",
        13,
    )


def test_the_hub_cannot_read_the_rhythm_without_the_device_key() -> None:
    client = client_for()
    household = str(client.get("/api/me", headers=headers()).json()["householdId"])
    assert client.get(f"/api/device/{household}/rhythm").status_code == 403


@pytest.mark.parametrize(
    "body",
    [
        {"quietFrom": "24:00", "quietUntil": "07:00", "cadenceMinutes": 60},
        {"quietFrom": "22:60", "quietUntil": "07:00", "cadenceMinutes": 60},
        {"quietFrom": "22", "quietUntil": "07:00", "cadenceMinutes": 60},
        {"quietFrom": "", "quietUntil": "07:00", "cadenceMinutes": 60},
        {"quietFrom": "22:00", "quietUntil": "sera", "cadenceMinutes": 60},
        {"quietFrom": "22:00", "quietUntil": "07:00", "cadenceMinutes": 0},
        {"quietFrom": "22:00", "quietUntil": "07:00", "cadenceMinutes": 1441},
    ],
)
def test_a_rhythm_that_cannot_be_honoured_is_refused(body: dict[str, object]) -> None:
    client = client_for()
    assert client.post("/api/rhythm", json=body, headers=headers()).status_code in (400, 422)


def test_the_timer_asks_often_enough_for_the_finest_spacing_offered() -> None:
    """The panel must not offer a spacing the hub cannot deliver. The unit file is where
    that promise is kept, so the unit file is what this reads."""
    unit = (REPO / "deploy" / "lanternina-picture.timer").read_text(encoding="utf-8")
    assert "OnCalendar=*:*:00" in unit, "the timer no longer fires once a minute"
    assert MIN_CADENCE_MINUTES == 1
    assert MAX_CADENCE_MINUTES == 24 * 60


def test_a_spacing_of_no_minutes_is_refused() -> None:
    with pytest.raises(ValueError):
        clean_rhythm("h1", quiet_from="22:00", quiet_until="07:00", cadence_minutes=0)


# ── The two settings that say when an afternoon may begin ────────────────────────────


def test_a_household_that_never_chose_has_no_day_for_an_afternoon() -> None:
    """The feature arrives switched off. A default that begins one would be this program
    deciding something the parent has not."""
    client = client_for()
    answer = client.get("/api/rhythm", headers=headers()).json()
    assert answer["afternoonDays"] == []
    assert answer["afternoonFrom"] == "15:00"
    assert answer["dayChoices"] == ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def test_the_days_reach_the_hub_in_week_order_and_without_repeats() -> None:
    client = client_for()
    household = str(client.get("/api/me", headers=headers()).json()["householdId"])

    client.post(
        "/api/rhythm",
        json={
            "quietFrom": "22:00",
            "quietUntil": "07:00",
            "cadenceMinutes": 60,
            "afternoonDays": ["sat", "wed", "wed"],
            "afternoonFrom": "16:20",
        },
        headers=headers(),
    )

    device = client.get(
        f"/api/device/{household}/rhythm", headers={"X-Device-Key": DEVICE_KEY}
    ).json()
    assert device["afternoonDays"] == ["wed", "sat"]
    assert device["afternoonFrom"] == "16:20"


def test_a_day_that_is_not_a_day_is_refused_rather_than_dropped() -> None:
    """Dropped quietly, it is a day the parent believes they chose."""
    client = client_for()
    refused = client.post(
        "/api/rhythm",
        json={
            "quietFrom": "22:00",
            "quietUntil": "07:00",
            "cadenceMinutes": 60,
            "afternoonDays": ["mercoledi"],
            "afternoonFrom": "15:00",
        },
        headers=headers(),
    )
    assert refused.status_code in (400, 422)


@pytest.mark.parametrize(
    ("minutes", "quiet"),
    [
        (21 * 60 + 29, False),
        (21 * 60 + 30, True),
        (23 * 60, True),
        (0, True),
        (6 * 60, True),
        (7 * 60 + 45, False),
        (12 * 60, False),
    ],
)
def test_the_quiet_window_wraps_past_midnight(minutes: int, quiet: bool) -> None:
    assert in_quiet_window(minutes, 21 * 60 + 30, 7 * 60 + 45) is quiet


def test_equal_ends_turn_the_quiet_window_off() -> None:
    """A parent who wants pictures at any hour has to be able to say so."""
    start = 9 * 60 + 15
    assert [in_quiet_window(m, start, start) for m in (0, 200, 555, 1400)] == [False] * 4


def test_a_daytime_window_does_not_wrap() -> None:
    assert in_quiet_window(10 * 60, 9 * 60 + 30, 17 * 60) is True
    assert in_quiet_window(9 * 60, 9 * 60 + 30, 17 * 60) is False


def test_a_picture_is_not_replaced_before_the_chosen_spacing(tmp_path: Path) -> None:
    screen = tmp_path / "display.bmp"
    screen.write_bytes(b"x")
    # Twelve minutes since the last change: not due at thirteen, due at twelve.
    now = time.time() + 12 * 60
    assert due(screen, 13, now) is False
    assert due(screen, 12, now) is True


def test_the_spacing_tolerates_the_timer_firing_early(tmp_path: Path) -> None:
    """A run that lands a few seconds early would otherwise skip its turn, and thirteen
    minutes would quietly become fourteen."""
    screen = tmp_path / "display.bmp"
    screen.write_bytes(b"x")
    twenty_seconds_early = time.time() + 13 * 60 - 20
    assert due(screen, 13, twenty_seconds_early) is True


def test_an_empty_display_is_always_due(tmp_path: Path) -> None:
    assert due(tmp_path / "nothing-here.bmp", 24 * 60, time.time()) is True


def test_an_unreachable_panel_leaves_the_house_on_its_last_known_rhythm() -> None:
    """Cloud unavailable means reduced capability, never a stopped system."""
    fallback = (23 * 60, 6 * 60 + 30, 45)
    assert read_rhythm("http://127.0.0.1:9", "h1", "key", fallback) == fallback
