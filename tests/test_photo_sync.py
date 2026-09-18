from __future__ import annotations

import pytest

from devices.camera_hub import CameraHub
from devices.house import House
from devices.sync_photos import synchronize
from tests.test_photo_store import PHOTO, jpeg
from tests.test_pictures import DEVICE_KEY, client_for, headers, household_of


def test_hub_sync_shows_photo_and_propagates_parent_deletion(tmp_path):
    client = client_for()
    household = household_of(client)
    hub = CameraHub(
        {"database": str(tmp_path / "photos.db")},
        House(
            panel="https://panel",
            household=household,
            device_key=DEVICE_KEY,
            sheets_dir=tmp_path,
        ),
        tmp_path / "screen.bmp",
    )
    hub.store.accept(PHOTO, "cam", jpeg(), captured=100, target=None)
    hub.store.record_camera(
        {
            "id": "cam",
            "kind": "camera",
            "model": "Waveshare ESP32-S3-CAM-OV5640",
            "name": "Waveshare cam",
            "lastSeen": 100,
            "diagnostics": {"phase": "sleep_planned", "previousSleepConfirmed": False},
        }
    )

    def ask(url, body, **kwargs):
        response = client.post(
            url.removeprefix("https://panel"), json=body, headers={"X-Device-Key": kwargs["key"]}
        )
        assert response.status_code == 200, response.text
        return response.json()

    assert synchronize(hub, ask) == 1
    assert client.post("/api/devices/cam", headers=headers(), json={
        "batteryStatusEnabled": True, "batteryStatusMinutes": 12,
    }).status_code == 200
    synchronize(hub, ask)
    assert hub.battery_settings("cam") == {
        "batteryStatusEnabled": True, "batteryStatusMinutes": 12,
    }
    page = client.get("/api/photos", headers=headers()).json()
    assert page["photos"][0]["id"] == PHOTO
    assert page["hub"]["pending"] == 0
    assert page["hub"]["cameras"][0]["history"][0]["phase"] == "sleep_planned"
    assert page["hub"]["cameras"][0]["history"][0]["previousSleepConfirmed"] is False
    client.post("/api/photos/delete", headers=headers(), json={"mode": "all", "ids": [PHOTO]})
    synchronize(hub, ask)
    assert hub.store.get(PHOTO)["jpeg"] is None
    assert not hub.store.accept(PHOTO, "cam", jpeg(), captured=100, target=None)
    assert synchronize(hub, ask) == 0
    assert client.get("/api/photos", headers=headers()).json()["total"] == 0


def test_offline_cloud_keeps_unsynced_original(tmp_path):
    hub = CameraHub(
        {"database": str(tmp_path / "photos.db")},
        House(
            panel="https://panel",
            household="house",
            device_key="key",
            sheets_dir=tmp_path,
        ),
        tmp_path / "screen.bmp",
    )
    hub.store.accept(PHOTO, "cam", jpeg(), captured=100, target=None)

    def offline(*args, **kwargs):
        raise OSError("offline")

    with pytest.raises(OSError):
        synchronize(hub, offline)
    assert hub.store.get(PHOTO)["jpeg"] == jpeg()
    assert hub.store.unsynced() == [{"id": PHOTO, "state": "pending"}]


def test_parent_selects_a_frozen_target_and_hub_receives_it(tmp_path):
    import time

    from panel.trail import CurrentTrail

    client = client_for()
    household = household_of(client)
    hub = CameraHub({"database": str(tmp_path / "photos.db")}, House(
        panel="https://panel", household=household, device_key=DEVICE_KEY, sheets_dir=tmp_path,
    ), tmp_path / "screen.bmp")
    first = {"run": "aft_first", "moment": "page", "since": 100}
    second = {"run": "aft_second", "moment": "page", "since": 101}
    hub.store.accept(PHOTO, "cam", jpeg(), captured=102, target={"candidates": [first, second]})
    hub.store.claim()
    hub.store.finish(PHOTO, "awaiting_assignment", "legacy photo awaiting parent assignment")
    client.app.state.trail.report_current(CurrentTrail(household, time.time(), ({
        "runId": "aft_second", "momentId": "page", "waitingSince": 101, "phase": "waiting",
    },)))

    def ask(url, body, **kwargs):
        response = client.post(url.removeprefix("https://panel"), json=body,
                               headers={"X-Device-Key": kwargs["key"]})
        assert response.status_code == 200, response.text
        return response.json()

    synchronize(hub, ask)
    path = f"/api/photos/{PHOTO}/activity"
    other = "b" * 32
    from dataclasses import replace

    own = client.app.state.photos.list(household)[0]
    client.app.state.photos.save("other", replace(own, id=other), jpeg())
    assert client.post(f"/api/photos/{other}/activity", headers=headers(), json={
        "runId": "aft_second",
    }).status_code == 404
    assert client.post(path, headers=headers(), json={"runId": "aft_absent"}).status_code == 409
    assert client.post(path, json={"runId": "aft_second"}).status_code == 503
    assert client.app.state.messages.pending(household) == []
    response = client.post(path, headers=headers(), json={"runId": "aft_second"})
    assert response.json() == {"queued": True}
    assert client.post(path, headers=headers(), json={"runId": "aft_second"}).json() == {
        "queued": True,
    }
    assert len(client.app.state.messages.pending(household)) == 1
    synchronize(hub, ask)
    assert hub.store.get(PHOTO)["state"] == "pending"
    import json

    assert json.loads(hub.store.get(PHOTO)["target"]) == second
    assert client.app.state.messages.pending(household) == []


def test_missing_local_photo_does_not_acknowledge_assignment(tmp_path):
    hub = CameraHub({"database": str(tmp_path / "photos.db")}, House(
        panel="https://panel", household="house", device_key="key", sheets_dir=tmp_path,
    ), tmp_path / "screen.bmp")
    heard = []

    def ask(url, body, **kwargs):
        if url.endswith("/photo-assignments/pull"):
            return {"assignments": [{"id": "command", "photoId": PHOTO, "runId": "aft_one",
                                     "momentId": "page", "waitingSince": 100}]}
        if url.endswith("/portal-photos/pull"):
            return {"photos": []}
        if url.endswith("/heard"):
            heard.append(url)
        return {"ids": []}

    synchronize(hub, ask)
    assert heard == []


def test_concurrent_assignment_identifiers_cannot_replace_a_choice():
    from panel.messages import InMemoryMessageStore, MessageConflict, PendingMessage
    from shared.message import Message, Says

    store = InMemoryMessageStore()
    first = PendingMessage(f"assign_{PHOTO}", "house", Message(
        Says.ASSIGN_PHOTO, 100, run_id="first", photo_id=PHOTO, moment_id="page", waiting_since=10,
    ))
    store.add(first)
    with pytest.raises(MessageConflict):
        store.add(PendingMessage(first.id, "house", Message(
            Says.ASSIGN_PHOTO, 101, run_id="second", photo_id=PHOTO, moment_id="page",
            waiting_since=10,
        )))
    assert store.pending("house") == [first]
