"""The two routes a house calls, and what a parent may do between them.

What is checked here is our half. The model is stood in for, because a test that measures
the cloud measures the cloud. The direction is checked as well: there is nothing in these
routes that lets the panel start or extend an afternoon, and a test that names the routes
is the only way that stays true as routes are added.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import afternoons as a
import pytest
from fastapi.testclient import TestClient

from panel.app import create_app
from panel.config import Settings
from panel.preferences import LANGUAGE_CHOICES, LANGUAGE_NAMES
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from shared.capabilities import HouseCapability
from shared.errors import CloudUnavailable, SafetyBlocked
from shared.experience import Continuation, Experience, ExperienceError

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
THE_AFTERNOON = json.loads(
    Path("experiences/un-pomeriggio-di-nuvole.json").read_text(encoding="utf-8")
)

THE_REST: dict[str, Any] = {
    "format_version": 2,
    "experience_id": "un-pomeriggio-di-nuvole",
    "after": "l-ultimo-foglio",
    "moments": [
        a.close(
            moment_id="due-nuvole",
            heading="Due nuvole",
            weights=a.weights(lines=("Il foglio resta sul tavolo.",)),
        )
    ],
}


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(create_app(store=InMemoryAccountStore(), settings=settings))


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def answering(monkeypatch: pytest.MonkeyPatch, outcome: Any) -> dict[str, Any]:
    """Stand in for the cloud. ``outcome`` is a payload to return or an exception to raise."""
    asked: dict[str, Any] = {}

    async def _continue(**given: Any) -> Any:
        asked.update(given)
        if isinstance(outcome, Exception):
            raise outcome
        return Continuation.from_dict(outcome), None

    monkeypatch.setattr("panel.continuing.continue_experience", _continue)
    return asked


def post(client: TestClient, household: str, **changes: Any) -> Any:
    body: dict[str, Any] = {
        "experience": THE_AFTERNOON,
        "after": "l-ultimo-foglio",
        "came": "marks",
        "reading": {"cells": [{"cell_id": "la-nuvola", "label": "Disegnala qui", "value": "x"}]},
    }
    body.update(changes)
    return client.post(
        f"/api/device/{household}/experience",
        json=body,
        headers={"X-Device-Key": DEVICE_KEY},
    )


# ── The afternoon carries on ─────────────────────────────────────────────────────────


def test_the_rest_of_the_afternoon_comes_back_in_the_reply(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    asked = answering(monkeypatch, THE_REST)

    response = post(client, household_of(client))

    assert response.status_code == 200
    assert response.json()["moments"][0]["heading"] == "Due nuvole"
    # The document reaching the model is the parsed one, not the bytes that arrived.
    assert asked["experience"]["experience_id"] == "un-pomeriggio-di-nuvole"
    assert asked["after"] == "l-ultimo-foglio"
    assert asked["came"] == "marks"


def test_the_call_is_written_down_against_the_household(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    answering(monkeypatch, THE_REST)
    household = household_of(client)

    post(client, household)

    usage = client.get("/api/usage", headers=headers()).json()
    assert usage["usage"]["total"]["calls"] == 1


# ── The four ways it says no ─────────────────────────────────────────────────────────


def test_a_branch_that_already_says_what_happens_is_not_paid_for(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`come-e-tornato` names both its outcomes. Asking about it buys a step somebody wrote."""
    client = client_for()
    asked = answering(monkeypatch, THE_REST)

    response = post(client, household_of(client), after="come-e-tornato")

    assert response.status_code == 400
    assert "already says" in response.json()["detail"]
    assert asked == {}, "nothing was asked of the cloud"


def test_a_moment_that_does_not_read_a_page_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    answering(monkeypatch, THE_REST)

    response = post(client, household_of(client), after="comincia")

    assert response.status_code == 400
    assert "does not read a page" in response.json()["detail"]


def test_the_gate_refusing_ends_the_afternoon_rather_than_degrading_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """There is nothing to fall back on: nobody wrote what comes after this branch."""
    client = client_for()
    answering(monkeypatch, SafetyBlocked("refused at severity 4: violence"))

    response = post(client, household_of(client))

    assert response.status_code == 422
    assert response.json()["detail"] == "refused_by_the_gate"


