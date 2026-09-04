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

**Format 2, and why it is a version rather than four fields.** `ideas/09` is a design for
an afternoon that cannot end badly, and the way it gets there is structure decided before
the afternoon starts rather than care while it runs. Four things it needs did not fit the
format as it was, and each one turns a hope about the runner into a property of the
document:

* **A way out of every moment** — :class:`WayOut`, twenty minutes at the most, naming
  something the person is holding. The ending is then reachable from anywhere by reading,
  not by improvising, and an ending reached early is the same ending.
* **Three weights** — :class:`Weighing`, short, standard and extended, with the same
  narrative outcome and different cost. Shortening an afternoon becomes picking a column
  that was written with the same care as the others. **The limit, stated where the field
  is:** the weight changes the minutes and the words, not the page. A ``hand_over`` hands
  over the same design at all three weights, because three page designs per moment is
  three times the drawing for a difference nobody asked for yet.
* **Four rungs of help** — :class:`Help`, each carrying the minutes after which the next
  arrives. The same text whether somebody asked or the time passed, and after the last one
  the moment is over.
* **The version that runs without printing** — ``instead`` on a ``hand_over`` and
  ``if_no_page`` on a ``collect``. The printer is the single point of failure of an
  afternoon made of paper, and improvising around it at 15:30 is the thing this avoids.

None of that counts anything about a person. Minutes and rungs are facts about an
afternoon that is happening, they are discarded when it ends, and there is still no field
here that could hold a verdict.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar, Final

from .capabilities import NEEDS, Act, HouseCapability
from .page import Page, PageError

EXPERIENCE_FORMAT_VERSION: Final = 2


class Weight(StrEnum):
    """How much of a moment gets done. Three versions of one narrative outcome.

    Chosen on entering a moment and unchanged until the next one. That single sentence is
    what makes an afternoon shortenable without anybody noticing: shortening is picking a
    column somebody wrote, not a runtime edit of somebody else's words.
    """

    SHORT = "short"
    STANDARD = "standard"
    EXTENDED = "extended"


# The order is the order of cost, and the parser relies on it: a document that gives the
# short version more minutes than the standard one is refused.
WEIGHTS: Final[tuple[Weight, ...]] = (Weight.SHORT, Weight.STANDARD, Weight.EXTENDED)



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

# What the afternoon is about, in a handful of words each: *mappe*, *il vento*, *un museo
# di oggetti trovati*. Short on purpose — a theme a parent has to read twice is a summary,
# and the summary is the overview.
MAX_THEME: Final = 40
MAX_THEMES: Final = 5

# The game itself, written out. Not a summary and not a brief: the world, the question it
# turns on, the beats, what is held back and when it is given, what gets made, and where it
# can go differently. Six thousand characters is about a thousand words — long enough for
# something intricate, and short enough that whoever runs the afternoon can hold it.
#
# The number is large on purpose. At 1400 what came back was a paragraph of intentions, and
# a paragraph of intentions is what produces an afternoon that could be any afternoon.
MAX_SCRIPT: Final = 6000

# An afternoon, bounded at both ends, and the length is the game's to choose: an hour, two,
# three. They are not all the same size and a format that treated them as one would be
# asking for the same game every time.
#
# Four hours is the ceiling because that is an afternoon. Something that wants a week is a
# different mode and will be built as one — it needs to survive being put down, which this
# format cannot do: the hub applies the end, and when it next asks and the time has passed,
# the experience is over whatever moment it had reached.
MIN_MINUTES: Final = 30
MAX_MINUTES: Final = 240

# How much a parent is asked to read. Each moment is a paragraph and each branch is
# another path through them, so this is a limit on the document rather than on the
# afternoon — an experience that needs more moments than this is asking to be approved
# unread.
MAX_MOMENTS: Final = 12

# Four rungs of help and no more: a narrative nudge, a concrete clue, an almost explicit
# instruction, and the answer handed over as a gift inside the story. After the last one
# the moment is over — there is no fifth wait and nothing to get right before going on.
HELP_LEVELS: Final = 4
MAX_HELP_AFTER: Final = 30

