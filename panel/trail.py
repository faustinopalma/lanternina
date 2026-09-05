"""Everything the system wrote for one afternoon, kept whole.

The parent approves an idea. What happens after that is written by an agent as the afternoon
goes, one move at a time, and none of it is approved by anybody — there is no moment where a
parent could stand between a move and the room without stopping the afternoon to do it. So
the trade is made in the open: the parent does not get a veto on each move, and in exchange
they get to read every one of them afterwards, in full, beside the script the move came from.

What the afternoon *came to* is not here. It is in `panel/what_happened.py`, kept separately
because it is read by something else — the next afternoon is written from it. Nothing here
has a field that judgement would fit in, and that is on purpose: this is a record of a
machine, and how an afternoon went with a person is not a fact about the machine.

One reading is here, and it is a different one. `agents/experience_judge.py` reads a plan
back against the promises the prompt that wrote it made, before anybody has done it and
without knowing anything about who will. That is a fact about a document, so it is filed
under :data:`WHAT_A_READER_MADE_OF_IT`, beside the plan it judges.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.capabilities import WENT_WRONG, Act

# What one generated thing is filed under. A move is filed under the act it performs —
# `shared.capabilities.Act`, so the vocabulary stays the house's own and nothing can be filed
# under something the house cannot do. A continuation is not an act: it is the rest of an
# afternoon, written in one go when a page came back and the plan said to ask.
WHAT_COMES_AFTER = "continuation"
# The moments as the deviser wrote them, filed when the afternoon begins. Beside it the house
# files what it actually performed, and the two differ whenever the clock made it run a
# shorter version or reach for the way out.
THE_PLAN = "plan"
# What one reader made of that plan, filed beside it. `panel/judging.py` writes it straight
# after the afternoon is devised and it is kept on the offered afternoon until the house
# says it began; this is where a parent finds it. It is a reading and not a decision:
# nothing anywhere consults it to allow or refuse an afternoon.
WHAT_A_READER_MADE_OF_IT = "judged"
# An image this container drew, filed where it was drawn. Beside it the house files whether
# the paper ever reached the table, and the two differ exactly when it is worth knowing. It
# carries the picture it produced and, in the body, what was asked for — a page a parent can
# see without the request that shaped it is half the record.
WHAT_WAS_DRAWN = "drawn"
# What the machine could not do: a page the printer never took, a continuation the checks
# refused, a model that was not there. Until now it existed only in the journal on the house,
# where the person reading the parent's page cannot see it, and an afternoon that quietly did
# less than its plan looked from here like an afternoon that went as written. Its spelling
# lives in `shared/capabilities.py`, because a house files one too.
# The other half, kept only while `panel/keeping.py` says this household is being worked on.
# Every row of this kind carries the instant that permission lapses and is deleted then.
WHAT_CAME_BACK = "came"
# Which of those a house may report having done. It performs acts and nothing else: a house
# filing a `plan` or a `continuation` would be claiming to have written one.
DONE = frozenset({str(one) for one in Act})
# A house may also say what stopped it, which is not a claim to have written anything.
HOUSE_MAY_FILE = DONE | {WENT_WRONG}

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
    # What was asked of the model that made this. Kept beside the thing it produced rather
    # than in a log, because a generated page without its request cannot be judged: a parent
    # reading a sheet that came out wrong needs to see whether it was asked for wrongly.
    asked: str = ""
    # The words a model wrote on a sheet, in the order they are on it. A page was always
    # generated like everything else and always kept, but only inside the plan's JSON, where
    # it was present and readable by nobody.
    paper: str = ""
    # When this row stops being kept. Zero is everything the system wrote, which is kept.
    # See :data:`WHAT_CAME_BACK`.
    until: float = 0.0

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "at": self.at,
            "kind": self.kind,
            "heading": self.heading,
            "body": self.body,
            "why": self.why,
            "pictureId": self.picture_id,
            "asked": self.asked,
            "paper": self.paper,
            "until": self.until,
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


def lapsed(record: Made, now: float) -> bool:
    """Whether this row was only ever going to be kept for a while, and that while is over.

    Deletion, not a filter: a store answers by removing the row, the way an expired note in
    `panel/preferences.py` is removed rather than hidden. A record that is filtered on the
    way out is still a record.
    """
    return bool(record.until) and record.until <= now


@runtime_checkable
class TrailStore(Protocol):
    def began(self, trail: Trail) -> Trail: ...

    def wrote(self, record: Made) -> Made: ...

    def list(self, household_id: str) -> list[Trail]: ...

    def get(self, household_id: str, run_id: str) -> Trail | None: ...

    def forget_everything(self, household_id: str) -> int: ...


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
            now = time.time()
            rows = self._made.get((household_id, run_id), [])
            kept = [one for one in rows if not lapsed(one, now)]
            if len(kept) != len(rows):
                self._made[(household_id, run_id)] = kept
            made = sorted(kept, key=lambda one: one.at)
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

    def forget_everything(self, household_id: str) -> int:
        with self._lock:
            keys = [one for one in self._trails if one[0] == household_id]
            gone = len(keys)
            for key in keys:
                del self._trails[key]
                gone += len(self._made.pop(key, []))
            return gone
