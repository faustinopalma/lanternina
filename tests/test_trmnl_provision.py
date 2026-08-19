from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

import devices.trmnl_provision as provisioner
from devices.trmnl_provision import (
    FLASH_SIZE_BYTES,
    ProvisioningConfig,
    provision,
    wait_for_port,
    write_nvs_csv,
)


def test_provisioning_config_defaults_to_mdns_name(tmp_path: Path) -> None:
    path = tmp_path / "provisioning.json"
    path.write_text(json.dumps({"ssid": "Home", "password": "secret"}), encoding="utf-8")
    config = ProvisioningConfig.load(path)
    assert config.base_url == "http://lanternina.local:8080"


def test_nvs_csv_contains_wifi_and_byos_without_losing_punctuation(tmp_path: Path) -> None:
    path = tmp_path / "nvs.csv"
    config = ProvisioningConfig("Home, 2.4", "comma,password", "http://lanternina.local:8080")
    write_nvs_csv(path, config)
    rows = list(csv.reader(path.open(encoding="utf-8")))
    values = {row[0]: row[3] for row in rows[1:] if row[1] == "data"}
    assert values["wifi_0_ssid"] == "Home, 2.4"
    assert values["wifi_0_pswd"] == "comma,password"
    assert values["api_url"] == "http://lanternina.local:8080"


def test_empty_wifi_configuration_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "provisioning.json"
    path.write_text(json.dumps({"ssid": "", "password": ""}), encoding="utf-8")
    with pytest.raises(ValueError):
        ProvisioningConfig.load(path)


def test_esptool_uses_version_4_reset_option_names() -> None:
    source = Path("devices/trmnl_provision.py").read_text(encoding="utf-8")
    assert '"usb_reset"' in source
    assert '"no_reset"' in source
    assert '"hard_reset"' in source
    assert '"usb-reset"' not in source
    assert '"read_flash"' in source
    assert "FLASH_SIZE = \"0x1000000\"" in source
    assert '"460800"' in source


MAC = "94:A9:90:CF:7D:04"


def _prepare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[dict[str, Path], list[list[str]]]:
    registry = tmp_path / "trmnl-devices.json"
    registry.write_text(
        json.dumps(
            {
                "version": 1,
                "devices": {MAC: {"token": "t" * 48, "friendly_id": "CF7D04", "provisioned": True}},
            }
        ),
        encoding="utf-8",
    )
    config = tmp_path / "provisioning.json"
    config.write_text(json.dumps({"ssid": "Home", "password": "secret"}), encoding="utf-8")
    firmware = tmp_path / "firmware.bin"
    firmware.write_bytes(b"\x00")
    backups = tmp_path / "backups"
    backups.mkdir()
    with (backups / (MAC.replace(":", "") + ".bin")).open("wb") as stream:
        stream.truncate(FLASH_SIZE_BYTES)

    commands: list[list[str]] = []
    monkeypatch.setattr(provisioner, "device_mac", lambda port: MAC)
    monkeypatch.setattr(provisioner, "run", lambda command: commands.append(command))
    paths = {
        "port": tmp_path / "ttyACM0",
        "config": config,
        "registry": registry,
        "firmware": firmware,
        "backups": backups,
    }
    paths["port"].write_text("", encoding="utf-8")
    return paths, commands


def _provision(paths: dict[str, Path], **extra: object) -> str:
    return provision(
        port=paths["port"],
        config_file=paths["config"],
        registry_file=paths["registry"],
        firmware_file=paths["firmware"],
        python=Path("python3"),
        esptool=None,
        nvs_generator=Path("nvs_partition_gen.py"),
        backup_dir=paths["backups"],
        **extra,  # type: ignore[arg-type]
    )


def test_a_cable_alone_never_reflashes_a_provisioned_display(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths, commands = _prepare(tmp_path, monkeypatch)
    assert _provision(paths) == f"already provisioned: {MAC}"
    assert commands == []


def test_force_reflashes_and_keeps_the_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths, commands = _prepare(tmp_path, monkeypatch)
    assert _provision(paths, force=True) == f"provisioned: {MAC}"
    assert any("write_flash" in command for command in commands)
    registry = json.loads(paths["registry"].read_text(encoding="utf-8"))
    assert registry["devices"][MAC]["token"] == "t" * 48


def test_the_udev_unit_cannot_reflash_on_its_own() -> None:
    unit = Path("deploy/lanternina-trmnl-provision@.service").read_text(encoding="utf-8")
    assert "--force" not in unit


def test_waiting_for_a_sleeping_display_gives_up_instead_of_hanging(tmp_path: Path) -> None:
    wait_for_port(tmp_path, 0.0)
    with pytest.raises(TimeoutError):
        wait_for_port(tmp_path / "absent", 0.2)