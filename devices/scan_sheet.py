"""Scan the sheet on the glass, read it, and say what came back.

Runs on the hub when somebody presses the button on the display: `trmnl_byos` writes down
the press and this acts on it, because a scan takes tens of seconds and the display is
holding the other end of an HTTP socket while it waits for its picture.

A flatbed with the lid down cannot see anything but the sheet, so the guarantee that no
person is in frame stops depending on this code. What still depends on it is the rest: the
full scan is rectified to the marker quadrilateral before anything is kept, and the page is
refused outright if the four markers are not all there rather than read at a guess.

What it says back describes ink. Which boxes carry a mark, which are empty, and which the
parent should look at. Nothing here decides whether a mark is the right one.

Reading happens in the cloud, through the panel, and there is no arithmetic underneath any
more. With the panel unreachable the page is not read: the display says so in a sentence
that blames nobody, and nothing is recorded.

**A press while an afternoon is under way belongs to the afternoon**, and until 24 August
2026 it did not go there. This module is the standalone-sheet path: it reads a page, says
what came back, and stops. `run_experience.carry_on` is the other reader, the one that moves
an afternoon on from the moment it is waiting at, and nothing started it — the unit exists
and had no caller. Measured in the house that day: a page went on the glass, was read
correctly in 29 s, the display described it, and the afternoon stood at its `collect` giving
out help about bringing the map to the glass while the map was on the glass.

The choice is made before the scan and not after, because a scan is 29 s of somebody
standing at the scanner and asking twice is not an option. So it is made from the only thing
knowable beforehand — whether an afternoon is waiting — and the sheet's own QR stays what
refuses a page that belongs somewhere else.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from devices.ask_panel import PanelUnreachable, read_page
from devices.epaper import render_notice_bmp, render_waiting_bmp
from devices.house import House, printer_in, scanner_in
from devices.print_page import recall, waiting
from devices.trmnl_byos import screen_for
from shared.ids import SheetId
from shared.vision_contracts import WhatCameBack

# 300 dpi over A4 is 2480x3508. A flatbed with the lid down needs no rectifying — the page
# is flat and the resolution is known — so this is simply what the reader is shown.
SCAN_RESOLUTION = "300"
SCAN_TIMEOUT_SECONDS = 120
LIST_TIMEOUT_SECONDS = 40


def find_scanner(model: str) -> str:
    """The scanner's device name, looked up now rather than remembered.

    Configured by the model printed on the front of the machine, because both names SANE
    offers carry something that moves: `airscan:e0:...` has an index the backend assigns
    while discovering, and `escl:https://192.168.0.5` has an address DHCP reassigns.

    Listing first is doing more work than resolving a name, and that is the point. An open
    that arrives before mDNS discovery has finished fails with "Invalid argument", which is
    what happened in front of somebody who had just pressed the button — and the same
    device string resolved fine a minute later. The list call is what waits for the machine
    to be found.
    """
    finished = subprocess.run(
        ["scanimage", "--formatted-device-list", "%d%n"],
        capture_output=True,
        timeout=LIST_TIMEOUT_SECONDS,
    )
    devices = [line.strip() for line in finished.stdout.decode("utf-8", "replace").splitlines()]
    found = [device for device in devices if model.lower() in device.lower()]
    if not found:
        raise ValueError(f"no scanner matching {model!r}; SANE offers {devices}")
    return found[0]


def scan_page(device: str) -> NDArray[np.uint8]:
    """One page off the glass, in memory. Nothing is written to disk on the way."""
    finished = subprocess.run(
        [
            "scanimage",
            "--device-name",
            device,
            "--format=pnm",
            "--mode",
            "Gray",
            "--resolution",
            SCAN_RESOLUTION,
        ],
        capture_output=True,
        timeout=SCAN_TIMEOUT_SECONDS,
    )
    if finished.returncode != 0:
        # What the backend said is the whole diagnosis — "Device busy" and "Invalid
        # argument" need different answers and an exit code tells them apart badly.
        raise ValueError(finished.stderr.decode("utf-8", "replace").strip() or "scan failed")
    buffer = np.frombuffer(finished.stdout, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("the scanner returned something that is not an image")
    return np.asarray(image, dtype=np.uint8)


def describe(came: WhatCameBack) -> tuple[str, list[str]]:
    """The words for the display. What is on the paper, never how it was done.

    A page that is not the one this house handed out is described anyway and not refused.
    Somebody putting back an earlier sheet, or a drawing from school, has not erred, and
    the old answer — *Questo foglio non è di Lanternina* — was a refusal aimed at a person
    for a mistake the working rules say cannot exist.
    """
    if not came.written:
        return "Fatto", ["Il foglio è arrivato.", "Non ci ho trovato segni. Va bene lo stesso."]
    lines = ["Ho guardato il foglio."]
    lines.extend(str(one) for one in came.describes[:2])
    if came.degraded:
        lines.append("Non sono riuscito a guardarlo bene.")
    return "Fatto", lines


def _to_the_afternoon(
    button_file: Path, sheets_dir: Path, target: Path, scanner: str
) -> int:
    """Hand the press to the afternoon's own reader, on the display that was pressed.

    The screen is the one somebody is standing at, not the one `screen_in` would pick: that
    chooses at random among the displays holding the job, and the person who pressed is here.

    Never raises past this point. A press answered with a stack trace is a display left on
    the waiting screen, and the afternoon still has its clock: whatever happens, it ends.
    """
    # Imported here because `run_experience` takes this module's scanner primitives, so the
    # two would not import each other at module scope.
    from devices.run_experience import carry_on

    house = House(
        printer=printer_in(os.environ),
        scanner=scanner,
        screen=target,
        sheets_dir=sheets_dir,
        panel=os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/"),
        household=os.environ.get("LANTERNINA_HOUSEHOLD", ""),
        device_key=os.environ.get("LANTERNINA_DEVICE_KEY", ""),
    )
    try:
        print(f"carrying the afternoon on: {carry_on(house, send=True)}")
    except Exception as exc:  # noqa: BLE001 - a press must not end in a traceback
        print(f"the afternoon did not carry on: {exc}")
        target.write_bytes(
            render_notice_bmp("Il foglio è arrivato", ["Adesso non riesco a leggerlo."])
        )
    button_file.unlink(missing_ok=True)
    return 0


def main() -> int:
    button_file = Path(sys.argv[1] if len(sys.argv) > 1 else "")
    sheets_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "")
    screen_file = Path(sys.argv[3] if len(sys.argv) > 3 else "")
    # The parent's choice first: the argument is what the unit file was written with, and
    # a scanner handed the job in the panel is the newer statement of the same thing.
    scanner = scanner_in(os.environ) or (sys.argv[4] if len(sys.argv) > 4 else "")
    if not (str(button_file) and str(sheets_dir) and str(screen_file) and scanner):
        print("usage: scan_sheet <button-file> <sheets-dir> <screen-file> <scanner-model>")
        return 1

    try:
        press = json.loads(button_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"no press to act on ({exc})")
        return 0
    friendly_id = str(press.get("friendlyId", ""))
    target = screen_for(screen_file, friendly_id)

    def say(heading: str, lines: list[str]) -> None:
        target.write_bytes(render_notice_bmp(heading, lines))

    from devices.run_experience import waiting_runs

    if waiting_runs(sheets_dir):
        return _to_the_afternoon(button_file, sheets_dir, target, scanner)

    # The display server already put this same screen up in the response the press caused;
    # writing the identical bytes is what makes this a no-op rather than a second redraw.
    target.write_bytes(render_waiting_bmp())
    try:
        came_off = scan_page(find_scanner(scanner))
    except (subprocess.SubprocessError, OSError, ValueError) as exc:
        print(f"the scanner did not answer: {exc}")
        say("Non ci sono riuscito", ["Lo scanner non ha risposto.", "Riprova più tardi."])
        return 0

    handed_out = waiting(sheets_dir)
    if not handed_out:
        # No blank to compare against, so there is nothing to say about the page. Not a
        # refusal: the sheet is fine, this house simply has nothing it is waiting for.
        print("no page was handed out, so there is nothing to compare this one to")
        say("Il foglio è arrivato", ["Adesso non ho niente con cui confrontarlo."])
        button_file.unlink(missing_ok=True)
        return 0
    sheet_id = SheetId(str(handed_out[-1]))

    try:
        came = read_page(
            recall(sheets_dir, sheet_id),
            came_off,
            about="",
            panel=os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/"),
            household=os.environ.get("LANTERNINA_HOUSEHOLD", ""),
            key=os.environ.get("LANTERNINA_DEVICE_KEY", ""),
        )
    except (PanelUnreachable, FileNotFoundError) as exc:
        # The button was pressed, so somebody is standing there. Saying nothing at all is
        # what the page gets; the person gets a sentence that claims nothing about it.
        print(f"the page was not read: {exc}")
        say("Il foglio è arrivato", ["Adesso non riesco a leggerlo.", "Lo lascio lì."])
        button_file.unlink(missing_ok=True)
        return 0

    heading, lines = describe(came)
    say(heading, lines)
    # The id and nothing else. Whether cells were written on is a fact about what somebody
    # did, and a journal is read by whoever can reach the machine — and, once a hub ships
    # its journal anywhere, by whoever can reach that.
    print(f"read {sheet_id}")
    button_file.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
