"""What the content is made of: interests, things to avoid, difficulty, variety, language.

These were a `LearnerProfile` written into the hub's code, so every piece of content
generated so far was tuned to a person who does not exist. They live here for the same
reason the rhythm does: the parent writes them, the hub reads them on its next run and
decides for itself, and saving them starts nothing.

What is stored is exactly the redacted subset `LearnerProfile.prompt_hints()` lets out of
the device. There is no field here for a name or an id, and no route that could carry
one: the hub holds them and never sends them up. Keeping the field list identical is what
keeps the separation between household and person from dissolving into a text field.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from shared.domain import ContentVariety, Difficulty

DIFFICULTY_CHOICES = tuple(str(value) for value in Difficulty)
VARIETY_CHOICES = tuple(str(value) for value in ContentVariety)

# The languages the content agent can be asked to write in. It is the household's choice
# and it is not the parent's browser language: content approved in one language is not
# approved in another.
LANGUAGE_CHOICES = ("it", "en")

# A line on the e-paper display is about eight words wide at the size it is read at, so
# anything above that would be a setting the hardware cannot honour.
WORDS_PER_LINE_CHOICES = (3, 4, 5, 6, 7, 8)

# Free text a person reads back and edits. The bound is what keeps one entry from becoming
# a paragraph of instructions inside a prompt.
MAX_ENTRY_LENGTH = 80
MAX_ENTRIES = 12

DEFAULT_DIFFICULTY = str(Difficulty.GENTLE)
DEFAULT_VARIETY = str(ContentVariety.BALANCED)
DEFAULT_LANGUAGE = "it"
DEFAULT_WORDS_PER_LINE = 6


@dataclass(frozen=True, slots=True)
class Preferences:
    """One household's content settings. No name, no id, no history — by construction."""

    household_id: str
    interests: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()
    difficulty: str = DEFAULT_DIFFICULTY
    variety: str = DEFAULT_VARIETY
    max_words_per_line: int = DEFAULT_WORDS_PER_LINE
    language: str = DEFAULT_LANGUAGE
    updated_at: float = 0.0
    updated_by: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "interests": list(self.interests),
            "avoid": list(self.avoid),
            "difficulty": self.difficulty,
            "variety": self.variety,
            "maxWordsPerLine": self.max_words_per_line,
            "language": self.language,
            "updatedAt": self.updated_at,
            "difficultyChoices": list(DIFFICULTY_CHOICES),
            "varietyChoices": list(VARIETY_CHOICES),
            "languageChoices": list(LANGUAGE_CHOICES),
            "wordsPerLineChoices": list(WORDS_PER_LINE_CHOICES),
        }


@runtime_checkable
class PreferencesStore(Protocol):
    def get(self, household_id: str) -> Preferences: ...

    def set(self, preferences: Preferences) -> Preferences: ...


@dataclass
class InMemoryPreferencesStore:
    _rows: dict[str, Preferences] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get(self, household_id: str) -> Preferences:
        with self._lock:
            # A household that has never chosen gets the defaults, not an error: the hub
            # has to be able to generate before anyone has opened the panel.
            return self._rows.get(household_id, Preferences(household_id=household_id))

    def set(self, preferences: Preferences) -> Preferences:
        with self._lock:
            self._rows[preferences.household_id] = preferences
            return preferences


def _clean_entry(raw: Any) -> str:
    """Free text from a person ends up in a model prompt, so newlines go here: they are
    the cheapest way to make one line of a prompt look like a new instruction."""
    if not isinstance(raw, str):
        raise ValueError("interests and things to avoid are written in words")
    entry = " ".join(raw.split())
    if len(entry) > MAX_ENTRY_LENGTH:
        raise ValueError(f"each entry must be at most {MAX_ENTRY_LENGTH} characters")
    return entry


def _clean_list(raw: Any, name: str) -> tuple[str, ...]:
    if isinstance(raw, str) or not isinstance(raw, (list, tuple)):
        raise ValueError(f"{name} is a list")
    entries = tuple(cleaned for cleaned in (_clean_entry(item) for item in raw) if cleaned)
    if len(entries) > MAX_ENTRIES:
        raise ValueError(f"{name} can hold at most {MAX_ENTRIES} entries")
    return entries


def clean_preferences(
    household_id: str,
    *,
    interests: Any,
    avoid: Any,
    difficulty: Any,
    variety: Any,
    max_words_per_line: Any,
    language: Any,
    updated_by: str = "",
) -> Preferences:
    """Normalise what the parent chose. Raises ValueError if it cannot be honoured."""
    if difficulty not in DIFFICULTY_CHOICES:
        raise ValueError(f"the difficulty must be one of {list(DIFFICULTY_CHOICES)}")
    if variety not in VARIETY_CHOICES:
        raise ValueError(f"the variety must be one of {list(VARIETY_CHOICES)}")
    if language not in LANGUAGE_CHOICES:
        raise ValueError(f"the language must be one of {list(LANGUAGE_CHOICES)}")
    if isinstance(max_words_per_line, bool) or max_words_per_line not in WORDS_PER_LINE_CHOICES:
        raise ValueError(f"the words per line must be one of {list(WORDS_PER_LINE_CHOICES)}")
    return Preferences(
        household_id=household_id,
        interests=_clean_list(interests, "the interests"),
        avoid=_clean_list(avoid, "the things to avoid"),
        difficulty=str(difficulty),
        variety=str(variety),
        max_words_per_line=int(max_words_per_line),
        language=str(language),
        updated_at=time.time(),
        updated_by=updated_by,
    )
