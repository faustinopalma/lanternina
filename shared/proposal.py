"""Proposals — the only thing an agent is allowed to produce.

Note what is *absent*: there is no `approved` flag, no `status` field, no `publish()`
method. An agent physically has nowhere to record that its own output is acceptable.
Approval state lives in the ledger (:mod:`shared.approval`), which agents do not hold.

A proposal is inert. It becomes deliverable only when the parent decides, and only via
:class:`~shared.approval.ApprovedItem`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .ids import LearnerId, ProposalId
from .safety import ScreenedPayload


class ProposalKind(StrEnum):
    EXERCISE = "exercise"
    ROUTINE_PROMPT = "routine_prompt"
    FEEDBACK = "feedback"
    SCHEDULE = "schedule"
    PRINT_LAYOUT = "print_layout"
    # A picture for a display. Approved by theme rather than one by one — see the
    # tradeoff recorded in tools/home_server.py.
    PICTURE = "picture"


@dataclass(frozen=True, slots=True)
class Proposal:
    """Something an agent suggests. Never something that happens."""

    id: ProposalId
    kind: ProposalKind
    agent: str
    learner_id: LearnerId
    payload: ScreenedPayload
    rationale: str
    created_at: float
    # After this instant the proposal is stale and the ledger will not accept a decision.
    expires_at: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def sealable(self) -> dict[str, Any]:
        """The structure the parent-approval seal covers."""
        return {
            "id": str(self.id),
            "kind": str(self.kind),
            "agent": self.agent,
            "learner_id": str(self.learner_id),
            "payload": self.payload.sealable(),
            "payload_seal": self.payload.seal.to_dict(),
            "created_at": self.created_at,
        }
