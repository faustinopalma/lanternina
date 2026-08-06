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

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            dev_auth=os.environ.get("LANTERNINA_DEV_AUTH", "") == "1",
            bootstrap_contact=os.environ.get("LANTERNINA_BOOTSTRAP_CONTACT", "")
            .strip()
            .casefold(),
        )
