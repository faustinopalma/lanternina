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
begins none: the feature arrives switched off. Every run reads that setting from the panel
and almost every run stops there; on a chosen day, at or after the hour, the house looks
once at what it may run.

Three limits, each of them about the house and none of them about a person:

* **One afternoon at a time.** Two sheets on the table from two afternoons is a house that
  has stopped making sense.
* **As many in a day as the parent chose, and two unless they said otherwise.** The house
  keeps a date and a number beside its runs, and the date is what makes it a rhythm rather
  than a tally: a file from yesterday reads as zero. It is added to when an afternoon
  begins and read by nothing else. A run that finds nothing to do counts nothing, so a
  decision taken at four o'clock is honoured at ten past rather than tomorrow.
* **It has to fit.** An afternoon may begin only if its whole length is over before the
  house goes quiet. That is why nothing here has an end-hour setting: the pause the parent
  already chose is the end, and the afternoon's own ``minutes`` say whether it fits.

**The timer is also what ends an afternoon.** Every run calls
:func:`devices.run_experience.conclude_what_is_over` before it does anything else, and
that is what makes "the ending always arrives" true rather than likely: thirty minutes
before an afternoon's end hour, the way out of wherever it got to goes on the display, and
the ending follows it. Until 23 August 2026 the same call deleted the run in silence, which
is the failure the whole project exists to prevent — measured on this house at 14:02 on 21
August, on `aft_5ec79e85`.

**And it is how the parent reaches an afternoon that is already running.** Before deciding
whether an ending is due, the house asks the panel whether anything was said — an end hour
that moved, or an ending brought forward. Still no route the other way: the panel holds a
row and this machine comes for it, so what a parent writes takes effect within one turn of
this timer and not at the moment they press.

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

from devices.house import CannotRun, House, printer_in, scanner_in, screen_in
from devices.run_experience import (
    begin,
    conclude_what_is_over,
    hear,
    offer_help,
    waiting_runs,
)
from shared.clock import date_there, wall_clock
from shared.experience import Experience, ExperienceError
from shared.ids import new_id
from shared.message import Message, MessageError

# Monday first, and these exact three letters: `panel/reminders.py` writes them and
# `devices/show_reminders.py` reads them, and a fourth spelling is a day nobody matches.
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

# What the house falls back on when it cannot reach the panel: no day, so nothing happens.
# That is not a degradation to be avoided — an afternoon is pulled from the panel, so a
# panel that will not answer means there is nothing to begin whatever the rhythm says.
NO_DAYS: tuple[str, ...] = ()
DEFAULT_AFTERNOON_FROM = "15:00"
DEFAULT_AFTERNOON_UNTIL = "19:00"

# What the house falls back on when the panel does not say how many a day. It matches the
# panel's own default: a hub reading an API too old to carry the field behaves like a house
# whose parent has not touched the setting, rather than like one with no ceiling at all.
DEFAULT_AFTERNOONS_A_DAY = 2

LOOK_TIMEOUT_SECONDS = 30
# Devising a whole afternoon is a model writing a dozen moments. Measured from the hub on
# 21 August 2026: 29.1 s for the one that succeeded.
DEVISE_TIMEOUT_SECONDS = 180

# How many scripts the parent should have waiting to decide about. The panel is where it is
# chosen; this is what the house falls back on when the panel does not say. Ten is enough
# for a sitting: somebody opens the panel, reads a few, approves what they like and closes
# it knowing the house is not about to run dry.
WANTED = 10

MINUTES_IN_A_DAY = 24 * 60


def minutes_of(value: str) -> int:
    """"HH:MM" as minutes past midnight. Raises ValueError on anything else."""
    hour, _, minute = value.strip().partition(":")
    hours, minutes = int(hour), int(minute)
    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        raise ValueError(f"not a time on the clock: {value}")
    return hours * 60 + minutes


