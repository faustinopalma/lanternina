"""The house decides in its own timezone, not in the machine's.

Found on the hub on 25 August 2026: the CM5 was set to `Europe/London` while the house is
in Italy. Every hour the parent chose was honoured an hour late — an afternoon set for
15:00 could not begin until 16:00 by the clock on the wall — and nothing anywhere said so.
The service ran every ten minutes, decided "not the moment", and exited silently.

These are written around one instant, `WHEN`, so the failure is visible as two different
answers to the same question. They fail on the version that reads `time.localtime`,
whatever zone the machine running the tests happens to be in, which is the property that
matters: a test that only passes on a European laptop would have missed this.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from devices.afternoon import its_moment, looked_today, mark_looked
from shared.clock import date_there, day_name, minutes_past_midnight, wall_clock

# 15:30 in Rome, which is 14:30 in London and 09:30 in New York. A Tuesday.
WHEN = datetime(2026, 8, 25, 15, 30, tzinfo=ZoneInfo("Europe/Rome")).timestamp()

ROME = "Europe/Rome"
LONDON = "Europe/London"
NEW_YORK = "America/New_York"


def a_rhythm(**changed: object) -> dict[str, object]:
    rhythm: dict[str, object] = {
        "afternoonDays": ["tue"],
        "afternoonFrom": "15:00",
        "quietFrom": "22:00",
        "quietUntil": "07:00",
        "timeZone": ROME,
    }
    rhythm.update(changed)
    return rhythm


def test_the_same_instant_is_a_different_hour_in_two_houses() -> None:
    assert minutes_past_midnight(WHEN, ROME) == 15 * 60 + 30
    assert minutes_past_midnight(WHEN, LONDON) == 14 * 60 + 30
    assert minutes_past_midnight(WHEN, NEW_YORK) == 9 * 60 + 30


def test_an_afternoon_set_for_three_begins_at_three_where_the_house_is() -> None:
    """The defect, stated as the two answers it gave.

    In Rome it is half past three and the afternoon may begin. On the machine as it was
    configured it was half past two, and it could not.
    """
    assert its_moment(a_rhythm(), wall_clock(WHEN, ROME)) is True
    assert its_moment(a_rhythm(), wall_clock(WHEN, LONDON)) is False


def test_a_house_far_enough_west_is_not_even_on_the_same_day() -> None:
    """Not a curiosity: the stamp that means "already done today" is a date.

    A hub whose zone is wrong enough rolls its day at the wrong moment, so the one thing
    the house does each day can be done twice or not at all around midnight.
    """
    midnight_in_rome = datetime(2026, 8, 26, 0, 30, tzinfo=ZoneInfo(ROME)).timestamp()

    assert date_there(midnight_in_rome, ROME) == "2026-08-26"
    assert date_there(midnight_in_rome, NEW_YORK) == "2026-08-25"
    assert day_name(midnight_in_rome, ROME) == "wed"
    assert day_name(midnight_in_rome, NEW_YORK) == "tue"


def test_the_stamp_turns_over_at_midnight_where_the_house_is(tmp_path: object) -> None:
    from pathlib import Path

    stamp = Path(str(tmp_path)) / "looked"
    mark_looked(stamp, WHEN, ROME)

    assert looked_today(stamp, WHEN, ROME) is True
    # Twenty-three hours later is the next day in Rome, so the house may look again.
    assert looked_today(stamp, WHEN + 23 * 3600, ROME) is False


def test_a_zone_the_machine_cannot_resolve_falls_back_rather_than_raising() -> None:
    """An afternoon must not fail to begin because a timezone database is out of date."""
    import time

    assert wall_clock(WHEN, "Mars/Olympus_Mons") == time.localtime(WHEN)
    assert wall_clock(WHEN, "") == time.localtime(WHEN)
