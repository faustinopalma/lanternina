"""What the home server offers for review, and what the parent decided about it.

Nothing here shows anything to anybody. A proposal arrives sealed exactly as the gate left
it, waits, and leaves again only because the house came back and asked.
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from shared.approval import ApprovalState

from ..gate import CurrentAccount, DeviceKey
from ..proposals import DECIDABLE, ProposalRecord, ProposalStore
from . import Decision

router = APIRouter()


class SubmittedProposal(BaseModel):
    """What the home server sends up for review, sealed exactly as the gate left it."""

    id: str
    kind: str
    agent: str
    rationale: str = ""
    createdAt: float = 0.0
    payload: dict[str, Any] = Field(default_factory=dict)
    payloadSeal: dict[str, Any] = Field(default_factory=dict)
    expiresAt: float | None = None


@router.get("/api/proposals")
def list_proposals(account: CurrentAccount, request: Request, state: str = "pending") -> Any:
    store: ProposalStore = request.app.state.proposals
    rows = store.list(str(account.household_id), state or None)
    return {"proposals": [row.to_public() for row in rows]}


@router.post("/api/proposals/{proposal_id}/decision")
def decide_proposal(
    proposal_id: str, decision: Decision, account: CurrentAccount, request: Request
) -> Any:
    """Record what the parent decided. This is the whole effect: it starts nothing."""
    if decision.state not in {s.value for s in DECIDABLE}:
        raise HTTPException(status_code=400, detail="unsupported_state")
    store: ProposalStore = request.app.state.proposals
    try:
        row = store.decide(
            str(account.household_id),
            proposal_id,
            decision.state,
            decided_by=str(account.id),
            note=decision.note,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="unknown_proposal") from exc
    return row.to_public()


@router.post("/api/device/{household_id}/proposals")
def submit_proposals(
    household_id: str, submitted: list[SubmittedProposal], _: DeviceKey, request: Request
) -> Any:
    """The home server offers a batch for review. Nothing is shown to anyone yet."""
    store: ProposalStore = request.app.state.proposals
    stored = [
        store.submit(
            ProposalRecord(
                id=item.id,
                household_id=household_id,
                kind=item.kind,
                agent=item.agent,
                rationale=item.rationale,
                created_at=item.createdAt or time.time(),
                payload=item.payload,
                payload_seal=item.payloadSeal,
                expires_at=item.expiresAt,
            )
        )
        for item in submitted
    ]
    return {"stored": [row.id for row in stored]}


@router.get("/api/device/{household_id}/proposals")
def device_proposals(
    household_id: str,
    _: DeviceKey,
    request: Request,
    state: str = ApprovalState.APPROVED.value,
) -> Any:
    """What the home server asked for. It pulls; nothing is ever pushed to the house."""
    store: ProposalStore = request.app.state.proposals
    rows = store.list(household_id, state or None)
    return {"proposals": [row.to_device() for row in rows]}
