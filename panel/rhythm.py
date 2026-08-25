"""When the house may do something, and how often.

Both were constants in the hub's code. Neither is ours to choose: a picture at four in the
morning spends battery on something nobody will look at, and the right spacing depends on
the room rather than on us.

The parent writes it here and nothing happens. The hub reads it on its next run and
decides for itself, which is the only order that keeps the panel unable to reach into the
house.

An afternoon has its own two settings, added 21 August 2026, and they are here rather than
in their own store because they answer the same question the other three do: when. The
default is no day at all. A house that has never been told when an afternoon may begin
never begins one, which is the right default for something that prints paper and puts
words on a display — and it means the feature arrives switched off rather than arriving.

There is no setting for how many, and there will not be one. The days say when it may
happen, the band says until when, and nothing counts what did.

Everything is minutes past midnight, in one unit: the two ends of each band, the spacing
between pictures and the hours an afternoon may begin and stop beginning are all clock
arithmetic, and a second unit is the usual way that goes wrong. What crosses the API is
"HH:MM" for the hours and a count of minutes for the spacing.

Both bands are said the way round a parent thinks — the hours a thing may happen, not the
hours it may not. It was a "pause" until 25 August 2026, and a parent could not tell what
it bounded: it sat above the afternoon controls and bounded only the pictures.
"""

from __future__ import annotations

import re
import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.clock import known_zone

from .reminders import DAYS

# The hub's timer fires once a minute, so a minute is the finest spacing it can honour.
# Above a day the setting stops being a rhythm.
MIN_CADENCE_MINUTES = 1
MAX_CADENCE_MINUTES = 24 * 60

# When the display may change its picture. A band, said the way round a parent thinks: the
# hours it may happen, not the hours it may not. It was a "pause" until 25 August 2026, and
# a parent reading the page could not tell what the pause bounded — it sat above the
# afternoon controls and bounded only the pictures.
DEFAULT_PICTURES_FROM_MINUTES = 7 * 60
DEFAULT_PICTURES_UNTIL_MINUTES = 22 * 60
DEFAULT_CADENCE_MINUTES = 60

# Mid-afternoon to before dinner, which is what the words mean. Only the default: no day is
# chosen by default, so this decides nothing until a parent picks one.
DEFAULT_AFTERNOON_FROM_MINUTES = 15 * 60
DEFAULT_AFTERNOON_UNTIL_MINUTES = 19 * 60

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
    pictures_from_minutes: int = DEFAULT_PICTURES_FROM_MINUTES
    pictures_until_minutes: int = DEFAULT_PICTURES_UNTIL_MINUTES
    cadence_minutes: int = DEFAULT_CADENCE_MINUTES
    # Which days an afternoon may begin on, and between which hours. Empty days mean none,
    # which is where every household starts.
    afternoon_days: tuple[str, ...] = ()
    afternoon_from_minutes: int = DEFAULT_AFTERNOON_FROM_MINUTES
    afternoon_until_minutes: int = DEFAULT_AFTERNOON_UNTIL_MINUTES
    # Where the house is, as an IANA name. Empty means the hub uses whatever zone its own
    # operating system is set to, which is what every house did before 25 August 2026 and
    # is why one of them honoured every chosen hour an hour late.
    time_zone: str = ""
    updated_at: float = 0.0
    updated_by: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "picturesFrom": clock(self.pictures_from_minutes),
            "picturesUntil": clock(self.pictures_until_minutes),
            "cadenceMinutes": self.cadence_minutes,
            "afternoonDays": list(self.afternoon_days),
            "afternoonFrom": clock(self.afternoon_from_minutes),
            "afternoonUntil": clock(self.afternoon_until_minutes),
            "timeZone": self.time_zone,
            "dayChoices": list(DAYS),
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


def days_of(value: Any) -> tuple[str, ...]:
    """The chosen days, in week order and without repeats. Raises ValueError on a name
    that is not a day: an unrecognised one dropped quietly is a day the parent believes
    they chose."""
    if isinstance(value, str) or not isinstance(value, Iterable):
        raise ValueError("the days are a list")
    chosen = {str(day).strip().lower() for day in value}
    unknown = sorted(chosen - set(DAYS))
    if unknown:
        raise ValueError(f"not a day of the week: {', '.join(unknown)}")
    return tuple(day for day in DAYS if day in chosen)


def zone_of(value: Any) -> str:
    """An IANA timezone name this machine can resolve, or empty for the hub's own.

    Refused rather than dropped when it is not a zone: a name the parent believes they
    chose, silently ignored, is an hour of error nobody can see. The list is not sent to
    the browser — it has `Intl.supportedValuesOf('timeZone')` of its own — so this is where
    the two sides are kept honest.
    """
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("the timezone is a name like Europe/Rome")
    name = value.strip()
    if not known_zone(name):
        raise ValueError(f"not a timezone this system knows: {name}")
    return name


def clean_rhythm(
    household_id: str,
    *,
    pictures_from: Any,
    pictures_until: Any,
    cadence_minutes: Any,
    afternoon_days: Any = (),
    afternoon_from: Any = None,
    afternoon_until: Any = None,
    time_zone: Any = None,
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
    begins = (
        DEFAULT_AFTERNOON_FROM_MINUTES
        if afternoon_from is None
        else minutes_of(afternoon_from, "the hour an afternoon may begin")
    )
    ends = (
        DEFAULT_AFTERNOON_UNTIL_MINUTES
        if afternoon_until is None
        else minutes_of(afternoon_until, "the hour after which no afternoon begins")
    )
    # Refused rather than swapped or wrapped: an afternoon prints paper and takes an hour,
    # so a band that runs through the middle of the night is a typing mistake, not a wish.
    if ends <= begins:
        raise ValueError("an afternoon must stop being allowed after it starts being allowed")
    return Rhythm(
        household_id=household_id,
        pictures_from_minutes=minutes_of(pictures_from, "the start of the picture hours"),
        pictures_until_minutes=minutes_of(pictures_until, "the end of the picture hours"),
        cadence_minutes=cadence_minutes,
        afternoon_days=days_of(afternoon_days),
        afternoon_from_minutes=begins,
        afternoon_until_minutes=ends,
        time_zone=zone_of(time_zone),
        updated_at=time.time(),
        updated_by=updated_by,
    )


def inside_band(now_minutes: int, start: int, end: int) -> bool:
    """Whether the clock is inside an open band. Equal ends mean all day.

    A band may wrap past midnight — pictures from 07:00 until 22:00 does not, a house that
    chose 20:00 until 08:00 does — so the two cases are separate and neither is the other's
    negation.
    """
    if start == end:
        return True
    if start < end:
        return start <= now_minutes < end
    return now_minutes >= start or now_minutes < end
