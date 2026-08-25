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

**The ending starts by itself, and that is what changed on 23 August 2026.** Until then an
afternoon that ran out of hours was deleted where it stood: measured on the house on 21
August, run `aft_5ec79e85` was begun at 09:17, never finished, and forgotten at 14:02 with
nothing said to anybody. An afternoon that stops without ending is the failure this whole
project exists to make impossible, so :func:`conclude_what_is_over` now plays the way out
of wherever the afternoon got to and then its ending, and deletes the run afterwards. The
trigger is arithmetic on a clock — thirty minutes before the end hour — and no model is
asked whether it is time.

Three things this does not do, each of them a rule rather than an omission.

* **Nothing waits for a person.** There is no timer that expects an answer, and stopping
  is not recorded as anything. The clock that brings the ending is about the hour, not
  about somebody being slow.
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
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devices import hands
from devices.ask_panel import PanelUnreachable, read_page
from devices.house import CannotRun, House, screen_in, the_sheet_layer_is_done
from devices.print_page import recall
from devices.scan_sheet import find_scanner, scan_page
from orchestrator.outgoing import Outgoing
from shared.experience import (
    ASK,
    HELP_LEVELS,
    Came,
    Close,
    Collect,
    Continuation,
    Experience,
    ExperienceError,
    Help,
    Moment,
    Weight,
    longest_at,
    moment_from_dict,
)
from shared.ids import SheetId, new_id
from shared.message import Message, Says
from shared.vision_contracts import WhatCameBack

# Asking for the rest of an afternoon is a model writing several moments, which takes
# longer than wording one sentence and is still something a person may be standing in
# front of. Chosen, not measured.
ASK_TIMEOUT_SECONDS = 120

# How long before the end hour the ending begins, whatever the afternoon had reached. The
# design's number. What it has to cover is the longest way out a document may carry —
# twenty minutes, refused above that by the format — plus the ten minutes the house's own
# timer may take to notice. So an ending that starts as late as T-20 still has its twenty
# minutes, and the close lands on the hour rather than after it.
ENDING_STARTS_AT_MINUTES = 30


