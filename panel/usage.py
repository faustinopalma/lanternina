"""What a household's pictures cost, and the cap that stops a runaway loop.

This is a count, not a bill. It records what the model backend said each call consumed,
and it exists so that two questions have answers: *how much has this house used this
month*, and *does that number agree with what Azure charges*. The second is why every
event carries the provider's own request id.

Nothing here is about her. A token count is a fact about a machine.

The event is append-only and carries its own id, so replaying it cannot count twice. That
costs one field now and would be expensive to add later, once there are figures somebody
has relied on.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable

from shared.routing import ModelUsage

KIND_IMAGE = "image"
KIND_TEXT = "text"

# Told apart because they cost differently: a picture the gate refused was still generated
# and still paid for, while one that never reached the model was not.
SERVED = "served"
REFUSED = "refused"
FAILED = "failed"

# An hourly picture is at most 744 a month. The default leaves room for a parent asking
# for a few by hand, and still stops a loop that has lost its mind.
DEFAULT_MONTHLY_PICTURE_CAP = 1000


def month_of(at: float) -> str:
    """The bucket a cap is measured over, in UTC so it does not move twice a year."""
    return datetime.fromtimestamp(at, UTC).strftime("%Y-%m")


@dataclass(frozen=True, slots=True)
class UsageEvent:
    id: str
    household_id: str
    at: float
    kind: str
    outcome: str
    deployment: str = ""
    request_id: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    # Part of input_tokens, billed at a discount.
    cached_input_tokens: int = 0
    # Part of output_tokens, and absent from the text the model returned.
    reasoning_tokens: int = 0
    size: str = ""
    quality: str = ""

    @property
    def period(self) -> str:
        return month_of(self.at)


@dataclass(frozen=True, slots=True)
class UsageSummary:
    household_id: str
    period: str
    calls: int = 0
    # Calls that reached the model, whatever the gate then decided. This is what the cap
    # counts, because it is what was paid for.
    billed_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    reasoning_tokens: int = 0

    def to_public(self) -> dict[str, Any]:
        return {
            "period": self.period,
            "calls": self.calls,
            "billedCalls": self.billed_calls,
            "inputTokens": self.input_tokens,
            "outputTokens": self.output_tokens,
            "cachedInputTokens": self.cached_input_tokens,
            "reasoningTokens": self.reasoning_tokens,
        }


def summarise(household_id: str, period: str, events: list[UsageEvent]) -> UsageSummary:
    billed = [event for event in events if event.outcome != FAILED]
    return UsageSummary(
        household_id=household_id,
        period=period,
        calls=len(events),
        billed_calls=len(billed),
        input_tokens=sum(event.input_tokens for event in events),
        output_tokens=sum(event.output_tokens for event in events),
        cached_input_tokens=sum(event.cached_input_tokens for event in events),
        reasoning_tokens=sum(event.reasoning_tokens for event in events),
    )


@runtime_checkable
class UsageStore(Protocol):
    def record(self, event: UsageEvent) -> UsageEvent: ...

    def summary(self, household_id: str, period: str) -> UsageSummary: ...


@dataclass
class InMemoryUsageStore:
    _rows: dict[tuple[str, str], UsageEvent] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, event: UsageEvent) -> UsageEvent:
        with self._lock:
            # Keyed by id, so a retry of the same event does not count twice.
            return self._rows.setdefault((event.household_id, event.id), event)

    def summary(self, household_id: str, period: str) -> UsageSummary:
        with self._lock:
            events = [
                event
                for (household, _), event in self._rows.items()
                if household == household_id and event.period == period
            ]
        return summarise(household_id, period, events)


def over_cap(store: UsageStore, household_id: str, cap: int, now: float | None = None) -> bool:
    """Whether this household has already paid for as many calls as it is allowed."""
    if cap <= 0:
        return False
    return store.summary(household_id, month_of(now or time.time())).billed_calls >= cap


def event_from(
    household_id: str,
    kind: str,
    outcome: str,
    reported: ModelUsage | None,
    *,
    event_id: str,
    at: float | None = None,
) -> UsageEvent:
    """One event from what the backend reported, or an empty one when it reported nothing."""
    return UsageEvent(
        id=event_id,
        household_id=household_id,
        at=at if at is not None else time.time(),
        kind=kind,
        outcome=outcome,
        deployment=reported.deployment if reported else "",
        request_id=reported.request_id if reported else "",
        input_tokens=reported.input_tokens if reported else 0,
        output_tokens=reported.output_tokens if reported else 0,
        cached_input_tokens=reported.cached_input_tokens if reported else 0,
        reasoning_tokens=reported.reasoning_tokens if reported else 0,
        size=reported.size if reported else "",
        quality=reported.quality if reported else "",
    )
