"""A parent working on an idea of their own.

Three things are worth pinning, and two of them are about where the line moved. This is the
one place a parent's own action calls a model, so the cap has to govern it and a test has to
say so. A draft holds the idea and never the plan, because free text cannot become a format
with a dozen checks behind it — approval hands the script to the deviser and everything runs
unchanged. And typing costs nothing, because asking a model to change one word is slower
than changing it and worse.
"""

from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from agents.idea_editor import Idea, idea_in, the_prompt
from panel.app import create_app
from panel.config import Settings
from panel.drafts import MAX_SAYING, Draft, InMemoryDraftStore, Said, cleaned
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from shared.experience import Experience, ExperienceError

PARENT = "parent@example.test"
THE_AFTERNOON = json.loads(
    Path("experiences/un-pomeriggio-di-nuvole.json").read_text(encoding="utf-8")
)


def client_for(**settings: Any) -> TestClient:
    kept = Settings(dev_auth=True, bootstrap_contact=PARENT, **settings)
    return TestClient(create_app(store=InMemoryAccountStore(), settings=kept))


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def an_idea(**changes: Any) -> Idea:
    kept: dict[str, Any] = {
        "reply": "Ho spostato il finale in cucina.",
        "title": "Le ventitré tacche",
        "overview": "Si conta quello che non c'è più.",
        "themes": ("memoria domestica", "pane"),
        "script": "THE WORLD\nUn pensile che nessuno apre.",
    }
    kept.update(changes)
    return Idea(**kept)


def rewriting(monkeypatch: pytest.MonkeyPatch, outcome: Any) -> dict[str, Any]:
    """Stand in for the cloud. ``outcome`` is an idea to return or an exception to raise."""
    asked: dict[str, Any] = {}

    async def _rewrite(**given: Any) -> Any:
        asked.update(given)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome, None

    monkeypatch.setattr("panel.editing.rewrite_the_idea", _rewrite)
    return asked


def start(client: TestClient, **body: Any) -> Any:
    return client.post("/api/drafts", json={"fromExperience": "", **body}, headers=headers())


# ── What a draft is ──────────────────────────────────────────────────────────────────


def test_a_draft_holds_the_idea_and_never_the_plan() -> None:
    """The four things an afternoon is approved by, and nothing with moments in it.

    A field for the plan would invite a parent to edit one, and a plan edited as free text
    fails the format after they had finished with it.
    """
    bookkeeping = {"id", "household_id", "created_at", "updated_at", "state", "said"}
    lineage = {"started_from", "became"}
    the_idea = {"title", "overview", "themes", "script"}

    held = {row.name for row in fields(Draft)}

    assert held == bookkeeping | lineage | the_idea


def test_a_turn_has_two_speakers_and_no_third() -> None:
    held = {row.name for row in fields(Said)}
    assert held == {"who", "words", "at"}


def test_a_pasted_document_is_refused_rather_than_cut() -> None:
    """Truncating is worse: the parent would never know which half the model was given."""
    assert cleaned("  spostalo in cucina ", "x") == "spostalo in cucina"
    with pytest.raises(ValueError):
        cleaned("x" * (MAX_SAYING + 1), "x")


def test_the_conversation_carried_to_the_model_is_bounded() -> None:
    """The whole thing is kept and shown; a prompt that grows without bound gets dearer
    every turn and its oldest turn is the least useful thing in it."""
    draft = Draft(
        id="d",
        household_id="h",
        created_at=0.0,
        said=tuple(Said(who="parent", words=str(n), at=float(n)) for n in range(40)),
    )

    assert len(draft.carrying()) == 12
    assert draft.carrying()[0].words == "28"


def test_one_household_cannot_see_another() -> None:
    store = InMemoryDraftStore()
    store.start(Draft(id="d1", household_id="h1", created_at=1.0))

    assert store.list("h2") == []
    assert store.get("h2", "d1") is None


# ── What the model is given, and what it may answer ──────────────────────────────────


