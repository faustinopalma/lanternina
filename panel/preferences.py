"""What the content is made of: where to start, what to keep away from, what is true now.

These were a `LearnerProfile` written into the hub's code, so every piece of content
generated so far was tuned to a person who does not exist. They live here for the same
reason the rhythm does: the parent writes them, the hub reads them on its next run and
decides for itself, and saving them starts nothing.

Until 27 August 2026 the field list here was kept identical to the one
`LearnerProfile.prompt_hints()` returns, and that mirror was the reason this page could not
hold the thing a parent most wants to say. A household's steering is almost always about
*now*: a month full of school, a death in the family, a week when nothing long will land.
Shredded into keywords with no lifetime, those become permanent.

So the mirror is gone and what replaced it is narrower and truer: **there is no field for a
name or an id, and no route that carries one.** What is added instead is a note in the
parent's own words with an expiry, and the expiry is enforced by deleting it rather than by
flagging it — see :func:`still_standing`. A note that cannot outlive four weeks cannot
become a record of anybody.

**Three settings have left this page, and all three for the same reason.** The words per
line went on 27 August: how wide a line is on an 800×480 display is a fact about the
hardware, and asking a parent to know it was us handing them our job. The shape — *simple,
medium, harder* — and the variety went on 4 September. The shape asked a parent to say in
three steps how much a person can take, which is a verdict, and the system now works that
out from what comes back off the glass. The variety asked a question a parent could not
answer, because nobody knows what *one new detail* means before seeing an afternoon; it is
not a setting any more and it is not a default either — an afternoon travels as far from the
last ones as it can, always.

What a parent may still say about how much to ask for is the note, in their own words, and
it is taken as a circumstance rather than as a level. That is the whole of the replacement.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field, replace
from typing import Any, Protocol, runtime_checkable

# The languages the content agent can be asked to write in. It is the household's choice
# and it is not the parent's browser language: content approved in one language is not
# approved in another.
LANGUAGE_CHOICES = ("it", "en")

# The name for the code, for anything that puts the choice into a sentence. "Write it in
# it." reads as a pronoun, and on 21 August 2026 that produced an afternoon in English for
# a household set to Italian — an instruction the model could only ignore.
LANGUAGE_NAMES = {"it": "Italian", "en": "English"}

# A line on the e-paper display is about eight words wide at the size it is read at. It is
# a constant of the hardware and no longer a question for a parent.
WORDS_PER_LINE = 6

# Free text a person reads back and edits. Eighty characters used to be the bound, which
# fitted "i ragni" and not "i ragni, e nemmeno disegnati" — so what was stored was a tag and
# the reason for it was lost. Two hundred fits the reason, and the reason is the part that
# steers.
MAX_ENTRY_LENGTH = 200
MAX_ENTRIES = 12

# The note is one paragraph, not a page: it goes into a prompt beside everything else, and a
# standing instruction that outweighs the rest of the prompt is a different kind of thing.
MAX_NOTE_LENGTH = 600

# How long a note stands before it is deleted. Renewable, and short enough that a parent who
# forgets it exists is not still steering with something they wrote in another season. Four
# weeks is roughly the horizon of the things this is for — a school term's worst month, a
# convalescence, a house being packed up.
NOTE_LASTS_SECONDS = 28 * 24 * 60 * 60

# How many sheets may be on the table at one time. A ceiling, never a target: the number an
# afternoon actually needs at any moment is usually one, and a second page is right when one
# page would have to carry two different things. Two is the default because a page that has
# to carry everything is the page nobody reads, and three is the top because an encyclopedia
# handed over in one go is the other failure. `docs/EVIDENCE.md §2` has the measurements.
#
# This is not a budget for the whole afternoon, and until 28 August 2026 the check read it
# as one. A three-hour afternoon that hands something over, takes it back and hands over the
# next thing spends four sheets and never crowds the table, and refusing it was reading the
# parent's answer as the answer to a question they were not asked.
SHEETS_CHOICES = (1, 2, 3)
DEFAULT_SHEETS = 2

DEFAULT_LANGUAGE = "it"


@dataclass(frozen=True, slots=True)
class Preferences:
    """One household's content settings. No name, no id, no history — by construction."""

    household_id: str
    interests: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()
    language: str = DEFAULT_LANGUAGE
    sheets: int = DEFAULT_SHEETS
    # What is true in this house at the moment, in the parent's own words, and the instant
    # it stops being true. Empty is the ordinary state.
    note: str = ""
    note_until: float = 0.0
    updated_at: float = 0.0
    updated_by: str = ""

    def standing(self, now: float) -> str:
        """The note if it is still true, and an empty string once it is not.

        Every reader goes through here rather than through the field, so an expired note
        cannot reach a prompt by somebody forgetting to check the date.
        """
        return self.note if self.note and now < self.note_until else ""

    def forgetting_what_expired(self, now: float) -> Preferences:
        """The same settings with a lapsed note removed rather than kept and ignored.

        Kept-and-ignored would leave a sentence about a hard month sitting in the store for
        as long as the household exists. Deleting it is what makes "this cannot become a
        record of anybody" a property of the data and not of the code that reads it.
        """
        if not self.note or now < self.note_until:
            return self
        return replace(self, note="", note_until=0.0)

    def to_public(self, now: float | None = None) -> dict[str, Any]:
        moment = time.time() if now is None else now
        return {
            "interests": list(self.interests),
            "avoid": list(self.avoid),
            "language": self.language,
            "sheets": self.sheets,
            "note": self.standing(moment),
            "noteUntil": self.note_until if self.standing(moment) else 0.0,
            "updatedAt": self.updated_at,
            "languageChoices": list(LANGUAGE_CHOICES),
            "sheetsChoices": list(SHEETS_CHOICES),
            "noteLastsDays": NOTE_LASTS_SECONDS // (24 * 60 * 60),
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
            stored = self._rows.get(household_id, Preferences(household_id=household_id))
            standing = stored.forgetting_what_expired(time.time())
            if standing is not stored:
                self._rows[household_id] = standing
            return standing

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


def _clean_note(raw: Any) -> str:
    """The one place a parent writes more than a line. Paragraph breaks survive as spaces.

    Same treatment as an entry and for the same reason: this reaches a prompt as material,
    quoted as JSON, and a newline is the cheapest way to make one line of it look like a new
    instruction.
    """
    if raw is None:
        return ""
    if not isinstance(raw, str):
        raise ValueError("the note is written in words")
    note = " ".join(raw.split())
    if len(note) > MAX_NOTE_LENGTH:
        raise ValueError(f"the note must be at most {MAX_NOTE_LENGTH} characters")
    return note


def clean_preferences(
    household_id: str,
    *,
    interests: Any,
    avoid: Any,
    language: Any,
    sheets: Any = DEFAULT_SHEETS,
    note: Any = "",
    now: float | None = None,
    updated_by: str = "",
) -> Preferences:
    """Normalise what the parent chose. Raises ValueError if it cannot be honoured."""
    moment = time.time() if now is None else now
    if language not in LANGUAGE_CHOICES:
        raise ValueError(f"the language must be one of {list(LANGUAGE_CHOICES)}")
    if sheets not in SHEETS_CHOICES:
        raise ValueError(f"the number of sheets must be one of {list(SHEETS_CHOICES)}")
    standing = _clean_note(note)
    return Preferences(
        household_id=household_id,
        interests=_clean_list(interests, "the interests"),
        avoid=_clean_list(avoid, "the things to avoid"),
        language=str(language),
        sheets=int(sheets),
        note=standing,
        # Saving the note again is how it is renewed: there is no separate button, because
        # a parent editing what is true now has already said it is still true.
        note_until=moment + NOTE_LASTS_SECONDS if standing else 0.0,
        updated_at=moment,
        updated_by=updated_by,
    )
