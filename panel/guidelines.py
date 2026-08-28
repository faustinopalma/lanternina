"""The limits an improvising afternoon has to stay inside, written by the parent.

`ideas/09` gives the execution layer a plan and `ideas/10` gives it a page. Neither says what
it may do when what actually happened is not what the plan assumed — a page that came back
blank, a printer with no paper, an afternoon that has plainly gone somewhere else. Following
the plan regardless is wrong, and stopping is worse: an afternoon that ends because reality
deviated is an afternoon that failed somebody for being alive.

So it improvises, and these are the bounds. The parent's own sentences about what must not
happen in this house, kept as they wrote them and handed to the model as material rather
than as instructions.

**Two kinds of bound, and only one of them is the parent's.** :data:`FIXED` is ours and cannot
be edited from anywhere: nothing says anything about the person, nothing announces a change,
an ending stays reachable, no equipment is invented that the house does not have. Those are
the working rules and a parent loosening them would not be configuring a system, they would be
removing its reason to exist. What the parent owns is the rest — the house-specific limits we
could not know: that nobody goes outside, that there are no scissors within reach, that
nothing may make a noise after nine.

**They only ever narrow, and that changed on 28 August 2026.** These used to be permissions —
"going out into the garden is fine" — and a permission widens what an afternoon may do, which
is why the prompt had to carry a sentence telling the model not to let one loosen the fixed
bounds. A page that can only narrow cannot loosen anything, so the guarantee stops depending
on a sentence a model has to honour. The parent asked for the change; this is the reason it
is the right one.

**The default is empty, deliberately.** A house that has said nothing gets the fixed bounds and
nothing narrower. Suggested lines belong in the panel, where a parent can read one and decide,
not in a store that would be putting words in their mouth.

**Untrusted, like everything a parent types.** These reach a prompt as quoted material and the
prompt says not to follow instructions written inside them. That is the working rules' line
about free text.

Writing one is inert: a row is stored and nothing else happens. The next afternoon that needs
to improvise finds them, because it asked.
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
    "Never say anything about the person: not how well anything was done, not how much "
    "effort it took, not what any of it suggests about them.",
    "Never announce, explain or apologise for a change of course. It arrives as part of "
    "what is happening.",
    "An ending stays reachable from wherever the afternoon has got to, and an ending "
    "reached early is the same ending.",
    "Use only what this house has. Never invent equipment, materials or a place.",
    "Nothing can be failed and nothing has to be finished.",
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
