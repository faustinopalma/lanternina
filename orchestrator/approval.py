"""The approval ledger: what was proposed, and what the parent decided.

This module holds the ``PARENT_APPROVAL`` sealer. Agents are never handed a ledger, so
``decide`` is out of their reach by construction, not by convention.

Approving in advance is the normal case: the parent reviews a batch when it suits them,
and delivery happens later, on its own schedule. Approval records a decision; it does not
start anything.

TODO(poc): storage is in memory. It must become an append-only file or Cosmos record, or
a restart silently withdraws every approval the parent already gave.
"""

from __future__ import annotations

import time

from shared.approval import ApprovalDecision, ApprovalState, ApprovedItem
from shared.ids import LearnerId, ProposalId
from shared.proposal import Proposal, ProposalKind
from shared.seal import Sealer, SealPurpose


class InMemoryLedger:
    """An :class:`~shared.approval.ApprovalLedger` kept in process memory."""

    def __init__(self, sealer: Sealer) -> None:
        if sealer.purpose is not SealPurpose.PARENT_APPROVAL:
            raise ValueError(f"the ledger needs a PARENT_APPROVAL sealer, got {sealer.purpose}")
        self._sealer = sealer
        self._proposals: dict[ProposalId, Proposal] = {}
        self._decisions: dict[ProposalId, ApprovalDecision] = {}
        self._items: dict[ProposalId, ApprovedItem] = {}

    def submit(self, proposal: Proposal) -> None:
        self._proposals.setdefault(proposal.id, proposal)

    def pending(self, learner_id: LearnerId | None = None) -> list[Proposal]:
        waiting = [
            p
            for p in self._proposals.values()
            if p.id not in self._decisions and (learner_id is None or p.learner_id == learner_id)
        ]
        return sorted(waiting, key=lambda p: p.created_at)

    def decide(
        self,
        proposal_id: ProposalId,
        state: ApprovalState,
        *,
        decided_by: str,
        note: str = "",
    ) -> ApprovedItem | None:
        proposal = self._proposals.get(proposal_id)
        if proposal is None:
            raise KeyError(f"unknown proposal {proposal_id}")
        decision = ApprovalDecision(
            proposal_id=proposal_id,
            state=state,
            decided_by=decided_by,
            decided_at=time.time(),
            note=note,
        )
        self._decisions[proposal_id] = decision
        if state is not ApprovalState.APPROVED:
            self._items.pop(proposal_id, None)
            return None

        # The seal covers the proposal *and* its safety seal, so an approved payload
        # cannot be swapped for a different one afterwards.
        draft = {"proposal": proposal.sealable(), "decision": decision.to_dict()}
        item = ApprovedItem(proposal=proposal, decision=decision, seal=self._sealer.seal(draft))
        self._items[proposal_id] = item
        return item

    def approved(
        self, learner_id: LearnerId, kind: ProposalKind | None = None
    ) -> list[ApprovedItem]:
        now = time.time()
        live = [
            item
            for item in self._items.values()
            if item.proposal.learner_id == learner_id
            and (kind is None or item.proposal.kind == kind)
            and (item.proposal.expires_at is None or item.proposal.expires_at > now)
        ]
        return sorted(live, key=lambda i: i.decision.decided_at, reverse=True)

    def withdraw(self, proposal_id: ProposalId, *, decided_by: str, note: str = "") -> None:
        self.decide(proposal_id, ApprovalState.WITHDRAWN, decided_by=decided_by, note=note)
