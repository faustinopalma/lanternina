"""Continuing an afternoon, because the house asked what happens next.

Why here and not in the house: this container holds the managed identity with access to
Foundry and to Content Safety, so nothing in the home needs a credential of its own. It is
the same reason `panel/wording.py` is here, and the gate is the reason the two are alike
rather than the two being alike by habit.

The gate matters more on this path than on any other, and the sentence is worth writing
out. A parent approves an experience once, from its overview. What a continuation puts on
a display and on paper is therefore seen by no adult before an adolescent sees it, so
``screen_continuation`` is the only thing between a model and a person. It is called here,
after the moments have been parsed and before they are handed back.

When this runs is not decided here. A write from the panel is inert, so nothing in the
panel can start an afternoon or extend one: this is answered inside the reply to the
request the hub made when a page came off its own glass.
"""

from __future__ import annotations

import os
import secrets
from typing import Any

from shared.agents import AgentContext
from shared.experience import Continuation
from shared.experience_checks import check
from shared.ids import LearnerId
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose

from .devising import RefusedByTheChecks
from .guidelines import FIXED


async def continue_experience(
    *,
    experience: dict[str, Any],
    after: str,
    came: str,
    reading: dict[str, Any],
    now: float,
    household_bounds: str = "",
) -> tuple[Continuation, ModelUsage | None]:
    """The rest of the afternoon, screened, and what the call consumed.

    ``household_bounds`` is what this house has written about what may be changed on the
    fly, already quoted by :meth:`~panel.guidelines.Guidelines.as_material`. The fixed
    bounds are not a parameter: they are ours, they hold in every household, and a caller
    that forgot them would be handing out the licence to improvise with only a parent's
    sentences behind it.

    Raises whatever the router raises when the cloud will not serve it,
    :class:`~shared.errors.SafetyBlocked` when the gate refuses what came back, and
    :class:`~shared.experience.ExperienceError` when it is not a continuation at all.
    """
    from agents.experience_continuer import ExperienceContinuer
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import (
        AzureContentSafetyGate,
        ContentSafetyConfig,
        screen_continuation,
    )

    environment = dict(os.environ)
    # The seal this gate mints is not used downstream: the hub plays moments, not a sealed
    # payload, exactly as it draws from strings on the reminder path. A per-process key
    # keeps the gate honest without pretending the seal travels anywhere.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # An empty learner and empty hints: an experience carries nothing about a person and
    # handing the agent nothing is the cheapest way to keep that true as the prompt changes.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    try:
        carrying_on = await ExperienceContinuer().continue_from(
            context,
            experience=experience,
            after=after,
            came=came,
            reading=reading,
            bounds=FIXED,
            household_bounds=household_bounds,
        )
        # The same checks the whole afternoon passed, on the half nobody approved. There is
        # no repair here and there will not be one: somebody is standing at the scanner, a
        # second model call is another fifteen seconds, and an afternoon that is not
        # continued stops — which is what an afternoon nobody continues does anyway.
        complaints = check(carrying_on)
        if complaints:
            raise RefusedByTheChecks(complaints)
        # The chokepoint. Nothing below this line may be skipped by an early return above
        # it: the parse and the checks can refuse, but only screening lets something through.
        await screen_continuation(gate, carrying_on, context=f"continuing after {after}")
    finally:
        await gate.aclose()
    return carrying_on, router.last_usage
