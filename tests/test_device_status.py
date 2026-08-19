"""The device status route: what the parent sees about the displays.

The property worth pinning is the vocabulary. The board has no fuel gauge, so the panel
must never show a percentage — and a display that has gone quiet has to be visible here,
because it is the one place a fault is allowed to appear.
"""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from panel.app import create_app
from panel.config import Settings
from panel.devices import SILENT_AFTER_SECONDS, InMemoryDeviceStatusStore
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
MAC = "94:A9:90:CF:7D:04"


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            devices=InMemoryDeviceStatusStore(),
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def report(client: TestClient, household: str, **overrides: object) -> None:
    body = {
        "id": MAC,
        "name": "CF7D04",
        "lastSeen": time.time(),
        "level": "mains",
        "voltage": 4.2,
        "rssi": -40.0,
        "firmware": "1.8.12",
        "model": "xiao_epaper_display",
    }
    body.update(overrides)
    response = client.post(
        f"/api/device/{household}/devices",
        json=[body],
        headers={"X-Device-Key": DEVICE_KEY},
    )
    assert response.status_code == 200, response.text


def test_the_parent_sees_what_the_hub_reported() -> None:
    client = client_for()
    household = household_of(client)
    report(client, household)

    devices = client.get("/api/devices", headers=headers()).json()["devices"]
    assert len(devices) == 1
    # `label` is what the display calls itself; `name` is the parent's, and empty until
    # they write one.
    assert devices[0]["label"] == "CF7D04"
    assert devices[0]["name"] == ""
    assert devices[0]["level"] == "mains"
    assert devices[0]["silent"] is False


def test_a_display_that_stopped_reporting_is_flagged() -> None:
    """The panel is the only place a fault may appear, so it has to appear here."""
    client = client_for()
    household = household_of(client)
    report(client, household, lastSeen=time.time() - SILENT_AFTER_SECONDS - 60)

    devices = client.get("/api/devices", headers=headers()).json()["devices"]
    assert devices[0]["silent"] is True


def test_no_percentage_is_ever_published() -> None:
    """There is no fuel gauge on this board: a percentage would be a guess with a
    decimal point on it."""
    client = client_for()
    household = household_of(client)
    report(client, household, level="low", voltage=3.65)

    device = client.get("/api/devices", headers=headers()).json()["devices"][0]
    assert "percent" not in " ".join(device.keys()).lower()
    assert device["level"] == "low"


def test_a_new_report_replaces_the_old_one() -> None:
    """State, not history: keeping every reading would log when the house is awake."""
    client = client_for()
    household = household_of(client)
    report(client, household, level="ok")
    report(client, household, level="critical")

    devices = client.get("/api/devices", headers=headers()).json()["devices"]
    assert len(devices) == 1
    assert devices[0]["level"] == "critical"


def test_another_household_sees_no_devices() -> None:
    client = client_for()
    report(client, "hh_someone_else")
    assert client.get("/api/devices", headers=headers()).json()["devices"] == []