@dataclass(frozen=True, slots=True)
class Afternoon:
    """One run, as much of it as the house has to remember between two moments.

    It holds the whole experience rather than its id, for the reason ``resume`` gives in
    the blueprint runner: the house runs what it started. A document edited while a sheet
    was on the table would otherwise send the second half of one afternoon after the first
    half of another.

    ``segment`` is the moments currently being played. It is empty until an outcome says
    ``ask``; from then on it is the continuation that came back, and the experience's own
    moments are out of reach. That is what makes a continuation self-contained: its
    branches name its own moments, so an id it shares with the approved document is a
    coincidence rather than a jump.

    **Where the line is between a record and a verdict**, because format 2 put more in
    here than format 1 had. What this file holds is what is happening now: which moment,
    which weight, which sheets have already come out of the printer, whether the ending has
    begun. Every one of those is a fact about an afternoon, and every one of them is
    deleted when the afternoon ends. What may never appear is a number about a person that
    outlives the session — "took the short weight again" is a verdict, and there is nowhere
    here for it to be written.
    """

    run_id: str
    experience: Experience
    started_at: float
    # The collect this run stopped at. A run is never stored anywhere else: an afternoon
    # between two moments that do not touch paper has nothing to wait for.
    waiting_at: str
    segment: tuple[Moment, ...] = ()
    weight: Weight = Weight.STANDARD
    # Which sheets this run has already put on the table. Reprinting one is the failure
    # `ideas/09 §6` names: restart from nothing at 16:40, print sheet three again, and the
    # thing the person was inside of breaks.
    printed: tuple[str, ...] = ()
    # The moment whose way out is being taken. Non-empty means the ending has begun and
    # the only thing left is the close.
    leaving_at: str = ""
    left_at: float = 0.0
    # When the afternoon arrived at the moment it is waiting at, and how many rungs of that
    # moment's ladder have been given. Both are about this moment and are reset by the next
    # one, which is what keeps them a fact about an afternoon rather than a tally about a
    # person: there is nowhere here to write how much help an afternoon needed in total,
    # and `waited_at` is discarded with the run.
    waited_since: float = 0.0
    helped: int = 0
    # When this afternoon is over. It starts as the length the document declares and the
    # parent may move it, which is why it is kept rather than computed: `ideas/09 §6` calls
    # the current end hour one of the things a runner must be able to rebuild from, and an
    # hour derived from `started_at` cannot be moved without lying about when it began.
    over_at: float = 0.0

    @property
    def moments(self) -> tuple[Moment, ...]:
        return self.segment or self.experience.moments

    @property
    def ending_starts_at(self) -> float:
        """When the ending begins whatever has happened. Arithmetic, not a decision."""
        return self.over_at - ENDING_STARTS_AT_MINUTES * 60.0

    def closing_due_at(self) -> float:
        """When the close follows a way out that is already in play.

        The way out's own minutes, or the end hour, whichever comes first. An ending that
        arrives after the hour the parent chose is not an ending that arrived.
        """
        out = self.moment(self.leaving_at).way_out
        return min(self.left_at + out.minutes * 60.0, self.over_at)

    def moment(self, moment_id: str) -> Moment:
        for moment in self.moments:
            if moment.id == moment_id:
                return moment
        raise CannotRun(f"there is no moment called {moment_id!r} in this afternoon")

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "waiting_at": self.waiting_at,
            "experience": self.experience.to_dict(),
            "segment": [moment.to_dict() for moment in self.segment],
            "weight": str(self.weight),
            "printed": list(self.printed),
            "leaving_at": self.leaving_at,
            "left_at": self.left_at,
            "waited_since": self.waited_since,
            "helped": self.helped,
            "over_at": self.over_at,
        }

    @staticmethod
    def from_dict(values: Any) -> Afternoon:
        began = float(values["started_at"])
        experience = Experience.from_dict(values["experience"])
        return Afternoon(
            run_id=str(values["run_id"]),
            experience=experience,
            started_at=began,
            waiting_at=str(values["waiting_at"]),
            segment=tuple(moment_from_dict(m) for m in values.get("segment", [])),
            weight=Weight(str(values.get("weight", Weight.STANDARD))),
            printed=tuple(str(sheet) for sheet in values.get("printed", [])),
            leaving_at=str(values.get("leaving_at", "")),
            left_at=float(values.get("left_at", 0.0)),
            # A run written before the ladder existed counts from when the afternoon began,
            # which is the best answer available. Not a falsy sentinel: zero is a real
            # instant, and treating it as "absent" is how a ladder silently never arrives.
            waited_since=float(values.get("waited_since", began)),
            helped=int(values.get("helped", 0)),
            over_at=float(values.get("over_at", began + experience.minutes * 60.0)),
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


def _forget(sheets_dir: Path, run: Afternoon, sheets: list[str]) -> None:
    """An afternoon that ended leaves nothing behind, not even that it happened."""
    from devices.print_page import blank_path

    _run_file(sheets_dir, run.run_id).unlink(missing_ok=True)
    for sheet_id in (*run.printed, *sheets):
        _page_file(sheets_dir, sheet_id).unlink(missing_ok=True)
        blank_path(sheets_dir, SheetId(sheet_id)).unlink(missing_ok=True)


def waiting_runs(sheets_dir: Path) -> list[str]:
    """Every afternoon this house has begun and not finished.

    One at a time is the rule the caller applies, and it is a rule about the house rather
    than about a person: two sheets on the table from two different afternoons is a house
    that has stopped making sense, not a person doing too much.
    """
    return sorted(path.stem for path in sorted(_runs(sheets_dir).glob("*.json")))


def _read_run(path: Path) -> Afternoon | None:
    try:
        return Afternoon.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, ExperienceError):
        return None


def conclude_what_is_over(house: House, now: float, *, send: bool = True) -> list[str]:
    """Bring every afternoon whose hour has come to its ending, and then forget it.

    This replaced ``forget_what_is_over`` on 23 August 2026, and the two are not variants
    of each other. The old one deleted a run whose hours had passed and said nothing to
    anybody — measured doing exactly that on the house, to `aft_5ec79e85`, at 14:02 on 21
    August. Deleting an afternoon is the one thing a system like this may not do: an
    afternoon that stops without ending is the failure the rules call impossible.

    Two steps, one per run of the house's timer, because a way out is something somebody
    does rather than something a display finishes saying.

    1. At thirty minutes before the end hour, the way out of wherever the afternoon got to
       goes on the display. Nothing announces it, nothing apologises for it, and nothing
       says the afternoon was shortened.
    2. When that way out's own minutes are up — or the end hour arrives, whichever is
       first — the ending goes on the display and the run is deleted.

    A run whose file cannot be read is deleted without an ending, because there is no
    document left to reach one through. That is the only path here that still forgets.
    """
    ended: list[str] = []
    for path in sorted(_runs(house.sheets_dir).glob("*.json")):
        run = _read_run(path)
        if run is None:
            path.unlink(missing_ok=True)
            ended.append(path.stem)
            continue
        if run.leaving_at:
            if now < run.closing_due_at():
                continue
            _close_it(house, run, send=send)
            _forget(house.sheets_dir, run, [])
            ended.append(run.run_id)
            continue
        if now < run.ending_starts_at:
            continue
        leaving = _take_the_way_out(house, run, now)
        if leaving is None:
            _forget(house.sheets_dir, run, [])
            ended.append(run.run_id)
            continue
        _write(_run_file(house.sheets_dir, run.run_id), leaving.to_dict())
    if ended:
        # Whatever the afternoon last put on a display now has an ending of its own.
        # Without this the sheet layer outranks the picture for as long as the display is
        # on the wall, which on the house was measured at two days.
        the_sheet_layer_is_done(house, now)
    _forget_orphan_pages(house.sheets_dir)
    return ended


