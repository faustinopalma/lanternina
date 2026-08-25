"""One move at a time, from a strategy a parent approved.

The deviser writes a whole afternoon in advance and `devices/run_experience.py` walks it.
That works and it is what runs today. What it cannot do is answer the room: a page came back
blank, twenty minutes went quiet, the object somebody picked up turned out to be more
interesting than the one the plan was pointing at.

This is the other half. It is handed the strategy — the thing the parent read and approved —
the plan for reference, what the house can do, and what has happened so far, and it answers
with **one move**. Then the house does that move and comes back. A turn is a model call, so
this is not free: `ideas/09` has the numbers, and the reason a move is one act rather than a
list is that a list would be a plan again, decided before the thing it is answering.

**What bounds it.** Not a second screening system — the words go out through
`generate_for_user` like everything else, and the provider moderates its own output. What
bounds it is the strategy, which is narrow and specific and was approved; the clock, which
is enforced here and not asked for; and the acts, which are the four the house can perform
and nothing else. An act it invents is refused by the parser rather than attempted.

**What it is not allowed to hold.** ``a_memory`` builds the history out of typed events, so
the only things it can say are things that happened: a display said this, a page was printed,
a page came back with ink here and none there, this much time passed. There is no field it
could put a judgement in, and that is deliberate rather than incidental.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from shared.agents import AgentContext
from shared.capabilities import Act, HouseCapability
from shared.experience import MAX_LINE, MAX_LINES, ExperienceError, plain
from shared.experience_prompt import THE_ACTS, THE_MARKS_ON_A_PAGE
from shared.ids import new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind

SAYS: Final = beside(__file__)

_INSTRUCTION: Final = SAYS.text("instruction", acts=THE_ACTS) + THE_MARKS_ON_A_PAGE

# Enough for a move with a page in it, which is the largest of the four. Anything longer is
# a model writing a plan when it was asked for a step.
MAX_MOVE_CHARS: Final = 3000

# How many things that happened are carried into a turn. Twenty is a whole afternoon at one
# move every few minutes; carrying all of it would grow the prompt without bound, and the
# oldest of them is the least useful thing in it. Chosen, not measured.
REMEMBERED: Final = 20


@dataclass(frozen=True, slots=True)
class Move:
    """One act, and why. ``why`` is for the log and reaches nobody in the house."""

    act: Act
    why: str
    heading: str = ""
    lines: tuple[str, ...] = ()
    page: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        said: dict[str, Any] = {"act": str(self.act), "why": self.why}
        if self.heading:
            said["heading"] = self.heading
        if self.lines:
            said["lines"] = list(self.lines)
        if self.page is not None:
            said["page"] = self.page
        return said


def a_memory(happened: Sequence[Mapping[str, Any]]) -> str:
    """What has happened, as JSON, with nothing in it that is about a person.

    The caller builds these out of what the house did and what came back. This function is
    the narrow place it goes through, and the keys it keeps are the whole vocabulary.
    """
    kept = [
        {key: value for key, value in one.items() if key in _REMEMBERABLE}
        for one in happened[-REMEMBERED:]
    ]
    return json.dumps(kept, ensure_ascii=False)


# A display said this, a page was printed, a page came back and where its ink was, how long
# passed, what the parent said about the clock. Anything else a caller puts in an event is
# dropped here rather than refused, because dropping it is what keeps this list the
# definition of what may be remembered.
_REMEMBERABLE: Final[frozenset[str]] = frozenset(
    {"what", "at", "heading", "lines", "page", "ink", "minutes"}
)


def the_prompt(
    *,
    strategy: str,
    themes: Sequence[str],
    plan: Mapping[str, Any],
    tools: frozenset[HouseCapability],
    happened: Sequence[Mapping[str, Any]],
    minutes_left: int,
) -> str:
    """The whole thing the model is sent, standing instruction and afternoon both."""
    return f"{_INSTRUCTION}\n" + SAYS.text(
        "household",
        strategy=strategy or "(none written; follow the plan)",
        themes=json.dumps(list(themes), ensure_ascii=False),
        plan=json.dumps(plan, ensure_ascii=False),
        tools=", ".join(sorted(str(one) for one in tools)),
        what_happened=a_memory(happened),
        minutes_left=minutes_left,
    )


class ExperienceAgent:
    """Decides the next move of an afternoon that is already happening."""

    name = "experience_agent"

    async def next_move(
        self,
        ctx: AgentContext,
        *,
        strategy: str,
        themes: Sequence[str],
        plan: Mapping[str, Any],
        tools: frozenset[HouseCapability],
        happened: Sequence[Mapping[str, Any]],
        minutes_left: int,
    ) -> Move:
        """One move, screened on the way out. Raises what the router raises.

        Somebody is in the room while this runs, so there is no repair loop: an answer the
        parser cannot read raises, and the caller falls back to the written plan, which is
        the thing that was approved and always works.
        """
        payload = await ctx.router.generate_for_user(
            ModelRequest(
                capability=Capability.PLANNING,
                prompt=the_prompt(
                    strategy=strategy,
                    themes=themes,
                    plan=plan,
                    tools=tools,
                    happened=happened,
                    minutes_left=minutes_left,
                ),
                request_id=new_request_id(),
                max_output_chars=MAX_MOVE_CHARS,
                purpose="the next move of an afternoon",
                content_kind=ContentKind.EXPERIENCE,
            )
        )
        return move_in(payload.body)


def move_in(text: str) -> Move:
    """Parse one move. Raises :class:`ExperienceError` on anything that is not one."""
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ExperienceError("the answer holds no object")
    try:
        values: Any = json.loads(text[start : end + 1])
    except ValueError as exc:
        raise ExperienceError(f"the answer is not JSON: {exc}") from exc
    if not isinstance(values, Mapping):
        raise ExperienceError("the answer is not an object")

    try:
        act = Act(str(values.get("act", "")))
    except ValueError as exc:
        acts = ", ".join(str(one) for one in Act)
        raise ExperienceError(f"a move must be one of {acts}") from exc

    lines = values.get("lines") or ()
    if isinstance(lines, str) or not isinstance(lines, Sequence):
        raise ExperienceError("lines must be a list")
    if len(lines) > MAX_LINES:
        raise ExperienceError(f"{len(lines)} lines; at most {MAX_LINES}")

    page = values.get("page")
    if act is Act.HAND_OVER and not isinstance(page, Mapping):
        raise ExperienceError("handing over means handing over a page")

    return Move(
        act=act,
        why=plain(str(values.get("why", "")), 120, "why"),
        heading=plain(str(values.get("heading", "")), 28, "a heading"),
        lines=tuple(plain(str(one), MAX_LINE, "a line") for one in lines),
        page=dict(page) if isinstance(page, Mapping) else None,
    )
