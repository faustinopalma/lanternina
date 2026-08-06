"""From "who are you" to "you may proceed" — or not.

The whole path a request takes before any route sees it:

    identify -> look up -> record the sign-up as PENDING -> maybe bootstrap -> require ACTIVE

The bootstrap is a separate, recorded decision rather than a special case inside
``register``. That keeps the store's promise intact — signing up never produces an active
account — and leaves ``decided_by="bootstrap"`` in the record, so how the first account
got in is visible forever instead of being folded into a status field.
"""

from __future__ import annotations

from shared.accounts import Account, AccountStatus, AccountStore, require_active

from .config import Settings
from .principal import Principal

BOOTSTRAP_DECIDER = "bootstrap"


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