# A way out has to be short enough to be worth taking, and the number is the one the
# design fixes. It is also what the arithmetic in `longest_at` is measured against.
MAX_WAY_OUT_MINUTES: Final = 20

# One moment, at one weight. Under a minute is not a moment; an hour is an afternoon.
MIN_WEIGHT_MINUTES: Final = 1
MAX_WEIGHT_MINUTES: Final = 60

MAX_IN_HAND: Final = 40
# A dimension is a short phrase, compared with other short phrases and never shown to
# anybody. Forty was chosen and it was too tight: on 24 August 2026 the real service was
# refused twice in a row over it, at 41 and 43 characters, for phrases like "un tavolo di
# casa nel tardo pomeriggio". Sixty is still a phrase and costs nothing.
MAX_DIMENSION: Final = 60

# The ten dimensions an afternoon is drawn along. They are recorded on the document for
# one reason: it makes "not the same afternoon again" a thing that can be checked instead
# of a thing that is hoped for. Nothing here is about a person — every one of them
# describes the afternoon.
DIMENSIONS: Final[tuple[str, ...]] = (
    "frame",
    "role",
    "mechanic",
    "progress",
    "paper",
    "glass",
    "displays",
    "camera",
    "tone",
    "ending",
)

# Which of the ten may come back. `frame` is where and when it is set, `role` is what the
# person is inside it: those are what a world is made of, and a house that liked one wants
# it again next week. The rest are the machinery — how it moves, what the paper is for, how
# it sounds, how it ends — and machinery repeated is the same afternoon in a different hat.
#
# This is the axis the whole thing turns on. Forcing every dimension to differ made variety
# checkable and made a run of afternoons impossible: nothing could recur, so nothing could
# be built on. Letting the world persist and the machinery vary is what a series is.
MAY_RECUR: Final[frozenset[str]] = frozenset({"frame", "role"})

# Which of the ten the house does not really choose. A flat with one display and a printer
# draws the same four values every week, so counting them as sameness charges a house for
# its hardware. They were counted until 30 August 2026, and the arithmetic was the problem:
# with four of the eight pinned by the equipment, two afternoons started halfway to a
# refusal before anything about them had been decided.
SET_BY_THE_HOUSE: Final[frozenset[str]] = frozenset({"paper", "glass", "displays", "camera"})

# How many of the remaining four — mechanic, progress, tone, ending — two afternoons may
# share before they are the same afternoon wearing a different hat. Three is a refusal; two
# is a coincidence.
#
# Two is also what makes a series possible. The same mechanic with a different progress is
# the shape `docs/EVIDENCE.md §3` argues for — a form shown, then the same form with new
# content — and the previous count, over all eight, refused it: repeating the mechanic and
# keeping the printer and the display was already three.
MAX_SHARED_DIMENSIONS: Final = 2

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


def _lines(raw: object, what: str = "lines") -> tuple[str, ...]:
    """A screenful, and never an empty one.

    Format 1 allowed no lines at all, on the grounds that a heading is enough. It is not,
    now that the same shape carries a way out and a rung of help: a rung with nothing in
    it is a rung the runner shows to nobody, and it would pass every other check.
    """
    if not isinstance(raw, Sequence) or isinstance(raw, str):
        raise ExperienceError(f"{what} must be a list")
    if not raw:
        raise ExperienceError(f"{what} says nothing, so there is nothing to show")
    if len(raw) > MAX_LINES:
        raise ExperienceError(f"{len(raw)} {what}; a screen holds {MAX_LINES}")
    return tuple(plain(line, MAX_LINE, "a line") for line in raw)


def _minutes(raw: object, low: int, high: int, what: str) -> int:
    value = _whole(raw, what)
    if not low <= value <= high:
        raise ExperienceError(f"{what} is {value} minutes; it must be {low} to {high}")
    return value


def _folded(text: str) -> str:
    """Text as it is compared, not as it is shown. Case and spacing carry no meaning here."""
    return " ".join(text.lower().split())


