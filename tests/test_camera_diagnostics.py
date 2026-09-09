from __future__ import annotations

import pytest

from devices.camera_diagnostics import clean_diagnostics
from devices.photo_store import PhotoStore


def test_sleep_intent_is_not_promoted_to_confirmation(tmp_path):
    store = PhotoStore(tmp_path / "photos.db")
    for number in range(25):
        report = {
            "id": "camera",
            "lastSeen": number,
            "diagnostics": clean_diagnostics(
                {
                    "phase": "sleep_planned",
                    "previousSleepConfirmed": False,
                    "bootId": "one",
                }
            ),
        }
        store.record_camera(report)
    report = store.cameras()[0]
    assert len(report["diagnosticHistory"]) == 20
    assert report["diagnosticHistory"][0]["receivedAt"] == 5
    assert report["diagnostics"]["previousSleepConfirmed"] is False
    store.record_camera(
        {
            "id": "camera",
            "lastSeen": 26,
            "diagnostics": clean_diagnostics(
                {
                    "phase": "operation_complete",
                    "bootId": "two",
                    "previousBootId": "one",
                    "wakeCause": "button",
                    "previousSleepConfirmed": True,
                    "sleepSeconds": 60,
                }
            ),
        }
    )
    assert store.cameras()[0]["diagnosticHistory"][-1]["previousSleepConfirmed"] is True


@pytest.mark.parametrize(
    "values",
    [[], {"captureMs": float("nan")}, {"phase": "x" * 97}, {"previousSleepConfirmed": "true"}],
)
def test_malformed_diagnostics_are_rejected(values):
    with pytest.raises(ValueError):
        clean_diagnostics(values)


def test_cloud_rejects_invalid_diagnostic_history():
    from panel.routes.photos import SyncReport

    with pytest.raises(ValueError):
        SyncReport(
            pending=0,
            localPhotos=0,
            cameras=[
                {
                    "id": "cam",
                    "history": [{"phase": "sleep_planned"}],
                }
            ],
        )
