"""Identity-bound camera builds; credentials never come from a previous build."""

from __future__ import annotations

import json
import re
import shutil
from contextlib import contextmanager
from pathlib import Path


def camera_mac(value: str) -> str:
    value = value.upper()
    if not re.fullmatch(r"(?:[0-9A-F]{2}:){5}[0-9A-F]{2}", value):
        raise ValueError("expected the complete camera MAC")
    return value


@contextmanager
def provisioning_lock(path: Path = Path("/var/lock/lanternina-camera.lock")):
    import fcntl

    with path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def prepare_build(source: Path, builds: Path, config: dict, wifi: dict, mac: str) -> Path:
    mac = camera_mac(mac)
    token = config["cameras"][mac]
    if not token or token in [value for key, value in config["cameras"].items() if key != mac]:
        raise ValueError("each camera must have its own nonempty token")
    builds.mkdir(parents=True, exist_ok=True)
    builds.chmod(0o711)
    build = builds / mac.replace(":", "")
    build.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name in ("src", "data"):
        if (source / name).exists():
            shutil.copytree(source / name, build / name, dirs_exist_ok=True)
    for name in ("platformio.ini", "partitions.csv"):
        shutil.copy2(source / name, build / name)
    include = build / "include"
    include.mkdir(exist_ok=True)
    values = {
        "WIFI_SSID": wifi["ssid"], "WIFI_PASSWORD": wifi["password"],
        "HUB_URL": f"https://{config['hub_address']}:8443",
        "CAMERA_TOKEN": token, "CAMERA_ID": mac,
        "HUB_CA": Path(config["certificate"]).read_text(encoding="utf-8"),
    }
    header = include / "camera_secrets.h"
    header.write_text(
        "#pragma once\n" + "".join(
            f"static const char *{key} = {json.dumps(value)};\n" for key, value in values.items()
        ), encoding="utf-8", newline="",
    )
    header.chmod(0o600)
    return build


def verify_hardware(output: str, mac: str) -> None:
    if not all(part in output.upper() for part in (
        "ESP32-S3", camera_mac(mac), "DETECTED FLASH SIZE: 8MB",
    )):
        raise ValueError("USB identity, ESP32-S3 and 8 MiB flash must all match before writing")