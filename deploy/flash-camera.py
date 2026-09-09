"""Build and flash one enrolled camera, preserving its queue on updates."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

BUILD = Path("/srv/lanternina/build/camera")
PYTHON = "/srv/lanternina/tools/platformio-venv/bin/python"
PIO = "/srv/lanternina/tools/platformio-venv/bin/pio"


def run(command: list[str]) -> None:
    began = time.monotonic()
    try:
        subprocess.run(command, check=True, timeout=240)
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", required=True)
    parser.add_argument("--first-install", action="store_true")
    args = parser.parse_args()
    mac = args.mac.upper()
    config = json.loads(Path("/etc/lanternina/camera.json").read_text())
    if mac not in config["cameras"]:
        raise ValueError("this board is not enrolled as a camera")
    port = Path(f"/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_{mac}-if00")
    if not port.exists():
        raise ValueError("the enrolled camera is not on USB")
    backups = Path("/var/lib/lanternina/camera-backups")
    backups.mkdir(exist_ok=True, mode=0o700)
    backup = backups / (mac.replace(":", "") + ".bin")
    tool = [PYTHON, "-m", "esptool", "--chip", "esp32s3", "--port", str(port)]
    if not backup.exists():
        partial = backup.with_suffix(".partial")
        run(
            tool
            + [
                "--baud",
                "921600",
                "--before",
                "usb_reset",
                "--after",
                "no_reset",
                "read_flash",
                "0",
                "0x800000",
                str(partial),
            ]
        )
        if partial.stat().st_size != 8388608:
            raise ValueError("incomplete camera backup")
        partial.chmod(0o600)
        partial.replace(backup)
    if backup.stat().st_size != 8388608:
        raise ValueError("camera backup is not 8 MiB")
    installed = backups / (mac.replace(":", "") + ".installed")
    if args.first_install and installed.exists():
        raise ValueError("already installed: refusing to erase the photograph queue")
    command = [
        "runuser",
        "-u",
        "fausto",
        "--",
        "env",
        "PLATFORMIO_CORE_DIR=/srv/lanternina/tools/camera-platformio",
        "PATH=/srv/lanternina/tools/platformio-venv/bin:" + os.environ["PATH"],
        PIO,
        "run",
        "-d",
        str(BUILD),
    ]
    run(command)
    run(command + ["-t", "upload", "--upload-port", str(port)])
    if args.first_install:
        run(command + ["-t", "uploadfs", "--upload-port", str(port)])
    run(tool + ["--before", "usb_reset", "--after", "hard_reset", "run"])
    installed.touch(mode=0o600)


if __name__ == "__main__":
    main()
