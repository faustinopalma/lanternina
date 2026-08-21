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

import pytest

from agents.experience_deviser import MAX_EXPERIENCE_CHARS, ExperienceDeviser, experience_in
from shared.agents import AgentContext
from shared.capabilities import HouseCapability
from shared.experience import EXPERIENCE_FORMAT_VERSION, Collect, ExperienceError, HandOver
from shared.ids import LearnerId
from shared.routing import ModelRequest
from shared.safety import ContentKind, SafetyVerdict, ScreenedPayload, ScreeningRecord
from shared.seal import Sealer, SealPurpose

AN_AFTERNOON: dict[str, Any] = {
    "title": "Un pomeriggio di ombre",
    "overview": "Il display dice di cercare un'ombra, poi esce un foglio da riempire.",
    "minutes": 120,
    "moments": [
        {
            "act": "say",
            "id": "cerca",
            "heading": "Cerca un'ombra",
            "lines": ["Fra poco esce un foglio."],
        },
        {
            "act": "hand_over",
            "id": "il-foglio",
            "design": {
                "title": "L'ombra di oggi",
                "instructions": "Riempi quello che vuoi.",
                "marks": [
                    {
                        "mark": "words",
                        "rect": {"x": 0.04, "y": 0.04, "w": 0.66, "h": 0.045},
                        "text": "L'ombra di oggi",
                        "size_mm": 6.5,
                    },
                    {
                        "mark": "draw_area",
                        "id": "il-disegno",
                        "rect": {"x": 0.05, "y": 0.2, "w": 0.9, "h": 0.45},
                        "label": "Disegnala qui",
                        "group": "ombra",
                    },
                ],
            },
        },
        {
            "act": "collect",
            "id": "com-e-andata",
            "outcomes": [
                {"when": "marks", "then": "ask"},
                {"when": "blank", "then": "basta"},
            ],
        },
        {
            "act": "close",
            "id": "basta",
            "heading": "Basta così",
            "lines": ["Il foglio resta con te."],
        },
    ],
}


class Router:
    """Stands in for the cloud. Keeps the request so the prompt can be looked at."""

    def __init__(self, body: str) -> None:
        self.body = body
        self.asked: ModelRequest | None = None
        self.last_usage = None

    async def generate_for_user(self, request: ModelRequest) -> ScreenedPayload:
        self.asked = request
        record = ScreeningRecord(verdict=SafetyVerdict.ALLOW, screener="a test")
        sealer = Sealer(SealPurpose.CONTENT_SAFETY, b"k" * 32, "test")
        draft = {"kind": str(ContentKind.EXERCISE_JSON), "body": self.body}
        return ScreenedPayload(
            kind=ContentKind.EXERCISE_JSON,
            body=self.body,
            record=record,
            seal=sealer.seal(draft),
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
    assert "Write it in English" in prompt
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
