"""Build and flash one enrolled camera, preserving its queue on updates."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from devices.camera_provision import (
    camera_mac,
    prepare_build,
    provisioning_lock,
    verify_hardware,
)

SOURCE = Path(__file__).resolve().parents[1]
PYTHON = "/srv/lanternina/tools/platformio-venv/bin/python"
PIO = "/srv/lanternina/tools/platformio-venv/bin/pio"


def run(command: list[str], *, capture: bool = False) -> str:
    began = time.monotonic()
    try:
        result = subprocess.run(command, check=True, timeout=600, capture_output=capture, text=True)
        return result.stdout or ""
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", required=True)
    parser.add_argument("--first-install", action="store_true")
    parser.add_argument("--hub-address")
    parser.add_argument("--build-user", default="fausto")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    mac = camera_mac(args.mac)
    if args.hub_address:
        run(["python3", str(SOURCE / "deploy/setup-camera.py"), "--mac", mac,
             "--hub-address", args.hub_address, "--build-user", args.build_user])
    with provisioning_lock():
        provision(args, mac)


def provision(args: argparse.Namespace, mac: str) -> None:
    import pwd

    owner = pwd.getpwnam(args.build_user)
    if not Path(PIO).exists():
        Path(PYTHON).parents[1].parent.mkdir(parents=True, exist_ok=True)
        run(["python3", "-m", "venv", str(Path(PYTHON).parents[1])])
        run([PYTHON, "-m", "pip", "install", "platformio==6.1.18", "esptool==4.8.1"])
    config = json.loads(Path("/etc/lanternina/camera.json").read_text())
    if mac not in config["cameras"]:
        raise ValueError("this board is not enrolled as a camera")
    if not config.get("hub_address"):
        raise ValueError("pass --hub-address once to migrate the existing camera configuration")
    port = Path(f"/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_{mac}-if00")
    if not port.exists():
        raise ValueError("the enrolled camera is not on USB")
    backups = Path("/var/lib/lanternina/camera-backups")
    backups.mkdir(parents=True, exist_ok=True, mode=0o700)
    backup = backups / (mac.replace(":", "") + ".bin")
    tool = [PYTHON, "-m", "esptool", "--chip", "esp32s3", "--port", str(port)]
    detected = run(tool + ["--before", "usb_reset", "flash_id"], capture=True)
    verify_hardware(detected, mac)
    print(f"Verified {mac}: ESP32-S3, 8 MiB flash", flush=True)
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
    wifi = json.loads(Path("/etc/lanternina/trmnl-provisioning.json").read_text())
    build = prepare_build(SOURCE / "firmware/camera", Path("/srv/lanternina/build/cameras"),
                          config, wifi, mac)
    core = Path("/srv/lanternina/tools/camera-platformio")
    core.mkdir(parents=True, exist_ok=True)
    os.chown(core, owner.pw_uid, owner.pw_gid)
    for path in [build, *build.rglob("*")]:
        os.chown(path, owner.pw_uid, owner.pw_gid)
    command = [
        "runuser",
        "-u",
        args.build_user,
        "--",
        "env",
        "PLATFORMIO_CORE_DIR=/srv/lanternina/tools/camera-platformio",
        "PATH=/srv/lanternina/tools/platformio-venv/bin:" + os.environ["PATH"],
        PIO,
        "run",
        "-d",
        str(build),
    ]
    run(command)
    if args.build_only:
        return
    flashed_at = time.time()
    run(command + ["-t", "upload", "--upload-port", str(port)])
    if args.first_install:
        run(command + ["-t", "uploadfs", "--upload-port", str(port)])
    run(tool + ["--before", "usb_reset", "--after", "hard_reset", "run"])
    installed.touch(mode=0o600)
    status = run([
        PYTHON, str(SOURCE / "tools/camera_usb.py"), "STATUS", "--mac", mac,
        "--authenticated-since", str(flashed_at),
    ], capture=True)
    if "filesystem=1" not in status or f"identity={mac}" not in status:
        raise ValueError("firmware flashed but USB identity/filesystem verification failed")
    print(status, flush=True)


if __name__ == "__main__":
    main()
