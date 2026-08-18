"""Tell the panel how the displays in this house are doing.

Runs on the hub, on a timer. It reads what each display reported on its last poll and
posts a snapshot upward. State, not history: the panel keeps one row per display, so
nothing here accumulates a record of when the house is awake.

Stdlib only, because the hub has no virtualenv for this and should not need one.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from devices.trmnl_byos import LEVEL_OK, last_state, load_devices, recorded_level

MAINS = "mains"


def snapshot(registry: Path, status_file: Path) -> list[dict[str, object]]:
    devices = load_devices(registry) if registry.exists() else {}
    reported: list[dict[str, object]] = []
    for device in devices.values():
        voltage, on_usb = last_state(status_file, device.mac)
        level = (
            MAINS
            if device.mains or on_usb
            else recorded_level(status_file, device.mac, device.mains)
        )
        entry = _entry(status_file, device.mac)
        reported.append(
            {
                "id": device.mac,
                "name": device.friendly_id or device.mac,
                "lastSeen": float(entry.get("lastSeen") or 0.0),
                "level": level or LEVEL_OK,
                "voltage": voltage,
                "rssi": entry.get("rssi"),
                "firmware": str(entry.get("firmware") or ""),
                "model": str(entry.get("model") or ""),
            }
        )
    return reported


def _entry(status_file: Path, mac: str) -> dict[str, object]:
    if not status_file.exists():
        return {}
    try:
        document = json.loads(status_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    entry = document.get("devices", {}).get(mac)
    return entry if isinstance(entry, dict) else {}


def main() -> int:
    panel = os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/")
    household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
    key = os.environ.get("LANTERNINA_DEVICE_KEY", "")
    if not (panel and household and key):
        print("missing LANTERNINA_PANEL_URL, LANTERNINA_HOUSEHOLD or LANTERNINA_DEVICE_KEY")
        return 1

    registry = Path(os.environ.get("TRMNL_DEVICE_REGISTRY", "/etc/lanternina/trmnl-devices.json"))
    status_file = Path(
        os.environ.get("TRMNL_STATUS_FILE", "/var/lib/lanternina/state/trmnl-status.json")
    )
    reported = snapshot(registry, status_file)
    if not reported:
        print("no displays registered")
        return 0

    request = urllib.request.Request(
        f"{panel}/api/device/{household}/devices",
        data=json.dumps(reported).encode(),
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            answer = json.loads(response.read())
    except (urllib.error.URLError, OSError) as exc:
        # The panel being unreachable is not a fault of this house. Say so and stop.
        print(f"panel unreachable: {exc}")
        return 1
    print(f"reported {len(answer.get('recorded', []))} display(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
