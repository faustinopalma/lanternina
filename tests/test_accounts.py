"""The account gate: signing in is not the same as being allowed.

The interesting test here is not that an active account passes. It is that everything
else fails, including a status nobody has invented yet.
"""

from __future__ import annotations

import dataclasses

import pytest

from panel.store import InMemoryAccountStore
from shared.accounts import Account, AccountStatus, AccountStore, require_active
from shared.errors import AccessDenied, AccountNotApproved, AccountNotFound


@pytest.fixture
def store() -> InMemoryAccountStore:
    return InMemoryAccountStore()


def test_the_store_satisfies_the_protocol(store: InMemoryAccountStore) -> None:
    assert isinstance(store, AccountStore)


def test_an_unknown_subject_is_refused_not_provisioned() -> None:
    with pytest.raises(AccountNotFound):
        require_active(None)


def test_signing_up_never_produces_an_active_account(store: InMemoryAccountStore) -> None:
    account = store.register(subject="sub-abc", contact="parent@example.test")
    assert account.status is AccountStatus.PENDING
    with pytest.raises(AccountNotApproved):
        require_active(account)


def test_signing_up_twice_does_not_reopen_a_decision(store: InMemoryAccountStore) -> None:
    first = store.register(subject="sub-abc", contact="parent@example.test")
    store.decide(first.id, AccountStatus.REJECTED, decided_by="admin")

    again = store.register(subject="sub-abc", contact="parent@example.test")

    assert again.id == first.id
    assert again.status is AccountStatus.REJECTED


def test_only_active_passes_the_gate(store: InMemoryAccountStore) -> None:
    account = store.register(subject="sub-abc", contact="parent@example.test")
    active = store.decide(account.id, AccountStatus.ACTIVE, decided_by="admin")

    assert require_active(active) is active


@pytest.mark.parametrize(
    "status", [s for s in AccountStatus if s is not AccountStatus.ACTIVE], ids=str
)
def test_every_status_that_is_not_active_is_denied(
    store: InMemoryAccountStore, status: AccountStatus
) -> None:
    """Parametrised over the enum rather than over a hand-written list.

    Add a member to AccountStatus and this test covers it automatically — so a new status
    has to be *deliberately* allowed, and cannot be allowed by forgetting.
    """
    account = store.register(subject="sub-abc", contact="parent@example.test")
    decided = store.decide(account.id, status, decided_by="admin")

    with pytest.raises(AccessDenied):
        require_active(decided)


def test_the_gate_is_not_written_as_a_blocklist() -> None:
    """The mutation check: a blocklist implementation must fail this.

    ``require_active`` is written as "must be ACTIVE". Rewriting it as "must not be
    PENDING or REJECTED or SUSPENDED" would pass every test above, and would silently
    admit the next status somebody adds. This simulates that future status.
    """
    imaginary_future_status = "trial"
    assert imaginary_future_status not in set(AccountStatus)

    account = Account(
        id="ac_test",  # type: ignore[arg-type]
        household_id="hh_test",  # type: ignore[arg-type]
        subject="sub-abc",
        contact="parent@example.test",
        status=imaginary_future_status,  # type: ignore[arg-type]
        created_at=0.0,
    )

    with pytest.raises(AccountNotApproved):
        require_active(account)


def test_a_decision_must_record_who_made_it(store: InMemoryAccountStore) -> None:
    account = store.register(subject="sub-abc", contact="parent@example.test")
    with pytest.raises(ValueError):
        store.decide(account.id, AccountStatus.ACTIVE, decided_by="")


def test_an_account_carries_nothing_about_the_learner() -> None:
    """The cloud stores households as opaque ids. See docs/ARCHITECTURE.md."""
    fields = {f.name for f in dataclasses.fields(Account)}
    forbidden = {"learner", "learner_id", "learner_name", "child", "child_name", "age",
                 "display_name", "interests", "difficulty", "diagnosis"}
    assert not (fields & forbidden), f"Account must not describe the learner: {fields & forbidden}"
