"""Bound device diagnostics without treating an announced sleep as observed sleep."""

from __future__ import annotations

import math
from typing import Any

TEXT_FIELDS = {
    "phase",
    "bootId",
    "previousBootId",
    "trigger",
    "captureResult",
    "captureId",
    "uploadId",
    "networkResult",
    "wakeCause",
    "resetReason",
}
NUMBER_FIELDS = {
    "uptimeMs",
    "captureMs",
    "sensorInitMs",
    "frameReadyMs",
    "storageMs",
    "uploadMs",
    "workMs",
    "jpegBytes",
    "width",
    "height",
    "queued",
    "freeHeap",
    "freePsram",
    "filesystemUsed",
    "filesystemTotal",
    "uploadHttp",
    "previousSleepAt",
    "sleepSeconds",
    "wakeCount",
    "resetCode",
}
BOOL_FIELDS = {
    "usb", "buttonPressed", "clockSet", "previousSleepConfirmed", "uploadAccepted",
    "captureRequested",
}


def clean_diagnostics(values: Any) -> dict[str, Any]:
    if not isinstance(values, dict):
        raise ValueError("diagnostics must be an object")
    cleaned: dict[str, Any] = {}
    for key in TEXT_FIELDS:
        if key in values:
            if not isinstance(values[key], str) or len(values[key]) > 96:
                raise ValueError("invalid diagnostic text")
            cleaned[key] = values[key]
    for key in NUMBER_FIELDS:
        if key in values:
            value = values[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("invalid diagnostic number")
            if not math.isfinite(value) or not -1000 <= value <= 1e13:
                raise ValueError("diagnostic number out of range")
            cleaned[key] = value
    for key in BOOL_FIELDS:
        if key in values:
            if not isinstance(values[key], bool):
                raise ValueError("invalid diagnostic flag")
            cleaned[key] = values[key]
    return cleaned
