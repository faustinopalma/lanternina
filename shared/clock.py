"""What time it is where the house is.

Every decision about when — the pause in the evening, the hour an afternoon may begin, the
moment a reminder is due — is wall-clock arithmetic, and wall-clock arithmetic needs a
place. Until 25 August 2026 that place was whatever zone the hub's operating system
happened to be set to, which on this house was `Europe/London` while the house is in Italy:
every hour the parent chose was honoured an hour late, and nothing anywhere could tell.

So the zone is a household setting, chosen in the panel beside the hours it applies to, and
read here. Two things follow, and both are the point:

* **A wrong machine is no longer a wrong system.** Reinstalling the hub, or moving it to a
  house in another country, changes nothing the parent has to know about.
* **It can be tested.** A test can ask what the house thinks the hour is in Rome on the day
  the clocks go back, which is not a question you can ask `time.localtime`.

An empty zone means "whatever this machine says", which is what every house did before this
existed. That is a deliberate fallback and not a good one: it is here so that a house
upgrading does not stop, and the panel shows the parent what the house is actually using.
"""

from __future__ import annotations

import time
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Monday first, matching `shared/reminders`-side spelling. A fourth spelling of a weekday
# is a day nobody matches, so there is one list and this is it.
DAYS: tuple[str, ...] = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def known_zone(name: str) -> bool:
    """Whether this is a zone the machine can actually resolve.

    Asked by trying it rather than by searching a list: `available_timezones()` reads the
    whole database off disk, and the only question worth answering is whether *this* name
    works *here*.
    """
    if not name:
        return True
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError, OSError):
        return False
    return True


def wall_clock(now: float, zone: str = "") -> time.struct_time:
    """The broken-down local time in ``zone``, or this machine's if there is none.

    Returns the same type as :func:`time.localtime` so it drops into everything that
    already reads ``tm_hour``, ``tm_min`` and ``tm_wday``.

    A zone the machine cannot resolve falls back to the machine's own rather than raising.
    An afternoon must not fail to begin because a timezone database is out of date, and the
    parent is told which zone is in use rather than being left to infer it from behaviour.
    """
    if not zone:
        return time.localtime(now)
    try:
        return datetime.fromtimestamp(now, ZoneInfo(zone)).timetuple()
    except (ZoneInfoNotFoundError, ValueError, OSError):
        return time.localtime(now)


def minutes_past_midnight(now: float, zone: str = "") -> int:
    """How far into the day it is where the house is."""
    there = wall_clock(now, zone)
    return there.tm_hour * 60 + there.tm_min


def day_name(now: float, zone: str = "") -> str:
    """Which day of the week it is where the house is, as the rhythm spells it."""
    return DAYS[wall_clock(now, zone).tm_wday]


def date_there(now: float, zone: str = "") -> str:
    """The calendar date where the house is, as ``YYYY-MM-DD``.

    This is what the hub stamps to mean "already done today", so it has to turn over at
    midnight in the house and not at midnight somewhere else.
    """
    there = wall_clock(now, zone)
    return f"{there.tm_year:04d}-{there.tm_mon:02d}-{there.tm_mday:02d}"
