"""Proposals as the cloud stores them, and the parent's decision on each.

What the cloud keeps is deliberately not a :class:`~shared.proposal.Proposal`: it holds
the screened payload and its safety seal as plain data, so the home server can verify the
seal itself after pulling. The **approval seal is never minted here** — it is minted on
the device with a key the cloud does not have. Losing the database would therefore cost
the record of what was decided, not the ability to forge a delivery.

Deciding is inert. It writes a row and returns. It calls no model, enqueues no work and
notifies nobody; the home server finds out on its next request, because it asked.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.approval import ApprovalState

# The states a parent can put a proposal into from the panel.
DECIDABLE = (ApprovalState.APPROVED, ApprovalState.REJECTED)


@dataclass(frozen=True, slots=True)
class ProposalRecord:
    id: str
    household_id: str
    kind: str
    agent: str
    rationale: str
    created_at: float
    # Exactly ScreenedPayload.sealable(), so the digest still matches after the round trip.
    payload: dict[str, Any]
    payload_seal: dict[str, Any]
    state: str = ApprovalState.PENDING.value
    decided_at: float | None = None
    decided_by: str = ""
    note: str = ""
    expires_at: float | None = None

    def to_public(self) -> dict[str, Any]:
        """What the panel shows the parent: the content, and why it was proposed."""
        return {
            "id": self.id,
            "kind": self.kind,
            "agent": self.agent,
            "rationale": self.rationale,
            "createdAt": self.created_at,
            "state": self.state,
            "contentKind": self.payload.get("kind", ""),
            "body": self.payload.get("body", ""),
            "decidedAt": self.decided_at,
            "decidedBy": self.decided_by,
            "note": self.note,
        }

    def to_device(self) -> dict[str, Any]:
        """Everything the home server needs to verify the safety seal for itself."""
        return {
            "id": self.id,
            "kind": self.kind,
            "agent": self.agent,
            "rationale": self.rationale,
            "createdAt": self.created_at,
            "state": self.state,
            "payload": self.payload,
            "payloadSeal": self.payload_seal,
            "expiresAt": self.expires_at,
        }


@runtime_checkable
class ProposalStore(Protocol):
    def submit(self, record: ProposalRecord) -> ProposalRecord: ...

    def list(self, household_id: str, state: str | None = None) -> list[ProposalRecord]: ...

    def decide(
        self, household_id: str, proposal_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> ProposalRecord: ...


@dataclass
class InMemoryProposalStore:
    """Enough to run the API and the tests. Obviously not a database."""

    _rows: dict[tuple[str, str], ProposalRecord] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def submit(self, record: ProposalRecord) -> ProposalRecord:
        with self._lock:
            key = (record.household_id, record.id)
            # Idempotent on id: a home server that retries must not create a second copy.
            return self._rows.setdefault(key, record)

    def list(self, household_id: str, state: str | None = None) -> list[ProposalRecord]:
        with self._lock:
            rows = [
                row
                for (household, _), row in self._rows.items()
                if household == household_id and (state is None or row.state == state)
            ]
        return sorted(rows, key=lambda row: row.created_at)

    def decide(
        self, household_id: str, proposal_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> ProposalRecord:
        if not decided_by:
            raise ValueError("a decision must record who made it")
        with self._lock:
            current = self._rows[(household_id, proposal_id)]
            decided = ProposalRecord(
                id=current.id,
                household_id=current.household_id,
                kind=current.kind,
                agent=current.agent,
                rationale=current.rationale,
                created_at=current.created_at,
                payload=current.payload,
                payload_seal=current.payload_seal,
                state=state,
                decided_at=time.time(),
                decided_by=decided_by,
                note=note,
                expires_at=current.expires_at,
            )
            self._rows[(household_id, proposal_id)] = decided
            return decided
