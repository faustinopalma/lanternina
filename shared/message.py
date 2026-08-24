"""What a parent may say while an afternoon is running, as a closed list of things.

Two channels, and `ideas/09 §8` is emphatic that they must not be joined. **Before**, a
parent may write anything: constraints, materials, themes, what to avoid, how long there is.
That is `panel/preferences.py`, it reaches a devising prompt as quoted material, and it is
the right place for whatever somebody wants to say. **During**, only this — a fact or a
constraint, chosen from a list, with a number attached where a number is needed.

The reason is specific and it is not about prompt injection. A sentence like "he is being
lazy, push him" enters the model's context and colours the tone of everything written after
it. A free text field aimed at a running afternoon is the most dangerous control on the
whole panel, and the defence that works is not screening it: it is not having it. There is
nowhere here to put a sentence.

**Three things this format cannot express**, and each one is a rule rather than a gap.

* **Anything about the person.** No name, no note, no reason. A message says something about
  the afternoon or about the house.
* **Anything that reaches a model.** These are read by :mod:`devices.run_experience`, which
  is code. Nothing here is ever put in a prompt.
* **Anything the adolescent could infer.** `§8` again: nothing a parent sends may produce a
  text that reveals the channel exists. An end hour that moves produces the ending arriving
  earlier, and the ending is the same ending, so there is nothing to notice.

**When it is applied.** At the end of the moment the afternoon is in, never in the middle of
an instruction. That is the runner's job and not this module's, but it is why the list is so
short: everything here has to be applicable at a seam, which rules out anything that would
change what somebody is currently holding.

**Inert on the way in.** A parent typing one of these writes a row and nothing else — no
model call, no queued work, nothing woken. The house finds it on its next look, because it
asked. That is the working rules' inert-dashboard line, and it is the reason a message
carries the moment it was written but nothing that could act on its own.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

MINUTES_IN_A_DAY: Final = 24 * 60


class MessageError(ValueError):
    """A message that is not one of the things a parent may say."""


class Says(StrEnum):
    """Everything a parent may say to a running afternoon. A fourth entry is a decision.

    Two, and the shortness is the design. `ideas/09 §8` lists more — pause, this device is
    broken, this material is missing, an interruption — and each of those needs the runner
    to do something it cannot do yet, so writing them here would be a vocabulary with no
    verbs behind it. They are named in `§23` as not built rather than declared and ignored.
    """

    # The afternoon is over by this hour, whatever it had reached. Moving it later is
    # allowed and is the same message with a later number: there is no separate "more time",
    # because two ways of saying one thing is how they drift apart.
    END_BY = "end_by"
    # Bring the ending forward to now. Not "stop": the afternoon still ends, by the way out
    # of wherever it got to and then its close, because an ending reached early is the same
    # ending and stopping without one is the failure this project exists to prevent.
    CLOSE_NOW = "close_now"


@dataclass(frozen=True, slots=True)
class Message:
    """One thing a parent said, and when they said it.

    ``minutes`` is minutes past midnight for :attr:`Says.END_BY`, and is not read for
    anything else. A single optional number rather than a payload per kind: two fields would
    be two things to keep in step, and nothing in `§8`'s list needs more than one number.
    """

    says: Says
    written_at: float
    minutes: int = 0

    def __post_init__(self) -> None:
        if self.says is Says.END_BY and not 0 <= self.minutes < MINUTES_IN_A_DAY:
            raise MessageError(
                f"{self.minutes} is not a time on the clock; it is minutes past midnight"
            )

    def to_dict(self) -> dict[str, Any]:
        return {"says": str(self.says), "writtenAt": self.written_at, "minutes": self.minutes}

    @staticmethod
    def from_dict(values: Any) -> Message:
        if not isinstance(values, dict):
            raise MessageError("a message must be an object")
        unknown = sorted(set(values) - {"says", "writtenAt", "minutes"})
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
        return Message(says=says, written_at=float(values.get("writtenAt", 0.0)), minutes=minutes)


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
