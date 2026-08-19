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
from typing import Any

from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.sheet import SheetSpec
from shared.vision_contracts import PageReading, RectifiedPage


def _context(now: float) -> AgentContext:
    from orchestrator.router import FoundryConfig, FoundryRouter

    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)))
    # An empty learner and empty hints: neither reader uses them, and handing them nothing
    # is the cheapest way to keep that true as the prompts change.
    return AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=now
    )


async def read_sheet(page: RectifiedPage, spec: SheetSpec, *, now: float) -> PageReading:
    """Read every cell ``spec`` declares. Raises what the router raises when the cloud will
    not serve it, which the caller reports as a house that could not be answered."""
    from agents.sheet_reader import SheetReader

    return await SheetReader().read_page(_context(now), page=page, spec=spec)


async def read_sentences(
    sentences: Sequence[tuple[str, str]], *, now: float
) -> Mapping[str, tuple[Any, Any, Any]]:
    """Place each ``(id, text)`` in the day. Raises what the router raises."""
    from agents.reminder_reader import ReminderReader

    return await ReminderReader().read_sentences(_context(now), sentences=sentences)
