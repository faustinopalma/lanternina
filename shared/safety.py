"""The content-safety contract: the single door every generated output must pass.

Rule: *nothing a model produced may reach the learner unless it has been screened.*

That rule is expressed by making :class:`ScreenedPayload` the **only** payload type a
:class:`~shared.proposal.Proposal` will accept. There is no code path that puts a raw
string in front of a user, because no user-facing type has a `str` field.

The gate itself lives in ``orchestrator/safety.py`` and is invoked exclusively by the
model router — agents never call it, and never see unscreened text at all.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from .seal import Seal, SealPurpose


class SafetyVerdict(StrEnum):
    ALLOW = "allow"
    BLOCK = "block"
    REVIEW = "review"  # not shown to the learner; queued for the parent to look at


class SafetyCategory(StrEnum):
    """Azure AI Content Safety categories, plus the ones this domain adds."""

    HATE = "hate"
    SELF_HARM = "self_harm"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    # Domain-specific screens layered on top of the Azure categories.
    AGE_INAPPROPRIATE = "age_inappropriate"
    FRIGHTENING = "frightening"
    OFF_TASK = "off_task"


class ContentKind(StrEnum):
    """What a screened payload actually is, so renderers know how to treat `body`."""

    PLAIN_TEXT = "plain_text"
    EXERCISE_JSON = "exercise_json"
    ROUTINE_PROMPT = "routine_prompt"
    FEEDBACK_TEXT = "feedback_text"
    PRINT_LAYOUT_JSON = "print_layout_json"
    # A generated picture, base64-encoded PNG. Still a str, so the seal covers it the same
    # way it covers a sentence, and no user-facing type gains a bytes field.
    IMAGE_PNG = "image_png"


@dataclass(frozen=True, slots=True)
class ScreeningRecord:
    """The evidence that screening happened, kept for audit."""

    verdict: SafetyVerdict
    severities: dict[SafetyCategory, int] = field(default_factory=dict)
    screener: str = "unknown"
    policy_version: str = "0"
    screened_at: float = 0.0
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": str(self.verdict),
            "severities": {str(k): v for k, v in sorted(self.severities.items())},
            "screener": self.screener,
            "policy_version": self.policy_version,
            "screened_at": self.screened_at,
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class ScreenedPayload:
    """Model output that has passed the safety gate and is sealed by it.

    Constructing one by hand is possible; producing one that *verifies* is not, because
    the HMAC key belongs to the gate. See :mod:`shared.seal`.
    """

    kind: ContentKind
    body: str
    record: ScreeningRecord
    seal: Seal

    def __post_init__(self) -> None:
        if self.record.verdict is not SafetyVerdict.ALLOW:
            raise ValueError(
                f"cannot build a ScreenedPayload from a {self.record.verdict} verdict"
            )
        if self.seal.purpose is not SealPurpose.CONTENT_SAFETY:
            raise ValueError(f"payload sealed for the wrong purpose: {self.seal.purpose}")

    def sealable(self) -> dict[str, Any]:
        """The exact structure the safety seal covers. Must stay stable across versions."""
        return {"kind": str(self.kind), "body": self.body, "record": self.record.to_dict()}


@runtime_checkable
class ContentSafetyGate(Protocol):
    """Implemented once, in ``orchestrator/safety.py``. Called only by the model router."""

    async def screen(self, kind: ContentKind, body: str, *, context: str = "") -> ScreenedPayload:
        """Screen ``body`` and return it sealed.

        Raises :class:`shared.errors.SafetyBlocked` when the verdict is not ALLOW — the
        caller must treat that as a normal outcome and fall back, not as a crash.
        """
        ...
