"""What this household's afternoons came to, kept so the next one can be written from it.

Until 28 August 2026 nothing here existed and the rule was that what came back was read and
then gone. The cost of that rule was the whole point of the system: an afternoon could not
be written from the last one, so it was written from settings a parent typed once. This is
the relaxation, asked for by the parent, and it is bounded by shape rather than by promise.

**What is kept is what happened, not who somebody is.** A row says which afternoon ran, what
it was about, how far it got, whether each sheet came back marked or blank, and what the
page reader said was on it. There is no field for a score, a level, an ability, a difficulty
that suits somebody, or a summary of a person — not because a rule forbids writing one, but
because there is nowhere to put it. What a model makes of these facts it makes at the moment
it writes, and it is gone again.

**It is the parent's to read and to delete.** Every row goes to the panel in plain language,
and `forget` empties the lot. A memory the parent cannot see is the thing this project said
it would not build, and that part has not changed.
"""

from __future__ import annotations

import json
import threading
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


def themes_ever(afternoons: list[Afternoon]) -> tuple[str, ...]:
    """Every subject this household has been offered, once each, oldest first."""
    said: list[str] = []
    for one in afternoons:
        for theme in one.themes:
            if theme not in said:
                said.append(theme)
    return tuple(said)


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
