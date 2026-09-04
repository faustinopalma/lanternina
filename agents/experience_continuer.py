"""Write the rest of an afternoon, after a page came back and the plan said ``ask``.

This is the moment an experience stops being a document and starts being devised. The
house has played what a parent approved as far as an outcome that says ``ask``; what is
asked for here is the rest, in the same vocabulary, with an ending of its own.

Two things bound what a model can do with that, and neither is in the prompt.

* **The format.** :class:`~shared.experience.Continuation` parses what comes back and
  refuses anything it does not define — an unknown key, a branch that leads backwards, a
  page collected before one was handed over, an afternoon that trails off. So the prompt
  below describes the format for the model's benefit, not as the thing that enforces it.
* **The gate.** ``orchestrator.safety.screen_continuation`` screens every word before the
  house is told anything, because a parent approved the experience once from its overview
  and has not seen this. That is the trade `ideas/08 §2` records, and this module is the
  place it is paid.

What the model is given is the experience and what came back off the glass. The document
carries nothing about a person and the reading describes ink; what the prompt carries is a
separate question, and since 4 September 2026 the answer is no longer *nothing* — see
`docs/NON-GOALS.md`.

What the prompt leaves out, said here rather than found later: a design may also carry
strokes and circles, and this prompt does not offer them. A continuation is therefore
made of words, boxes, lines and space to draw, and the drawing is the adolescent's. A
model that should draw on the page is a longer prompt and a separate measurement.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any, Final

from shared.agents import AgentContext
from shared.experience import (
    EXPERIENCE_FORMAT_VERSION,
    MAX_MOMENTS,
    Continuation,
    ExperienceError,
)
from shared.experience_prompt import (
    HOW_THE_TEXT_READS,
    ONLY_WHAT_YOU_CAN_ANSWER,
    THE_ACTS,
    THE_LIMITS,
    THE_MARKS_ON_A_PAGE,
    THE_SHAPE_OF_A_MOMENT,
    WHAT_MAKES_IT_WORTH_DOING,
)
from shared.ids import new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind

# A continuation is several moments, and in format 2 a moment carries three weighings, four
# rungs of help and a way out on top of what it had. Measured against
# `experiences/un-pomeriggio-di-nuvole.json` on 23 August 2026: its four moments after the
# first collect are 4 869 characters of compact JSON, against 1 583 in format 1. This is
# that, with room for a longer one.
MAX_CONTINUATION_CHARS: Final = 9000

SAYS: Final = beside(__file__)

_FORMAT: Final = (
    SAYS.text("format") + THE_SHAPE_OF_A_MOMENT + THE_ACTS + THE_MARKS_ON_A_PAGE
)

_RULES: Final = (
    SAYS.text("rules-head", max_moments=MAX_MOMENTS)
    + THE_LIMITS
    + SAYS.text("rules-tail")
)

_MANNER: Final = (
    SAYS.text("manner-head")
    + HOW_THE_TEXT_READS
    + ONLY_WHAT_YOU_CAN_ANSWER
    + WHAT_MAKES_IT_WORTH_DOING
    + SAYS.text("manner-tail")
)

_INSTRUCTION: Final = _FORMAT + _RULES + _MANNER

# What the plan assumed and what happened are not always the same thing. The bounds it
# improvises within are `panel/guidelines.py`; the words are in the files beside this one.
# The blank line before each is the assembly's, not the prose's.
_LATITUDE: Final = "\n" + SAYS.text("latitude")

_HOUSE_SAYS: Final = "\n" + SAYS.text("house-says")


def with_bounds(fixed: Sequence[str], household: str = "") -> str:
    """The instruction, plus what may be improvised and how far.

    ``fixed`` is ours and ``household`` is the parent's, and they are separated in the prompt
    for the same reason they are separated in the store: one of them can be edited from a
    browser and the other cannot.
    """
    said = _INSTRUCTION + _LATITUDE + "\n".join(f"- {line}" for line in fixed) + "\n"
    if household:
        said += _HOUSE_SAYS + household + "\n"
    return said


def the_prompt(
    *,
    experience: dict[str, Any],
    after: str,
    came: str,
    reading: dict[str, Any],
    bounds: Sequence[str] = (),
    household_bounds: str = "",
    pitch: str = "",
) -> str:
    """The whole thing the model is sent, standing instruction and household both.

    Its own function so that what is sent can be read without running anything:
    `tools/prompts.py` renders it into `docs/prompts/`, and a test refuses a change here
    that has not been rendered.

    ``pitch`` is :meth:`shared.profile.Profile.as_material`, empty when this house has too
    little behind it. It goes in ahead of the page rather than after it, so that the model
    reads the handwriting already knowing what to do with it rather than deciding.
    """
    instruction = (
        with_bounds(bounds, household_bounds) if bounds or household_bounds else _INSTRUCTION
    )
    return (
        f"{instruction}\n"
        + (SAYS.text("pitch", pitch=pitch) if pitch else "")
        + SAYS.text(
            "household",
            experience=json.dumps(experience, ensure_ascii=False),
            after=after,
            came=came,
            ink=json.dumps(_ink(reading), ensure_ascii=False),
        )
    )


class ExperienceContinuer:
    """Writes the moments after an ``ask``, screened by the caller before it goes home."""

    name = "experience_continuer"

    async def continue_from(
        self,
        ctx: AgentContext,
        *,
        experience: dict[str, Any],
        after: str,
        came: str,
        reading: dict[str, Any],
        bounds: Sequence[str] = (),
        household_bounds: str = "",
        pitch: str = "",
    ) -> Continuation:
        """The rest of the afternoon, parsed. Raises when what came back is not one.

        Nothing is salvaged from a partial answer. Half a continuation is half an
        afternoon, and the house handles "no continuation" already — it stops.

        An answer the format cannot read is asked for once more rather than thrown away:
        see :meth:`repair_unreadable` for what changed that and why.

        ``bounds`` and ``household_bounds`` are what it may improvise within when the page
        did not come back the way the plan assumed. With neither given it is told nothing
        about taking liberties, which is the narrowest this ever is.
        """
        asked = the_prompt(
            experience=experience,
            after=after,
            came=came,
            reading=reading,
            bounds=bounds,
            household_bounds=household_bounds,
            pitch=pitch,
        )
        answer = await self._ask(ctx, asked, experience, after)
        try:
            return _continuation_in(
                answer,
                experience_id=str(experience.get("experience_id", "")),
                after=after,
            )
        except ExperienceError as refusal:
            return await self.repair_unreadable(
                ctx, answer=answer, refusal=str(refusal), experience=experience, after=after
            )

    async def repair_unreadable(
        self,
        ctx: AgentContext,
        *,
        answer: str,
        refusal: str,
        experience: dict[str, Any],
        after: str,
    ) -> Continuation:
        """The same answer, for a continuation the format would not read at all.

        `ideas/08 §7` said there would be no repair on this path, and gave the reason: a
        second model call is another fifteen seconds with somebody standing at the scanner,
        and an afternoon that is not continued stops — which is what an afternoon nobody
        continues does anyway. **That last clause was wrong**, and a simulated run of
        24 August 2026 is what showed it: the continuation was refused for
        ``a line is 45 characters; at most 44`` and the afternoon ended there. It could have
        gone on. One character is not a reason to lose an hour.

        Once, and no more. The refusal is already written for whoever has to fix it — it
        names the rule and the offending number — which is why the parser's messages are
        worded the way they are.
        """
        again = await self._ask(
            ctx,
            SAYS.text("repair", refusal=refusal)
            + f"{_FORMAT}{_RULES}"
            + f"What was refused: {answer}\n",
            experience,
            after,
        )
        return _continuation_in(
            again, experience_id=str(experience.get("experience_id", "")), after=after
        )

    async def _ask(
        self, ctx: AgentContext, prompt: str, experience: dict[str, Any], after: str
    ) -> str:
        payload = await ctx.router.generate_for_user(
            ModelRequest(
                capability=Capability.PLANNING,
                prompt=prompt,
                request_id=new_request_id(),
                max_output_chars=MAX_CONTINUATION_CHARS,
                purpose=f"continuing {experience.get('experience_id', '')} after {after}",
                content_kind=ContentKind.EXERCISE_JSON,
            )
        )
        return str(payload.body)


def _ink(reading: dict[str, Any]) -> list[dict[str, str]]:
    """What was on the page, in the reader's own three words and nothing more.

    The reading carries ids, confidences and notes for the parent panel. What a model
    needs to decide what happens next is which of the printed places carry a mark, so
    that is all it is given: fewer fields is fewer things for a prompt to be about.
    """
    out: list[dict[str, str]] = []
    for cell in reading.get("cells", []):
        if not isinstance(cell, dict):
            continue
        value = cell.get("value")
        out.append(
            {
                "place": str(cell.get("label") or value or cell.get("cell_id", "")),
                "ink": "marks" if value else str(cell.get("confidence", "")),
            }
        )
    return out


def _continuation_in(text: str, *, experience_id: str, after: str) -> Continuation:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ExperienceError("the answer holds no object")
    try:
        parsed: Any = json.loads(text[start : end + 1])
    except ValueError as exc:
        raise ExperienceError(f"the answer is not JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ExperienceError("the answer is not an object")
    # Which afternoon and which branch are known here and are not asked for: a model made
    # to echo two ids can get them wrong, and there is nothing to learn from it doing so.
    # The house checks them again on arrival, where they guard against a wrong answer
    # rather than against a wrong model.
    return Continuation.from_dict(
        {
            "format_version": EXPERIENCE_FORMAT_VERSION,
            "experience_id": experience_id,
            "after": after,
            "moments": parsed.get("moments", []),
        }
    )
