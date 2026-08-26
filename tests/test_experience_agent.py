"""The agent that runs an afternoon, one move at a time.

Three things are worth pinning. It cannot invent an act, because the house can only do four
things and an invented one would be a move nobody can perform. It cannot be handed a memory
that says something about a person, because the memory is built out of a fixed vocabulary
and everything else is dropped. And a page moment has to carry a page, because handing over
nothing is the failure that looks like success.
"""

from __future__ import annotations

import json

import pytest

from agents.experience_agent import Move, a_memory, move_in, the_prompt
from shared.capabilities import Act, HouseCapability
from shared.experience import ExperienceError


def test_a_move_is_one_act_and_why() -> None:
    said = move_in('{"act": "say", "why": "the page came back blank", "lines": ["Guarda fuori."]}')

    assert said.act is Act.SAY
    assert said.lines == ("Guarda fuori.",)
    assert said.why == "the page came back blank"


def test_an_act_the_house_cannot_perform_is_refused() -> None:
    with pytest.raises(ExperienceError) as raised:
        move_in('{"act": "improvise", "why": "x"}')

    assert "must be one of" in str(raised.value)


def test_handing_over_without_a_page_is_refused() -> None:
    with pytest.raises(ExperienceError):
        move_in('{"act": "hand_over", "why": "x"}')


def test_the_memory_holds_what_happened_and_nothing_about_anybody() -> None:
    """The vocabulary is the guarantee: a caller cannot smuggle a judgement through."""
    said = json.loads(
        a_memory(
            [
                {"what": "printed", "page": {"title": "Le nuvole"}},
                {
                    "what": "came-back",
                    "ink": ["one cell written", "one left blank"],
                    "effort": "tried hard",
                    "level": 3,
                },
            ]
        )
    )

    assert said[1] == {"what": "came-back", "ink": ["one cell written", "one left blank"]}


def test_the_memory_is_bounded() -> None:
    """A whole afternoon fits; a prompt that grows without bound does not."""
    said = json.loads(a_memory([{"what": str(i)} for i in range(60)]))

    assert len(said) == 20
    assert said[0] == {"what": "40"}


def test_the_prompt_carries_the_script_the_clock_and_the_tools() -> None:
    prompt = the_prompt(
        script="find out who left the ledger",
        themes=["un registro", "pesi impossibili"],
        plan={"moments": []},
        tools=frozenset({HouseCapability.PRINT_A4, HouseCapability.SCAN_A4}),
        happened=[],
        minutes_left=35,
    )

    assert "find out who left the ledger" in prompt
    assert "print_a4, scan_a4" in prompt
    assert "35" in prompt
    # The four verbs come from the same registry the deviser's prompt is built from.
    for act in Act:
        assert str(act) in prompt


def test_a_move_says_only_what_the_house_can_act_on() -> None:
    said = Move(act=Act.CLOSE, why="the hour is nearly up", lines=("Tienilo.",))

    assert set(said.to_dict()) == {"act", "why", "lines"}
