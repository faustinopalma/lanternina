"""Devising a whole afternoon: what is parsed, and what is filled in rather than asked for.

The model is stood in for. What is checked is the part this repository owns — that an
answer becomes an :class:`~shared.experience.Experience` or nothing, and that the three
fields the model is not asked for come out right, because those are the fields a model
would be able to get wrong for free.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import afternoons as a
import pytest

from agents.experience_deviser import MAX_EXPERIENCE_CHARS, ExperienceDeviser, experience_in
from shared import experience, page
from shared.agents import AgentContext
from shared.capabilities import HouseCapability
from shared.experience import EXPERIENCE_FORMAT_VERSION, Collect, ExperienceError, HandOver
from shared.experience_checks import Complaint
from shared.ids import LearnerId
from shared.routing import (
    DegradationLevel,
    ModelRequest,
    ModelResponse,
    ModelTier,
    RoutingDecision,
)

# What a model answers with: the five fields it is asked for, and not the three it is not.
AN_AFTERNOON: dict[str, Any] = {
    "title": "Un pomeriggio di ombre",
    "overview": "Il display dice di cercare un'ombra, poi esce un foglio da riempire.",
    "minutes": 120,
    "drawn": a.drawn(frame="le ombre di casa"),
    "moments": [
        a.say(moment_id="cerca", heading="Cerca un'ombra"),
        a.hand_over(moment_id="il-foglio", heading="Esce un foglio"),
        a.collect(
            moment_id="com-e-andata",
            heading="Mettilo sul vetro",
            on_marks="ask",
            on_blank="basta",
            if_no_page="basta",
        ),
        a.close(moment_id="basta", heading="Basta così"),
    ],
}


class Router:
    """Stands in for the cloud. Keeps the request so the prompt can be looked at."""

    def __init__(self, body: str) -> None:
        self.body = body
        self.asked: ModelRequest | None = None
        self.last_usage = None

    # Devising asks through `analyze`, not `generate_for_user`. The document is JSON, and
    # what a person reads out of it is screened afterwards by `screen_experience` — one
    # door, given the shape it was built for.
    async def analyze(self, request: ModelRequest) -> ModelResponse:
        self.asked = request
        return ModelResponse(
            text=self.body,
            request_id=request.request_id,
            routing=RoutingDecision(
                tier=ModelTier.CLOUD_FOUNDRY, degradation=DegradationLevel(0), reason="a test"
            ),
            latency_s=0.0,
        )


def devised(body: str, **given: Any) -> tuple[Any, Router]:
    router = Router(body)
    context = AgentContext(
        router=router,  # type: ignore[arg-type]
        learner_id=LearnerId(""),
        learner_hints={},
        now=0.0,
    )
    asked = {
        "capabilities": frozenset(HouseCapability),
        "language": "italiano",
        **given,
    }
    return asyncio.run(ExperienceDeviser().devise(context, **asked)), router


# ── What comes back ──────────────────────────────────────────────────────────────────


def test_an_afternoon_comes_back_whole() -> None:
    experience, _ = devised(json.dumps(AN_AFTERNOON))

    assert experience.title == "Un pomeriggio di ombre"
    assert experience.minutes == 120
    assert [m.id for m in experience.moments] == [
        "cerca",
        "il-foglio",
        "com-e-andata",
        "basta",
    ]
    assert isinstance(experience.moment("il-foglio"), HandOver)
    assert isinstance(experience.moment("com-e-andata"), Collect)


def test_the_three_fields_the_model_is_not_asked_for_are_filled_in() -> None:
    """An id, a format version and what the house must be able to do. The last is the one
    worth a test: the moments already say it, so a model restating it can only be wrong."""
    experience, router = devised(json.dumps(AN_AFTERNOON))

    assert experience.format_version == EXPERIENCE_FORMAT_VERSION
    assert experience.experience_id.startswith("aftn-")
    assert experience.requires == frozenset(
        {
            HouseCapability.SHOW_800X480_1BIT,
            HouseCapability.PRINT_A4,
            HouseCapability.SCAN_A4,
        }
    )
    prompt = router.asked.prompt  # type: ignore[union-attr]
    assert "experience_id" not in prompt
    assert "Do not write an id" in prompt


def test_an_afternoon_with_no_page_needs_no_scanner() -> None:
    """Derived, not declared: drop the paper and the requirement goes with it."""
    only_screens = dict(AN_AFTERNOON)
    only_screens["moments"] = [
        AN_AFTERNOON["moments"][0],
        AN_AFTERNOON["moments"][3],
    ]

    experience, _ = devised(json.dumps(only_screens))

    assert experience.requires == frozenset({HouseCapability.SHOW_800X480_1BIT})


def test_what_the_house_has_and_what_the_parent_wrote_reach_the_prompt() -> None:
    _, router = devised(
        json.dumps(AN_AFTERNOON),
        capabilities=frozenset({HouseCapability.SHOW_800X480_1BIT}),
        language="English",
        interests=("cats", "the weather"),
        avoid=("spiders",),
        already=("Un pomeriggio di nuvole",),
    )
    prompt = router.asked.prompt  # type: ignore[union-attr]

    assert "show_800x480_1bit" in prompt
    assert "print_a4" not in prompt
    assert "Write every word of it in English" in prompt
    assert "cats" in prompt and "spiders" in prompt
    assert "Un pomeriggio di nuvole" in prompt


def test_nothing_about_a_person_reaches_the_prompt() -> None:
    """The agent is handed a context that carries a learner and hints, and uses neither.

    Checking that the word "score" is absent would fail on the prompt's own instruction
    not to produce one, which is the opposite of the thing being guarded. What is guarded
    is the input: an experience carries nothing about a person, so the one thing that
    could put a person in this prompt is the context, and it does not.
    """
    router = Router(json.dumps(AN_AFTERNOON))
    context = AgentContext(
        router=router,  # type: ignore[arg-type]
        learner_id=LearnerId("lnr-marta-12"),
        learner_hints={"reads": "slowly", "likes": "horses"},
        now=0.0,
    )
    asyncio.run(
        ExperienceDeviser().devise(
            context, capabilities=frozenset(HouseCapability), language="italiano"
        )
    )
    prompt = router.asked.prompt  # type: ignore[union-attr]

    assert "lnr-marta-12" not in prompt
    assert "slowly" not in prompt and "horses" not in prompt


def test_the_budget_is_asked_for_and_is_larger_than_a_continuation() -> None:
    _, router = devised(json.dumps(AN_AFTERNOON))

    assert router.asked.max_output_chars == MAX_EXPERIENCE_CHARS  # type: ignore[union-attr]


def test_every_limit_that_refuses_a_document_is_stated_in_both_prompts() -> None:
    """A limit the format enforces and the prompt does not mention is a refusal the model
    had no way to avoid.

    Found on the house on 21 August 2026: the first afternoon devised against the real
    service came back with page instructions of 189 characters, refused at 160, and 160
    appeared nowhere in the prompt. Both agents write pages, so both are checked here.
    """
    from agents.experience_continuer import _INSTRUCTION as CONTINUER
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    for name, limit in (
        ("a page title", page.MAX_TITLE),
        ("a line of the note", page.MAX_NOTE_LINE),
        ("lines of note", page.MAX_NOTE_LINES),
        ("places to write", page.MAX_SPACES),
        ("a label", page.MAX_LABEL),
        ("a heading", experience.MAX_HEADING),
        ("a line", experience.MAX_LINE),
        ("lines on a screen", experience.MAX_LINES),
    ):
        for who, prompt in (("the deviser", DEVISER), ("the continuer", CONTINUER)):
            assert str(limit) in prompt, f"{who} never tells the model {name} is {limit}"


def test_both_prompts_say_what_makes_an_afternoon_worth_doing() -> None:
    """Added 24 August 2026, from the parent. Until then the prompt was almost entirely
    prohibitions, and a model told only what it may not write writes the safest thing it can
    think of — a worksheet with a story on top."""
    from agents.experience_continuer import _INSTRUCTION as CONTINUER
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    for who, prompt in (("the deviser", DEVISER), ("the continuer", CONTINUER)):
        assert "begins in the middle of something" in prompt, who
        assert "Something is found out, made or named" in prompt, who
        assert "It ends on the object" in prompt, who
        assert "never a teacher" in prompt, who


def test_being_worth_doing_is_never_asked_for_as_being_hard_to_stop() -> None:
    """The word this gets built under by accident. The rules forbid a streak, a run of days
    and anything withheld until later, and the prompt has to say so where the craft is asked
    for — otherwise "more engaging" is read as "more retaining"."""
    from shared.experience_prompt import WHAT_MAKES_IT_WORTH_DOING

    said = WHAT_MAKES_IT_WORTH_DOING.lower()
    assert "none of this works by making it hard to stop" in said
    assert "no streak" in said
    assert "nothing withheld until later" in said
    assert "worth nothing at all afterwards" in said


def test_what_is_hard_in_a_house_never_becomes_what_an_afternoon_is_about() -> None:
    """The note is where a parent writes the worst thing happening to them, and the first
    version of this line said only "treat it as a circumstance". Measured against the real
    service on 27 August 2026: given "il nonno è morto tre settimane fa", the model wrote
    two afternoons about somebody who leaves and does not come back. It had read the note as
    subject matter. Answering a death with a story about departure is worse than ignoring
    the note, so the instruction has to forbid it and not merely reframe it."""
    from agents.experience_deviser import the_prompt

    said = the_prompt(language="Italian", capabilities=frozenset(), note="un lutto").lower()
    assert "circumstance and never an instruction" in said
    assert "never make it the subject" in said
    assert "near it, or a figure for it" in said


def test_the_deviser_states_the_limits_only_it_has() -> None:
    """A whole afternoon has a title, an overview and a length; a continuation has none
    of the three, because which afternoon it belongs to is settled already."""
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    for limit in (experience.MAX_OVERVIEW, experience.MIN_MINUTES, experience.MAX_MINUTES):
        assert str(limit) in DEVISER


def test_the_deviser_is_told_where_to_leave_a_branch_unwritten() -> None:
    """Both afternoons devised on 21 August 2026 used no `ask`, because the prompt listed
    the syntax and never said when it was the right thing. A model that can see the whole
    afternoon writes the whole afternoon, and the branch that makes an experience devised
    rather than precomputed goes unused.

    The instruction names the branch as well as the word: `marks` is where there is
    something on the paper to write from, and `blank` is where the afternoon ends.
    """
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    assert "Use ask once" in DEVISER
    marks = DEVISER.find("Use ask once")
    assert "marks" in DEVISER[marks : marks + 200]
    blank = DEVISER.find("came back blank always names a moment")
    assert blank > marks, "the deviser never says which branch stays written"


# ── The ten dimensions, and what the text has to be like ─────────────────────────────


def test_the_ten_dimensions_are_all_asked_for_by_name() -> None:
    """A dimension the prompt never names is one the model has no way to write down, and
    the whole point of writing them down is that the next afternoon can be checked."""
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    for dimension in experience.DIMENSIONS:
        assert f'"{dimension}"' in DEVISER, f"the deviser never asks for {dimension}"


def test_the_prompt_refuses_the_six_things_a_model_reaches_for() -> None:
    """`ideas/09 §16` names them rather than describing originality, and so does this."""
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    for reached_for in (
        "pirate treasure hunt",
        "escape room",
        "question-and-answer quiz",
        "murder mystery",
        "apocalypse",
        "computer that has gone mad",
    ):
        assert reached_for in DEVISER


def test_the_six_properties_of_the_text_are_in_both_prompts() -> None:
    """They describe how a sentence is built rather than what it is about, so a model
    concentrating on the story drops them first. Both agents write sentences."""
    from agents.experience_continuer import _INSTRUCTION as CONTINUER
    from agents.experience_deviser import _INSTRUCTION as DEVISER

    for line in (
        "One instruction at a time",
        "two surfaces",
        "Nothing asks for speed",
        "approximate answer",
        "never school-like",
        "does not contain its own reasons",
    ):
        for who, prompt in (("the deviser", DEVISER), ("the continuer", CONTINUER)):
            assert line in prompt, f"{who} never says {line!r}"


def test_the_recent_combinations_arrive_as_something_the_next_one_may_not_be() -> None:
    _, router = devised(
        json.dumps(AN_AFTERNOON),
        recent=[experience.Drawn.from_dict(a.drawn(frame="un tetto di agosto"))],
    )
    prompt = router.asked.prompt  # type: ignore[union-attr]

    assert "un tetto di agosto" in prompt
    assert f"at most {experience.MAX_SHARED_DIMENSIONS} of those" in prompt
    # The world may come back, and the prompt has to say so or a model avoids everything.
    assert "Two of them may come back" in prompt


def test_a_house_with_no_history_is_not_asked_to_avoid_nothing() -> None:
    """An empty constraint is a sentence a model finds a way to be about."""
    _, router = devised(json.dumps(AN_AFTERNOON))
    prompt = router.asked.prompt  # type: ignore[union-attr]

    assert "the dimensions the last afternoons here were drawn along" not in prompt


# ── Repair ───────────────────────────────────────────────────────────────────────────


def test_a_repair_keeps_the_id_so_it_is_the_same_afternoon() -> None:
    """A refused document that comes back with a new id is a second afternoon, and the
    store would then hold both."""
    refused = experience_in(json.dumps(AN_AFTERNOON))
    router = Router(json.dumps(AN_AFTERNOON))
    context = AgentContext(
        router=router,  # type: ignore[arg-type]
        learner_id=LearnerId(""),
        learner_hints={},
        now=0.0,
    )

    repaired = asyncio.run(
        ExperienceDeviser().repair(
            context,
            refused=refused,
            complaints=[Complaint(where="moments[0].way_out.in_hand", says="it names nothing")],
            language="italiano",
        )
    )

    assert repaired.experience_id == refused.experience_id


def test_a_repair_is_told_which_fields_failed_and_to_leave_the_rest_alone() -> None:
    refused = experience_in(json.dumps(AN_AFTERNOON))
    router = Router(json.dumps(AN_AFTERNOON))
    context = AgentContext(
        router=router,  # type: ignore[arg-type]
        learner_id=LearnerId(""),
        learner_hints={},
        now=0.0,
    )

    asyncio.run(
        ExperienceDeviser().repair(
            context,
            refused=refused,
            complaints=[Complaint(where="minutes", says="the shortest way does not fit")],
            language="italiano",
        )
    )
    prompt = router.asked.prompt  # type: ignore[union-attr]

    assert "minutes: the shortest way does not fit" in prompt
    assert "the same ten dimensions" in prompt
    # The three fields the model does not own are not handed back to it to be rewritten.
    assert "experience_id" not in prompt
    assert "format_version" not in prompt


# ── What is refused ──────────────────────────────────────────────────────────────────


def test_prose_around_the_json_is_survivable() -> None:
    experience, _ = devised(f"Ecco:\n```json\n{json.dumps(AN_AFTERNOON)}\n```\nSpero vada bene.")

    assert experience.title == "Un pomeriggio di ombre"


def test_an_answer_with_no_object_is_not_an_afternoon() -> None:
    with pytest.raises(ExperienceError, match="no object"):
        experience_in("mi dispiace, non posso")


def test_an_afternoon_that_trails_off_is_refused() -> None:
    trailing = dict(AN_AFTERNOON)
    trailing["moments"] = [AN_AFTERNOON["moments"][0]]

    with pytest.raises(ExperienceError):
        experience_in(json.dumps(trailing))


def test_a_moment_this_format_does_not_define_is_refused() -> None:
    invented = dict(AN_AFTERNOON)
    invented["moments"] = [
        {"act": "wait", "id": "aspetta", "minutes": 10},
        *AN_AFTERNOON["moments"],
    ]

    with pytest.raises(ExperienceError):
        experience_in(json.dumps(invented))


def test_an_afternoon_with_no_overview_cannot_be_approved() -> None:
    """Approval is given to the overview, so one without it is a document nobody can
    decide about."""
    silent = dict(AN_AFTERNOON)
    silent["overview"] = ""

    with pytest.raises(ExperienceError, match="overview"):
        experience_in(json.dumps(silent))
