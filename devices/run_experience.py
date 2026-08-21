"""Run an experience: play it until a page is on the table, and again when one comes back.

An experience is data; this is the code that means something by it. Every act maps to one
call into a module that already existed — the notice renderer, the printer queue, the
scanner, the page reader — and nothing here interprets what the experience says beyond
choosing which of those calls to make.

The seam is different from :mod:`devices.run_blueprint`, and that is the whole reason
this module exists rather than a verb being added there. A blueprint had two halves,
because it read paper once. An experience has one half per page that comes back: it is
played forward until a ``collect``, and every later stretch begins with a page on the
glass. So there is no ``start``/``resume`` pair; there is :func:`begin` and
:func:`carry_on`, and ``carry_on`` may be called as many times as the afternoon has
collects.

Three things this does not do, each of them a rule rather than an omission.

* **Nothing waits.** An afternoon nobody continues stops where it is. There is no timer,
  no reminder and no record that something was left unfinished — the run file simply sits
  there until a page arrives or the afternoon's own hours run out.
* **Nothing is pushed.** A ``collect`` whose outcome says ``ask`` is answered inside the
  reply to a request this house makes, which is :func:`_ask`. The panel cannot start
  anything here.
* **Nothing is guessed.** A page the reader could not tell about does not become a
  ``blank``, because ``blank`` is a branch somebody wrote and taking it would be inventing
  what happened. See :func:`came_back`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devices.house import CannotRun, House, screen_in, show
from devices.print_sheet import compose_and_print, recall
from devices.read_page import PanelUnreachable, read_page
from devices.scan_sheet import find_scanner, scan_page
from shared.experience import (
    ASK,
    Came,
    Close,
    Collect,
    Continuation,
    Experience,
    ExperienceError,
    HandOver,
    Moment,
    Say,
    moment_from_dict,
)
from shared.ids import new_exercise_id, new_id, new_sheet_id
from shared.sheet import SheetSpec
from shared.vision_contracts import PageReading, ReadConfidence
from vision.read_sheet import detect_markers, read_qr, rectify

# Asking for the rest of an afternoon is a model writing several moments, which takes
# longer than wording one sentence and is still something a person may be standing in
# front of. Chosen, not measured.
ASK_TIMEOUT_SECONDS = 120


@dataclass(frozen=True, slots=True)
class Afternoon:
    """One run, as much of it as the house has to remember between two pages.

    It holds the whole experience rather than its id, for the reason ``resume`` gives in
    the blueprint runner: the house runs what it started. A document edited while a sheet
    was on the table would otherwise send the second half of one afternoon after the first
    half of another.

    ``segment`` is the moments currently being played. It is empty until an outcome says
    ``ask``; from then on it is the continuation that came back, and the experience's own
    moments are out of reach. That is what makes a continuation self-contained: its
    branches name its own moments, so an id it shares with the approved document is a
    coincidence rather than a jump.
    """

    run_id: str
    experience: Experience
    started_at: float
    # The collect this run stopped at. A run is never stored anywhere else: an afternoon
    # between two moments that do not touch paper has nothing to wait for.
    waiting_at: str
    segment: tuple[Moment, ...] = ()

    @property
    def moments(self) -> tuple[Moment, ...]:
        return self.segment or self.experience.moments

    @property
    def over_at(self) -> float:
        return self.started_at + self.experience.minutes * 60.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "waiting_at": self.waiting_at,
            "experience": self.experience.to_dict(),
            "segment": [moment.to_dict() for moment in self.segment],
        }

    @staticmethod
    def from_dict(values: Any) -> Afternoon:
        return Afternoon(
            run_id=str(values["run_id"]),
            experience=Experience.from_dict(values["experience"]),
            started_at=float(values["started_at"]),
            waiting_at=str(values["waiting_at"]),
            segment=tuple(moment_from_dict(m) for m in values.get("segment", [])),
        )


def load_experience(path: Path) -> Experience:
    return Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))


# ── Where a run is kept ──────────────────────────────────────────────────────────────


def _runs(sheets_dir: Path) -> Path:
    return sheets_dir / "afternoons"


def _run_file(sheets_dir: Path, run_id: str) -> Path:
    return _runs(sheets_dir) / f"{run_id}.json"


def _page_file(sheets_dir: Path, sheet_id: str) -> Path:
    """The note that says which afternoon a printed sheet belongs to.

    The paper carries the run, exactly as it carried the blueprint before it: two sheets
    can be in the house at once and the one on the glass says which afternoon it is.
    """
    return _runs(sheets_dir) / "pages" / f"{sheet_id}.json"


def _write(path: Path, values: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _forget(sheets_dir: Path, run: Afternoon, sheets: list[SheetSpec]) -> None:
    """An afternoon that ended leaves nothing behind, not even that it happened."""
    _run_file(sheets_dir, run.run_id).unlink(missing_ok=True)
    for spec in sheets:
        _page_file(sheets_dir, str(spec.sheet_id)).unlink(missing_ok=True)


def waiting_runs(sheets_dir: Path) -> list[str]:
    """Every afternoon this house has begun and not finished.

    One at a time is the rule the caller applies, and it is a rule about the house rather
    than about a person: two sheets on the table from two different afternoons is a house
    that has stopped making sense, not a person doing too much.
    """
    return sorted(path.stem for path in sorted(_runs(sheets_dir).glob("*.json")))


def forget_what_is_over(sheets_dir: Path, now: float) -> list[str]:
    """Delete every run whose hours have passed, and the notes on its paper.

    The runner itself notices the hours when a page arrives, because that is the only
    moment it is awake. A run nobody ever brought a page back to would otherwise sit on
    disk for good, holding a whole afternoon's text and blocking the next one. Nothing is
    said to anybody and nothing is recorded: an afternoon that ran out of hours is over,
    which is what an afternoon nobody continued was always going to be.
    """
    gone: list[str] = []
    for path in sorted(_runs(sheets_dir).glob("*.json")):
        try:
            run = Afternoon.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, KeyError, ExperienceError):
            # A run file this house cannot read is not an afternoon it can carry on.
            path.unlink(missing_ok=True)
            gone.append(path.stem)
            continue
        if now <= run.over_at:
            continue
        path.unlink(missing_ok=True)
        gone.append(run.run_id)
    for note in sorted((_runs(sheets_dir) / "pages").glob("*.json")):
        try:
            run_id = str(json.loads(note.read_text(encoding="utf-8"))["run_id"])
        except (OSError, ValueError, KeyError):
            note.unlink(missing_ok=True)
            continue
        if run_id in gone:
            note.unlink(missing_ok=True)
    return gone


# ── Playing ──────────────────────────────────────────────────────────────────────────


def _do(house: House, moment: Moment, *, send: bool) -> SheetSpec | None:
    if isinstance(moment, Say | Close):
        show(house, moment.heading, list(moment.lines))
        return None
    if isinstance(moment, HandOver):
        if not house.printer:
            raise CannotRun("there is no printer in this house")
        return compose_and_print(
            moment.design,
            sheets_dir=house.sheets_dir,
            sheet_id=new_sheet_id(),
            exercise_id=new_exercise_id(),
            printer=house.printer,
            send=send,
        )
    raise CannotRun("a collect is the seam between two stretches of an afternoon")


def _play(
    house: House, moments: tuple[Moment, ...], start: int, *, send: bool
) -> tuple[Collect | None, list[SheetSpec]]:
    """Run moments forward from ``start`` until a page has to come back, or it closes.

    Returns the ``collect`` it stopped at — or None, meaning the afternoon is over — and
    every sheet it put on the table on the way.
    """
    printed: list[SheetSpec] = []
    for moment in moments[start:]:
        if isinstance(moment, Collect):
            return moment, printed
        spec = _do(house, moment, send=send)
        if spec is not None:
            printed.append(spec)
        if isinstance(moment, Close):
            return None, printed
    # `_check_graph` refuses a document that could reach here, so this is a bug rather
    # than a badly written afternoon.
    raise CannotRun("the afternoon ran off the end of its moments")


def _pause(house: House, run: Afternoon, at: Collect, printed: list[SheetSpec]) -> None:
    """Write down where the afternoon got to, and which paper points back at it."""
    waiting = Afternoon(
        run_id=run.run_id,
        experience=run.experience,
        started_at=run.started_at,
        waiting_at=at.id,
        segment=run.segment,
    )
    _write(_run_file(house.sheets_dir, run.run_id), waiting.to_dict())
    for spec in printed:
        _write(_page_file(house.sheets_dir, str(spec.sheet_id)), {"run_id": run.run_id})


def begin(
    house: House, experience: Experience, *, now: float | None = None, send: bool = True
) -> str | None:
    """Play an afternoon up to its first page. Returns the run id, if it is waiting for one.

    None means it closed without ever needing paper back, and nothing was written down.
    """
    if not experience.runnable_in(house.capabilities):
        raise CannotRun(f"this house cannot run {experience.title}")
    run = Afternoon(
        run_id=new_id("aft"),
        experience=experience,
        started_at=time.time() if now is None else now,
        waiting_at="",
    )
    at, printed = _play(house, run.moments, 0, send=send)
    if at is None:
        return None
    _pause(house, run, at, printed)
    return run.run_id


def came_back(reading: PageReading) -> Came | None:
    """Which of the two words describes this page, or None if neither honestly does.

    A cell the reader could not tell about has no value and no mark, so a page of nothing
    but unsure cells would otherwise read as ``blank`` — and ``blank`` is a branch somebody
    wrote, usually the one that closes the afternoon kindly. Taking it because the reading
    was poor would be closing an afternoon on a page that was filled in. So the run stops
    instead, which is the same thing it does when the panel cannot be reached: the page
    stays where it is and nothing is said about it.
    """
    if any(cell.value for cell in reading.cells):
        return Came.MARKS
    if any(cell.confidence is ReadConfidence.UNSURE for cell in reading.cells):
        return None
    return Came.BLANK


def _read(house: House) -> tuple[SheetSpec, PageReading]:
    """Read whatever is on the glass. With no panel there is no reading and no second-best."""
    if not house.scanner:
        raise CannotRun("there is no scanner in this house")
    page = scan_page(find_scanner(house.scanner))
    rectified = rectify(page, detect_markers(page))
    payload = read_qr(rectified)
    spec = recall(house.sheets_dir, payload.sheet_id)
    try:
        reading = read_page(
            rectified,
            spec,
            panel=house.panel,
            household=house.household,
            key=house.device_key,
        )
    except PanelUnreachable as exc:
        raise CannotRun(f"the page was not read: {exc}") from exc
    return spec, reading


def _ask(
    house: House, run: Afternoon, at: Collect, came: Came, reading: PageReading
) -> Continuation:
    """Post what came back and receive the rest of the afternoon.

    This is the one call in this module that reaches outside the house, and its direction
    is the point: the hub asks, and the model thinks inside the answer. There is no
    endpoint here for the panel to call, so nothing outside can start, extend or redirect
    an afternoon.
    """
    if not (house.panel and house.household and house.device_key):
        raise CannotRun("no panel is configured, so there is nobody to ask")
    body = json.dumps(
        {
            "experience": run.experience.to_dict(),
            "after": at.id,
            "came": str(came),
            "reading": reading.to_dict(),
        }
    ).encode()
    request = urllib.request.Request(
        f"{house.panel.rstrip('/')}/api/device/{house.household}/experience",
        data=body,
        headers={"X-Device-Key": house.device_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=ASK_TIMEOUT_SECONDS) as response:
            answer = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise CannotRun(f"the panel refused to go on: {exc.code} {detail}") from exc
    except (OSError, ValueError) as exc:
        raise CannotRun(f"the panel did not answer: {exc}") from exc
    try:
        carrying_on = Continuation.from_dict(answer)
    except ExperienceError as exc:
        raise CannotRun(f"what came back is not a continuation: {exc}") from exc
    # Checked here as well as in the panel, because a continuation for another afternoon
    # or another branch would be played as if it had been asked for.
    if carrying_on.experience_id != run.experience.experience_id:
        raise CannotRun(
            f"the continuation is for {carrying_on.experience_id!r}, not "
            f"{run.experience.experience_id!r}"
        )
    if carrying_on.after != at.id:
        raise CannotRun(f"the continuation follows {carrying_on.after!r}, not {at.id!r}")
    if not carrying_on.requires <= house.capabilities:
        raise CannotRun("the continuation asks for something this house does not have")
    return carrying_on


def carry_on(house: House, *, now: float | None = None, send: bool = True) -> str:
    """Read the page on the glass and play the stretch of afternoon that follows it.

    Returns a sentence for whoever is watching. It says what happened to the afternoon
    and nothing about the person who filled the page in.
    """
    moment = time.time() if now is None else now
    spec, reading = _read(house)
    pointer = _page_file(house.sheets_dir, str(spec.sheet_id))
    if not pointer.is_file():
        raise CannotRun(f"sheet {spec.sheet_id} does not belong to an afternoon this house started")
    run_id = str(json.loads(pointer.read_text(encoding="utf-8"))["run_id"])
    run_path = _run_file(house.sheets_dir, run_id)
    if not run_path.is_file():
        # The afternoon ended and took its own file with it; this is the paper catching up.
        pointer.unlink(missing_ok=True)
        raise CannotRun("that afternoon is already over")
    run = Afternoon.from_dict(json.loads(run_path.read_text(encoding="utf-8")))

    if moment > run.over_at:
        # An afternoon lasts an afternoon. Noticed when a page arrives rather than by a
        # timer, because nothing here runs while nobody is doing anything.
        _forget(house.sheets_dir, run, [spec])
        return "that afternoon is over"

    at = run.moments[_index_of(run, run.waiting_at)]
    if not isinstance(at, Collect):
        raise CannotRun(f"{run.waiting_at!r} is not a moment that reads a page")
    came = came_back(reading)
    if came is None:
        return "the page was not clear enough to say what came back"
    then = _then(at, came)

    if then == ASK:
        carrying_on = _ask(house, run, at, came, reading)
        run = Afternoon(
            run_id=run.run_id,
            experience=run.experience,
            started_at=run.started_at,
            waiting_at=run.waiting_at,
            segment=carrying_on.moments,
        )
        start = 0
    else:
        start = _index_of(run, then)

    following, printed = _play(house, run.moments, start, send=send)
    if following is None:
        _forget(house.sheets_dir, run, [spec, *printed])
        return "the afternoon is finished"
    _pause(house, run, following, printed)
    return f"waiting for a page at {following.id}"


def _then(at: Collect, came: Came) -> str:
    for outcome in at.outcomes:
        if outcome.when is came:
            return outcome.then
    raise CannotRun(f"{at.id!r} does not say what happens when a page comes back {came}")


def _index_of(run: Afternoon, moment_id: str) -> int:
    for index, moment in enumerate(run.moments):
        if moment.id == moment_id:
            return index
    raise CannotRun(f"there is no moment called {moment_id!r} in this afternoon")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an experience in this house.")
    parser.add_argument("what", choices=("begin", "carry-on"))
    parser.add_argument("--experience", type=Path, help="the file, for begin")
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
        if args.what == "begin":
            if args.experience is None:
                parser.error("begin needs --experience")
            experience = load_experience(args.experience)
            run_id = begin(house, experience, send=not args.no_paper)
            print(f"{experience.title}: {run_id or 'closed without asking for paper'}")
        else:
            print(carry_on(house, send=not args.no_paper))
    except (ExperienceError, CannotRun, ValueError, OSError) as exc:
        print(f"{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
