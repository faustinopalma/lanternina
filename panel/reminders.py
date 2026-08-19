"""What the parent wants remembered, written the way they would say it.

A sentence here is not a reminder yet. It is what somebody typed — "lavarsi i denti dopo
cena", "mercoledì porta fuori il bidone" — kept exactly as they wrote it and marked as not
yet read.

The marking is the whole point, and it comes from a rule rather than from a preference. A
write from the panel is inert: it may persist state and nothing else, so the panel cannot
ask a model what a sentence means at the moment the sentence is typed. What it can do is
say that nobody has looked yet. The house asks later, on the timer it already has, and the
reading happens inside the answer to that request.

So this module holds only the parent's half. Nothing here interprets, schedules or shows
anything, and a sentence that will never become a reminder is indistinguishable from one
that will until the house has been asked.
"""

from __future__ import annotations

import re
import secrets
import threading
import time
from dataclasses import dataclass, field, replace
from typing import Any, Protocol, runtime_checkable

# Long enough for a sentence with a day and an hour in it, short enough that the box is
# plainly not for writing paragraphs in.
MAX_SENTENCE_LENGTH = 200

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


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

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "createdAt": self.created_at,
            "read": self.read_at > 0.0,
            "readAt": self.read_at,
        }


@runtime_checkable
class SentenceStore(Protocol):
    def add(self, sentence: Sentence) -> Sentence: ...

    def list(self, household_id: str) -> list[Sentence]: ...

    def rewrite(self, household_id: str, sentence_id: str, text: str) -> Sentence: ...

    def remove(self, household_id: str, sentence_id: str) -> None: ...


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
            updated = replace(current, text=text, read_at=0.0)
            self._rows[(household_id, sentence_id)] = updated
            return updated

    def remove(self, household_id: str, sentence_id: str) -> None:
        with self._lock:
            self._rows.pop((household_id, sentence_id), None)


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
