"""Asking again for a continuation the format could not read.

`ideas/08 §7` decided there would be no repair on this path, and gave a reason: a second
model call is another fifteen seconds with somebody standing at the scanner, and an afternoon
that is not continued stops — which is what an afternoon nobody continues does anyway.

**That last clause was wrong**, and an experiment on the simulated house is what showed it.
On 24 August 2026 a run reached its second page, had it read, and then ended on
``502 not_a_continuation: a line is 45 characters; at most 44``. The afternoon could have
gone on. One character is not a reason to lose an hour.

Once, and no more: a second refusal is a model that cannot write this document, and asking a
third time spends money on the same answer.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import afternoons as a
import pytest

from agents.experience_continuer import ExperienceContinuer
from shared.agents import AgentContext
from shared.experience import ExperienceError
from shared.ids import LearnerId
from shared.routing import ModelRequest

THE_AFTERNOON: dict[str, Any] = a.an_afternoon()


def a_context(router: Any) -> AgentContext:
    return AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=1.0)


def a_continuation(line: str) -> str:
    return json.dumps(
        {
            "moments": [
                a.close(
                    moment_id="due-nuvole",
                    heading="Due nuvole",
                    weights=a.weights(lines=(line,)),
                )
            ]
        },
        ensure_ascii=False,
    )


TOO_LONG = "x" * 45
FITS = "Il foglio resta sul tavolo."


def continue_with(*replies: str) -> tuple[Any, Any]:
    """Run the continuer against a model that gives ``replies`` in order."""
    from unittest.mock import Mock

    router = Mock()
    said = list(replies)
    asked: list[str] = []

    async def _generate(request: ModelRequest) -> Any:
        asked.append(request.prompt)
        answer = Mock()
        answer.body = said.pop(0) if said else "{}"
        return answer

    router.generate_for_user = _generate
    carrying_on = asyncio.run(
        ExperienceContinuer().continue_from(
            a_context(router),
            experience=THE_AFTERNOON,
            after="che-torna",
            came="marks",
            reading={},
        )
    )
    return carrying_on, asked


def test_a_continuation_the_format_reads_is_not_asked_for_twice() -> None:
    """The repair costs a model call. It must not happen when nothing is wrong."""
    carrying_on, asked = continue_with(a_continuation(FITS))

    assert carrying_on.moments[0].heading == "Due nuvole"
    assert len(asked) == 1


def test_a_line_one_character_too_long_is_asked_for_again_rather_than_lost() -> None:
    """The measured failure: 45 characters where 44 are allowed, and an afternoon that
    ended there. Made to fail on the version without the repair, where it raises
    `a line is 45 characters; at most 44` instead of carrying on."""
    carrying_on, asked = continue_with(a_continuation(TOO_LONG), a_continuation(FITS))

    assert carrying_on.moments[0].heading == 'Due nuvole'
    assert len(asked) == 2, "it asked once, was refused, and asked again"


def test_the_second_ask_names_the_rule_and_the_offending_number() -> None:
    """This is why the parser's messages are worded the way they are: a repair prompt that
    says only "it was refused" leaves a model to guess which of forty limits it broke."""
    _, asked = continue_with(a_continuation(TOO_LONG), a_continuation(FITS))

    assert "45 characters" in asked[1]
    assert "at most 44" in asked[1]
    assert "rewording the rest is not a repair" in asked[1]


def test_the_second_ask_carries_what_was_refused_so_the_rest_survives() -> None:
    """A repair that sends back the whole document and asks for a new one changes an
    afternoon that was already mostly right."""
    _, asked = continue_with(a_continuation(TOO_LONG), a_continuation(FITS))

    assert "Due nuvole" in asked[1], "the answer it is repairing is in the prompt"
    assert "same moments, the same words, the same branches" in asked[1]


def test_a_second_refusal_is_the_end_of_it() -> None:
    """Twice is a model that cannot write this document. A third ask spends money on the
    same answer, and somebody is standing at the scanner."""
    with pytest.raises(ExperienceError, match="45 characters"):
        continue_with(a_continuation(TOO_LONG), a_continuation(TOO_LONG))