# Words that name nothing on their own: articles, prepositions and the Italian contractions
# of the two, plus the English equivalents. A phrase stripped to these has named no object.
_NOT_AN_OBJECT: Final[frozenset[str]] = frozenset(
    """
    il lo la i gli le un uno una un' l' d' dell della dello dei degli delle del
    di a da in con su per tra fra al allo alla ai agli alle dal dalla dallo dai dagli dalle
    nel nello nella nei negli nelle sul sullo sulla sui sugli sulle che e ed o od
    the a an of in on at to for with from and or its his her their this that
    """.split()
)

# Below this a word is not doing the naming: "ada" and "il" alike are too short to be the
# thing a way out reaches for, and matching on them would let anything through.
_LONG_ENOUGH: Final = 4


def names_the_same_thing(phrase: str, said: str) -> bool:
    """Whether ``said`` mentions the object that ``phrase`` names.

    **This used to be an exact substring test, and it was refusing good afternoons.**
    ``in_hand`` is a noun phrase written once, and the story that put the object on the
    table wrote it a different way — *la pagina del quaderno* against a page called *il
    quaderno* in one line and *la pagina* in another. The object had been named twice and
    the check refused it, because it was comparing the wording and not the thing. Measured
    on 3 September 2026: it was the most frequent refusal in the run, and each one cost a
    whole second devising.

    So the test is now: the phrase as written, or any one content word of it long enough to
    be doing the naming. That keeps what the rule is for — an ending may not reach for an
    object nobody was ever given, which is the goodbye felt as a cut — and stops it turning
    into a demand that the same words be repeated. What it gives up is said plainly: a
    phrase sharing an incidental word with something earlier now passes. This was always a
    test against text and never against the world, and `the_way_out_starts_from_something`
    says so in as many words.
    """
    kept = _folded(phrase)
    if kept and kept in said:
        return True
    return any(
        word in said
        for word in kept.split()
        if len(word) >= _LONG_ENOUGH and word not in _NOT_AN_OBJECT
    )


# ── The three weights, the ladder, and the way out ───────────────────────────────────


@dataclass(frozen=True, slots=True)
class Weighing:
    """One moment at one of its three costs: how long it takes, and what it says.

    The design's short version is "about a third of the time, one step, material already
    to hand". That is a description of what somebody writes, not something this format can
    check — what it does check is that the three are genuinely different, so a model that
    writes the same number three times is refused rather than quietly giving the runner
    nothing to shorten with.
    """

    minutes: int
    lines: tuple[str, ...]

    def __post_init__(self) -> None:
        if not MIN_WEIGHT_MINUTES <= self.minutes <= MAX_WEIGHT_MINUTES:
            raise ExperienceError(
                f"a weight of {self.minutes} minutes is outside "
                f"{MIN_WEIGHT_MINUTES}–{MAX_WEIGHT_MINUTES}"
            )
        if not self.lines:
            raise ExperienceError("a weight with no lines shows nothing")

    def to_dict(self) -> dict[str, Any]:
        return {"minutes": self.minutes, "lines": list(self.lines)}

    @staticmethod
    def from_dict(values: object) -> Weighing:
        if not isinstance(values, Mapping):
            raise ExperienceError("a weight must be an object")
        _only(values, {"minutes", "lines"}, "a weight")
        return Weighing(
            minutes=_minutes(
                values.get("minutes"), MIN_WEIGHT_MINUTES, MAX_WEIGHT_MINUTES, "a weight"
            ),
            lines=_lines(values.get("lines"), "lines of a weight"),
        )


def _weights(raw: object) -> tuple[Weighing, ...]:
    """The three versions of one moment, in the order of their cost."""
    if not isinstance(raw, Mapping):
        raise ExperienceError("weights must be an object with short, standard and extended")
    _only(raw, {str(w) for w in WEIGHTS}, "weights")
    missing = [str(w) for w in WEIGHTS if str(w) not in raw]
    if missing:
        raise ExperienceError(
            f"this moment has no {', '.join(missing)} version, so it cannot be shortened "
            f"or stretched without somebody inventing one at the time"
        )
    weighed = tuple(Weighing.from_dict(raw[str(w)]) for w in WEIGHTS)
    named = (("short", "standard"), ("standard", "extended"))
    for lighter, heavier, names in zip(weighed[:-1], weighed[1:], named, strict=True):
        if lighter.minutes >= heavier.minutes:
            raise ExperienceError(
                f"the {names[0]} version takes {lighter.minutes} minutes and the "
                f"{names[1]} one {heavier.minutes}; three weights that cost the same are "
                f"one weight written out three times"
            )
    return weighed


