"""Cache the parent-selected display interval for the local display server."""

from __future__ import annotations

import json
from pathlib import Path


def save_interval(path: Path, minutes: object) -> None:
    if isinstance(minutes, bool) or not isinstance(minutes, int) or not 1 <= minutes <= 1440:
        raise ValueError("display polling interval must be 1 to 1440 whole minutes")
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({"minutes": minutes}), encoding="utf-8")
    temporary.replace(path)


def interval_seconds(path: Path | None) -> int | None:
    if path is None:
        return None
    try:
        minutes = json.loads(path.read_text(encoding="utf-8"))["minutes"]
        if isinstance(minutes, bool) or not isinstance(minutes, int) or not 1 <= minutes <= 1440:
            return None
        return minutes * 60
    except (OSError, ValueError, KeyError, TypeError):
        return None