from __future__ import annotations

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
