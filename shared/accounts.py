"""Accounts, and the gate that decides whether one may do anything.

Signing in proves who you are. It does not get you an account. A parent who completes
sign-up lands in :attr:`AccountStatus.PENDING`, where every request is refused until an
administrator activates them.

Two reasons this exists, and they are worth keeping distinct:

1. **Keeping strangers out.** The panel is reachable from the internet, so identity alone
   cannot be the authorisation.
2. **Keeping the bill down.** Generating content calls paid models. A pending account
   generates nothing, so it costs nothing. The gate is therefore also the cost control.

Deliberately kept in the application rather than in the identity provider. Entra External
ID can block a sign-up synchronously, but it cannot hold one open for a human to decide
later — and directory contents do not survive the tenant move this project already
expects. See docs/DEPLOY.md §6.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from .errors import AccountNotApproved, AccountNotFound
from .ids import AccountId, HouseholdId


class AccountStatus(StrEnum):
    PENDING = "pending"  # signed up, waiting for a human
    ACTIVE = "active"  # the only status that may do anything
    REJECTED = "rejected"  # refused; keeps the record so the same subject cannot retry
    SUSPENDED = "suspended"  # was active, revoked


@dataclass(frozen=True, slots=True)
class Account:
    """A parent's account.

    Holds the parent's own contact address, because an administrator deciding whether a
    sign-up is legitimate needs something to look at. It holds **nothing about the
    learner** — not a name, not an age, not a profile. The household is an opaque id
    here; only the device in the home knows who is behind it.
    """

    id: AccountId
    household_id: HouseholdId
    # The 'sub' claim from the identity provider. Opaque, stable, and the only thing a
    # token can be matched on.
    subject: str
    # The parent's email as presented at sign-up. Shown to the administrator, never sent
    # to a model.
    contact: str
    status: AccountStatus
    created_at: float
    decided_at: float | None = None
    decided_by: str = ""
    note: str = ""


def require_active(account: Account | None) -> Account:
    """Return the account, or refuse.

    Written as "must be ACTIVE" rather than "must not be one of the blocked statuses" on
    purpose: a status added to :class:`AccountStatus` in a year's time is then denied by
    default instead of quietly granted. ``tests/test_accounts.py`` fails if this is
    inverted.
    """
    if account is None:
        raise AccountNotFound("no account for this subject")
    if account.status is not AccountStatus.ACTIVE:
        raise AccountNotApproved(f"account is {account.status}")
    return account


@runtime_checkable
class AccountStore(Protocol):
    """Where accounts live. The API reads; only an administrator path writes decisions."""

    def by_subject(self, subject: str) -> Account | None:
        """The account for an identity-provider subject, or None if never seen."""
        ...

    def register(self, *, subject: str, contact: str) -> Account:
        """Record a new sign-up as PENDING. Idempotent on subject.

        Never returns an ACTIVE account: there is no path from signing in to being
        allowed that does not pass through a human.
        """
        ...

    def pending(self) -> list[Account]:
        """Accounts awaiting a decision, oldest first."""
        ...

    def has_active(self) -> bool:
        """Whether any account has been activated. Gates the one-shot bootstrap."""
        ...

    def decide(
        self,
        account_id: AccountId,
        status: AccountStatus,
        *,
        decided_by: str,
        note: str = "",
    ) -> Account:
        """Record an administrator's decision."""
        ...
