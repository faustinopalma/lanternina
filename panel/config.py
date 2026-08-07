"""Settings the panel reads from the environment.

Two of these decide whether the panel is safe, so both default to the closed position:
without ``LANTERNINA_DEV_AUTH`` nobody can be identified, and without
``LANTERNINA_BOOTSTRAP_CONTACT`` nobody is activated automatically.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    # Accepts the caller's identity from plain request headers. Development only.
    dev_auth: bool
    # The one address allowed to self-activate, and only while no account is active yet.
    bootstrap_contact: str
    # Base URL of the identity provider. Its discovery document supplies issuer and keys.
    oidc_authority: str = ""
    # Our own application id. Without it, a token minted for any other application in the
    # same directory would be accepted.
    oidc_audience: str = ""

    @property
    def oidc_configured(self) -> bool:
        return bool(self.oidc_authority and self.oidc_audience)

    @property
    def oidc_audiences(self) -> tuple[str, ...]:
        """Comma separated, because which form Entra emits has not been measured."""
        return tuple(value.strip() for value in self.oidc_audience.split(",") if value.strip())

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            dev_auth=os.environ.get("LANTERNINA_DEV_AUTH", "") == "1",
            bootstrap_contact=os.environ.get("LANTERNINA_BOOTSTRAP_CONTACT", "")
            .strip()
            .casefold(),
            oidc_authority=os.environ.get("LANTERNINA_OIDC_AUTHORITY", "").strip(),
            oidc_audience=os.environ.get("LANTERNINA_OIDC_AUDIENCE", "").strip(),
        )
