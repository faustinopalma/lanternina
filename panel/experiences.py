"""Afternoons a house has been offered, and the parent's decision on each.

An experience arrives here devised and already screened, and waits. What the parent reads
is the overview; what they decide is whether this afternoon may happen in their house at
all. Everything inside it then reaches an adolescent on the strength of that one decision,
which is the trade `ideas/08 §2` records rather than hides.

Deciding is inert. It writes a row and returns: no model is called, no work is enqueued,
nobody is notified. The house finds out on its next request, because it asked.

Not a :class:`~panel.proposals.ProposalRecord`, and the reason is one field. A proposal
carries a safety seal minted on the device with a key the cloud does not have, and the
home server verifies it after pulling. An experience is devised in the cloud, so the only
seal this container could mint is one nobody can check. A record with an unverifiable seal
in it is worse than a record with no seal field, so this is its own small store and the
house trusts the gate that ran here, over TLS, with a device key — the same trust the
reading of a page and the continuing of an afternoon already run on.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.approval import ApprovalState

# What a parent may do to an offered afternoon. Withdrawing an approved one is a second
# decision and it stops the house being handed it again; an afternoon already running is
# not reached by it, because nothing here can reach into a house.
DECIDABLE = (ApprovalState.APPROVED, ApprovalState.REJECTED, ApprovalState.WITHDRAWN)
WITHDRAWABLE_FROM = (ApprovalState.APPROVED.value,)


@dataclass(frozen=True, slots=True)
class OfferedExperience:
    """One devised afternoon, as the cloud keeps it."""

    id: str
    household_id: str
    # The whole document, exactly as `Experience.to_dict` wrote it. Kept whole rather than
    # in pieces because the parent approves this and the house runs this, and a document
    # reassembled from columns is not obviously the one that was read.
    experience: dict[str, Any]
    created_at: float
    state: str = ApprovalState.PENDING.value
    decided_at: float | None = None
    decided_by: str = ""
    note: str = ""
    # When the house began it. Not a decision — the state above is the parent's word and
    # stays theirs — but a fact about the house, and the only thing that keeps an approved
    # afternoon from being handed over again every day. Nothing about who did it, how far
    # they got or whether it finished: an afternoon that ends still leaves nothing.
    begun_at: float = 0.0

    @property
    def title(self) -> str:
        return str(self.experience.get("title", ""))

    def to_public(self) -> dict[str, Any]:
        """What the parent is shown: the idea they judge it by, and the whole plan.

        The idea is the overview, the themes and the strategy — what it is about and how it
        should go. That is what approval is given to, and `ideas/08 §2` settled it. The plan
        goes too, for a parent who wants to look; nothing may assume they did.
        """
        return {
            "id": self.id,
            "title": self.title,
            "overview": self.experience.get("overview", ""),
            "themes": list(self.experience.get("themes") or ()),
            "strategy": self.experience.get("strategy", ""),
            "minutes": self.experience.get("minutes", 0),
            "createdAt": self.created_at,
            "state": self.state,
            "experience": self.experience,
            "decidedAt": self.decided_at,
            "decidedBy": self.decided_by,
            "note": self.note,
            "begunAt": self.begun_at,
        }

    def to_device(self) -> dict[str, Any]:
        """What the house is given: the document, and nothing about who decided it."""
        return {"id": self.id, "experience": self.experience}


@dataclass(frozen=True, slots=True)
class Backlog:
    """How much is approved and not yet begun, and how far it carries.

    A parent sits down once and approves several, then may not open the panel for a week.
    What they need before closing it is not a list — it is one number that says whether the
    house has enough. ``days`` is that number: the stock divided by the days an afternoon
    may begin on, rounded down, so it is a floor and never a promise.

    It counts afternoons and minutes and nothing else. How many were run, how often, how
    long anybody spent: none of that is here, and none of it is anywhere.
    """

    approved: int
    minutes: int
    # Afternoons a week the rhythm allows. Zero when no day is chosen, and then `days` is
    # zero too — a stock that carries nowhere, which is the truth about a house that has
    # not said when anything may happen.
    per_week: int

    @property
    def days(self) -> int:
        if self.per_week <= 0 or self.approved <= 0:
            return 0
        return int(self.approved * 7 / self.per_week)

    def to_public(self) -> dict[str, Any]:
        return {
            "approved": self.approved,
            "minutes": self.minutes,
            "perWeek": self.per_week,
            "days": self.days,
        }


def backlog_of(rows: list[OfferedExperience], *, days_a_week: int) -> Backlog:
    """The stock a house is sitting on. Begun ones are spent and do not count."""
    waiting = [
        row
        for row in rows
        if row.state == ApprovalState.APPROVED.value and not row.begun_at
    ]
    return Backlog(
        approved=len(waiting),
        minutes=sum(int(row.experience.get("minutes", 0) or 0) for row in waiting),
        per_week=days_a_week,
    )


@runtime_checkable
class ExperienceStore(Protocol):
    def offer(self, record: OfferedExperience) -> OfferedExperience: ...

    def list(self, household_id: str, state: str | None = None) -> list[OfferedExperience]: ...

    def get(self, household_id: str, experience_id: str) -> OfferedExperience | None: ...

    def decide(
        self, household_id: str, experience_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> OfferedExperience: ...

    def begun(self, household_id: str, experience_id: str, at: float) -> OfferedExperience: ...


@dataclass
class InMemoryExperienceStore:
    """Enough to run the API and the tests. Obviously not a database."""

    _rows: dict[tuple[str, str], OfferedExperience] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def offer(self, record: OfferedExperience) -> OfferedExperience:
        with self._lock:
            key = (record.household_id, record.id)
            # Idempotent on id, so a house that retries does not stack up afternoons a
            # parent then has to refuse one by one.
            return self._rows.setdefault(key, record)

    def list(self, household_id: str, state: str | None = None) -> list[OfferedExperience]:
        with self._lock:
            rows = [
                row
                for (household, _), row in self._rows.items()
                if household == household_id and (state is None or row.state == state)
            ]
        return sorted(rows, key=lambda row: row.created_at)

    def get(self, household_id: str, experience_id: str) -> OfferedExperience | None:
        with self._lock:
            return self._rows.get((household_id, experience_id))

    def decide(
        self, household_id: str, experience_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> OfferedExperience:
        if not decided_by:
            raise ValueError("a decision must record who made it")
        with self._lock:
            current = self._rows[(household_id, experience_id)]
            decided = OfferedExperience(
                id=current.id,
                household_id=current.household_id,
                experience=current.experience,
                created_at=current.created_at,
                state=state,
                decided_at=time.time(),
                decided_by=decided_by,
                note=note,
                begun_at=current.begun_at,
            )
            self._rows[(household_id, experience_id)] = decided
        return decided

    def begun(self, household_id: str, experience_id: str, at: float) -> OfferedExperience:
        with self._lock:
            current = self._rows[(household_id, experience_id)]
            # The first time stands. A house that says it again is a retry, not a second
            # afternoon, and moving the moment would say something that is not true.
            if current.begun_at:
                return current
            started = OfferedExperience(
                id=current.id,
                household_id=current.household_id,
                experience=current.experience,
                created_at=current.created_at,
                state=current.state,
                decided_at=current.decided_at,
                decided_by=current.decided_by,
                note=current.note,
                begun_at=at,
            )
            self._rows[(household_id, experience_id)] = started
        return started
