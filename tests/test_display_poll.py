from __future__ import annotations

import pytest

from devices.display_poll import interval_seconds, save_interval
from tests.test_rhythm import DEVICE_KEY, client_for, headers


def test_parent_choice_reaches_device_report_and_local_cache(tmp_path):
    client = client_for()
    household = client.get("/api/me", headers=headers()).json()["householdId"]
    response = client.post("/api/rhythm", headers=headers(), json={
        "picturesFrom": "07:00", "picturesUntil": "22:00", "cadenceMinutes": 60,
        "displayPollMinutes": 30,
    })
    assert response.status_code == 200
    answer = client.post(f"/api/device/{household}/devices", json=[],
                         headers={"X-Device-Key": DEVICE_KEY}).json()
    path = tmp_path / "display-poll.json"
    save_interval(path, answer["displayPollMinutes"])
    assert interval_seconds(path) == 1800


@pytest.mark.parametrize("bad", [None, True, 0, 1441, 1.5, "10"])
def test_invalid_update_preserves_last_good_interval(tmp_path, bad):
    path = tmp_path / "display-poll.json"
    save_interval(path, 10)
    with pytest.raises(ValueError):
        save_interval(path, bad)
    assert interval_seconds(path) == 600


def test_missing_cache_uses_existing_configuration(tmp_path):
    assert interval_seconds(tmp_path / "missing") is None
    assert interval_seconds(None) is None


def test_individual_intervals_and_legacy_cache(tmp_path):
    path = tmp_path / "display-poll.json"
    path.write_text('{"minutes": 17}', encoding="utf-8")
    assert interval_seconds(path, "first") == 1020
    save_interval(path, 17, [
        {"id": "first", "kind": "display", "displayPollMinutes": 5},
        {"id": "second", "kind": "display", "displayPollMinutes": 30},
    ])
    assert interval_seconds(path, "first") == 300
    assert interval_seconds(path, "second") == 1800
    assert interval_seconds(path, "unknown") == 1020
    with pytest.raises(ValueError):
        save_interval(path, 17, [
            {"id": "first", "kind": "display", "displayPollMinutes": 0},
        ])
    assert interval_seconds(path, "first") == 300