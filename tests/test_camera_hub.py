from __future__ import annotations

import io
import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
from PIL import Image

from devices.camera_hub import CameraHub, camera_model, captured_at, make_handler, render_photo
from devices.house import House
from tests.test_photo_store import PHOTO, jpeg


@pytest.mark.parametrize("values,expected", [
    ({"board": "waveshare-ov5640"}, ("Waveshare", "Waveshare ESP32-S3-CAM-OV5640")),
    ({"firmware": "waveshare-2026-09-16-lcd1-2"},
     ("Waveshare", "Waveshare ESP32-S3-CAM-OV5640")),
    ({"firmware": "camera-2026-09-14-d5-d8"}, ("XIAO", "XIAO ESP32S3 Sense")),
    ({"board": "unrecognized", "firmware": "camera-other"}, ("Camera", "ESP32 camera")),
    ({}, ("Camera", "ESP32 camera")),
])
def test_camera_model_distinguishes_board_and_legacy_firmware(values, expected):
    assert camera_model(values) == expected


def test_battery_settings_are_cached_by_identity_and_invalid_updates_preserve_them(tmp_path):
    hub = CameraHub({"database": str(tmp_path / "photos.db")},
                    House(sheets_dir=tmp_path), tmp_path / "screen.bmp")
    assert hub.battery_settings("WAVE") == {}
    answer = {"things": [{"id": "WAVE", "kind": "camera",
                           "batteryStatusEnabled": True, "batteryStatusMinutes": 15}]}
    hub.save_battery_settings(answer)
    assert hub.battery_settings("WAVE") == {
        "batteryStatusEnabled": True, "batteryStatusMinutes": 15,
    }
    assert hub.battery_settings("OTHER")["batteryStatusEnabled"] is False
    answer["things"][0]["batteryStatusMinutes"] = 0
    hub.save_battery_settings(answer)
    assert hub.battery_settings("WAVE")["batteryStatusMinutes"] == 15
    hub.save_battery_settings({})
    assert hub.battery_settings("WAVE")["batteryStatusEnabled"] is True
    hub.save_battery_settings({"things": []})
    assert hub.battery_settings("WAVE")["batteryStatusEnabled"] is False


def test_camera_status_reports_model_voltage_and_authenticated_battery_settings(tmp_path):
    hub = CameraHub({"database": str(tmp_path / "photos.db"), "cameras": {"WAVE": "token"}},
                    House(sheets_dir=tmp_path), tmp_path / "screen.bmp")
    hub.save_battery_settings({"things": [{"id": "WAVE", "kind": "camera",
        "batteryStatusEnabled": True, "batteryStatusMinutes": 7}]})
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(hub))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    values = {"board": "waveshare-ov5640", "voltage": 4.11, "rssi": -40, "usb": False}
    request = urllib.request.Request(f"http://127.0.0.1:{server.server_port}/status",
        json.dumps(values).encode(), {"X-Camera-Id": "WAVE", "Authorization": "Bearer token"})
    try:
        with urllib.request.urlopen(request) as response:
            assert json.load(response) == {"received": True, "batteryStatusEnabled": True,
                                          "batteryStatusMinutes": 7}
        row = hub.store.cameras()[0]
        assert row["name"] == "Waveshare WAVE"
        assert row["model"] == "Waveshare ESP32-S3-CAM-OV5640"
        assert row["voltage"] == 4.11
        assert row["level"] == "ok"
        request.remove_header("Authorization")
        with pytest.raises(urllib.error.HTTPError) as denied:
            urllib.request.urlopen(request)
        assert denied.value.code == 401
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_photo_frame_contains_the_whole_portrait() -> None:
    image = Image.open(io.BytesIO(render_photo(jpeg())))
    assert image.size == (800, 480)
    assert image.mode == "1"


