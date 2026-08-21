"""When this house begins an afternoon, and when it asks for one to be written.

The runner in :mod:`devices.run_experience` plays an afternoon it is handed. Nothing
handed it one: ``begin`` took a file, so an afternoon happened because somebody typed a
path. This is the part that was missing, and it is the house's own clock rather than
anything the panel can reach.

The direction is the whole design, and it is the same one everything else here points in.
The house looks; the panel answers. There is no route the other way, so an approved
afternoon sits in the cloud until this machine decides it is time — and a parent who
approves one has not started anything.

**The rhythm, and what it is not.** The parent chooses which days an afternoon may begin
on and from what hour. The default is no day at all, so a house that has never been told
begins none: the feature arrives switched off. On a chosen day, at or after the hour, the
house looks once. That is one network call a chosen day, not one a minute.

Three limits, each of them about the house and none of them about a person:

* **One afternoon at a time.** Two sheets on the table from two afternoons is a house that
  has stopped making sense.
* **One look a day.** The stamp is a date, not a tally. Nothing counts how many afternoons
  happened, this week or ever, and there is no setting for how many there should be.
* **It has to fit.** An afternoon may begin only if its whole length is over before the
  house goes quiet. That is why nothing here has an end-hour setting: the pause the parent
  already chose is the end, and the afternoon's own ``minutes`` say whether it fits.

**What is asked for, and when.** If the look finds nothing approved and nothing waiting
with the parent, the house asks for one to be devised. It arrives pending, so it cannot
run today: the earliest it can happen is the next chosen day, after somebody has read it.
That lag is the approval, working.

Stdlib only for the network and the clock; the runner it calls is not.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from devices.house import CannotRun, House, screen_in
from devices.run_experience import begin, forget_what_is_over, waiting_runs
from shared.experience import Experience, ExperienceError

# Monday first, and these exact three letters: `panel/reminders.py` writes them and
# `devices/show_reminders.py` reads them, and a fourth spelling is a day nobody matches.
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

# What the house falls back on when it has never reached the panel: no day, so nothing
# happens. A default that began an afternoon would be this program deciding something the
# parent has not.
NO_DAYS: tuple[str, ...] = ()
DEFAULT_AFTERNOON_FROM = "15:00"
DEFAULT_QUIET_FROM = "22:00"
DEFAULT_QUIET_UNTIL = "07:00"

# How stale the copy of the rhythm may get. The panel's API scales to zero, so reading it
# every minute would hold a replica awake all day for an answer that changes once a month.
# What it costs is freshness: a parent who changes the days is honoured within this.
RHYTHM_MAX_AGE_SECONDS = 6 * 3600

LOOK_TIMEOUT_SECONDS = 30
# Devising a whole afternoon is a model writing a dozen moments. Measured from the hub on
# 21 August 2026: 29.1 s for the one that succeeded.
DEVISE_TIMEOUT_SECONDS = 180

MINUTES_IN_A_DAY = 24 * 60


def minutes_of(value: str) -> int:
    """"HH:MM" as minutes past midnight. Raises ValueError on anything else."""
    hour, _, minute = value.strip().partition(":")
    hours, minutes = int(hour), int(minute)
    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        raise ValueError(f"not a time on the clock: {value}")
    return hours * 60 + minutes


def in_quiet_window(minutes: int, start: int, end: int) -> bool:
    """Equal ends mean no pause at all, so a parent can turn the window off."""
    if start == end:
        return False
    if start < end:
        return start <= minutes < end
    return minutes >= start or minutes < end


def fits_before_the_pause(minutes_now: int, length: int, start: int, end: int) -> bool:
    """Whether a whole afternoon of ``length`` minutes is over before the house goes quiet.

    This is the reason there is no end-hour setting. An afternoon that would still be
    running at the hour the parent picked for quiet is one that ends on a display nobody
    is meant to be looking at, and the length is written on the afternoon itself.
    """
    if start == end:
        return True
    if in_quiet_window(minutes_now, start, end):
        return False
    return length <= (start - minutes_now) % MINUTES_IN_A_DAY


def _day(now: float) -> str:
    then = time.localtime(now)
    return f"{then.tm_year:04d}-{then.tm_mon:02d}-{then.tm_mday:02d}"


def looked_today(stamp: Path, now: float) -> bool:
    """Whether the house has already looked today.

    The file holds a date, deliberately, and not a count. What it stops is a second
    afternoon on the same day and a devise request every ten minutes at a panel that is
    answering 503; what it does not do is keep a tally of anything, because there is
    nothing here that a tally would be about.
    """
    try:
        return stamp.read_text(encoding="utf-8").strip() == _day(now)
    except OSError:
        return False


def mark_looked(stamp: Path, now: float) -> None:
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(_day(now) + "\n", encoding="utf-8")


def load_rhythm(path: Path, now: float) -> dict[str, Any] | None:
    """The last rhythm the panel gave us, or None if there is none or it is too old."""
    try:
        if now - path.stat().st_mtime > RHYTHM_MAX_AGE_SECONDS:
            return None
        saved: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return saved


def save_rhythm(path: Path, rhythm: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(rhythm), encoding="utf-8")
    temporary.replace(path)


def _get(url: str, key: str, timeout: int) -> Any:
    request = urllib.request.Request(url, headers={"X-Device-Key": key})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def _post(url: str, key: str, body: dict[str, Any], timeout: int) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def read_rhythm(panel: str, household: str, key: str) -> dict[str, Any]:
    """The days and the hours the parent chose. Raises on anything the house cannot use."""
    answer = _get(f"{panel}/api/device/{household}/rhythm", key, LOOK_TIMEOUT_SECONDS)
    return {
        "afternoonDays": [str(day) for day in (answer.get("afternoonDays") or [])],
        "afternoonFrom": str(answer.get("afternoonFrom") or DEFAULT_AFTERNOON_FROM),
        "quietFrom": str(answer.get("quietFrom") or DEFAULT_QUIET_FROM),
        "quietUntil": str(answer.get("quietUntil") or DEFAULT_QUIET_UNTIL),
    }


def the_rhythm(panel: str, household: str, key: str, cache: Path, now: float) -> dict[str, Any]:
    """The rhythm, from the copy on disk while it is fresh enough.

    An unreachable panel and an empty cache mean no day at all, which is a house that does
    nothing rather than a house that guesses.
    """
    saved = load_rhythm(cache, now)
    if saved is not None:
        return saved
    try:
        fresh = read_rhythm(panel, household, key)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"cannot read the rhythm ({exc}); no afternoon begins")
        return {
            "afternoonDays": list(NO_DAYS),
            "afternoonFrom": DEFAULT_AFTERNOON_FROM,
            "quietFrom": DEFAULT_QUIET_FROM,
            "quietUntil": DEFAULT_QUIET_UNTIL,
        }
    save_rhythm(cache, fresh)
    return fresh


def its_moment(rhythm: dict[str, Any], now: time.struct_time) -> bool:
    """Whether this is a day and an hour the parent said an afternoon may begin on."""
    if DAYS[now.tm_wday] not in rhythm["afternoonDays"]:
        return False
    return now.tm_hour * 60 + now.tm_min >= minutes_of(rhythm["afternoonFrom"])


def what_the_house_may_run(panel: str, household: str, key: str) -> tuple[list[Any], int]:
    """The approved afternoons and how many are still with the parent."""
    answer = _get(
        f"{panel}/api/device/{household}/experiences", key, LOOK_TIMEOUT_SECONDS
    )
    return list(answer.get("experiences") or []), int(answer.get("waiting") or 0)


def ask_for_one(panel: str, household: str, key: str, house: House) -> str:
    """Ask for an afternoon to be devised. It arrives pending and cannot run today."""
    answer = _post(
        f"{panel}/api/device/{household}/experiences",
        key,
        {"capabilities": sorted(str(c) for c in house.capabilities)},
        DEVISE_TIMEOUT_SECONDS,
    )
    return str(answer.get("title") or answer.get("id") or "")


def say_it_began(panel: str, household: str, key: str, offered_id: str) -> None:
    """Tell the panel this one has happened, so it is not offered again tomorrow.

    Failing here costs one repeated afternoon and nothing else, so it does not stop the
    one that has already started.
    """
    try:
        _post(
            f"{panel}/api/device/{household}/experiences/{offered_id}/begun",
            key,
            {},
            LOOK_TIMEOUT_SECONDS,
        )
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"the panel was not told it began ({exc})")


def choose(offered: list[Any], house: House) -> tuple[str, Experience] | None:
    """The oldest approved afternoon this house can actually run, or nothing.

    The panel sorts by when it was devised, so this is first-in-first-out: an afternoon
    that has been waiting is not passed over for a newer one.
    """
    for row in offered:
        try:
            experience = Experience.from_dict(row["experience"])
        except (ExperienceError, KeyError, TypeError) as exc:
            print(f"an offered afternoon could not be read ({exc}); skipping it")
            continue
        if experience.runnable_in(house.capabilities):
            return str(row.get("id") or experience.experience_id), experience
        print(f"this house cannot run {experience.title}; skipping it")
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Begin an afternoon, if it is time.")
    parser.add_argument(
        "--no-paper", action="store_true", help="lay the sheet out without sending it"
    )
    args = parser.parse_args(argv)

    panel = os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/")
    household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
    key = os.environ.get("LANTERNINA_DEVICE_KEY", "")
    sheets_dir = Path(os.environ.get("LANTERNINA_SHEETS_DIR", ""))
    if not (panel and household and key and str(sheets_dir) != "."):
        print("missing panel URL, household, device key or sheets directory")
        return 1

    house = House(
        printer=os.environ.get("LANTERNINA_PRINTER", ""),
        scanner=os.environ.get("LANTERNINA_SCANNER", ""),
        screen=screen_in(os.environ),
        sheets_dir=sheets_dir,
        panel=panel,
        household=household,
        device_key=key,
    )
    # Beside the runs rather than among them: `waiting_runs` reads every .json in
    # `afternoons/` as an afternoon, so a cache file in there would be one.
    cache = sheets_dir / "afternoon-rhythm.json"
    stamp = sheets_dir / "afternoon-looked.stamp"
    now = time.time()

    for run_id in forget_what_is_over(sheets_dir, now):
        print(f"{run_id} ran out of hours and is over")
    still_going = waiting_runs(sheets_dir)
    if still_going:
        print(f"an afternoon is already under way: {', '.join(still_going)}")
        return 0

    rhythm = the_rhythm(panel, household, key, cache, now)
    try:
        if not its_moment(rhythm, time.localtime(now)):
            return 0
    except ValueError as exc:
        print(f"the rhythm cannot be read as a clock ({exc}); no afternoon begins")
        return 0

    if looked_today(stamp, now):
        return 0

    try:
        offered, waiting = what_the_house_may_run(panel, household, key)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        # Not stamped: the house did not manage to look, so it may look again in a minute.
        print(f"the panel did not say what this house may run ({exc})")
        return 0
    # Stamped as soon as the look succeeded, and before anything else can fail. One look a
    # day is the rule, so a printer that is off costs the afternoon rather than costing a
    # sheet every ten minutes until somebody notices.
    mark_looked(stamp, now)

    chosen = choose(offered, house)
    if chosen is None:
        if waiting:
            print(f"{waiting} waiting for the parent; nothing to begin")
            return 0
        try:
            title = ask_for_one(panel, household, key, house)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            print(f"no afternoon was devised ({exc})")
            return 0
        print(f"asked for one, and it is waiting for the parent: {title}")
        return 0

    offered_id, experience = chosen
    minutes_now = time.localtime(now).tm_hour * 60 + time.localtime(now).tm_min
    if not fits_before_the_pause(
        minutes_now,
        experience.minutes,
        minutes_of(rhythm["quietFrom"]),
        minutes_of(rhythm["quietUntil"]),
    ):
        print(f"{experience.title} would not be over before the pause; not beginning it")
        return 0

    try:
        run_id = begin(house, experience, now=now, send=not args.no_paper)
    except (CannotRun, ExperienceError, OSError) as exc:
        print(f"{experience.title} did not begin ({exc})")
        return 1
    say_it_began(panel, household, key, offered_id)
    print(f"{experience.title}: {run_id or 'closed without asking for paper'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
