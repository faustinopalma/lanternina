"""Reading a page against the blank it was printed from.

`ideas/10 §3`. What is held here is not that the parser works. It is the three lines this
reader must not cross, and each of them fails on an implementation that looks right.

Nothing is salvaged from a half-answer, because a partial reading is indistinguishable from
a whole one by the time anything acts on it. A page that is not the one handed over is
reported and not refused, because a refusal here lands on a person for a mistake the working
rules say cannot exist. And what a model wrote is bounded before anybody keeps it, because
the one prompt in this repository that looks at somebody's handwriting is the one place a
sentence about them could get in.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from agents.page_reader import PageReader
from orchestrator.router import StubRouter
from shared.agents import AgentContext
from shared.ids import LearnerId
from shared.routing import Capability, PageImage
from shared.vision_contracts import MAX_DESCRIPTION_CHARS, MAX_DESCRIPTIONS, WhatCameBack

A_PAGE = PageImage(png=b"a page", width=1240, height=1754)
WRITTEN_ON = PageImage(png=b"a page with ink", width=1240, height=1754)


def read(reply: str, *, about: str = "") -> tuple[StubRouter, WhatCameBack]:
    router = StubRouter(replies=[reply])
    ctx = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=1000.0)
    came = asyncio.run(
        PageReader().read(ctx, blank=A_PAGE, came_back=WRITTEN_ON, about=about)
    )
    return router, came


def an_answer(**values: Any) -> str:
    return json.dumps({"written": True, "same_sheet": True, "describes": [], **values})


# ── What it asks for ─────────────────────────────────────────────────────────────────


def test_the_blank_goes_first_and_both_go() -> None:
    """The instruction names them in order, so the order is part of the contract."""
    router, _ = read(an_answer())

    assert router.seen[0].images == (A_PAGE, WRITTEN_ON)
    assert router.seen[0].capability is Capability.VISION_READ


def test_no_grid_is_described_to_the_model() -> None:
    """The whole point: nothing about cells, rectangles or ids reaches the prompt, because
    there is no longer anything of the sort on the page."""
    router, _ = read(an_answer())

    said = router.seen[0].prompt.lower()
    for word in ("rectangle", "% across", "% down", "cell id", "checkbox"):
        assert word not in said


def test_what_the_sheet_asked_for_is_context_and_not_an_answer() -> None:
    router, _ = read(an_answer(), about="disegna la stessa cosa sei volte")

    assert "disegna la stessa cosa sei volte" in router.seen[0].prompt
    assert "for context only" in router.seen[0].prompt


def test_the_prompt_forbids_saying_anything_about_the_person() -> None:
    """Said in the prompt as well as enforced by the shape, because the shape only stops a
    field and a description is free text."""
    router, _ = read(an_answer())

    said = router.seen[0].prompt
    assert "not say anything about the person" in said
    assert "nothing here that can be got wrong" in said


# ── What it refuses ──────────────────────────────────────────────────────────────────


def test_a_cut_off_answer_is_kept_by_nobody() -> None:
    """A partial reading and a whole one look identical by the time anything acts on it."""
    _, came = read(an_answer(describes=["x" * 40_000]))

    assert came.describes == ()
    assert came.written is False
    assert came.degraded is True


def test_an_answer_that_is_not_json_is_kept_by_nobody() -> None:
    _, came = read("Certamente! Ecco cosa vedo sul foglio.")

    assert came.describes == ()
    assert came.degraded is True


def test_more_descriptions_than_allowed_are_cut_to_the_cap() -> None:
    _, came = read(an_answer(describes=[f"riga {n}" for n in range(MAX_DESCRIPTIONS + 5)]))

    assert len(came.describes) == MAX_DESCRIPTIONS


def test_a_description_longer_than_a_line_is_cut() -> None:
    """A model narrating instead of reporting is where a sentence about a person gets in."""
    _, came = read(an_answer(describes=["x" * (MAX_DESCRIPTION_CHARS + 60)]))

    assert len(came.describes[0]) == MAX_DESCRIPTION_CHARS


def test_a_description_that_is_not_a_list_is_dropped_rather_than_read() -> None:
    _, came = read(an_answer(describes="una riga sola, non una lista"))

    assert came.describes == ()


# ── The wrong sheet is a fact, not a refusal ─────────────────────────────────────────


def test_a_page_that_is_not_the_one_handed_over_is_still_read() -> None:
    """`ideas/10 §3`: the model interprets what is there. Refusing to look until identity is
    settled is a machine's anxiety, and the refusal would land on a person."""
    _, came = read(an_answer(same_sheet=False, describes=["un disegno di una casa"]))

    assert came.same_sheet is False
    assert came.written is True
    assert came.describes == ("un disegno di una casa",)
    assert came.degraded is False


def test_an_answer_that_does_not_say_is_taken_as_the_sheet_that_was_expected() -> None:
    """The field informs an afternoon; it does not gate one. Absent means do not make a
    fuss, which is the only default that cannot produce a complaint at somebody."""
    _, came = read(json.dumps({"written": True, "describes": ["un segno"]}))

    assert came.same_sheet is True


def test_a_page_nobody_wrote_on_is_an_ordinary_answer() -> None:
    """Blank is a legitimate outcome and the afternoon has a branch for it. Nothing here
    treats it as a failure to read."""
    _, came = read(an_answer(written=False, describes=[]))

    assert came.written is False
    assert came.degraded is False


# ── What it carries ──────────────────────────────────────────────────────────────────


def test_it_carries_no_field_for_a_verdict() -> None:
    """The rule is that nothing states a verdict about a person, and the cheapest way to
    keep it is to have nowhere to put one.

    The exact set is the assertion, and a substring search for words like "grade" is not:
    the first version of this test failed on `degraded`, which contains one.
    """
    assert set(WhatCameBack.__dataclass_fields__) == {
        "written",
        "same_sheet",
        "describes",
        "read_at",
        "degraded",
        "metadata",
    }


def test_it_survives_the_wire() -> None:
    _, came = read(an_answer(describes=["tre parole sulla prima riga"]))

    assert WhatCameBack.from_dict(came.to_dict()) == came
