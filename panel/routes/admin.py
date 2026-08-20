"""The administration surface: who is waiting to be let in, and the decision.

Three routes and nothing else. Deliberately not a search over every account — a route that
answers questions about one address is a way to find out who is registered.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request

from shared.accounts import AccountStatus, AccountStore
from shared.ids import AccountId

from ..admin import ADMISSIONS, CurrentAdmin, waiting_view
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
