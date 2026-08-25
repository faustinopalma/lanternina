"""The equipment a run touches, and the two rules about touching it.

Everything here was written inside :mod:`devices.run_blueprint` and moved out on 21
August 2026, unchanged, when a second runner appeared. It is not about blueprints or
about experiences: it is about which display a notice lands on and who owns the file
afterwards, and both of those are properties of the house.

The two rules are worth their sentence each, because both were bought with a display
that looked broken.

* **Which display** is the parent's choice, made in the panel and read back from the
  cached assignment. A caller working from a stale note put the sheet's notice on the
  picture display on 19 August 2026, and nothing in the code could tell.
* **Who owns the file** survives a write. Temp-file-and-rename silently hands a file to
  whoever ran the command, which on 17 and 19 August 2026 broke first the display
  server's read and then the button path's write.
"""

from __future__ import annotations

import os
import random
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from devices.epaper import render_notice_bmp
from devices.inventory import holders, load_jobs
from devices.pretend import Pretend
from devices.trmnl_byos import screen_for, sheet_layer_until
from shared.capabilities import JOB_SHEET, REACHABLE, HouseCapability
from shared.ids import SheetId


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
    # Where the reading happens. Empty means the house cannot have a page read at all:
    # since 21 August 2026 there is no arithmetic underneath, so a run that reaches its
    # `read_sheet` step with no panel simply stops there.
    panel: str = ""
    household: str = ""
    device_key: str = ""
    # Set, and this house has no equipment and behaves as though it had all of it. Every
    # path a simulated house writes is inside this directory, which is why a pretend run
    # cannot reach a real display: not because something checks, but because the real
    # paths are never built. See :mod:`devices.pretend`.
    pretend: Path | None = None

    @property
    def capabilities(self) -> frozenset[HouseCapability]:
        # A pretend house has whatever an experience can ask for, read off the registry
        # rather than listed here: a device added to `shared/capabilities.py` is reachable
        # in simulation on the same commit, which is the point of simulating at all.
        if self.pretend is not None:
            return REACHABLE
        found: set[HouseCapability] = set()
        if self.printer:
            found.add(HouseCapability.PRINT_A4)
        if self.scanner:
            found.add(HouseCapability.SCAN_A4)
        if self.screen is not None:
            found.add(HouseCapability.SHOW_800X480_1BIT)
        return frozenset(found)

    @property
    def pretending(self) -> Pretend | None:
        return Pretend(self.pretend) if self.pretend is not None else None


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


def _jobs_file(env: Mapping[str, str]) -> Path | None:
    named = env.get("LANTERNINA_JOBS_FILE", "")
    if named:
        return Path(named)
    shared = env.get("TRMNL_SCREEN_FILE", "")
    return Path(shared).with_name("jobs.json") if shared else None


def printer_in(env: Mapping[str, str]) -> str:
    """The queue this house prints to: the printer the parent gave the job to.

    Until 25 August 2026 this was `LANTERNINA_PRINTER` and nothing else, so handing the
    print job to a second printer in the panel changed the row and not where the paper
    came out. That variable is now the fallback: a house whose panel has said nothing, or
    whose chosen printer has no CUPS queue, prints exactly where it printed before.
    """
    configured = env.get("LANTERNINA_PRINTER", "")
    jobs = _jobs_file(env)
    if jobs is None:
        return configured
    from devices.inventory import chosen_printer

    return chosen_printer(jobs, configured)


def scanner_in(env: Mapping[str, str]) -> str:
    """The scanner model this house reads from, chosen the same way as the printer."""
    configured = env.get("LANTERNINA_SCANNER", "")
    jobs = _jobs_file(env)
    if jobs is None:
        return configured
    from devices.inventory import chosen_scanner

    return chosen_scanner(jobs, configured)


def show(house: House, heading: str, lines: list[str]) -> None:
    pretending = house.pretending
    if pretending is not None:
        from devices import pretend as simulated

        simulated.show(pretending, heading, lines)
        return
    if house.screen is None:
        raise CannotRun("there is no display in this house")
    # Something new on the sheet layer means it is current again, whatever the last
    # afternoon's ending said about when it was done.
    sheet_layer_until(house.screen).unlink(missing_ok=True)
    replace(house.screen, render_notice_bmp(heading, lines))


