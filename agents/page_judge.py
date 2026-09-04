"""Place one returned page on the axes an afternoon is pitched along.

The first half of what `docs/NON-GOALS.md` allowed on 4 September 2026, and it is one half
on purpose. This is a model reading one page. :mod:`shared.profile` is arithmetic reading
the series this produces. Neither knows what the other is doing, and that is what the
parent asked for when they said the roles are always divided.

**It is given nothing that could confirm an answer it has already been handed.** No profile,
no history, no other afternoon, no household, no name — one page, the blank it came from,
and what that page asked for. A model shown the current state and asked whether it still
holds agrees with it, because agreeing with its context is what a model does, and a series
of agreements is a state that stopped being measured after the first entry.

**It is not the reader.** :mod:`agents.page_reader` describes ink for the model that writes
the rest of the afternoon, and what it says reaches a display within a minute. This one
places the page on two scales, and what it says reaches a store and no person. Keeping them
apart costs a second vision call per sheet and buys the thing that made the split worth
having: the reading cannot acquire a judgement by having one written into the same answer.

**It runs after the reply, never inside it.** Somebody is standing at the scanner. A page
reading was measured at 14.4 s on 3 September 2026 and this is another call of the same
shape, so it goes into the background as `panel/judging.py` does — an afternoon must not be
made slower by something whose whole purpose is to measure it.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, Final

from shared.agents import AgentContext
from shared.ids import new_request_id
from shared.profile import HIGHEST, LOWEST, Axis, Noticed
from shared.prompts import beside
from shared.routing import Capability, ModelRequest, PageImage

# `span` is not asked for: no page shows how long somebody sat, and a model asked anyway
# would answer from the quantity of ink, which is the axis above wearing another name.
PLACED_FROM_A_PAGE: Final[tuple[Axis, ...]] = (Axis.LOAD, Axis.INK)

# One sentence about the paper. The same bound `shared/vision_contracts` puts on a line of
# description, doubled, because this one is a sentence rather than a phrase.
MAX_SAYS: Final = 240

_INSTRUCTION: Final = beside(__file__).text(
    "instruction", lowest=LOWEST, highest=HIGHEST
).rstrip("\n")

_MAX_OUTPUT: Final = 200 + MAX_SAYS


class PageJudge:
    """Places one page on the axes. Sees the page and nothing about the house."""

    name = "page_judge"

    async def place(
        self,
        ctx: AgentContext,
        *,
        blank: PageImage,
        came_back: PageImage,
        asked_for: str = "",
    ) -> Noticed:
        """One page placed, or placed on nothing when the answer could not be read.

        Never raises on a bad answer. A placement that cannot be read is a thinner series,
        which the arithmetic downstream already handles by counting how many it has; turning
        it into an exception would let a diagnostic take down the call it rode in on.
        """
        prompt = _INSTRUCTION
        if asked_for:
            prompt += f"\nWhat the sheet asked for: {asked_for}"
        answer = await ctx.router.analyze(
            ModelRequest(
                capability=Capability.VISION_READ,
                prompt=prompt,
                # The blank first, in the order the instruction names them.
                images=(blank, came_back),
                request_id=new_request_id(),
                max_output_chars=_MAX_OUTPUT,
                purpose="placing a returned page on the axes an afternoon is pitched along",
            )
        )
        said = {} if answer.truncated else _said_in(answer.text)
        return Noticed(
            at=ctx.now,
            came_back=True,
            where=_where_in(said),
            says=" ".join(str(said.get("says") or "").split())[:MAX_SAYS],
        )


def _said_in(text: str) -> Mapping[str, Any]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return {}
    try:
        parsed: Any = json.loads(text[start : end + 1])
    except ValueError:
        return {}
    return parsed if isinstance(parsed, Mapping) else {}


def _where_in(said: Mapping[str, Any]) -> dict[Axis, int]:
    """The placements that are numbers in range. An axis left out stays left out.

    Clamped rather than refused, because a model answering 7 on a scale of 5 has said which
    end it means, and dropping that is losing a real answer over a formatting slip.
    """
    where: dict[Axis, int] = {}
    for axis in PLACED_FROM_A_PAGE:
        value = said.get(str(axis))
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        where[axis] = max(LOWEST, min(HIGHEST, int(round(float(value)))))
    return where
