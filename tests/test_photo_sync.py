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

    def ask(url, body, **kwargs):
        response = client.post(
            url.removeprefix("https://panel"), json=body, headers={"X-Device-Key": kwargs["key"]}
        )
        assert response.status_code == 200, response.text
        return response.json()

    assert synchronize(hub, ask) == 1
    page = client.get("/api/photos", headers=headers()).json()
    assert page["photos"][0]["id"] == PHOTO
    assert page["hub"]["pending"] == 0
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
