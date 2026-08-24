"""Reading, because the house asked: a filled-in sheet, and the parent's sentences.

Why here and not in the house: this container holds the managed identity with access to
Foundry, so nothing in the home needs a credential of its own. The house still decides
when — it posts a page, or asks for its reminders — and nothing here can reach the house.

What arrives for a sheet is the rectified crop and the sheet's own description of where
its boxes are. Not the room, not a face, not a name: the crop is the area inside the four
corner markers and the description is ids, positions and the words printed on the paper.
What arrives for a reminder is the sentence the parent typed, which is theirs and stays
inside the household.

The gate is absent on purpose. It screens what a person will read, and a reading is not
that: it comes back as which boxes carry a mark, or as an hour, and the sentence built
from it is written in the repository. Anything said *about* a reading goes through
generation, and through the gate, like everything else.
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.routing import ModelUsage

if TYPE_CHECKING:
    from orchestrator.router import FoundryRouter


def _cloud(now: float) -> tuple[FoundryRouter, AgentContext]:
    """The router and the context around it. The router is handed back because what a call
    consumed is read off it afterwards, and a router is built per request."""
    from orchestrator.router import FoundryConfig, FoundryRouter

    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)))
    # An empty learner and empty hints: neither reader uses them, and handing them nothing
    # is the cheapest way to keep that true as the prompts change.
    return router, AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=now
    )


async def read_sentences(
    sentences: Sequence[tuple[str, str]], *, now: float
) -> tuple[Mapping[str, tuple[Any, Any, Any]], ModelUsage | None]:
    """Place each ``(id, text)`` in the day, and say what the call consumed. Raises what
    the router raises."""
    from agents.reminder_reader import ReminderReader

    router, context = _cloud(now)
    placements = await ReminderReader().read_sentences(context, sentences=sentences)
    return placements, router.last_usage
