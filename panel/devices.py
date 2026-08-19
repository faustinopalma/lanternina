"""What each display last reported about itself, for the parent panel.

The charge is deliberately coarse. The board has no fuel gauge, so a percentage would be
arithmetic performed on a guess: the panel says "full", "half", "recharge it" or "on
mains", which is what a person can act on anyway.

Nothing here is about a person. A battery reading is a fact about a device.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# How long a display may stay silent before the panel says so. Two missed hours is well
# past any polling interval we set, so it means something is actually wrong.
SILENT_AFTER_SECONDS = 7200


@dataclass(frozen=True, slots=True)
class DeviceStatus:
    id: str
    household_id: str
    name: str
    last_seen: float
    # "mains", "ok", "low" or "critical" — decided by the hub, which knows the thresholds.
    level: str = "ok"
    voltage: float | None = None
    rssi: float | None = None
    firmware: str = ""
    model: str = ""

    def silent_for(self, now: float | None = None) -> float:
        return max(0.0, (now or time.time()) - self.last_seen)

    def to_public(self, now: float | None = None) -> dict[str, Any]:
        silent = self.silent_for(now)
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "voltage": self.voltage,
            "rssi": self.rssi,
            "firmware": self.firmware,
            "model": self.model,
            "lastSeen": self.last_seen,
            "silentSeconds": silent,
            # The panel is where a fault is allowed to appear. The display never says it.
            "silent": silent > SILENT_AFTER_SECONDS,
        }


@runtime_checkable
class DeviceStatusStore(Protocol):
    def record(self, status: DeviceStatus) -> DeviceStatus: ...

    def list(self, household_id: str) -> list[DeviceStatus]: ...


@dataclass
class InMemoryDeviceStatusStore:
    _rows: dict[tuple[str, str], DeviceStatus] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, status: DeviceStatus) -> DeviceStatus:
        with self._lock:
            self._rows[(status.household_id, status.id)] = status
        return status

    def list(self, household_id: str) -> list[DeviceStatus]:
        with self._lock:
            rows = [
                row
                for (household, _), row in self._rows.items()
                if household == household_id
            ]
        return sorted(rows, key=lambda row: row.name)
