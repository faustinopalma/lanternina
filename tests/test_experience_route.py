"""The route that answers an ask, and the four ways it says no.

What is checked here is our half. The model is stood in for, because a test that measures
the cloud measures the cloud. The direction is checked as well: there is nothing in this
route that lets the panel start or extend an afternoon, and a test that names the routes
is the only way that stays true as routes are added.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from shared.errors import CloudUnavailable, SafetyBlocked
from shared.experience import Continuation, ExperienceError

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
THE_AFTERNOON = json.loads(
    Path("experiences/un-pomeriggio-di-nuvole.json").read_text(encoding="utf-8")
)

THE_REST: dict[str, Any] = {
    "format_version": 1,
    "experience_id": "un-pomeriggio-di-nuvole",
    "after": "l-ultimo-foglio",
    "moments": [
        {
            "act": "close",
            "id": "due-nuvole",
            "heading": "Due nuvole",
            "lines": ["Restano sul tavolo."],
        }
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
        dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY, monthly_call_cap=1
    )
    client = TestClient(create_app(store=InMemoryAccountStore(), settings=settings))
    asked = answering(monkeypatch, THE_REST)
    household = household_of(client)

    assert post(client, household).status_code == 200
    asked.clear()
    second = post(client, household)

    assert second.status_code == 429
    assert asked == {}


def test_the_hub_cannot_ask_without_the_device_key() -> None:
    client = client_for()
    household = household_of(client)

    assert client.post(f"/api/device/{household}/experience", json={}).status_code == 403


# ── The direction ────────────────────────────────────────────────────────────────────


def test_nothing_in_the_panel_can_start_or_change_an_afternoon() -> None:
    """The rule that was not smoothed. Every path this feature adds is one the house
    calls; there is no route a browser could use to put moments into a house."""
    client = client_for()
    published = client.get("/openapi.json").json()["paths"]
    paths = {path for path in published if "experience" in path}

    assert paths == {"/api/device/{household_id}/experience"}
