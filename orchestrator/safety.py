"""The content-safety gate: the single door model output passes before it is proposed.

This module and ``orchestrator/router.py`` are the only two places permitted to import a
cloud SDK. Three callers reach the gate and no more: the router, for everything an agent
generates, :func:`screen_experience`, for a whole afternoon before a parent reads it, and
:func:`screen_continuation`, for the rest of one. Agents never see unscreened text, so an
agent cannot route around screening even by mistake.

The gate holds the ``CONTENT_SAFETY`` sealer. That is what makes the rule enforceable
rather than customary: anyone can construct a :class:`~shared.safety.ScreenedPayload`,
but only this module can produce one whose seal survives ``assert_deliverable``.

The two experience functions are here rather than beside the experience code for the
reason the router is: the gate is the only thing between a model and a person, and a
caller who could reach the words without reaching one of these would be a way around it.

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
from shared.experience import Continuation, Experience
from shared.safety import (
    ContentKind,
    ContentSafetyGate,
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


# ── An afternoon, whole or in part ───────────────────────────────────────────────────


def words_for_a_person(plan: Continuation | Experience) -> str:
    """Everything in an afternoon that somebody will read, one line each.

    Gathered rather than screened field by field, because what arrives arrives as one
    thing and a refusal applies to all of it: half an afternoon is not a thing this house
    can put on a display.

    A whole experience also carries a title and an overview, and those go in too. They are
    the parent's half rather than the adolescent's — the overview is what approval is
    given to — and a model wrote them, which is the only qualification this door asks for.

    Which words those are is :attr:`shared.experience.Moment.words` and not a second list
    kept here. It was a second list until format 2, and a second list is how the gate and
    the block list end up disagreeing about whether a rung of help is text somebody reads.
    """
    lines: list[str] = []
    if isinstance(plan, Experience):
        lines.append(plan.title)
        lines.append(plan.overview)
    for moment in plan.moments:
        lines.extend(moment.words)
    return "\n".join(line for line in lines if line.strip())


async def screen_experience(
    gate: ContentSafetyGate, experience: Experience, *, context: str = ""
) -> ScreenedPayload:
    """The door a devised afternoon passes before a parent is offered it.

    Earlier than :func:`screen_continuation`, and for a different reason. A parent does
    read this one, so the gate is not the only thing between a model and a person here —
    but an overview is what they read, and everything else in the document reaches an
    adolescent on the strength of that overview. Screening the whole thing now is what
    makes approving it from a summary an honest thing to ask.
    """
    body = words_for_a_person(experience)
    if not body:
        raise SafetyBlocked("an afternoon with no words for anybody is not one")
    return await gate.screen(ContentKind.PLAIN_TEXT, body, context=context)


async def screen_continuation(
    gate: ContentSafetyGate, carrying_on: Continuation, *, context: str = ""
) -> ScreenedPayload:
    """The door a continuation passes before a house is told to play it.

    This is the gate doing more work than it was built for, and the reason is recorded in
    `ideas/08 §2` rather than discovered here: a parent approves an experience once, from
    its overview, so what a continuation puts on a display and on paper has been seen by
    no adult. Between a model and a person there is this call and nothing else.

    Raises :class:`~shared.errors.SafetyBlocked` when the gate refuses, which the caller
    treats as a normal outcome — an afternoon that is not continued simply stops, which is
    what an afternoon nobody continues does anyway.
    """
    body = words_for_a_person(carrying_on)
    if not body:
        # A continuation with nothing to read passes any screen trivially, which is the
        # one way an unscreened afternoon could reach a house through this function.
        raise SafetyBlocked("a continuation with no words for anybody is not one")
    return await gate.screen(ContentKind.PLAIN_TEXT, body, context=context)
