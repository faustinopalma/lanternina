"""Play one afternoon with nobody in the room, and write down what happened.

A headless `devices/run_experience.py`. It walks the moments the way the house does — pick
a weight on entering, say the lines, hand over a page as the words that would be printed,
stop at a `collect` and ask the simulation what came back, take the branch — and it stops
where the house would stop.

**Two things it does not do, and both are deliberate.** No page is drawn: an image costs
about 25 s and four cents and this loop is about whether an afternoon works, not whether it
is pretty, so a sheet reaches the simulation as the words that would be lettered onto it.
And a branch that says ``ask`` ends the run rather than buying a continuation — the
continuer is a second prompt with its own failures, and mixing the two would make a score
that cannot say which one it is about. `research/README.md` names both as limits.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from shared.agents import AgentContext
from shared.experience import (
    ASK,
    Collect,
    Experience,
    HandOver,
    Moment,
    Say,
    Weight,
)

from .calls import what_they_did

# Where a run stopped. The same words `panel/what_happened.py` files, so a played afternoon
# can be written into the memory the next one is devised from.
CLOSED = "closed"
WAY_OUT = "way_out"
STOPPED = "stopped"
WENT_WRONG = "went_wrong"

# A guard against a document that loops through a branch we misread. The format forbids
# backwards outcomes, so reaching this is a defect and it is written into the transcript.
MOST_MOMENTS = 40


@dataclass
class Played:
    """One afternoon after it was played, and everything a score can be read from."""

    household: str
    title: str
    experience: dict[str, Any]
    weight: str
    ending: str = ""
    reached: str = ""
    minutes: int = 0
    displays: list[str] = field(default_factory=list)
    sheets: list[dict[str, Any]] = field(default_factory=list)
    trail: list[str] = field(default_factory=list)

    def transcript(self) -> str:
        """The afternoon as somebody who watched it would write it down."""
        return "\n".join(self.trail)


def _sheet_as_words(moment: HandOver) -> str:
    page = moment.page
    lines = [f"[{page.kind}] {page.title}", *page.note]
    lines += [f"— {one.label} ({one.room})" for one in page.spaces]
    return "\n".join(one for one in lines if one)


async def play(
    ctx: AgentContext,
    *,
    experience: Experience,
    household: str,
    weight: Weight,
    mood: str,
) -> Played:
    """Walk the moments until the afternoon ends, is stopped, or asks for a continuation."""
    played = Played(
        household=household,
        title=experience.title,
        experience=experience.to_dict(),
        weight=str(weight),
    )
    played.trail.append(f"TITOLO: {experience.title}")
    played.trail.append(f"COME VA LA GIORNATA: {mood}")
    played.trail.append(f"PESO SCELTO: {weight}")

    by_id = {one.id: one for one in experience.moments}
    order = list(experience.moments)
    index = 0
    steps = 0

    while index < len(order) and steps < MOST_MOMENTS:
        steps += 1
        moment: Moment = order[index]
        played.reached = moment.id
        weighing = moment.at(weight)
        played.minutes += weighing.minutes
        played.trail.append(f"\n[{moment.act}] {moment.heading}")
        for line in weighing.lines:
            played.trail.append(f"  display: {line}")
            played.displays.append(line)

        if isinstance(moment, Say):
            index += 1
            continue

        if isinstance(moment, HandOver):
            sheet = _sheet_as_words(moment)
            played.trail.append("  foglio consegnato:")
            played.trail += [f"    {one}" for one in sheet.splitlines()]
            played.sheets.append({"momentId": moment.id, "sheet": sheet})
            index += 1
            continue

        if isinstance(moment, Collect):
            waiting = next(
                (one for one in reversed(played.sheets) if "came" not in one), None
            )
            if waiting is None:
                played.trail.append("  DIFETTO: si raccoglie un foglio che non è uscito")
                played.ending = WENT_WRONG
                return played
            did = await what_they_did(
                ctx,
                displays=played.displays,
                sheet=waiting["sheet"],
                mood=mood,
                minutes_in=played.minutes,
            )
            came = "marks" if str(did.get("came")) == "marks" else "blank"
            waiting["came"] = came
            waiting["reading"] = str(did.get("onIt", ""))
            waiting["why"] = str(did.get("why", ""))
            played.trail.append(f"  il foglio torna: {came}")
            played.trail.append(f"    sul foglio: {waiting['reading']}")
            played.trail.append(f"    dice: {waiting['why']}")
            if did.get("stop"):
                played.trail.append("  ha smesso qui")
                played.trail.append(f"  via d'uscita: {moment.way_out.heading}")
                played.trail += [f"    display: {one}" for one in moment.way_out.lines]
                played.minutes += moment.way_out.minutes
                played.ending = STOPPED
                return played
            goes = next((one.then for one in moment.outcomes if str(one.when) == came), ASK)
            played.trail.append(f"  va a: {goes}")
            if goes == ASK:
                played.trail.append("  (qui il pomeriggio vero chiederebbe la continuazione)")
                played.ending = WAY_OUT
                return played
            if goes not in by_id:
                played.trail.append(f"  DIFETTO: {goes!r} non è un momento di questo pomeriggio")
                played.ending = WENT_WRONG
                return played
            index = order.index(by_id[goes])
            continue

        # A close. Nothing follows it.
        played.ending = CLOSED
        return played

    played.ending = played.ending or WENT_WRONG
    return played


def now() -> float:
    return time.time()
