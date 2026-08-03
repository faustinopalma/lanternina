"""The approval layer's contract: the parent's decision, recorded and sealed.

Only the ledger implementation (``orchestrator/approval.py``) holds the
``PARENT_APPROVAL`` sealer, so only the ledger can mint an :class:`ApprovedItem` that
passes :func:`shared.delivery.assert_deliverable`.

Agents can call :meth:`ApprovalLedger.submit`; nothing else. They cannot call ``decide``
because they are never handed a ledger — see :class:`shared.agents.AgentContext`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from .ids import LearnerId, ProposalId
from .proposal import Proposal, ProposalKind
from .seal import Seal, SealPurpose


class ApprovalState(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"  # parent revoked something previously approved


@dataclass(frozen=True, slots=True)
class ApprovalDecision:
    proposal_id: ProposalId
    state: ApprovalState
    decided_by: str
    decided_at: float
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": str(self.proposal_id),
            "state": str(self.state),
            "decided_by": self.decided_by,
            "decided_at": self.decided_at,
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class ApprovedItem:
    """A proposal the parent greenlit. The only thing the delivery layer accepts."""

    proposal: Proposal
    decision: ApprovalDecision
    seal: Seal

    def __post_init__(self) -> None:
        if self.decision.state is not ApprovalState.APPROVED:
            raise ValueError(f"cannot build an ApprovedItem from state {self.decision.state}")
        if self.decision.proposal_id != self.proposal.id:
            raise ValueError("decision does not refer to this proposal")
        if self.seal.purpose is not SealPurpose.PARENT_APPROVAL:
            raise ValueError(f"item sealed for the wrong purpose: {self.seal.purpose}")

    def sealable(self) -> dict[str, Any]:
        return {"proposal": self.proposal.sealable(), "decision": self.decision.to_dict()}


@runtime_checkable
class ApprovalLedger(Protocol):
    """Append-only record of what was proposed and what the parent decided."""

    def submit(self, proposal: Proposal) -> None:
        """Queue a proposal for review. Idempotent on proposal id."""
        ...

    def pending(self, learner_id: LearnerId | None = None) -> list[Proposal]:
        """Proposals awaiting a decision, oldest first."""
        ...

    def decide(
        self,
        proposal_id: ProposalId,
        state: ApprovalState,
        *,
        decided_by: str,
        note: str = "",
    ) -> ApprovedItem | None:
        """Record the parent's decision. Returns a sealed item only when APPROVED."""
        ...

    def approved(
        self, learner_id: LearnerId, kind: ProposalKind | None = None
    ) -> list[ApprovedItem]:
        """Currently-valid approved items, newest first. Excludes withdrawn and expired."""
        ...

    def withdraw(self, proposal_id: ProposalId, *, decided_by: str, note: str = "") -> None:
        """Revoke a previous approval. Takes effect before the next delivery."""
        ...
