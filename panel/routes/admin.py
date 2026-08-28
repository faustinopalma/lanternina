"""The administration surface: who is waiting to be let in, the decision, and the one
permission that is not a parent's to give.

Deliberately not a search over every account — a route that answers questions about one
address is a way to find out who is registered. The keeping routes take a household id
rather than offering a list, for the same reason and with the same cost: an administrator
has to already know which household they are working on.
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from shared.accounts import AccountStatus, AccountStore
from shared.ids import AccountId

from ..admin import ADMISSIONS, CurrentAdmin, waiting_view
from ..keeping import KeepingStore, granted, withdrawn
from . import Decision

router = APIRouter()


@router.get("/api/admin/me")
def admin_me(admin: CurrentAdmin) -> dict[str, Any]:
    """Who the administration surface believes is calling.

    It exists so the page can tell "you hold no administrator role" apart from
    "nobody is waiting": both would otherwise be an empty list.
    """
    return {"subject": admin.subject, "contact": admin.contact}


@router.get("/api/admin/accounts")
def waiting_accounts(_: CurrentAdmin, request: Request) -> Any:
    """The sign-ups awaiting a decision, oldest first. Deliberately not a search over
    every account: a route that answers questions about one address is a way to find
    out who is registered."""
    store: AccountStore = request.app.state.store
    return {"accounts": [waiting_view(row) for row in store.pending()]}


@router.post("/api/admin/accounts/{account_id}/decision")
def admit_account(
    account_id: str, decision: Decision, admin: CurrentAdmin, request: Request
) -> Any:
    """Admit or refuse one sign-up. This is the whole effect: a status changes, and
    who changed it is recorded. Nothing is generated and nobody is notified."""
    if decision.state not in {status.value for status in ADMISSIONS}:
        raise HTTPException(status_code=400, detail="unsupported_state")
    store: AccountStore = request.app.state.store
    try:
        row = store.decide(
            AccountId(account_id),
            AccountStatus(decision.state),
            decided_by=admin.subject,
            note=decision.note,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="unknown_account") from exc
    return waiting_view(row)


class BeingWorkedOn(BaseModel):
    """Whether this household is one somebody is building against."""

    model_config = ConfigDict(extra="forbid")

    keeping: bool


@router.get("/api/admin/households/{household_id}/keeping")
def is_being_worked_on(household_id: str, _: CurrentAdmin, request: Request) -> Any:
    store: KeepingStore = request.app.state.keeping
    return store.get(household_id).to_public(time.time())


@router.post("/api/admin/households/{household_id}/keeping")
def work_on(
    household_id: str, what: BeingWorkedOn, admin: CurrentAdmin, request: Request
) -> Any:
    """Turn on, or renew, the one exception in `panel/keeping.py`.

    On is not a state that stays on. Every call sets a fresh instant a fortnight out, so a
    household is being worked on for as long as somebody keeps saying so and no longer.
    Turning it off stops what is kept from now; it does not delete what a standing
    permission already allowed, because those rows lapse on their own date and a route that
    erased a record would be a different and worse thing than one that stops adding to it.
    """
    store: KeepingStore = request.app.state.keeping
    now = time.time()
    make = granted if what.keeping else withdrawn
    return store.set(make(household_id, by=admin.subject, now=now)).to_public(now)
