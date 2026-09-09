from __future__ import annotations

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