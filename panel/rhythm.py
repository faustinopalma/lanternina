"""When the display may change, and how often.

Both were constants in the hub's code. Neither is ours to choose: a picture at four in the
morning spends battery on something nobody will look at, and the right spacing depends on
the room rather than on us.

The parent writes it here and nothing happens. The hub reads it on its next run and
decides for itself, which is the only order that keeps the panel unable to reach into the
house.

Everything is minutes past midnight, in one unit: the two ends of the pause and the
spacing between pictures are all clock arithmetic, and a second unit is the usual way that
goes wrong. What crosses the API is "HH:MM" for the ends and a count of minutes for the
spacing.
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# The hub's timer fires once a minute, so a minute is the finest spacing it can honour.
# Above a day the setting stops being a rhythm.
MIN_CADENCE_MINUTES = 1
MAX_CADENCE_MINUTES = 24 * 60

DEFAULT_QUIET_FROM_MINUTES = 22 * 60
DEFAULT_QUIET_UNTIL_MINUTES = 7 * 60
DEFAULT_CADENCE_MINUTES = 60

_CLOCK = re.compile(r"^(\d{1,2}):(\d{2})$")


def clock(minutes: int) -> str:
    """Minutes past midnight as the parent wrote them: 1350 is "22:30"."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def minutes_of(value: Any, name: str) -> int:
    """Parse "HH:MM". Raises ValueError if it is not a time on the clock."""
    if not isinstance(value, str) or not _CLOCK.match(value.strip()):
        raise ValueError(f"{name} is written as HH:MM")
    hour, minute = (int(part) for part in value.strip().split(":"))
    if hour > 23 or minute > 59:
        raise ValueError(f"{name} must be a time between 00:00 and 23:59")
    return hour * 60 + minute


@dataclass(frozen=True, slots=True)
class Rhythm:
    household_id: str
    quiet_from_minutes: int = DEFAULT_QUIET_FROM_MINUTES
    quiet_until_minutes: int = DEFAULT_QUIET_UNTIL_MINUTES
    cadence_minutes: int = DEFAULT_CADENCE_MINUTES
    updated_at: float = 0.0
    updated_by: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "quietFrom": clock(self.quiet_from_minutes),
            "quietUntil": clock(self.quiet_until_minutes),
            "cadenceMinutes": self.cadence_minutes,
            "updatedAt": self.updated_at,
            "minCadenceMinutes": MIN_CADENCE_MINUTES,
            "maxCadenceMinutes": MAX_CADENCE_MINUTES,
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


def clean_rhythm(
    household_id: str,
    *,
    quiet_from: Any,
    quiet_until: Any,
    cadence_minutes: Any,
    updated_by: str = "",
) -> Rhythm:
    """Normalise what the parent chose. Raises ValueError if it cannot be honoured."""
    if isinstance(cadence_minutes, bool) or not isinstance(cadence_minutes, int):
        raise ValueError("the spacing is a whole number of minutes")
    if not MIN_CADENCE_MINUTES <= cadence_minutes <= MAX_CADENCE_MINUTES:
        raise ValueError(
            f"the spacing must be between {MIN_CADENCE_MINUTES} and "
            f"{MAX_CADENCE_MINUTES} minutes"
        )
    return Rhythm(
        household_id=household_id,
        quiet_from_minutes=minutes_of(quiet_from, "the start of the pause"),
        quiet_until_minutes=minutes_of(quiet_until, "the end of the pause"),
        cadence_minutes=cadence_minutes,
        updated_at=time.time(),
        updated_by=updated_by,
    )


def in_quiet_window(now_minutes: int, start: int, end: int) -> bool:
    """Equal ends mean no pause at all, so a parent can turn the window off."""
    if start == end:
        return False
    if start < end:
        return start <= now_minutes < end
    return now_minutes >= start or now_minutes < end