def fits_inside_the_band(
    minutes_now: int, length: int, start: int, end: int, *, the_hour_decides: bool = True
) -> bool:
    """Whether a whole afternoon of ``length`` minutes is over before the band closes.

    The length is written on the afternoon itself. An afternoon that would still be running
    after the hour the parent chose is one that ends on a display nobody is meant to be
    looking at, so it is not begun — a shorter one may still fit, which is why `choose` asks
    this about each of them rather than about the first.

    ``the_hour_decides`` is false when the parent pressed the button. A press overrides the
    start and never the end, which is what the button itself promises: it steps over the day
    and the hour, not the evening. Before this was a parameter a press at nine in the morning
    was refused by the same band it had just been allowed to ignore, and the refusal said the
    afternoon would not be over by half past seven, with ten hours to go.
    """
    if the_hour_decides and minutes_now < start:
        return False
    if minutes_now >= end:
        return False
    return length <= end - minutes_now


def the_day_stamp(sheets_dir: Path) -> Path:
    """Beside the runs and not among them: `waiting_runs` globs the directory next door."""
    return sheets_dir / "afternoons-today.json"


def begun_today(stamp: Path, now: float, zone: str = "") -> int:
    """How many afternoons have begun since midnight where the house is.

    A date and a number, deliberately, and the date is what makes it a rhythm rather than a
    tally: a file left from yesterday reads as zero rather than as history, and nothing here
    accumulates across days. It bounds the house's day; it is not a record of anybody, it
    reaches no display, no sheet and no page, and the only thing that reads it is the
    decision below about whether one more may begin.

    The date turns over at midnight where the house is, which is why the zone is a
    parameter: on a hub set to the wrong country the day rolled at the wrong hour.

    Unreadable reads as zero. The failure worth protecting against is a house that refuses
    to begin an afternoon for a reason nobody can see, not a house that begins one extra.
    """
    try:
        kept = json.loads(stamp.read_text(encoding="utf-8"))
        if not isinstance(kept, dict) or kept.get("date") != date_there(now, zone):
            return 0
        return max(0, int(kept.get("begun") or 0))
    except (OSError, ValueError, TypeError):
        return 0


def note_one_began(stamp: Path, now: float, zone: str = "") -> None:
    """Add one to today's count, starting again from zero when the date has moved."""
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(
        json.dumps(
            {"date": date_there(now, zone), "begun": begun_today(stamp, now, zone) + 1}
        ),
        encoding="utf-8",
    )


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
    a_day = answer.get("afternoonsADay")
    return {
        "afternoonDays": [str(day) for day in (answer.get("afternoonDays") or [])],
        "afternoonFrom": str(answer.get("afternoonFrom") or DEFAULT_AFTERNOON_FROM),
        "afternoonUntil": str(answer.get("afternoonUntil") or DEFAULT_AFTERNOON_UNTIL),
        # Not `or`: a parent who chose none means none, and that is not the same as absent.
        "afternoonsADay": DEFAULT_AFTERNOONS_A_DAY if a_day is None else int(a_day),
        "timeZone": str(answer.get("timeZone") or ""),
    }


def the_rhythm(panel: str, household: str, key: str) -> dict[str, Any]:
    """The rhythm, read fresh on every run, or no day at all.

    There was a copy on disk here until 21 August 2026, kept for six hours so that the
    panel's API could scale to zero between afternoons. It was wrong twice over. A parent
    who turned afternoons on watched nothing happen and had nothing to tell them why —
    measured that same evening, the days were saved at 15:21 and the house was still
    deciding on a rhythm read at 14:02. And it bought nothing: the afternoon itself is
    pulled from the panel, so a house that cannot reach it has nothing to begin however
    fresh its idea of the days.

    What it costs is one small request per run of the timer, so 144 a day rather than 4.
    """
    try:
        return read_rhythm(panel, household, key)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"cannot read the rhythm ({exc}); no afternoon begins")
        return {
            "afternoonDays": list(NO_DAYS),
            "afternoonFrom": DEFAULT_AFTERNOON_FROM,
            "afternoonUntil": DEFAULT_AFTERNOON_UNTIL,
            "afternoonsADay": DEFAULT_AFTERNOONS_A_DAY,
            "timeZone": "",
        }


def its_moment(rhythm: dict[str, Any], now: time.struct_time) -> bool:
    """Whether this is a day and an hour the parent said an afternoon may begin on."""
    if DAYS[now.tm_wday] not in rhythm["afternoonDays"]:
        return False
    minutes = now.tm_hour * 60 + now.tm_min
    return (
        minutes_of(rhythm["afternoonFrom"])
        <= minutes
        < minutes_of(rhythm["afternoonUntil"])
    )