@dataclass(frozen=True, slots=True)
class Help:
    """One rung: what is said, and after how many minutes the next rung arrives.

    The same text is used whether somebody asked for help or whether the time simply
    passed. Two voices for the same thing is how a system tells a person it noticed they
    were stuck, and there is nowhere here to put the second one.
    """

    after_minutes: int
    lines: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"after_minutes": self.after_minutes, "lines": list(self.lines)}

    @staticmethod
    def from_dict(values: object) -> Help:
        if not isinstance(values, Mapping):
            raise ExperienceError("a rung of help must be an object")
        _only(values, {"after_minutes", "lines"}, "a rung of help")
        return Help(
            after_minutes=_minutes(
                values.get("after_minutes"), 1, MAX_HELP_AFTER, "a rung of help"
            ),
            lines=_lines(values.get("lines"), "lines of a rung of help"),
        )


def _ladder(raw: object) -> tuple[Help, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, str):
        raise ExperienceError("help must be a list of rungs")
    if len(raw) != HELP_LEVELS:
        raise ExperienceError(
            f"this moment carries {len(raw)} rungs of help; it must carry {HELP_LEVELS}, "
            f"ending with the answer handed over"
        )
    rungs = tuple(Help.from_dict(rung) for rung in raw)
    # Not strict: the second list is the first one shifted, so it is one shorter by design.
    for lower, upper in zip(rungs, rungs[1:], strict=False):
        if lower.after_minutes >= upper.after_minutes:
            raise ExperienceError(
                f"a rung arrives after {upper.after_minutes} minutes and the one before it "
                f"after {lower.after_minutes}; the ladder goes up"
            )
    return rungs


@dataclass(frozen=True, slots=True)
class WayOut:
    """How to reach the ending from exactly this moment, in twenty minutes or less.

    ``in_hand`` names something the person is holding right then, and the text has to name
    it too — that is checked here, and it is the whole reason this field exists rather
    than the way out being three more lines. The recurring defect of a generated plan is
    the goodbye that is not anchored to anything: the character says farewell and it is
    over, and the shortening is felt as a cut. A way out that starts from the sheet in
    somebody's hands does not read as one.

    That this is a *way out* and not an *ending* matters: it leads to the same close the
    afternoon was always going to reach, and nothing in it says anything was skipped.
    """

    in_hand: str
    heading: str
    lines: tuple[str, ...]
    minutes: int

    def __post_init__(self) -> None:
        if len(self.in_hand) < 3:
            raise ExperienceError(
                f"{self.in_hand!r} is too short to name an object somebody is holding"
            )
        if not self.heading:
            raise ExperienceError("a way out needs a heading")
        if self.minutes > MAX_WAY_OUT_MINUTES:
            raise ExperienceError(
                f"this way out takes {self.minutes} minutes; a way out is at most "
                f"{MAX_WAY_OUT_MINUTES}, or it is not a way out"
            )
        said = _folded(" ".join((self.heading, *self.lines)))
        if not names_the_same_thing(self.in_hand, said):
            raise ExperienceError(
                f"this way out is about {self.in_hand!r} and never names it; say the object "
                f"in the lines, in whatever words the story already uses for it"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "in_hand": self.in_hand,
            "heading": self.heading,
            "lines": list(self.lines),
            "minutes": self.minutes,
        }

    @staticmethod
    def from_dict(values: object) -> WayOut:
        if not isinstance(values, Mapping):
            raise ExperienceError("a moment with no way out cannot reach the ending from itself")
        _only(values, {"in_hand", "heading", "lines", "minutes"}, "a way out")
        return WayOut(
            in_hand=plain(values.get("in_hand", ""), MAX_IN_HAND, "what is in hand"),
            heading=plain(values.get("heading", ""), MAX_HEADING, "a heading"),
            lines=_lines(values.get("lines"), "lines of a way out"),
            minutes=_minutes(values.get("minutes"), 1, MAX_WAY_OUT_MINUTES, "a way out"),
        )


