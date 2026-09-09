"""Verify live camera telemetry and a synthetic cloud archive/delete cycle on the hub."""

from __future__ import annotations

import base64
import io
import json
import os
import shlex
import time
import uuid
from pathlib import Path

from PIL import Image, ImageDraw

from devices.ask_panel import _ask
from devices.camera_hub import CameraHub
from devices.house import House
from devices.sync_photos import synchronize


def main() -> None:
    for name in ("panel.env", "trmnl-byos.env", "experience.env", "scanner.env"):
        for line in (Path("/etc/lanternina") / name).read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            key, separator, value = line.partition("=")
            if separator:
                values = shlex.split(value)
                os.environ[key.strip()] = " ".join(values)
    config = json.loads(Path("/etc/lanternina/camera.json").read_text())
    house = House(
        panel=os.environ["LANTERNINA_PANEL_URL"],
        household=os.environ["LANTERNINA_HOUSEHOLD"],
        device_key=os.environ["LANTERNINA_DEVICE_KEY"],
        sheets_dir=Path(os.environ["LANTERNINA_SHEETS_DIR"]),
    )
    hub = CameraHub(config, house, Path(os.environ["TRMNL_SCREEN_FILE"]))
    reports = hub.store.cameras()
    if not reports:
        raise RuntimeError("no authenticated camera telemetry has arrived")
    print("camera telemetry:", json.dumps(reports))
    print("synchronized photographs:", synchronize(hub))
    prefix = f"{house.panel.rstrip('/')}/api/device/{house.household}/photos"
    photo_id = uuid.uuid4().hex
    image = Image.new("RGB", (320, 240), "white")
    ImageDraw.Draw(image).text((30, 110), "CAMERA ARCHIVE TEST", fill="black")
    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    body = {
        "id": photo_id,
        "camera": "integration-test",
        "receivedAt": time.time(),
        "state": "done",
        "imageBase64": base64.b64encode(buffer.getvalue()).decode(),
    }

    def ask(path: str, data: dict) -> dict:
        return _ask(prefix + path, data, key=house.device_key, timeout=30)

    try:
        for _attempt in range(2):
            receipt = ask("", body)
            assert receipt == {"id": photo_id, "stored": True, "deleted": False}, receipt
        receipt = ask(f"/{photo_id}/delete", {})
        assert receipt == {"id": photo_id, "deleted": True}, receipt
        receipt = ask("", body)
        assert receipt == {"id": photo_id, "stored": False, "deleted": True}, receipt
        print("VERDICT: live upload, duplicate and deletion tombstone passed")
    finally:
        ask(f"/{photo_id}/delete", {})


if __name__ == "__main__":
    main()
