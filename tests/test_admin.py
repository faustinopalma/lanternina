"""The administration surface, and the one thing it must never do.

The interesting tests here are not "an administrator can admit a parent". They are the
refusals: a token that is valid in every respect except the role, a parent's token, and a
deployment where nobody configured an administrator at all.
"""

from __future__ import annotations

import time
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import FastAPI
from fastapi.testclient import TestClient

from panel.admin import ADMISSIONS
from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from panel.tokens import TokenVerifier
from shared.accounts import AccountStatus

ISSUER = "https://login.microsoftonline.com/937847db/v2.0"
AUDIENCE = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
ROLE = "Lanternina.Admin"
ADMIN_SUBJECT = "admin-oid"
ADMIN_CONTACT = "admin@example.test"
PARENT = "parent@example.test"


@pytest.fixture(scope="module")
def keypair() -> tuple[Any, Any]:
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private, private.public_key()


class FixedKey:
    def __init__(self, key: Any) -> None:
        self._key = key

    def key_for(self, token: str) -> Any:
        return self._key


def admin_token(private: Any, **overrides: Any) -> str:
    now = int(time.time())
    claims: dict[str, Any] = {
        "iss": ISSUER,
        "aud": AUDIENCE,
        "sub": ADMIN_SUBJECT,
        "preferred_username": ADMIN_CONTACT,
        "roles": [ROLE],
        "iat": now,
        "exp": now + 300,
    }
    claims.update(overrides)
    for key, value in list(claims.items()):
        if value is None:
            del claims[key]
    return jwt.encode(claims, private, algorithm="RS256")


def panel(
    public: Any, *, required_role: str = ROLE, configured: bool = True
) -> tuple[TestClient, InMemoryAccountStore, FastAPI]:
    store = InMemoryAccountStore()
    settings = Settings(
        dev_auth=True,
        bootstrap_contact="",
        admin_oidc_authority="https://provider.example.test/v2.0" if configured else "",
        admin_oidc_audience=AUDIENCE if configured else "",
    )
    app = create_app(store=store, settings=settings)
    # Supplied rather than fetched: the discovery document lives on the internet, and the
    # panel has no development shortcut into the administration routes on purpose.
    app.state.admin_verifier = TokenVerifier(
        issuer=ISSUER, audience=AUDIENCE, keys=FixedKey(public), required_role=required_role
    )
    return TestClient(app), store, app


def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def sign_up(client: TestClient, subject: str, contact: str = PARENT) -> None:
    """A parent signs in for the first time and is recorded as pending."""
    client.get("/api/me", headers={DEV_SUBJECT_HEADER: subject, DEV_CONTACT_HEADER: contact})


def test_an_administrator_sees_who_is_waiting(keypair: tuple[Any, Any]) -> None:
    private, public = keypair
    client, _store, _app = panel(public)
    sign_up(client, "sub-one")

    answer = client.get("/api/admin/accounts", headers=bearer(admin_token(private)))

    assert answer.status_code == 200
    waiting = answer.json()["accounts"]
    assert [row["contact"] for row in waiting] == [PARENT]
    assert waiting[0]["status"] == AccountStatus.PENDING


def test_the_waiting_list_says_nothing_about_a_household_or_a_subject(
    keypair: tuple[Any, Any],
) -> None:
    """An administrator decides on an address. Everything else about a family is none of
    their business, and the way to keep it that way is to not send it."""
    private, public = keypair
    client, _store, _app = panel(public)
    sign_up(client, "sub-one")

    row = client.get("/api/admin/accounts", headers=bearer(admin_token(private))).json()[
        "accounts"
    ][0]

    assert set(row) == {"id", "contact", "status", "createdAt", "decidedAt"}


def test_admitting_records_the_administrator_who_decided(keypair: tuple[Any, Any]) -> None:
    private, public = keypair
    client, store, _app = panel(public)
    sign_up(client, "sub-one")
    account_id = store.by_subject("sub-one").id  # type: ignore[union-attr]

    answer = client.post(
        f"/api/admin/accounts/{account_id}/decision",
        json={"state": "active", "note": "known to me"},
        headers=bearer(admin_token(private)),
    )

    assert answer.status_code == 200
    decided = store.by_subject("sub-one")
    assert decided is not None
    assert decided.status is AccountStatus.ACTIVE
    # The subject, not the address: an address can change in the directory, and a decision
    # already taken must not be re-attributed when it does.
    assert decided.decided_by == ADMIN_SUBJECT
    assert decided.note == "known to me"