def _forget_orphan_pages(sheets_dir: Path) -> None:
    """Notes pointing at a run that is gone. A sheet whose afternoon ended is just paper."""
    still_here = set(waiting_runs(sheets_dir))
    for note in sorted((_runs(sheets_dir) / "pages").glob("*.json")):
        try:
            run_id = str(json.loads(note.read_text(encoding="utf-8"))["run_id"])
        except (OSError, ValueError, KeyError):
            note.unlink(missing_ok=True)
            continue
        if run_id not in still_here:
            note.unlink(missing_ok=True)


# ── What the parent said ─────────────────────────────────────────────────────────────


def hear(house: House, said: Sequence[Message], now: float) -> list[str]:
    """Apply what a parent said to every afternoon under way. Returns what changed.

    `ideas/09 §8`. Two things move an end hour and nothing else moves anything: the list in
    :class:`~shared.message.Says` is short because everything on it has to be applicable at
    a seam, and these two are applicable anywhere because they change a number the ending
    already reads.

    **Applied at once, and felt at the end of the moment.** `§8` says a message is applied at
    the end of the current moment and never in the middle of an instruction. That holds here
    without any waiting, because moving the end hour changes nothing a person can see: what
    it changes is when :func:`conclude_what_is_over` next decides the ending is due, and that
    is checked at moment boundaries and by the clock. Nothing is redrawn, nothing is
    interrupted, and there is nothing to notice.

    **Nothing says a message arrived.** No acknowledgement on the display, no change of tone,
    no apology. `§8` is explicit that a text revealing the channel exists is the one thing
    this must not produce, and the way to be sure is that this function draws nothing at all.

    A message about an afternoon that has already begun its ending is ignored: the way out is
    in somebody's hands, and moving the hour under it would either cut it short or leave it
    hanging. That is the one place where "at a seam" bites.
    """
    changed: list[str] = []
    for path in sorted(_runs(house.sheets_dir).glob("*.json")):
        run = _read_run(path)
        if run is None or run.leaving_at:
            continue
        moved = run
        for message in said:
            moved = _apply(moved, message, now)
        if moved.over_at == run.over_at:
            continue
        _write(_run_file(house.sheets_dir, run.run_id), moved.to_dict())
        changed.append(f"{run.run_id} is now over at {_clock(moved.over_at)}")
    return changed


def _apply(run: Afternoon, message: Message, now: float) -> Afternoon:
    if message.says is Says.CLOSE_NOW:
        # The ending is brought forward to this instant rather than the afternoon being
        # stopped. Reusing the one path to an ending is the point: there is no second way
        # to finish, so there is no second way to finish badly.
        return _over_at(run, now + ENDING_STARTS_AT_MINUTES * 60.0)
    if message.says is Says.END_BY:
        return _over_at(run, _today_at(message.minutes, now))
    return run


def _today_at(minutes_past_midnight: int, now: float) -> float:
    """An hour on the clock as an instant, on the day the afternoon is happening.

    Local midnight is recomputed rather than derived from ``now`` by arithmetic, because a
    day is not always 86 400 seconds long and an afternoon that ends an hour early on the
    last Sunday of October is a bug nobody would look for.
    """
    today = time.localtime(now)
    midnight = time.mktime((today.tm_year, today.tm_mon, today.tm_mday, 0, 0, 0, 0, 0, -1))
    return midnight + minutes_past_midnight * 60.0


def _clock(instant: float) -> str:
    return time.strftime("%H:%M", time.localtime(instant))


