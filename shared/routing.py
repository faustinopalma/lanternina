"""The model-routing contract.

Exactly one implementation exists (``orchestrator/router.py``) and it is the **only**
module in the repo permitted to import an Azure SDK or touch the local model runtime.
Agents receive a :class:`ModelRouter` and nothing lower-level.

Two entry points, deliberately different types:

* :meth:`ModelRouter.generate_for_user` returns :class:`~shared.safety.ScreenedPayload` —
  it screens on the way out. Anything destined for the learner uses this.
* :meth:`ModelRouter.analyze` returns a raw :class:`ModelResponse` for internal reasoning
  (planning, reading a worksheet). Its text is *not* screened, and it cannot be placed in
  a :class:`~shared.proposal.Proposal`, because a Proposal only accepts a ScreenedPayload.

Degradation is a first-class part of the contract: every response reports the tier that
served it and whether capability was reduced. The router must never raise because the
cloud is down — it falls back, and says so.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from typing import Any, Protocol, runtime_checkable

from .ids import RequestId
from .safety import ContentKind, ScreenedPayload


class Capability(StrEnum):
    """What the caller needs done, not which model does it."""

    TEXT_GENERATION = "text_generation"
    STRUCTURED_GENERATION = "structured_generation"
    VISION_READ = "vision_read"
    PLANNING = "planning"


class ModelTier(StrEnum):
    """Where a request was served. Ordered from most to least capable."""

    CLOUD_FOUNDRY = "cloud_foundry"
    LOCAL_SLM = "local_slm"
    CACHED_FALLBACK = "cached_fallback"


class DegradationLevel(IntEnum):
    """How reduced the current capability is. Surfaced to the parent panel, never hidden."""

    FULL = 0  # cloud reachable, everything available
    REDUCED = 1  # local model only: simpler content, no vision reading of handwriting
    MINIMAL = 2  # pre-approved cached content only; no generation at all
    # There is no level for "system unavailable". Going dark is not an allowed state.


@dataclass(frozen=True, slots=True)
class PageImage:
    """A rectified page crop, the only image type that may be sent to a model.

    Full camera frames cannot reach here: :class:`~shared.vision_contracts.RawFrame`
    exposes no conversion to bytes.
    """

    png: bytes
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class ModelRequest:
    capability: Capability
    prompt: str
    request_id: RequestId
    # Populated only for VISION_READ. Never a full frame — see PageImage.
    images: tuple[PageImage, ...] = ()
    max_output_chars: int = 400
    # Free-text note for logs and the parent panel ("generating a counting exercise").
    purpose: str = ""
    # For generate_for_user: what kind of content this is, so the gate can pick a policy.
    content_kind: ContentKind = ContentKind.PLAIN_TEXT
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    tier: ModelTier
    degradation: DegradationLevel
    reason: str


@dataclass(frozen=True, slots=True)
class ModelResponse:
    """Raw model output. Internal use only — see the module docstring."""

    text: str
    request_id: RequestId
    routing: RoutingDecision
    latency_s: float
    truncated: bool = False


@dataclass(frozen=True, slots=True)
class RouterHealth:
    """What the router currently believes about its backends. Shown in the parent panel."""

    cloud_available: bool
    local_available: bool
    degradation: DegradationLevel
    last_cloud_error: str = ""
    last_checked_at: float = 0.0


@runtime_checkable
class ModelRouter(Protocol):
    async def generate_for_user(self, request: ModelRequest) -> ScreenedPayload:
        """Generate content intended for the learner, screened and sealed on the way out.

        Raises:
            SafetyBlocked: the gate rejected the output. Callers retry or fall back.
            NoCapacityError: no tier could serve it, including the cache.
        """
        ...

    async def analyze(self, request: ModelRequest) -> ModelResponse:
        """Internal reasoning. The result must not be shown to the learner directly."""
        ...

    def health(self) -> RouterHealth:
        """Current backend availability. Cheap; safe to poll from the panel."""
        ...
