from __future__ import annotations

import json
import os
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
from PIL import Image

from devices import trmnl_byos
from devices.trmnl_byos import (
    DEVICE_LOG_KEEP,
    LEVEL_CRITICAL,
    LEVEL_LOW,
    LEVEL_OK,
    LOW_BATTERY_REFRESH,
    PRESS_REFRESH,
    USB_REFRESH,
    Config,
    battery_level,
    load_devices,
    log_messages,
    make_handler,
    mark_provisioned,
    record_device_log,
    register_device,
    screen_for,
    set_mains,
    validate_screen,
)
from tools.make_trmnl_test_screen import make_screen

MAC = "94:A9:90:CF:7D:04"
TOKEN = "test-token"


@pytest.fixture
def server(tmp_path: Path) -> tuple[str, ThreadingHTTPServer]:
    screen = tmp_path / "screen.bmp"
    make_screen(screen)
    registry = tmp_path / "devices.json"
    device = register_device(registry, MAC)
    document = json.loads(registry.read_text(encoding="utf-8"))
    document["devices"][MAC]["token"] = TOKEN
    registry.write_text(json.dumps(document), encoding="utf-8")
    assert device.mac == MAC
    config = Config("http://127.0.0.1", screen, registry)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}", httpd
    httpd.shutdown()
    thread.join()


def get(url: str, headers: dict[str, str] | None = None) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def test_setup_display_and_screen(server: tuple[str, ThreadingHTTPServer]) -> None:
    base_url, _ = server
    status, payload = get(f"{base_url}/api/setup", {"ID": MAC})
    setup = json.loads(payload)

    assert status == 200
    assert setup["api_key"] == TOKEN

    status, payload = get(
        f"{base_url}/api/display", {"ID": MAC, "Access-Token": TOKEN}
    )
    display = json.loads(payload)
    assert status == 200
    assert display["status"] == 0
    assert display["update_firmware"] is False

    status, bitmap = get(f"{base_url}/screen/{TOKEN}.bmp")
    assert status == 200
    assert bitmap[:2] == b"BM"


def test_unknown_device_and_wrong_token_are_refused(
    server: tuple[str, ThreadingHTTPServer],
) -> None:
    base_url, _ = server
    assert get(f"{base_url}/api/setup", {"ID": "00:00:00:00:00:00"})[0] == 404
    assert get(f"{base_url}/api/display", {"ID": MAC, "Access-Token": "wrong"})[0] == 403


def test_battery_level_thresholds() -> None:
    """A device that says nothing is not the same as a full one, but it is treated as ok:
    refusing to show anything because a reading is missing would be worse."""
    assert battery_level(4.2) == LEVEL_OK
    assert battery_level(3.75) == LEVEL_OK
    assert battery_level(3.70) == LEVEL_LOW
    assert battery_level(3.62) == LEVEL_LOW
    assert battery_level(3.60) == LEVEL_CRITICAL
    assert battery_level(3.1) == LEVEL_CRITICAL
    assert battery_level(None) == LEVEL_OK