def _over_at(run: Afternoon, when: float) -> Afternoon:
    return Afternoon(
        run_id=run.run_id,
        experience=run.experience,
        started_at=run.started_at,
        waiting_at=run.waiting_at,
        segment=run.segment,
        weight=run.weight,
        printed=run.printed,
        leaving_at=run.leaving_at,
        left_at=run.left_at,
        waited_since=run.waited_since,
        helped=run.helped,
        over_at=when,
    )


# ── Help ─────────────────────────────────────────────────────────────────────────────


def offer_help(house: House, now: float, *, send: bool = True) -> list[str]:
    """Put the next rung of the ladder on the display, for every afternoon whose is due.

    `ideas/09 §4`. Four rungs, written into every moment, checked before the document was
    saved, read by the parent — and until now nothing could reach them. A third of what a
    model writes was going nowhere.

    ``after_minutes`` is counted from arriving at the moment and not from the rung before,
    which is why the format refuses a ladder that does not go up: 3, 6, 10, 15 means a nudge
    at three minutes and the answer at fifteen, not at thirty-four.

    **Two lines this deliberately does not cross.**

    *After the last rung, nothing.* `ideas/09 §4` says the moment is over and the afternoon
    moves on. Here the only moment an afternoon can be waiting at is a ``collect``, so moving
    on would mean ending the afternoon because nobody had come back — an action triggered by
    silence, which is the shape the working rules forbid. The ending stays where it is: the
    clock at T-30, which is about the hour and not about the person. So there is no fifth
    rung and no ending here.

    *Nothing says that time passed.* The rung is the same text somebody would have been given
    for asking, which is `§4`'s own rule, and it can only be that if it never mentions
    waiting. Nothing here adds a word to it.

    Asking for help is not built. When it is, it calls this with the rung it wants, and the
    text is the same text — the decision left open in `§17` is which surface the asking lands
    on, not what it says.
    """
    given: list[str] = []
    for path in sorted(_runs(house.sheets_dir).glob("*.json")):
        run = _read_run(path)
        if run is None or run.leaving_at:
            # An afternoon on its way to the ending is not stuck; it is finishing.
            continue
        helped = _next_rung(run, now)
        if helped is None:
            continue
        rung, at = helped
        out = Outgoing()
        hands.say(house, at.heading, list(out.lines(f"{at.id}.help{run.helped + 1}", rung.lines,
                                               written=rung.lines)))
        _say_the_tally(out)
        _write(_run_file(house.sheets_dir, run.run_id), _one_rung_on(run).to_dict())
        given.append(f"{run.run_id} {at.id} rung {run.helped + 1}")
        del send  # a rung is words on a display; nothing is printed and nothing is sent
    return given


def _next_rung(run: Afternoon, now: float) -> tuple[Help, Moment] | None:
    """The rung that has come due and not been given, or None."""
    if run.helped >= HELP_LEVELS:
        return None
    try:
        at = run.moment(run.waiting_at)
    except CannotRun:
        return None
    rung = at.help[run.helped]
    if now - run.waited_since < rung.after_minutes * 60.0:
        return None
    return rung, at


def _one_rung_on(run: Afternoon) -> Afternoon:
    return Afternoon(
        run_id=run.run_id,
        experience=run.experience,
        started_at=run.started_at,
        waiting_at=run.waiting_at,
        segment=run.segment,
        weight=run.weight,
        printed=run.printed,
        leaving_at=run.leaving_at,
        left_at=run.left_at,
        waited_since=run.waited_since,
        helped=run.helped + 1,
        over_at=run.over_at,
    )


def _take_the_way_out(house: House, run: Afternoon, now: float) -> Afternoon | None:
    """Put the way out of wherever this afternoon got to on the display.

    None means there was nothing to leave from — a run pointing at a moment its own
    document no longer has, which is a broken record rather than an afternoon.
    """
    try:
        at = run.moment(run.waiting_at)
    except CannotRun:
        return None
    out = at.way_out
    hands.say(house, out.heading, list(out.lines))
    return Afternoon(
        run_id=run.run_id,
        experience=run.experience,
        started_at=run.started_at,
        waiting_at=run.waiting_at,
        segment=run.segment,
        weight=run.weight,
        printed=run.printed,
        leaving_at=at.id,
        left_at=now,
        waited_since=run.waited_since,
        helped=run.helped,
        over_at=run.over_at,
    )


