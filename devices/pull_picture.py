"""Ask the panel for a new picture and put it on the display.

Runs on the hub, on a timer. The house decides when: the panel paints only because it was
asked, and has no way to reach this machine on its own.

Two refusals are normal and are treated as such, leaving the current picture alone: the
content gate declining an image, and the cloud being unreachable. A display that keeps
yesterday's picture is a much better outcome than a blank one.

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


def install(screen_file: Path, image: bytes) -> None:
    """Write the picture where the display server will find it, atomically."""
    temporary = screen_file.with_suffix(screen_file.suffix + ".tmp")
    temporary.write_bytes(image)
    validate_screen(temporary)  # never install something the panel cannot render
    temporary.replace(screen_file)


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
    start, end, cadence = read_rhythm(panel, household, key, (start, end, cadence))

    if in_quiet_window(time.localtime(), start, end):
        print(f"pause ({start // 60:02d}:{start % 60:02d}–{end // 60:02d}:{end % 60:02d}): "
              "leaving the picture alone")
        return 0

    if not due(screen_file, cadence, time.time()):
        print(f"less than {cadence} minutes since the last picture: leaving it alone")
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
        install(screen_file, image)
    except ValueError as exc:
        print(f"refused a picture the display cannot render: {exc}")
        return 1
    print(f"new picture on the display: {answer.get('theme', '')} ({len(image)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
