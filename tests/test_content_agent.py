"""The content path, from generation to what may be delivered.

These tests use the real gate and the real ledger with a stubbed severity analyzer, so
the seals exercised here are the ones production mints. Nothing reaches the network.
"""

from __future__ import annotations

import json
import time

import pytest

from agents.content import HouseholdContentAgent
from orchestrator.approval import InMemoryLedger
from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
from shared.agents import AgentContext
from shared.approval import ApprovalState
from shared.delivery import assert_deliverable, is_deliverable
from shared.domain import ActivityKind, Difficulty, LearnerProfile
from shared.errors import SafetyBlocked, UnusableGeneration
from shared.ids import LearnerId
from shared.proposal import ProposalKind
from shared.routing import ModelRequest
from shared.safety import ContentKind, SafetyCategory, ScreenedPayload
from shared.seal import Sealer, SealPurpose

SAFETY_KEY = b"safety-key-for-tests"
APPROVAL_KEY = b"approval-key-for-tests"

EXERCISE_JSON = json.dumps(
    {
        "titolo": "Animali",
        "istruzioni": "Barra una scelta.",
        "esercizi": [{"domanda": "Chi ha gli aculei?", "scelte": ["riccio", "volpe"]}],
        "perche": "tema scelto dal genitore",
    }
)


def _gate(severities: dict[SafetyCategory, int] | None = None) -> AzureContentSafetyGate:
    async def analyzer(text: str) -> dict[SafetyCategory, int]:
        return severities or {c: 0 for c in (SafetyCategory.HATE, SafetyCategory.VIOLENCE)}

    return AzureContentSafetyGate(
        ContentSafetyConfig(endpoint="https://example.invalid"),
        Sealer(SealPurpose.CONTENT_SAFETY, SAFETY_KEY, "test-gate"),
        analyzer=analyzer,
    )


class _ScreeningRouter:
    """A router that answers from a script but screens exactly like the real one."""

    def __init__(self, gate: AzureContentSafetyGate, reply: str) -> None:
        self._gate = gate
        self._reply = reply

    async def generate_for_user(self, request: ModelRequest) -> ScreenedPayload:
        return await self._gate.screen(request.content_kind, self._reply)


def _context(
    reply: str = EXERCISE_JSON, gate: AzureContentSafetyGate | None = None
) -> AgentContext:
    profile = LearnerProfile(id=LearnerId("lr_test"), display_name="Test", interests=("animali",))
    return AgentContext.for_learner(_ScreeningRouter(gate or _gate(), reply), profile, time.time())


async def test_gate_refuses_anything_the_detector_flags() -> None:
    gate = _gate({SafetyCategory.VIOLENCE: 2})
    with pytest.raises(SafetyBlocked):
        await gate.screen(ContentKind.PLAIN_TEXT, "whatever")


async def test_agent_wraps_a_screened_payload_and_signs_its_own_name() -> None:
    proposal = await HouseholdContentAgent().propose_exercise(
        _context(), kind=ActivityKind.PRINTED_EXERCISE, difficulty=Difficulty.GENTLE
    )
    assert proposal.kind is ProposalKind.EXERCISE
    assert proposal.agent == "content"
    assert proposal.payload.kind is ContentKind.EXERCISE_JSON
    assert proposal.rationale


async def test_malformed_generation_is_dropped_rather_than_repaired() -> None:
    """The body cannot be edited into shape: doing so would break the safety seal."""
    with pytest.raises(UnusableGeneration):
        await HouseholdContentAgent().propose_exercise(
            _context(reply="Ecco il tuo esercizio!"),
            kind=ActivityKind.PRINTED_EXERCISE,
            difficulty=Difficulty.GENTLE,
        )


async def test_only_an_approved_proposal_becomes_deliverable() -> None:
    proposal = await HouseholdContentAgent().propose_exercise(
        _context(), kind=ActivityKind.PRINTED_EXERCISE, difficulty=Difficulty.GENTLE
    )
    ledger = InMemoryLedger(Sealer(SealPurpose.PARENT_APPROVAL, APPROVAL_KEY, "panel"))
    ledger.submit(proposal)
    assert [p.id for p in ledger.pending()] == [proposal.id]

    item = ledger.decide(proposal.id, ApprovalState.APPROVED, decided_by="parent")
    assert item is not None
    assert_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)
    assert ledger.pending() == []

    ledger.withdraw(proposal.id, decided_by="parent")
    assert ledger.approved(proposal.learner_id) == []


async def test_content_swapped_after_approval_cannot_be_delivered() -> None:
    """Approval covers the payload, so an approved item cannot carry different words."""
    from dataclasses import replace

    proposal = await HouseholdContentAgent().propose_exercise(
        _context(), kind=ActivityKind.PRINTED_EXERCISE, difficulty=Difficulty.GENTLE
    )
    ledger = InMemoryLedger(Sealer(SealPurpose.PARENT_APPROVAL, APPROVAL_KEY, "panel"))
    ledger.submit(proposal)
    item = ledger.decide(proposal.id, ApprovalState.APPROVED, decided_by="parent")
    assert item is not None

    tampered = replace(
        item,
        proposal=replace(proposal, payload=replace(proposal.payload, body="testo sostituito")),
    )
    assert not is_deliverable(tampered, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)


async def test_a_rejected_proposal_yields_nothing_to_deliver() -> None:
    proposal = await HouseholdContentAgent().propose_exercise(
        _context(), kind=ActivityKind.PRINTED_EXERCISE, difficulty=Difficulty.GENTLE
    )
    ledger = InMemoryLedger(Sealer(SealPurpose.PARENT_APPROVAL, APPROVAL_KEY, "panel"))
    ledger.submit(proposal)
    assert ledger.decide(proposal.id, ApprovalState.REJECTED, decided_by="parent") is None
    assert ledger.approved(proposal.learner_id) == []
