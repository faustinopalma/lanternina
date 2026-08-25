"""Wording a reminder, because the house asked for its reminders.

Why here and not in the house: this container holds the managed identity with access to
Foundry and to Content Safety, so nothing in the home needs a credential of its own. It is
the same reason `panel/painting.py` is here, and the gate is the reason the two are alike
rather than the two being alike by habit — words on a display are content reaching the
adolescent, so they go out through ``generate_for_user`` and are screened before they are
returned.

When this runs is not decided here. A write from the panel is inert: it may persist state
and nothing else. So a sentence is worded inside the answer to the request the house makes
for its reminders, at the same moment the sentence is read, and never because somebody
typed something.

What the parent approves is the reminder, not each wording. That is the weakening already
made for pictures, where a theme is approved and the images vary inside it, and it is not
a new one. What the wordings are is visible to the parent in the panel, which the pictures
path does not offer.
"""

from __future__ import annotations

import os
import secrets

from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose


async def word_sentence(
    text: str, at: str, *, now: float
) -> tuple[tuple[str, ...], ModelUsage | None]:
    """Ways of saying one placed sentence, and what the call consumed.

    Raises whatever the router raises when the cloud will not serve it, including
    :class:`~shared.errors.SafetyBlocked` when the gate refuses what came back.
    """
    from agents.reminder_wording import ReminderWording
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    # The seal this gate mints is not used downstream on this path: the hub draws from the
    # strings we return, not from a sealed payload, exactly as it does for a picture. A
    # per-process key keeps the gate honest without pretending the seal travels anywhere.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # An empty learner and empty hints: the wording is about the parent's sentence, and
    # handing the agent nothing is the cheapest way to keep that true as the prompt changes.
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=now
    )
    try:
        wordings = await ReminderWording().word_sentence(context, text=text, at=at)
    finally:
        await gate.aclose()
    return wordings, router.last_usage


async def say_sentence_now(
    text: str, at: str, *, now: float
) -> tuple[str, str, ModelUsage | None]:
    """One way of saying a sentence for the showing about to happen, what it is about,
    and what the call consumed.

    The same gate as above and a different question: this is asked when a reminder comes
    due rather than when its sentence is read, so the words are new each time instead of
    being picked from four made once.

    Raises whatever the router raises, including
    :class:`~shared.errors.SafetyBlocked` when the gate refuses what came back.
    """
    from agents.reminder_wording import ReminderWording
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=now
    )
    try:
        said, subject = await ReminderWording().say_it_now(context, text=text, at=at)
    finally:
        await gate.aclose()
    return said, subject, router.last_usage
