"""Settings the panel reads from the environment.

Three of these decide whether the panel is safe, so all three default to the closed
position: without ``LANTERNINA_DEV_AUTH`` nobody can be identified, without
``LANTERNINA_BOOTSTRAP_CONTACT`` nobody is activated automatically, and without
``LANTERNINA_ADMIN_OIDC_AUTHORITY`` nobody can admit anyone.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from .usage import DEFAULT_MONTHLY_CALL_CAP


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
    # The administrator's identity provider, deliberately not the parents'. Empty closes
    # the administration routes: no environment variable, no administration.
    admin_oidc_authority: str = ""
    # Comma-separated, because Entra emits the bare application id for some configurations
    # and its api:// form for others, and both name the same application.
    admin_oidc_audience: str = ""
    # The app role an administrator's token must carry. The role is assigned in the
    # directory, so nothing the panel writes can grant it — which is the point of holding
    # this privilege outside the database the administrator edits.
    admin_role: str = "Lanternina.Admin"
    # Where proposals live. Empty keeps the in-memory store, which forgets on restart.
    cosmos_endpoint: str = ""
    cosmos_database: str = "lanternina"
    # Shared secret the server in the home presents. Empty closes the device routes.
    device_key: str = ""
    # Where shown pictures are archived. Empty keeps them in memory only.
    blob_endpoint: str = ""
    pictures_container: str = "pictures"
    # How many paid calls one household may make in a month, of any kind. Zero removes the
    # cap, which has to be typed on purpose.
    monthly_call_cap: int = DEFAULT_MONTHLY_CALL_CAP

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
    def admin_configured(self) -> bool:
        return bool(self.admin_oidc_authority and self.admin_oidc_audience and self.admin_role)

    @property
    def admin_audiences(self) -> tuple[str, ...]:
        return tuple(
            value.strip() for value in self.admin_oidc_audience.split(",") if value.strip()
        )

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
            admin_oidc_authority=os.environ.get(
                "LANTERNINA_ADMIN_OIDC_AUTHORITY", ""
            ).strip(),
            admin_oidc_audience=os.environ.get("LANTERNINA_ADMIN_OIDC_AUDIENCE", "").strip(),
            admin_role=os.environ.get("LANTERNINA_ADMIN_ROLE", "Lanternina.Admin").strip(),
            cosmos_endpoint=os.environ.get("LANTERNINA_COSMOS_ENDPOINT", "").strip(),
            cosmos_database=os.environ.get("LANTERNINA_COSMOS_DATABASE", "lanternina").strip(),
            device_key=os.environ.get("LANTERNINA_DEVICE_KEY", "").strip(),
            blob_endpoint=os.environ.get("LANTERNINA_BLOB_ENDPOINT", "").strip(),
            pictures_container=os.environ.get(
                "LANTERNINA_PICTURES_CONTAINER", "pictures"
            ).strip(),
            monthly_call_cap=int(
                os.environ.get(
                    "LANTERNINA_MONTHLY_CALL_CAP", str(DEFAULT_MONTHLY_CALL_CAP)
                )
            ),
        )
