"""The last thing every word passes before it reaches a display or a printer.

Beside :mod:`orchestrator.safety` and not inside it, because the two doors are looking for
different things and joining them would blur both. The safety gate asks whether a text is
harmful, over a network, with a model behind it. This asks whether a text is the kind of
thing this house says: short enough for the screen, free of praise, blame, hurry and
score, and silent about the machinery that produced it. It runs locally, in microseconds,
on the house, with nothing to be unavailable.

`ideas/09 §7` puts the same list at two times. Before an afternoon is saved,
:mod:`shared.experience_checks` runs it over every pre-written word and a document that
fails is repaired instead of stored. While the afternoon runs, this runs it over whatever
is actually about to be shown — which is the pre-written text most of the time, and a
model's sentence the rest of the time. **When a text is refused, the pre-written text from
the plan is used instead.** That fallback is the reason the written texts are mandatory in
the first place, and it is why nothing here can fail: there is always something to say.

**The counter is the point as much as the filter is.** Refusals are counted by slot, and a
slot that is refused often is a defect in the devising prompt rather than a case to handle
at run time. A filter nobody reads the numbers off is a filter that quietly hides a bad
prompt for months.

What the counter is not: it counts slots, which are places in a document. It does not
count afternoons, people, sessions or anything that outlives the run. The numbers go to
the journal when the run ends and nowhere else — there is no file, and nothing accumulates
across afternoons.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Final

from shared.blocklist import Blocked, blocked_in
from shared.experience import MAX_HEADING, MAX_LINE


@dataclass(frozen=True, slots=True)
class Refused:
    """Why one text did not go out. Kept as a value so the caller can log it plainly."""

    slot: str
    why: str

    def __str__(self) -> str:
        return f"{self.slot}: {self.why}"


def why_not(text: str, *, limit: int) -> str:
    """Why this text may not go out, or an empty string.

    Three reasons and no more, in the order they cost. Length is arithmetic. The block list
    is a regex over a folded string. Neither calls anything.
    """
    if not text.strip():
        return "it says nothing"
    if len(text) > limit:
        return f"it is {len(text)} characters and the limit is {limit}"
    found: tuple[Blocked, ...] = blocked_in(text)
    if found:
        return "it says " + ", ".join(str(entry) for entry in found)
    return ""


@dataclass(slots=True)
class Outgoing:
    """Every string on its way out of the house, and the tally of what did not make it.

    One of these lives for one afternoon. It holds no text — only how many times each slot
    was refused — so a run that ends leaves counts of places in a document behind, and
    nothing about what anybody read or wrote.
    """

    refusals: Counter[str] = field(default_factory=Counter)
    reasons: list[Refused] = field(default_factory=list)

    def line(self, slot: str, proposed: str, *, written: str) -> str:
        """One line for a display: the proposed one if it may go out, else the written one."""
        return self._pass(slot, proposed, written=written, limit=MAX_LINE)

    def heading(self, slot: str, proposed: str, *, written: str) -> str:
        return self._pass(slot, proposed, written=written, limit=MAX_HEADING)

    def lines(
        self, slot: str, proposed: tuple[str, ...], *, written: tuple[str, ...]
    ) -> tuple[str, ...]:
        """A screenful. Refused as one thing, because half a screenful is not a screenful.

        A line at a time would let a filter cut the middle of a paragraph and leave
        something that reads as if a sentence went missing — which is exactly the seam this
        whole design is trying not to show.
        """
        for index, text in enumerate(proposed):
            why = why_not(text, limit=MAX_LINE)
            if why:
                self._refuse(slot, f"line {index + 1} {why}")
                return written
        if not proposed:
            self._refuse(slot, "it says nothing")
            return written
        return proposed

    def _pass(self, slot: str, proposed: str, *, written: str, limit: int) -> str:
        why = why_not(proposed, limit=limit)
        if not why:
            return proposed
        self._refuse(slot, why)
        return written

    def _refuse(self, slot: str, why: str) -> None:
        self.refusals[slot] += 1
        self.reasons.append(Refused(slot=slot, why=why))

    def tally(self) -> str:
        """The line that goes in the journal when the afternoon ends, or nothing at all."""
        if not self.refusals:
            return ""
        worst = ", ".join(
            f"{slot} {count}" for slot, count in self.refusals.most_common(MOST_REPORTED)
        )
        return f"texts refused, by slot: {worst}"


# How many slots the journal line names. More than a handful is a wall of numbers nobody
# reads, and the tail is by definition the part that is not a defect in the prompt.
MOST_REPORTED: Final = 5
