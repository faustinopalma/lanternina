from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from devices.trmnl_provision import ProvisioningConfig, write_nvs_csv


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