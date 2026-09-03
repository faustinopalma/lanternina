"""Read an afternoon that was devised, and say where it does not do what it was asked to.

`shared/experience_checks.py` says in its own docstring that a plan can pass all six checks
and still be a worksheet, and that this is unchecked. This is what checks it, and it is not
a gate: nothing here runs before an afternoon reaches a house. It exists for the hours spent
changing the prompts, where the question is *did that edit make them better* and there has
never been an answer to it except reading ten afternoons by hand.

**It invents no criteria.** Every finding it may report is a promise
`shared/experience_prompt.what-makes-it-worth-doing.md` already makes, so a finding is the
distance between what the deviser was told and what came back — not somebody's taste. That
is also why there is no score: `ideas/11 §5` holds the argument, and its short form is that
a form right for ``stretch`` is wrong for ``gentle``, so one number about an afternoon
freezes a judgement about a context that is not present when it is made.

**It is shown the moments and not the script.** The script, the overview, the title and the
ten dimensions are the author's eye, and the script usually contains the answer. What goes
across is what reaches the person. Asking a reader to state the question and its answer from
that alone is the test — an afternoon whose question cannot be stated by somebody who read
every word of it does not have one. Comparing what this reader worked out against what the
author wrote is left to whoever is doing the prompt work, because that comparison is a
judgement and this run is where judgements are cheap.

**Two kinds, and the judge decides which before it judges.** An afternoon where nothing can
be got wrong is a thing this system makes and always has — `attic/catalogue/three-words.json`
was the first sheet ever written here and it says «scegli quella che preferisci, non ce n'è
una giusta». Half the promises do not apply to it, and applying them anyway would be
marking it down for not being something else.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Final

from shared.agents import AgentContext
from shared.experience import MAX_LINE, Experience
from shared.experience_checks import Complaint
from shared.ids import new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest

SAYS: Final = beside(__file__)

_INSTRUCTION: Final = SAYS.text("instruction") + SAYS.text("format", max_line=MAX_LINE)

# The names a finding may carry. Closed, because a category invented once cannot be counted
# across runs, and counting across runs is the only reason to do this ten times.
FINDINGS: Final[frozenset[str]] = frozenset(
    {
        "given_away",
        "no_question",
        "not_worth_having",
        "can_be_failed",
        "no_way_in",
        "a_beat_with_no_mark",
        "something_not_in_a_house",
        "does_not_end_on_the_object",
    }
)

# Which findings belong to which kind. A judge that reports `given_away` about an afternoon
# it has just called open has contradicted itself, and that is worth seeing rather than
# quietly dropping — so this is used to report the contradiction, not to filter it.
ONLY_IF_WRONG_IS_POSSIBLE: Final[frozenset[str]] = frozenset(
    {"given_away", "no_question", "not_worth_having"}
)
ONLY_IF_NOTHING_CAN_BE_WRONG: Final[frozenset[str]] = frozenset({"can_be_failed"})

MAX_FINDINGS: Final = 8
MAX_SAYS: Final = 400
_MAX_OUTPUT: Final = 400 + 2 * MAX_LINE + MAX_FINDINGS * (MAX_SAYS + 80)


@dataclass(frozen=True, slots=True)
class Verdict:
    """What one reader made of one afternoon, having seen only what the person sees."""

    can_be_wrong: bool
    # What the reader worked out, in its own words. Empty when it could not say, and an
    # empty `question` on an afternoon where something can be got wrong is the loudest
    # result this produces.
    question: str
    answer: str
    findings: tuple[Complaint, ...]
    # The reader's answer could not be read at all. Kept apart from "no findings", which is
    # a real and ordinary result and means the opposite.
    degraded: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def names(self) -> tuple[str, ...]:
        """The finding names, for counting across a run."""
        return tuple(one.where.split(":", 1)[0] for one in self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "can_be_wrong": self.can_be_wrong,
            "question": self.question,
            "answer": self.answer,
            "degraded": self.degraded,
            "findings": [{"where": one.where, "says": one.says} for one in self.findings],
        }


def what_the_person_sees(experience: Experience) -> str:
    """The afternoon with the author's eye taken out, as JSON.

    Dropping rather than selecting, so a field added to the format arrives here by default
    and has to be argued out. The four dropped are the ones a person never sees.
    """
    whole = experience.to_dict()
    for author_only in ("title", "overview", "themes", "script", "drawn"):
        whole.pop(author_only, None)
    return json.dumps(whole, ensure_ascii=False, indent=1)


class ExperienceJudge:
    """Reads a devised afternoon against the promises its prompt made. Never a gate."""

    name = "experience_judge"

    async def judge(self, ctx: AgentContext, *, experience: Experience) -> Verdict:
        answer = await ctx.router.analyze(
            ModelRequest(
                capability=Capability.PLANNING,
                prompt=f"{_INSTRUCTION}\nThe afternoon, as the person receives it:\n"
                f"{what_the_person_sees(experience)}",
                request_id=new_request_id(),
                max_output_chars=_MAX_OUTPUT,
                purpose="judging a devised afternoon while the prompts are being changed",
            )
        )
        said = {} if answer.truncated else _said_in(answer.text)
        return Verdict(
            can_be_wrong=bool(said.get("can_be_wrong", True)),
            question=_one_line(said.get("question")),
            answer=_one_line(said.get("answer")),
            findings=_findings_in(said.get("findings")),
            degraded=not said,
            metadata={
                "judged_by": self.name,
                "request_id": str(answer.request_id),
                "latency_s": round(answer.latency_s, 2),
                "judged_at": ctx.now or time.time(),
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


def _one_line(raw: Any) -> str:
    return " ".join(str(raw or "").split())[:MAX_LINE]


def _findings_in(raw: Any) -> tuple[Complaint, ...]:
    """Never raises. A finding that cannot be read is dropped, not turned into a failure.

    The name is kept in ``where`` ahead of a colon rather than in a field of its own,
    because `Complaint` is what a repair loop already consumes and adding a third field to
    it for this would change a contract that six checks depend on.
    """
    if isinstance(raw, str) or not isinstance(raw, (list, tuple)):
        return ()
    kept: list[Complaint] = []
    for one in raw[:MAX_FINDINGS]:
        if not isinstance(one, Mapping):
            continue
        name = str(one.get("finding", "")).strip()
        says = " ".join(str(one.get("says", "")).split())[:MAX_SAYS]
        if name not in FINDINGS or not says:
            continue
        where = " ".join(str(one.get("where", "experience")).split())[:80] or "experience"
        kept.append(Complaint(where=f"{name}: {where}", says=says))
    return tuple(kept)


def contradictions(verdict: Verdict) -> tuple[str, ...]:
    """Findings that do not belong to the kind the judge said this afternoon was.

    Reported rather than filtered. A judge that calls an afternoon open and then says its
    answer was given away has not understood it, and hiding that would hide the one signal
    that says so.
    """
    wrong_kind = (
        ONLY_IF_WRONG_IS_POSSIBLE if not verdict.can_be_wrong else ONLY_IF_NOTHING_CAN_BE_WRONG
    )
    return tuple(name for name in verdict.names if name in wrong_kind)