# ── The four moments ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class _Moment:
    """What every moment carries, whatever it does.

    Five fields and none of them optional. The three that are new in format 2 are here
    rather than on the acts that seem to need them, because the guarantee is about every
    moment: an afternoon where one moment out of nine has no way out is an afternoon that
    can strand, and where the missing one is is not something anybody can hold in mind.
    """

    id: str
    heading: str
    weights: tuple[Weighing, ...]
    help: tuple[Help, ...]
    way_out: WayOut

    act: ClassVar[Act]

    def __post_init__(self) -> None:
        if not self.heading:
            raise ExperienceError(f"moment {self.id!r} has no heading")
        if len(self.weights) != len(WEIGHTS):
            raise ExperienceError(f"moment {self.id!r} does not carry its three weights")
        if len(self.help) != HELP_LEVELS:
            raise ExperienceError(f"moment {self.id!r} does not carry {HELP_LEVELS} rungs of help")
        self._also()

    def _also(self) -> None:
        """Whatever this act needs beyond the common fields. Nothing, for most of them."""

    def at(self, weight: Weight) -> Weighing:
        return self.weights[WEIGHTS.index(weight)]

    @property
    def words(self) -> tuple[str, ...]:
        """Everything in this moment a person's eye lands on.

        One list, so that the block-list check, the repair loop and the safety gate cannot
        disagree about what counts as text somebody reads. What is left out is left out
        because nobody reads it: ids, rectangles, mark kinds and groups.
        """
        said = [self.heading]
        for weighing in self.weights:
            said.extend(weighing.lines)
        for rung in self.help:
            said.extend(rung.lines)
        said.append(self.way_out.heading)
        said.extend(self.way_out.lines)
        said.append(self.way_out.in_hand)
        said.extend(self._more_words())
        return tuple(said)

    @property
    def words_before_the_way_out(self) -> tuple[str, ...]:
        """The same, without the way out itself.

        The check that a way out starts from something already in hand needs this: counting
        a way out's own sentences as evidence would make every way out its own proof.
        """
        said = [self.heading]
        for weighing in self.weights:
            said.extend(weighing.lines)
        for rung in self.help:
            said.extend(rung.lines)
        said.extend(self._more_words())
        return tuple(said)

    def _more_words(self) -> tuple[str, ...]:
        """Whatever this act puts in front of somebody besides a display."""
        return ()


def _common(values: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": _identifier(values.get("id"), "a moment id"),
        "heading": plain(values.get("heading", ""), MAX_HEADING, "a heading"),
        "weights": _weights(values.get("weights")),
        "help": _ladder(values.get("help")),
        "way_out": WayOut.from_dict(values.get("way_out")),
    }


def _common_dict(moment: _Moment) -> dict[str, Any]:
    return {
        "act": str(moment.act),
        "id": moment.id,
        "heading": moment.heading,
        "weights": {str(w): moment.at(w).to_dict() for w in WEIGHTS},
        "help": [rung.to_dict() for rung in moment.help],
        "way_out": moment.way_out.to_dict(),
    }


_COMMON_KEYS: Final[set[str]] = {"act", "id", "heading", "weights", "help", "way_out"}


@dataclass(frozen=True, slots=True)
class Say(_Moment):
    """Put words on a display. The words are in the document, so they were read."""

    act: ClassVar[Act] = Act.SAY

    def to_dict(self) -> dict[str, Any]:
        return _common_dict(self)

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Say:
        _only(values, _COMMON_KEYS, "a say moment")
        return Say(**_common(values))


