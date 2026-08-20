"""The agent that designs a sheet, instead of filling a template with words.

What it replaces did the job and did it in one shape: four questions, four boxes each,
always in the same places, laid out by arithmetic. Nothing was ever wrong with a page it
produced and nothing was ever surprising about one either. This agent is handed the marks
of :mod:`shared.pagedesign` and decides where they go — so a sheet can have a drawing at
the top, a line to write on, and boxes that sit where the page wanted them.

Three things it is held to, and each one is checked here rather than asked for politely:

* **The page must ask for something back.** A sheet that only assigns is the shape this
  project keeps trying not to build. Every design carries at least one line where the
  person doing it can say what they would like next, in their own words.
* **The page must be cheap to print.** The vocabulary has no fill, so the remaining way to
  spend ink is a great many strokes; :func:`printing.compose.compose` measures them and
  refuses. This agent asks for a light page and then finds out, rather than trusting.
* **What it produces is a proposal.** It reaches nobody until a parent has approved it,
  and the words on it went through the gate on the way out of the router.

The prompt describes the material, not a person. What it may carry about the household is
what ``prompt_hints()`` lets out — the same list every other agent gets.
"""

from __future__ import annotations

import json
from typing import Any, Final

from shared.errors import UnusableGeneration
from shared.ids import new_proposal_id, new_request_id
from shared.pagedesign import (
    MAX_MARKS,
    MAX_READABLE,
    MAX_STROKE_INK_MM2,
    MAX_STROKE_MM,
    MIN_BOX_SIDE,
    MIN_STROKE_MM,
    DesignError,
    PageDesign,
    WriteLine,
)
from shared.proposal import Proposal, ProposalKind
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind, ScreenedPayload

# Room for the JSON of a full page. Measured against the vocabulary: a tick box is about
# 110 characters, a stroke of eight vertices about 150, and a page is allowed 120 marks.
_MAX_OUTPUT_CHARS: Final = 16000

_VOCABULARY: Final = """\
Coordinates are fractions of the sheet's frame: x and y from 0 at the top-left to 1 at the
bottom-right. Sizes w and h are fractions too.

  {"mark":"stroke","vertices":[[x,y],[x,y],...],"width_mm":0.3}
      A run of straight segments. Two to 40 vertices. This is how everything is drawn.
  {"mark":"circle","cx":x,"cy":y,"r":r,"width_mm":0.3}
      An outline circle. r is a fraction of the sheet's width.
  {"mark":"words","rect":{"x":,"y":,"w":,"h":},"text":"...","size_mm":4.0}
      Printed words. Text size between 2.5 and 8 mm.
  {"mark":"tick_box","id":"q1a","rect":{...},"label":"sole","group":"q1"}
      A small square to put a mark in. Boxes that answer the same question share a group.
  {"mark":"write_line","id":"ask","rect":{...},"label":"..."}
      A line to write on. Drawn as a rule, not a box.
  {"mark":"draw_area","id":"d1","rect":{...},"label":"..."}
      A framed space to draw in.

There is no mark that fills an area, and there is no colour. Everything is a black line on
white paper.

Only tick_box, write_line and draw_area can be read back. A stroke or a circle is ink and
nothing more: if you draw a small circle for somebody to mark, whatever they put in it is
lost, because nothing ever looks there. Anything the person is meant to write in, mark or
draw in has to be one of those three."""


def _rules(quad_w_mm: float, quad_h_mm: float) -> str:
    return f"""\
The sheet is {quad_w_mm:.0f} by {quad_h_mm:.0f} millimetres inside its frame.

Keep it light. It is printed on a home inkjet, and a heavy page is slow, wet and wasteful:
  - Draw with lines. Never hatch or shade to suggest a solid shape.
  - All the strokes together may total {MAX_STROKE_INK_MM2:.0f} square millimetres of ink,
    which is roughly {MAX_STROKE_INK_MM2 / 0.3:.0f} millimetres of a {0.3} mm line. A small
    drawing costs a few hundred; a page-wide pattern does not fit.
  - Stroke widths between {MIN_STROKE_MM} and {MAX_STROKE_MM} mm.

Leave the four corners alone: nothing above y=0.02, and nothing in the top-right corner
between x=0.75 and x=1.0 above y=0.16. Markers and a code live there.

A box or a line to write on must be at least {MIN_BOX_SIDE} of the sheet on each side.
Answerable places must not overlap each other. At most {MAX_READABLE} of them, and at most
{MAX_MARKS} marks in total.

The page must ask, not only assign. Give it at least one write_line where the person can
say what they would like to do next, in their own words.

Do not make a form. A column of identical ruled lines with a label in front of each is a
form, and a page of two such columns is a worse one. Concretely:
  - Do not use the same mark more than four times in a row in the same arrangement.
  - Let the drawing carry part of the work instead of decorating a corner: things to
    count, to join with a line, to label, to circle, to continue.
  - Vary what is asked. A page can hold one thing to count, one thing to write, one thing
    to draw and one thing to choose, and that reads as an afternoon rather than a test.
  - Use tick_box where the answer is a choice. It is quicker to do than a written line and
    it is the only thing this house can still read when the network is down.
  - Put the parts where the subject suggests, not in a grid. Whitespace is allowed."""


