"""Who may admit a parent, and where that privilege comes from.

The administrator is not a parent with a flag. They sign in against a different directory
— the workforce tenant that administers the subscription — and their privilege arrives in
the token as an app role. Three consequences, and each is the reason for a choice below:

* **The privilege does not live in the table it edits.** A fault in the write path that
  admits accounts cannot promote whoever exploits it, because being an administrator is
  not a row anybody here can write.
* **There is nothing to bootstrap.** ``panel/gate.py`` needs a configured address to let
  the first parent in; nothing equivalent is needed here, because the first administrator
  is made in the directory before this code ever runs.
* **The parent's token cannot reach these routes and this one cannot reach theirs.** The
  two are separate applications with separate audiences, so a token is refused by the
  audience check before any question of roles is asked.

There is no development bypass. ``LANTERNINA_DEV_AUTH`` opens the parent path on a plain
header; doing the same here would be a header that admits accounts. Unconfigured means
503, and the tests supply a verifier rather than a shortcut.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI, Request

from shared.accounts import Account, AccountStatus
from shared.errors import AuthNotConfigured

from .config import Settings
from .principal import bearer_token
from .tokens import TokenVerifier

# What an administrator may set. PENDING is absent because a decision is not undone, and
# SUSPENDED because nothing lists active accounts yet — offering it would be a state
# reachable only by typing an id by hand. TODO(poc): add it with the list that justifies it.
ADMISSIONS = (AccountStatus.ACTIVE, AccountStatus.REJECTED)


@dataclass(frozen=True, slots=True)
class Administrator:
    """The person deciding. Recorded on every decision, by subject rather than by address:
    an address can be changed in the directory, and a decision is not re-attributed when
    it is."""

    subject: str
    contact: str


def admin_verifier_for(app: FastAPI) -> TokenVerifier | None:
    """Built on first use, like the parent's. Returns None when nothing is configured, so
    the caller answers "not configured" rather than "not allowed"."""
    settings: Settings = app.state.settings
    if not settings.admin_configured:
        return None
    if app.state.admin_verifier is None:
        app.state.admin_verifier = TokenVerifier.from_authority(
            settings.admin_oidc_authority,
            settings.admin_audiences,
            settings.admin_role,
        )
    verifier: TokenVerifier = app.state.admin_verifier
    return verifier


def current_admin(request: Request) -> Administrator:
    """Module scope for the same reason as ``current_account``: with postponed
    annotations, FastAPI cannot resolve a dependency that only exists inside a closure."""
    verifier = admin_verifier_for(request.app)
    if verifier is None:
        raise AuthNotConfigured("no administrator identity provider is configured")

    claims = verifier.verify(bearer_token(request.headers))
    return Administrator(subject=claims.subject, contact=claims.contact)


CurrentAdmin = Annotated[Administrator, Depends(current_admin)]


def waiting_view(account: Account) -> dict[str, object]:
    """What an administrator is shown about a sign-up.

    The contact address and when it appeared: enough to judge whether a sign-up is
    legitimate, and nothing about a household or a person. The identity-provider subject
    stays out — it is how a token is matched, not something to put on a screen.
    """
    return {
        "id": str(account.id),
        "contact": account.contact,
        "status": str(account.status),
        "createdAt": account.created_at,
        "decidedAt": account.decided_at,
    }
