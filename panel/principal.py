"""Who is calling.

Establishing identity is not the same as granting access — that is :mod:`panel.gate`.
This module only answers "which identity-provider subject is on the other end", and
refuses to answer at all when it has no trustworthy way to tell.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from shared.errors import AuthNotConfigured

from .config import Settings

DEV_SUBJECT_HEADER = "x-dev-subject"
DEV_CONTACT_HEADER = "x-dev-contact"


@dataclass(frozen=True, slots=True)
class Principal:
    """An authenticated caller, before any question of permission."""

    subject: str
    contact: str


def principal_from_headers(headers: Mapping[str, str], settings: Settings) -> Principal:
    """Identify the caller, or refuse.

    TODO(poc): validate a real Entra External ID token and take the subject from the
    ``sub`` claim. Until that exists this raises rather than inventing a caller, because
    a panel that trusts a header it received over the internet is worse than one that
    serves nobody.
    """
    if not settings.dev_auth:
        raise AuthNotConfigured("no token validation is wired, and dev auth is off")

    subject = headers.get(DEV_SUBJECT_HEADER, "").strip()
    if not subject:
        raise AuthNotConfigured(f"dev auth is on but {DEV_SUBJECT_HEADER} is missing")

    return Principal(subject=subject, contact=headers.get(DEV_CONTACT_HEADER, "").strip())
