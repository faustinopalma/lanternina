"""Everything the system wrote for one afternoon, and nothing about who it was written for.

The parent approves an idea. What happens after that is written by an agent as the afternoon
goes, one move at a time, and none of it is approved by anybody — there is no moment where a
parent could stand between a move and the room without stopping the afternoon to do it. So
the trade is made in the open: the parent does not get a veto on each move, and in exchange
they get to read every one of them afterwards, in full, beside the script the move came from.

**The asymmetry is the point.** What the system generated is kept whole and forever. What the
adolescent did with it is not kept at all — not the pages that came back, not what was written
on them, not how long anything took, not whether it was finished. A trail with both halves in
it would be a record of a person; a trail with only this half is a record of a machine, which
is the thing that needs watching. `docs/NON-GOALS.md` says the same in prose.

That also decides what a trail cannot become. There is no field here that could hold a
judgement, a total or a comparison, because there is no row here about a person to attach one
to. Counting trails would count afternoons, which is a fact about the house; nothing counts
them, because nobody asked and a number on a page invites being made to go up.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.capabilities import Act

# What one generated thing is filed under. A move is filed under the act it performs —
# `shared.capabilities.Act`, so the vocabulary stays the house's own and nothing can be filed
# under something the house cannot do. A continuation is not an act: it is the rest of an
# afternoon, written in one go when a page came back and the plan said to ask.
WHAT_COMES_AFTER = "continuation"
# The moments as the deviser wrote them, filed when the afternoon begins. Beside it the house
# files what it actually performed, and the two differ whenever the clock made it run a
# shorter version or reach for the way out.
THE_PLAN = "plan"
# Which of those a house may report having done. It performs acts and nothing else: a house
# filing a `plan` or a `continuation` would be claiming to have written one.
DONE = frozenset({str(one) for one in Act})

# How much of one generated thing is kept. A move is capped at 3000 characters upstream and a
# script at 6000; this is the backstop for a caller that is neither, and it truncates rather
# than refusing, because losing the tail of a record is better than losing the record.
MAX_BODY = 20_000


@dataclass(frozen=True, slots=True)
class Made:
    """One thing the system wrote, and when."""

    id: str
    household_id: str
    run_id: str
    at: float
    kind: str
    heading: str = ""
    body: str = ""
    # Why the agent said it did this. It reaches nobody in the house — it exists so that a
    # parent reading the trail afterwards can see the reasoning, not only the output.
    why: str = ""
    # For a picture, which one in the archive. Empty for everything else.
    picture_id: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "at": self.at,
            "kind": self.kind,
            "heading": self.heading,
            "body": self.body,
            "why": self.why,
            "pictureId": self.picture_id,
        }


@dataclass(frozen=True, slots=True)
class Trail:
    """One afternoon's worth of it. ``made`` is empty in a list of summaries."""

    run_id: str
    household_id: str
    experience_id: str
    title: str
    overview: str
    began_at: float
    script: str = ""
    made: tuple[Made, ...] = ()

    def summary(self) -> dict[str, Any]:
        """The card. Enough to recognise an afternoon, without carrying its script."""
        return {
            "runId": self.run_id,
            "experienceId": self.experience_id,
            "title": self.title,
            "overview": self.overview,
            "beganAt": self.began_at,
        }

    def to_public(self) -> dict[str, Any]:
        return {
            **self.summary(),
            "script": self.script,
            "made": [one.to_public() for one in self.made],
        }


def clipped(body: str) -> str:
    """Long bodies are kept short rather than refused. See :data:`MAX_BODY`."""
    text = str(body or "")
    return text if len(text) <= MAX_BODY else text[:MAX_BODY]


@runtime_checkable
class TrailStore(Protocol):
    def began(self, trail: Trail) -> Trail: ...

    def wrote(self, record: Made) -> Made: ...

    def list(self, household_id: str) -> list[Trail]: ...

    def get(self, household_id: str, run_id: str) -> Trail | None: ...


@dataclass
class InMemoryTrailStore:
    """Enough to run the API and the tests. Obviously not a database."""

    _trails: dict[tuple[str, str], Trail] = field(default_factory=dict)
    _made: dict[tuple[str, str], list[Made]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def began(self, trail: Trail) -> Trail:
        with self._lock:
            # Idempotent on the run, like the experience store: a house that retries the
            # first move must not open a second trail for one afternoon.
            return self._trails.setdefault((trail.household_id, trail.run_id), trail)

    def wrote(self, record: Made) -> Made:
        with self._lock:
            self._made.setdefault((record.household_id, record.run_id), []).append(record)
        return record

    def list(self, household_id: str) -> list[Trail]:
        with self._lock:
            rows = [
                Trail(
                    run_id=one.run_id,
                    household_id=one.household_id,
                    experience_id=one.experience_id,
                    title=one.title,
                    overview=one.overview,
                    began_at=one.began_at,
                )
                for (household, _), one in self._trails.items()
                if household == household_id
            ]
        return sorted(rows, key=lambda row: row.began_at, reverse=True)

    def get(self, household_id: str, run_id: str) -> Trail | None:
        with self._lock:
            found = self._trails.get((household_id, run_id))
            if found is None:
                return None
            made = sorted(self._made.get((household_id, run_id), []), key=lambda one: one.at)
            return Trail(
                run_id=found.run_id,
                household_id=found.household_id,
                experience_id=found.experience_id,
                title=found.title,
                overview=found.overview,
                began_at=found.began_at,
                script=found.script,
                made=tuple(made),
            )