# What the parent asked for, if it is the kind this runner acts on. Named here rather than
# imported from `panel` because the hub does not import the panel: the word is the wire.
BEGIN_NOW = "beginNow"


def the_standing_request(panel: str, household: str, key: str) -> str:
    """The id of a waiting "begin one now", or empty.

    A press is the only thing that can start an afternoon outside the hours the parent
    chose, and it still does not reach into the house: the panel wrote a row and this is
    the house coming to look. A panel that cannot be reached means no press, which is the
    same as no press at all — the afternoon simply waits for its hour.
    """
    try:
        answer = _get(f"{panel}/api/device/{household}/request", key, LOOK_TIMEOUT_SECONDS)
    except (urllib.error.URLError, OSError, ValueError):
        return ""
    standing = answer.get("request")
    if not isinstance(standing, dict) or standing.get("kind") != BEGIN_NOW:
        return ""
    return str(standing.get("id") or "")


def _tail(request_id: str) -> str:
    """Enough of an id to match two log lines. Not a clock, though it has read like one."""
    return request_id[-6:]


def the_request_is_done(panel: str, household: str, key: str, request_id: str) -> None:
    """Clear it by id, so a second press that landed meanwhile survives.

    Swallowed on failure: the afternoon has begun either way, and a request left standing
    costs one extra afternoon rather than a broken one. It expires on its own after a day.
    """
    try:
        _post(
            f"{panel}/api/device/{household}/request/{request_id}/done",
            key,
            {},
            LOOK_TIMEOUT_SECONDS,
        )
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"the request was acted on but not cleared ({exc})")


def what_the_house_may_run(
    panel: str, household: str, key: str
) -> tuple[list[Any], int, int]:
    """The approved afternoons, how many are with the parent, and how many they want.

    The third is the panel's setting rather than the hub's constant: how full the list a
    parent decides from should be is a decision about them, and it is made where they are.
    A panel that does not send it leaves the house on its own default.
    """
    answer = _get(
        f"{panel}/api/device/{household}/experiences", key, LOOK_TIMEOUT_SECONDS
    )
    return (
        list(answer.get("experiences") or []),
        int(answer.get("waiting") or 0),
        int(answer.get("wanted") or WANTED),
    )


def ask_for_one(panel: str, household: str, key: str, house: House) -> str:
    """Ask for an afternoon to be devised. It arrives pending and cannot run today."""
    answer = _post(
        f"{panel}/api/device/{household}/experiences",
        key,
        {"capabilities": sorted(str(c) for c in house.capabilities)},
        DEVISE_TIMEOUT_SECONDS,
    )
    return str(answer.get("title") or answer.get("id") or "")


def say_it_began(
    panel: str, household: str, key: str, offered_id: str, run_id: str = ""
) -> None:
    """Tell the panel this one has happened, so it is not offered again tomorrow.

    The run id goes with it so the panel can open the trail under the same name the house
    files its acts under. Failing here costs one repeated afternoon and nothing else, so it
    does not stop the one that has already started.
    """
    try:
        _post(
            f"{panel}/api/device/{household}/experiences/{offered_id}/begun",
            key,
            {"runId": run_id},
            LOOK_TIMEOUT_SECONDS,
        )
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"the panel was not told it began ({exc})")


def listen(house: House, now: float) -> list[str]:
    """Ask the panel what the parent said, apply it, and say each one was heard.

    `ideas/09 §23`. This is the whole channel from the panel into a running afternoon, and
    it points the same way everything else here does: the panel holds a row, the house
    comes for it. A parent moving the end hour reaches the room because this call happened,
    not because anything was sent.

    **Before the ending is decided, and that is the only ordering that matters.** The next
    thing this timer does is ask whether an afternoon's hour has come; an hour that moved
    after that question would wait ten minutes to be honoured, and "close now" that takes
    ten minutes is not what the words say.

    **Said to have been heard once it is applied**, one at a time and by id, so a message
    the parent wrote in the meantime is still waiting afterwards. A message that cannot be
    read is left alone rather than cleared: it means the two sides disagree about what may
    be said, which is ours to fix, and it stops being offered within the hour anyway.

    Never raises. A panel that will not answer means an afternoon that goes on exactly as
    it was going.
    """
    try:
        answer = _get(
            f"{house.panel}/api/device/{house.household}/messages",
            house.device_key,
            LOOK_TIMEOUT_SECONDS,
        )
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"the panel did not say whether anything was said ({exc})")
        return []

    heard: list[tuple[str, Message]] = []
    for row in answer.get("messages") or []:
        if not isinstance(row, dict):
            continue
        said = dict(row)
        message_id = str(said.pop("id", ""))
        try:
            heard.append((message_id, Message.from_dict(said)))
        except MessageError as exc:
            print(f"the panel said something this house cannot read ({exc})")
    if not heard:
        return []

    changed = hear(house, [message for _, message in heard], now)
    for message_id, _ in heard:
        try:
            _post(
                f"{house.panel}/api/device/{house.household}/messages/{message_id}/heard",
                house.device_key,
                {},
                LOOK_TIMEOUT_SECONDS,
            )
        except (urllib.error.URLError, OSError, ValueError) as exc:
            # It was applied; being told again in ten minutes applies the same end hour.
            print(f"the panel was not told it was heard ({exc})")
    return changed


