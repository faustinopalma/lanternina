from __future__ import annotations

import pytest

from tests.test_pictures import DEVICE_KEY, client_for, headers, household_of


def test_camera_is_listed_with_unknown_battery_and_its_real_timestamp():
    client = client_for()
    household = household_of(client)
    result = client.post(
        f"/api/device/{household}/devices",
        headers={"X-Device-Key": DEVICE_KEY},
        json=[
            {
                "id": "camera",
                "kind": "camera",
                "name": "XIAO",
                "lastSeen": 100,
                "level": "unknown",
                "voltage": None,
            }
        ],
    )
    assert result.status_code == 200
    row = client.get("/api/devices", headers=headers()).json()["devices"][0]
    assert row["kind"] == "camera"
    assert row["voltage"] is None
    assert row["level"] == "unknown"
    assert row["lastSeen"] == 100


def test_camera_voltage_is_preserved_when_a_sensor_is_available():
    client = client_for()
    household = household_of(client)
    client.post(
        f"/api/device/{household}/devices",
        headers={"X-Device-Key": DEVICE_KEY},
        json=[{"id": "camera", "kind": "camera", "level": "low", "voltage": 3.65}],
    )
    row = client.get("/api/devices", headers=headers()).json()["devices"][0]
    assert row["voltage"] == 3.65
    assert row["level"] == "low"


def test_return_selection_filters_roles_and_can_choose_each_device(monkeypatch):
    from devices.inventory import return_device

    things = [
        {"id": "CAM-A", "kind": "camera", "jobs": ["scan"], "name": "Scocca bianca"},
        {"id": "CAM-B", "kind": "camera", "jobs": ["scan"], "name": "Scocca nera"},
        {"id": "CAM-C", "kind": "camera", "jobs": []},
        {"id": "CAM-D", "kind": "camera", "jobs": ["return", "scan"], "forgottenAt": 1},
        {"id": "scanner", "kind": "scanner", "jobs": ["scan"]},
    ]
    seen = set()
    for index in (0, 1, 2):
        def choose(candidates, index=index):
            assert [thing["id"] for thing in candidates] == ["CAM-A", "CAM-B", "scanner"]
            return candidates[index]

        monkeypatch.setattr("devices.inventory.random.choice", choose)
        selected = return_device(things, paper=True)
        seen.add(selected["id"])
        assert selected["name"] == things[index if index < 2 else 4].get("name", "scanner")
    assert seen == {"CAM-A", "CAM-B", "scanner"}
    assert return_device([things[2], things[3]], paper=False) is None
    monkeypatch.setattr("devices.inventory.random.choice", lambda candidates: candidates[0])
    assert return_device([{"id": "CAM", "kind": "camera", "jobs": ["return"]}],
                         paper=True)["id"] == "CAM"
    assert return_device([things[-1]], paper=False) is None


def test_parent_assigns_camera_functions_and_the_hub_receives_them():
    from panel.preferences import Preferences

    client = client_for()
    household = household_of(client)
    client.app.state.preferences.set(Preferences(household_id=household, language="en"))
    endpoint = f"/api/device/{household}/devices"
    device_headers = {"X-Device-Key": DEVICE_KEY}
    report = [{"id": "CAM", "kind": "camera", "name": "XIAO"}]
    client.post(endpoint, headers=device_headers, json=report)
    response = client.post("/api/devices/CAM", headers=headers(),
                           json={"jobs": ["return", "scan"], "name": "Green"})
    assert response.status_code == 200
    result = client.post(endpoint, headers=device_headers, json=report).json()
    assert result["language"] == "en"
    row = next(thing for thing in result["things"] if thing["id"] == "CAM")
    assert row["jobs"] == ["scan"]
    assert row["jobChoices"] == ["scan"]
    assert row["name"] == "Green"
    assert client.post("/api/devices/CAM", headers=headers(), json={"jobs": []}).status_code == 200
    result = client.post(endpoint, headers=device_headers, json=report).json()
    assert result["things"][0]["jobs"] == []


@pytest.mark.parametrize("kind", ["camera", "scanner"])
@pytest.mark.parametrize("jobs", [("scan",), ("return",), ("return", "scan")])
def test_saved_assignments_become_one_removable_function(kind, jobs):
    from panel.devices import Thing, clean_jobs

    thing = Thing(id="device", household_id="hh", kind=kind, jobs=jobs)
    assert thing.to_public()["jobs"] == ["scan"]
    assert thing.to_public()["jobChoices"] == ["scan"]
    assert clean_jobs(kind, jobs) == ("scan",)
    assert clean_jobs(kind, []) == ()
