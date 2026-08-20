"""Ask the panel for a new picture and put it on the display.

Runs on the hub, on a timer that fires once a minute. The house decides when: the panel
paints only because it was asked, and has no way to reach this machine on its own.

The minute is for the decision, not for the network. The rhythm is read from the panel at
the moment a picture is asked for, and kept in a local file; every run in between decides
from that copy and touches nothing. The panel's API scales to zero, so a GET a minute
would hold a replica awake all day for an answer that changes once a week. What that costs
is freshness: a rhythm the parent changes is noticed at the next picture, so at most one
spacing late.

Two refusals are normal and are treated as such, leaving the current picture alone: the
content gate declining an image, and the cloud being unreachable. A display that keeps
yesterday's picture is a much better outcome than a blank one.

The parent can also ask for a picture they have already seen to go back up. That request
is collected here, at the moment a picture is due, and takes the place of the painting.
The panel records it and has no way to deliver it, so the wait is up to one spacing.

Stdlib only, so the hub needs no virtualenv for this.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from devices.trmnl_byos import validate_screen

# Nobody looks at a picture at four in the morning, and every refresh costs a generation.
# All three are the parent's to choose; these are the defaults used until the panel says
# otherwise, and when it cannot be reached at all.
QUIET_FROM = "22:00"
QUIET_UNTIL = "07:00"
DEFAULT_CADENCE_MINUTES = 60

# The timer fires once a minute. The tolerance is what keeps a spacing of thirteen minutes
# from becoming fourteen: without it the run that lands a second early skips its turn.
CADENCE_GRACE_SECONDS = 30

# The one thing the parent can ask for through the panel. Spelled the same as
# `panel/requests.py` says it; the hub ignores anything it does not recognise, so a kind
# added up there does not have to arrive here on the same day.
REQUEST_SHOW_AGAIN = "showAgain"

def minutes_of(value: str) -> int:
    """"HH:MM" as minutes past midnight. Raises ValueError on anything else."""
    hour, _, minute = value.strip().partition(":")
    hour_number, minute_number = int(hour), int(minute)
    if not (0 <= hour_number <= 23 and 0 <= minute_number <= 59):
        raise ValueError(f"not a time on the clock: {value}")
    return hour_number * 60 + minute_number


def in_quiet_window(now: time.struct_time, start: int, end: int) -> bool:
    minutes = now.tm_hour * 60 + now.tm_min
    if start == end:
        return False
    if start < end:
        return start <= minutes < end
    return minutes >= start or minutes < end


def read_rhythm(
    panel: str, household: str, key: str, fallback: tuple[int, int, int]
) -> tuple[int, int, int]:
    """The pause and the spacing the parent chose, in minutes, or the fallback if the
    panel is silent.

    An unreachable panel means the house keeps working to its last known shape, not that
    it stops.
    """
    request = urllib.request.Request(
        f"{panel}/api/device/{household}/rhythm", headers={"X-Device-Key": key}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            answer = json.loads(response.read())
        return (
            minutes_of(str(answer["quietFrom"])),
            minutes_of(str(answer["quietUntil"])),
            int(answer["cadenceMinutes"]),
        )
    except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"cannot read the rhythm ({exc}); using {fallback}")
        return fallback


def due(screen_file: Path, cadence_minutes: int, now: float) -> bool:
    """Whether enough time has passed since the picture last changed.

    The file's own timestamp is the record of that, so there is no second copy of the
    truth to keep in step.
    """
    try:
        last_change = screen_file.stat().st_mtime
    except OSError:
        return True  # nothing on the display yet
    return now - last_change >= cadence_minutes * 60 - CADENCE_GRACE_SECONDS


def load_rhythm(path: Path) -> tuple[int, int, int] | None:
    """The last rhythm the panel gave us, or None if there is no usable copy.

    None is not an error, it is the state of a hub that has never painted. It matters
    because the caller must then ask rather than assume: a default spacing held for one
    default period is how a fresh hub ignores the parent for an hour.
    """
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
        return (int(saved["quietFrom"]), int(saved["quietUntil"]), int(saved["cadence"]))
    except (OSError, ValueError, KeyError, TypeError):
        return None


def save_rhythm(path: Path, start: int, end: int, cadence: int) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps({"quietFrom": start, "quietUntil": end, "cadence": cadence}),
        encoding="utf-8",
    )
    temporary.replace(path)


def install(screen_file: Path, image: bytes) -> None:
    """Write the picture where the display server will find it, atomically."""
    temporary = screen_file.with_suffix(screen_file.suffix + ".tmp")
    temporary.write_bytes(image)
    validate_screen(temporary)  # never install something the panel cannot render
    temporary.replace(screen_file)


def picture_file(shared: Path, jobs_file: Path) -> Path:
    """Where the picture goes: the file of one of the displays that hold that job.

    Writing to the shared file was what made the defect of 19 August 2026 permanent. One
    press created `screen-<id>.bmp` for a display, that file took the display over for
    good, and the pictures — which only ever reached the shared file — never came back.
    Addressing the display that holds the job writes to the same file the press did, so a
    press costs one picture instead of the display.

    Several displays may hold the job. The one chosen is the one whose picture is oldest,
    ties broken at random, because that is the only rule under which every one of them
    actually changes: picking at random would leave a display that keeps losing the toss
    showing the same picture for a day. It costs one generation per display per spacing
    rather than one per spacing, which is what a parent asking for two picture frames is
    asking for.

    With no answer from the panel the shared file is still the target, which is what the
    house did before anybody could say which display was which.
    """
    import random

    from devices.inventory import holders, load_jobs
    from devices.trmnl_byos import picture_for

    chosen = [
        picture_for(shared, str(thing.get("label") or ""))
        for thing in holders(load_jobs(jobs_file), "picture")
        if thing.get("label")
    ]
    if not chosen:
        return shared
    random.shuffle(chosen)
    return min(chosen, key=_painted_at)


def _painted_at(screen_file: Path) -> float:
    """When this display last changed. Never painted sorts first."""
    try:
        return screen_file.stat().st_mtime
    except OSError:
        return 0.0


def standing_request(panel: str, household: str, key: str) -> dict[str, Any] | None:
    """What the parent has asked the house to do, or None.

    Asked for at the moment a picture is due and not before. The panel cannot reach this
    machine, so a press waits until the house next looks, which is up to one spacing —
    with the default that is an hour. Asking every minute instead would hold an API
    replica awake all day to hear "nothing" almost every time.

    Never raises. A panel that does not answer means the house paints as it always does.
    """
    request = urllib.request.Request(
        f"{panel}/api/device/{household}/request", headers={"X-Device-Key": key}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            asked = json.loads(response.read()).get("request")
    except (urllib.error.URLError, OSError, ValueError, AttributeError) as exc:
        print(f"cannot read what was asked for ({exc}); painting as usual")
        return None
    return asked if isinstance(asked, dict) else None


def archived_picture(panel: str, household: str, key: str, picture_id: str) -> bytes | None:
    """One picture out of the archive, ready for the display, or None if it is not there.

    None is a normal answer: an archive that has aged a picture out is a reason to drop
    the request, not a fault.
    """
    request = urllib.request.Request(
        f"{panel}/api/device/{household}/pictures/{picture_id}",
        headers={"X-Device-Key": key},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return base64.b64decode(json.loads(response.read())["imageBase64"])
    except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"cannot fetch the picture that was asked for ({exc})")
        return None


def request_done(panel: str, household: str, key: str, request_id: str) -> None:
    """Say the house has dealt with it, so it is not done twice. Never raises: a request
    that stays behind costs one repeat, and raising here would cost the picture."""
    request = urllib.request.Request(
        f"{panel}/api/device/{household}/request/{request_id}/done",
        data=b"",
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=30).close()
    except (urllib.error.URLError, OSError) as exc:
        print(f"could not clear the request ({exc}); it may be acted on again")


def serve_request(
    panel: str, household: str, key: str, target: Path, asked: dict[str, Any]
) -> bool:
    """Put back the picture the parent chose. True if the display now holds it.

    This takes the place of a painting rather than being added to it: the house was about
    to spend a model call on a new picture, and the parent has said which one they want
    instead. A request the house cannot honour is cleared anyway — leaving it would make
    every later run try the same missing picture and never paint.
    """
    if str(asked.get("kind") or "") != REQUEST_SHOW_AGAIN:
        return False
    request_id = str(asked.get("id") or "")
    image = archived_picture(panel, household, key, str(asked.get("subject") or ""))
    if image is None:
        request_done(panel, household, key, request_id)
        return False
    try:
        install(target, image)
    except ValueError as exc:
        print(f"refused a picture the display cannot render: {exc}")
        request_done(panel, household, key, request_id)
        return False
    request_done(panel, household, key, request_id)
    print(f"put back on {target.name}: {len(image)} bytes")
    return True


def main() -> int:
    panel = os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/")
    household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
    key = os.environ.get("LANTERNINA_DEVICE_KEY", "")
    screen_file = Path(os.environ.get("TRMNL_SCREEN_FILE", ""))
    if not (panel and household and key and str(screen_file)):
        print("missing panel URL, household, device key or screen file")
        return 1

    start = minutes_of(os.environ.get("LANTERNINA_QUIET_FROM", QUIET_FROM))
    end = minutes_of(os.environ.get("LANTERNINA_QUIET_UNTIL", QUIET_UNTIL))
    cadence = int(os.environ.get("LANTERNINA_CADENCE_MINUTES", DEFAULT_CADENCE_MINUTES))
    rhythm_file = Path(
        os.environ.get("LANTERNINA_RHYTHM_FILE", "") or screen_file.with_name("rhythm.json")
    )
    jobs_file = Path(
        os.environ.get("LANTERNINA_JOBS_FILE", "") or screen_file.with_name("jobs.json")
    )
    # Which display this is going to is decided here, once: the spacing is measured on the
    # file the picture will land in, so a display that has just been given the job is not
    # made to wait out the last one's hour.
    target = picture_file(screen_file, jobs_file)
    saved = load_rhythm(rhythm_file)
    if saved is None:
        start, end, cadence = read_rhythm(panel, household, key, (start, end, cadence))
        save_rhythm(rhythm_file, start, end, cadence)
    else:
        start, end, cadence = saved

    if in_quiet_window(time.localtime(), start, end):
        print(f"pause ({start // 60:02d}:{start % 60:02d}–{end // 60:02d}:{end % 60:02d}): "
              "leaving the picture alone")
        return 0

    if not due(target, cadence, time.time()):
        print(f"less than {cadence} minutes since the last picture: leaving it alone")
        return 0

    # Asking for a picture is the one moment the panel is worth waking, so it is also when
    # we find out whether the parent has changed the rhythm since.
    start, end, cadence = read_rhythm(panel, household, key, (start, end, cadence))
    save_rhythm(rhythm_file, start, end, cadence)
    if in_quiet_window(time.localtime(), start, end):
        print("the pause was moved and now covers this hour: leaving the picture alone")
        return 0
    if not due(target, cadence, time.time()):
        print(f"the spacing was widened to {cadence} minutes: leaving the picture alone")
        return 0

    # The parent may have asked for a picture they already have back. That is the answer to
    # this turn, and it costs no generation.
    asked = standing_request(panel, household, key)
    if asked is not None and serve_request(panel, household, key, target, asked):
        return 0

    request = urllib.request.Request(
        f"{panel}/api/device/{household}/paint",
        data=b"",
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            answer = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        # 409 is the content gate declining, 429 the household's monthly cap, 503 the cloud
        # being unavailable. All three mean the display keeps what it has, which is a good
        # outcome and not a failure.
        print(f"no new picture ({exc.code}): keeping the current one")
        return 0
    except (urllib.error.URLError, OSError) as exc:
        print(f"panel unreachable: {exc}. Keeping the current picture.")
        return 0

    image = base64.b64decode(answer["imageBase64"])
    try:
        install(target, image)
    except ValueError as exc:
        print(f"refused a picture the display cannot render: {exc}")
        return 1
    print(f"new picture on {target.name}: {answer.get('theme', '')} ({len(image)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
