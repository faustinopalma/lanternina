"""Tell the panel what is in this house, and be told what each thing is for.

Runs on the hub, on a timer. It reads what each display reported on its last poll, looks
over mDNS for the printers and the scanners, and posts a snapshot upward. State, not
history: the panel keeps one row per thing, so nothing here accumulates a record of when
the house is awake.

The answer carries the jobs back down, which is why the discovery happens here rather than
on a timer of its own — this call was already being made every five minutes. The answer is
cached, so a panel that cannot be reached leaves the house working to the last known
assignment.

Nothing found is nothing removed. An empty mDNS answer means "found nothing this time",
and the panel is never told to forget anything: leaving the list is a decision the parent
takes.

Stdlib only, because the hub has no virtualenv for this and should not need one.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from devices.inventory import (
    discover,
    learner_name,
    load_jobs,
    refused_ids,
    save_jobs,
    screen_names,
)
from devices.trmnl_byos import LEVEL_OK, identify_for, last_state, load_devices, recorded_level

# `panel/requests.py` says them. Anything else here is somebody else's request, and this
# side leaves it standing rather than clearing something it did not act on.
REQUEST_IDENTIFY = "identify"
REQUEST_LOOK_NOW = "lookNow"

MAINS = "mains"


def snapshot(registry: Path, status_file: Path) -> list[dict[str, object]]:
    devices = load_devices(registry) if registry.exists() else {}
    reported: list[dict[str, object]] = []
    for device in devices.values():
        voltage, on_usb = last_state(status_file, device.mac)
        level = (
            MAINS
            if device.mains or on_usb
            else recorded_level(status_file, device.mac, device.mains)
        )
        entry = _entry(status_file, device.mac)
        reported.append(
            {
                "id": device.mac,
                "kind": "display",
                "name": device.friendly_id or device.mac,
                "lastSeen": float(entry.get("lastSeen") or 0.0),
                "level": level or LEVEL_OK,
                "voltage": voltage,
                "rssi": entry.get("rssi"),
                "firmware": str(entry.get("firmware") or ""),
                "model": str(entry.get("model") or ""),
            }
        )
    return reported


def _entry(status_file: Path, mac: str) -> dict[str, object]:
    if not status_file.exists():
        return {}
    try:
        document = json.loads(status_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    entry = document.get("devices", {}).get(mac)
    return entry if isinstance(entry, dict) else {}


def label_of(things: object, thing_id: str) -> str:
    """What the display calls itself, which is what its screen files are named after."""
    for thing in things if isinstance(things, list) else ():
        if isinstance(thing, dict) and thing.get("id") == thing_id:
            return str(thing.get("label") or "")
    return ""


def say_which_one(panel: str, household: str, key: str, shared: Path, things: object) -> None:
    """Act on what the parent asked the house to do about its devices, and clear it.

    Two kinds reach here. One puts an id card up on a display. The other asks the house to
    look at the network now, which is what this run has already done by the time it gets
    here — so acting on it is nothing but saying so and taking the row away.

    Never raises. A panel that cannot be reached, or a request about something this house
    does not have a screen for, leaves everything exactly as it was.
    """
    try:
        asked_for = urllib.request.Request(
            f"{panel}/api/device/{household}/request", headers={"X-Device-Key": key}
        )
        with urllib.request.urlopen(asked_for, timeout=30) as answer:
            asked = json.loads(answer.read()).get("request")
    except (urllib.error.URLError, OSError, ValueError, AttributeError) as exc:
        print(f"cannot read what was asked for ({exc})")
        return
    if not isinstance(asked, dict):
        return
    kind = asked.get("kind")
    if kind == REQUEST_LOOK_NOW:
        print("asked to look at the network: this run has just done it")
    elif kind == REQUEST_IDENTIFY:
        label = label_of(things, str(asked.get("subject") or ""))
        if not label:
            print(f"asked to identify {asked.get('subject')!r}, which is not a display here")
            return
        try:
            identify_for(shared, label).write_text("", encoding="utf-8")
        except OSError as exc:
            print(f"could not put the id card up on {label}: {exc}")
            return
        print(f"{label} will say which one it is until somebody presses its button")
    else:
        return
    done = urllib.request.Request(
        f"{panel}/api/device/{household}/request/{asked.get('id')}/done",
        headers={"X-Device-Key": key},
        method="POST",
    )
    try:
        urllib.request.urlopen(done, timeout=30).close()
    except (urllib.error.URLError, OSError) as exc:
        # What was asked for has happened. A request left standing only means it is acted
        # on again next time, which for both of these kinds costs nothing.
        print(f"could not clear the request ({exc})")


def main() -> int:
    panel = os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/")
    household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
    key = os.environ.get("LANTERNINA_DEVICE_KEY", "")
    if not (panel and household and key):
        print("missing LANTERNINA_PANEL_URL, LANTERNINA_HOUSEHOLD or LANTERNINA_DEVICE_KEY")
        return 1

    registry = Path(os.environ.get("TRMNL_DEVICE_REGISTRY", "/etc/lanternina/trmnl-devices.json"))
    status_file = Path(
        os.environ.get("TRMNL_STATUS_FILE", "/var/lib/lanternina/state/trmnl-status.json")
    )
    jobs_file = Path(
        os.environ.get("LANTERNINA_JOBS_FILE", "/var/lib/lanternina/state/jobs.json")
    )
    reported = snapshot(registry, status_file)
    seen_at = time.time()
    found = discover()
    reported.extend(thing.reported(seen_at) for thing in found)
    # Carried up so the panel can say which name was refused and why. The refusal happened
    # here, on the only side that knows who lives in the house.
    already_refused = refused_ids(load_jobs(jobs_file))
    for entry in reported:
        entry["nameRefused"] = entry["id"] in already_refused
    print(f"{len(reported)} thing(s) to report, {len(found)} found on the network")
    if not reported:
        return 0

    request = urllib.request.Request(
        f"{panel}/api/device/{household}/devices",
        data=json.dumps(reported).encode(),
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            answer = json.loads(response.read())
    except (urllib.error.URLError, OSError) as exc:
        # The panel being unreachable is not a fault of this house: the cached jobs stay
        # exactly as they were, and everything keeps running to them.
        print(f"panel unreachable: {exc}")
        return 1

    things = answer.get("things")
    if isinstance(things, list):
        # A name a parent typed reaches a model as material. This is the only side that
        # knows who lives here, so it is the only side that can refuse "Sofia's printer",
        # and it refuses before the name is written anywhere the house reads from.
        kept, refused = screen_names(things, learner_name())
        save_jobs(jobs_file, kept)
        for thing_id in refused:
            print(f"refused the name on {thing_id}: it carries a person's name")
    shared = Path(os.environ.get("TRMNL_SCREEN_FILE", ""))
    if shared.name:
        say_which_one(panel, household, key, shared, things)
    print(f"reported {len(answer.get('recorded', []))} thing(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
