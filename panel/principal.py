"""Who is calling.

Establishing identity is not the same as granting access — that is :mod:`panel.gate`.
This module only answers "which identity-provider subject is on the other end", and
refuses to answer at all when it has no trustworthy way to tell.

Two ways in, and the token always wins: switching dev auth on by accident where a real
identity provider is configured must not downgrade it to header trust.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from shared.errors import AuthNotConfigured, NotAuthenticated

from .config import Settings
from .tokens import TokenVerifier

DEV_SUBJECT_HEADER = "x-dev-subject"
DEV_CONTACT_HEADER = "x-dev-contact"
BEARER_PREFIX = "bearer "


@dataclass(frozen=True, slots=True)
class Principal:
    """An authenticated caller, before any question of permission."""

    subject: str
    contact: str


def principal_from_headers(
    headers: Mapping[str, str],
    settings: Settings,
    verifier: TokenVerifier | None = None,
) -> Principal:
    """Identify the caller, or refuse."""
    if verifier is not None:
        claims = verifier.verify(_bearer_token(headers))
        return Principal(subject=claims.subject, contact=claims.contact)

    if not settings.dev_auth:
        raise AuthNotConfigured("no identity provider is configured, and dev auth is off")

    subject = headers.get(DEV_SUBJECT_HEADER, "").strip()
    if not subject:
        raise AuthNotConfigured(f"dev auth is on but {DEV_SUBJECT_HEADER} is missing")

    return Principal(subject=subject, contact=headers.get(DEV_CONTACT_HEADER, "").strip())


def _bearer_token(headers: Mapping[str, str]) -> str:
    authorization = headers.get("authorization", "")
    if not authorization.lower().startswith(BEARER_PREFIX):
        raise NotAuthenticated("no bearer token")

    token = authorization[len(BEARER_PREFIX) :].strip()
    if not token:
        raise NotAuthenticated("no bearer token")
    return token
