"""Designing a sheet is a cloud call, so it happens here rather than in the house.

The same shape as :mod:`panel.wording` and for the same reason: the hub holds no Azure
credential, the gate lives beside the router, and a house asks the panel when it wants
something a model has to make. What comes back is a proposal — nothing here decides that
a sheet is printed.
"""

from __future__ import annotations

import os
import secrets

from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.pagedesign import PageDesign
from shared.proposal import Proposal
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose


async def design_sheet(
    topic: str,
    *,
    hints: dict[str, object],
    now: float,
    quad_w_mm: float = 178.0,
    quad_h_mm: float = 251.0,
) -> tuple[Proposal, PageDesign, ModelUsage | None]:
    """Ask for one designed sheet, and hand back the proposal, the design and the cost.

    The design is returned beside the proposal because the caller has to lay it out before
    it can know whether it fits and what it will cost in ink, and re-parsing the payload to
    find that out would be the same work done twice.

    Raises whatever the router raises when the cloud will not serve it, including
    :class:`~shared.errors.SafetyBlocked` when the gate refuses the page, and
    :class:`~shared.errors.UnusableGeneration` when what came back cannot be drawn.
    """
    from agents.sheet_designer import SheetDesigner, design_from
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    # As in `panel/wording.py`: the seal is not what the house trusts downstream, so a
    # per-process key keeps the gate honest without pretending the seal travels.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints=hints, now=now
    )
    try:
        proposal = await SheetDesigner().propose_sheet(
            context, topic=topic, quad_w_mm=quad_w_mm, quad_h_mm=quad_h_mm
        )
    finally:
        await gate.aclose()
    return proposal, design_from(proposal.payload), router.last_usage