@dataclass(frozen=True, slots=True)
class HandOver(_Moment):
    """Print a page and leave it on the table.

    ``page`` is a :class:`~shared.page.Page`: what kind of object the paper is, the words on
    it, where to leave room to write, and what its drawing shows. It carries no coordinates
    and nothing on it has an identity — the whole sheet is drawn by a model from those words,
    and it is read by handing a model the blank and what came back off the glass.

    ``instead`` is the same moment with no printer: what the display says so that the
    afternoon carries on when the toner ran out at half past three. It is written now and
    checked now, because the alternative is a model improvising an apology at the moment
    something broke. It is mandatory, and a plan whose paper moments do not all carry one
    is refused. It is also what plays when the page could not be drawn at all.

    Nothing here says the page will come back. It is a physical object somebody may pick
    up, or not.
    """

    act: ClassVar[Act] = Act.HAND_OVER

    page: Page
    instead: tuple[str, ...]

    def _more_words(self) -> tuple[str, ...]:
        # The illustration is not among them: it describes a drawing and is never lettered,
        # so screening it here would say a page is safe because an ask was.
        return (*self.page.words(), *self.instead)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_common_dict(self),
            "page": self.page.to_dict(),
            "instead": list(self.instead),
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> HandOver:
        _only(values, _COMMON_KEYS | {"page", "instead"}, "a hand_over moment")
        raw = values.get("page")
        if not isinstance(raw, Mapping):
            raise ExperienceError("a hand_over moment needs a page")
        try:
            page = Page.from_dict(raw)
        except PageError as exc:
            # One refusal for the parent to read, whichever layer noticed.
            raise ExperienceError(f"what it hands over is not a page: {exc}") from exc
        return HandOver(
            **_common(values),
            page=page,
            instead=_lines(values.get("instead"), "what is said instead of printing"),
        )


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
class Collect(_Moment):
    """Read back the page this experience handed over, and go on knowing what came back.

    It takes no parameter about what to read, and that is the point: there is nothing to
    aim and no subject to choose. It reads whatever is on the glass and refuses the page
    if it is not one this experience put there.

    ``if_no_page`` is where the afternoon goes when there is no page to read at all —
    because the printer was unwell and the moment before this one ran its ``instead``.
    It names a later moment, or says ``ask``. Without it a house with no printer would
    reach a moment whose whole job is to read paper and have nowhere to go.

    Reading is a model's job, and the consequence is stated rather than worked around —
    no cloud, no reading. A page that comes back while the panel is unreachable waits, and
    the afternoon stops at this moment rather than guessing past it.
    """

    act: ClassVar[Act] = Act.COLLECT

    outcomes: tuple[Outcome, ...]
    if_no_page: str

    def _also(self) -> None:
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
            **_common_dict(self),
            "outcomes": [outcome.to_dict() for outcome in self.outcomes],
            "if_no_page": self.if_no_page,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Collect:
        _only(values, _COMMON_KEYS | {"outcomes", "if_no_page"}, "a collect moment")
        raw = values.get("outcomes", [])
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise ExperienceError("outcomes must be a list")
        if_no_page = values.get("if_no_page", "")
        if if_no_page != ASK:
            if_no_page = _identifier(if_no_page, "where a moment goes when nothing was printed")
        return Collect(
            **_common(values),
            outcomes=tuple(Outcome.from_dict(o) for o in raw),
            if_no_page=str(if_no_page),
        )


