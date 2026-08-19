"""What the parent wants remembered, written the way they would say it.

A sentence here is not a reminder yet. It is what somebody typed — "lavarsi i denti dopo
cena", "mercoledì porta fuori il bidone" — kept exactly as they wrote it and marked as not
yet read.

The marking is the whole point, and it comes from a rule rather than from a preference. A
write from the panel is inert: it may persist state and nothing else, so the panel cannot
ask a model what a sentence means at the moment the sentence is typed. What it can do is
say that nobody has looked yet. The house asks later, on the timer it already has, and the
reading happens inside the answer to that request.

So this module holds the parent's half and what the house made of it. Nothing here
interprets, schedules or shows anything: the reading arrives from outside, already turned
into a time or into a question, and is written down here.
"""

from __future__ import annotations

import re
import secrets
import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from typing import Any, Final, Protocol, runtime_checkable

# Long enough for a sentence with a day and an hour in it, short enough that the box is
# plainly not for writing paragraphs in.
MAX_SENTENCE_LENGTH = 200

# A question comes from a model and is shown to the parent, so it is bounded like anything
# else that arrives from outside. One line, because it asks for one missing thing.
MAX_QUESTION_LENGTH = 120

# Monday first, and these exact three letters, because the hub and the panel both read
# them. A day the model spells any other way is not a day.
DAYS: Final = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_CLOCK = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


@dataclass(frozen=True, slots=True)
class Sentence:
    id: str
    household_id: str
    text: str
    created_at: float
    created_by: str = ""
    # When the house last read this line. Zero means nobody has, which is where every
    # sentence starts and where it returns whenever the parent edits it.
    read_at: float = 0.0
    # What the house made of it. "HH:MM" when it could place the sentence in the day, and
    # empty when it could not; days of the week it applies to, empty meaning every day.
    at: str = ""
    days: tuple[str, ...] = ()
    # What the house needs to know before this can be a reminder. Empty when it does not.
    question: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "createdAt": self.created_at,
            "read": self.read_at > 0.0,
            "readAt": self.read_at,
            "at": self.at,
            "days": list(self.days),
            "question": self.question,
        }


@runtime_checkable
class SentenceStore(Protocol):
    def add(self, sentence: Sentence) -> Sentence: ...

    def list(self, household_id: str) -> list[Sentence]: ...

    def rewrite(self, household_id: str, sentence_id: str, text: str) -> Sentence: ...

    def remove(self, household_id: str, sentence_id: str) -> None: ...

    def record_reading(
        self,
        household_id: str,
        sentence_id: str,
        *,
        read_at: float,
        at: str,
        days: tuple[str, ...],
        question: str,
    ) -> Sentence: ...


@dataclass
class InMemorySentenceStore:
    _rows: dict[tuple[str, str], Sentence] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, sentence: Sentence) -> Sentence:
        with self._lock:
            self._rows[(sentence.household_id, sentence.id)] = sentence
        return sentence

    def list(self, household_id: str) -> list[Sentence]:
        with self._lock:
            rows = [
                row
                for (household, _), row in self._rows.items()
                if household == household_id
            ]
        return sorted(rows, key=lambda row: row.created_at)

    def rewrite(self, household_id: str, sentence_id: str, text: str) -> Sentence:
        with self._lock:
            current = self._rows[(household_id, sentence_id)]
            # A changed sentence is one nobody has read, and what the house made of the
            # old wording was made of words that are no longer there.
            updated = replace(
                current, text=text, read_at=0.0, at="", days=(), question=""
            )
            self._rows[(household_id, sentence_id)] = updated
            return updated

    def remove(self, household_id: str, sentence_id: str) -> None:
        with self._lock:
            self._rows.pop((household_id, sentence_id), None)

    def record_reading(
        self,
        household_id: str,
        sentence_id: str,
        *,
        read_at: float,
        at: str,
        days: tuple[str, ...],
        question: str,
    ) -> Sentence:
        with self._lock:
            current = self._rows[(household_id, sentence_id)]
            updated = replace(
                current, read_at=read_at, at=at, days=days, question=question
            )
            self._rows[(household_id, sentence_id)] = updated
            return updated


def clean_sentence(raw: str) -> str:
    """Normalise what the parent typed. Raises ValueError if it is not usable.

    Runs of whitespace collapse to one space and line breaks go with them. That is not a
    reading of the sentence: the words, their order and their spelling are untouched, and
    what comes back is what gets stored and what the panel shows, so there is still only
    one copy. A line break is removed because this text is handed to a model later, and a
    second line is the cheapest way to make one sentence look like a new instruction.
    """
    text = " ".join(raw.split())
    if not text:
        raise ValueError("a reminder needs some words")
    if len(text) > MAX_SENTENCE_LENGTH:
        raise ValueError(f"a reminder must be at most {MAX_SENTENCE_LENGTH} characters")
    if _CONTROL.search(text):
        raise ValueError("a reminder is written in ordinary characters")
    return text


def new_sentence_id() -> str:
    return f"rm_{secrets.token_hex(4)}"


def make_sentence(household_id: str, text: str, created_by: str) -> Sentence:
    return Sentence(
        id=new_sentence_id(),
        household_id=household_id,
        text=clean_sentence(text),
        created_at=time.time(),
        created_by=created_by,
    )


def clean_reading(at: Any, days: Any, question: Any) -> tuple[str, tuple[str, ...], str]:
    """Take what a model said about one sentence and keep only what is well formed.

    Nothing here raises. A model that answers oddly should cost a question to the parent,
    not a failed request for the whole household: an hour that is not an hour is dropped,
    a day that is not a day is dropped, and a sentence left with no hour is a sentence the
    house could not place — which is a real outcome and has a place to be shown.
    """
    hour = str(at or "").strip()
    when = hour if _CLOCK.match(hour) else ""

    chosen = {str(day or "").strip().lower()[:3] for day in _as_sequence(days)}
    on = tuple(day for day in DAYS if day in chosen)
    # Every day and all seven days are the same thing, and one of them is shorter to read.
    if len(on) == len(DAYS):
        on = ()

    asked = " ".join(str(question or "").split())
    asked = _CONTROL.sub("", asked)[:MAX_QUESTION_LENGTH]
    # A question about a sentence the house did place would be a question nobody can act
    # on: the parent would be asked to fix something that is not broken.
    return when, on, "" if when else asked


def _as_sequence(value: Any) -> Sequence[Any]:
    """A model may send one day rather than a list, and a string is not a list of days."""
    if isinstance(value, str) or not isinstance(value, Sequence):
        return [value] if value else []
    return value
