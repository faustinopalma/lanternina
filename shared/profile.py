"""Where an afternoon should be pitched for this house, and what that is worked out from.

`docs/NON-GOALS.md`, 4 September 2026. Until then the rule was that nothing about a person
was kept anywhere and that this was a fact of the types. It was withdrawn because an
afternoon written without any idea of the level it should be pitched at is an afternoon
pitched at nobody, and every mechanism the system had for calibrating — a parent's one-off
setting, a list of subjects already covered — was a proxy for the thing it was refusing to
hold.

**The roles are split, and the split is the design rather than a tidiness.** One model reads
one page and says what it sees, knowing nothing about the house, nothing about the profile
and nothing about any other afternoon: :class:`Noticed` is what it answers, and a model with
no history in front of it cannot confirm a history. Those answers accumulate into a series.
This module is the second half — arithmetic over that series, with no model in it, which is
what makes the state readable, testable and wrong in ways somebody can point at.

**It is never called a score and it is not one.** A score ranks somebody. What is here is a
position on three axes, each of which names something an afternoon can be written
differently for, and which exists only because it changes what gets written. An axis that
would not change a sentence in the prompt has no business being an axis.

**Where it may appear.** In the prompt of the model that devises an afternoon and the model
that runs one. Nowhere else: no display, no printed sheet, no page in the parent's panel.
:mod:`shared.blocklist` is what stops it surfacing in what a person reads, and
`tests/test_boundaries.py` is what stops it reaching the browser.

**The window is what damps it, and there is no other smoothing.** The state is recomputed
from the last :data:`WEIGHED` notices every time it is asked for, so one page moves an axis
by at most ``1/n`` of the scale and nothing is carried over from the last computation. That
is cheaper than hysteresis and it can be checked by hand, which hysteresis cannot.

**A sheet that never came back is evidence too, and it is the one that needs a guard.** It
may mean what was asked was too much; it may equally mean the scanner is in another room or
broken, and nothing here can tell those apart. So a sheet that did not come back counts only
in a house that has had at least one come back — otherwise a house with a dead scanner is
walked down to the bottom of every axis and nobody would know why.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Final


class Axis(StrEnum):
    """The three things an afternoon is pitched along. Closed, because a name invented once
    cannot be compared with the same name meant differently a month later."""

    #: How many things have to be held together at once before the afternoon makes sense.
    LOAD = "load"
    #: How much a sheet asks somebody to put on it, from a mark to a page of writing.
    INK = "ink"
    #: How long the afternoon runs before it wants to be over.
    SPAN = "span"


# What a page may be placed at. Five rather than three because the model placing it
# discriminates better than the bands do, and three is what survives averaging.
LOWEST: Final = 1
HIGHEST: Final = 5

# The last few sheets and the last few afternoons the state is read off. Eight matches
# `panel/what_happened.RECENT`, so the prompt's history and the prompt's pitch are drawn
# from the same stretch of time rather than from two different ones.
WEIGHED: Final = 8

# Below this many placements an axis says nothing at all. Two afternoons that went badly are
# a fortnight, not a level, and the deviser writes better with no sentence than with a wrong
# one — which is `panel/what_happened.ENOUGH_TO_LEAN_ON`, kept at the same number.
ENOUGH_TO_LEAN_ON: Final = 3

# The 1–5 scale cut into three equal parts. Stated as arithmetic rather than as chosen
# numbers so that changing the scale moves the bands with it.
_LOW_ABOVE: Final = LOWEST + (HIGHEST - LOWEST) / 3.0
_HIGH_ABOVE: Final = LOWEST + 2.0 * (HIGHEST - LOWEST) / 3.0


class Band(StrEnum):
    LOW = "low"
    MIDDLE = "middle"
    HIGH = "high"


def band_of(value: float) -> Band:
    if value < _LOW_ABOVE:
        return Band.LOW
    if value <= _HIGH_ABOVE:
        return Band.MIDDLE
    return Band.HIGH


# What each band asks for, in the register the deviser is already written in: a property of
# the afternoon, never a remark about the person it is for. The three `load` sentences are
# the ones that were `SHAPES` in `agents/experience_deviser.py` until 4 September 2026, when
# a parent stopped being asked to choose between them; they are kept word for word because
# they are the only text here that has ever been in front of the real service.
PITCHES: Final[dict[Axis, dict[Band, str]]] = {
    Axis.LOAD: {
        Band.LOW: (
            "one thing that is wrong and one thing to find out, told plainly; nothing "
            "that has to be matched against something from an hour ago"
        ),
        Band.MIDDLE: (
            "two things that have to be put side by side before either makes sense, and "
            "one turn where what looked true stops being true"
        ),
        Band.HIGH: (
            "three things to relate, and something that only resolves once all three are "
            "in hand — still one question, and every step still clear on its own"
        ),
    },
    Axis.INK: {
        Band.LOW: (
            "what a sheet asks for is something to mark, place, cut or draw rather than "
            "something to write out; a page that comes back with a few marks on it has "
            "been used properly and should be designed so that it has"
        ),
        Band.MIDDLE: (
            "a sheet may ask for a few words as well as marks, and the space left for "
            "them should be small enough that filling it is obviously finishable"
        ),
        Band.HIGH: (
            "a sheet may ask for writing at length, and for a page to be filled rather "
            "than ticked; leave room for somebody who will use all of it"
        ),
    },
    Axis.SPAN: {
        Band.LOW: (
            "write the standard weight towards the short end of its window, and keep the "
            "way out within easy reach of every moment"
        ),
        Band.MIDDLE: "write the standard weight at the middle of its window",
        Band.HIGH: (
            "the standard weight may run to the long end of its window, and a late "
            "moment may be the one the whole afternoon was for"
        ),
    },
}


@dataclass(frozen=True, slots=True)
class Noticed:
    """One sheet, as one model saw it, or as the absence of one.

    ``where`` is empty in two cases and they are not the same. A sheet that never came back
    has ``came_back`` false and is read as the bottom of :attr:`Axis.INK` under the guard in
    :func:`read_from`. A sheet that came back and could not be placed — the model refused,
    the cloud was down — has ``came_back`` true and an empty ``where``, and it counts
    towards nothing.

    ``says`` is one line from the model about what it saw on the paper. It is here so that a
    placement can be argued with by whoever is doing the prompt work, and it goes into no
    prompt: a sentence about one page, handed to the model writing the next afternoon, is
    the reading of a person arriving by the back door.
    """

    at: float
    came_back: bool = True
    where: dict[Axis, int] = field(default_factory=dict)
    says: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "at": self.at,
            "cameBack": self.came_back,
            "where": {str(axis): value for axis, value in self.where.items()},
            "says": self.says,
        }

    @staticmethod
    def from_dict(values: Any) -> Noticed:
        raw = values.get("where") or {}
        return Noticed(
            at=float(values.get("at") or 0.0),
            came_back=bool(values.get("cameBack", True)),
            where={
                Axis(name): _in_range(raw[name])
                for name in raw
                if name in set(Axis) and _is_a_number(raw[name])
            },
            says=str(values.get("says") or ""),
        )


@dataclass(frozen=True, slots=True)
class Ran:
    """One afternoon's own numbers, which is all :attr:`Axis.SPAN` is read off.

    No page shows how long somebody sat, so this axis has no model in it at all. It is the
    minutes the plan asked for against the minutes the house reported, and whether the
    afternoon reached its own ending or was brought to one.
    """

    planned_minutes: int
    minutes: int
    carried_through: bool


@dataclass(frozen=True, slots=True)
class Profile:
    """Where this house sits on each axis now, and how much was behind each answer.

    ``seen`` is beside ``where`` rather than under it because a caller that wants to say
    *this is thin* needs the denominator, and a state that hides its denominator is the
    shape a score has.
    """

    where: dict[Axis, Band] = field(default_factory=dict)
    seen: dict[Axis, int] = field(default_factory=dict)

    def knows_anything(self) -> bool:
        return bool(self.where)

    def as_material(self) -> str:
        """The pitch, as sentences about the afternoon. Empty when nothing is known yet.

        Empty is a real answer and not a failure: a house with no history gets a prompt with
        no pitch block in it, and the deviser invents freely, which is what it did for the
        whole of August.
        """
        return "\n".join(
            PITCHES[axis][self.where[axis]] for axis in Axis if axis in self.where
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "where": {str(axis): str(band) for axis, band in self.where.items()},
            "seen": {str(axis): count for axis, count in self.seen.items()},
        }


def _is_a_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _in_range(value: Any) -> int:
    return max(LOWEST, min(HIGHEST, int(round(float(value)))))


def _placed(notices: Sequence[Noticed], axis: Axis) -> list[int]:
    """Every placement on this axis in the window, with the missing-sheet rule applied.

    A sheet that did not come back reads as the bottom of :attr:`Axis.INK` and says nothing
    about the other two: a page nobody put on the glass cannot show how many things had to
    be held at once. And it is dropped altogether in a house that has never had a sheet come
    back, because there the likeliest reading is a scanner and not a person.
    """
    lately = list(notices)[-WEIGHED:]
    ever_came_back = any(one.came_back for one in lately)
    values: list[int] = []
    for one in lately:
        if one.came_back:
            if axis in one.where:
                values.append(one.where[axis])
        elif axis is Axis.INK and ever_came_back:
            values.append(LOWEST)
    return values


def _span_of(runs: Sequence[Ran]) -> list[int]:
    """Each afternoon placed on the span axis from its own two numbers and its ending.

    The fraction of the planned minutes that were actually spent, mapped onto the same 1–5
    scale everything else uses so that one set of bands serves all three axes. An afternoon
    that ran its whole length and reached its own ending is at the top; one that stopped a
    third of the way through is at the bottom.
    """
    values: list[int] = []
    for one in list(runs)[-WEIGHED:]:
        if one.planned_minutes <= 0 or one.minutes <= 0:
            continue
        far = min(1.0, one.minutes / one.planned_minutes)
        if not one.carried_through:
            # Brought to an end rather than reaching one. The minutes were still spent, so
            # this is a step down and not a floor: an afternoon that ran two hours and was
            # ended by the clock is not the same as one abandoned after twenty minutes.
            far *= 0.75
        values.append(_in_range(LOWEST + far * (HIGHEST - LOWEST)))
    return values


def read_from(notices: Sequence[Noticed] = (), runs: Sequence[Ran] = ()) -> Profile:
    """The state now, from the series and the afternoons. No model, no memory, no state.

    Called every time a prompt is built rather than stored and updated, so there is one
    place a wrong answer can come from and it is this function.
    """
    where: dict[Axis, Band] = {}
    seen: dict[Axis, int] = {}
    for axis in Axis:
        values = _span_of(runs) if axis is Axis.SPAN else _placed(notices, axis)
        seen[axis] = len(values)
        if len(values) >= ENOUGH_TO_LEAN_ON:
            where[axis] = band_of(sum(values) / len(values))
    return Profile(where=where, seen=seen)
