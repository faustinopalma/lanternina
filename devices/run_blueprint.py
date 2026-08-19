"""Run a blueprint on the equipment this house actually has.

A blueprint is data; this is the code that means something by it. Every verb maps to one
call into a module that already existed — the layout, the printer queue, the notice
renderer, the sheet reader — and nothing here interprets anything the blueprint says
beyond choosing which of those calls to make.

The run comes in two halves, and the seam is the paper. ``start`` runs the steps up to the
first ``read_sheet`` and stops, because at that point the sheet is in somebody's hands and
the machine has nothing to do. ``resume`` runs the rest, and it identifies the run from the
QR code on the page itself rather than from whatever ran most recently: the paper carries
which experience it belongs to, so two sheets in the house cannot be confused.

Nothing waits, polls or reminds. If the sheet never comes back, ``resume`` is never called,
and that is the whole of what happens — no follow-up, no record that something was left
unfinished, nothing to see later.

The printer queue and the scanner model are passed in. The display is not: which screen a
notice lands on is the parent's choice, made in the panel, and it is read back from the
cached assignment the same way the picture path reads its own. ``--screen`` still overrides
it, for a house that has no cache yet. TODO(poc): the printer and the scanner are still the
caller's word — see ideas/01-panel.md §9.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import stat
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from devices.epaper import render_notice_bmp
from devices.inventory import JOB_SHEET, holders, load_jobs
from devices.print_sheet import lay_out_and_print, recall
from devices.read_page import read_page
from devices.scan_sheet import describe, find_scanner, scan_page
from devices.trmnl_byos import screen_for
from shared.blueprint import (
    Blueprint,
    BlueprintError,
    PrintSheet,
    ShowReading,
    ShowWords,
    Step,
    Verb,
)
from shared.capabilities import HouseCapability
from shared.ids import SheetId, new_exercise_id, new_sheet_id
from shared.sheet import SheetSpec
from shared.vision_contracts import PageReading
from vision.read_sheet import detect_markers, read_qr, rectify


class CannotRun(RuntimeError):
    """The house cannot do what this step needs, or the sheet is not where it should be."""


# Looked up rather than imported because `os.chown` does not exist on Windows, where
# there is no owner to preserve. Development happens there and the running happens on the
# hub, so the check has to hold on both.
_chown = getattr(os, "chown", None)


@dataclass(frozen=True, slots=True)
class House:
    """The three things a run touches, or nothing where a thing is absent."""

    printer: str = ""
    scanner: str = ""
    screen: Path | None = None
    sheets_dir: Path = Path(".")
    # Where the reading happens. Empty means the house reads its own pages with
    # arithmetic and says the answer is degraded, which is what it does when the panel is
    # unreachable anyway.
    panel: str = ""
    household: str = ""
    device_key: str = ""

    @property
    def capabilities(self) -> frozenset[HouseCapability]:
        found: set[HouseCapability] = set()
        if self.printer:
            found.add(HouseCapability.PRINT_A4)
        if self.scanner:
            found.add(HouseCapability.SCAN_A4)
        if self.screen is not None:
            found.add(HouseCapability.SHOW_800X480_1BIT)
        return frozenset(found)


def load_blueprint(path: Path) -> Blueprint:
    return Blueprint.from_dict(json.loads(path.read_text(encoding="utf-8")))


def sheet_file(shared: Path, jobs_file: Path) -> Path:
    """Where a notice about the sheet goes: the file of one of the displays that hold it.

    The same resolution the picture path makes for itself. Until 19 August 2026 this half
    of the house took the screen from whoever called it, so a caller working from a stale
    note put the sheet's notice on the picture display, and nothing here could tell.

    Several displays may hold the job, and one of them is picked at random each time. That
    is what was asked for and it has a cost worth saying plainly: on a house with two, a
    notice appears on one of them, and somebody standing at the other does not see it.

    With no answer from the panel the shared file is still the target, which is what the
    house did before anybody could say which display was which.
    """
    labels = sorted(
        str(thing.get("label") or "")
        for thing in holders(load_jobs(jobs_file), JOB_SHEET)
        if thing.get("label")
    )
    return screen_for(shared, random.choice(labels)) if labels else shared


def screen_in(env: Mapping[str, str]) -> Path | None:
    """The file the sheet's display reads, or None if this house has no display at all."""
    shared = env.get("TRMNL_SCREEN_FILE", "")
    if not shared:
        return None
    path = Path(shared)
    jobs = env.get("LANTERNINA_JOBS_FILE", "") or str(path.with_name("jobs.json"))
    return sheet_file(path, Path(jobs))


