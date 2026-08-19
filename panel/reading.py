"""Reading a sheet because the house asked, using a vision model.

Why here and not in the house: this container holds the managed identity with access to
Foundry, so nothing in the home needs a credential of its own. The house still decides
when — it posts a page and waits — and nothing here can reach the house.

What arrives is the rectified crop and the sheet's own description of where its boxes are.
Not the room, not a face, not a name: the crop is the area inside the four corner markers
and the description is ids, positions and the words printed on the paper.

The gate is absent on purpose. It screens what a person will read, and a reading is not
that: it comes back as which boxes carry a mark, and the sentence built from it is written
in the repository. Anything said *about* a reading goes through generation, and through
the gate, like everything else.
"""

from __future__ import annotations

import os

from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.sheet import SheetSpec
from shared.vision_contracts import PageReading, RectifiedPage


async def read_sheet(page: RectifiedPage, spec: SheetSpec, *, now: float) -> PageReading:
    """Read every cell ``spec`` declares. Raises what the router raises when the cloud will
    not serve it, which the caller reports as a house that could not be answered."""
    from agents.sheet_reader import SheetReader
    from orchestrator.router import FoundryConfig, FoundryRouter

    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)))
    # An empty learner and empty hints: the reader uses neither, and handing it nothing is
    # the cheapest way to keep that true as the prompt changes.
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=now
    )
    return await SheetReader().read_page(context, page=page, spec=spec)
