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
* **An app role can be required.** The administrator surface needs a privilege that our
  own database cannot grant, and ``roles`` is assigned in the directory. Optional, so the
  parent path is unchanged.
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
    # App roles the directory put in the token. Empty for a parent's token, which asks for
    # a scope and is granted no role at all.
    roles: tuple[str, ...] = ()


class _JwksKeys:
    def __init__(self, jwks_uri: str) -> None:
        self._client = PyJWKClient(jwks_uri)

    def key_for(self, token: str) -> Any:
        return self._client.get_signing_key_from_jwt(token).key


class TokenVerifier:
    """Validates tokens from one issuer, for one audience."""

    def __init__(
        self,
        *,
        issuer: str,
        audience: str | Sequence[str],
        keys: SigningKeys,
        required_role: str = "",
    ) -> None:
        self._issuer = issuer
        # A token matching any one of these is accepted. Entra emits the application id
        # for some configurations and its api:// form for others, and both name this same
        # application, so accepting both admits nothing a single value would exclude.
        self._audiences = [audience] if isinstance(audience, str) else list(audience)
        self._keys = keys
        self._required_role = required_role

    @classmethod
    def from_authority(
        cls,
        authority: str,
        audience: str | Sequence[str],
        required_role: str = "",
    ) -> TokenVerifier:
        """Read issuer and jwks_uri from the authority's discovery document."""
        url = authority.rstrip("/") + DISCOVERY_PATH
        try:
            document = httpx.get(url, timeout=10).raise_for_status().json()
            issuer = document["issuer"]
            jwks_uri = document["jwks_uri"]
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise AuthNotConfigured(f"could not read OIDC metadata from {url}: {exc}") from exc

        return cls(
            issuer=issuer,
            audience=audience,
            keys=_JwksKeys(jwks_uri),
            required_role=required_role,
        )

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

        raw_roles = payload.get("roles")
        roles = tuple(str(role) for role in raw_roles) if isinstance(raw_roles, list) else ()
        # Read before the check so a token with no roles claim at all is refused by the
        # same line as one carrying the wrong role, with the same message.
        if self._required_role and self._required_role not in roles:
            raise NotAuthenticated("token rejected")

        # The measured External ID token uses preferred_username; email remains first so
        # another configured user flow can provide the more specific claim.
        contact = str(payload.get("email") or payload.get("preferred_username") or "").strip()
        return Claims(subject=subject, contact=contact, roles=roles)
