"""The series of pages this house has had read, and the state computed from it.

Two halves that never meet, which is the whole point. :mod:`agents.page_judge` is a model
looking at one page with nothing else in front of it, and what it answers lands here as one
row. :func:`shared.profile.read_from` is arithmetic over those rows and over how the
afternoons themselves went, and it holds no model at all. A state written by a model that
had been shown the previous state would be a state that agreed with itself.

**Nothing here is computed once and kept.** The rows are kept; the state is worked out from
the last few of them every time a prompt is built, which means there is exactly one place a
wrong pitch can come from and it is a function anybody can run by hand.

**It is the parent's to delete along with everything else.** ``forget`` empties the series
for a household, and the route that forgets what happened calls both — a memory a parent
cannot clear is what the panel exists not to build.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.profile import Noticed, Profile, Ran, read_from

from .what_happened import CLOSED, Afternoon

# How many rows are kept per household. Ten times the window the state is read off, so a
# thin stretch after a holiday still has something behind it, and bounded so that a house
# running for a year is not carrying four hundred rows to average eight of them.
KEPT = 80


@runtime_checkable
class NoticedStore(Protocol):
    def notice(self, household_id: str, noticed: Noticed) -> Noticed: ...

    def list(self, household_id: str) -> list[Noticed]: ...

    def forget(self, household_id: str) -> None: ...


@dataclass
class InMemoryNoticedStore:
    _rows: dict[str, list[Noticed]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def notice(self, household_id: str, noticed: Noticed) -> Noticed:
        with self._lock:
            series = self._rows.setdefault(household_id, [])
            series.append(noticed)
            del series[:-KEPT]
            return noticed

    def list(self, household_id: str) -> list[Noticed]:
        with self._lock:
            return list(self._rows.get(household_id, ()))

    def forget(self, household_id: str) -> None:
        with self._lock:
            self._rows.pop(household_id, None)


def how_long_it_was_meant_to_take(experience: dict[str, Any]) -> int:
    """The minutes the plan asked for, from the document the afternoon ran.

    Zero when the document cannot be read that way, which :func:`shared.profile.read_from`
    drops rather than treating as an afternoon of no length.
    """
    try:
        return max(0, int(experience.get("minutes") or 0))
    except (TypeError, ValueError):
        return 0


def runs_from(afternoons: Sequence[Afternoon], planned: dict[str, int]) -> tuple[Ran, ...]:
    """The span evidence: what each afternoon was meant to take against what it took.

    ``planned`` maps an experience id to the minutes its document asked for. An afternoon
    whose document is no longer in the store contributes nothing rather than being counted
    at a length nobody knows.
    """
    return tuple(
        Ran(
            planned_minutes=planned.get(one.experience_id, 0),
            minutes=one.minutes,
            carried_through=one.ending == CLOSED,
        )
        for one in afternoons
    )


def the_profile(
    notices: Sequence[Noticed], afternoons: Sequence[Afternoon], planned: dict[str, int]
) -> Profile:
    """Where this house sits now. One call, so callers cannot each assemble it differently."""
    return read_from(notices, runs_from(afternoons, planned))


def a_sheet_that_never_came_back(now: float | None = None) -> Noticed:
    """One row for a sheet that was handed over and did not return.

    A different fact from a page that came back blank, and the difference is an act: blank
    means somebody carried it to the glass. This one covers the sheet still on the table,
    the sheet in the bin, the afternoon walked away from — and the scanner in another room.
    Nothing can tell those apart, which is why :func:`shared.profile.read_from` only counts
    these in a house that has had a sheet come back at all.
    """
    return Noticed(at=time.time() if now is None else now, came_back=False)