class SheetDesigner:
    """Designs one page. Nothing here decides whether it is printed."""

    name = "sheet_designer"

    async def propose_sheet(
        self,
        ctx: Any,
        *,
        topic: str,
        quad_w_mm: float = 178.0,
        quad_h_mm: float = 251.0,
    ) -> Proposal:
        """Ask for a page about ``topic`` and hand back what came, or refuse it.

        The default frame is A4 with this project's margins and marker size. It is passed
        in rather than imported so that this module keeps knowing nothing about paper.
        """
        payload = await ctx.router.generate_for_user(
            ModelRequest(
                capability=Capability.STRUCTURED_GENERATION,
                prompt=self._prompt(ctx.learner_hints, topic, quad_w_mm, quad_h_mm),
                request_id=new_request_id(),
                max_output_chars=_MAX_OUTPUT_CHARS,
                purpose=f"sheet/{topic}",
                content_kind=ContentKind.PRINT_LAYOUT_JSON,
            )
        )
        design = design_from(payload)
        return Proposal(
            id=new_proposal_id(),
            kind=ProposalKind.PRINT_LAYOUT,
            agent=self.name,
            learner_id=ctx.learner_id,
            payload=payload,
            rationale=f"{design.title}: un foglio di esercizi disegnato a tratti",
            created_at=ctx.now,
        )

    def _prompt(
        self, hints: dict[str, Any], topic: str, quad_w_mm: float, quad_h_mm: float
    ) -> str:
        language = hints.get("language", "it")
        interests = ", ".join(hints.get("interests", [])) or "niente in particolare"
        avoid = ", ".join(hints.get("avoid", [])) or "niente"
        words_per_line = hints.get("max_words_per_line", 6)
        return (
            "Design one sheet of paper: a short piece of practice of the kind an adolescent "
            "is given now and then, to do by hand with a pencil.\n\n"
            f"What it is about: {topic}.\n"
            f"Written in: {language}. Short lines, about {words_per_line} words each.\n"
            f"Things this house likes: {interests}. Things to leave out: {avoid}.\n\n"
            "It should take a quarter of an hour, not an afternoon. Make it pleasant to "
            "look at as well as usable: a small line drawing that has something to do with "
            "the subject, room to breathe, and nothing crowded. Somebody should be able to "
            "stop halfway and have done something real.\n\n"
            f"{_VOCABULARY}\n\n"
            f"{_rules(quad_w_mm, quad_h_mm)}\n\n"
            'Answer with JSON and nothing else: {"title":"...","instructions":"...",'
            '"marks":[...]}\n'
            "The title and the instructions are read by the person doing the sheet, so "
            "write them in that language too. Do not say anything about who they are, do "
            "not praise, and do not print the answers anywhere on the page."
        )


def design_from(payload: ScreenedPayload) -> PageDesign:
    """Read a design out of what the gate screened, or refuse it.

    Refuses rather than repairs, all the way down. A design that is nearly right is a
    design somebody would have to look at to know what was changed, and a page reaches a
    person: asking the model again is cheaper than a page nobody reviewed.
    """
    try:
        values = json.loads(payload.body)
    except json.JSONDecodeError as exc:
        raise UnusableGeneration(f"the design is not JSON: {exc}") from exc
    if not isinstance(values, dict):
        raise UnusableGeneration("the design is not an object")

    try:
        design = PageDesign.from_dict(values)
    except DesignError as exc:
        raise UnusableGeneration(f"the design cannot be drawn: {exc}") from exc

    if not any(isinstance(m, WriteLine) for m in design.marks):
        # The one property of this system's sheets that the format itself does not carry:
        # a page may be well-formed and still only assign.
        raise UnusableGeneration(
            "the design has nowhere to write a request; a sheet that only assigns is not "
            "the sheet this system prints"
        )
    return design
