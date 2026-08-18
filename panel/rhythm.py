"""When the display may change, and how often.

Both were constants in the hub's code. Neither is ours to choose: a picture at four in the
morning spends battery on something nobody will look at, and the right spacing depends on
the room rather than on us.

The parent writes it here and nothing happens. The hub reads it on its next run and
decides for itself, which is the only order that keeps the panel unable to reach into the
house.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# The hub asks once an hour, so anything finer cannot be honoured and is not offered.
CADENCE_CHOICES = (1, 2, 3, 4, 6, 8, 12, 24)

DEFAULT_QUIET_FROM_HOUR = 22
DEFAULT_QUIET_UNTIL_HOUR = 7
DEFAULT_CADENCE_HOURS = 1


@dataclass(frozen=True, slots=True)
class Rhythm:
    household_id: str
    quiet_from_hour: int = DEFAULT_QUIET_FROM_HOUR
    quiet_until_hour: int = DEFAULT_QUIET_UNTIL_HOUR
    cadence_hours: int = DEFAULT_CADENCE_HOURS
    updated_at: float = 0.0
    updated_by: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "quietFromHour": self.quiet_from_hour,
            "quietUntilHour": self.quiet_until_hour,
            "cadenceHours": self.cadence_hours,
            "updatedAt": self.updated_at,
            "cadenceChoices": list(CADENCE_CHOICES),
        }


@runtime_checkable
class RhythmStore(Protocol):
    def get(self, household_id: str) -> Rhythm: ...

    def set(self, rhythm: Rhythm) -> Rhythm: ...


@dataclass
class InMemoryRhythmStore:
    _rows: dict[str, Rhythm] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get(self, household_id: str) -> Rhythm:
        with self._lock:
            # A household that has never chosen gets the defaults, not an error: the hub
            # has to be able to run before anyone has opened the panel.
            return self._rows.get(household_id, Rhythm(household_id=household_id))

    def set(self, rhythm: Rhythm) -> Rhythm:
        with self._lock:
            self._rows[rhythm.household_id] = rhythm
            return rhythm


def _clean_hour(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a whole hour")
    if not 0 <= value <= 23:
        raise ValueError(f"{name} must be between 0 and 23")
    return value


def clean_rhythm(
    household_id: str,
    *,
    quiet_from_hour: Any,
    quiet_until_hour: Any,
    cadence_hours: Any,
    updated_by: str = "",
) -> Rhythm:
    """Normalise what the parent chose. Raises ValueError if it cannot be honoured."""
    if isinstance(cadence_hours, bool) or cadence_hours not in CADENCE_CHOICES:
        raise ValueError(f"the cadence must be one of {list(CADENCE_CHOICES)} hours")
    return Rhythm(
        household_id=household_id,
        quiet_from_hour=_clean_hour(quiet_from_hour, "the start of quiet hours"),
        quiet_until_hour=_clean_hour(quiet_until_hour, "the end of quiet hours"),
        cadence_hours=int(cadence_hours),
        updated_at=time.time(),
        updated_by=updated_by,
    )


def in_quiet_hours(hour: int, start: int, end: int) -> bool:
    """Equal ends mean no quiet hours at all, so a parent can turn the window off."""
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end
