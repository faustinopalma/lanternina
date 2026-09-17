"""Household execution bounds, separate from configurable activity prompts.

The fixed bounds preserve safety, isolation, approved scope, available equipment and the
ability to stop. The parent adds household-specific limits. Educational and editorial
choices belong to the three prompts in :mod:`shared.steering`, not to these bounds.
Saving updates a stored row; it does not contact a device or start an activity.
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Final, Protocol, runtime_checkable

# Long enough for a sentence about one thing — "non deve far salire nessuno su una sedia" —
# and short enough that the box is plainly not for writing a policy in.
MAX_LINE_CHARS: Final = 160
# More than a parent will read back before approving is a list nobody is really deciding.
MAX_LINES: Final = 12

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")

# Ours, and not editable from anywhere. Stated here rather than only inside a prompt so that
# the difference between what a parent may change and what nobody may is a thing in the code.
FIXED: Final = (
    "Preserve safety, household isolation and the scope approved by the parent.",
    "Use available tools and declared materials; distinguish observations from assumptions.",
    "Keep closure reachable and honor a stop request without requiring further work.",
)


@dataclass(frozen=True, slots=True)
class Guidelines:
    """The limits this household puts on an afternoon that is improvising."""

    household_id: str
    lines: tuple[str, ...] = ()
    updated_at: float = 0.0
    updated_by: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "lines": list(self.lines),
            # Shown beside the parent's own, so that what they are adding to is legible.
            # Read-only on the way out and refused on the way in.
            "fixed": list(FIXED),
            "updatedAt": self.updated_at,
            "lineLimit": MAX_LINE_CHARS,
            "maxLines": MAX_LINES,
        }

    def as_material(self) -> str:
        """The parent's lines for a prompt, quoted. Empty when they have written none."""
        if not self.lines:
            return ""
        return "\n".join(f"- {line}" for line in self.lines)


@runtime_checkable
class GuidelineStore(Protocol):
    def get(self, household_id: str) -> Guidelines: ...

    def set(self, guidelines: Guidelines) -> Guidelines: ...


@dataclass
class InMemoryGuidelineStore:
    _rows: dict[str, Guidelines] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get(self, household_id: str) -> Guidelines:
        with self._lock:
            # A household that has never written any gets none, not an error: the house has
            # to be able to run an afternoon before anybody has opened the panel.
            return self._rows.get(household_id, Guidelines(household_id=household_id))

    def set(self, guidelines: Guidelines) -> Guidelines:
        with self._lock:
            self._rows[guidelines.household_id] = guidelines
            return guidelines


def clean_lines(
    household_id: str, raw: Any, *, updated_by: str = "", now: float | None = None
) -> Guidelines:
    """Normalise what the parent wrote. Raises ValueError if it cannot be kept.

    Runs of whitespace collapse and line breaks go with them, for the reason
    `panel/reminders.py` gives: this text is handed to a model, and a second line is the
    cheapest way to make one sentence look like a new instruction.
    """
    if isinstance(raw, str) or not isinstance(raw, (list, tuple)):
        raise ValueError("the guidelines are a list of lines")
    kept: list[str] = []
    for entry in raw:
        line = " ".join(str(entry).split())
        if not line:
            continue
        if len(line) > MAX_LINE_CHARS:
            raise ValueError(f"a line must be at most {MAX_LINE_CHARS} characters")
        if _CONTROL.search(line):
            raise ValueError("a line is written in ordinary characters")
        kept.append(line)
    if len(kept) > MAX_LINES:
        raise ValueError(f"at most {MAX_LINES} lines")
    return Guidelines(
        household_id=household_id,
        lines=tuple(kept),
        updated_at=now if now is not None else time.time(),
        updated_by=updated_by,
    )
