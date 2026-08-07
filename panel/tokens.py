"""Turning a bearer token into a subject we can trust.

The parts that matter are the ones easy to get subtly wrong:

* **The algorithm is pinned to RS256.** Passing the algorithms the token itself asks for
  is the algorithm-confusion attack: an attacker flips ``alg`` to ``HS256`` and signs with
  the public key, which is public. ``none`` is refused for the same family of reasons.
* **Issuer and JWKS come from the discovery document**, not from a URL template. Entra's
  CIAM issuer format is not something to hardcode from memory, and a wrong guess fails
  closed but for a confusing reason.
* **Audience is checked.** Without it, a token minted for any other application in the
  same directory would be accepted here.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

import httpx
import jwt
from jwt import PyJWKClient

from shared.errors import AuthNotConfigured, NotAuthenticated

SIGNING_ALGORITHM = "RS256"
DISCOVERY_PATH = "/.well-known/openid-configuration"


class SigningKeys(Protocol):
    """Supplies the public key a token claims to be signed with."""

    def key_for(self, token: str) -> Any: ...


@dataclass(frozen=True, slots=True)
class Claims:
    subject: str
    contact: str


class _JwksKeys:
    def __init__(self, jwks_uri: str) -> None:
        self._client = PyJWKClient(jwks_uri)

    def key_for(self, token: str) -> Any:
        return self._client.get_signing_key_from_jwt(token).key


class TokenVerifier:
    """Validates tokens from one issuer, for one audience."""

    def __init__(
        self, *, issuer: str, audience: str | Sequence[str], keys: SigningKeys
    ) -> None:
        self._issuer = issuer
        # A token matching any one of these is accepted. Entra emits the application id
        # for some configurations and its api:// form for others, and both name this same
        # application, so accepting both admits nothing a single value would exclude.
        self._audiences = [audience] if isinstance(audience, str) else list(audience)
        self._keys = keys

    @classmethod
    def from_authority(cls, authority: str, audience: str | Sequence[str]) -> TokenVerifier:
        """Read issuer and jwks_uri from the authority's discovery document."""
        url = authority.rstrip("/") + DISCOVERY_PATH
        try:
            document = httpx.get(url, timeout=10).raise_for_status().json()
            issuer = document["issuer"]
            jwks_uri = document["jwks_uri"]
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise AuthNotConfigured(f"could not read OIDC metadata from {url}: {exc}") from exc

        return cls(issuer=issuer, audience=audience, keys=_JwksKeys(jwks_uri))

    def verify(self, token: str) -> Claims:
        try:
            key = self._keys.key_for(token)
            payload = jwt.decode(
                token,
                key,
                algorithms=[SIGNING_ALGORITHM],
                audience=self._audiences,
                issuer=self._issuer,
                options={"require": ["exp", "iat", "iss", "aud", "sub"]},
            )
        except jwt.PyJWTError as exc:
            # One message for every reason, so a caller cannot probe which check failed.
            raise NotAuthenticated("token rejected") from exc

        subject = str(payload.get("sub", "")).strip()
        if not subject:
            raise NotAuthenticated("token rejected")

        # TODO(poc): confirm which claim the user flow actually emits; if neither is
        # present the account is still created, just without an address to show the
        # administrator.
        contact = str(payload.get("email") or payload.get("preferred_username") or "").strip()
        return Claims(subject=subject, contact=contact)
