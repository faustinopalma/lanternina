"""The delivery boundary: what may reach the learner, and what must not.

Each test is an attack. If any of them starts passing content through, the guarantee the
README makes to a parent has quietly stopped being true.
"""

from __future__ import annotations

import time

import pytest

from shared.approval import ApprovalDecision, ApprovalState, ApprovedItem
from shared.delivery import assert_deliverable, is_deliverable
from shared.errors import NotApprovedError, SealVerificationError
from shared.ids import LearnerId, new_proposal_id
from shared.proposal import Proposal, ProposalKind
from shared.safety import ContentKind, SafetyVerdict, ScreenedPayload, ScreeningRecord
from shared.seal import SealPurpose, Sealer

SAFETY_KEY = b"safety-key-for-tests"
APPROVAL_KEY = b"approval-key-for-tests"


def _screened(body: str = "Ecco tre parole da ricopiare.") -> ScreenedPayload:
    record = ScreeningRecord(
        verdict=SafetyVerdict.ALLOW, screener="test-gate", policy_version="1", screened_at=time.time()
    )
    gate = Sealer(SealPurpose.CONTENT_SAFETY, SAFETY_KEY, "test-gate")
    unsealed = {"kind": str(ContentKind.FEEDBACK_TEXT), "body": body, "record": record.to_dict()}
    return ScreenedPayload(ContentKind.FEEDBACK_TEXT, body, record, gate.seal(unsealed))


def _proposal(payload: ScreenedPayload, expires_at: float | None = None) -> Proposal:
    return Proposal(
        id=new_proposal_id(),
        kind=ProposalKind.FEEDBACK,
        agent="content",
        learner_id=LearnerId("learner-1"),
        payload=payload,
        rationale="short and specific to the page",
        created_at=time.time(),
        expires_at=expires_at,
    )


def _approve(proposal: Proposal) -> ApprovedItem:
    decision = ApprovalDecision(proposal.id, ApprovalState.APPROVED, "parent", time.time())
    ledger = Sealer(SealPurpose.PARENT_APPROVAL, APPROVAL_KEY, "test-ledger")
    seal = ledger.seal({"proposal": proposal.sealable(), "decision": decision.to_dict()})
    return ApprovedItem(proposal, decision, seal)


def test_screened_and_approved_content_is_delivered() -> None:
    item = _approve(_proposal(_screened()))
    assert_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)
    assert is_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)


def test_an_agent_cannot_forge_an_approval() -> None:
    """An agent holds neither key, so it can build the object but not a valid seal."""
    proposal = _proposal(_screened())
    decision = ApprovalDecision(proposal.id, ApprovalState.APPROVED, "content-agent", time.time())
    forged = Sealer(SealPurpose.PARENT_APPROVAL, b"a-key-the-agent-invented", "content-agent")
    item = ApprovedItem(
        proposal, decision, forged.seal({"proposal": proposal.sealable(), "decision": decision.to_dict()})
    )
    with pytest.raises(SealVerificationError):
        assert_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)


def test_content_cannot_be_swapped_after_approval() -> None:
    """The approval seal covers the safety seal, so approving something mild and
    substituting something else afterwards does not survive delivery."""
    original = _proposal(_screened("Ecco tre parole da ricopiare."))
    item = _approve(original)

    swapped_payload = ScreenedPayload(
        original.payload.kind, "something else entirely", original.payload.record, original.payload.seal
    )
    swapped = Proposal(
        id=original.id,
        kind=original.kind,
        agent=original.agent,
        learner_id=original.learner_id,
        payload=swapped_payload,
        rationale=original.rationale,
        created_at=original.created_at,
    )
    with pytest.raises(SealVerificationError):
        assert_deliverable(
            ApprovedItem(swapped, item.decision, item.seal),
            safety_key=SAFETY_KEY,
            approval_key=APPROVAL_KEY,
        )


def test_unscreened_content_cannot_become_a_payload() -> None:
    """A BLOCK or REVIEW verdict cannot be wrapped into deliverable content at all."""
    seal = Sealer(SealPurpose.CONTENT_SAFETY, SAFETY_KEY, "test-gate").seal({})
    for verdict in (SafetyVerdict.BLOCK, SafetyVerdict.REVIEW):
        with pytest.raises(ValueError):
            ScreenedPayload(ContentKind.PLAIN_TEXT, "...", ScreeningRecord(verdict=verdict), seal)


def test_a_seal_issued_for_one_purpose_does_not_work_for_the_other() -> None:
    """Keeping the two keys distinct is what stops the safety gate minting approvals."""
    proposal = _proposal(_screened())
    decision = ApprovalDecision(proposal.id, ApprovalState.APPROVED, "parent", time.time())
    wrong_purpose = Sealer(SealPurpose.CONTENT_SAFETY, APPROVAL_KEY, "test-gate")
    with pytest.raises(ValueError):
        ApprovedItem(proposal, decision, wrong_purpose.seal({}))


def test_only_an_approved_decision_can_be_delivered() -> None:
    proposal = _proposal(_screened())
    for state in (ApprovalState.PENDING, ApprovalState.REJECTED, ApprovalState.WITHDRAWN):
        with pytest.raises(ValueError):
            ApprovedItem(
                proposal,
                ApprovalDecision(proposal.id, state, "parent", time.time()),
                Sealer(SealPurpose.PARENT_APPROVAL, APPROVAL_KEY, "test-ledger").seal({}),
            )


def test_an_expired_approval_stops_being_deliverable() -> None:
    item = _approve(_proposal(_screened(), expires_at=time.time() - 1))
    with pytest.raises(NotApprovedError):
        assert_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)
    assert not is_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)
