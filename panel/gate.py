"""From "who are you" to "you may proceed" — or not.

The whole path a request takes before any route sees it:

    identify -> look up -> record the sign-up as PENDING -> maybe bootstrap -> require ACTIVE

The bootstrap is a separate, recorded decision rather than a special case inside
``register``. That keeps the store's promise intact — signing up never produces an active
account — and leaves ``decided_by="bootstrap"`` in the record, so how the first account
got in is visible forever instead of being folded into a status field.

Two kinds of caller reach this panel, and both are answered here: a parent, who arrives
with a token and has to be an active account, and the server in the home, which arrives
with a shared key and is not an account at all. ``panel/admin.py`` is the third and stays
separate on purpose — a different directory, a different audience.
"""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request

from shared.accounts import Account, AccountStatus, AccountStore, require_active

from .config import Settings
from .principal import Principal, principal_from_headers
from .tokens import TokenVerifier

BOOTSTRAP_DECIDER = "bootstrap"


def verifier_for(app: FastAPI) -> TokenVerifier | None:
    """Built on first use, so an identity provider that is unreachable at startup answers
    503 rather than stopping the container from starting at all."""
    settings: Settings = app.state.settings
    if not settings.oidc_configured:
        return None
    if app.state.verifier is None:
        app.state.verifier = TokenVerifier.from_authority(
            settings.oidc_authority, settings.oidc_audience
        )
    verifier: TokenVerifier = app.state.verifier
    return verifier


def current_account(request: Request) -> Account:
    """Module scope on purpose: `from __future__ import annotations` postpones the
    annotation, and FastAPI cannot resolve a name that only exists inside a closure."""
    settings: Settings = request.app.state.settings
    principal = principal_from_headers(request.headers, settings, verifier_for(request.app))
    return resolve_account(principal, request.app.state.store, settings)


CurrentAccount = Annotated[Account, Depends(current_account)]


def require_device(request: Request) -> str:
    """Identify the server in the home. Closed unless a key is configured."""
    settings: Settings = request.app.state.settings
    if not settings.device_configured:
        raise HTTPException(status_code=503, detail="device_not_configured")
    presented = request.headers.get("X-Device-Key", "")
    if not secrets.compare_digest(presented, settings.device_key):
        raise HTTPException(status_code=403, detail="not_authorised")
    return presented


DeviceKey = Annotated[str, Depends(require_device)]


def resolve_account(principal: Principal, store: AccountStore, settings: Settings) -> Account:
    """The gate. Raises :class:`~shared.errors.AccessDenied` unless the caller is active."""
    account = store.by_subject(principal.subject)
    if account is None:
        account = store.register(subject=principal.subject, contact=principal.contact)

    account = _maybe_bootstrap(account, store, settings)
    return require_active(account)


def _maybe_bootstrap(account: Account, store: AccountStore, settings: Settings) -> Account:
    """Activate the very first account, once, and never again.

    Guarded on ``has_active()`` rather than on a flag someone must remember to unset: once
    anyone is in, the configured address stops meaning anything, so leaving the variable
    behind after go-live is inert instead of dangerous.
    """
    if not settings.bootstrap_contact:
        return account
    if account.status is not AccountStatus.PENDING:
        return account
    if account.contact.strip().casefold() != settings.bootstrap_contact:
        return account
    if store.has_active():
        return account

    return store.decide(
        account.id,
        AccountStatus.ACTIVE,
        decided_by=BOOTSTRAP_DECIDER,
        note="first account, activated by configuration",
    )
