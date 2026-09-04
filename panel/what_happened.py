"""What this household's afternoons came to, kept so the next one can be written from it.

Until 28 August 2026 nothing here existed and the rule was that what came back was read and
then gone. The cost of that rule was the whole point of the system: an afternoon could not
be written from the last one, so it was written from settings a parent typed once. This is
the relaxation, asked for by the parent, and it is bounded by shape rather than by promise.

**What is kept here is what happened, not who somebody is** — and that is now a division of
labour rather than a rule about the whole system. A row says which afternoon ran, what it
was about, how far it got, whether each sheet came back marked or blank, and what the page
reader said was on it. It has no field for a level or a summary of a person, because those
belong to the profile that is kept beside it; this store is the evidence and not the reading
of it.

Until 4 September 2026 this paragraph said no such reading existed anywhere, and that there
was nowhere to put one. That rule was withdrawn: an afternoon cannot be pitched at the right
level without a profile, and refusing to hold one was refusing to do the work well.

**It is the parent's to read and to delete.** Every row goes to the panel in plain language,
and `forget` empties the lot. A memory the parent cannot see is the thing this project said
it would not build, and that part has not changed.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# What the page reader said, capped. Long enough for a sentence about a sheet and short
# enough that nobody is tempted to keep a transcript.
MAX_READING = 400
# How many afternoons reach a prompt. All of them are kept; the prompt gets the recent ones,
# because a model handed forty afternoons writes about the list instead of about today.
RECENT = 8

# How an afternoon stopped. Facts about a run, and the vocabulary is closed so that nothing
# can file a judgement under a name nobody agreed on.
CLOSED = "closed"
WAY_OUT = "way_out"
STOPPED = "stopped"
WENT_WRONG = "went_wrong"
ENDINGS = frozenset({CLOSED, WAY_OUT, STOPPED, WENT_WRONG})


@dataclass(frozen=True, slots=True)
class Answered:
    """One sheet that went out, and what came back of it."""

    moment_id: str
    came: str
    reading: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"momentId": self.moment_id, "came": self.came, "reading": self.reading}


@dataclass(frozen=True, slots=True)
class Afternoon:
    """One afternoon that ran, as facts about the afternoon."""

    household_id: str
    run_id: str
    experience_id: str
    title: str
    at: float
    themes: tuple[str, ...] = ()
    weight: str = ""
    minutes: int = 0
    reached: str = ""
    ending: str = ""
    answered: tuple[Answered, ...] = ()

    def to_public(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "experienceId": self.experience_id,
            "title": self.title,
            "at": self.at,
            "themes": list(self.themes),
            "weight": self.weight,
            "minutes": self.minutes,
            "reached": self.reached,
            "ending": self.ending,
            "answered": [one.to_dict() for one in self.answered],
        }

    def for_the_prompt(self) -> dict[str, Any]:
        """The same afternoon with the run ids dropped: they name nothing a model can use."""
        return {
            "title": self.title,
            "themes": list(self.themes),
            "howLong": self.weight,
            "minutes": self.minutes,
            "ending": self.ending,
            "sheets": [
                {"came": one.came, "onIt": one.reading} for one in self.answered
            ],
        }


@runtime_checkable
class WhatHappenedStore(Protocol):
    def remember(self, afternoon: Afternoon) -> Afternoon: ...

    def list(self, household_id: str) -> list[Afternoon]: ...

    def forget(self, household_id: str) -> None: ...


@dataclass
class InMemoryWhatHappenedStore:
    _rows: dict[str, dict[str, Afternoon]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def remember(self, afternoon: Afternoon) -> Afternoon:
        with self._lock:
            # By run, so a house that reports the same afternoon twice does not double it.
            house = self._rows.setdefault(afternoon.household_id, {})
            house[afternoon.run_id] = afternoon
            return afternoon

    def list(self, household_id: str) -> list[Afternoon]:
        with self._lock:
            return sorted(self._rows.get(household_id, {}).values(), key=lambda one: one.at)

    def forget(self, household_id: str) -> None:
        with self._lock:
            self._rows.pop(household_id, None)


def clean_reading(raw: Any) -> str:
    """What a page reader said, as one line and no longer than :data:`MAX_READING`."""
    if not isinstance(raw, str):
        return ""
    said = " ".join(raw.split())
    return said[:MAX_READING]


# How far back a subject counts as just used, and as used lately. Afternoons and not days:
# a house that ran four in a week and a house that ran four in two months have been over the
# same ground, and a clock would say otherwise.
JUST_USED = 3
USED_LATELY = 10
# How many older subjects are carried. The list has to stop somewhere, and what it keeps is
# the ones used most often rather than the most recent of them: a subject this house has been
# given five times is the rut, and one it was given once two years ago is not.
CARRIED_FROM_BEFORE = 12


@dataclass(frozen=True, slots=True)
class Ground:
    """What this house has been over already, in three bands by how recently.

    Three and not one, because the answer is different in each. A subject from last week is
    a repeat; the same subject from two years ago is somewhere to return to from another
    side. A flat list cannot say that, and a flat list of everything is also the thing that
    stops fitting in a prompt.
    """

    just_used: tuple[str, ...] = ()
    used_lately: tuple[str, ...] = ()
    used_before: tuple[str, ...] = ()

    def anything(self) -> bool:
        return bool(self.just_used or self.used_lately or self.used_before)

    def to_dict(self) -> dict[str, Any]:
        return {
            "justUsed": list(self.just_used),
            "usedLately": list(self.used_lately),
            "usedBefore": list(self.used_before),
        }


def the_ground(by_afternoon: Sequence[Sequence[str]]) -> Ground:
    """The subjects of every afternoon ever proposed here, oldest first, compacted.

    Every afternoon *proposed* and not only every one run: something offered and never
    played has still been used, and offering it again is the repeat this is here to stop.

    A subject lands in the band of the last afternoon it appeared in. What falls out is the
    tail of the oldest band, ordered by how often each subject has come up, so the list stops
    growing without losing the ruts.
    """
    last_seen: dict[str, int] = {}
    times: dict[str, int] = {}
    total = len(by_afternoon)
    for index, themes in enumerate(by_afternoon):
        back = total - index
        for raw in themes:
            theme = str(raw).strip()
            if not theme:
                continue
            last_seen[theme] = min(last_seen.get(theme, back), back)
            times[theme] = times.get(theme, 0) + 1
    just = tuple(one for one, back in last_seen.items() if back <= JUST_USED)
    lately = tuple(
        one for one, back in last_seen.items() if JUST_USED < back <= USED_LATELY
    )
    older = [one for one, back in last_seen.items() if back > USED_LATELY]
    older.sort(key=lambda one: (-times[one], one))
    return Ground(just, lately, tuple(older[:CARRIED_FROM_BEFORE]))


# What to do with the last few afternoons when deciding how much to ask for. Not a claim
# about anybody: it is read off how the runs went and it is computed again every time.
STEADY = (
    "Ask for about what the last ones asked for. Nothing here says to move either way."
)
MORE = (
    "The last few ran to their end and came back written on. This one may hold more "
    "together at once: one more thing to relate, or one more turn before the answer."
)
LESS = (
    "Several of the last few stopped early or came back untouched. Ask for fewer things at "
    "once and make the first thing smaller. Do not make it shorter and do not make it "
    "simpler to read: what is heavy is how much has to be held at the same time."
)
# How many recent runs the direction is read off. Fewer than three is not enough to lean on.
WEIGHED = 6
ENOUGH_TO_LEAN_ON = 3


@dataclass(frozen=True, slots=True)
class HowItHasGone:
    """How the last few runs went, and which way that says to move.

    Counts and never a level. It is computed at the moment a prompt is built and stored
    nowhere: a number written down about somebody is the thing this project does not keep,
    and the same number read off the runs each time is not one.
    """

    ran: int = 0
    carried_through: int = 0
    brought_to_an_end: int = 0
    stopped: int = 0
    marked: int = 0
    blank: int = 0

    def direction(self) -> str:
        if self.ran < ENOUGH_TO_LEAN_ON:
            return STEADY
        went_far = self.carried_through / self.ran
        gave_up = (self.stopped + self.brought_to_an_end) / self.ran
        wrote_on = self.marked / (self.marked + self.blank) if self.marked + self.blank else 0.0
        if went_far >= 0.7 and wrote_on >= 0.6:
            return MORE
        if gave_up >= 0.5 or (self.marked + self.blank and wrote_on <= 0.34):
            return LESS
        return STEADY

    def to_dict(self) -> dict[str, Any]:
        return {
            "afternoonsRun": self.ran,
            "ranToTheEnd": self.carried_through,
            "endedEarly": self.brought_to_an_end,
            "stopped": self.stopped,
            "sheetsWrittenOn": self.marked,
            "sheetsBlank": self.blank,
        }


def how_it_has_gone(afternoons: Sequence[Afternoon], *, weighed: int = WEIGHED) -> HowItHasGone:
    """The last few runs counted up. Empty history gives zeroes, which say to stay put."""
    lately = list(afternoons)[-weighed:]
    marked = sum(1 for one in lately for sheet in one.answered if sheet.came == "marks")
    blank = sum(1 for one in lately for sheet in one.answered if sheet.came == "blank")
    return HowItHasGone(
        ran=len(lately),
        carried_through=sum(1 for one in lately if one.ending == CLOSED),
        brought_to_an_end=sum(1 for one in lately if one.ending == WAY_OUT),
        stopped=sum(1 for one in lately if one.ending in (STOPPED, WENT_WRONG)),
        marked=marked,
        blank=blank,
    )


def remembered(
    *,
    household_id: str,
    run_id: str,
    experience: dict[str, Any],
    at: float,
    weight: str = "",
    minutes: int = 0,
    reached: str = "",
    ending: str = "",
    answered: tuple[Answered, ...] = (),
) -> Afternoon:
    """One afternoon out of the document it ran and what the house said happened to it."""
    themes = tuple(str(one) for one in (experience.get("themes") or ()) if str(one))
    return Afternoon(
        household_id=household_id,
        run_id=run_id,
        experience_id=str(experience.get("experience_id", "")),
        title=str(experience.get("title", "")),
        at=at,
        themes=themes,
        weight=weight,
        minutes=minutes,
        reached=reached,
        ending=ending if ending in ENDINGS else "",
        answered=answered,
    )


def as_material(afternoons: list[Afternoon], *, recent: int = RECENT) -> str:
    """The recent afternoons as JSON, for a prompt. Empty when there are none.

    Quoted like everything else that is not instruction: a reading is what a model wrote
    about a sheet somebody wrote on, and it reaches this prompt as something to weigh.
    """
    if not afternoons:
        return ""
    return json.dumps(
        [one.for_the_prompt() for one in afternoons[-recent:]], ensure_ascii=False
    )
