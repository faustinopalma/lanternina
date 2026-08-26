"""An idea a parent is working on, and the conversation they are shaping it in.

The parent has been able to approve or refuse what a model devised, and nothing else. This
is the other direction: an idea they steer, from an afternoon that already exists or from a
blank page, with a model rewriting the text as they talk to it and the text itself open to
be typed in directly.

**What a draft holds is the idea, not the plan.** Title, overview, themes and script — the
four things `panel/experiences.py` says a parent approves an afternoon by. The moments are
machinery: weights, help rungs, ways out, and a dozen checks that refuse a document that
cannot be run well. Free text cannot become that, and pretending it could would mean a
parent approving something that fails the format after they had finished with it. So
approval hands the script to the deviser as a brief, and what comes back is screened and
checked like every other afternoon.

**This is the one place a write from the panel spends money**, and `docs/NON-GOALS.md` was
amended rather than quietly bent. What the inertness rule protects is the house: nothing
here starts an afternoon, wakes the hub, or puts anything in a room. A parent working on
their own draft touches none of that, and the monthly limit governs it like every other
call.

Nothing here is about an adolescent. A draft carries no name, no id and no history, and the
conversation is the parent's own words and the model's — there is no field a reading of a
page or an account of how something went would fit in.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field, replace
from typing import Any, Protocol, runtime_checkable

OPEN = "open"
APPROVED = "approved"
CLOSED = "closed"

# Who said one turn. Two speakers and no third: a draft is a parent and the model they are
# working with, and a field that could hold anybody else is a field somebody will fill.
THE_PARENT = "parent"
THE_SYSTEM = "system"

# What one turn may be. Long enough for a paragraph of steering, short enough that a pasted
# document is refused rather than quietly sent.
MAX_SAYING = 2000
# How many turns are carried into the prompt. The whole conversation is kept and shown; this
# is what the model is given, because a prompt that grows without bound gets slower and
# dearer every turn and the oldest turn is the least useful thing in it.
CARRIED = 12
# How many turns one draft may hold at all. A conversation this long is a parent who should
# start again, and the bound is what keeps one draft from becoming a bill.
MAX_TURNS = 80


@dataclass(frozen=True, slots=True)
class Said:
    """One turn. ``who`` is the parent or the system, and there is no third."""

    who: str
    words: str
    at: float

    def to_public(self) -> dict[str, Any]:
        return {"who": self.who, "words": self.words, "at": self.at}


@dataclass(frozen=True, slots=True)
class Draft:
    """An idea being worked on, with the conversation that shaped it."""

    id: str
    household_id: str
    created_at: float
    updated_at: float = 0.0
    title: str = ""
    overview: str = ""
    themes: tuple[str, ...] = ()
    script: str = ""
    said: tuple[Said, ...] = ()
    state: str = OPEN
    # Which offered afternoon it was opened from, if it was opened from one. Kept so the
    # parent can see what they started with; the draft is a copy and editing it never
    # reaches back.
    started_from: str = ""
    # The afternoon approval produced, once it has. A draft that made one is finished.
    became: str = ""

    @property
    def blank(self) -> bool:
        return not (self.title or self.overview or self.script or self.themes)

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "overview": self.overview,
            "themes": list(self.themes),
            "script": self.script,
            "said": [one.to_public() for one in self.said],
            "state": self.state,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "startedFrom": self.started_from,
            "became": self.became,
        }

    def summary(self) -> dict[str, Any]:
        """The card. No conversation and no script: a list of drafts is not a read."""
        return {
            "id": self.id,
            "title": self.title,
            "overview": self.overview,
            "state": self.state,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "turns": len(self.said),
        }

    def carrying(self) -> tuple[Said, ...]:
        """The turns the model is given. See :data:`CARRIED`."""
        return self.said[-CARRIED:]


def cleaned(words: Any, name: str) -> str:
    """One typed thing, bounded. Raises ValueError rather than truncating.

    Truncating a parent's sentence is worse than refusing it: they would never know which
    half the model was given.
    """
    if not isinstance(words, str):
        raise ValueError(f"{name} is text")
    said = words.strip()
    if len(said) > MAX_SAYING:
        raise ValueError(f"{name} must be {MAX_SAYING} characters or fewer")
    return said


@runtime_checkable
class DraftStore(Protocol):
    def start(self, draft: Draft) -> Draft: ...

    def get(self, household_id: str, draft_id: str) -> Draft | None: ...

    def list(self, household_id: str) -> list[Draft]: ...

    def save(self, draft: Draft) -> Draft: ...


@dataclass
class InMemoryDraftStore:
    """Enough to run the API and the tests. Obviously not a database."""

    _rows: dict[tuple[str, str], Draft] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def start(self, draft: Draft) -> Draft:
        with self._lock:
            return self._rows.setdefault((draft.household_id, draft.id), draft)

    def get(self, household_id: str, draft_id: str) -> Draft | None:
        with self._lock:
            return self._rows.get((household_id, draft_id))

    def list(self, household_id: str) -> list[Draft]:
        with self._lock:
            rows = [
                row for (household, _), row in self._rows.items() if household == household_id
            ]
        return sorted(rows, key=lambda row: row.updated_at or row.created_at, reverse=True)

    def save(self, draft: Draft) -> Draft:
        with self._lock:
            kept = replace(draft, updated_at=time.time())
            self._rows[(draft.household_id, draft.id)] = kept
            return kept
