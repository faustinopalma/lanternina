"""Devising an afternoon, because the house asked whether there was one to be had.

Why here and not in the house: this container holds the managed identity with access to
Foundry and to Content Safety, so nothing in the home needs a credential of its own. The
same reason `panel/continuing.py` and `panel/wording.py` are here.

When this runs is not decided here, and that is the rule this feature would break if it
were. A write from the panel is inert, so a parent asking for an afternoon cannot cause
one to be written: nothing in the panel calls this. It is called inside the reply to a
request the hub made, on the rhythm the hub already has, and what comes back waits for a
parent to read it.

The gate is called before the document is stored, not before it is played. An experience
sits in the panel where a parent reads it, so screening it late would mean an adult was
shown model output nobody had looked at — and by then the same words have been stored.
"""

from __future__ import annotations

import os
import secrets

from shared.agents import AgentContext
from shared.capabilities import HouseCapability
from shared.experience import Experience
from shared.ids import LearnerId
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose


async def devise_experience(
    *,
    capabilities: frozenset[HouseCapability],
    language: str,
    interests: tuple[str, ...],
    avoid: tuple[str, ...],
    already: tuple[str, ...],
    now: float,
) -> tuple[Experience, ModelUsage | None]:
    """One afternoon, screened, and what the call consumed.

    Raises whatever the router raises when the cloud will not serve it,
    :class:`~shared.errors.SafetyBlocked` when the gate refuses it, and
    :class:`~shared.experience.ExperienceError` when it is not an experience at all.
    """
    from agents.experience_deviser import ExperienceDeviser
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import (
        AzureContentSafetyGate,
        ContentSafetyConfig,
        screen_experience,
    )

    environment = dict(os.environ)
    # As on the continuing path: the seal this gate mints travels nowhere, because the
    # house is handed moments and not a sealed payload. A per-process key keeps the gate
    # honest without pretending otherwise.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # An empty learner and empty hints: an experience carries nothing about a person, and
    # handing the agent nothing is the cheapest way to keep that true as the prompt grows.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    try:
        experience = await ExperienceDeviser().devise(
            context,
            capabilities=capabilities,
            language=language,
            interests=interests,
            avoid=avoid,
            already=already,
        )
        # The chokepoint. Nothing above it may return early past it: the parse can refuse,
        # but only screening lets something through.
        await screen_experience(gate, experience, context="devising an afternoon")
    finally:
        await gate.aclose()
    return experience, router.last_usage