def choose(
    offered: list[Any],
    house: House,
    *,
    minutes_now: int,
    band_from: int,
    band_until: int,
    the_hour_decides: bool = True,
) -> tuple[str, Experience] | None:
    """The oldest approved afternoon this house can run and still finish in time, or nothing.

    The panel sorts by when it was devised, so this is first-in-first-out: an afternoon
    that has been waiting is not passed over for a newer one.

    The clock is asked about each of them rather than about whichever came first. A house
    holding a two-hour afternoon and a one-hour one at six o'clock can run the second, and
    for a while it ran neither: the first was picked, found not to fit, and that was the end
    of the run.
    """
    for row in offered:
        try:
            experience = Experience.from_dict(row["experience"])
        except (ExperienceError, KeyError, TypeError) as exc:
            print(f"an offered afternoon could not be read ({exc}); skipping it")
            continue
        if not experience.runnable_in(house.capabilities):
            print(f"this house cannot run {experience.title}; skipping it")
            continue
        if not fits_inside_the_band(
            minutes_now,
            experience.minutes,
            band_from,
            band_until,
            the_hour_decides=the_hour_decides,
        ):
            print(
                f"{experience.title} takes {experience.minutes} minutes and there are "
                f"{max(0, band_until - minutes_now)} left; skipping it"
            )
            continue
        return str(row.get("id") or experience.experience_id), experience
    return None


