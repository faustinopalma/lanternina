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
from shared.experience import Continuation, Experience
from shared.experience_checks import check
from shared.ids import LearnerId
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose

from .devising import RefusedByTheChecks
from .guidelines import FIXED


def _up_to(experience: dict[str, Any], after: str) -> tuple[str, ...]:
    """Everything the afternoon put in front of somebody up to and including ``after``.

    A document that will not parse yields nothing rather than raising: the continuer is
    about to be handed the same document and its refusal is the one worth reading.
    """
    try:
        whole = Experience.from_dict(experience)
    except Exception:
        return ()
    said: list[str] = []
    for moment in whole.moments:
        said.extend(moment.words_before_the_way_out)
        if moment.id == after:
            break
    return tuple(said)


async def continue_experience(
    *,
    experience: dict[str, Any],
    after: str,
    came: str,
    reading: dict[str, Any],
    now: float,
    household_bounds: str = "",
    pitch: str = "",
) -> tuple[Continuation, ModelUsage | None]:
    """The rest of the afternoon, screened, and what the call consumed.

    ``household_bounds`` is what this house has written about what may be changed on the
    fly, already quoted by :meth:`~panel.guidelines.Guidelines.as_material`. The fixed
    bounds are not a parameter: they are ours, they hold in every household, and a caller
    that forgot them would be handing out the licence to improvise with only a parent's
    sentences behind it.

    ``pitch`` is where this house sits, from :meth:`shared.profile.Profile.as_material`. It
    is the one thing here that is about the person rather than about the afternoon, and it
    reaches the model and nothing else — `shared/blocklist.py` refuses a sentence that tells
    the reader the afternoon was fitted to them, and the screening below is what makes that
    a gate rather than a hope.

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
    # An empty learner and empty hints: `AgentContext` carries the two fields a retired path
    # used, and where this house sits travels as `pitch` instead, because a pitch is prose
    # for one prompt rather than a field an agent may read for itself.
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
            pitch=pitch,
        )
        # The same checks the whole afternoon passed, on the half nobody approved, and
        # given the half that already happened: a continuation begins in the middle, so a
        # check that starts counting at its first moment refuses an ending reaching for the
        # page the earlier stretch handed over. There is no repair here and there will not
        # be one: somebody is standing at the scanner, a second model call is another
        # fifteen seconds, and an afternoon that is not continued stops — which is what an
        # afternoon nobody continues does anyway.
        complaints = check(carrying_on, already_said=_up_to(experience, after))
        if complaints:
            raise RefusedByTheChecks(complaints)
        # The chokepoint. Nothing below this line may be skipped by an early return above
        # it: the parse and the checks can refuse, but only screening lets something through.
        await screen_continuation(gate, carrying_on, context=f"continuing after {after}")
    finally:
        await gate.aclose()
    return carrying_on, router.last_usage