def test_the_prompt_carries_the_draft_and_what_was_just_said() -> None:
    prompt = the_prompt(
        language="Italian",
        title="Le nuvole",
        overview="Si guarda il cielo.",
        themes=["cielo"],
        script="THE WORLD\nUna finestra.",
        said=[Said(who="parent", words="più corta", at=1.0)],
        asking="spostala in cucina",
    )

    assert "spostala in cucina" in prompt
    assert "Una finestra" in prompt
    assert "più corta" in prompt
    # A blank draft is named as blank, because writing from nothing is a different job
    # from changing something.
    assert "Is it blank: no" in prompt


def test_a_blank_draft_says_so() -> None:
    prompt = the_prompt(
        language="Italian",
        title="",
        overview="",
        themes=[],
        script="",
        said=[],
        asking="qualcosa sul pane",
    )

    assert "Is it blank: yes" in prompt


def test_an_answer_past_the_format_is_refused() -> None:
    """The bounds are the format's own, so a draft that passes here is one the deviser can
    be given and a parent can be shown."""
    with pytest.raises(ExperienceError):
        idea_in(json.dumps({"reply": "x", "title": "t", "overview": "o", "script": "s" * 9000}))
    with pytest.raises(ExperienceError):
        idea_in("not json at all")


def test_an_answer_wrapped_in_a_sentence_is_still_an_answer() -> None:
    """Refusing that would cost a turn to punish something nobody in the house can see."""
    said = idea_in('Ecco:\n```json\n{"reply": "fatto", "title": "T", "script": "S"}\n```')

    assert said.reply == "fatto"
    assert said.title == "T"


# ── The routes ───────────────────────────────────────────────────────────────────────


def test_starting_one_calls_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Opening a draft is inert. The first message is what spends anything."""
    client = client_for()
    called: list[str] = []

    async def _never(**_: Any) -> Any:
        called.append("asked")
        raise AssertionError("a draft must not call a model until the parent says something")

    monkeypatch.setattr("panel.editing.rewrite_the_idea", _never)

    answer = start(client)

    assert answer.status_code == 200
    assert answer.json()["said"] == []
    assert called == []


def test_a_draft_opened_from_an_afternoon_is_a_copy(monkeypatch: pytest.MonkeyPatch) -> None:
    """Taking an afternoon apart must not be a way to lose it."""
    client = client_for(device_key="k")

    async def _devise(**_: Any) -> Any:
        return Experience.from_dict(THE_AFTERNOON | {"script": "il copione"}), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    household = str(client.get("/api/me", headers=headers()).json()["householdId"])
    devised = client.post(
        f"/api/device/{household}/experiences",
        json={"capabilities": ["print_a4", "scan_a4", "show_800x480_1bit"]},
        headers={"X-Device-Key": "k"},
    ).json()

    draft = start(client, fromExperience=devised["id"]).json()
    client.post(
        f"/api/drafts/{draft['id']}/text",
        json={"script": "tutt'altro"},
        headers=headers(),
    )

    assert draft["script"] == "il copione"
    still = client.get("/api/experiences?state=pending", headers=headers()).json()
    assert still["experiences"][0]["script"] == "il copione"


def test_saying_something_rewrites_the_text_and_keeps_both_turns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    asked = rewriting(monkeypatch, an_idea())
    draft = start(client).json()

    answer = client.post(
        f"/api/drafts/{draft['id']}/say",
        json={"words": "spostala in cucina"},
        headers=headers(),
    )

    assert answer.status_code == 200
    said = answer.json()
    assert said["script"] == "THE WORLD\nUn pensile che nessuno apre."
    assert [one["who"] for one in said["said"]] == ["parent", "system"]
    assert said["said"][0]["words"] == "spostala in cucina"
    assert said["said"][1]["words"] == "Ho spostato il finale in cucina."
    assert asked["asking"] == "spostala in cucina"


def test_typing_costs_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    """A parent changing one word should not have to ask a model, and should not pay."""
    client = client_for()

    async def _never(**_: Any) -> Any:
        raise AssertionError("typing must not call a model")

    monkeypatch.setattr("panel.editing.rewrite_the_idea", _never)
    draft = start(client).json()

    answer = client.post(
        f"/api/drafts/{draft['id']}/text",
        json={"title": "Il pensile", "script": "THE WORLD\nUna cucina."},
        headers=headers(),
    )

    assert answer.status_code == 200
    assert answer.json()["title"] == "Il pensile"
    assert client.get("/api/usage", headers=headers()).json()["usage"]["total"]["calls"] == 0


def test_a_turn_is_written_down_against_the_household(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """This is the one place a parent can spend money, so it is counted like everything
    else and the monthly limit governs it."""
    client = client_for()
    rewriting(monkeypatch, an_idea())
    draft = start(client).json()

    client.post(f"/api/drafts/{draft['id']}/say", json={"words": "x"}, headers=headers())

    assert client.get("/api/usage", headers=headers()).json()["usage"]["total"]["calls"] == 1


def test_the_monthly_cap_stops_a_conversation(monkeypatch: pytest.MonkeyPatch) -> None:
    client = client_for(monthly_limit=1)
    rewriting(monkeypatch, an_idea())
    draft = start(client).json()

    first = client.post(f"/api/drafts/{draft['id']}/say", json={"words": "x"}, headers=headers())
    second = client.post(f"/api/drafts/{draft['id']}/say", json={"words": "y"}, headers=headers())

    assert first.status_code == 200
    assert second.status_code == 429


def test_approving_hands_the_script_to_the_deviser_as_a_brief(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The idea is the parent's; the machinery is the deviser's. Nothing is relaxed."""
    client = client_for()
    asked: dict[str, Any] = {}

    async def _devise(**given: Any) -> Any:
        asked.update(given)
        return Experience.from_dict(THE_AFTERNOON), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    draft = start(client).json()
    client.post(
        f"/api/drafts/{draft['id']}/text",
        json={"title": "Il pensile", "script": "THE WORLD\nUna cucina."},
        headers=headers(),
    )

    answer = client.post(f"/api/drafts/{draft['id']}/approve", headers=headers())

    assert answer.status_code == 200
    assert "Una cucina" in asked["brief"]
    assert "Il pensile" in asked["brief"]
    # Approved on the way in: the parent wrote it and pressed approve on it, and asking
    # them to find it in the pending list and approve it again is asking twice.
    approved = client.get("/api/experiences?state=approved", headers=headers()).json()
    assert len(approved["experiences"]) == 1


