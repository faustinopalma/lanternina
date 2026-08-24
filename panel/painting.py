"""Painting a picture because the server in the home asked for one.

Why here and not in the house: this container already holds a managed identity with
access to Foundry and to Content Safety, so nothing in the home needs a long-lived
credential of its own. The house still decides *when* — it calls this route on its own
schedule, and nothing here can call the house.

What painting here costs: the parent-approval seal cannot be minted, because its key lives
on the device and must stay there. The picture is screened, and its subject is a theme the
parent approved, but it carries no parent seal. That is the same weakening theme-level
approval already made, not a new one — and it is the reason this path is only ever used
for pictures, never for words.
"""

from __future__ import annotations

import os
import random
import secrets
from collections.abc import Callable

from shared.ids import new_id
from shared.manner import a_manner
from shared.routing import Capability, ModelRequest, ModelUsage
from shared.safety import ContentKind
from shared.seal import Sealer, SealPurpose

# Used only when the parent's list is empty, so a display asking for a picture always gets
# one. Going blank because nobody has typed a theme yet would be the wrong failure.
FALLBACK_THEMES = (
    "animali del bosco",
    "il sistema solare",
    "fiori di campo",
    "montagne e nuvole",
)

# Written for a screen with two levels and no backlight: fine detail and text both vanish
# once the picture is dithered, so neither is asked for.
#
# The manner is appended per call and never stored in this string. Without it the prompt was
# a pure function of the theme, so a household with three themes saw the same three pictures
# for as long as it kept them — noticed by the parent, 24 August 2026.
PICTURE_PROMPT = (
    "Black and white ink illustration of {theme}. Bold clean outlines, large simple "
    "shapes, strong contrast, generous white space, calm and friendly. "
    "No text, no letters, no numbers, no watermark, no border, no frame."
)


def choose_theme(labels: list[str]) -> str:
    return random.choice(labels or list(FALLBACK_THEMES))


def identity_claims() -> dict[str, str]:
    """Who this container is, according to the token it actually gets.

    Written after four role assignments failed to shift a 401: every hypothesis about
    *which* identity was calling had been a deduction, and this is the measurement.
    Returns identifying claims only — never the token.
    """
    import base64
    import json

    from azure.identity import DefaultAzureCredential

    token = DefaultAzureCredential().get_token(
        "https://cognitiveservices.azure.com/.default"
    ).token
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    claims = json.loads(base64.urlsafe_b64decode(payload))
    return {
        "oid": str(claims.get("oid", "")),
        "appid": str(claims.get("appid") or claims.get("azp") or ""),
        "aud": str(claims.get("aud", "")),
        "iss": str(claims.get("iss", "")),
        "tid": str(claims.get("tid", "")),
        "idtyp": str(claims.get("idtyp", "")),
    }


async def paint(
    theme: str,
    size: str = "1536x1024",
    *,
    on_usage: Callable[[ModelUsage | None], None] | None = None,
) -> tuple[str, str, ModelUsage | None]:
    """Generate one picture for ``theme``. Returns its id, the base64 PNG, and what the
    backend said the call consumed.

    Raises whatever the router raises when the cloud will not serve it, including
    :class:`~shared.errors.SafetyBlocked` when the gate refuses the result.
    """
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig

    environment = dict(os.environ)
    # The seal this gate mints is not used downstream on this path: the device renders
    # from the bytes we return, not from a sealed payload. A per-process key keeps the
    # gate honest about what it is without pretending the seal travels anywhere.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    drawn = a_manner()
    try:
        payload = await router.generate_for_user(
            ModelRequest(
                capability=Capability.IMAGE_GENERATION,
                prompt=f"{PICTURE_PROMPT.format(theme=theme)} {drawn.as_sentence()}",
                request_id=new_id("rq"),  # type: ignore[arg-type]
                purpose=f"picture/{theme}",
                content_kind=ContentKind.IMAGE_PNG,
                metadata={"size": size, "manner": drawn.to_dict()},
            )
        )
    finally:
        # Reported even when the gate refuses: that call was made and paid for anyway.
        if on_usage is not None:
            on_usage(router.last_usage)
        await gate.aclose()
    return new_id("pic"), payload.body, router.last_usage