def _close_it(house: House, run: Afternoon, *, send: bool = True) -> None:
    """The ending, reached early, which is the same ending.

    It says nothing about what was not seen. `ideas/09 §3` is the whole argument for that
    and it is one sentence: an ending that refers to what was skipped tells the person
    something was taken away from them.
    """
    ending = _the_ending(run.moments)
    if ending is None:
        return
    _do(house, ending, run.weight, send=send)


def _the_ending(moments: tuple[Moment, ...]) -> Close | None:
    """The close this afternoon was always going to reach.

    The last one in the list when there are several: the branches that close earlier are
    kinder endings for shorter paths, and the one at the end is the afternoon's own.
    """
    closes = [moment for moment in moments if isinstance(moment, Close)]
    return closes[-1] if closes else None


# ── Playing ──────────────────────────────────────────────────────────────────────────


def _do(
    house: House,
    moment: Moment,
    weight: Weight,
    *,
    send: bool,
    out: Outgoing | None = None,
) -> str | None:
    """Play one moment at one weight. Returns the id of the sheet it printed, if it did.

    The verb is looked up rather than branched on: what each one does lives in
    :mod:`devices.hands`, one function per device, so this stays the same length however
    many devices a house grows.
    """
    return hands.play(house, moment, weight, out or Outgoing(), send)


def _weight_for(moments: tuple[Moment, ...], start: int, minutes_left: float) -> Weight:
    """Which of the three versions to run from here, so that the ending still fits.

    In code, not in a model. `ideas/09 §5` gives the order — everything to its short
    weight, then optional moments dropped, then merges, then the way out — and this is the
    first of the four, which is the one that costs nothing and is always available. The
    others are not built; the way out is, and it is what the clock reaches for at T-30.

    Standard unless standard does not fit. Extended is never chosen here: choosing to make
    an afternoon longer because there is room is a decision about what somebody wants, and
    the runner does not know that.
    """
    if longest_at(moments, Weight.STANDARD, start=start) * 60.0 <= minutes_left:
        return Weight.STANDARD
    return Weight.SHORT


def _play(
    house: House,
    run: Afternoon,
    start: int,
    *,
    now: float,
    send: bool,
    out: Outgoing | None = None,
) -> tuple[Collect | None, list[str], Weight]:
    """Run moments forward from ``start`` until a page has to come back, or it closes.

    Returns the ``collect`` it stopped at — or None, meaning the afternoon is over — every
    sheet it put on the table on the way, and the weight it ran at.
    """
    moments = run.moments
    weight = _weight_for(moments, start, run.over_at - now)
    printed: list[str] = []
    for moment in moments[start:]:
        if isinstance(moment, Collect):
            return moment, printed, weight
        sheet_id = _do(house, moment, weight, send=send, out=out)
        if sheet_id is not None:
            printed.append(sheet_id)
        if isinstance(moment, Close):
            return None, printed, weight
    # `_check_graph` refuses a document that could reach here, so this is a bug rather
    # than a badly written afternoon.
    raise CannotRun("the afternoon ran off the end of its moments")


def _pause(
    house: House,
    run: Afternoon,
    at: Collect,
    printed: list[str],
    weight: Weight,
    now: float,
) -> None:
    """Write down where the afternoon got to, and which paper points back at it.

    Arriving at a moment resets its ladder. A rung given at the moment before has nothing to
    do with this one, and carrying the count forward would be the beginning of a tally.
    """
    waiting = Afternoon(
        run_id=run.run_id,
        experience=run.experience,
        started_at=run.started_at,
        waiting_at=at.id,
        segment=run.segment,
        weight=weight,
        printed=(*run.printed, *printed),
        waited_since=now,
        over_at=run.over_at,
    )
    _write(_run_file(house.sheets_dir, run.run_id), waiting.to_dict())
    for sheet_id in printed:
        _write(_page_file(house.sheets_dir, sheet_id), {"run_id": run.run_id})


def begin(
    house: House, experience: Experience, *, now: float | None = None, send: bool = True
) -> str | None:
    """Play an afternoon up to its first page. Returns the run id, if it is waiting for one.

    None means it closed without ever needing paper back, and nothing was written down.
    """
    if not experience.runnable_in(house.capabilities):
        raise CannotRun(f"this house cannot run {experience.title}")
    moment = time.time() if now is None else now
    run = Afternoon(
        run_id=new_id("aft"),
        experience=experience,
        started_at=moment,
        waiting_at="",
        over_at=moment + experience.minutes * 60.0,
    )
    out = Outgoing()
    at, printed, weight = _play(house, run, 0, now=moment, send=send, out=out)
    _say_the_tally(out)
    if at is None:
        return None
    _pause(house, run, at, printed, weight, moment)
    return run.run_id