def top_up(
    panel: str,
    household: str,
    key: str,
    house: House,
    *,
    waiting: int,
    wanted: int,
) -> None:
    """Ask for one more script when the parent has fewer than they want. Never raises.

    One per run of the timer, and the timer is every minute, so a parent who approves four
    has four more within the quarter hour. Not the whole shortfall at once: devising is a
    model writing a script and a dozen moments, and four of those in one second is a bill
    nobody agreed to and four afternoons drawn without seeing each other.

    It counts what is *waiting to be decided*, not what is approved. Those are different
    questions — how much the house has to run, and how much the parent has to read — and
    `panel/experiences.Backlog` answers the first.
    """
    if wanted <= 0 or waiting >= wanted:
        return
    try:
        title = ask_for_one(panel, household, key, house)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"no script was written ({exc})")
        return
    print(f"{waiting} waiting for the parent, wanted {wanted}; wrote one more: {title}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Begin an afternoon, if it is time.")
    parser.add_argument(
        "--no-paper", action="store_true", help="lay the sheet out without sending it"
    )
    parser.add_argument(
        "--only-help",
        action="store_true",
        help="put the next rung of help on the display, and nothing else",
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
        printer=printer_in(os.environ),
        scanner=scanner_in(os.environ),
        screen=screen_in(os.environ),
        sheets_dir=sheets_dir,
        panel=panel,
        household=household,
        device_key=key,
    )
    now = time.time()

    # Help has one owner, and it is `--only-help` on its own unit. It was offered here too
    # until 25 August 2026, which was harmless while this ran every ten minutes and the
    # help unit every one; when this went to a minute the two collided and offered the same
    # rung twice in the same second, racing to write the same run file — measured at
    # 13:38:04 on `aft_78a067a8`. It stays on the separate unit rather than moving here,
    # because it touches no network: a rung is in the run file and goes to a display, so it
    # keeps arriving on a run that cannot reach the panel at all.
    if args.only_help:
        for given in offer_help(house, now, send=not args.no_paper):
            print(f"help: {given}")
        return 0

    # Before the ending is decided, not after: an end hour that moved would otherwise wait
    # ten minutes to be honoured, and "close now" that takes ten minutes is not that.
    for moved in listen(house, now):
        print(moved)

    for run_id in conclude_what_is_over(house, now, send=not args.no_paper):
        print(f"{run_id} reached its ending and is over")

    # Above the hour and above whether a room is busy, and both for the same reason:
    # writing a script puts nothing in the room. It fills the list the parent decides from,
    # and a parent may open the panel at eight in the morning or while an afternoon is
    # running. Both were found the hard way, on 26 August 2026 — first the queue wrote
    # nothing outside 12:00–19:30, then it stopped at four of five because an afternoon was
    # under way and the runner returned before it ever got here.
    try:
        offered, waiting, wanted = what_the_house_may_run(panel, household, key)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"the panel did not say what this house may run ({exc})")
        return 0
    top_up(panel, household, key, house, waiting=waiting, wanted=wanted)

    still_going = waiting_runs(sheets_dir)
    if still_going:
        print(f"an afternoon is already under way: {', '.join(still_going)}")
        return 0

    rhythm = the_rhythm(panel, household, key)
    zone = str(rhythm.get("timeZone") or "")
    there = wall_clock(now, zone)

    asked = the_standing_request(panel, household, key)
    if asked:
        print(
            f"the parent asked for one (request {_tail(asked)}); "
            "the day and the hour do not decide"
        )

    # A press steps over the day and the hour; it does not step over this. The ceiling is
    # the parent's own number and raising it is one field away, so honouring a press against
    # it would leave the setting meaning nothing.
    stamp = the_day_stamp(sheets_dir)
    ceiling = int(rhythm["afternoonsADay"])
    already = begun_today(stamp, now, zone)
    if already >= ceiling:
        print(
            f"{already} began today and the parent chose at most {ceiling} a day; "
            "none begins"
        )
        if asked:
            # Cleared rather than left standing. A press that outlives the day would be
            # found again after midnight, when the count is zero and the hour it overrides
            # is the middle of the night.
            the_request_is_done(panel, household, key, asked)
        return 0

    try:
        if not asked and not its_moment(rhythm, there):
            # Said out loud, because it was not. Two silent returns meant a house that did
            # nothing for a reason nobody could recover: on 25 August 2026 the answer was
            # that the hub's own clock was an hour behind the house it stood in.
            print(
                f"not the moment: {time.strftime('%a %H:%M', there)}"
                f"{f' in {zone}' if zone else ' by this machine'}"
                f", and the parent chose {', '.join(rhythm['afternoonDays']) or 'no day'}"
                f" from {rhythm['afternoonFrom']} to {rhythm['afternoonUntil']}"
            )
            return 0
    except ValueError as exc:
        print(f"the rhythm cannot be read as a clock ({exc}); no afternoon begins")
        return 0

    minutes_now = there.tm_hour * 60 + there.tm_min
    chosen = choose(
        offered,
        house,
        minutes_now=minutes_now,
        band_from=minutes_of(rhythm["afternoonFrom"]),
        band_until=minutes_of(rhythm["afternoonUntil"]),
        the_hour_decides=not asked,
    )
    if chosen is None:
        print(
            f"nothing approved that fits before {rhythm['afternoonUntil']}; "
            f"{waiting} waiting for the parent"
        )
        return 0

    offered_id, experience = chosen
    # Named here rather than inside `begin`, so the panel can be told which run to keep the
    # record under before the first moment has finished playing.
    run_name = new_id("aft")
    try:
        run_id = begin(house, experience, run_id=run_name, now=now, send=not args.no_paper)
    except (CannotRun, ExperienceError, OSError) as exc:
        print(f"{experience.title} did not begin ({exc})")
        return 1
    # Counted before the panel is told, because the afternoon is already in the room: a
    # network failure here must not make it invisible to tomorrow's ceiling.
    note_one_began(stamp, now, zone)
    say_it_began(panel, household, key, offered_id, run_name)
    if asked:
        the_request_is_done(panel, household, key, asked)
    print(f"{experience.title}: {run_id or 'closed without asking for paper'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