def test_an_answer_that_is_not_a_continuation_is_not_half_played(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    answering(monkeypatch, ExperienceError("two moments share an id"))

    response = post(client, household_of(client))

    assert response.status_code == 502


def test_the_cloud_being_unreachable_stops_the_afternoon(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    answering(monkeypatch, CloudUnavailable("no route"))

    response = post(client, household_of(client))

    assert response.status_code == 503


def test_the_monthly_cap_is_refused_and_nothing_is_asked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings(
        dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY, monthly_limit=1
    )
    client = TestClient(create_app(store=InMemoryAccountStore(), settings=settings))
    asked = answering(monkeypatch, THE_REST)
    household = household_of(client)

    assert post(client, household).status_code == 200
    asked.clear()
    second = post(client, household)

    assert second.status_code == 429
    assert asked == {}


# ── Devising one, and the parent deciding about it ───────────────────────────────────


def devising(monkeypatch: pytest.MonkeyPatch, outcome: Any) -> dict[str, Any]:
    """Stand in for the cloud. ``outcome`` is a document to return or an exception."""
    asked: dict[str, Any] = {}

    async def _devise(**given: Any) -> Any:
        asked.update(given)
        if isinstance(outcome, Exception):
            raise outcome
        return Experience.from_dict(outcome), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    return asked


def ask_for_one(client: TestClient, household: str, **changes: Any) -> Any:
    body: dict[str, Any] = {"capabilities": ["print_a4", "scan_a4", "show_800x480_1bit"]}
    body.update(changes)
    return client.post(
        f"/api/device/{household}/experiences",
        json=body,
        headers={"X-Device-Key": DEVICE_KEY},
    )


def what_the_house_may_run(client: TestClient, household: str) -> Any:
    response = client.get(
        f"/api/device/{household}/experiences", headers={"X-Device-Key": DEVICE_KEY}
    )
    return response.json()["experiences"]


def test_a_devised_afternoon_waits_for_the_parent_rather_than_going_home(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The house asked and was answered, and still may not run it. That is the shape of
    approval: nothing reaches an adolescent because a machine wanted it to."""
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)

    response = ask_for_one(client, household)

    assert response.status_code == 200
    assert response.json()["state"] == "pending"
    assert what_the_house_may_run(client, household) == []


def test_the_parent_reads_the_overview_and_may_read_every_branch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    ask_for_one(client, household_of(client))

    waiting = client.get("/api/experiences", headers=headers()).json()["experiences"]

    assert len(waiting) == 1
    assert waiting[0]["overview"].startswith("Il display dice")
    assert [m["id"] for m in waiting[0]["experience"]["moments"]][0] == "comincia"


def test_the_house_may_run_it_once_it_is_approved_and_not_before(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    offered = ask_for_one(client, household).json()["id"]

    client.post(
        f"/api/experiences/{offered}/decision",
        json={"state": "approved"},
        headers=headers(),
    )

    runnable = what_the_house_may_run(client, household)
    assert [row["id"] for row in runnable] == [offered]
    assert runnable[0]["experience"]["title"] == "Un pomeriggio di nuvole"


def test_withdrawing_takes_it_back_out_of_what_the_house_may_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    offered = ask_for_one(client, household).json()["id"]
    client.post(
        f"/api/experiences/{offered}/decision",
        json={"state": "approved"},
        headers=headers(),
    )

    taken_back = client.post(
        f"/api/experiences/{offered}/decision",
        json={"state": "withdrawn"},
        headers=headers(),
    )

    assert taken_back.status_code == 200
    assert what_the_house_may_run(client, household) == []


def approve(client: TestClient, offered: str) -> Any:
    return client.post(
        f"/api/experiences/{offered}/decision",
        json={"state": "approved"},
        headers=headers(),
    )


def test_the_house_is_told_how_many_are_still_with_the_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """So that it does not ask for a second afternoon while the first is unread. It is the
    depth of somebody's inbox and says nothing about anybody's afternoon."""
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    ask_for_one(client, household)

    answer = client.get(
        f"/api/device/{household}/experiences", headers={"X-Device-Key": DEVICE_KEY}
    ).json()

    assert answer["waiting"] == 1
    assert answer["experiences"] == []


def test_the_house_cannot_pull_a_document_the_parent_has_not_approved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """There used to be a state parameter here. A house able to fetch a pending document
    could run one, and then approval would be held up by the hub's code, not by this."""
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    ask_for_one(client, household)

    asked = client.get(
        f"/api/device/{household}/experiences?state=pending",
        headers={"X-Device-Key": DEVICE_KEY},
    ).json()

    assert asked["experiences"] == []


def test_an_afternoon_the_house_began_is_not_handed_over_again(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Otherwise the same approved afternoon happens every day the parent forgets to
    withdraw it, which is an approval nobody gave."""
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    offered = ask_for_one(client, household).json()["id"]
    approve(client, offered)
    assert [row["id"] for row in what_the_house_may_run(client, household)] == [offered]

    said = client.post(
        f"/api/device/{household}/experiences/{offered}/begun",
        headers={"X-Device-Key": DEVICE_KEY},
    )

    assert said.status_code == 200
    assert said.json()["begunAt"] > 0
    assert what_the_house_may_run(client, household) == []


def test_saying_it_began_twice_does_not_move_the_moment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A hub that retries is a retry, not a second afternoon."""
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    offered = ask_for_one(client, household).json()["id"]
    approve(client, offered)

    first = client.post(
        f"/api/device/{household}/experiences/{offered}/begun",
        headers={"X-Device-Key": DEVICE_KEY},
    ).json()["begunAt"]
    again = client.post(
        f"/api/device/{household}/experiences/{offered}/begun",
        headers={"X-Device-Key": DEVICE_KEY},
    ).json()["begunAt"]

    assert first == again


def test_a_browser_cannot_say_an_afternoon_began(monkeypatch: pytest.MonkeyPatch) -> None:
    """It is a fact about the house, written by the house. The parent's word stays the
    state, and nothing a browser can reach writes this one."""
    client = client_for()
    devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    offered = ask_for_one(client, household).json()["id"]

    refused = client.post(
        f"/api/device/{household}/experiences/{offered}/begun", headers=headers()
    )

    assert refused.status_code == 403


def test_only_what_the_afternoons_were_is_handed_to_the_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """What they were called, how they worked and what they were about — so that the next
    one is different, and nothing else: not who did them, not how far anybody got, not what
    came back."""
    client = client_for()
    asked = devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    ask_for_one(client, household)
    asked.clear()

    ask_for_one(client, household)

    assert asked["already"] == ("Un pomeriggio di nuvole",)
    assert set(asked) == {
        "capabilities",
        "language",
        "interests",
        "avoid",
        "already",
        "recent",
        "subjects",
        # How many things an afternoon holds together at once, and how long a line runs.
        # Both are properties of the material; neither says anything about a person.
        "difficulty",
        "words_per_line",
        "now",
    }


def test_what_the_parent_wrote_in_their_settings_is_what_is_devised_from(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    asked = devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    client.post(
        "/api/preferences",
        json={
            "interests": ["le nuvole"],
            "avoid": ["i ragni"],
            "difficulty": "gentle",
            "variety": "balanced",
            "maxWordsPerLine": 6,
            "language": "en",
        },
        headers=headers(),
    )

    ask_for_one(client, household)

    assert asked["language"] == "English", "the code is a pronoun in an English sentence"
    assert asked["interests"] == ("le nuvole",)
    assert asked["avoid"] == ("i ragni",)


def test_the_shape_the_parent_chose_reaches_the_prompt_as_a_sentence_about_the_material(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chosen in the panel since the first version and read by nothing until 27 August 2026:
    it was stored, shown back, and dropped on the way to the model. A parent moving it saw
    no change in what arrived, which is worse than not offering the choice."""
    from agents.experience_deviser import SHAPES, the_prompt

    client = client_for()
    asked = devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)
    client.post(
        "/api/preferences",
        json={
            "interests": [],
            "avoid": [],
            "difficulty": "stretch",
            "variety": "balanced",
            "maxWordsPerLine": 8,
            "language": "it",
        },
        headers=headers(),
    )

    ask_for_one(client, household)

    assert asked["difficulty"] == "stretch"
    assert asked["words_per_line"] == 8
    written = the_prompt(
        language="Italian",
        capabilities=frozenset(),
        shape=SHAPES["stretch"],
        words_per_line=8,
    )
    assert SHAPES["stretch"] in written
    assert "about 8 words" in written
    assert "gentle" not in written and "stretch" not in written, (
        "the word a parent picked is a setting; what the model reads is a property of "
        "the material, and nothing in the prompt may name the choice itself"
    )


def test_the_language_reaches_the_model_by_name_and_not_by_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Measured on the house on 21 August 2026: a household set to "it" was handed the
    sentence "Write it in it.", and the afternoon came back in English. Every choice must
    have a name, or the next one added repeats it."""
    client = client_for()
    asked = devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)

    for code in LANGUAGE_CHOICES:
        client.post(
            "/api/preferences",
            json={
                "interests": [],
                "avoid": [],
                "difficulty": "gentle",
                "variety": "balanced",
                "maxWordsPerLine": 6,
                "language": code,
            },
            headers=headers(),
        )
        ask_for_one(client, household)
        assert asked["language"] == LANGUAGE_NAMES[code]
        assert asked["language"] != code


def test_equipment_the_house_does_not_have_is_not_devised_for(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    asked = devising(monkeypatch, THE_AFTERNOON)

    ask_for_one(client, household_of(client), capabilities=["show_800x480_1bit"])

    assert asked["capabilities"] == frozenset({HouseCapability.SHOW_800X480_1BIT})


def test_a_house_that_claims_equipment_nobody_defined_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    asked = devising(monkeypatch, THE_AFTERNOON)

    response = ask_for_one(client, household_of(client), capabilities=["read_minds"])

    assert response.status_code == 400
    assert asked == {}, "nothing was asked of the cloud"


def test_an_afternoon_the_gate_refuses_is_not_stored_for_anybody_to_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    devising(monkeypatch, SafetyBlocked("refused at severity 4: violence"))
    household = household_of(client)

    response = ask_for_one(client, household)

    assert response.status_code == 422
    assert client.get("/api/experiences", headers=headers()).json()["experiences"] == []


def test_the_cap_stops_an_afternoon_being_devised(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = Settings(
        dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY, monthly_limit=1
    )
    client = TestClient(create_app(store=InMemoryAccountStore(), settings=settings))
    asked = devising(monkeypatch, THE_AFTERNOON)
    household = household_of(client)

    assert ask_for_one(client, household).status_code == 200
    asked.clear()

    assert ask_for_one(client, household).status_code == 429
    assert asked == {}


def test_the_hub_cannot_ask_without_the_device_key() -> None:
    client = client_for()
    household = household_of(client)

    assert client.post(f"/api/device/{household}/experience", json={}).status_code == 403


# ── The direction ────────────────────────────────────────────────────────────────────


def test_nothing_in_the_panel_can_start_or_change_an_afternoon() -> None:
    """The rule that was not smoothed, pinned by naming every route this feature has.

    Three of these are the house calling; the three a browser can call are a list and two
    ways of recording a decision — one card, or a handful in a sitting. There is no path a
    browser could use to put moments into a house, and this test fails the moment somebody
    adds one, which is the only way that stays true.
    """
    client = client_for()
    published = client.get("/openapi.json").json()["paths"]
    paths = {path: sorted(published[path]) for path in published if "experience" in path}

    assert paths == {
        "/api/device/{household_id}/experience": ["post"],
        "/api/device/{household_id}/experiences": ["get", "post"],
        "/api/device/{household_id}/experiences/{experience_id}/begun": ["post"],
        "/api/experiences": ["get"],
        "/api/experiences/decisions": ["post"],
        "/api/experiences/{experience_id}/decision": ["post"],
    }