# How long an ending stays on the wall before the display goes back to its picture.
# Long enough that somebody in another room still finds it; short enough that a wall does
# not become a museum. Before this existed the answer was "until some later afternoon
# happens to overwrite it", which on the house was two days.
SHEET_LAYER_MINUTES = 20


def the_sheet_layer_is_done(house: House, now: float) -> None:
    """The afternoon is over: its screen has this long left, and then the picture returns.

    One marker for the house rather than one per display, which is also what covers the
    trap: a run's moments are spread at random over every display that holds the job, so
    clearing only the one this process picked would leave the others exactly as they were.

    No branch on pretending: a simulated house has no screen path at all, which is the
    same guarantee by construction rather than by a check.
    """
    if house.screen is None:
        return
    ends = sheet_layer_until(house.screen)
    try:
        ends.write_text(str(now + SHEET_LAYER_MINUTES * 60.0), encoding="utf-8")
    except OSError:
        # An afternoon that ended must not fail because a marker could not be written.
        pass


def hand_over(
    house: House,
    drawn: NDArray[np.uint8],
    *,
    sheet_id: SheetId,
    send: bool = True,
) -> NDArray[np.uint8]:
    """Put a page on the table, wherever this house's table is, and keep its blank.

    The branch is here rather than in a runner on purpose. A runner that could tell a
    pretend house from a real one would grow a second way of running an afternoon, and the
    two would drift apart at exactly the speed nobody was watching.

    ``drawn`` is the page as a model drew it. Nothing on this side decides what is on it.
    """
    from devices.print_page import make_sheet, print_page

    pretending = house.pretending
    if pretending is not None:
        from devices import pretend as simulated

        blank, pdf = make_sheet(drawn, sheets_dir=house.sheets_dir, sheet_id=sheet_id)
        # The same blank the printer would have produced, so the sheet that can be laid on
        # the simulated glass is the sheet that would have come out.
        simulated.hand_over(pretending, sheet_id, pdf, blank)
        return blank
    if not house.printer:
        raise CannotRun("there is no printer in this house")
    return print_page(
        drawn,
        sheets_dir=house.sheets_dir,
        sheet_id=sheet_id,
        printer=house.printer,
        send=send,
    )


def replace(path: Path, data: bytes) -> None:
    """Write the file whole, and leave it belonging to whoever owned it.

    Temp-file-and-rename keeps a half-written screen off the display. It also silently
    hands the file to whoever ran the command: on 17 August 2026 that turned
    ``trmnl-devices.json`` from ``root:lanternina`` into ``root:root``, the display server
    lost its read, and the symptom was a display that looked dead.

    A file that does not exist yet has no owner to keep. It takes the directory's group
    and not the directory's user, which is the correction of 21 August 2026: the state
    directory is ``root:lanternina``, so giving a new screen the directory's user means a
    process that is not root trying to give a file to root, and Linux says
    ``Operation not permitted``. The afternoon stopped at its first moment with a display
    that had never been written. The group is the half that matters and the half that is
    allowed, because the reader and the writer are both in it.

    On 19 August 2026 a run under ``sudo`` created ``screen-CF7D04.bmp`` as ``root:root``:
    the display server could still read it, but the button path — ``fausto:lanternina`` —
    could no longer write that display at all. That is why a new file is group-writable.
    """
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    existing = path.stat() if path.exists() else None
    was = existing or path.parent.stat()
    if _chown is not None:
        try:
            _chown(temporary, was.st_uid if existing else -1, was.st_gid)
        except PermissionError:
            # Keeping an owner is worth trying and never worth failing over: a screen
            # written by the wrong user is still a screen, and no screen at all is a
            # display showing yesterday.
            pass
    temporary.chmod(stat.S_IMODE(was.st_mode) if existing else 0o664)
    temporary.replace(path)
