"""What the content is made of: interests, things to avoid, difficulty, variety, language.

These were a `LearnerProfile` written into the hub's code, so every piece of content
generated so far was tuned to a person who does not exist. They live here for the same
reason the rhythm does: the parent writes them, the hub reads them on its next run and
decides for itself, and saving them starts nothing.

What is stored is exactly the field list `LearnerProfile.prompt_hints()` returns. There is
no field here for a name or an id, and no route that carries one — not because the panel
may not hold one, but because nothing has needed it yet. Keeping the two lists identical is
what keeps household settings and person from dissolving into one text field.
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

# The name for the code, for anything that puts the choice into a sentence. "Write it in
# it." reads as a pronoun, and on 21 August 2026 that produced an afternoon in English for
# a household set to Italian — an instruction the model could only ignore.
LANGUAGE_NAMES = {"it": "Italian", "en": "English"}

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

# How many scripts should be waiting for the parent to decide about. The house writes one
# more whenever there are fewer, at any hour — writing one puts nothing in a room. Ten is
# enough for a sitting; the bounds keep a typing mistake from becoming a bill.
DEFAULT_SCRIPTS_WANTED = 10
MIN_SCRIPTS_WANTED = 0
MAX_SCRIPTS_WANTED = 30


@dataclass(frozen=True, slots=True)
class Preferences:
    """One household's content settings. No name, no id, no history — by construction."""

    household_id: str
    interests: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()
    difficulty: str = DEFAULT_DIFFICULTY
    variety: str = DEFAULT_VARIETY
    max_words_per_line: int = DEFAULT_WORDS_PER_LINE
    scripts_wanted: int = DEFAULT_SCRIPTS_WANTED
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
            "scriptsWanted": self.scripts_wanted,
            "language": self.language,
            "updatedAt": self.updated_at,
            "difficultyChoices": list(DIFFICULTY_CHOICES),
            "varietyChoices": list(VARIETY_CHOICES),
            "languageChoices": list(LANGUAGE_CHOICES),
            "wordsPerLineChoices": list(WORDS_PER_LINE_CHOICES),
            "minScriptsWanted": MIN_SCRIPTS_WANTED,
            "maxScriptsWanted": MAX_SCRIPTS_WANTED,
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
    scripts_wanted: Any = None,
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
    wanted = DEFAULT_SCRIPTS_WANTED if scripts_wanted is None else scripts_wanted
    if isinstance(wanted, bool) or not isinstance(wanted, int):
        raise ValueError("how many to keep waiting is a whole number")
    if not MIN_SCRIPTS_WANTED <= wanted <= MAX_SCRIPTS_WANTED:
        raise ValueError(
            f"how many to keep waiting must be between {MIN_SCRIPTS_WANTED} "
            f"and {MAX_SCRIPTS_WANTED}"
        )
    return Preferences(
        household_id=household_id,
        interests=_clean_list(interests, "the interests"),
        avoid=_clean_list(avoid, "the things to avoid"),
        difficulty=str(difficulty),
        variety=str(variety),
        max_words_per_line=int(max_words_per_line),
        scripts_wanted=int(wanted),
        language=str(language),
        updated_at=time.time(),
        updated_by=updated_by,
    )
