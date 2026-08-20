"""What the parent has asked the house to do, waiting for the house to come and look.

A write from the panel is inert: it may persist state and nothing else. So "put this
picture back" cannot be a job handed to the hub — the panel has no way to reach into the
house and is not allowed to acquire one. What it can be is a record. The parent presses,
one row is written, and the hub finds it the next time it asks. Nothing is woken, nothing
is queued, and the hub is free to look when it chooses and to decline.

Three decisions are written down here rather than left to be discovered:

* **One request per household, the last one wins.** A parent who presses twice before the
  hub looks meant the second press; a queue would put a picture they have changed their
  mind about on the display first, and would need a rule for how long the queue may grow.
* **A request that nobody collected expires after a day.** The longest spacing a parent
  can set between pictures is twenty-four hours, so a day is the longest a request can
  legitimately be waiting; past that the hub was off, and a picture asked for yesterday is
  not what somebody wants appearing tomorrow.
* **The hub clears it, and only the one it acted on.** Clearing by id means a second press
  that lands while the hub is fetching the first picture is still there afterwards,
  instead of being thrown away by a hub that only knows "there was something".
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# Put this picture back on the display. The only kind so far, and named rather than
# implied, so the second kind does not have to change the shape of the first.
KIND_SHOW_AGAIN = "showAgain"
KINDS = (KIND_SHOW_AGAIN,)

# See the module docstring: one day, because the widest spacing a parent may choose is one
# day. Kept as seconds because that is what the comparison is in.
REQUEST_LIFETIME_SECONDS = 24 * 60 * 60


@dataclass(frozen=True, slots=True)
class HouseRequest:
    """Something the parent asked for, which the house has not yet come to collect."""

    id: str
    household_id: str
    kind: str
    subject: str
    asked_at: float
    asked_by: str = ""

    def stale(self, now: float) -> bool:
        return now - self.asked_at >= REQUEST_LIFETIME_SECONDS

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "subject": self.subject,
            "askedAt": self.asked_at,
        }


@runtime_checkable
class RequestStore(Protocol):
    def put(self, asked: HouseRequest) -> HouseRequest: ...

    def get(self, household_id: str) -> HouseRequest | None: ...

    def clear(self, household_id: str, request_id: str) -> bool: ...


@dataclass
class InMemoryRequestStore:
    _rows: dict[str, HouseRequest] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def put(self, asked: HouseRequest) -> HouseRequest:
        with self._lock:
            self._rows[asked.household_id] = asked
            return asked

    def get(self, household_id: str) -> HouseRequest | None:
        with self._lock:
            standing = self._rows.get(household_id)
            # Expiry is applied on the way out rather than by something that sweeps: there
            # is no timer up here, and a row nobody reads costs nothing to leave lying.
            if standing is not None and standing.stale(time.time()):
                del self._rows[household_id]
                return None
            return standing

    def clear(self, household_id: str, request_id: str) -> bool:
        with self._lock:
            standing = self._rows.get(household_id)
            if standing is None or standing.id != request_id:
                return False
            del self._rows[household_id]
            return True


def clean_request(
    household_id: str,
    *,
    kind: str,
    subject: str,
    asked_by: str = "",
    now: float | None = None,
) -> HouseRequest:
    """Normalise what the parent asked for. Raises ValueError if it cannot be honoured."""
    from shared.ids import new_id

    if kind not in KINDS:
        raise ValueError(f"not something the house is asked for: {kind}")
    wanted = subject.strip()
    if not wanted:
        raise ValueError("a request has to say what it is about")
    return HouseRequest(
        id=str(new_id("ask")),
        household_id=household_id,
        kind=kind,
        subject=wanted,
        asked_at=now if now is not None else time.time(),
        asked_by=asked_by,
    )
