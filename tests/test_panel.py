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


def test_device_key_is_bound_to_one_household() -> None:
    from panel.photos import Photo

    settings = Settings(
        dev_auth=True, bootstrap_contact="", device_key="synthetic-key-a",
        device_household="family-a",
    )
    app = create_app(settings=settings)
    app.state.photos.save(
        "family-b", Photo("b" * 32, "camera", 1, 1, 1, 1, "done", "digest"), b"image",
    )
    client = TestClient(app)
    device = {"X-Device-Key": "synthetic-key-a"}
    assert client.get("/api/device/family-a/photos/deleted", headers=device).status_code == 200
    assert client.get("/api/device/family-b/photos/deleted", headers=device).status_code == 403
    assert client.post(
        f"/api/device/family-b/photos/{'b' * 32}/delete", headers=device,
    ).status_code == 403
    assert app.state.photos.get("family-b", "b" * 32) == b"image"


def test_every_device_route_rejects_a_different_household_before_running() -> None:
    from hashlib import sha256

    client = TestClient(create_app(settings=Settings(
        dev_auth=False, bootstrap_contact="",
        device_key_hashes=(("family-a", sha256(b"key-a").hexdigest()),
                           ("family-b", sha256(b"key-b").hexdigest())),
    )))
    checked = 0
    for path, operations in client.app.openapi()["paths"].items():
        if not path.startswith("/api/device/"):
            continue
        assert "{household_id}" in path
        import re

        url = re.sub(r"\{[^}]+\}", "probe", path.replace("{household_id}", "family-b"))
        for method in operations:
            if method not in {"get", "post", "delete", "put", "patch"}:
                continue
            for key in ("key-a", "", "wrong"):
                response = client.request(method, url, headers={"X-Device-Key": key})
                assert response.status_code == 403, (method, path, response.text)
                checked += 1
    assert checked > 60
    assert client.get(
        "/api/device/family-b/photos/deleted", headers={"X-Device-Key": "key-b"},
    ).status_code == 200


def test_device_key_without_household_fails_closed() -> None:
    client = TestClient(create_app(settings=Settings(
        dev_auth=True, bootstrap_contact="", device_key="unbound",
    )))
    assert client.get(
        "/api/device/family-a/photos/deleted", headers={"X-Device-Key": "unbound"},
    ).status_code == 503


@pytest.mark.parametrize("raw", [
    "[]", "null", "not-json", '{"family-a":"bad"}',
    '{"family-a":42}', '{"family-a":{}}',
    '{"family-a":"' + "a" * 64 + '","family-a":"' + "b" * 64 + '"}',
    '{"family-a":"' + "a" * 64 + '","family-b":"' + "a" * 64 + '"}',
])
def test_invalid_device_bindings_are_rejected_without_echoing_them(monkeypatch, raw) -> None:
    monkeypatch.delenv("LANTERNINA_DEVICE_KEY", raising=False)
    monkeypatch.setenv("LANTERNINA_DEVICE_KEY_HASHES", raw)
    with pytest.raises(ValueError, match="^invalid device household bindings$"):
        Settings.from_env()


def test_device_key_rotation_and_revocation(monkeypatch) -> None:
    import hashlib
    import json
    from dataclasses import replace

    monkeypatch.delenv("LANTERNINA_DEVICE_KEY", raising=False)
    monkeypatch.setenv("LANTERNINA_DEVICE_KEY_HASHES", json.dumps({
        "family-a": hashlib.sha256(b"new-key").hexdigest(),
    }))
    app = create_app(settings=Settings.from_env())
    client = TestClient(app)
    url = "/api/device/family-a/photos/deleted"
    assert client.get(url, headers={"X-Device-Key": "old-key"}).status_code == 403
    assert client.get(url, headers={"X-Device-Key": "new-key"}).status_code == 200
    app.state.settings = replace(app.state.settings, device_key_hashes=())
    assert client.get(url, headers={"X-Device-Key": "new-key"}).status_code == 503


def test_device_binding_export_never_returns_the_raw_key(tmp_path) -> None:
    import hashlib
    import json

    from tools.device_bindings import bindings_from

    path = tmp_path / "config.yaml"
    key = "a" * 64
    path.write_text(f"household: family-a\ndevice_key: {key}\n", encoding="utf-8")
    previous = {"family-b": hashlib.sha256(b"other-key").hexdigest()}
    bindings = bindings_from(path, json.dumps(previous))
    assert bindings == {**previous, "family-a": hashlib.sha256(key.encode()).hexdigest()}
    assert key not in json.dumps(bindings)
    path.write_text("household: family-a\ndevice_key: short\n", encoding="utf-8")
    with pytest.raises(ValueError, match="^cannot produce device bindings"):
        bindings_from(path)


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


def test_every_method_the_api_serves_is_one_a_browser_may_send() -> None:
    """The CORS list against what the app actually exposes, rather than against a memory.

    `DELETE /api/trail` shipped on 5 September 2026 while the list said GET and POST. The
    route was right, the store was right, and the browser never sent the request at all: the
    preflight was refused, so the panel showed a failure that had never reached the API. A
    hand-written list beside a growing set of routes is the shape of that fault, and this is
    the check that makes it impossible to repeat.

    OPTIONS is excluded because it is the preflight itself, which the middleware answers.
    """
    from panel.app import BROWSER_METHODS

    client, _ = client_for()
    served = {
        method.upper()
        for path in client.app.openapi()["paths"].values()  # type: ignore[attr-defined]
        for method in path
    } - {"options"} - {"OPTIONS"}

    assert served <= set(BROWSER_METHODS), (
        f"the panel serves {sorted(served - set(BROWSER_METHODS))} and a browser may not send it"
    )


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