def test_received_photo_waits_outside_hours_and_runs_once_when_allowed(tmp_path, monkeypatch):
    hub = CameraHub({"database": str(tmp_path / "photos.db")},
                    House(sheets_dir=tmp_path), tmp_path / "screen.bmp")
    target = {"run": "aft_one", "moment": "page", "since": 100}
    hub.store.accept(PHOTO, "cam", jpeg(), captured=110, target=target)
    allowed = False
    calls = []
    from shared.vision_contracts import PhotoMatch

    monkeypatch.setattr("devices.camera_hub.photo_candidates",
                        lambda *_: ([target], [{"title": "Clouds", "expected": "Sky"}]))
    monkeypatch.setattr("devices.camera_hub.target_is_waiting", lambda *_: True)
    monkeypatch.setattr("devices.camera_hub.match_photo", lambda *_args, **_kw: PhotoMatch(0, 90,
                                                                                         False))
    monkeypatch.setattr("devices.camera_hub.activity_time_allowed", lambda *_: allowed)
    monkeypatch.setattr("devices.camera_hub.carry_on", lambda *args, **kwargs: calls.append(kwargs)
                        or "waiting for a page at next")
    assert not hub.process_one()
    assert hub.store.get(PHOTO)["state"] == "pending"
    assert calls == []
    allowed = True
    assert hub.process_one()
    assert len(calls) == 1
    assert calls[0]["photograph"] != jpeg()
    assert calls[0]["target"] == target
    assert not hub.process_one()


@pytest.mark.parametrize("jobs,displayed", [(["picture"], False), (["photo"], True), ([], False)])
def test_photographs_only_reach_explicitly_assigned_displays(
    tmp_path, monkeypatch, jobs, displayed,
):
    from devices.trmnl_byos import photo_for

    shared = tmp_path / "screen.bmp"
    assignments = tmp_path / "jobs.json"
    monkeypatch.setenv("LANTERNINA_JOBS_FILE", str(assignments))
    monkeypatch.setattr("devices.inventory.load_jobs", lambda _: [
        {"id": "display", "kind": "display", "label": "screen", "jobs": jobs},
    ])
    hub = CameraHub({"database": str(tmp_path / "photos.db")}, House(sheets_dir=tmp_path), shared)
    hub.store.accept(PHOTO, "camera", jpeg(), captured=None, target=None)
    assert hub.process_one()
    assert photo_for(shared, "screen").exists() is displayed
    assert hub.store.get(PHOTO)["jpeg"] == jpeg()
    assert hub.store.get(PHOTO)["state"] == "done"


@pytest.mark.parametrize("outcome", ["none", "uncertain", "stale", "changed", "match"])
def test_camera_classifies_multiple_activities_without_parent_assignment(
    tmp_path, monkeypatch, outcome,
):
    from shared.vision_contracts import PhotoMatch

    hub = CameraHub({"database": str(tmp_path / "photos.db")},
                    House(sheets_dir=tmp_path), tmp_path / "screen.bmp")
    first = {"run": "one", "moment": "build", "since": 10}
    second = {"run": "two", "moment": "sky", "since": 11}
    targets = [first, second]
    hub.store.accept(PHOTO, "camera", jpeg(), captured=12, target={"candidates": targets})
    selected, shown, received = [], [], []
    monkeypatch.setattr("devices.camera_hub.activity_time_allowed", lambda *_: True)
    monkeypatch.setattr("devices.camera_hub.photo_candidates", lambda *_: (
        ([], []) if outcome == "stale" else (targets, [{"title": "Bridge"}, {"title": "Clouds"}])
    ))

    def match(photograph, candidates, **kwargs):
        assert len(candidates) == 2
        assert outcome != "stale"
        return PhotoMatch(None if outcome in ("none", "uncertain") else 1, 270,
                          outcome == "uncertain")

    monkeypatch.setattr("devices.camera_hub.match_photo", match)
    monkeypatch.setattr("devices.camera_hub.target_is_waiting", lambda *_: outcome != "changed")
    monkeypatch.setattr("devices.camera_hub.note_photo_received",
                        lambda *args: received.append(args[1]))
    monkeypatch.setattr("devices.camera_hub.carry_on", lambda *args, **kwargs:
                        selected.append(kwargs) or "waiting for a page at next")
    monkeypatch.setattr(hub, "display_photo", lambda *args: shown.append(args))
    assert hub.process_one()
    row = hub.store.get(PHOTO)
    assert row["state"] == "done"
    assert row["jpeg"] == jpeg()
    assert not hub.process_one()
    if outcome == "match":
        assert received == [second]
        assert selected[0]["target"] == second
        assert Image.open(io.BytesIO(selected[0]["photograph"])).size == (48, 64)
        assert not shown
    else:
        assert not received and not selected
        assert bool(shown) is (outcome == "none")
        assert row["target"] == "null"
        assert row["detail"] == "photo_match_" + ("stale" if outcome == "changed" else outcome)