def _show(house: House, heading: str, lines: list[str]) -> None:
    if house.screen is None:
        raise CannotRun("there is no display in this house")
    _replace(house.screen, render_notice_bmp(heading, lines))


def _replace(path: Path, data: bytes) -> None:
    """Write the file whole, and leave it belonging to whoever owned it.

    Temp-file-and-rename keeps a half-written screen off the display. It also silently
    hands the file to whoever ran the command: on 17 August 2026 that turned
    ``trmnl-devices.json`` from ``root:lanternina`` into ``root:root``, the display server
    lost its read, and the symptom was a display that looked dead.

    A file that does not exist yet has no owner to keep, so it takes the directory's and is
    made group-writable. On 19 August 2026 a run under ``sudo`` created
    ``screen-CF7D04.bmp`` as ``root:root``: the display server could still read it, but the
    button path — ``fausto:lanternina`` — could no longer write that display at all.
    """
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    existing = path.stat() if path.exists() else None
    was = existing or path.parent.stat()
    if _chown is not None:
        _chown(temporary, was.st_uid, was.st_gid)
    temporary.chmod(stat.S_IMODE(was.st_mode) if existing else 0o664)
    temporary.replace(path)


def _print(house: House, step: PrintSheet, *, send: bool) -> SheetSpec:
    if not house.printer:
        raise CannotRun("there is no printer in this house")
    return lay_out_and_print(
        step.sheet.to_body(),
        sheets_dir=house.sheets_dir,
        sheet_id=new_sheet_id(),
        exercise_id=new_exercise_id(),
        printer=house.printer,
        send=send,
    )


def _read(house: House) -> tuple[SheetSpec, PageReading]:
    """Read whatever is on the glass, and refuse it if it is not one of our sheets."""
    if not house.scanner:
        raise CannotRun("there is no scanner in this house")
    page = scan_page(find_scanner(house.scanner))
    rectified = rectify(page, detect_markers(page))
    payload = read_qr(rectified)
    spec = recall(house.sheets_dir, payload.sheet_id)
    reading = read_page(
        rectified,
        spec,
        panel=house.panel,
        household=house.household,
        key=house.device_key,
    )
    return spec, reading


def _run_state(house: House, sheet_id: SheetId) -> Path:
    directory = house.sheets_dir / "runs"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{sheet_id}.json"


def start(house: House, blueprint: Blueprint, *, send: bool = True) -> SheetId | None:
    """Run up to the first step that reads paper. Returns the sheet id, if one was printed."""
    printed: SheetSpec | None = None
    for step in blueprint.steps_for(house.capabilities):
        if step.verb is Verb.READ_SHEET:
            if printed is None:
                raise CannotRun("nothing was printed, so there is nothing to read back")
            _remember(house, blueprint, printed)
            return printed.sheet_id
        printed = _do(house, step, printed=printed, reading=None, send=send) or printed
    return printed.sheet_id if printed else None