def _say_the_tally(out: Outgoing) -> None:
    """The refusal counts, to the journal and nowhere else."""
    tally = out.tally()
    if tally:
        print(tally)


def came_back(came: WhatCameBack) -> Came | None:
    """Which of the two words describes this page, or None if neither honestly does.

    A reading the model could not make — ``degraded`` — is not "blank". Blank is a branch
    somebody wrote, usually the one that closes the afternoon kindly, and taking it because
    the reading failed would be closing an afternoon on a page that was filled in. So the
    run stops instead, which is what it does when the panel cannot be reached: the page
    stays where it is and nothing is said about it.

    A sheet that is not the one that was handed over is still read, and still answers. That
    is `ideas/10 §3`: somebody putting back an earlier page has not erred, and there is
    nothing here that may refuse a person's paper.
    """
    if came.degraded:
        return None
    return Came.MARKS if came.written else Came.BLANK


def _read(house: House, run: Afternoon | None = None) -> tuple[str, WhatCameBack]:
    """Read whatever is on the glass, against the blank this house kept.

    Which sheet it is comes from the house's own expectation — the last one it handed out
    — and not from anything printed on the paper. `ideas/10 §3` chose that way round on
    purpose: the page is the evidence and the expectation is only the tie-break, and the
    model says in the same breath whether this looks like the sheet it was given.

    The one branch a pretend house needs, and it is here rather than further up because
    this is where the scanner is. What changes is where the pixels come from; what does not
    change is that a vision model in the cloud is what reads them.
    """
    from devices.print_page import waiting

    pretending = house.pretending
    if pretending is not None:
        from devices import pretend as simulated

        try:
            sheet_id, came_off = simulated.off_the_glass(pretending, house)
        except LookupError as exc:
            raise CannotRun(str(exc)) from exc
    else:
        if not house.scanner:
            raise CannotRun("there is no scanner in this house")
        came_off = scan_page(find_scanner(house.scanner))
        handed_out = waiting(house.sheets_dir)
        if not handed_out:
            raise CannotRun("this house is not waiting for a page")
        sheet_id = str(handed_out[-1])
    blank = recall(house.sheets_dir, SheetId(sheet_id))
    about = run.experience.title if run is not None else ""
    try:
        came = read_page(
            blank,
            came_off,
            about=about,
            panel=house.panel,
            household=house.household,
            key=house.device_key,
        )
    except PanelUnreachable as exc:
        raise CannotRun(f"the page was not read: {exc}") from exc
    return sheet_id, came


def _ask(
    house: House, run: Afternoon, at: Collect, came: Came, reading: WhatCameBack
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
    sheet_id, reading = _read(house)
    pointer = _page_file(house.sheets_dir, sheet_id)
    if not pointer.is_file():
        raise CannotRun(f"sheet {sheet_id} does not belong to an afternoon this house started")
    run_id = str(json.loads(pointer.read_text(encoding="utf-8"))["run_id"])
    run_path = _run_file(house.sheets_dir, run_id)
    if not run_path.is_file():
        # The afternoon ended and took its own file with it; this is the paper catching up.
        pointer.unlink(missing_ok=True)
        raise CannotRun("that afternoon is already over")
    run = Afternoon.from_dict(json.loads(run_path.read_text(encoding="utf-8")))

    if run.leaving_at:
        # The ending is already on the display. A page arriving now is not late for
        # anything: it is read, and the afternoon finishes where it was always going to.
        return "that afternoon is finishing"

    if moment >= run.ending_starts_at:
        # The hour, not the person. Nothing here says the afternoon was shortened, and the
        # ending this reaches is the same ending it would have reached the long way.
        leaving = _take_the_way_out(house, run, moment)
        if leaving is None:
            _forget(house.sheets_dir, run, [sheet_id])
            return "that afternoon is over"
        _write(_run_file(house.sheets_dir, run.run_id), leaving.to_dict())
        return "that afternoon is on its way to the ending"

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
            weight=run.weight,
            printed=run.printed,
            over_at=run.over_at,
        )
        start = 0
    else:
        start = _index_of(run, then)

    out = Outgoing()
    following, printed, weight = _play(house, run, start, now=moment, send=send, out=out)
    _say_the_tally(out)
    if following is None:
        _forget(house.sheets_dir, run, [sheet_id, *printed])
        return "the afternoon is finished"
    _pause(house, run, following, printed, weight, moment)
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
