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

    @property
    def title(self) -> str:
        return str(self.experience.get("title", ""))

    def to_public(self) -> dict[str, Any]:
        """What the parent is shown: the overview they judge it by, and the whole plan.

        Both, not one. Approval is given to the overview — that is what `ideas/08 §2`
        settled — but a parent who wants to read every branch must be able to, or the
        overview is the only thing that exists and the document is a claim about itself.
        """
        return {
            "id": self.id,
            "title": self.title,
            "overview": self.experience.get("overview", ""),
            "minutes": self.experience.get("minutes", 0),
            "createdAt": self.created_at,
            "state": self.state,
            "experience": self.experience,
            "decidedAt": self.decided_at,
            "decidedBy": self.decided_by,
            "note": self.note,
        }

    def to_device(self) -> dict[str, Any]:
        """What the house is given: the document, and nothing about who decided it."""
        return {"id": self.id, "experience": self.experience}


@runtime_checkable
class ExperienceStore(Protocol):
    def offer(self, record: OfferedExperience) -> OfferedExperience: ...

    def list(self, household_id: str, state: str | None = None) -> list[OfferedExperience]: ...

    def get(self, household_id: str, experience_id: str) -> OfferedExperience | None: ...

    def decide(
        self, household_id: str, experience_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> OfferedExperience: ...


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
            )
            self._rows[(household_id, experience_id)] = decided
        return decided
