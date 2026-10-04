"""Build and install the identity-bound M5Stack Timer Camera target on the hub."""

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
CORE = "/srv/lanternina/tools/m5stack-platformio"
FLASH_BYTES = 4 * 1024 * 1024


def run(command: list[str], *, capture: bool = False) -> str:
    began = time.monotonic()
    try:
        result = subprocess.run(
            command, check=True, timeout=900, capture_output=capture, text=True,
        )
        return result.stdout or ""
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s", flush=True)


def verify_hardware(output: str, mac: str) -> None:
    patterns = (
        r"^Chip is ESP32-D0WDQ6-V3(?:\s|$)",
        rf"^MAC: {re.escape(camera_mac(mac))}\s*$",
        r"^Detected flash size: 4MB\s*$",
    )
    if not all(re.search(pattern, output, re.MULTILINE | re.IGNORECASE) for pattern in patterns):
        raise ValueError("expected matching MAC, ESP32-D0WDQ6-V3 and 4 MiB flash")


def verify_backup(backup: Path) -> str:
    if backup.stat().st_size != FLASH_BYTES:
        raise ValueError("the complete M5Stack backup must contain 4,194,304 bytes")
    with backup.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    checksum = backup.with_suffix(".bin.sha256")
    if not checksum.exists() or checksum.read_text().split()[:1] != [digest]:
        raise ValueError("the original M5Stack backup checksum does not match")
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
    if not memory or not 3 * 1024 * 1024 <= int(memory[1]) <= 4 * 1024 * 1024:
        raise ValueError("expected the ESP32's 4 MiB mapped PSRAM heap")
    fields = dict(re.findall(r"\b(\w+)=([^\s]+)", status))
    expected = {
        "filesystem": "1", "identity": camera_mac(mac), "board": "m5stack-timer-camera",
        "button_gpio": "4", "wake_gpio": "13", "led_gpio": "2",
    }
    if any(fields.get(key) != value for key, value in expected.items()):
        raise ValueError("M5Stack flashed but hardware/status verification failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--first-install", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    mac = camera_mac(args.mac)
    port = Path(args.port)
    if port.parent != Path("/dev/serial/by-id") or not port.exists():
        raise ValueError("select the present camera using its stable /dev/serial/by-id path")
    with provisioning_lock():
        config = json.loads(Path("/etc/lanternina/camera.json").read_text())
        if mac not in config["cameras"]:
            raise ValueError("enroll this camera with setup-camera.py before building")
        tool = [PYTHON, "-m", "esptool", "--chip", "esp32", "--port", str(port),
                "--baud", "115200", "--before", "default_reset", "--after", "hard_reset"]
        verify_hardware(run(tool + ["flash_id"], capture=True), mac)
        backups = Path("/var/lib/lanternina/camera-backups")
        backup = backups / f"{mac.replace(':', '')}.bin"
        print(f"Verified original backup SHA256={verify_backup(backup)}", flush=True)
        installed = backups / f"{mac.replace(':', '')}.m5stack-installed"
        validate_update(args.first_install, installed.exists())
        wifi = json.loads(Path("/etc/lanternina/trmnl-provisioning.json").read_text())
        build = prepare_build(
            SOURCE / "firmware/camera-m5stack",
            Path("/srv/lanternina/build/m5stack-cameras"), config, wifi, mac,
        )
        (build / "data").mkdir(exist_ok=True)
        environment = ["env", f"PLATFORMIO_CORE_DIR={CORE}", PIO, "run", "-d", str(build)]
        run(environment)
        if args.build_only:
            return
        if args.first_install:
            run(tool + ["verify_flash", "0", str(backup)])
        flashed_at = time.time()
        run(environment + ["-t", "upload", "--upload-port", str(port)])
        if args.first_install:
            run(environment + ["-t", "uploadfs", "--upload-port", str(port)])
            installed.write_text(f"{flashed_at}\n", encoding="ascii")
        run(tool + ["run"])
        status = run([
            PYTHON, str(SOURCE / "tools/camera_usb.py"), "REPORT", "--mac", mac,
            "--port", str(port), "--authenticated-since", str(flashed_at),
        ], capture=True)
        print(status, flush=True)
        verify_status(status, mac)


if __name__ == "__main__":
    main()