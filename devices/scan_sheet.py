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
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from devices.epaper import render_notice_bmp, render_waiting_bmp
from devices.print_sheet import recall
from devices.trmnl_byos import screen_for
from shared.vision_contracts import PageReading
from vision.read_sheet import MarkersNotFound, detect_markers, read_cells, read_qr, rectify

# 300 dpi over A4 is 2480x3508: enough that an ArUco module is about 30 pixels, and the
# detector wants four. Higher costs seconds per scan and buys nothing measurable.
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


def describe(reading: PageReading, spec_title: str) -> tuple[str, list[str]]:
    """The words for the display. A count of marks, never a count of right answers."""
    marked = [cell for cell in reading.cells if cell.value]
    lines = [f"Ho letto il foglio: {spec_title}."]
    if marked:
        lines.append("Hai segnato: " + ", ".join(str(cell.value) for cell in marked) + ".")
    else:
        lines.append("Non ho trovato segni. Va bene lo stesso.")
    if reading.degraded:
        lines.append("Qualche casella non era chiara: la guarda un adulto.")
    return "Fatto", lines


def main() -> int:
    button_file = Path(sys.argv[1] if len(sys.argv) > 1 else "")
    sheets_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "")
    screen_file = Path(sys.argv[3] if len(sys.argv) > 3 else "")
    scanner = sys.argv[4] if len(sys.argv) > 4 else ""
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

    # The display server already put this same screen up in the response the press caused;
    # writing the identical bytes is what makes this a no-op rather than a second redraw.
    target.write_bytes(render_waiting_bmp())
    try:
        page = scan_page(find_scanner(scanner))
    except (subprocess.SubprocessError, OSError, ValueError) as exc:
        print(f"the scanner did not answer: {exc}")
        say("Non ci sono riuscito", ["Lo scanner non ha risposto.", "Riprova più tardi."])
        return 0

    try:
        flat = rectify(page, detect_markers(page))
    except MarkersNotFound as exc:
        print(f"page refused: {exc}")
        say(
            "Non l'ho letto",
            ["Il foglio era storto o coperto.", "Rimettilo dritto e premi di nuovo."],
        )
        return 0

    try:
        spec = recall(sheets_dir, read_qr(flat).sheet_id)
    except (ValueError, OSError, KeyError) as exc:
        print(f"cannot tell which sheet this is: {exc}")
        say("Non l'ho riconosciuto", ["Questo foglio non è di Lanternina."])
        return 0

    reading = read_cells(flat, spec)
    heading, lines = describe(reading, spec.title)
    say(heading, lines)
    marks = ", ".join(
        f"{cell.cell_id}={'segno' if cell.value else 'vuota'}" for cell in reading.cells
    )
    print(f"read {spec.sheet_id}: {marks}")
    button_file.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
