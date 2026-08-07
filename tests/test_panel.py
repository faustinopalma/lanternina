"""The panel's front door.

Covers the three ways in — unconfigured, denied, bootstrapped — and the property that
matters most for a page anyone on the internet can reach: refusals must not leak who
exists.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from panel import app as panel_app
from panel.app import create_app
from panel.config import Settings
from panel.gate import BOOTSTRAP_DECIDER
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from shared.accounts import AccountStatus
from shared.errors import NotAuthenticated

PARENT = "parent@example.test"


def client_for(
    *, dev_auth: bool = True, bootstrap: str = ""
) -> tuple[TestClient, InMemoryAccountStore]:
    store = InMemoryAccountStore()
    settings = Settings(dev_auth=dev_auth, bootstrap_contact=bootstrap.casefold())
    return TestClient(create_app(store=store, settings=settings)), store


def headers(subject: str, contact: str = PARENT) -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: subject, DEV_CONTACT_HEADER: contact}


def test_health_needs_no_auth_and_no_store() -> None:
    client, _ = client_for(dev_auth=False)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class RefusingVerifier:
    def verify(self, token: str) -> object:
        raise NotAuthenticated("token rejected")


def test_a_configured_provider_beats_dev_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    """The bootstrap address is the one case a dev header would otherwise open, which is
    why it is the case worth pinning: with a provider configured it must still be shut."""
    monkeypatch.setattr(
        panel_app.TokenVerifier,
        "from_authority",
        classmethod(lambda cls, *_: RefusingVerifier()),
    )
    settings = Settings(
        dev_auth=True,
        bootstrap_contact=PARENT,
        oidc_authority="https://provider.example.test/v2.0",
        oidc_audience="an-application-id",
    )
    client = TestClient(create_app(store=InMemoryAccountStore(), settings=settings))

    response = client.get("/api/me", headers=headers("sub-abc"))

    assert response.status_code == 403


def test_without_dev_auth_the_panel_serves_nobody() -> None:
    client, _ = client_for(dev_auth=False)
    response = client.get("/api/me", headers=headers("sub-abc"))
    assert response.status_code == 503
    assert response.json()["detail"] == "auth_not_configured"


def test_dev_auth_without_a_subject_is_refused() -> None:
    client, _ = client_for()
    assert client.get("/api/me").status_code == 503


def test_a_new_caller_is_recorded_but_refused() -> None:
    client, store = client_for()

    response = client.get("/api/me", headers=headers("sub-abc"))

    assert response.status_code == 403
    recorded = store.by_subject("sub-abc")
    assert recorded is not None and recorded.status is AccountStatus.PENDING


def test_refusals_do_not_reveal_whether_an_account_exists() -> None:
    """A stranger and a known-but-pending parent must be told exactly the same thing."""
    client, store = client_for()
    client.get("/api/me", headers=headers("sub-known"))

    stranger = client.get("/api/me", headers=headers("sub-never-seen", "other@example.test"))
    known = client.get("/api/me", headers=headers("sub-known"))

    assert (stranger.status_code, stranger.json()) == (known.status_code, known.json())


def test_the_bootstrap_address_gets_in_and_is_recorded_as_such() -> None:
    client, store = client_for(bootstrap=PARENT)

    response = client.get("/api/me", headers=headers("sub-abc"))

    assert response.status_code == 200
    assert response.json()["status"] == AccountStatus.ACTIVE
    account = store.by_subject("sub-abc")
    assert account is not None and account.decided_by == BOOTSTRAP_DECIDER


def test_the_bootstrap_fires_once_even_for_the_same_address() -> None:
    """The guard is 'nobody is active yet', not 'the variable was removed'.

    Leaving LANTERNINA_BOOTSTRAP_CONTACT set after go-live must be inert rather than a
    standing invitation, because someone will forget to remove it.
    """
    client, _ = client_for(bootstrap=PARENT)
    assert client.get("/api/me", headers=headers("sub-first")).status_code == 200

    second = client.get("/api/me", headers=headers("sub-second", PARENT))

    assert second.status_code == 403


def test_a_different_address_is_never_bootstrapped() -> None:
    client, _ = client_for(bootstrap=PARENT)
    response = client.get("/api/me", headers=headers("sub-abc", "someone@example.test"))
    assert response.status_code == 403


@pytest.mark.parametrize("blocked", [AccountStatus.REJECTED, AccountStatus.SUSPENDED])
def test_a_blocked_account_is_refused_even_at_the_bootstrap_address(
    blocked: AccountStatus,
) -> None:
    client, store = client_for(bootstrap=PARENT)
    account = store.register(subject="sub-abc", contact=PARENT)
    store.decide(account.id, blocked, decided_by="admin")

    assert client.get("/api/me", headers=headers("sub-abc")).status_code == 403


def test_the_response_says_nothing_about_the_learner() -> None:
    client, _ = client_for(bootstrap=PARENT)
    body = client.get("/api/me", headers=headers("sub-abc")).json()
    assert set(body) == {"accountId", "householdId", "status"}
