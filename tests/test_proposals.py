"""Proposals through the panel: submitted by the home server, decided by the parent.

The properties worth pinning are the boundaries, not the happy path: a household must not
see another household's proposals, the device routes must be shut unless a key is
configured, and deciding must persist without starting anything.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.proposals import InMemoryProposalStore
from panel.store import InMemoryAccountStore

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"

PROPOSAL = {
    "id": "pr_test01",
    "kind": "routine_prompt",
    "agent": "content",
    "rationale": "promemoria per la sera",
    "createdAt": 1.0,
    "payload": {"kind": "routine_prompt", "body": "Verso le 17:30, puoi sistemare lo zaino."},
    "payloadSeal": {"purpose": "content-safety", "signature": "abc"},
}


def client_for(*, device_key: str = DEVICE_KEY) -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=device_key)
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            proposals=InMemoryProposalStore(),
        )
    )


def headers(subject: str = "parent-1", contact: str = PARENT) -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: subject, DEV_CONTACT_HEADER: contact}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def submit(client: TestClient, household: str, proposal: dict[str, object]) -> None:
    response = client.post(
        f"/api/device/{household}/proposals",
        json=[proposal],
        headers={"X-Device-Key": DEVICE_KEY},
    )
    assert response.status_code == 200, response.text


def test_the_parent_sees_what_the_home_server_submitted() -> None:
    client = client_for()
    household = household_of(client)
    submit(client, household, PROPOSAL)

    listed = client.get("/api/proposals", headers=headers()).json()["proposals"]
    assert [row["id"] for row in listed] == ["pr_test01"]
    assert listed[0]["body"].startswith("Verso le 17:30")
    assert listed[0]["rationale"] == "promemoria per la sera"


def test_deciding_persists_and_the_home_server_finds_it_when_it_asks() -> None:
    client = client_for()
    household = household_of(client)
    submit(client, household, PROPOSAL)

    decided = client.post(
        "/api/proposals/pr_test01/decision",
        json={"state": "approved", "note": "va bene"},
        headers=headers(),
    )
    assert decided.status_code == 200
    assert decided.json()["state"] == "approved"
    assert client.get("/api/proposals", headers=headers()).json()["proposals"] == []

    pulled = client.get(
        f"/api/device/{household}/proposals",
        headers={"X-Device-Key": DEVICE_KEY},
    ).json()["proposals"]
    assert len(pulled) == 1
    # The safety seal survives the round trip, so the home server can verify it itself.
    assert pulled[0]["payloadSeal"] == PROPOSAL["payloadSeal"]
    assert pulled[0]["payload"] == PROPOSAL["payload"]


def test_a_rejected_proposal_is_never_offered_to_the_home_server() -> None:
    client = client_for()
    household = household_of(client)
    submit(client, household, PROPOSAL)
    client.post(
        "/api/proposals/pr_test01/decision", json={"state": "rejected"}, headers=headers()
    )

    pulled = client.get(
        f"/api/device/{household}/proposals", headers={"X-Device-Key": DEVICE_KEY}
    ).json()["proposals"]
    assert pulled == []


def test_a_parent_cannot_invent_a_state() -> None:
    client = client_for()
    submit(client, household_of(client), PROPOSAL)
    response = client.post(
        "/api/proposals/pr_test01/decision", json={"state": "approved_by_me"}, headers=headers()
    )
    assert response.status_code == 400


def test_another_household_sees_nothing() -> None:
    client = client_for()
    submit(client, "hh_someone_else", PROPOSAL)
    assert client.get("/api/proposals", headers=headers()).json()["proposals"] == []


def test_device_routes_are_shut_without_a_key() -> None:
    client = client_for(device_key="")
    response = client.get("/api/device/hh_x/proposals", headers={"X-Device-Key": "guess"})
    assert response.status_code == 503


def test_device_routes_refuse_a_wrong_key() -> None:
    client = client_for()
    response = client.get("/api/device/hh_x/proposals", headers={"X-Device-Key": "wrong"})
    assert response.status_code == 403


def test_submitting_twice_does_not_duplicate() -> None:
    client = client_for()
    household = household_of(client)
    submit(client, household, PROPOSAL)
    submit(client, household, PROPOSAL)
    listed = client.get("/api/proposals", headers=headers()).json()["proposals"]
    assert len(listed) == 1