def resume(house: House, catalogue: Path) -> None:
    """Read the sheet on the glass and run what the blueprint asks for afterwards."""
    spec, reading = _read(house)
    state = _run_state(house, spec.sheet_id)
    if not state.is_file():
        raise CannotRun(f"sheet {spec.sheet_id} does not belong to a run this house started")
    remembered = json.loads(state.read_text(encoding="utf-8"))
    blueprint = load_blueprint(catalogue / f"{remembered['blueprint_id']}.json")
    if blueprint.version != remembered["version"]:
        # The house runs what it started, not what the catalogue holds now.
        raise CannotRun(
            f"this sheet came from version {remembered['version']} and the catalogue now "
            f"holds version {blueprint.version}"
        )
    # Where to carry on from is found again rather than remembered as a number, so that a
    # display switched off between the two halves shifts no index.
    steps = blueprint.steps_for(house.capabilities)
    after = [position for position, step in enumerate(steps) if step.verb is Verb.READ_SHEET]
    if not after:
        raise CannotRun("this blueprint has no step that reads paper")
    for step in steps[after[0] + 1 :]:
        _do(house, step, printed=spec, reading=reading, send=True)


def _remember(house: House, blueprint: Blueprint, spec: SheetSpec) -> None:
    state = _run_state(house, spec.sheet_id)
    state.write_text(
        json.dumps(
            {
                "blueprint_id": str(blueprint.blueprint_id),
                "version": blueprint.version,
                "sheet_id": str(spec.sheet_id),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _do(
    house: House,
    step: Step,
    *,
    printed: SheetSpec | None,
    reading: PageReading | None,
    send: bool,
) -> SheetSpec | None:
    if isinstance(step, ShowWords):
        _show(house, step.heading, list(step.lines))
        return None
    if isinstance(step, PrintSheet):
        return _print(house, step, send=send)
    if isinstance(step, ShowReading):
        if reading is None or printed is None:
            raise CannotRun("there is no reading to show")
        _, lines = describe(reading, printed.title)
        _show(house, step.heading, lines)
        return None
    if step.verb is Verb.READ_SHEET:
        raise CannotRun("reading is the seam between the two halves of a run")
    # ASK_MODEL. TODO(poc): the verb is part of the vocabulary and nothing on the hub
    # answers it yet; asking a model for content is ideas/07 §2, not §1.
    raise CannotRun(f"{step.verb} is in the vocabulary but not wired on this hub")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a blueprint on this house.")
    parser.add_argument("half", choices=("start", "resume"))
    parser.add_argument("--blueprint", type=Path, help="the file, for start")
    parser.add_argument("--catalogue", type=Path, help="the directory, for resume")
    parser.add_argument("--sheets-dir", type=Path, required=True)
    parser.add_argument("--printer", default="")
    parser.add_argument("--scanner", default="")
    parser.add_argument(
        "--screen",
        type=Path,
        help="override the display; by default the one the parent gave the sheet job to",
    )
    parser.add_argument(
        "--no-paper", action="store_true", help="lay the sheet out without sending it"
    )
    args = parser.parse_args(argv)

    house = House(
        printer=args.printer,
        scanner=args.scanner,
        screen=args.screen or screen_in(os.environ),
        sheets_dir=args.sheets_dir,
        panel=os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/"),
        household=os.environ.get("LANTERNINA_HOUSEHOLD", ""),
        device_key=os.environ.get("LANTERNINA_DEVICE_KEY", ""),
    )
    try:
        if args.half == "start":
            if args.blueprint is None:
                parser.error("start needs --blueprint")
            blueprint = load_blueprint(args.blueprint)
            if not blueprint.runnable_in(house.capabilities):
                print(f"this house cannot run {blueprint.title}")
                return 1
            sheet_id = start(house, blueprint, send=not args.no_paper)
            print(f"{blueprint.title}: printed {sheet_id}")
        else:
            if args.catalogue is None:
                parser.error("resume needs --catalogue")
            resume(house, args.catalogue)
            print("read and reported")
    except (BlueprintError, CannotRun, ValueError, OSError) as exc:
        print(f"{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
