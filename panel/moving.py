"""One move of an afternoon that is already happening.

The twin of `panel/continuing.py`, and the difference between them is what they are given.
The continuer is handed a branch the plan wrote and asked to write the moments after it;
this is handed the strategy and what has happened and asked for one act. One is filling in
a blank the plan left; the other is answering a room the plan did not foresee.

Screened on the way out like everything else, through the router's own gate. There is no
repair: somebody is standing there, and the caller has the written plan to fall back on.
"""

from __future__ import annotations

import os
import secrets
from collections.abc import Mapping, Sequence
from typing import Any

from agents.experience_agent import ExperienceAgent, Move
from shared.agents import AgentContext
from shared.domain import LearnerId
from shared.experience import Experience
from shared.seal import Sealer, SealPurpose


async def decide_a_move(
    *,
    afternoon: Experience,
    happened: Sequence[Mapping[str, Any]],
    minutes_left: int,
    now: float = 0.0,
) -> tuple[Move, Any]:
    """The next move, and what the call consumed. Raises what the agent raises."""
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # An empty learner and empty hints, as in `panel/continuing.py`: an afternoon carries
    # nothing about a person, and handing the agent nothing is the cheapest way to keep
    # that true as the prompt changes.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    try:
        move = await ExperienceAgent().next_move(
            context,
            strategy=afternoon.strategy,
            themes=afternoon.themes,
            # The plan goes as it was approved, for reference. An agent that could not see
            # it would be improvising against a strategy alone, and the strategy is a page.
            plan=afternoon.to_dict(),
            tools=afternoon.requires,
            happened=happened,
            minutes_left=minutes_left,
        )
    finally:
        await gate.aclose()
    return move, router.last_usage
