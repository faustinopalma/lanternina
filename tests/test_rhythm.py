"""When the display may change, and how often.

Two things used to be constants: the quiet window and the spacing between pictures. The
tests worth having are the ones about what happens at the edges — a window that wraps past
midnight, a window turned off, and a hub that cannot reach the panel at all. The last one
matters most: an unreachable panel must leave the house working, not stopped.
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
from panel.rhythm import CADENCE_CHOICES, InMemoryRhythmStore, clean_rhythm, in_quiet_hours
from panel.store import InMemoryAccountStore

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"


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
    assert answer["quietFromHour"] == 22
    assert answer["quietUntilHour"] == 7
    assert answer["cadenceHours"] == 1


def test_what_the_parent_chose_is_what_the_hub_is_told() -> None:
    client = client_for()
    household = str(client.get("/api/me", headers=headers()).json()["householdId"])

    written = client.post(
        "/api/rhythm",
        json={"quietFromHour": 21, "quietUntilHour": 8, "cadenceHours": 3},
        headers=headers(),
    )
    assert written.status_code == 200

    device = client.get(
        f"/api/device/{household}/rhythm", headers={"X-Device-Key": DEVICE_KEY}
    ).json()
    assert (device["quietFromHour"], device["quietUntilHour"], device["cadenceHours"]) == (
        21,
        8,
        3,
    )


def test_the_hub_cannot_read_the_rhythm_without_the_device_key() -> None:
    client = client_for()
    household = str(client.get("/api/me", headers=headers()).json()["householdId"])
    assert client.get(f"/api/device/{household}/rhythm").status_code == 403


@pytest.mark.parametrize(
    "body",
    [
        {"quietFromHour": 24, "quietUntilHour": 7, "cadenceHours": 1},
        {"quietFromHour": -1, "quietUntilHour": 7, "cadenceHours": 1},
        {"quietFromHour": 22, "quietUntilHour": 99, "cadenceHours": 1},
        {"quietFromHour": 22, "quietUntilHour": 7, "cadenceHours": 5},
        {"quietFromHour": 22, "quietUntilHour": 7, "cadenceHours": 0},
    ],
)
def test_a_rhythm_that_cannot_be_honoured_is_refused(body: dict[str, int]) -> None:
    client = client_for()
    assert client.post("/api/rhythm", json=body, headers=headers()).status_code == 400


def test_a_cadence_finer_than_the_timer_is_not_offered() -> None:
    """The hub asks once an hour, so half an hour is a promise we could not keep."""
    assert min(CADENCE_CHOICES) == 1
    with pytest.raises(ValueError):
        clean_rhythm("h1", quiet_from_hour=22, quiet_until_hour=7, cadence_hours=0)


@pytest.mark.parametrize(
    ("hour", "quiet"),
    [(21, False), (22, True), (23, True), (0, True), (6, True), (7, False), (12, False)],
)
def test_the_quiet_window_wraps_past_midnight(hour: int, quiet: bool) -> None:
    assert in_quiet_hours(hour, 22, 7) is quiet


def test_equal_ends_turn_the_quiet_window_off() -> None:
    """A parent who wants pictures at any hour has to be able to say so."""
    assert [in_quiet_hours(hour, 9, 9) for hour in (0, 3, 12, 23)] == [False] * 4


def test_a_daytime_window_does_not_wrap() -> None:
    assert in_quiet_hours(10, 9, 17) is True
    assert in_quiet_hours(8, 9, 17) is False


def test_a_picture_is_not_replaced_before_the_chosen_spacing(tmp_path: Path) -> None:
    screen = tmp_path / "display.bmp"
    screen.write_bytes(b"x")
    now = time.time() + 3600
    # Just inside the three hours the parent asked for, and just outside it.
    assert due(screen, 3, now) is False
    assert due(screen, 1, now) is True


def test_the_spacing_tolerates_the_timer_firing_early(tmp_path: Path) -> None:
    """systemd adds up to five minutes of jitter; a strict comparison would skip a turn
    and silently double the spacing."""
    screen = tmp_path / "display.bmp"
    screen.write_bytes(b"x")
    five_minutes_early = time.time() + 3600 - 5 * 60
    assert due(screen, 1, five_minutes_early) is True


def test_an_empty_display_is_always_due(tmp_path: Path) -> None:
    assert due(tmp_path / "nothing-here.bmp", 24, time.time()) is True


def test_an_unreachable_panel_leaves_the_house_on_its_last_known_rhythm() -> None:
    """Cloud unavailable means reduced capability, never a stopped system."""
    fallback = (23, 6, 2)
    assert read_rhythm("http://127.0.0.1:9", "h1", "key", fallback) == fallback
