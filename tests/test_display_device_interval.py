from __future__ import annotations

from panel.cosmos_store import _from_thing, _to_thing
from panel.devices import Thing
from tests.test_rhythm import DEVICE_KEY, client_for, headers


def test_intervals_are_per_display_and_survive_status_and_name_updates():
    client = client_for()
    household = client.get("/api/me", headers=headers()).json()["householdId"]
    report = [{"id": "first", "kind": "display"}, {"id": "second", "kind": "display"},
              {"id": "cam", "kind": "camera"}]
    device_headers = {"X-Device-Key": DEVICE_KEY}
    client.post(f"/api/device/{household}/devices", json=report, headers=device_headers)
    assert client.post("/api/devices/first", headers=headers(), json={
        "displayPollMinutes": 30,
    }).json()["displayPollMinutes"] == 30
    client.post("/api/devices/first", headers=headers(), json={"name": "Display"})
    rows = client.post(f"/api/device/{household}/devices", json=report,
                       headers=device_headers).json()["things"]
    intervals = {row["id"]: row["displayPollMinutes"] for row in rows}
    assert intervals == {"first": 30, "second": 10, "cam": None}
    for invalid in (0, 1441, True, "10", 2.5):
        assert client.post("/api/devices/first", headers=headers(), json={
            "displayPollMinutes": invalid,
        }).status_code == 422
    assert client.post("/api/devices/cam", headers=headers(), json={
        "displayPollMinutes": 20,
    }).status_code == 400


def test_cosmos_document_retains_per_display_interval():
    thing = Thing("display", "house", "display", display_poll_minutes=35)
    assert _to_thing(_from_thing(thing)).display_poll_minutes == 35
    document = _from_thing(thing)
    del document["displayPollMinutes"]
    assert _to_thing(document).display_poll_minutes is None