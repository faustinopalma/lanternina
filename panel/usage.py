"""What a household's model calls cost, and the cap that stops a runaway loop.

This is a count, not a bill. It records what the model backend said each call consumed,
and it exists so that two questions have answers: *how much has this house used this
month*, and *does that number agree with what Azure charges*. The second is why every
event carries the provider's own request id.

The figures are reported per kind as well as together. A picture, a wording and a reading
cost different amounts of different things, so one total covering all three is a number
whose name does not say what it holds.

Nothing here is about a person. A token count is a fact about a machine.

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
# Kept apart from KIND_TEXT rather than folded into it. A reading is a measurement — what
# is on a page, what hour a sentence names — and nothing it produces is shown to anybody;
# the wordings under KIND_TEXT are read off a display. Summing the two would give back a
# figure whose name says less than it holds, which is the thing just taken apart.
KIND_READ = "read"
# Reported even when a household has made none of that kind, so a figure of zero is
# distinguishable from a kind the panel forgot to mention.
KINDS = (KIND_IMAGE, KIND_TEXT, KIND_READ)

# Told apart because they cost differently: a picture the gate refused was still generated
# and still paid for, while one that never reached the model was not.
SERVED = "served"
REFUSED = "refused"
FAILED = "failed"

# What a working month costs, added up per path rather than guessed. Pictures: the parent
# sets the spacing, default 60 minutes, and if they switch the night pause off that is 24
# a day, 744 in a 31-day month. Readings: one call per page put on the glass, so a house
# that scans ten a day pays 310. Reminders: a sentence is read once and worded once in its
# life, so one new sentence a day is 62. Total 1116 in a month nobody would call unusual.
#
# The figure that stood here was 1000, chosen when a picture was the only thing counted.
# It is now below an ordinary month, which makes the cap the thing that decides how much a
# house may do rather than the thing that stops a fault.
#
# Twice the ordinary month. What that buys is that a house behaving as designed never
# meets the cap; what it costs is that a loop which has lost its mind runs about a day
# longer before it is stopped. The finest spacing a parent can set is one minute, which is
# 900 pictures a day inside the default waking hours, so 2000 ends it on the third day.
DEFAULT_MONTHLY_CALL_CAP = 2000

# The highest a parent may raise the fuse from the panel. A fuse that can be set to
# anything is not a fuse, and one that cannot be raised stops legitimate work: this is the
# line between the two. At the finest spacing a parent may set — one minute, 900 calls a
# day inside the default waking hours — a runaway loop reaches 20000 in about three weeks,
# so the calendar month ends it either way. It bounds calls and not money: the unit price
# is still not known, which is written up in ideas/04-system.md.
MAX_MONTHLY_CALL_CAP = 20000


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
class UsageTotals:
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
            "calls": self.calls,
            "billedCalls": self.billed_calls,
            "inputTokens": self.input_tokens,
            "outputTokens": self.output_tokens,
            "cachedInputTokens": self.cached_input_tokens,
            "reasoningTokens": self.reasoning_tokens,
        }


@dataclass(frozen=True, slots=True)
class UsageSummary:
    household_id: str
    period: str
    total: UsageTotals = UsageTotals()
    by_kind: dict[str, UsageTotals] = field(default_factory=dict)

    def to_public(self) -> dict[str, Any]:
        return {
            "period": self.period,
            "total": self.total.to_public(),
            "byKind": {kind: totals.to_public() for kind, totals in self.by_kind.items()},
        }


def _totals(events: list[UsageEvent]) -> UsageTotals:
    return UsageTotals(
        calls=len(events),
        billed_calls=len([event for event in events if event.outcome != FAILED]),
        input_tokens=sum(event.input_tokens for event in events),
        output_tokens=sum(event.output_tokens for event in events),
        cached_input_tokens=sum(event.cached_input_tokens for event in events),
        reasoning_tokens=sum(event.reasoning_tokens for event in events),
    )


def summarise(household_id: str, period: str, events: list[UsageEvent]) -> UsageSummary:
    kinds = dict.fromkeys((*KINDS, *(event.kind for event in events)))
    return UsageSummary(
        household_id=household_id,
        period=period,
        total=_totals(events),
        by_kind={
            kind: _totals([event for event in events if event.kind == kind]) for kind in kinds
        },
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
    return store.summary(household_id, month_of(now or time.time())).total.billed_calls >= cap


@dataclass(frozen=True, slots=True)
class Fuse:
    """Where a household's fuse has been set, and who last moved it.

    Absent means nobody has moved it and the configured default applies, so changing
    `LANTERNINA_MONTHLY_CALL_CAP` still reaches every household that never touched it.
    """

    household_id: str
    calls: int
    raised_at: float = 0.0
    raised_by: str = ""


@runtime_checkable
class FuseStore(Protocol):
    def get(self, household_id: str) -> Fuse | None: ...

    def set(self, fuse: Fuse) -> Fuse: ...


@dataclass
class InMemoryFuseStore:
    _rows: dict[str, Fuse] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get(self, household_id: str) -> Fuse | None:
        with self._lock:
            return self._rows.get(household_id)

    def set(self, fuse: Fuse) -> Fuse:
        with self._lock:
            self._rows[fuse.household_id] = fuse
        return fuse


def cap_of(store: FuseStore, household_id: str, configured: int) -> int:
    """Where this household's fuse sits: where it was moved to, or the configured default."""
    moved = store.get(household_id)
    return configured if moved is None else moved.calls


def clean_cap(calls: int, spent: int) -> int:
    """The fuse a parent may set. Raises ValueError with what is wrong and what is allowed.

    Zero is not reachable from the panel. It means "no fuse at all" to :func:`over_cap`,
    and switching the protection off is a deployment decision, not a click.
    """
    if calls < 1 or calls > MAX_MONTHLY_CALL_CAP:
        raise ValueError(f"the fuse is between 1 and {MAX_MONTHLY_CALL_CAP} calls a month")
    if calls <= spent:
        # Otherwise the parent raises it, nothing starts, and the panel looks broken.
        raise ValueError(f"this month has already spent {spent} calls; set it above that")
    return calls


def fuse_blown(
    usage: UsageStore, fuses: FuseStore, household_id: str, configured: int
) -> bool:
    """Whether this household's fuse has gone, wherever it has been set."""
    return over_cap(usage, household_id, cap_of(fuses, household_id, configured))


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
