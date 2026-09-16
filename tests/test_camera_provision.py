from __future__ import annotations

import runpy
from pathlib import Path

import pytest

from devices.camera_provision import camera_mac, prepare_build, verify_hardware


def test_builds_regenerate_selected_credentials_and_keep_identities_separate(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    for name in ("platformio.ini", "partitions.csv"):
        (source / name).write_text("fixture", encoding="utf-8")
    certificate = tmp_path / "ca.pem"
    certificate.write_text("test CA", encoding="utf-8")
    first, second = "94:A9:90:D0:9D:D0", "94:A9:90:D0:9D:D1"
    config = {"cameras": {first: "first-token", second: "second-token"},
              "certificate": str(certificate), "hub_address": "lanternina.local"}
    wifi = {"ssid": "test", "password": "test-password"}
    builds = tmp_path / "builds"
    first_build = prepare_build(source, builds, config, wifi, first)
    second_build = prepare_build(source, builds, config, wifi, second)
    assert first_build != second_build
    header = first_build / "include/camera_secrets.h"
    header.write_text("stale credentials", encoding="utf-8")
    prepare_build(source, builds, config, wifi, first)
    assert 'CAMERA_TOKEN = "first-token"' in header.read_text()
    assert second not in header.read_text()
    assert "first-token" not in (second_build / "include/camera_secrets.h").read_text()
    config["cameras"][second] = "first-token"
    with pytest.raises(ValueError, match="own nonempty token"):
        prepare_build(source, builds, config, wifi, first)


def test_detected_board_must_match_identity_chip_and_flash():
    mac = "94:A9:90:D0:9D:D0"
    output = f"Chip is ESP32-S3\nMAC: {mac}\nDetected flash size: 8MB"
    verify_hardware(output, mac)
    for wrong in (output.replace(mac, "other"), output.replace("8MB", "16MB"),
                  output.replace("ESP32-S3", "ESP32")):
        with pytest.raises(ValueError):
            verify_hardware(wrong, mac)
    with pytest.raises(ValueError):
        camera_mac("../../other")


def test_waveshare_guard_keeps_the_xiao_guard_strict():
    script = runpy.run_path(str(Path(__file__).parents[1] / "deploy/flash-waveshare-camera.py"))
    mac = "28:84:85:B1:6C:08"
    output = (
        "Chip is ESP32-S3 (QFN56) (revision v0.2)\n"
        "Features: WiFi, BLE, Embedded PSRAM 8MB (AP_3v3)\n"
        f"MAC: {mac}\nDetected flash size: 16MB\n"
    )
    script["verify_hardware"](output, mac)
    with pytest.raises(ValueError):
        verify_hardware(output, mac)
    for wrong in (
        output.replace(mac, "94:A9:90:D0:9D:D0"),
        output.replace("16MB", "8MB"),
        output.replace("16MB", "16MBX"),
        output.replace("ESP32-S3", "ESP32-S2"),
        output.replace("PSRAM 8MB", "PSRAM 2MB"),
    ):
        with pytest.raises(ValueError):
            script["verify_hardware"](wrong, mac)


def test_waveshare_first_install_cannot_erase_an_installed_queue():
    script = runpy.run_path(str(Path(__file__).parents[1] / "deploy/flash-waveshare-camera.py"))
    script["validate_update"](True, False)
    script["validate_update"](False, True)
    with pytest.raises(ValueError, match="refusing to erase"):
        script["validate_update"](True, True)
    with pytest.raises(ValueError, match="explicit"):
        script["validate_update"](False, False)


def test_waveshare_partition_layout_covers_exactly_16_mib():
    import csv

    path = Path(__file__).parents[1] / "firmware/camera-waveshare/partitions.csv"
    end = 0x9000
    with path.open() as stream:
        rows = list(csv.reader(stream, skipinitialspace=True))
    assert rows
    for row in rows:
        if not row:
            continue
        offset, size = int(row[3], 0), int(row[4], 0)
        assert offset == end
        assert size > 0
        end = offset + size
    assert end == 16 * 1024 * 1024


def test_waveshare_status_accounts_for_psram_heap_overhead():
    script = runpy.run_path(str(Path(__file__).parents[1] / "deploy/flash-waveshare-camera.py"))
    mac = "28:84:85:B1:6C:08"
    status = (
        "board=waveshare-ov5640 expander=1 button_gpio=1 led_gpio=2\n"
        f"status usb=1 psram=8386199 filesystem=1 identity={mac}\n"
    )
    script["verify_status"](status, mac)
    for wrong in (
        status.replace("8386199", "0"), status.replace("8386199", "2097152"),
        status.replace("expander=1", "expander=0"), status.replace(mac, "other"),
    ):
        with pytest.raises(ValueError):
            script["verify_status"](wrong, mac)