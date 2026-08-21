"""What an experience is: a plan a machine runs, a page a parent reads to the end.

An experience is a thing to do across an afternoon. It is devised fresh — not chosen from
a list — for one house, from what that house has and what happened last time. It lands
partly on a display and partly on paper, it changes course on what comes back through the
glass, and it finishes.

It is not :mod:`shared.blueprint`, and the difference is the whole reason this module
exists. A blueprint is a flat sequence with no branch, on purpose: an experience that
would change course on what came back had to be two experiences or a person. That
restriction is what made the paper loop a worksheet — here is a task, do it, I will look
at it — and it is lifted here. What is not lifted is the property underneath it: **an
experience carries no code.**

Where the line falls now, said once so it can be argued with:

* **Branching, yes.** A ``collect`` moment names what may come back and where each answer
  leads. A parent reading the document reads every branch, because the branches are all
  written down.
* **Computation, no.** There is no expression, no variable, no arithmetic, no counter and
  no loop — the moments form a directed graph and a cycle is refused while the document is
  being read. The set of things an experience can express is the set of fields of the four
  moment types below.
* **What is not written down yet is asked for, and what comes back is more of this.** An
  outcome may say ``ask`` instead of naming a moment. Then the house sends up what came
  back and receives a :class:`Continuation` — further moments, over this same vocabulary,
  with an ending of their own. A model steers an afternoon without ever writing a program,
  because the only thing it can hand back is data this module parses.

Three absences carried over from the blueprint, all still load-bearing.

* **Nothing points a sensor at a person.** ``COLLECT`` reads the page this experience
  handed over, off a flatbed with the lid down. There is no parameter for what to frame,
  so there is nothing to set to "the room".
* **Nothing counts.** No field for how many afternoons, how far anybody got, how many
  moments were reached. An ending may be satisfying; nothing here exists to make the next
  one more likely, and the absence of the field is what keeps a counter from arriving
  later wearing a useful feature's coat.
* **Nothing waits.** No moment pauses for a person or asks again. An experience nobody
  continues stops, and stopping is not recorded as anything.

And one absence that is new. **There is nothing about a person in here at all** — no name,
no learner, no profile, not even a household. An experience is devised for a house by that
house's own agent, and it travels no further than the hub that asked for it.

What it costs. A parent approves this from its overview, at a general level, and not
moment by moment — so inside an approved experience, and behind an ``ask``, what reaches
the adolescent has not been seen by an adult. :mod:`orchestrator.safety` is then the only
thing between a model and a person, and it is doing more work than it was built for. That
is the trade, and it is recorded in `ideas/08 §2` rather than discovered here.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar, Final

from .capabilities import HouseCapability
from .pagedesign import DesignError, PageDesign

EXPERIENCE_FORMAT_VERSION: Final = 1


class Act(StrEnum):
    """Everything an experience can ask for. A fifth entry is a person editing this file."""

    SAY = "say"
    HAND_OVER = "hand_over"
    COLLECT = "collect"
    CLOSE = "close"


# What each act needs the house to be able to do. The document does not get to say: a
# moment that puts paper on the table needs a printer whatever its author wrote.
NEEDS: Final[Mapping[Act, HouseCapability]] = {
    Act.SAY: HouseCapability.SHOW_800X480_1BIT,
    Act.HAND_OVER: HouseCapability.PRINT_A4,
    Act.COLLECT: HouseCapability.SCAN_A4,
    Act.CLOSE: HouseCapability.SHOW_800X480_1BIT,
}


class Came(StrEnum):
    """What a page can have come back as. Two words, and both describe ink.

    Not three, and not a number. "Half of them" is a count of a person's marks one step
    away from being a score, and the reader's own vocabulary — marked, empty, unsure — has
    no way to produce it honestly anyway. Which boxes carry a mark is a richer question and
    it is not answered here: it is what ``ask`` carries upward.
    """

    MARKS = "marks"
    BLANK = "blank"


# What an outcome may say instead of naming a moment. ``ask`` means the rest of the
# afternoon is not written yet: the house sends up what came back and receives a
# continuation — more moments, in this same format, with their own ending.
ASK: Final = "ask"

# Text limits. The two display ones are measured: the notice renderer's fonts have 728 px
# of usable width, and 44 characters of ordinary Italian come to 681 px in the body font,
# 28 characters to about 697 px in the heading font. Longer text still renders — the
# renderer wraps — so these are the width at which a line stays a line. The rest are
# chosen, not measured.
MAX_HEADING: Final = 28
MAX_LINE: Final = 44
MAX_LINES: Final = 4
MAX_TITLE: Final = 60
MAX_OVERVIEW: Final = 600

# An afternoon, bounded at both ends. Under half an hour is not an afternoon; over six
# hours is something that has forgotten to finish. The hub applies it: when it next asks
# and the time has passed, the experience is over whatever moment it had reached.
MIN_MINUTES: Final = 30
MAX_MINUTES: Final = 360

# How much a parent is asked to read. Each moment is a paragraph and each branch is
# another path through them, so this is a limit on the document rather than on the
# afternoon — an experience that needs more moments than this is asking to be approved
# unread.
MAX_MOMENTS: Final = 12

_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,31}$")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class ExperienceError(ValueError):
    """An experience that cannot be read, or that says one thing and does another."""


def plain(raw: object, limit: int, what: str) -> str:
    """One line of text as it may be stored, or raise.

    Control characters are removed rather than refused, for the reason
    :mod:`shared.blueprint` gives: this text was written by a model and ends up on a
    display or inside another prompt, and a line break is the cheapest way to make one
    line of a document look like a new instruction.
    """
    if not isinstance(raw, str):
        raise ExperienceError(f"{what} must be text, not {type(raw).__name__}")
    text = " ".join(_CONTROL.sub(" ", raw).split())
    if len(text) > limit:
        raise ExperienceError(f"{what} is {len(text)} characters; at most {limit}")
    return text


def _identifier(raw: object, what: str) -> str:
    if not isinstance(raw, str) or not _ID.match(raw):
        # The offending value is quoted because this refusal travels to whoever asked, and
        # "a moment id is wrong" in a document with nine of them is a message that costs a
        # reader the work of finding which. Truncated: it is text a model wrote.
        raise ExperienceError(
            f"{what} must be 2 to 32 characters of a-z, 0-9 or hyphen, not {str(raw)[:40]!r}"
        )
    return raw


def _whole(raw: object, what: str) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise ExperienceError(f"{what} must be a whole number")
    return raw


def _only(values: Mapping[str, Any], allowed: set[str], what: str) -> None:
    """Refuse a key nobody declared. What the parent did not read cannot run."""
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise ExperienceError(f"{what} carries {unknown}, which this format does not define")


def _lines(raw: object) -> tuple[str, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, str):
        raise ExperienceError("lines must be a list")
    if len(raw) > MAX_LINES:
        raise ExperienceError(f"{len(raw)} lines; a screen holds {MAX_LINES}")
    return tuple(plain(line, MAX_LINE, "a line") for line in raw)


# ── The four moments ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Say:
    """Put words on a display. The words are in the document, so they were read."""

    act: ClassVar[Act] = Act.SAY

    id: str
    heading: str
    lines: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.heading:
            raise ExperienceError("a moment that says something needs a heading")

    def to_dict(self) -> dict[str, Any]:
        return {
            "act": str(self.act),
            "id": self.id,
            "heading": self.heading,
            "lines": list(self.lines),
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Say:
        _only(values, {"act", "id", "heading", "lines"}, "a say moment")
        return Say(
            id=_identifier(values.get("id"), "a moment id"),
            heading=plain(values.get("heading", ""), MAX_HEADING, "a heading"),
            lines=_lines(values.get("lines", [])),
        )


@dataclass(frozen=True, slots=True)
class HandOver:
    """Print a designed page and leave it on the table.

    ``design`` is a :class:`~shared.pagedesign.PageDesign`: marks over a closed
    vocabulary with no mark that fills an area, so an experience cannot spend an
    afternoon's ink however enthusiastic the model that devised it was.

    Nothing here says the page will come back. It is a physical object somebody may pick
    up, or not.
    """

    act: ClassVar[Act] = Act.HAND_OVER

    id: str
    design: PageDesign

    def to_dict(self) -> dict[str, Any]:
        return {"act": str(self.act), "id": self.id, "design": self.design.to_dict()}

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> HandOver:
        _only(values, {"act", "id", "design"}, "a hand_over moment")
        raw = values.get("design")
        if not isinstance(raw, Mapping):
            raise ExperienceError("a hand_over moment needs a design")
        try:
            design = PageDesign.from_dict(raw)
        except DesignError as exc:
            # One refusal for the parent to read, whichever layer noticed.
            raise ExperienceError(f"the page it hands over is not a design: {exc}") from exc
        return HandOver(id=_identifier(values.get("id"), "a moment id"), design=design)


@dataclass(frozen=True, slots=True)
class Outcome:
    """One thing that may have come back, and where the afternoon goes from there.

    ``then`` is the id of a later moment, or ``ask``. It is not an expression and there is
    nowhere to put one: an experience that wanted to say "if more than half" would have to
    say it in a sentence to a model, through ``ask``, where it is somebody's judgement
    rather than this format's arithmetic.
    """

    when: Came
    then: str

    def to_dict(self) -> dict[str, Any]:
        return {"when": str(self.when), "then": self.then}

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Outcome:
        _only(values, {"when", "then"}, "an outcome")
        raw = str(values.get("when", ""))
        try:
            when = Came(raw)
        except ValueError as exc:
            raise ExperienceError(f"a page cannot come back {raw!r}") from exc
        then = values.get("then", "")
        if then != ASK:
            then = _identifier(then, "what an outcome leads to")
        return Outcome(when=when, then=str(then))


@dataclass(frozen=True, slots=True)
class Collect:
    """Read back the page this experience handed over, and go on knowing what came back.

    It takes no parameter about what to read, and that is the point: there is nothing to
    aim and no subject to choose. It reads whatever is on the glass and refuses the page
    if it is not one this experience put there.

    Reading is a model's job, and the consequence is stated rather than worked around —
    no cloud, no reading. A page that comes back while the panel is unreachable waits, and
    the afternoon stops at this moment rather than guessing past it.
    """

    act: ClassVar[Act] = Act.COLLECT

    id: str
    outcomes: tuple[Outcome, ...]

    def __post_init__(self) -> None:
        seen = [outcome.when for outcome in self.outcomes]
        missing = [str(came) for came in Came if came not in seen]
        if missing:
            raise ExperienceError(
                f"this moment does not say what happens when a page comes back "
                f"{', '.join(missing)}"
            )
        if len(seen) != len(set(seen)):
            raise ExperienceError("two outcomes describe the same page coming back")

    def to_dict(self) -> dict[str, Any]:
        return {
            "act": str(self.act),
            "id": self.id,
            "outcomes": [outcome.to_dict() for outcome in self.outcomes],
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Collect:
        _only(values, {"act", "id", "outcomes"}, "a collect moment")
        raw = values.get("outcomes", [])
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise ExperienceError("outcomes must be a list")
        return Collect(
            id=_identifier(values.get("id"), "a moment id"),
            outcomes=tuple(Outcome.from_dict(o) for o in raw),
        )


@dataclass(frozen=True, slots=True)
class Close:
    """Say on a display that the afternoon is over.

    Separate from :class:`Say` because of what it means rather than what it draws: an
    experience with no ``close`` reachable is an afternoon that trails off, and the
    graph check below refuses one.
    """

    act: ClassVar[Act] = Act.CLOSE

    id: str
    heading: str
    lines: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.heading:
            raise ExperienceError("a moment that closes needs a heading")

    def to_dict(self) -> dict[str, Any]:
        return {
            "act": str(self.act),
            "id": self.id,
            "heading": self.heading,
            "lines": list(self.lines),
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Close:
        _only(values, {"act", "id", "heading", "lines"}, "a close moment")
        return Close(
            id=_identifier(values.get("id"), "a moment id"),
            heading=plain(values.get("heading", ""), MAX_HEADING, "a heading"),
            lines=_lines(values.get("lines", [])),
        )


Moment = Say | HandOver | Collect | Close

_MOMENTS: Final[Mapping[str, Any]] = {
    str(Act.SAY): Say.from_dict,
    str(Act.HAND_OVER): HandOver.from_dict,
    str(Act.COLLECT): Collect.from_dict,
    str(Act.CLOSE): Close.from_dict,
}


def moment_from_dict(values: Mapping[str, Any]) -> Moment:
    if not isinstance(values, Mapping):
        raise ExperienceError("a moment must be an object")
    act = str(values.get("act", ""))
    parse = _MOMENTS.get(act)
    if parse is None:
        raise ExperienceError(f"{act!r} is not one of the acts: {sorted(_MOMENTS)}")
    parsed: Moment = parse(values)
    return parsed


# ── The experience ───────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Experience:
    """One afternoon, whole, in a form a parent reads before it may happen in their house.

    The moments are ordered, and the order is what runs when nothing branches: a moment
    that is not a ``collect`` is followed by the next one in the list. A ``collect`` is
    followed by whichever of its outcomes the page turned out to be. That is the entire
    control flow, and it fits in this paragraph on purpose.
    """

    experience_id: str
    title: str
    # What this is, in the words the parent judges it by. Not a description of the moments:
    # the moments are right there and can be read. This is what approval is given to.
    overview: str
    minutes: int
    moments: tuple[Moment, ...]
    requires: frozenset[HouseCapability]
    format_version: int = EXPERIENCE_FORMAT_VERSION

    def __post_init__(self) -> None:
        if self.format_version != EXPERIENCE_FORMAT_VERSION:
            raise ExperienceError(
                f"experience format {self.format_version} is not {EXPERIENCE_FORMAT_VERSION}"
            )
        if not _ID.match(self.experience_id):
            raise ExperienceError(f"{self.experience_id!r} is not an experience id")
        if not self.title:
            raise ExperienceError("an experience without a title cannot be offered")
        if not self.overview:
            raise ExperienceError("an experience with no overview cannot be approved")
        if not MIN_MINUTES <= self.minutes <= MAX_MINUTES:
            raise ExperienceError(
                f"{self.minutes} minutes is outside {MIN_MINUTES}–{MAX_MINUTES}: an "
                f"experience lasts an afternoon"
            )
        if not self.moments:
            raise ExperienceError("an experience with no moment does nothing")
        if len(self.moments) > MAX_MOMENTS:
            raise ExperienceError(f"{len(self.moments)} moments; at most {MAX_MOMENTS}")

        ids = [moment.id for moment in self.moments]
        if len(ids) != len(set(ids)):
            raise ExperienceError("two moments share an id, so a branch cannot name one")

        needed = frozenset(NEEDS[moment.act] for moment in self.moments)
        if self.requires != needed:
            raise ExperienceError(
                f"declares it requires {_names(self.requires)} and its moments need "
                f"{_names(needed)}"
            )
        _check_paper(self.moments)
        _check_graph(self.moments)

    def moment(self, moment_id: str) -> Moment:
        for moment in self.moments:
            if moment.id == moment_id:
                return moment
        raise ExperienceError(f"there is no moment called {moment_id!r}")

    def runnable_in(self, available: frozenset[HouseCapability]) -> bool:
        """Whether this house can run it at all.

        A house that cannot must never be offered it. Unlike a blueprint there is no
        skipping: an experience is devised for one house that already has what it needs,
        so a missing capability is a mistake by whoever devised it, not a variation.
        """
        return self.requires <= available

    def to_dict(self) -> dict[str, Any]:
        return {
            "format_version": self.format_version,
            "experience_id": self.experience_id,
            "title": self.title,
            "overview": self.overview,
            "minutes": self.minutes,
            "requires": sorted(str(c) for c in self.requires),
            "moments": [moment.to_dict() for moment in self.moments],
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Experience:
        if not isinstance(values, Mapping):
            raise ExperienceError("an experience must be an object")
        _only(
            values,
            {
                "format_version",
                "experience_id",
                "title",
                "overview",
                "minutes",
                "requires",
                "moments",
            },
            "an experience",
        )
        raw = values.get("moments", [])
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise ExperienceError("moments must be a list")
        return Experience(
            experience_id=_identifier(values.get("experience_id"), "an experience id"),
            title=plain(values.get("title", ""), MAX_TITLE, "a title"),
            overview=plain(values.get("overview", ""), MAX_OVERVIEW, "an overview"),
            minutes=_whole(values.get("minutes"), "minutes"),
            moments=tuple(moment_from_dict(m) for m in raw),
            requires=_capabilities(values.get("requires", [])),
            format_version=_whole(
                values.get("format_version", EXPERIENCE_FORMAT_VERSION), "format_version"
            ),
        )


@dataclass(frozen=True, slots=True)
class Continuation:
    """The rest of an afternoon, written after an outcome said ``ask``.

    This is what "the house asks and the cloud thinks inside the answer" is, spelled as a
    type. The house posts what came back off the glass; what it gets is this, and this is
    parsed by the same code and held to the same rules as the document a parent approved.
    A model steering an afternoon therefore has exactly the same vocabulary it had when
    the afternoon was devised, and no more.

    It carries no overview, because nobody is approving it — that decision was taken once,
    over the experience, and its cost is stated in the module docstring and in
    `ideas/08 §2`.
    """

    experience_id: str
    # The collect moment whose outcome said ``ask``. It is here so that a continuation
    # arriving for a different afternoon, or for a branch that was not taken, is refused
    # by the house instead of played.
    after: str
    moments: tuple[Moment, ...]
    format_version: int = EXPERIENCE_FORMAT_VERSION

    def __post_init__(self) -> None:
        if self.format_version != EXPERIENCE_FORMAT_VERSION:
            raise ExperienceError(
                f"experience format {self.format_version} is not {EXPERIENCE_FORMAT_VERSION}"
            )
        if not _ID.match(self.experience_id):
            raise ExperienceError(f"{self.experience_id!r} is not an experience id")
        if not _ID.match(self.after):
            raise ExperienceError(f"{self.after!r} is not a moment id")
        if not self.moments:
            raise ExperienceError("a continuation with no moment does nothing")
        if len(self.moments) > MAX_MOMENTS:
            raise ExperienceError(f"{len(self.moments)} moments; at most {MAX_MOMENTS}")
        ids = [moment.id for moment in self.moments]
        if len(ids) != len(set(ids)):
            raise ExperienceError("two moments share an id, so a branch cannot name one")
        _check_paper(self.moments)
        _check_graph(self.moments)

    @property
    def requires(self) -> frozenset[HouseCapability]:
        """What these moments need. Computed rather than declared: nobody is reading it."""
        return frozenset(NEEDS[moment.act] for moment in self.moments)

    def to_dict(self) -> dict[str, Any]:
        return {
            "format_version": self.format_version,
            "experience_id": self.experience_id,
            "after": self.after,
            "moments": [moment.to_dict() for moment in self.moments],
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Continuation:
        if not isinstance(values, Mapping):
            raise ExperienceError("a continuation must be an object")
        _only(
            values,
            {"format_version", "experience_id", "after", "moments"},
            "a continuation",
        )
        raw = values.get("moments", [])
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise ExperienceError("moments must be a list")
        return Continuation(
            experience_id=_identifier(values.get("experience_id"), "an experience id"),
            after=_identifier(values.get("after"), "a moment id"),
            moments=tuple(moment_from_dict(m) for m in raw),
            format_version=_whole(
                values.get("format_version", EXPERIENCE_FORMAT_VERSION), "format_version"
            ),
        )


def _capabilities(raw: object) -> frozenset[HouseCapability]:
    if not isinstance(raw, Sequence) or isinstance(raw, str):
        raise ExperienceError("requires must be a list")
    found: set[HouseCapability] = set()
    for entry in raw:
        try:
            found.add(HouseCapability(str(entry)))
        except ValueError as exc:
            raise ExperienceError(f"{entry!r} is not a capability a house can have") from exc
    return frozenset(found)


def _check_paper(moments: Sequence[Moment]) -> None:
    """A page can only be collected if this experience put one on the table.

    Checked while the document is read rather than left to the run, because the parent
    approves the document. An experience that reads a page nobody handed over is broken
    before it reaches a house.
    """
    handed = False
    for position, moment in enumerate(moments, start=1):
        if moment.act is Act.HAND_OVER:
            handed = True
        elif moment.act is Act.COLLECT and not handed:
            raise ExperienceError(
                f"moment {position} collects a page that was never handed over"
            )


def _check_graph(moments: Sequence[Moment]) -> None:
    """Every branch leads somewhere, no branch leads backwards, and the afternoon ends.

    Backwards is the one that matters. A cycle is a loop, a loop is a program, and a
    program is the thing this format exists not to be — so it is refused here rather than
    stopped by a step counter at run time, where the parent is not.

    Ending is the other. A moment that is not a ``collect`` is followed by the next in the
    list, so an experience whose last moment is a ``say`` runs off the end and trails off.
    The last moment is therefore a ``close``, or a ``collect`` — and a ``collect`` at the
    end can only ask, because there is nothing after it to name.
    """
    position_of = {moment.id: index for index, moment in enumerate(moments)}

    for index, moment in enumerate(moments):
        if not isinstance(moment, Collect):
            continue
        for outcome in moment.outcomes:
            if outcome.then == ASK:
                continue
            target = position_of.get(outcome.then)
            if target is None:
                raise ExperienceError(
                    f"{moment.id!r} leads to {outcome.then!r}, which is not a moment"
                )
            if target <= index:
                raise ExperienceError(
                    f"{moment.id!r} leads back to {outcome.then!r}; an experience goes "
                    f"forward, and a loop is a program"
                )

    if moments[-1].act not in (Act.CLOSE, Act.COLLECT):
        raise ExperienceError(
            "the last moment neither closes nor collects, so the afternoon trails off; "
            "an experience that does not say it is over is the one thing this format "
            "will not carry"
        )

    reachable = _reachable(moments)
    unreachable = sorted({m.id for m in moments} - reachable)
    if unreachable:
        raise ExperienceError(
            f"{unreachable} cannot be reached; a moment nobody arrives at was approved "
            f"for nothing"
        )


def _reachable(moments: Sequence[Moment]) -> set[str]:
    """Which moments a run can actually arrive at, starting from the first.

    A ``collect`` is followed by whichever of its outcomes the page turned out to be, and
    by nothing else — so the moment printed after it in the list is reached only if an
    outcome names it.
    """
    position_of = {moment.id: index for index, moment in enumerate(moments)}
    seen: set[str] = set()
    pending = [0]
    while pending:
        index = pending.pop()
        if index >= len(moments):
            continue
        moment = moments[index]
        if moment.id in seen:
            continue
        seen.add(moment.id)
        if isinstance(moment, Collect):
            for outcome in moment.outcomes:
                if outcome.then != ASK:
                    pending.append(position_of[outcome.then])
        elif moment.act is not Act.CLOSE:
            pending.append(index + 1)
    return seen


def _names(capabilities: frozenset[HouseCapability]) -> str:
    return ", ".join(sorted(str(c) for c in capabilities)) or "nothing"
