"""Read a filled-in sheet with a vision model.

The first implementation of :class:`~shared.agents.VisionAgent`, and the reader the paper
loop actually uses. It replaces arithmetic that counted dark pixels against two constants:
that worked on printed ink and failed on the thing it was for, reporting four ticked boxes
as empty and saying it was certain. A threshold nobody in a house can tune is the wrong
shape for this problem, and the arithmetic stays only as the answer given when the cloud
cannot be reached.

What leaves the house is the rectified crop and, for each cell, its id, where it sits on
the page and the choice printed under it. No name, no profile, no household. This agent is
handed an :class:`~shared.agents.AgentContext` with an empty learner and empty hints, which
is the cheapest available proof that it reads none of them.

Two things it must not do, and both are refusals rather than guesses: a cell the model did
not answer for is marked for the parent to look at, and so is one it answered for with
anything other than the three words it was offered. The vocabulary is deliberately three
words wide — marked, empty, unsure — because the question is whether there is ink in a box,
and a longer answer would be the model saying something about the person who made it.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from typing import Any, Final

from shared.agents import AgentContext
from shared.ids import CellId, new_request_id
from shared.routing import Capability, ModelRequest, PageImage
from shared.sheet import SheetSpec
from shared.vision_contracts import CellReading, PageReading, ReadConfidence, RectifiedPage

MARKED: Final = "marked"
EMPTY: Final = "empty"
UNSURE: Final = "unsure"

# Room for one short object per cell, plus the wrapper. Measured against the shape asked
# for below: `{"id":"q1c1","mark":"marked"}` is 30 characters, and the allowance is double
# that so a model that pretty-prints its JSON is not cut off mid-answer.
_PER_CELL_CHARS: Final = 60
_WRAPPER_CHARS: Final = 200

_INSTRUCTION: Final = (
    "The image is a worksheet. Every box listed below is a box somebody could put a mark "
    "in. For each one, say whether it has a mark in it.\n"
    "Answer with JSON and nothing else, in this exact shape:\n"
    '{"cells": [{"id": "<the id below>", "mark": "marked|empty|unsure"}]}\n'
    'Use "marked" if there is any pen or pencil mark inside the box: a tick, a cross, a '
    'scribble, a filled shape. Use "empty" if the box has nothing in it but the printed '
    'outline. Use "unsure" if you cannot tell — that is a good answer and is better than '
    "a wrong one.\n"
    "Include every id exactly once. Do not add ids that are not listed. Do not say "
    "anything about the handwriting, and do not say which mark would be correct: there is "
    "no correct one.\n"
    "The boxes, with where each sits on the page as a percentage from the top-left "
    "corner, and the word printed under it:\n"
)


class SheetReader:
    """Reads the cells a :class:`SheetSpec` declares, and nothing else on the page."""

    name = "sheet_reader"

    async def read_page(
        self, ctx: AgentContext, *, page: RectifiedPage, spec: SheetSpec
    ) -> PageReading:
        request = ModelRequest(
            capability=Capability.VISION_READ,
            prompt=_prompt_for(spec),
            request_id=new_request_id(),
            images=(PageImage(png=page.png, width=page.width, height=page.height),),
            max_output_chars=_WRAPPER_CHARS + _PER_CELL_CHARS * len(spec.cells),
            purpose=f"reading sheet {spec.sheet_id}",
        )
        answer = await ctx.router.analyze(request)
        marks = {} if answer.truncated else _marks_in(answer.text)
        note = "the answer was cut short" if answer.truncated else ""
        return PageReading(
            sheet_id=spec.sheet_id,
            exercise_id=spec.exercise_id,
            cells=tuple(_reading_of(cell, marks, note) for cell in spec.cells),
            read_at=ctx.now or time.time(),
            degraded=False,
            metadata={
                "read_by": self.name,
                "request_id": str(answer.request_id),
                "latency_s": round(answer.latency_s, 2),
            },
        )


def _prompt_for(spec: SheetSpec) -> str:
    lines = [
        f"  {cell.id}: {round(cell.rect.x * 100)}% across, {round(cell.rect.y * 100)}% "
        f"down, printed word {cell.label!r}"
        for cell in spec.cells
    ]
    return _INSTRUCTION + "\n".join(lines)


def _marks_in(text: str) -> Mapping[str, str]:
    """What the model said, or nothing at all if it did not answer in the shape asked.

    Nothing is salvaged from a partial answer. A half-parsed reading looks exactly like a
    whole one by the time it reaches a display, and the cost of throwing it away is one
    screen saying a grown-up will look.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return {}
    try:
        parsed: Any = json.loads(text[start : end + 1])
    except ValueError:
        return {}
    if not isinstance(parsed, Mapping):
        return {}
    found: dict[str, str] = {}
    for entry in parsed.get("cells", []):
        if isinstance(entry, Mapping) and "id" in entry:
            found[str(entry["id"])] = str(entry.get("mark", "")).strip().lower()
    return found


def _reading_of(cell: Any, marks: Mapping[str, str], note: str) -> CellReading:
    mark = marks.get(str(cell.id), "")
    if mark == MARKED:
        return CellReading(
            cell_id=CellId(str(cell.id)),
            kind=cell.kind,
            value=cell.label,
            confidence=ReadConfidence.LIKELY,
        )
    if mark == EMPTY:
        return CellReading(
            cell_id=CellId(str(cell.id)),
            kind=cell.kind,
            value=None,
            confidence=ReadConfidence.LIKELY,
        )
    return CellReading(
        cell_id=CellId(str(cell.id)),
        kind=cell.kind,
        value=None,
        confidence=ReadConfidence.UNSURE,
        needs_review=True,
        note=note or (f"the reading said {mark!r}" if mark else "the reading skipped it"),
    )
