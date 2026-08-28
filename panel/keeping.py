"""The one half of an afternoon that is kept only while somebody is building this.

`panel/trail.py` keeps what the system wrote and nothing about the person it was written
for. That asymmetry is the product. This module is the single exception to it, and it is
written as an exception rather than as a setting, because the two are not the same thing: a
setting is something a system offers, and an exception is something a system admits to.

While this is being built, a household an administrator names also keeps what came back off
the glass, so that an afternoon that went wrong can be read against what it was answering.
Four properties, each of them a choice and not an accident:

* **Off unless somebody turned it on.** A household with no row keeps nothing, which is
  every household nobody is working on.
* **Not the parent's to set.** It is written through `panel/routes/admin.py`, against the
  administrator's own directory and app role, so no fault in the parent's write path can
  turn it on and nothing in the panel a parent sees mentions it.
* **It lapses rather than waiting to be turned off.** There is no state anybody has to
  remember to undo: :data:`KEPT_FOR_DAYS` after it was last set, it is off. Turning it off
  early is one call; leaving it on for a year is not reachable without saying so eight times.
* **What it allowed goes with it.** Every row it let through carries the same instant, and
  `panel/trail.py` deletes those rows the first time the record is read past it.

What it costs, stated where the claim is: for as long as the permission stands, that
household's record is a record of a person and not only of a machine. That is the trade, it
is bounded in time and in scope, and `docs/NON-GOALS.md` names it beside the promise.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# How long one permission stands. Two weeks is long enough to run a fortnight of afternoons
# and short enough that a household left switched on is switched off before the next season.
# Chosen, not measured.
KEPT_FOR_DAYS = 14
KEPT_FOR_SECONDS = KEPT_FOR_DAYS * 24 * 60 * 60


@dataclass(frozen=True, slots=True)
class Keeping:
    """Whether one household is being worked on, and until when.

    There is nothing here about what is kept, only about the permission: what may be written
    down under it is decided by `panel/routes/experience.py`, at the one place where the
    other half already crosses the wire.
    """

    household_id: str
    until: float = 0.0
    set_by: str = ""
    set_at: float = 0.0

    def standing(self, now: float) -> bool:
        return self.until > now

    def to_public(self, now: float) -> dict[str, Any]:
        standing = self.standing(now)
        return {
            "householdId": self.household_id,
            "keeping": standing,
            "until": self.until if standing else 0.0,
            "daysAtATime": KEPT_FOR_DAYS,
            "setBy": self.set_by if standing else "",
        }


def kept_until(now: float) -> float:
    return now + KEPT_FOR_SECONDS


def granted(household_id: str, *, by: str, now: float) -> Keeping:
    return Keeping(household_id=household_id, until=kept_until(now), set_by=by, set_at=now)


def withdrawn(household_id: str, *, by: str, now: float) -> Keeping:
    """Off now, rather than off at the next renewal. Rows already written still lapse on
    their own instant: an administrator revoking a permission is not a delete button, and
    offering one here would be a route that erases a record."""
    return Keeping(household_id=household_id, until=0.0, set_by=by, set_at=now)


@runtime_checkable
class KeepingStore(Protocol):
    def get(self, household_id: str) -> Keeping: ...

    def set(self, keeping: Keeping) -> Keeping: ...


@dataclass
class InMemoryKeepingStore:
    """Enough to run the API and the tests. Obviously not a database."""

    _rows: dict[str, Keeping] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get(self, household_id: str) -> Keeping:
        with self._lock:
            found = self._rows.get(household_id)
            if found is None:
                return Keeping(household_id=household_id)
            if not found.standing(time.time()):
                # Lapsed is deleted, not remembered as off. See the module docstring.
                self._rows.pop(household_id, None)
                return Keeping(household_id=household_id)
            return found

    def set(self, keeping: Keeping) -> Keeping:
        with self._lock:
            if keeping.until:
                self._rows[keeping.household_id] = keeping
            else:
                self._rows.pop(keeping.household_id, None)
        return keeping


def kept_for(store: KeepingStore, household_id: str, now: float) -> float:
    """The instant rows written now would lapse at, or zero when nothing is being kept.

    One call at the one place that writes the other half, so that "is this household being
    worked on" and "how long does what I write last" are the same question and cannot drift
    apart into two answers.
    """
    if not store.get(household_id).standing(now):
        return 0.0
    return kept_until(now)
