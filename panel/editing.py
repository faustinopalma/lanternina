"""One turn of a parent working on an idea, and turning a finished one into an afternoon.

Two things live here because they are the two halves of the same feature. Rewriting is a
model call that produces text a parent reads and edits; approving is the deviser being
handed that text as a brief, and what comes back is checked and screened exactly like an
afternoon nobody steered — `panel/devising.py` does the work, and this passes the brief.

**A rewrite is not screened by the gate and does not need to be.** What comes back is shown
to the parent, who asked for it and is looking at it, and it reaches nobody else until they
approve — and approval goes through `devise_experience`, which screens. Screening twice
would cost a call on every turn of a conversation to protect an adult from words they
requested. `ideas/04 §21` is the same argument: the provider moderates its own output, and
we do not build a second system beside it.
"""

from __future__ import annotations

import os
import secrets
from collections.abc import Sequence
from typing import Any

from agents.idea_editor import Idea, IdeaEditor, idea_in
from shared.agents import AgentContext
from shared.capabilities import HouseCapability
from shared.domain import LearnerId
from shared.experience import Experience
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose


async def rewrite_the_idea(
    *,
    language: str,
    title: str,
    overview: str,
    themes: Sequence[str],
    script: str,
    said: Sequence[Any],
    asking: str,
    now: float = 0.0,
) -> tuple[Idea, ModelUsage | None]:
    """The idea as the parent's message leaves it, and what the call consumed."""
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # An empty learner and empty hints. A draft carries nothing about a person and this is
    # the cheapest way to keep that true as the prompt changes.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    try:
        answer = await IdeaEditor().ask(
            context,
            language=language,
            title=title,
            overview=overview,
            themes=themes,
            script=script,
            said=said,
            asking=asking,
        )
    finally:
        await gate.aclose()
    return idea_in(answer), router.last_usage


async def afternoon_from(
    *,
    brief: str,
    capabilities: frozenset[HouseCapability],
    language: str,
    interests: tuple[str, ...],
    avoid: tuple[str, ...],
    difficulty: str,
    variety: str,
    note: str,
    now: float,
) -> tuple[Experience, ModelUsage | None]:
    """Turn a parent's finished idea into an afternoon a house can run.

    The same path a devised afternoon takes, with the brief added: checked, repaired once
    if it has to be, screened. Nothing is relaxed because a parent wrote it — a script
    asking for a scoreboard is refused by the same check either way, and a parent who is
    told so can change it and try again.

    ``already``, ``recent`` and ``subjects`` are deliberately empty. Those exist to stop
    the house being handed the same afternoon twice on its own rhythm; this one was asked
    for by name, and telling the model not to write what it has just been told to write is
    the wrong instruction.
    """
    from .devising import devise_experience

    return await devise_experience(
        brief=brief,
        capabilities=capabilities,
        language=language,
        interests=interests,
        avoid=avoid,
        difficulty=difficulty,
        variety=variety,
        note=note,
        already=(),
        now=now,
    )
