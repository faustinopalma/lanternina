"""Cache the parent-selected display interval for the local display server."""

from __future__ import annotations

import json
from pathlib import Path


def save_interval(path: Path, minutes: object, things: object = None) -> None:
    if isinstance(minutes, bool) or not isinstance(minutes, int) or not 1 <= minutes <= 1440:
        raise ValueError("display polling interval must be 1 to 1440 whole minutes")
    devices = {}
    for thing in things if isinstance(things, list) else ():
        if not isinstance(thing, dict) or thing.get("kind") != "display":
            continue
        chosen = thing.get("displayPollMinutes")
        if chosen is None:
            continue
        if isinstance(chosen, bool) or not isinstance(chosen, int) or not 1 <= chosen <= 1440:
            raise ValueError("display polling interval must be 1 to 1440 whole minutes")
        devices[str(thing["id"])] = chosen
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({"minutes": minutes, "devices": devices}), encoding="utf-8")
    temporary.replace(path)


def interval_seconds(path: Path | None, device_id: str = "") -> int | None:
    if path is None:
        return None
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        minutes = document.get("devices", {}).get(device_id, document["minutes"])
        if isinstance(minutes, bool) or not isinstance(minutes, int) or not 1 <= minutes <= 1440:
            return None
        return minutes * 60
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None