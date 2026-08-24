"""Read a page by comparing it with the blank it was printed from.

`ideas/10 §3`. `agents/sheet_reader.py` reads a grid: it is handed a list of boxes with
their rectangles and the word printed under each, and answers three words per box. That
reader is the reason a page has to be a grid, and the grid is the reason a page looks like a
form. This one is handed **two pictures** — the blank and what came off the glass — and asked
what is on the second that is not on the first.

Nothing about the page has to be declared. No rectangles, no cell kinds, no ids, no code
printed in a corner. The difference between two pictures is a thing a model can see, and
describing where an answer was supposed to go was only ever a way of asking it to look
there.

**It describes ink and never a person.** The same line the working rules draw, and the same
one the older reader holds: *a house drawn in the third box* describes a page; anything about
who drew it, how well, or whether it is right, is not. The instruction says so twice, because
this is the one prompt in the repository where a model is looking at somebody's handwriting.

**Whether it is the right sheet is reported, not enforced.** The parent's correction, `§3`:
the model has to interpret what is on the paper anyway, so refusing to look until identity is
settled is a machine's anxiety. Today an unrecognised page produces *this sheet is not
Lanternina's*, which is a refusal aimed at a person for a mistake the working rules say cannot
exist. A page that is not the one handed over is still a page somebody worked on.

**Nothing is salvaged from a partial answer.** A half-parsed reading looks exactly like a
whole one by the time anything acts on it, and the cost of throwing it away is one screen
saying a grown-up will look.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from typing import Any, Final

from shared.agents import AgentContext
from shared.ids import new_request_id
from shared.routing import Capability, ModelRequest, PageImage
from shared.vision_contracts import (
    MAX_DESCRIPTION_CHARS,
    MAX_DESCRIPTIONS,
    WhatCameBack,
)

_INSTRUCTION: Final = (
    "Two images of the same kind of sheet of paper. The first is the sheet as it was "
    "printed, with nothing written on it. The second is the sheet after somebody had it.\n"
    "Say what is on the second that is not on the first.\n"
    "Answer with JSON and nothing else, in this exact shape:\n"
    '{"written": true, "same_sheet": true, "describes": ["...", "..."]}\n'
    '"written" is true if anything at all was added: a line, a word, a drawing, a tick, a '
    "scribble. False if the second sheet carries nothing the first did not.\n"
    '"same_sheet" is true if the second image is the first sheet, written on. False if it '
    "is a different sheet altogether. Say false plainly; it is not a complaint.\n"
    '"describes" is what was added, one short phrase each, at most '
    f"{MAX_DESCRIPTIONS} of them and at most {MAX_DESCRIPTION_CHARS} characters each. "
    "Describe the ink on the paper and where it sits: 'a house drawn in the box on the "
    "left', 'three words on the first line', 'the second box left untouched'.\n"
    "Two things you must not do. Do not say anything about the person: not how well it was "
    "done, not how much effort it took, not what it suggests about them. And do not say "
    "whether anything is correct, because there is nothing here that can be got wrong.\n"
    "If nothing was added, say so with an empty list. That is a good answer."
)

# The wrapper plus the room the descriptions are allowed. Generous by half, so a model that
# pretty-prints its JSON is not cut off in the middle of a sentence and thrown away.
_MAX_OUTPUT: Final = 300 + MAX_DESCRIPTIONS * (MAX_DESCRIPTION_CHARS + 10) * 2


class PageReader:
    """Reads a page against its blank. Knows nothing about what the page was asking."""

    name = "page_reader"

    async def read(
        self,
        ctx: AgentContext,
        *,
        blank: PageImage,
        came_back: PageImage,
        about: str = "",
    ) -> WhatCameBack:
        """``about`` is what the moment asked for, in the household's own words, or empty.

        It is passed to give the description something to be about — a page asking for a
        drawing and a page asking for a list are read differently — and never to tell the
        model what a good answer would be. There is no good answer.
        """
        prompt = _INSTRUCTION
        if about:
            prompt += f"\nWhat the sheet asked for, for context only: {about}"
        answer = await ctx.router.analyze(
            ModelRequest(
                capability=Capability.VISION_READ,
                prompt=prompt,
                request_id=new_request_id(),
                # The blank first, in the order the instruction names them.
                images=(blank, came_back),
                max_output_chars=_MAX_OUTPUT,
                purpose="reading a page against its blank",
            )
        )
        said = {} if answer.truncated else _said_in(answer.text)
        return WhatCameBack(
            written=bool(said.get("written", False)),
            # An answer that did not say is treated as the sheet it was expecting, because
            # this field exists to inform an afternoon and not to refuse a person's page.
            same_sheet=bool(said.get("same_sheet", True)),
            describes=_clean(said.get("describes", ())),
            read_at=ctx.now or time.time(),
            degraded=not said,
            metadata={
                "read_by": self.name,
                "request_id": str(answer.request_id),
                "latency_s": round(answer.latency_s, 2),
            },
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


def _clean(lines: Any) -> tuple[str, ...]:
    """Bound what a model wrote before anybody keeps it. Never raises: an unusable line is
    dropped rather than turning the whole reading into a failure."""
    if isinstance(lines, str) or not isinstance(lines, (list, tuple)):
        return ()
    kept: list[str] = []
    for line in lines[:MAX_DESCRIPTIONS]:
        words = " ".join(str(line).split())[:MAX_DESCRIPTION_CHARS].strip()
        if words:
            kept.append(words)
    return tuple(kept)
