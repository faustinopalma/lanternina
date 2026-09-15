"""Parent invitations and invitation-bound adolescent access."""

from __future__ import annotations

import hashlib
import secrets
import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field

from panel.gate import CurrentAccount, verifier_for
from panel.principal import Principal, principal_from_headers
from shared.accounts import AccountStatus

router = APIRouter()


def identity(request: Request) -> Principal:
    return principal_from_headers(
        request.headers, request.app.state.settings, verifier_for(request.app)
    )


Identity = Annotated[Principal, Depends(identity)]


def active_member(request: Request, principal: Identity) -> dict[str, Any]:
    member = request.app.state.portal.read()["members"].get(principal.subject)
    if member and member["active"]:
        parent = request.app.state.store.by_subject(member["parent"])
        if parent and parent.status == AccountStatus.ACTIVE:
            return member
    raise HTTPException(403, "portal_access_required")


Member = Annotated[dict[str, Any], Depends(active_member)]


class InviteBody(BaseModel):
    email: str = Field(min_length=3, max_length=254, pattern=r"^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$")


class AcceptBody(BaseModel):
    token: str = Field(min_length=40, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")


@router.get("/api/adolescents")
def family(account: CurrentAccount, request: Request) -> dict:
    data = request.app.state.portal.read()
    household = str(account.household_id)
    now = time.time()
    return {
        "members": [
            {key: row[key] for key in ("id", "email", "active", "joinedAt")}
            for row in data["members"].values() if row["household"] == household
        ],
        "invitations": [
            {**{key: row[key] for key in ("id", "email", "expiresAt", "status")},
             "status": "expired" if row["status"] in {"ready", "sent"} and row["expiresAt"] < now
             else row["status"]}
            for row in data["invitations"].values() if row["household"] == household
        ],
    }


@router.post("/api/adolescents/invitations", status_code=201)
def invite(body: InviteBody, account: CurrentAccount, request: Request, response: Response) -> dict:
    response.headers["Cache-Control"] = "no-store"
    email = body.email.strip().casefold()
    if email == account.contact.strip().casefold():
        raise HTTPException(409, "parent_email")
    token = secrets.token_urlsafe(32)
    digest = hashlib.sha256(token.encode()).hexdigest()
    now = time.time()
    row = {
        "id": secrets.token_hex(16), "email": email, "household": str(account.household_id),
        "parent": account.subject, "createdAt": now, "expiresAt": now + 72 * 3600,
        "status": "ready",
    }

    def reserve(data: dict) -> None:
        invitations = data["invitations"]
        recent = [item for item in invitations.values()
                  if item["household"] == row["household"] and item["createdAt"] > now - 86400]
        if len(recent) >= 10:
            raise HTTPException(429, "invitation_limit")
        for other in invitations.values():
            if other["household"] == row["household"] and other["email"] == email and (
                other["status"] in {"ready", "sent", "sending"}
            ):
                other["status"] = "revoked"
        invitations[digest] = row

    request.app.state.portal.change(reserve)
    return {"id": row["id"], "expiresAt": row["expiresAt"], "status": "ready", "code": token}


@router.post("/api/portal/accept")
def accept(body: AcceptBody, principal: Identity, request: Request) -> dict:
    digest = hashlib.sha256(body.token.encode()).hexdigest()
    if request.app.state.store.by_subject(principal.subject) is not None:
        raise HTTPException(409, "parent_account")
    now = time.time()
    subject_key = hashlib.sha256(principal.subject.encode()).hexdigest()

    def reserve_attempt(data: dict) -> bool:
        attempts = {key: row for key, row in data.get("redemptions", {}).items()
                    if row["since"] > now - 900}
        data["redemptions"] = attempts
        row = attempts.get(subject_key)
        if row is None:
            if len(attempts) >= 10000:
                return False
            row = attempts[subject_key] = {"since": now, "count": 0}
        if row["count"] >= 20:
            return False
        row["count"] += 1
        return True

    if not request.app.state.portal.change(reserve_attempt):
        raise HTTPException(429, "redemption_limit", headers={"Retry-After": "900"})

    def consume(data: dict) -> dict:
        row = data["invitations"].get(digest)
        if row and row["status"] == "accepted" and row.get("subject") == principal.subject:
            member = data["members"].get(principal.subject)
            if member and member["active"]:
                return {"joined": True}
        if not row or row["status"] not in {"ready", "sent"} or row["expiresAt"] <= time.time():
            raise HTTPException(410, "invitation_unavailable")
        if principal.contact.strip().casefold() != row["email"]:
            raise HTTPException(403, "invitation_email_mismatch")
        parent = request.app.state.store.by_subject(row["parent"])
        if not parent or parent.status != AccountStatus.ACTIVE:
            raise HTTPException(403, "portal_access_required")
        previous = data["members"].get(principal.subject)
        if previous and previous["household"] != row["household"]:
            raise HTTPException(409, "already_joined")
        data["members"][principal.subject] = {
            "id": previous["id"] if previous else secrets.token_hex(16),
            "email": row["email"], "household": row["household"], "parent": row["parent"],
            "joinedAt": time.time(), "active": True,
        }
        row.update(status="accepted", subject=principal.subject)
        return {"joined": True}

    return request.app.state.portal.change(consume)


@router.get("/api/portal/me")
def me(member: Member) -> dict:
    return {"id": member["id"], "email": member["email"]}


@router.delete("/api/adolescents/{record_id}")
def revoke(record_id: str, account: CurrentAccount, request: Request) -> dict:
    def remove(data: dict) -> None:
        household = str(account.household_id)
        for row in data["invitations"].values():
            if row["id"] == record_id and row["household"] == household:
                if row["status"] != "accepted":
                    row["status"] = "revoked"
                return
        for row in data["members"].values():
            if row["id"] == record_id and row["household"] == household:
                row["active"] = False
                for invitation in data["invitations"].values():
                    if invitation["household"] == household and invitation["email"] == row["email"]:
                        invitation["status"] = "revoked"
                return
        raise HTTPException(404, "unknown_access")

    request.app.state.portal.change(remove)
    return {"revoked": True}