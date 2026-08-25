"""What the parent said to a running afternoon, waiting for the house to come and look.

`shared/message.py` says what may be said and `devices/run_experience.hear` applies it.
This is the part in between: where a message sits between the parent typing it and the
house asking. Nothing here interprets anything — a row is written, and the house finds it
on the look it already makes every minute.

**Inert on the way in**, which is the rule and not a preference. Writing one calls no
model, queues nothing and wakes nothing. There is no route from here into the house, and
the panel is not allowed to acquire one, so the parent's press costs one row and the
afternoon changes when the house next asks.

**A list rather than one row per household.** ``hear`` takes a sequence and folds it in
order, so the store hands over what is pending and the house applies all of it. Keeping
only the last would give the same answer today — both things a parent may say assign the
end hour outright — but that is a property of this vocabulary rather than of the channel,
and it would stop being true of the first message that is not an assignment.

**Cleared by id, by the house.** A message the parent writes while the house is midway
through the previous one is still there afterwards, because the house says which one it
heard rather than saying "that lot".

**An hour, and then it is gone.** A message still waiting after an hour was written to a
house that was not listening. What that buys is that a message cannot reach an afternoon
it was not written about. What it costs is that a message written while the house is off
is lost, and the parent sees it disappear rather than being told it did not arrive.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.ids import new_id
from shared.message import Message, Says, at_the_clock

# An hour. It was written as "six looks of the house's ten-minute timer", which was the
# same number until the timer went to one minute on 25 August 2026 and would have taken
# this to six. The quantity that matters is how long a parent's sentence should survive a
# house that is off or unreachable, and that has nothing to do with how often a healthy
# one looks: an hour is long enough to cover a reboot and short enough that a sentence
# about an afternoon cannot arrive inside the next one.
MESSAGE_LIFETIME_SECONDS = 60 * 60


@dataclass(frozen=True, slots=True)
class PendingMessage:
    """One thing the parent said, and whether the house has come for it yet.

    The id is the store's, not the message's: :class:`~shared.message.Message` carries what
    was said, and this carries which row said it. Keeping them apart is what lets the house
    hand back an id without the vocabulary growing a field that is about bookkeeping.
    """

    id: str
    household_id: str
    said: Message
    written_by: str = ""

    def stale(self, now: float) -> bool:
        return now - self.said.written_at >= MESSAGE_LIFETIME_SECONDS

    def to_public(self) -> dict[str, Any]:
        return {"id": self.id, **self.said.to_dict()}


@runtime_checkable
class MessageStore(Protocol):
    def add(self, pending: PendingMessage) -> PendingMessage: ...

    def pending(self, household_id: str) -> list[PendingMessage]: ...

    def heard(self, household_id: str, message_id: str) -> bool: ...


@dataclass
class InMemoryMessageStore:
    _rows: dict[tuple[str, str], PendingMessage] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, pending: PendingMessage) -> PendingMessage:
        with self._lock:
            self._rows[(pending.household_id, pending.id)] = pending
            return pending

    def pending(self, household_id: str) -> list[PendingMessage]:
        now = time.time()
        with self._lock:
            # Expiry is applied on the way out rather than by something that sweeps: there
            # is no timer up here, and a row nobody reads costs nothing to leave lying.
            for key, row in list(self._rows.items()):
                if row.stale(now):
                    del self._rows[key]
            rows = [
                row for (household, _), row in self._rows.items() if household == household_id
            ]
        return sorted(rows, key=lambda row: row.said.written_at)

    def heard(self, household_id: str, message_id: str) -> bool:
        with self._lock:
            return self._rows.pop((household_id, message_id), None) is not None


def clean_message(
    household_id: str,
    *,
    says: Any,
    at: str = "",
    written_by: str = "",
    now: float | None = None,
) -> PendingMessage:
    """Normalise what the parent chose. Raises MessageError on anything not on the list.

    ``at`` is "HH:MM", because that is what a form gives and what the parent chose; the
    minutes past midnight the message carries are arithmetic and belong on this side of the
    API rather than in a browser. What may be said is decided by ``Message.from_dict`` and
    not repeated here: a second place that decides that is a second policy.
    """
    said = Message.from_dict(
        {
            "says": str(says),
            "writtenAt": float(now if now is not None else time.time()),
            "minutes": at_the_clock(at) if str(says) == Says.END_BY else 0,
        }
    )
    return PendingMessage(
        id=str(new_id("say")), household_id=household_id, said=said, written_by=written_by
    )
