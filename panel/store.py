"""An in-memory :class:`~shared.accounts.AccountStore`.

Real enough to run the API and the tests against, and obviously not a database. The
Cosmos-backed implementation is the next step; it is not written yet, so nothing here
pretends to persist.

TODO(poc): replace with a Cosmos-backed store partitioned on householdId. Until then a
restart forgets every decision, which is safe — it forgets them as PENDING, not ACTIVE.
"""

from __future__ import annotations

import threading
import time

from shared.accounts import Account, AccountStatus, AccountStore
from shared.ids import AccountId, new_account_id, new_household_id


class InMemoryAccountStore:
    """Conforms to :class:`~shared.accounts.AccountStore`."""

    def __init__(self) -> None:
        self._by_id: dict[AccountId, Account] = {}
        self._subject_index: dict[str, AccountId] = {}
        self._lock = threading.Lock()

    def by_subject(self, subject: str) -> Account | None:
        with self._lock:
            account_id = self._subject_index.get(subject)
            return self._by_id.get(account_id) if account_id else None

    def register(self, *, subject: str, contact: str) -> Account:
        with self._lock:
            existing_id = self._subject_index.get(subject)
            if existing_id is not None:
                # Idempotent, and deliberately does not reset a decision already taken:
                # signing in again must not turn a REJECTED account back into PENDING.
                return self._by_id[existing_id]

            account = Account(
                id=new_account_id(),
                household_id=new_household_id(),
                subject=subject,
                contact=contact,
                status=AccountStatus.PENDING,
                created_at=time.time(),
            )
            self._by_id[account.id] = account
            self._subject_index[subject] = account.id
            return account

    def pending(self) -> list[Account]:
        with self._lock:
            waiting = [a for a in self._by_id.values() if a.status is AccountStatus.PENDING]
        return sorted(waiting, key=lambda a: a.created_at)

    def has_active(self) -> bool:
        with self._lock:
            return any(a.status is AccountStatus.ACTIVE for a in self._by_id.values())

    def decide(
        self,
        account_id: AccountId,
        status: AccountStatus,
        *,
        decided_by: str,
        note: str = "",
    ) -> Account:
        if not decided_by:
            raise ValueError("a decision must record who made it")
        with self._lock:
            current = self._by_id.get(account_id)
            if current is None:
                raise KeyError(account_id)
            decided = Account(
                id=current.id,
                household_id=current.household_id,
                subject=current.subject,
                contact=current.contact,
                status=status,
                created_at=current.created_at,
                decided_at=time.time(),
                decided_by=decided_by,
                note=note,
            )
            self._by_id[account_id] = decided
            return decided


_ = AccountStore  # imported so a drift between protocol and implementation is visible here
