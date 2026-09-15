"""Settings the panel reads from the environment.

Three of these decide whether the panel is safe, so all three default to the closed
position: without ``LANTERNINA_DEV_AUTH`` nobody can be identified, without
``LANTERNINA_BOOTSTRAP_CONTACT`` nobody is activated automatically, and without
``LANTERNINA_ADMIN_OIDC_AUTHORITY`` nobody can admit anyone.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field

from .usage import DEFAULT_MONTHLY_LIMIT


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
    device_key: str = field(default="", repr=False)
    device_household: str = ""
    device_key_hashes: tuple[tuple[str, str], ...] = ()
    # Where shown pictures are archived. Empty keeps them in memory only.
    blob_endpoint: str = ""
    pictures_container: str = "pictures"
    # Sheets drawn for the printer. Its own container because it is its own kind of thing:
    # a picture is chosen for a display and a page is offered to paper, and on 6 September
    # 2026 they shared one archive, so the parent's wall of pictures had two lined sheets in
    # the middle of it.
    pages_container: str = "pages"
    # How many paid calls one household may make in a month, of any kind, unless the parent
    # has set their own. Zero removes the limit, which has to be typed on purpose.
    monthly_limit: int = DEFAULT_MONTHLY_LIMIT

    def __post_init__(self) -> None:
        bindings = list(self.device_key_hashes)
        if self.device_key and self.device_household:
            digest = hashlib.sha256(self.device_key.encode()).hexdigest()
            bindings.append((self.device_household, digest))
        if any(
            not isinstance(household, str) or not household or household != household.strip()
            or "/" in household or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            for household, digest in bindings
        ) or len({household for household, _ in bindings}) != len(bindings) or len(
            {digest for _, digest in bindings}
        ) != len(bindings):
            raise ValueError("invalid device household bindings")

    @property
    def bound_device_keys(self) -> dict[str, str]:
        bindings = dict(self.device_key_hashes)
        if self.device_key and self.device_household:
            bindings[self.device_household] = hashlib.sha256(self.device_key.encode()).hexdigest()
        return bindings

    @property
    def blob_configured(self) -> bool:
        return bool(self.blob_endpoint and self.pictures_container)

    @property
    def cosmos_configured(self) -> bool:
        return bool(self.cosmos_endpoint and self.cosmos_database)

    @property
    def device_configured(self) -> bool:
        return bool(self.bound_device_keys)

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
            device_household=os.environ.get("LANTERNINA_DEVICE_HOUSEHOLD", "").strip(),
            device_key_hashes=_device_key_hashes(
                os.environ.get("LANTERNINA_DEVICE_KEY_HASHES", "{}")
            ),
            blob_endpoint=os.environ.get("LANTERNINA_BLOB_ENDPOINT", "").strip(),
            pictures_container=os.environ.get(
                "LANTERNINA_PICTURES_CONTAINER", "pictures"
            ).strip(),
            pages_container=os.environ.get("LANTERNINA_PAGES_CONTAINER", "pages").strip(),
            monthly_limit=int(
                os.environ.get("LANTERNINA_MONTHLY_LIMIT", str(DEFAULT_MONTHLY_LIMIT))
            ),
        )


def _device_key_hashes(raw: str) -> tuple[tuple[str, str], ...]:
    try:
        if not raw.lstrip().startswith("{"):
            raise ValueError
        pairs = json.loads(raw, object_pairs_hook=lambda entries: entries)
        if not isinstance(pairs, list) or any(
            not isinstance(value, str) for _, value in pairs
        ):
            raise ValueError
        return tuple(pairs)
    except (ValueError, TypeError):
        raise ValueError("invalid device household bindings") from None