def test_activity_hours_closing_during_matching_defers_without_receipt(tmp_path, monkeypatch):
    from shared.vision_contracts import PhotoMatch

    hub = CameraHub({"database": str(tmp_path / "photos.db")}, House(sheets_dir=tmp_path),
                    tmp_path / "screen.bmp")
    target = {"run": "one", "moment": "build", "since": 10}
    hub.store.accept(PHOTO, "camera", jpeg(), captured=12, target={"candidates": [target]})
    allowed = True
    monkeypatch.setattr("devices.camera_hub.activity_time_allowed", lambda *_: allowed)
    monkeypatch.setattr("devices.camera_hub.photo_candidates",
                        lambda *_: ([target], [{"title": "Bridge"}]))
    monkeypatch.setattr("devices.camera_hub.target_is_waiting", lambda *_: True)

    def match(*args, **kwargs):
        nonlocal allowed
        allowed = False
        return PhotoMatch(0, 0, False)

    monkeypatch.setattr("devices.camera_hub.match_photo", match)
    monkeypatch.setattr("devices.camera_hub.note_photo_received",
                        lambda *_: pytest.fail("receipt outside hours"))
    monkeypatch.setattr("devices.camera_hub.carry_on", lambda *_: pytest.fail("advance"))
    assert not hub.process_one()
    row = hub.store.get(PHOTO)
    assert row["state"] == "pending"
    assert row["detail"] == "photo_match_deferred"
    assert "candidates" in json.loads(row["target"])


@pytest.mark.parametrize("rotation", [0, 90, 180, 270])
def test_vision_rotation_is_clockwise_after_exif_orientation(rotation):
    from devices.camera_hub import orient_photo

    image = Image.new("RGB", (64, 48), "white")
    image.paste("red", (0, 0, 32, 24))
    output = io.BytesIO()
    exif = image.getexif()
    exif[274] = 6
    image.save(output, "JPEG", quality=100, exif=exif)
    original = output.getvalue()
    oriented = Image.open(io.BytesIO(orient_photo(original, rotation)))
    expected = image.rotate(-90 - rotation, expand=True)
    assert oriented.size == expected.size
    for horizontal, vertical in [(8, 8), (8, oriented.height - 8),
                                  (oriented.width - 8, 8),
                                  (oriented.width - 8, oriented.height - 8)]:
        assert max(abs(actual - wanted) for actual, wanted in zip(
            oriented.getpixel((horizontal, vertical)), expected.getpixel((horizontal, vertical)),
            strict=True,
        )) < 20
    assert output.getvalue() == original


@pytest.mark.parametrize("header", [{}, {"X-Capture-Age": "-2"}, {"X-Captured-At": "nan"}])
def test_unknown_or_invalid_capture_time_is_not_current(header: dict[str, str]) -> None:
    assert captured_at(header, 100) is None


def test_upload_requires_camera_identity_and_durable_receipt(tmp_path: Path, monkeypatch) -> None:
    hub = CameraHub(
        {
            "database": str(tmp_path / "photos.db"),
            "cameras": {"CAM": "secret"},
            "family_password": "separate",
        },
        House(sheets_dir=tmp_path),
        tmp_path / "s.bmp",
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(hub))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/photos/{PHOTO}"
    headers = {"Content-Type": "image/jpeg", "X-Camera-Id": "CAM"}
    try:
        with pytest.raises(urllib.error.HTTPError) as denied:
            urllib.request.urlopen(urllib.request.Request(url, jpeg(), headers, method="PUT"))
        assert denied.value.code == 401
        headers["Authorization"] = "Bearer secret"
        headers["X-Capture-Purpose"] = "diagnostic"
        monkeypatch.setattr("devices.camera_hub.camera_target", lambda *_: pytest.fail(
            "a diagnostic photograph must not reach an activity"
        ))
        for expected in (201, 200):
            with urllib.request.urlopen(
                urllib.request.Request(url, jpeg(), headers, method="PUT")
            ) as response:
                assert response.status == expected
                assert json.load(response) == {"id": PHOTO, "stored": True}
        assert hub.store.get(PHOTO)["jpeg"] == jpeg()
        with pytest.raises(urllib.error.HTTPError) as denied:
            urllib.request.urlopen(urllib.request.Request(url, headers=headers))
        assert denied.value.code == 401
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
