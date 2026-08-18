"""Settings the panel reads from the environment.

Two of these decide whether the panel is safe, so both default to the closed position:
without ``LANTERNINA_DEV_AUTH`` nobody can be identified, and without
``LANTERNINA_BOOTSTRAP_CONTACT`` nobody is activated automatically.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from .usage import DEFAULT_MONTHLY_PICTURE_CAP


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
    # Browser origins allowed to call this API. Empty means none, which is why a front end
    # served from anywhere else has to be named here on purpose.
    allowed_origins: str = ""
    # Where proposals live. Empty keeps the in-memory store, which forgets on restart.
    cosmos_endpoint: str = ""
    cosmos_database: str = "lanternina"
    # Shared secret the server in the home presents. Empty closes the device routes.
    device_key: str = ""
    # Where shown pictures are archived. Empty keeps them in memory only.
    blob_endpoint: str = ""
    pictures_container: str = "pictures"
    # How many paid calls one household may make in a month. Zero removes the cap, which
    # has to be typed on purpose.
    monthly_picture_cap: int = DEFAULT_MONTHLY_PICTURE_CAP

    @property
    def blob_configured(self) -> bool:
        return bool(self.blob_endpoint and self.pictures_container)

    @property
    def cosmos_configured(self) -> bool:
        return bool(self.cosmos_endpoint and self.cosmos_database)

    @property
    def device_configured(self) -> bool:
        return bool(self.device_key)

    @property
    def oidc_configured(self) -> bool:
        return bool(self.oidc_authority and self.oidc_audience)

    @property
    def origins(self) -> tuple[str, ...]:
        return tuple(value.strip() for value in self.allowed_origins.split(",") if value.strip())

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            dev_auth=os.environ.get("LANTERNINA_DEV_AUTH", "") == "1",
            bootstrap_contact=os.environ.get("LANTERNINA_BOOTSTRAP_CONTACT", "")
            .strip()
            .casefold(),
            oidc_authority=os.environ.get("LANTERNINA_OIDC_AUTHORITY", "").strip(),
            oidc_audience=os.environ.get("LANTERNINA_OIDC_AUDIENCE", "").strip(),
            allowed_origins=os.environ.get("LANTERNINA_ALLOWED_ORIGINS", "").strip(),
            cosmos_endpoint=os.environ.get("LANTERNINA_COSMOS_ENDPOINT", "").strip(),
            cosmos_database=os.environ.get("LANTERNINA_COSMOS_DATABASE", "lanternina").strip(),
            device_key=os.environ.get("LANTERNINA_DEVICE_KEY", "").strip(),
            blob_endpoint=os.environ.get("LANTERNINA_BLOB_ENDPOINT", "").strip(),
            pictures_container=os.environ.get(
                "LANTERNINA_PICTURES_CONTAINER", "pictures"
            ).strip(),
            monthly_picture_cap=int(
                os.environ.get(
                    "LANTERNINA_MONTHLY_PICTURE_CAP", str(DEFAULT_MONTHLY_PICTURE_CAP)
                )
            ),
        )
