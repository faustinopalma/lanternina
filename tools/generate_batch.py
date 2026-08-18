"""Generate a batch of proposals and show what the parent would be asked to approve.

The batch is the normal case, not a demo shortcut: the parent reviews several days' worth
of material in one sitting, and delivery happens later, on its own schedule.

Run it with the venv active::

    python -m tools.generate_batch --exercises 2 --prompts 2 --render build/display.png

Everything it prints comes back from Azure AI Foundry and has passed the content-safety
gate. Nothing here approves anything on the parent's behalf except the ``--approve-all``
flag, which exists so the display render has something to draw and says so when used.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import secrets
import sys
import time
from pathlib import Path

from agents.content import HouseholdContentAgent
from orchestrator.approval import InMemoryLedger
from orchestrator.router import FoundryConfig, FoundryRouter
from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
from shared.agents import AgentContext
from shared.approval import ApprovalState
from shared.domain import ActivityKind, ContentVariety, Difficulty, LearnerProfile
from shared.errors import SafetyBlocked, UnusableGeneration
from shared.exercise import CHOICES, EXERCISES, INSTRUCTIONS, QUESTION, TITLE, field
from shared.ids import LearnerId
from shared.proposal import Proposal, ProposalKind
from shared.seal import Sealer, SealPurpose

# Synthetic on purpose: no real profile belongs in this repository. See the working rules.
DEMO_PROFILE = LearnerProfile(
    id=LearnerId("lr_demo"),
    display_name="Profilo di prova",
    interests=("animali", "cucina", "spazio"),
    avoid=("temporali", "rumori forti"),
    default_difficulty=Difficulty.GENTLE,
    content_variety=ContentVariety.BALANCED,
    max_words_per_line=6,
    language="it",
)

TOPICS = ("gli animali del bosco", "preparare la merenda", "i pianeti", "i colori in cucina")
ROUTINE_STEPS = (("mettere in ordine lo zaino", "17:30"), ("bere un bicchiere d'acqua", "11:00"))


def _keys() -> tuple[bytes, bytes]:
    """Device-local HMAC keys. Ephemeral here; on the mini-PC they come from .env."""
    safety = os.environ.get("LANTERNINA_SAFETY_KEY", "")
    approval = os.environ.get("LANTERNINA_APPROVAL_KEY", "")
    if not safety or not approval:
        print("no seal keys in the environment: using ephemeral ones for this run only\n")
        return secrets.token_bytes(32), secrets.token_bytes(32)
    return safety.encode(), approval.encode()


def _show(proposal: Proposal, index: int) -> None:
    payload = proposal.payload
    severities = ", ".join(f"{k}={v}" for k, v in sorted(payload.record.severities.items()))
    print(f"\n{'=' * 78}")
    print(f"[{index}] {proposal.kind}  ·  id {proposal.id}  ·  agente {proposal.agent}")
    print(f"     perche: {proposal.rationale}")
    print(f"     screening: {payload.record.verdict} ({severities or 'nessuna categoria'})")
    print(f"     sigillo sicurezza: {payload.seal.signature[:16]}…")
    print("-" * 78)
    if payload.kind.value.endswith("json"):
        content = json.loads(payload.body)
        print(f"  {field(content, TITLE, '')}")
        print(f"  {field(content, INSTRUCTIONS, '')}")
        for entry in field(content, EXERCISES, []):
            print(f"   · {field(entry, QUESTION, '')}")
            for choice in field(entry, CHOICES, []):
                print(f"       [ ] {choice}")
    else:
        print(f"  {payload.body.strip()}")


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exercises", type=int, default=2)
    parser.add_argument("--prompts", type=int, default=2)
    parser.add_argument("--approve-all", action="store_true")
    parser.add_argument("--render", type=Path, default=None)
    parser.add_argument(
        "--render-kind",
        choices=[k.value for k in ProposalKind],
        default=ProposalKind.ROUTINE_PROMPT.value,
    )
    args = parser.parse_args()

    safety_key, approval_key = _keys()
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(dict(os.environ)),
        Sealer(SealPurpose.CONTENT_SAFETY, safety_key, "orchestrator.safety"),
    )
    try:
        return await _run(args, gate, safety_key, approval_key)
    finally:
        await gate.aclose()


async def _run(
    args: argparse.Namespace,
    gate: AzureContentSafetyGate,
    safety_key: bytes,
    approval_key: bytes,
) -> int:
    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)), gate=gate)
    agent = HouseholdContentAgent()
    ledger = InMemoryLedger(Sealer(SealPurpose.PARENT_APPROVAL, approval_key, "parent-panel"))
    ctx = AgentContext.for_learner(router, DEMO_PROFILE, time.time())

    started = time.perf_counter()
    produced: list[Proposal] = []
    for index in range(args.exercises):
        try:
            produced.append(
                await agent.propose_exercise(
                    ctx,
                    kind=ActivityKind.PRINTED_EXERCISE,
                    difficulty=DEMO_PROFILE.default_difficulty,
                    topic_hint=TOPICS[index % len(TOPICS)],
                )
            )
        except (SafetyBlocked, UnusableGeneration) as exc:
            print(f"scartata una proposta: {type(exc).__name__}: {exc}")
    for index in range(args.prompts):
        label, at = ROUTINE_STEPS[index % len(ROUTINE_STEPS)]
        try:
            produced.append(await agent.propose_routine_prompt(ctx, step_label=label, at=at))
        except (SafetyBlocked, UnusableGeneration) as exc:
            print(f"scartata una proposta: {type(exc).__name__}: {exc}")

    for proposal in produced:
        ledger.submit(proposal)
    for index, proposal in enumerate(ledger.pending(), start=1):
        _show(proposal, index)

    elapsed = time.perf_counter() - started
    print(f"\n{'=' * 78}")
    print(f"{len(produced)} proposte in attesa · generate in {elapsed:.1f}s")

    if args.approve_all:
        print("--approve-all: sto decidendo al posto del genitore, solo per questa prova")
        for proposal in ledger.pending():
            ledger.decide(proposal.id, ApprovalState.APPROVED, decided_by="demo", note="prova")

    if args.render:
        items = ledger.approved(DEMO_PROFILE.id, ProposalKind(args.render_kind))
        if not items:
            print(f"niente da disegnare: nessuna proposta {args.render_kind} approvata")
            return 0
        from devices.epaper import render_epaper_bmp, render_epaper_png

        render = render_epaper_bmp if args.render.suffix.lower() == ".bmp" else render_epaper_png
        image = render(items[-1], safety_key=safety_key, approval_key=approval_key)
        args.render.parent.mkdir(parents=True, exist_ok=True)
        args.render.write_bytes(image)
        print(f"display: {args.render} ({len(image)} byte, 800x480, 1 bit)")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