def _server_with_low_screen(tmp_path: Path) -> tuple[str, ThreadingHTTPServer, str, Path]:
    screen = tmp_path / "screen.bmp"
    make_screen(screen)
    low = tmp_path / "low.bmp"
    make_screen(low)
    low.write_bytes(low.read_bytes()[:-1] + b"\x00")  # same geometry, different bytes

    registry = tmp_path / "devices.json"
    register_device(registry, MAC)
    token = json.loads(registry.read_text(encoding="utf-8"))["devices"][MAC]["token"]
    config = Config(
        "http://127.0.0.1",
        screen,
        registry,
        status_file=tmp_path / "status.json",
        low_battery_file=low,
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return f"http://127.0.0.1:{httpd.server_port}", httpd, token, low


def test_usb_power_keeps_the_panel_responsive_and_silences_the_battery(
    tmp_path: Path,
) -> None:
    """Plugged in, the voltage sits near full because it is charging, so a battery notice
    would be both wrong and impossible to act on."""
    base_url, httpd, token, low = _server_with_low_screen(tmp_path)
    try:
        headers = {
            "ID": MAC,
            "Access-Token": token,
            "Battery-Voltage": "3.65",
            "USB-Connected": "true",
        }
        _status, payload = get(f"{base_url}/api/display", headers)
        display = json.loads(payload)

        assert display["refresh_rate"] == str(USB_REFRESH)
        _code, bitmap = get(f"{base_url}/screen/{token}.bmp")
        assert bitmap != low.read_bytes()
    finally:
        httpd.shutdown()


SECOND_MAC = "E8:3D:C1:FB:9F:18"


def test_a_display_with_a_job_of_its_own_stops_following_the_picture(tmp_path: Path) -> None:
    """Two displays, one server, and only one of them is showing the hourly picture.

    The second is the one standing by the printer: what it shows is about the sheet, so it
    must not be overwritten by the next picture the house paints.
    """
    shared = tmp_path / "screen.bmp"
    make_screen(shared)
    registry = tmp_path / "devices.json"
    first = register_device(registry, MAC)
    second = register_device(registry, SECOND_MAC)

    own = screen_for(shared, second.friendly_id)
    Image.new("1", (800, 480), 1).save(own, format="BMP")

    httpd = ThreadingHTTPServer(
        ("127.0.0.1", 0), make_handler(Config("http://127.0.0.1", shared, registry))
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{httpd.server_port}"
    try:
        assert get(f"{base_url}/screen/{first.token}.bmp")[1] == shared.read_bytes()
        assert get(f"{base_url}/screen/{second.token}.bmp")[1] == own.read_bytes()

        # Nothing to show of its own is the normal state, and it means the picture.
        own.unlink()
        assert get(f"{base_url}/screen/{second.token}.bmp")[1] == shared.read_bytes()
    finally:
        httpd.shutdown()
        thread.join()


def test_a_short_press_is_recorded_and_a_timer_wake_is_not(tmp_path: Path) -> None:
    """The press is the only thing in this system that starts a scan, so it has to be
    legible without a wire we do not have. The firmware already says why it woke."""
    screen = tmp_path / "screen.bmp"
    make_screen(screen)
    registry = tmp_path / "devices.json"
    device = register_device(registry, MAC)
    button = tmp_path / "button.json"
    config = Config("http://127.0.0.1", screen, registry, button_file=button)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{httpd.server_port}"
    try:
        headers = {"ID": MAC, "Access-Token": device.token}
        get(f"{base_url}/api/display", {**headers, "Update-Source": "timer"})
        assert not button.exists(), "a scheduled poll is not somebody asking for anything"

        get(f"{base_url}/api/display", {**headers, "Update-Source": "EXT0"})
        assert json.loads(button.read_text(encoding="utf-8"))["mac"] == MAC
    finally:
        httpd.shutdown()
        thread.join()


def test_the_cache_key_follows_the_bytes(tmp_path: Path) -> None:
    """If the name did not move with the picture, a new one could go unfetched."""
    base_url, httpd, token, _low = _server_with_low_screen(tmp_path)
    try:
        headers = {"ID": MAC, "Access-Token": token, "USB-Connected": "true"}
        first = json.loads(get(f"{base_url}/api/display", headers)[1])["filename"]
        second = json.loads(get(f"{base_url}/api/display", headers)[1])["filename"]
        assert first == second
    finally:
        httpd.shutdown()


def test_a_display_declared_on_mains_never_sleeps_long(tmp_path: Path) -> None:
    """The board reports USB-Connected false even when plugged in, because its firmware
    only implements the check on two other boards. So the flag in the registry is the
    only path that can work here, and it is the one that has to be covered."""
    base_url, httpd, token, low = _server_with_low_screen(tmp_path)
    registry = tmp_path / "devices.json"
    set_mains(registry, MAC, True)
    try:
        headers = {"ID": MAC, "Access-Token": token, "Battery-Voltage": "3.55"}
        display = json.loads(get(f"{base_url}/api/display", headers)[1])

        assert display["refresh_rate"] == str(USB_REFRESH)
        _code, bitmap = get(f"{base_url}/screen/{token}.bmp")
        assert bitmap != low.read_bytes()
    finally:
        httpd.shutdown()


def test_declaring_mains_keeps_the_token(tmp_path: Path) -> None:
    registry = tmp_path / "devices.json"
    original = register_device(registry, MAC)
    updated = set_mains(registry, MAC, True)
    assert updated.token == original.token
    assert load_devices(registry)[MAC].mains is True


def test_an_emptying_battery_changes_the_picture_and_the_sleep(tmp_path: Path) -> None:
    screen = tmp_path / "screen.bmp"
    make_screen(screen)
    low = tmp_path / "low.bmp"
    make_screen(low)
    low.write_bytes(low.read_bytes()[:-1] + b"\x00")  # same geometry, different bytes

    registry = tmp_path / "devices.json"
    register_device(registry, MAC)
    token = json.loads(registry.read_text(encoding="utf-8"))["devices"][MAC]["token"]
    config = Config(
        "http://127.0.0.1",
        screen,
        registry,
        status_file=tmp_path / "status.json",
        low_battery_file=low,
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{httpd.server_port}"
        headers = {"ID": MAC, "Access-Token": token, "Battery-Voltage": "3.65"}
        _status, payload = get(f"{base_url}/api/display", headers)
        display = json.loads(payload)

        assert display["refresh_rate"] == str(LOW_BATTERY_REFRESH)
        # The cache key has to move, or the device keeps the picture it already holds.
        assert display["filename"] != "lanternina-ok"

        _code, bitmap = get(f"{base_url}/screen/{token}.bmp")
        assert bitmap == low.read_bytes()
    finally:
        httpd.shutdown()
        thread.join()


def test_generated_screen_has_the_firmware_geometry(tmp_path: Path) -> None:
    screen = tmp_path / "screen.bmp"
    make_screen(screen)
    assert len(validate_screen(screen)) == 48_062


def _server_that_answers_a_press(
    tmp_path: Path,
) -> tuple[str, ThreadingHTTPServer, str, Path, Path]:
    shared = tmp_path / "screen.bmp"
    make_screen(shared)
    waiting = tmp_path / "waiting.bmp"
    make_screen(waiting)
    waiting.write_bytes(waiting.read_bytes()[:-1] + b"\x00")  # same geometry, other bytes

    registry = tmp_path / "devices.json"
    device = register_device(registry, MAC)
    config = Config(
        "http://127.0.0.1",
        shared,
        registry,
        button_file=tmp_path / "button.json",
        waiting_file=waiting,
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    own = screen_for(shared, device.friendly_id)
    return f"http://127.0.0.1:{httpd.server_port}", httpd, device.token, waiting, own


def poll(base_url: str, token: str, woke_by: str) -> dict[str, str]:
    headers = {"ID": MAC, "Access-Token": token, "Update-Source": woke_by}
    return json.loads(get(f"{base_url}/api/display", headers)[1])


def test_a_press_is_answered_in_the_response_it_caused(tmp_path: Path) -> None:
    """Somebody who presses and sees nothing presses again and holds it down, and holding
    is the gesture that used to wipe the Wi-Fi. So the press has to change the screen in
    the request it caused, not at the next poll."""
    base_url, httpd, token, waiting, _own = _server_that_answers_a_press(tmp_path)
    try:
        assert poll(base_url, token, "timer")["refresh_rate"] != str(PRESS_REFRESH)
        assert get(f"{base_url}/screen/{token}.bmp")[1] != waiting.read_bytes()

        assert poll(base_url, token, "EXT0")["refresh_rate"] == str(PRESS_REFRESH)
        assert get(f"{base_url}/screen/{token}.bmp")[1] == waiting.read_bytes()
    finally:
        httpd.shutdown()


def test_the_answer_does_not_wait_for_the_ordinary_poll(tmp_path: Path) -> None:
    """The scan writes what it read; the next poll is the short one, and it carries the
    result. After that the display goes back to its usual spacing on its own."""
    base_url, httpd, token, _waiting, own = _server_that_answers_a_press(tmp_path)
    try:
        poll(base_url, token, "EXT0")

        make_screen(own)
        own.write_bytes(own.read_bytes()[:-2] + b"\x00\x00")  # what the scan read back

        assert poll(base_url, token, "timer")["refresh_rate"] != str(PRESS_REFRESH)
        assert get(f"{base_url}/screen/{token}.bmp")[1] == own.read_bytes()
    finally:
        httpd.shutdown()


def test_a_scan_that_never_answers_does_not_hold_the_display(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Nothing is ever written back, so the waiting screen would otherwise be forever."""
    monkeypatch.setattr(trmnl_byos, "PRESS_PATIENCE_SECONDS", 0)
    base_url, httpd, token, waiting, _own = _server_that_answers_a_press(tmp_path)
    try:
        poll(base_url, token, "EXT0")

        assert poll(base_url, token, "timer")["refresh_rate"] != str(PRESS_REFRESH)
        assert get(f"{base_url}/screen/{token}.bmp")[1] != waiting.read_bytes()
    finally:
        httpd.shutdown()


def test_each_registered_device_gets_a_distinct_token(tmp_path: Path) -> None:
    registry = tmp_path / "devices.json"
    first = register_device(registry, MAC)
    second = register_device(registry, "94:A9:90:CF:7D:05")
    assert first.token != second.token
    assert register_device(registry, MAC) == first
    assert mark_provisioned(registry, MAC).provisioned is True
    if os.name != "nt":
        assert registry.stat().st_mode & 0o777 == 0o640


def test_request_log_does_not_expose_the_screen_token(
    server: tuple[str, ThreadingHTTPServer], capsys: pytest.CaptureFixture[str]
) -> None:
    base_url, _ = server
    assert get(f"{base_url}/screen/{TOKEN}.bmp")[0] == 200
    assert TOKEN not in capsys.readouterr().err


def test_what_a_display_reports_about_itself_is_kept(tmp_path: Path) -> None:
    """These reports were discarded until a failure turned out to be explained by them,
    and by nothing else we were recording."""
    log_file = tmp_path / "device-logs.jsonl"
    body = {
        "log": {
            "logs_array": [
                {"log_message": "mDNS could not resolve lanternina.local", "log_codeline": 42}
            ]
        }
    }
    entry = record_device_log(log_file, MAC, json.dumps(body).encode())

    assert entry["mac"] == MAC
    assert log_messages(entry["body"]) == ["mDNS could not resolve lanternina.local"]
    kept = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(kept) == 1
    assert json.loads(kept[0])["mac"] == MAC


def test_the_device_log_stays_bounded(tmp_path: Path) -> None:
    """A log that grows without limit on the one machine that must not fill its disk is
    an outage waiting for a quiet week."""
    log_file = tmp_path / "device-logs.jsonl"
    for index in range(DEVICE_LOG_KEEP + 25):
        record_device_log(log_file, MAC, json.dumps({"log_message": f"n{index}"}).encode())

    kept = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(kept) == DEVICE_LOG_KEEP
    # The newest survives; the oldest is the one dropped.
    assert f"n{DEVICE_LOG_KEEP + 24}" in kept[-1]
    assert "n0" not in log_file.read_text(encoding="utf-8")


def test_a_report_that_is_not_json_is_still_kept(tmp_path: Path) -> None:
    """The device writes this text. Storing it must not depend on it being well formed."""
    log_file = tmp_path / "device-logs.jsonl"
    entry = record_device_log(log_file, MAC, b"crash before the JSON was finished {")
    assert "crash before" in str(entry["body"])


def test_a_posted_log_is_recorded_and_still_answered(tmp_path: Path) -> None:
    screen = tmp_path / "screen.bmp"
    make_screen(screen)
    registry = tmp_path / "devices.json"
    register_device(registry, MAC)
    token = json.loads(registry.read_text(encoding="utf-8"))["devices"][MAC]["token"]
    log_file = tmp_path / "device-logs.jsonl"
    config = Config("http://127.0.0.1", screen, registry, device_log_file=log_file)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{httpd.server_port}"
        request = urllib.request.Request(
            f"{base_url}/api/log",
            data=json.dumps({"log_message": "wifi weak"}).encode(),
            headers={"ID": MAC, "Access-Token": token, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            assert response.status == 204
        assert "wifi weak" in log_file.read_text(encoding="utf-8")
    finally:
        httpd.shutdown()
        thread.join()