def test_an_admitted_parent_can_then_use_the_panel(keypair: tuple[Any, Any]) -> None:
    """The point of the whole surface, stated once end to end."""
    private, public = keypair
    client, store, _app = panel(public)
    sign_up(client, "sub-one")
    assert client.get("/api/me", headers={DEV_SUBJECT_HEADER: "sub-one"}).status_code == 403

    account_id = store.by_subject("sub-one").id  # type: ignore[union-attr]
    client.post(
        f"/api/admin/accounts/{account_id}/decision",
        json={"state": "active"},
        headers=bearer(admin_token(private)),
    )

    assert client.get("/api/me", headers={DEV_SUBJECT_HEADER: "sub-one"}).status_code == 200


def test_a_token_without_the_role_is_refused(keypair: tuple[Any, Any]) -> None:
    """Valid signature, right issuer, right audience, not expired — and no role.

    Checked against a control: the same token, verified without a required role, is
    accepted. Without that line the test would pass for any reason at all.
    """
    private, public = keypair
    client, _store, _app = panel(public)

    refused = client.get(
        "/api/admin/accounts", headers=bearer(admin_token(private, roles=None))
    )
    assert refused.status_code == 403

    permissive, _store, _app = panel(public, required_role="")
    assert (
        permissive.get(
            "/api/admin/accounts", headers=bearer(admin_token(private, roles=None))
        ).status_code
        == 200
    )


def test_a_different_role_does_not_open_the_door(keypair: tuple[Any, Any]) -> None:
    private, public = keypair
    client, _store, _app = panel(public)

    answer = client.get(
        "/api/admin/accounts", headers=bearer(admin_token(private, roles=["Lanternina.Reader"]))
    )

    assert answer.status_code == 403


def test_a_parents_dev_header_opens_nothing(keypair: tuple[Any, Any]) -> None:
    """``LANTERNINA_DEV_AUTH`` is on in these settings, and it is a parent's shortcut.

    If it reached here it would be a request header that admits accounts.
    """
    _private, public = keypair
    client, _store, _app = panel(public)

    answer = client.get(
        "/api/admin/accounts",
        headers={DEV_SUBJECT_HEADER: "sub-one", DEV_CONTACT_HEADER: PARENT},
    )

    assert answer.status_code == 403


def test_without_an_administrator_provider_the_routes_are_shut(
    keypair: tuple[Any, Any],
) -> None:
    """Unconfigured answers 503, not 403: the remedy is ours, not the caller's."""
    private, public = keypair
    client, _store, _app = panel(public, configured=False)

    answer = client.get("/api/admin/accounts", headers=bearer(admin_token(private)))

    assert answer.status_code == 503
    assert answer.json()["detail"] == "auth_not_configured"


def test_only_the_two_admissible_states_are_accepted(keypair: tuple[Any, Any]) -> None:
    private, public = keypair
    client, store, _app = panel(public)
    sign_up(client, "sub-one")
    account_id = store.by_subject("sub-one").id  # type: ignore[union-attr]

    for state in ("pending", "suspended", "approved", ""):
        answer = client.post(
            f"/api/admin/accounts/{account_id}/decision",
            json={"state": state},
            headers=bearer(admin_token(private)),
        )
        assert answer.status_code == 400, state

    assert {status.value for status in ADMISSIONS} == {"active", "rejected"}


def test_an_unknown_account_is_a_404_and_changes_nothing(keypair: tuple[Any, Any]) -> None:
    private, public = keypair
    client, store, _app = panel(public)

    answer = client.post(
        "/api/admin/accounts/ac_nosuchid/decision",
        json={"state": "active"},
        headers=bearer(admin_token(private)),
    )

    assert answer.status_code == 404
    assert not store.has_active()
