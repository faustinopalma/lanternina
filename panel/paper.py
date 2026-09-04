"""The two things the house cannot do for itself: draw a page, and read one back.

Both live here for the same reason `panel/continuing.py` does. This container holds the
managed identity that reaches Foundry and Content Safety; the hub holds a device key and no
credential, so it asks and the answer comes back inside the reply to its own request.

Nothing here starts anything. Both are answers to a request the house made — one when it is
about to hand a page over, one when a page has come off its glass.
"""

from __future__ import annotations

import os
import secrets
from typing import TYPE_CHECKING, Any

from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.page import Page
from shared.profile import Noticed
from shared.routing import ModelUsage, PageImage
from shared.seal import Sealer, SealPurpose
from shared.vision_contracts import WhatCameBack

if TYPE_CHECKING:
    from orchestrator.router import FoundryRouter


def _cloud(now: float) -> tuple[FoundryRouter, AgentContext, Any]:
    """The router, the context around it, and the gate that has to be closed afterwards."""
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    # The seal this gate mints travels nowhere: the house is handed pixels, not a sealed
    # payload. A per-process key keeps the gate honest without pretending otherwise.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "panel.paper"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # An empty learner and empty hints: a page carries nothing about a person, and handing
    # the agents nothing is the cheapest way to keep that true as the prompts change.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    return router, context, gate


async def draw_page(page: Page, *, now: float) -> tuple[bytes, ModelUsage | None]:
    """The whole page as a PNG, screened as an image by the gate the router holds.

    Raises what the router raises when the cloud will not serve it. The house treats that
    as a page it did not get, and the moment plays its ``instead``.
    """
    from agents.page_maker import PageMaker

    router, context, gate = _cloud(now)
    try:
        png = await PageMaker().draw(context, page)
    finally:
        await gate.aclose()
    return png, router.last_usage


async def read_the_page(
    blank: PageImage, came_back: PageImage, *, about: str, now: float
) -> tuple[WhatCameBack, ModelUsage | None]:
    """What is on the second image that is not on the first, and what the call consumed.

    ``about`` is what this moment of the afternoon was for, in the house's own words. It is
    context for the reading and never a claim about anybody.
    """
    from agents.page_reader import PageReader

    router, context, gate = _cloud(now)
    try:
        came = await PageReader().read(context, blank=blank, came_back=came_back, about=about)
    finally:
        await gate.aclose()
    return came, router.last_usage


async def place_the_page(
    blank: PageImage, came_back: PageImage, *, asked_for: str, now: float
) -> tuple[Noticed, ModelUsage | None]:
    """Where this one page sits on the axes an afternoon is pitched along.

    A second call over the same two images, and the second call is the point: the reading
    above steers the rest of the afternoon and reaches a display within the minute, while
    this reaches a store and no person. One answer carrying both would let a judgement into
    the text by the shortest possible route.

    The model is given the page and nothing about the house, so it cannot agree with a state
    it was shown. What it answers is one row of a series; the state is arithmetic over the
    series, in :func:`shared.profile.read_from`.
    """
    from agents.page_judge import PageJudge

    router, context, gate = _cloud(now)
    try:
        noticed = await PageJudge().place(
            context, blank=blank, came_back=came_back, asked_for=asked_for
        )
    finally:
        await gate.aclose()
    return noticed, router.last_usage