@dataclass(frozen=True, slots=True)
class Close(_Moment):
    """Say on a display that the afternoon is over.

    Separate from :class:`Say` because of what it means rather than what it draws: an
    experience with no ``close`` reachable is an afternoon that trails off, and the
    graph check below refuses one.
    """

    act: ClassVar[Act] = Act.CLOSE

    def to_dict(self) -> dict[str, Any]:
        return _common_dict(self)

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Close:
        _only(values, _COMMON_KEYS, "a close moment")
        return Close(**_common(values))


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
class Drawn:
    """The ten dimensions this afternoon was drawn along, one short phrase each.

    A seed alone flattens after a few afternoons: the same shape arrives wearing different
    nouns. What produces variety is passing the last few combinations to the devising
    agent as something it may not repeat, and that only works if a combination is written
    down. So it is a field.

    Everything in here describes the afternoon and nothing describes a person. "What the
    paper is for" is a property of a plan; there is no dimension for who it is for,
    because there is nowhere in this format for such a thing to live.
    """

    frame: str
    role: str
    mechanic: str
    progress: str
    paper: str
    glass: str
    displays: str
    camera: str
    tone: str
    ending: str

    def as_tuple(self) -> tuple[str, ...]:
        return tuple(getattr(self, name) for name in DIMENSIONS)

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in DIMENSIONS}

    @staticmethod
    def from_dict(values: object) -> Drawn:
        if not isinstance(values, Mapping):
            raise ExperienceError(
                "an experience must say which ten dimensions it was drawn along, or "
                "nobody can tell it apart from the last one"
            )
        _only(values, set(DIMENSIONS), "the dimensions")
        missing = [name for name in DIMENSIONS if not str(values.get(name, "")).strip()]
        if missing:
            raise ExperienceError(f"these dimensions were not drawn: {', '.join(missing)}")
        return Drawn(
            **{
                name: plain(values.get(name, ""), MAX_DIMENSION, f"the {name} dimension")
                for name in DIMENSIONS
            }
        )


def shared_dimensions(one: Drawn, other: Drawn) -> tuple[str, ...]:
    """Which of the ten two afternoons drew the same way. Compared folded, not literally."""
    return tuple(
        name
        for name, mine, theirs in zip(
            DIMENSIONS, one.as_tuple(), other.as_tuple(), strict=True
        )
        if _folded(mine) == _folded(theirs)
    )


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
    drawn: Drawn
    # What it is about, and how it should go. This is the idea the parent approves, and it
    # is what whatever runs the afternoon reads. Empty is allowed: the moments are a whole
    # plan on their own.
    themes: tuple[str, ...] = ()
    script: str = ""
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
            "themes": list(self.themes),
            "script": self.script,
            "minutes": self.minutes,
            "requires": sorted(str(c) for c in self.requires),
            "drawn": self.drawn.to_dict(),
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
                "themes",
                "script",
                "minutes",
                "requires",
                "drawn",
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
            themes=_themes(values.get("themes", [])),
            script=plain(values.get("script", ""), MAX_SCRIPT, "a script"),
            minutes=_whole(values.get("minutes"), "minutes"),
            moments=tuple(moment_from_dict(m) for m in raw),
            requires=_capabilities(values.get("requires", [])),
            drawn=Drawn.from_dict(values.get("drawn")),
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


