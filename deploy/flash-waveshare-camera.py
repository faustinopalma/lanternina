"""Build and flash a Waveshare camera without changing the XIAO target."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

from devices.camera_provision import camera_mac, prepare_build, provisioning_lock

SOURCE = Path(__file__).resolve().parents[1]
PYTHON = "/srv/lanternina/tools/platformio-venv/bin/python"
PIO = "/srv/lanternina/tools/platformio-venv/bin/pio"
CORE = "/srv/lanternina/tools/waveshare-platformio"
FLASH_BYTES = 16777216


def run(command: list[str], *, capture: bool = False) -> str:
    began = time.monotonic()
    try:
        result = subprocess.run(
            command, check=True, timeout=600, capture_output=capture, text=True,
        )
        return result.stdout or ""
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s", flush=True)


def verify_hardware(output: str, mac: str) -> None:
    patterns = (
        r"^Chip is ESP32-S3(?:\s|$)",
        rf"^MAC: {re.escape(camera_mac(mac))}\s*$",
        r"^Detected flash size: 16MB\s*$",
        r"^Features: .*Embedded PSRAM 8MB",
    )
    if not all(re.search(pattern, output, re.MULTILINE | re.IGNORECASE) for pattern in patterns):
        raise ValueError("expected matching MAC, ESP32-S3, 16 MiB flash and 8 MB PSRAM")


def verify_backup(backup: Path) -> str:
    if backup.stat().st_size != FLASH_BYTES:
        raise ValueError("the complete Waveshare backup must contain 16,777,216 bytes")
    with backup.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    checksum = backup.with_suffix(".bin.sha256")
    if not checksum.exists() or checksum.read_text().split()[0] != digest:
        raise ValueError("the original Waveshare backup checksum does not match")
    if backup.stat().st_mode & 0o077:
        raise ValueError("the original camera backup must be private")
    return digest


def validate_update(first_install: bool, installed: bool) -> None:
    if first_install and installed:
        raise ValueError("already installed: refusing to erase the photograph queue")
    if not first_install and not installed:
        raise ValueError("first installation requires explicit --first-install")


def verify_status(status: str, mac: str) -> None:
    memory = re.search(r"\bpsram=(\d+)\b", status)
    if not memory or not 7 * 1024 * 1024 <= int(memory[1]) <= 8 * 1024 * 1024:
        raise ValueError("Waveshare PSRAM heap is absent or smaller than the bring-up bound")
    if not all(value in status for value in (
        "filesystem=1", f"identity={camera_mac(mac)}", "board=waveshare-ov5640",
        "expander=1", "button_gpio=1", "led_gpio=2",
    )):
        raise ValueError("Waveshare flashed but hardware/status verification failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", required=True)
    parser.add_argument("--first-install", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    mac = camera_mac(args.mac)
    with provisioning_lock():
        config = json.loads(Path("/etc/lanternina/camera.json").read_text())
        if mac not in config["cameras"]:
            raise ValueError("enroll this camera with setup-camera.py before building")
        port = Path(f"/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_{mac}-if00")
        if not port.exists():
            raise ValueError("the selected camera is not present on USB")
        tool = [PYTHON, "-m", "esptool", "--chip", "esp32s3", "--port", str(port)]
        detected = run(tool + ["--before", "usb_reset", "flash_id"], capture=True)
        verify_hardware(detected, mac)
        backups = Path("/var/lib/lanternina/camera-backups")
        backup = backups / f"{mac.replace(':', '')}.bin"
        print(f"Verified original backup SHA256={verify_backup(backup)}", flush=True)
        installed = backups / f"{mac.replace(':', '')}.waveshare-installed"
        validate_update(args.first_install, installed.exists())
        wifi = json.loads(Path("/etc/lanternina/trmnl-provisioning.json").read_text())
        build = prepare_build(
            SOURCE / "firmware/camera-waveshare",
            Path("/srv/lanternina/build/waveshare-cameras"), config, wifi, mac,
        )
        (build / "data").mkdir(exist_ok=True)
        environment = ["env", f"PLATFORMIO_CORE_DIR={CORE}", PIO, "run", "-d", str(build)]
        run(environment)
        if args.build_only:
            return
        flashed_at = time.time()
        run(environment + ["-t", "upload", "--upload-port", str(port)])
        if args.first_install:
            run(environment + ["-t", "uploadfs", "--upload-port", str(port)])
            installed.write_text(f"{flashed_at}\n", encoding="ascii")
        run(tool + ["--before", "usb_reset", "--after", "hard_reset", "run"])
        status = run([
            PYTHON, str(SOURCE / "tools/camera_usb.py"), "STATUS", "--mac", mac,
            "--authenticated-since", str(flashed_at),
        ], capture=True)
        print(status, flush=True)
        verify_status(status, mac)


if __name__ == "__main__":
    main()
