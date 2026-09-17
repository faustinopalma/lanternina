"""Parent commands carried to the hub by its authenticated polling channels.

Deadline commands change when a planned ending begins. Termination names one live activity.
Photo assignment names the original activity, moment and waiting interval so a delayed
command cannot attach the photograph to a later step.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

MINUTES_IN_A_DAY: Final = 24 * 60


class MessageError(ValueError):
    """A message that is not one of the things a parent may say."""


class Says(StrEnum):
    """Commands implemented by the activity runner and photograph queue."""

    # The afternoon is over by this hour, whatever it had reached. Moving it later is
    # allowed and is the same message with a later number: there is no separate "more time",
    # because two ways of saying one thing is how they drift apart.
    END_BY = "end_by"
    CLOSE_NOW = "close_now"
    TERMINATE = "terminate"
    ASSIGN_PHOTO = "assign_photo"


@dataclass(frozen=True, slots=True)
class Message:
    """One command with its timestamp and kind-specific target fields."""

    says: Says
    written_at: float
    minutes: int = 0
    run_id: str = ""
    photo_id: str = ""
    moment_id: str = ""
    waiting_since: float = 0.0

    def __post_init__(self) -> None:
        if self.says in {Says.TERMINATE, Says.ASSIGN_PHOTO} and not self.run_id:
            raise MessageError("termination requires an activity")
        if len(self.run_id) > 200:
            raise MessageError("activity id is too long")
        if self.says is Says.ASSIGN_PHOTO and (
            not re.fullmatch(r"[0-9a-f]{32}", self.photo_id) or not self.moment_id
            or len(self.moment_id) > 200 or not math.isfinite(self.waiting_since)
            or self.waiting_since < 0
        ):
            raise MessageError("photo assignment requires a valid photo and waiting moment")
        if self.says is Says.END_BY and not 0 <= self.minutes < MINUTES_IN_A_DAY:
            raise MessageError(
                f"{self.minutes} is not a time on the clock; it is minutes past midnight"
            )

    def to_dict(self) -> dict[str, Any]:
        return {"says": str(self.says), "writtenAt": self.written_at, "minutes": self.minutes,
                **({"runId": self.run_id} if self.run_id else {}),
                **({"photoId": self.photo_id, "momentId": self.moment_id,
                    "waitingSince": self.waiting_since} if self.photo_id else {})}

    @staticmethod
    def from_dict(values: Any) -> Message:
        if not isinstance(values, dict):
            raise MessageError("a message must be an object")
        unknown = sorted(set(values) - {
            "says", "writtenAt", "minutes", "runId", "photoId", "momentId", "waitingSince",
        })
        if unknown:
            raise MessageError(f"a message carries {unknown}, which is not something to say")
        raw = str(values.get("says", ""))
        try:
            says = Says(raw)
        except ValueError as exc:
            raise MessageError(
                f"{raw!r} is not something a parent may say; the list is "
                f"{sorted(str(s) for s in Says)}"
            ) from exc
        minutes = values.get("minutes", 0)
        if isinstance(minutes, bool) or not isinstance(minutes, int):
            raise MessageError("minutes must be a whole number of minutes past midnight")
        return Message(says=says, written_at=float(values.get("writtenAt", 0.0)), minutes=minutes,
                       run_id=str(values.get("runId") or ""),
                       photo_id=str(values.get("photoId") or ""),
                       moment_id=str(values.get("momentId") or ""),
                       waiting_since=float(values.get("waitingSince", 0)))


def at_the_clock(value: str) -> int:
    """"HH:MM" as minutes past midnight, for a panel that takes an hour from a form."""
    hour, _, minute = value.strip().partition(":")
    try:
        hours, minutes = int(hour), int(minute)
    except ValueError as exc:
        raise MessageError(f"not a time on the clock: {value!r}") from exc
    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        raise MessageError(f"not a time on the clock: {value!r}")
    return hours * 60 + minutes
