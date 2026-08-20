"""Put a reminder on a display when its hour comes, and take it down when it passes.

Runs on the hub, on a timer that fires once a minute. This is the other half of the
feature whose panel side was built on 19 August 2026: the parent writes sentences, the
house asks what they mean, and this is what makes one of them appear in front of somebody.

The house owns the clock, and it has to. A write from the panel is inert, so the panel
cannot decide that a moment has come; all it can do is answer, when asked, with the
reminders that have an hour attached. Deciding that 13:30 is now is this module's job.

What it does not do is the part that had to be got right. It never records that a reminder
was seen, or dismissed, or ignored: the file it keeps says which reminder it last put on
which display, which is what a thing that draws needs in order not to draw twice, and it
holds nothing that could be read as a count of anybody's behaviour. A reminder nobody
presses is shown until its window closes and is then simply taken down. Nothing is sent
anywhere because a button was not pressed.

The words on the screen are the parent's own sentence, shown as written. Generating the
wording is a separate piece and is not built yet — see `ideas/05-routines.md` §1.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from devices.inventory import holders, load_jobs
from devices.pull_picture import minutes_of
from devices.trmnl_byos import reminder_for, validate_screen
from shared.capabilities import JOB_REMIND

# Monday first, to line up with `time.struct_time.tm_wday`. The same three letters as
# `panel/reminders.py`, which is the only other place they are spelled: the hub cannot
# import the panel, so `tests/test_show_reminders.py` compares the two.
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

# How long a reminder stays on the display after its hour. Long enough that somebody who
# walks past a few minutes later still sees it, short enough that it does not become the
# wallpaper — a reminder that is always there is not a reminder. It does not extend past
# midnight: a reminder at 23:50 is shown for ten minutes and then the day is over.
WINDOW_MINUTES = 30

# How stale the copy of the reminders may get before the panel is asked again. Five
# minutes is the spacing the status push already uses, so this adds no new order of
# magnitude to how often the cloud is woken. What it costs is that a sentence written just
# now becomes a reminder up to five minutes later, which is the trade already accepted for
# the rhythm.
CACHE_MAX_AGE_SECONDS = 300


def ask_panel(panel: str, household: str, key: str) -> list[dict[str, Any]] | None:
    """The reminders that have an hour, or None if the panel could not be reached.

    This is also the request inside which the panel reads any sentence nobody has read
    yet, so it is the only moment a new sentence can become a reminder at all.
    """
    request = urllib.request.Request(
        f"{panel}/api/device/{household}/reminders",
        data=b"",
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            answer = json.loads(response.read())
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"panel unreachable: {exc}")
        return None
    found = answer.get("reminders")
    if not isinstance(found, list):
        return None
    if answer.get("degraded"):
        print("the panel could not read every sentence; using what it did place")
    return [item for item in found if isinstance(item, dict)]


def load_cache(path: Path) -> tuple[list[dict[str, Any]], float]:
    """The last answer from the panel and when it arrived. Never read is (no rows, 0)."""
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
        rows = saved["reminders"]
        if not isinstance(rows, list):
            return [], 0.0
        return [row for row in rows if isinstance(row, dict)], float(saved["at"])
    except (OSError, ValueError, KeyError, TypeError):
        return [], 0.0


def save_cache(path: Path, reminders: list[dict[str, Any]], at: float) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps({"at": at, "reminders": reminders}), encoding="utf-8")
    temporary.replace(path)


def occurrence_of(reminder: dict[str, Any], now: time.struct_time) -> str:
    """What tells one showing of a reminder from the next one, tomorrow at the same hour.

    Not a record of anything: it is thrown away as soon as the window closes, and it names
    a reminder and a date, never a person and never an outcome.
    """
    return f"{reminder.get('id', '')}@{time.strftime('%Y-%m-%d', now)}@{reminder.get('at', '')}"


def due_now(reminders: list[dict[str, Any]], now: time.struct_time) -> dict[str, Any] | None:
    """The reminder whose moment is this minute, or None.

    The most recent one wins when two windows overlap: at 13:35, a reminder for 13:30 is
    more of the moment than one for 13:10 that is still inside its half hour.
    """
    today = DAYS[now.tm_wday]
    minutes = now.tm_hour * 60 + now.tm_min
    best: tuple[int, dict[str, Any]] | None = None
    for reminder in reminders:
        days = [str(day) for day in reminder.get("days") or ()]
        if days and today not in days:
            continue
        try:
            start = minutes_of(str(reminder.get("at") or ""))
        except ValueError:
            # An hour that is not an hour was already dropped by the panel; a second
            # reading of the same thing costs nothing and keeps this total.
            continue
        if 0 <= minutes - start < WINDOW_MINUTES and (best is None or start > best[0]):
            best = (start, reminder)
    return None if best is None else best[1]


def load_shown(path: Path) -> dict[str, str]:
    """Which showing each display is currently on, so nothing is drawn twice.

    The entry is cleared when the window closes, so this file holds only what is on a
    screen right now. It is deliberately unable to say whether anybody pressed anything:
    a reminder taken down by a press and one still standing look exactly the same here.
    """
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
        rows = saved["displays"]
        return {str(k): str(v) for k, v in rows.items()} if isinstance(rows, dict) else {}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return {}


def save_shown(path: Path, displays: dict[str, str]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps({"displays": displays}), encoding="utf-8")
    temporary.replace(path)


def draw(reminder: dict[str, Any]) -> bytes:
    """The hour, and the sentence the parent wrote, on one screen."""
    from devices.epaper import render_notice_bmp

    return render_notice_bmp(str(reminder.get("at", "")), [str(reminder.get("text", ""))])


def install(path: Path, image: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(image)
    validate_screen(temporary)  # never install something the display cannot render
    temporary.replace(path)


def displays_that_remind(jobs_file: Path) -> list[str]:
    """The friendly ids of the displays the parent gave the reminder job to.

    Empty means nothing happens at all, which is what makes this safe to install before
    anybody has handed the job out: no panel is called and no screen is touched.
    """
    return [
        str(thing.get("label"))
        for thing in holders(load_jobs(jobs_file), JOB_REMIND)
        if thing.get("label")
    ]


def main() -> int:
    panel = os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/")
    household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
    key = os.environ.get("LANTERNINA_DEVICE_KEY", "")
    screen_file = Path(os.environ.get("TRMNL_SCREEN_FILE", ""))
    if not (panel and household and key and str(screen_file)):
        print("missing panel URL, household, device key or screen file")
        return 1

    jobs_file = Path(
        os.environ.get("LANTERNINA_JOBS_FILE", "") or screen_file.with_name("jobs.json")
    )
    cache_file = Path(
        os.environ.get("LANTERNINA_REMINDERS_FILE", "")
        or screen_file.with_name("reminders.json")
    )
    shown_file = screen_file.with_name("reminders-shown.json")

    wanted = displays_that_remind(jobs_file)
    if not wanted:
        print("no display shows reminders: nothing to do")
        return 0

    reminders, fetched_at = load_cache(cache_file)
    now = time.time()
    if now - fetched_at >= CACHE_MAX_AGE_SECONDS:
        fresh = ask_panel(panel, household, key)
        if fresh is not None:
            reminders = fresh
            save_cache(cache_file, reminders, now)
        elif not reminders:
            # Never reached the panel and nothing kept: reduced capability, not a fault.
            print("no reminders to work from yet")
            return 0

    clock = time.localtime(now)
    due = due_now(reminders, clock)
    occurrence = "" if due is None else occurrence_of(due, clock)

    shown = load_shown(shown_file)
    for friendly_id in wanted:
        if shown.get(friendly_id, "") == occurrence:
            # Already dealt with. Either it is still on the screen, or somebody pressed
            # the button and it went away — and putting it back would make the press mean
            # nothing, which is the one thing a dismissal must not mean.
            continue
        target = reminder_for(screen_file, friendly_id)
        if due is None:
            target.unlink(missing_ok=True)
            print(f"{friendly_id}: the moment has passed")
        else:
            install(target, draw(due))
            print(f"{friendly_id}: {due.get('at', '')} {due.get('text', '')}")
        shown[friendly_id] = occurrence
    save_shown(shown_file, shown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
