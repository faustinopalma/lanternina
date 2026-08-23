"""What a designed experience is: data over a closed vocabulary of verbs.

A blueprint is a thing to do — a game, an activity — designed once and offered to many
houses. It has to be two things at the same time: something a machine runs without a
person in the loop, and something a person reads to the end before deciding it may run in
their home.

**A blueprint carries no code.** It is a short, flat sequence of steps, and a step is one
of the five dataclasses below. There is no expression to evaluate, no branch, no loop, no
name to look up. The whole set of things a blueprint can express is the set of fields of
those five types, which is why an administrator reading one has read all of it. Adding a
verb is a person editing this module; it is not something a blueprint can do to itself.

The price is real and worth stating. An experience that would change course on what came
back on the sheet cannot be written here — it has to be two experiences, or a person. We
pay that rather than accept the alternative, which is a blueprint that carries a program:
then an agent writes programs that run in other people's houses and an administrator
approves them by reading prose, which is a signature on something that was not read.

:mod:`shared.experience` is where that price was reconsidered, on 21 August 2026, and it
draws the line in a different place: branching yes, computation no. This module is not
superseded by it — a blueprint is a thing designed once for every house and approved by an
administrator, and an experience is devised for one house and approved by its parent.

Three absences are load-bearing.

* **Nothing points a sensor at a person.** ``READ_SHEET`` reads the sheet the same run
  printed, off a flatbed with the lid down. There is no parameter for what to frame, so
  there is nothing to set to "the room" — the blueprint has no way to say it, rather than
  a rule against saying it.
* **Nothing counts.** A blueprint has no field for how many houses took it, how often it
  ran, or how it went. Ordering a catalogue by any of those is an engagement metric in a
  useful feature's clothing, and the absence of the field is what keeps it out.
* **Nothing waits.** No verb pauses for a person, schedules a later step or asks again.
  Walking away in the middle is therefore indistinguishable from reaching the end: the run
  stops, and nothing is recorded about who stopped it or when.

What a blueprint *does* record is what it needs. ``requires`` and ``uses_if_present`` are
declared by the author and checked here against the steps, so the sentence an
administrator reads and the equipment the thing actually touches cannot disagree.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar, Final

from .capabilities import HouseCapability
from .ids import BlueprintId
from .pagedesign import DesignError, PageDesign

BLUEPRINT_FORMAT_VERSION: Final = 1


class Verb(StrEnum):
    """Everything a blueprint can ask for. A sixth entry is a person editing this file."""

    SHOW_WORDS = "show_words"
    PRINT_SHEET = "print_sheet"
    READ_SHEET = "read_sheet"
    SHOW_READING = "show_reading"
    ASK_MODEL = "ask_model"


# What each verb needs the house to be able to do. The blueprint does not get to say:
# a step that prints needs a printer whatever its author wrote.
#
# ``ASK_MODEL`` maps to nothing, and that is not an omission. No model runs on the device
# — every call goes to Azure — so reaching one is a question about the network, reported
# as a DegradationLevel, and not a property of the equipment in the house.
NEEDS: Final[Mapping[Verb, HouseCapability | None]] = {
    Verb.SHOW_WORDS: HouseCapability.SHOW_800X480_1BIT,
    Verb.PRINT_SHEET: HouseCapability.PRINT_A4,
    Verb.READ_SHEET: HouseCapability.SCAN_A4,
    Verb.SHOW_READING: HouseCapability.SHOW_800X480_1BIT,
    Verb.ASK_MODEL: None,
}

# Text limits. The two display ones were measured against the notice renderer's fonts,
# which have 728 px of usable width: 44 characters of ordinary Italian come to 681 px in
# the body font and 28 characters to about 697 px in the heading font. Longer text still
# renders — the renderer wraps — so these are the width at which a line stays a line, not
# a guarantee. The rest are chosen, not measured.
MAX_HEADING: Final = 28
MAX_LINE: Final = 44
MAX_LINES: Final = 4
MAX_TITLE: Final = 60
MAX_SUMMARY: Final = 400
MAX_AUTHOR: Final = 60
MAX_TOPIC_HINT: Final = 60
# Long enough for the two experiences written by hand and for the shape they suggest.
# A blueprint that needs more steps than this is probably two experiences.
MAX_STEPS: Final = 8

_ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,39}$")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class BlueprintError(ValueError):
    """A blueprint that cannot be read, or that says one thing and does another."""


def plain(raw: object, limit: int, what: str) -> str:
    """One line of text as it may be stored, or raise.

    Control characters are removed rather than refused. A blueprint arrives from outside
    the house and part of it ends up inside a model prompt or on a display, and a line
    break is the cheapest way to make one line of a document look like a new instruction.
    """
    if not isinstance(raw, str):
        raise BlueprintError(f"{what} must be text, not {type(raw).__name__}")
    text = " ".join(_CONTROL.sub(" ", raw).split())
    if len(text) > limit:
        raise BlueprintError(f"{what} is {len(text)} characters; at most {limit}")
    return text


def _flag(raw: object, what: str) -> bool:
    if not isinstance(raw, bool):
        raise BlueprintError(f"{what} must be true or false")
    return raw


def _only(values: Mapping[str, Any], allowed: set[str], what: str) -> None:
    """Refuse a key nobody declared. What the administrator did not read cannot run."""
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise BlueprintError(f"{what} carries {unknown}, which this format does not define")


# ── The five steps ───────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ShowWords:
    """Put words on a display. The words are in the blueprint, so they were read."""

    verb: ClassVar[Verb] = Verb.SHOW_WORDS

    heading: str
    lines: tuple[str, ...]
    optional: bool = False

    def __post_init__(self) -> None:
        if not self.heading:
            raise BlueprintError("a step that shows words needs a heading")
        if len(self.lines) > MAX_LINES:
            raise BlueprintError(f"{len(self.lines)} lines; a screen holds {MAX_LINES}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "verb": str(self.verb),
            "heading": self.heading,
            "lines": list(self.lines),
            "optional": self.optional,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> ShowWords:
        _only(values, {"verb", "heading", "lines", "optional"}, "a show_words step")
        raw = values.get("lines", [])
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise BlueprintError("lines must be a list")
        return ShowWords(
            heading=plain(values.get("heading", ""), MAX_HEADING, "a heading"),
            lines=tuple(plain(line, MAX_LINE, "a line") for line in raw),
            optional=_flag(values.get("optional", False), "optional"),
        )


@dataclass(frozen=True, slots=True)
class PrintSheet:
    """Put a designed page on paper.

    The design is a :class:`~shared.pagedesign.PageDesign`: marks over a closed
    vocabulary, with no mark that fills an area, so a blueprint cannot ask a house to
    spend an afternoon's ink. Until 21 August 2026 this carried questions and choices
    instead, and one module turned them into rectangles — which meant the only page this
    format could express was four questions of four boxes.
    """

    verb: ClassVar[Verb] = Verb.PRINT_SHEET

    design: PageDesign
    optional: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {"verb": str(self.verb), "design": self.design.to_dict(), "optional": self.optional}

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> PrintSheet:
        _only(values, {"verb", "design", "optional"}, "a print_sheet step")
        raw = values.get("design")
        if not isinstance(raw, Mapping):
            raise BlueprintError("a print_sheet step needs a design")
        try:
            design = PageDesign.from_dict(raw)
        except DesignError as exc:
            # One refusal for an administrator to read, whichever layer noticed.
            raise BlueprintError(f"the sheet it prints is not a design: {exc}") from exc
        return PrintSheet(
            design=design,
            optional=_flag(values.get("optional", False), "optional"),
        )


@dataclass(frozen=True, slots=True)
class ReadSheet:
    """Read back the sheet this run printed.

    It takes no parameter, and that is the point. There is nothing to aim, nothing to
    choose, no subject: it reads whatever is on the glass and refuses the page outright if
    the four corner markers are not all there.
    """

    verb: ClassVar[Verb] = Verb.READ_SHEET

    optional: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {"verb": str(self.verb), "optional": self.optional}

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> ReadSheet:
        _only(values, {"verb", "optional"}, "a read_sheet step")
        return ReadSheet(optional=_flag(values.get("optional", False), "optional"))


@dataclass(frozen=True, slots=True)
class ShowReading:
    """Say on the display what came back on the paper.

    Separate from ``SHOW_WORDS`` because of who wrote the words. There the text is in the
    blueprint and an administrator read it; here the blueprint supplies only the heading
    and the sentences are composed by code in this repository, which describes ink —
    which boxes carry a mark — and has no vocabulary for whether a mark was the right one.
    """

    verb: ClassVar[Verb] = Verb.SHOW_READING

    heading: str
    optional: bool = False

    def __post_init__(self) -> None:
        if not self.heading:
            raise BlueprintError("a step that shows a reading needs a heading")

    def to_dict(self) -> dict[str, Any]:
        return {"verb": str(self.verb), "heading": self.heading, "optional": self.optional}

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> ShowReading:
        _only(values, {"verb", "heading", "optional"}, "a show_reading step")
        return ShowReading(
            heading=plain(values.get("heading", ""), MAX_HEADING, "a heading"),
            optional=_flag(values.get("optional", False), "optional"),
        )


class Asks(StrEnum):
    """What a blueprint may ask a model for. Closed, like everything else here."""

    EXERCISE = "exercise"


@dataclass(frozen=True, slots=True)
class AskModel:
    """Ask a model for content, of a kind this vocabulary names.

    There is no prompt field. A blueprint that carried one would be carrying a program
    written in prose, and the closed vocabulary would be closed only on paper. What it
    carries instead is which of the named things it wants and, at most, a topic — the same
    surface ``ContentAgent.propose_exercise`` already exposes. Everything else about the
    request comes from the household's own settings, which reach a model as the hints
    ``prompt_hints()`` returns.

    Neither hand-written experience uses this verb, and the runner on the hub refuses it:
    generating content centrally is the next entry in ideas/07, not this one.
    """

    verb: ClassVar[Verb] = Verb.ASK_MODEL

    asks_for: Asks
    topic_hint: str = ""
    optional: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "verb": str(self.verb),
            "asks_for": str(self.asks_for),
            "topic_hint": self.topic_hint,
            "optional": self.optional,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> AskModel:
        _only(values, {"verb", "asks_for", "topic_hint", "optional"}, "an ask_model step")
        raw = str(values.get("asks_for", ""))
        try:
            asks_for = Asks(raw)
        except ValueError as exc:
            raise BlueprintError(f"a model cannot be asked for {raw!r}") from exc
        return AskModel(
            asks_for=asks_for,
            topic_hint=plain(values.get("topic_hint", ""), MAX_TOPIC_HINT, "a topic hint"),
            optional=_flag(values.get("optional", False), "optional"),
        )


Step = ShowWords | PrintSheet | ReadSheet | ShowReading | AskModel

_STEPS: Final[Mapping[str, Any]] = {
    str(Verb.SHOW_WORDS): ShowWords.from_dict,
    str(Verb.PRINT_SHEET): PrintSheet.from_dict,
    str(Verb.READ_SHEET): ReadSheet.from_dict,
    str(Verb.SHOW_READING): ShowReading.from_dict,
    str(Verb.ASK_MODEL): AskModel.from_dict,
}


def step_from_dict(values: Mapping[str, Any]) -> Step:
    if not isinstance(values, Mapping):
        raise BlueprintError("a step must be an object")
    verb = str(values.get("verb", ""))
    parse = _STEPS.get(verb)
    if parse is None:
        raise BlueprintError(f"{verb!r} is not one of the verbs: {sorted(_STEPS)}")
    parsed: Step = parse(values)
    return parsed


# ── The blueprint ────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Blueprint:
    """A designed experience, whole, in a form a person can read to the end."""

    blueprint_id: BlueprintId
    version: int
    title: str
    # What this is, in the words an administrator judges it by. Not a description of the
    # steps: the steps are right there and can be read.
    summary: str
    author: str
    steps: tuple[Step, ...]
    requires: frozenset[HouseCapability]
    uses_if_present: frozenset[HouseCapability]
    format_version: int = BLUEPRINT_FORMAT_VERSION

    def __post_init__(self) -> None:
        if self.format_version != BLUEPRINT_FORMAT_VERSION:
            raise BlueprintError(
                f"blueprint format {self.format_version} is not {BLUEPRINT_FORMAT_VERSION}"
            )
        if not _ID.match(self.blueprint_id):
            raise BlueprintError(f"{self.blueprint_id!r} is not a blueprint id")
        if self.version < 1:
            raise BlueprintError("a blueprint starts at version 1")
        if not self.title:
            raise BlueprintError("a blueprint without a title cannot be offered")
        if not self.steps:
            raise BlueprintError("a blueprint with no step does nothing")
        if len(self.steps) > MAX_STEPS:
            raise BlueprintError(f"{len(self.steps)} steps; at most {MAX_STEPS}")

        required, optional = _needed_by(self.steps)
        if self.requires != required:
            raise BlueprintError(
                f"declares it requires {_names(self.requires)} and its steps need "
                f"{_names(required)}"
            )
        if self.uses_if_present != optional:
            raise BlueprintError(
                f"declares it uses {_names(self.uses_if_present)} if present and its "
                f"optional steps use {_names(optional)}"
            )
        _check_order(self.steps)

    def runnable_in(self, available: frozenset[HouseCapability]) -> bool:
        """Whether this house can run it at all.

        A house that cannot must never be offered it. Offering and then failing costs the
        parent their own effort working out whose fault it was, which is worse than the
        experience never having appeared.
        """
        return self.requires <= available

    def steps_for(self, available: frozenset[HouseCapability]) -> tuple[Step, ...]:
        """The steps that run here. Raises if the house is missing something required."""
        if not self.runnable_in(available):
            missing = _names(self.requires - available)
            raise BlueprintError(f"this house cannot {missing}")
        return tuple(
            step
            for step in self.steps
            if not step.optional or NEEDS[step.verb] in available or NEEDS[step.verb] is None
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format_version": self.format_version,
            "blueprint_id": str(self.blueprint_id),
            "version": self.version,
            "title": self.title,
            "summary": self.summary,
            "author": self.author,
            "requires": sorted(str(c) for c in self.requires),
            "uses_if_present": sorted(str(c) for c in self.uses_if_present),
            "steps": [step.to_dict() for step in self.steps],
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Blueprint:
        _only(
            values,
            {
                "format_version",
                "blueprint_id",
                "version",
                "title",
                "summary",
                "author",
                "requires",
                "uses_if_present",
                "steps",
            },
            "a blueprint",
        )
        raw_steps = values.get("steps", [])
        if not isinstance(raw_steps, Sequence) or isinstance(raw_steps, str):
            raise BlueprintError("steps must be a list")
        return Blueprint(
            blueprint_id=BlueprintId(plain(values.get("blueprint_id", ""), 40, "an id")),
            version=_whole(values.get("version"), "version"),
            title=plain(values.get("title", ""), MAX_TITLE, "a title"),
            summary=plain(values.get("summary", ""), MAX_SUMMARY, "a summary"),
            author=plain(values.get("author", ""), MAX_AUTHOR, "an author"),
            steps=tuple(step_from_dict(step) for step in raw_steps),
            requires=_capabilities(values.get("requires", []), "requires"),
            uses_if_present=_capabilities(values.get("uses_if_present", []), "uses_if_present"),
            format_version=_whole(
                values.get("format_version", BLUEPRINT_FORMAT_VERSION), "format_version"
            ),
        )


def _whole(raw: object, what: str) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise BlueprintError(f"{what} must be a whole number")
    return raw


def _capabilities(raw: object, what: str) -> frozenset[HouseCapability]:
    if not isinstance(raw, Sequence) or isinstance(raw, str):
        raise BlueprintError(f"{what} must be a list")
    found: set[HouseCapability] = set()
    for entry in raw:
        try:
            found.add(HouseCapability(str(entry)))
        except ValueError as exc:
            raise BlueprintError(f"{entry!r} is not a capability a house can have") from exc
    return frozenset(found)


def _needed_by(
    steps: Sequence[Step],
) -> tuple[frozenset[HouseCapability], frozenset[HouseCapability]]:
    """What the steps need, split into what must be there and what is used if it is."""
    required: set[HouseCapability] = set()
    optional: set[HouseCapability] = set()
    for step in steps:
        needed = NEEDS[step.verb]
        if needed is None:
            continue
        (optional if step.optional else required).add(needed)
    # A capability some step needs outright is required, whatever an optional step says.
    return frozenset(required), frozenset(optional - required)


def _check_order(steps: Sequence[Step]) -> None:
    """A step that reads back needs a sheet before it, and a reading before it is said.

    Checked here rather than left to the runner because an administrator approves the
    document, not the run. A blueprint that reads a sheet nobody printed is broken while
    it is being read, and should not reach a house to find out.
    """
    printed = False
    read = False
    for position, step in enumerate(steps, start=1):
        if step.verb is Verb.PRINT_SHEET:
            printed = True
        elif step.verb is Verb.READ_SHEET:
            if not printed:
                raise BlueprintError(f"step {position} reads a sheet that was never printed")
            read = True
        elif step.verb is Verb.SHOW_READING and not read:
            raise BlueprintError(f"step {position} shows a reading that never happened")


def _names(capabilities: frozenset[HouseCapability]) -> str:
    return ", ".join(sorted(str(c) for c in capabilities)) or "nothing"