def test_a_refused_draft_says_why_so_the_parent_can_change_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A script asking for a scoreboard is refused by the same check whoever wrote it.
    The reason comes back because the parent has the text and can fix it."""
    from panel.devising import RefusedByTheChecks

    client = client_for()

    async def _devise(**_: Any) -> Any:
        raise RefusedByTheChecks(["a threshold that counts points"])

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    draft = start(client).json()
    client.post(
        f"/api/drafts/{draft['id']}/text", json={"script": "un punteggio"}, headers=headers()
    )

    answer = client.post(f"/api/drafts/{draft['id']}/approve", headers=headers())

    assert answer.status_code == 422
    assert "counts points" in answer.json()["detail"]
    # And the draft is still open, because the parent is going to change it.
    assert client.get(f"/api/drafts/{draft['id']}", headers=headers()).json()["state"] == "open"


def test_an_empty_draft_cannot_be_approved() -> None:
    client = client_for()
    draft = start(client).json()

    answer = client.post(f"/api/drafts/{draft['id']}/approve", headers=headers())

    assert answer.status_code == 400


def test_closing_one_ends_it() -> None:
    client = client_for()
    draft = start(client).json()

    assert client.post(f"/api/drafts/{draft['id']}/close", headers=headers()).status_code == 200
    said = client.post(f"/api/drafts/{draft['id']}/say", json={"words": "x"}, headers=headers())
    assert said.status_code == 409


def test_a_draft_belongs_to_the_household_that_opened_it() -> None:
    client = client_for()
    start(client)

    other = client.get(
        "/api/drafts/dft_nothing",
        headers=headers(),
    )
    assert other.status_code == 404


def test_the_house_cannot_reach_any_of_this() -> None:
    """A device key opens the routes the house needs and none of these. Nothing here can
    be triggered from outside the parent's own login."""
    client = client_for(device_key="k")

    for path in ("/api/drafts", "/api/drafts/dft_1/say"):
        answer = client.post(path, json={}, headers={"X-Device-Key": "k"})
        assert answer.status_code != 200, path
