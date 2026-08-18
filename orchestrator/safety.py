"""The content-safety gate: the single door model output passes before it is proposed.

This module and ``orchestrator/router.py`` are the only two places permitted to import a
cloud SDK, and only the router calls this gate. Agents never see unscreened text, so an
agent cannot route around screening even by mistake.

The gate holds the ``CONTENT_SAFETY`` sealer. That is what makes the rule enforceable
rather than customary: anyone can construct a :class:`~shared.safety.ScreenedPayload`,
but only this module can produce one whose seal survives ``assert_deliverable``.

TODO(poc): :class:`~shared.safety.SafetyCategory` also declares AGE_INAPPROPRIATE,
FRIGHTENING and OFF_TASK. Azure Content Safety has no detector for those, so they are
absent from the record rather than reported as zero — an unmeasured category must not
look like a measured-and-clean one.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Final, Protocol

from shared.errors import CloudUnavailable, SafetyBlocked
from shared.safety import (
    ContentKind,
    SafetyCategory,
    SafetyVerdict,
    ScreenedPayload,
    ScreeningRecord,
)
from shared.seal import Sealer, SealPurpose

POLICY_VERSION: Final = "1"
SCREENER_NAME: Final = "azure-content-safety"

# The four categories the service returns, mapped onto our vocabulary.
_AZURE_CATEGORIES: Final = {
    "Hate": SafetyCategory.HATE,
    "SelfHarm": SafetyCategory.SELF_HARM,
    "Sexual": SafetyCategory.SEXUAL,
    "Violence": SafetyCategory.VIOLENCE,
}


class SeverityAnalyzer(Protocol):
    """Whatever can score a piece of text. Injected so the gate is testable offline."""

    async def __call__(self, text: str) -> dict[SafetyCategory, int]: ...


class ImageAnalyzer(Protocol):
    """The same, for a base64 PNG."""

    async def __call__(self, image_b64: str) -> dict[SafetyCategory, int]: ...


def _severities(result: Any) -> dict[SafetyCategory, int]:
    severities: dict[SafetyCategory, int] = {}
    for entry in result.categories_analysis:
        category = _AZURE_CATEGORIES.get(str(entry.category))
        if category is not None:
            severities[category] = int(entry.severity or 0)
    return severities


@dataclass(frozen=True, slots=True)
class ContentSafetyConfig:
    endpoint: str
    # Azure's FourSeverityLevels scale reports 0, 2, 4 or 6. Two is the first non-zero
    # step, so this refuses anything the detector flags at all. It buys a wide margin for
    # an audience of one adolescent, and it costs occasional false refusals — which are
    # cheap here, because a refused generation is simply not proposed.
    block_at_severity: int = 2

    @staticmethod
    def from_env(env: dict[str, str]) -> ContentSafetyConfig:
        endpoint = env.get("LANTERNINA_CONTENT_SAFETY_ENDPOINT", "")
        if not endpoint:
            raise ValueError("missing configuration: LANTERNINA_CONTENT_SAFETY_ENDPOINT")
        return ContentSafetyConfig(
            endpoint=endpoint,
            block_at_severity=int(env.get("LANTERNINA_SAFETY_BLOCK_AT", "2")),
        )


class _AzureAnalyzer:
    """Everything that touches the Content Safety SDK, in one narrow place."""

    def __init__(self, endpoint: str, credential: Any | None) -> None:
        self._endpoint = endpoint
        self._credential = credential
        self._own_credential: Any | None = None
        self._client: Any | None = None

    def _client_or_build(self) -> Any:
        if self._client is None:
            from azure.ai.contentsafety.aio import ContentSafetyClient
            from azure.identity.aio import DefaultAzureCredential

            if self._credential is None:
                self._own_credential = DefaultAzureCredential()
            self._client = ContentSafetyClient(
                endpoint=self._endpoint,
                credential=self._credential or self._own_credential,
            )
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None
        if self._own_credential is not None:
            await self._own_credential.close()
            self._own_credential = None

    async def __call__(self, text: str) -> dict[SafetyCategory, int]:
        from azure.ai.contentsafety.models import AnalyzeTextOptions

        try:
            result = await self._client_or_build().analyze_text(AnalyzeTextOptions(text=text))
        except Exception as exc:  # the SDK raises many unrelated types
            raise CloudUnavailable(
                f"content safety unreachable: {type(exc).__name__}: {exc}"
            ) from exc
        return _severities(result)

    async def image(self, image_b64: str) -> dict[SafetyCategory, int]:
        from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData

        try:
            result = await self._client_or_build().analyze_image(
                AnalyzeImageOptions(image=ImageData(content=image_b64))
            )
        except Exception as exc:  # the SDK raises many unrelated types
            raise CloudUnavailable(
                f"content safety unreachable: {type(exc).__name__}: {exc}"
            ) from exc
        return _severities(result)


class AzureContentSafetyGate:
    """A :class:`~shared.safety.ContentSafetyGate` backed by Azure AI Content Safety."""

    def __init__(
        self,
        config: ContentSafetyConfig,
        sealer: Sealer,
        *,
        credential: Any | None = None,
        analyzer: SeverityAnalyzer | None = None,
        image_analyzer: ImageAnalyzer | None = None,
    ) -> None:
        if sealer.purpose is not SealPurpose.CONTENT_SAFETY:
            raise ValueError(f"the safety gate needs a CONTENT_SAFETY sealer, got {sealer.purpose}")
        self._config = config
        self._sealer = sealer
        backend = _AzureAnalyzer(config.endpoint, credential)
        self._analyze: SeverityAnalyzer = analyzer or backend
        self._analyze_image: ImageAnalyzer = image_analyzer or backend.image

    async def screen(
        self, kind: ContentKind, body: str, *, context: str = ""
    ) -> ScreenedPayload:
        # A picture is screened as a picture: the text categories say nothing about it.
        severities = (
            await self._analyze_image(body)
            if kind is ContentKind.IMAGE_PNG
            else await self._analyze(body)
        )
        worst = max(severities.values(), default=0)
        blocked = worst >= self._config.block_at_severity
        record = ScreeningRecord(
            verdict=SafetyVerdict.BLOCK if blocked else SafetyVerdict.ALLOW,
            severities=severities,
            screener=SCREENER_NAME,
            policy_version=POLICY_VERSION,
            screened_at=time.time(),
            detail=context,
        )
        if blocked:
            flagged = sorted(
                c for c, s in severities.items() if s >= self._config.block_at_severity
            )
            raise SafetyBlocked(f"refused at severity {worst}: {', '.join(map(str, flagged))}")

        # Seal exactly what ScreenedPayload will expose, or delivery would reject it later.
        draft = {"kind": str(kind), "body": body, "record": record.to_dict()}
        return ScreenedPayload(kind=kind, body=body, record=record, seal=self._sealer.seal(draft))

    async def aclose(self) -> None:
        """Release the HTTP session, when the analyzer owns one."""
        for candidate in (self._analyze, self._analyze_image):
            closer = getattr(candidate, "aclose", None) or getattr(
                getattr(candidate, "__self__", None), "aclose", None
            )
            if closer is not None:
                await closer()
                return
