"""Seals — the mechanism that makes the safety and approval chokepoints enforceable.

Python cannot make a constructor genuinely private, so "only the safety gate may create
screened content" cannot be enforced by visibility alone. Instead each chokepoint holds a
device-local HMAC key and *signs* what it emits. The delivery boundary
(:mod:`shared.delivery`) verifies both signatures before anything reaches the learner.

An agent can therefore construct a :class:`~shared.safety.ScreenedPayload` object, but it
cannot produce a payload that survives delivery, because it does not hold the keys. The
guarantee is: **content that was not screened, or not approved, cannot be delivered** —
not "developers remember to call the gate".

Keys live only on the mini-PC (see ``.env.example``); they are never sent anywhere.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

from .errors import SealVerificationError

SEAL_VERSION: Final = 1


class SealPurpose(StrEnum):
    """What a seal attests. A seal is only valid for the purpose it was issued for."""

    CONTENT_SAFETY = "content-safety"
    PARENT_APPROVAL = "parent-approval"


def digest_payload(payload: Any) -> str:
    """Return a stable SHA-256 hex digest of any JSON-serialisable payload.

    Sorted keys and a compact separator make the digest independent of dict ordering, so
    the same logical content always digests identically.
    """
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Seal:
    """An HMAC attestation issued by one of the two chokepoints."""

    purpose: SealPurpose
    digest: str
    signature: str
    issued_at: float
    issuer: str
    version: int = SEAL_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "purpose": str(self.purpose),
            "digest": self.digest,
            "signature": self.signature,
            "issued_at": self.issued_at,
            "issuer": self.issuer,
            "version": self.version,
        }


class Sealer:
    """Issues seals for one purpose. Held only by the layer that owns that purpose.

    The safety gate holds the ``CONTENT_SAFETY`` sealer; the approval ledger holds the
    ``PARENT_APPROVAL`` sealer. Nothing else should ever be handed one.
    """

    __slots__ = ("_purpose", "_key", "_issuer")

    def __init__(self, purpose: SealPurpose, key: bytes, issuer: str) -> None:
        if not key:
            raise ValueError(f"refusing to create a {purpose} sealer with an empty key")
        self._purpose = purpose
        self._key = key
        self._issuer = issuer

    @property
    def purpose(self) -> SealPurpose:
        return self._purpose

    def seal(self, payload: Any) -> Seal:
        digest = digest_payload(payload)
        issued_at = time.time()
        signature = _sign(self._key, self._purpose, digest, issued_at, self._issuer)
        return Seal(
            purpose=self._purpose,
            digest=digest,
            signature=signature,
            issued_at=issued_at,
            issuer=self._issuer,
        )


def verify_seal(seal: Seal, payload: Any, key: bytes, expected_purpose: SealPurpose) -> None:
    """Raise :class:`SealVerificationError` unless ``seal`` genuinely covers ``payload``."""
    if seal.version != SEAL_VERSION:
        raise SealVerificationError(f"unsupported seal version {seal.version}")
    if seal.purpose != expected_purpose:
        raise SealVerificationError(
            f"seal purpose {seal.purpose!r} does not match expected {expected_purpose!r}"
        )
    actual = digest_payload(payload)
    if not hmac.compare_digest(actual, seal.digest):
        raise SealVerificationError("payload does not match the sealed digest (content altered)")
    expected_sig = _sign(key, seal.purpose, seal.digest, seal.issued_at, seal.issuer)
    if not hmac.compare_digest(expected_sig, seal.signature):
        raise SealVerificationError(f"invalid {seal.purpose} signature from issuer {seal.issuer!r}")


def _sign(key: bytes, purpose: SealPurpose, digest: str, issued_at: float, issuer: str) -> str:
    # utf-8 named as in digest_payload: issuer is free text, so the bytes decide the signature.
    message = f"{SEAL_VERSION}|{purpose}|{digest}|{issued_at!r}|{issuer}"
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()