def _themes(raw: object) -> tuple[str, ...]:
    """What the afternoon is about. Empty is allowed; a document may predate the field."""
    if not isinstance(raw, Sequence) or isinstance(raw, str):
        raise ExperienceError("themes must be a list")
    if len(raw) > MAX_THEMES:
        raise ExperienceError(f"{len(raw)} themes; at most {MAX_THEMES}")
    return tuple(plain(str(one), MAX_THEME, "a theme") for one in raw if str(one).strip())


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

    Those two together already mean the ending is reachable from every moment, which is
    `ideas/09 §14 #2`: edges only point forward, so every path arrives at the last moment,
    and the last moment either closes or asks. A separate walk to prove it was written here
    and taken out again — it could not be made to fail on any document this parser accepts,
    and a check nobody can write a failing case for is a claim rather than a check. What is
    left over is the document whose every branch says ``ask``, and that is refused by
    :func:`shared.experience_checks.the_ending_is_written_down`.
    """
    position_of = {moment.id: index for index, moment in enumerate(moments)}

    for index, moment in enumerate(moments):
        if not isinstance(moment, Collect):
            continue
        for where, target_id in _leads_from(moment):
            if target_id == ASK:
                continue
            target = position_of.get(target_id)
            if target is None:
                raise ExperienceError(
                    f"{moment.id!r} leads to {target_id!r} {where}, which is not a moment"
                )
            if target <= index:
                raise ExperienceError(
                    f"{moment.id!r} leads back to {target_id!r}; an experience goes "
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


def _leads_from(moment: Collect) -> tuple[tuple[str, str], ...]:
    """Every id a collect can send the afternoon to, and what sent it there.

    ``if_no_page`` is an edge like any other. It was not one in format 1 because it did
    not exist, and the printerless path is worth nothing if the graph does not know it is
    a path.
    """
    return (
        *((f"when a page comes back {outcome.when}", outcome.then) for outcome in moment.outcomes),
        ("when nothing was printed", moment.if_no_page),
    )


def longest_at(moments: Sequence[Moment], weight: Weight, *, start: int = 0) -> int:
    """The most minutes a run through these moments can take, at one weight.

    The longest path and not the sum: branches are alternatives, and adding them together
    would refuse a document that fits every way it can actually be run. Where a branch
    says ``ask``, the way out of that moment is counted — the continuation is a document
    nobody has written yet, and the only thing known about that stretch of afternoon is
    that it can be brought to an end from there.

    ``start`` is which moment to measure from, so the runner can ask the same question in
    the middle of an afternoon that the checks asked before it began.
    """
    position_of = {moment.id: index for index, moment in enumerate(moments)}
    beyond: list[int] = [0] * len(moments)
    for index in range(len(moments) - 1, -1, -1):
        moment = moments[index]
        here = moment.at(weight).minutes
        if moment.act is Act.CLOSE:
            beyond[index] = here
        elif isinstance(moment, Collect):
            onward = [
                moment.way_out.minutes if target == ASK else beyond[position_of[target]]
                for _, target in _leads_from(moment)
            ]
            beyond[index] = here + max(onward, default=0)
        else:
            beyond[index] = here + (beyond[index + 1] if index + 1 < len(moments) else 0)
    return beyond[start] if 0 <= start < len(beyond) else 0


def sheets_at_once(moments: Sequence[Moment], *, start: int = 0) -> int:
    """The most sheets that can be on the table at one time, anywhere in these moments.

    Until 28 August 2026 this counted the sheets a whole afternoon spends, and the number
    the parent had chosen was two. They meant two *at a time*: a three-hour afternoon that
    hands something over, takes it back, and hands over the next thing is four interactions
    and four sheets, and none of them is a crowded table. Counting the total refused that
    afternoon and there was no reason to.

    So the count runs along a path and resets at every ``collect``, because a collect is the
    moment the paper goes back on the glass and stops being what somebody is looking at. The
    largest run any path reaches is the answer. The longest path and not the sum, for the
    reason :func:`longest_at` gives: branches are alternatives.

    The whole afternoon is left bounded by its own shape rather than by a second number.
    A ``collect`` must follow a ``hand_over`` and there are at most :data:`MAX_MOMENTS`
    moments, so an afternoon allowed two sheets at a time cannot reach nine whatever it
    does. That is a ceiling nobody has to maintain.
    """
    position_of = {moment.id: index for index, moment in enumerate(moments)}
    # `run` is the sheets still on the table entering this moment's path; `most` is the
    # largest run any complete path from here reaches.
    run: list[int] = [0] * len(moments)
    most: list[int] = [0] * len(moments)
    for index in range(len(moments) - 1, -1, -1):
        moment = moments[index]
        if isinstance(moment, Collect):
            onward = [
                0 if target == ASK else most[position_of[target]]
                for _, target in _leads_from(moment)
            ]
            run[index] = 0
            most[index] = max(onward, default=0)
            continue
        if moment.act is Act.CLOSE:
            continue
        after = index + 1
        carried = run[after] if after < len(moments) else 0
        reached = most[after] if after < len(moments) else 0
        run[index] = carried + (1 if moment.act is Act.HAND_OVER else 0)
        most[index] = max(reached, run[index])
    return most[start] if 0 <= start < len(most) else 0


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
            for _, target in _leads_from(moment):
                if target != ASK:
                    pending.append(position_of[target])
        elif moment.act is not Act.CLOSE:
            pending.append(index + 1)
    return seen


def _names(capabilities: frozenset[HouseCapability]) -> str:
    return ", ".join(sorted(str(c) for c in capabilities)) or "nothing"
