"""The model calls this loop makes that the house never makes.

Two of them, and both are here rather than in `agents/` because neither is part of the
product: one stands in for an adolescent so an afternoon can be played with nobody in the
room, and one reads the transcript afterwards and scores it. Putting them in `agents/`
would put a judge of children's work inside a system whose first rule is that it does not
judge anybody.

They use the same router and the same gate as everything else, so a research run pays the
same safety cost the real path does and fails the same way when the cloud is not there.
"""

from __future__ import annotations

import json
import os
import secrets
from typing import Any

from shared.agents import AgentContext
from shared.ids import LearnerId, new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind
from shared.seal import Sealer, SealPurpose

SAYS = beside(__file__)

# Long enough for a page's worth of description, short enough that neither call can turn
# into an essay nobody reads.
MAX_ANSWER = 1200
MAX_APPRAISAL = 4000


def a_context(now: float) -> AgentContext:
    """A router and a gate, built the same way `panel/devising.py` builds them."""
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    return AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)


def _json_in(said: str) -> dict[str, Any]:
    """The object in an answer that may have arrived wrapped in a fence."""
    text = said.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError(f"no object in the answer: {said[:200]!r}")
    parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("the answer is not an object")
    return parsed


async def what_they_did(
    ctx: AgentContext,
    *,
    displays: list[str],
    sheet: str,
    mood: str,
    minutes_in: int,
) -> dict[str, Any]:
    """What a simulated adolescent does with a sheet: JSON with ``came``, ``onIt``, ``stop``.

    ``mood`` is the one dial. It is a property of a day and not of a person — *a day when
    nothing long will land* is a Tuesday, not a diagnosis — and it exists so that a run
    covers the branch where a sheet comes back blank, which is the branch a willing
    simulation never reaches and the one the format most needs exercised.
    """
    payload = await ctx.router.analyze(
        ModelRequest(
            capability=Capability.PLANNING,
            prompt=SAYS.text(
                "adolescent",
                displays="\n".join(displays),
                sheet=sheet,
                mood=mood,
                minutes=minutes_in,
            ),
            request_id=new_request_id(),
            max_output_chars=MAX_ANSWER,
            purpose="standing in for somebody, in research",
            content_kind=ContentKind.EXERCISE_JSON,
        )
    )
    return _json_in(payload.text)


async def appraise(ctx: AgentContext, *, transcript: str) -> dict[str, Any]:
    """Score one played afternoon on the axes in `research/appraisal.axes.md`."""
    payload = await ctx.router.analyze(
        ModelRequest(
            capability=Capability.PLANNING,
            prompt=SAYS.text("appraisal", transcript=transcript),
            request_id=new_request_id(),
            max_output_chars=MAX_APPRAISAL,
            purpose="scoring an afternoon, in research",
            content_kind=ContentKind.EXERCISE_JSON,
        )
    )
    return _json_in(payload.text)
