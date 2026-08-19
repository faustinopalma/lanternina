"""Provision a TRMNL DIY kit connected to the Lanternina hub over USB."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from devices.trmnl_byos import load_devices, mark_provisioned, normalize_mac, register_device

NVS_OFFSET = "0x9000"
NVS_SIZE = "0x5000"
FLASH_SIZE = "0x1000000"
FLASH_SIZE_BYTES = int(FLASH_SIZE, 16)
MAC_PATTERN = re.compile(r"^[0-9A-F]{2}(?::[0-9A-F]{2}){5}$")
PORT_POLL_SECONDS = 0.1


@dataclass(frozen=True, slots=True)
class ProvisioningConfig:
    ssid: str
    password: str
    base_url: str

    @classmethod
    def load(cls, path: Path) -> ProvisioningConfig:
        document = json.loads(path.read_text(encoding="utf-8"))
        config = cls(
            ssid=str(document["ssid"]),
            password=str(document["password"]),
            base_url=str(document.get("base_url", "http://lanternina.local:8080")),
        )
        if not config.ssid or not config.password:
            raise ValueError("Wi-Fi SSID and password must be configured")
        return config


def wait_for_port(port: Path, seconds: float) -> None:
    """A running display is on the USB bus only while awake — a few seconds every minute."""
    deadline = time.monotonic() + seconds
    while not port.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"serial port never appeared: {port}")
        time.sleep(PORT_POLL_SECONDS)


def device_mac(port: Path) -> str:
    output = subprocess.run(
        ["udevadm", "info", "--query=property", f"--name={port}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    properties = dict(line.split("=", 1) for line in output.splitlines() if "=" in line)
    mac = normalize_mac(properties.get("ID_SERIAL_SHORT", ""))
    if not MAC_PATTERN.fullmatch(mac):
        raise ValueError("USB device does not expose an ESP32 MAC serial number")
    return mac


def write_nvs_csv(path: Path, config: ProvisioningConfig) -> None:
    rows = [
        ("key", "type", "encoding", "value"),
        ("wificaptive", "namespace", "", ""),
        ("wifi_0_ssid", "data", "string", config.ssid),
        ("wifi_0_pswd", "data", "string", config.password),
        ("wifi_0_5g", "data", "u8", "0"),
        ("wifi_0_ent", "data", "u8", "0"),
        ("wifi_last_index", "data", "i32", "0"),
        ("data", "namespace", "", ""),
        ("api_url", "data", "string", config.base_url),
    ]
    with path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerows(rows)
    path.chmod(0o600)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def provision(
    *,
    port: Path,
    config_file: Path,
    registry_file: Path,
    firmware_file: Path,
    python: Path,
    esptool: Path | None,
    nvs_generator: Path,
    backup_dir: Path,
    force: bool = False,
    wait_seconds: float = 0.0,
) -> str:
    wait_for_port(port, wait_seconds)
    mac = device_mac(port)
    existing = load_devices(registry_file).get(mac) if registry_file.exists() else None
    # Plugging a cable must never reflash on its own; only an explicit --force may.
    if existing is not None and existing.provisioned and not force:
        return f"already provisioned: {mac}"

    config = ProvisioningConfig.load(config_file)
    register_device(registry_file, mac)

    with tempfile.TemporaryDirectory(prefix="lanternina-trmnl-") as directory:
        work = Path(directory)
        csv_file = work / "nvs.csv"
        nvs_file = work / "nvs.bin"
        write_nvs_csv(csv_file, config)
        run(
            [
                str(python),
                str(nvs_generator),
                "generate",
                str(csv_file),
                str(nvs_file),
                NVS_SIZE,
                "--outdir",
                str(work),
            ]
        )
        esptool_command = (
            [str(python), str(esptool)] if esptool is not None else [str(python), "-m", "esptool"]
        )
        common = esptool_command + [
            "--chip",
            "esp32s3",
            "--port",
            str(port),
            "--baud",
            "460800",
        ]
        backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        backup_file = backup_dir / f"{mac.replace(':', '')}.bin"
        if backup_file.exists() and backup_file.stat().st_size != FLASH_SIZE_BYTES:
            backup_file.unlink()
        if not backup_file.exists():
            partial_backup = backup_file.with_suffix(".bin.partial")
            partial_backup.unlink(missing_ok=True)
            run(
                common
                + [
                    "--before",
                    "usb_reset",
                    "--after",
                    "no_reset",
                    "read_flash",
                    "0x0",
                    FLASH_SIZE,
                    str(partial_backup),
                ]
            )
            if partial_backup.stat().st_size != FLASH_SIZE_BYTES:
                raise ValueError("flash backup has an unexpected size")
            partial_backup.chmod(0o600)
            partial_backup.replace(backup_file)
        run(
            common
            + [
                "--before",
                "usb_reset",
                "--after",
                "no_reset",
                "write_flash",
                "0x0",
                str(firmware_file),
            ]
        )
        run(
            common
            + [
                "--before",
                "no_reset",
                "--after",
                "hard_reset",
                "write_flash",
                NVS_OFFSET,
                str(nvs_file),
            ]
        )

    mark_provisioned(registry_file, mac)
    return f"provisioned: {mac}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=Path, required=True)
    parser.add_argument(
        "--config", type=Path, default=Path("/etc/lanternina/trmnl-provisioning.json")
    )
    parser.add_argument(
        "--registry", type=Path, default=Path("/etc/lanternina/trmnl-devices.json")
    )
    parser.add_argument(
        "--firmware",
        type=Path,
        default=Path("/opt/lanternina/firmware/trmnl-7inch5-og-diy-kit.bin"),
    )
    parser.add_argument(
        "--python", type=Path, default=Path("/srv/lanternina/tools/platformio-venv/bin/python")
    )
    parser.add_argument(
        "--esptool",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--nvs-generator",
        type=Path,
        default=Path("/srv/lanternina/tools/nvs_partition_gen.py"),
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=Path("/var/lib/lanternina/trmnl-backups"),
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--wait-seconds", type=float, default=0.0)
    args = parser.parse_args()
    print(provision(
        port=args.port,
        config_file=args.config,
        registry_file=args.registry,
        firmware_file=args.firmware,
        python=args.python,
        esptool=args.esptool,
        nvs_generator=args.nvs_generator,
        backup_dir=args.backup_dir,
        force=args.force,
        wait_seconds=args.wait_seconds,
    ))


if __name__ == "__main__":
    main()