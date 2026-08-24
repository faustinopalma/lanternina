"""Words an afternoon does not say, in one place because it is checked twice.

`ideas/09 §7` puts a filter at two different times, and they have to hold the same list or
they are two policies. Before an afternoon is saved, every written word in the document is
checked against this and a document that fails is repaired rather than stored. While the
afternoon runs, every string heading for a display or a printer is checked against the same
list, and one that fails is replaced by the text already written in the plan.

Five groups, and the reason each is here is the same reason stated five ways: none of them
is about the words being unpleasant. They are the ways a text stops being the thing
somebody is doing and becomes a remark about them, or about the machine.

* **Praise and blame** turn an afternoon into an assessment. "Nothing the system states is
  a verdict about a person" is a rule of this project, and praise is a verdict with a
  friendly face.
* **Hurry** is a countdown by another name. Nothing here can be failed, and nothing can be
  failed for being slow either.
* **Score** is the field this project must never grow, appearing as a sentence instead of
  as a column.
* **The machinery** is the one that is easy to lose. A text that mentions adapting,
  shortening, the time left, the parent, the system or the model tells the person that
  something was decided about them behind the afternoon. `ideas/09 §8` is emphatic that
  the parent's channel must never be revealed; this is where that becomes code.

**What this is not.** It is not a safety classifier, and it does not replace
:mod:`orchestrator.safety` — that gate looks for harm, this list looks for tone. Nor is it
a guarantee: a model can write a verdict without using any of these words. What a list of
literal phrases buys is that the *common* failure is caught for nothing, at both times,
with no model call. What it costs is false refusals — "veloce" is a fine word for a cloud
— and the cost is bounded by where the refusals land: at devise time a repair round, at
run time the pre-written text.

The phrases are Italian first because that is what the house speaks, with the English
equivalents beside them because the prompts, the tests and half the repository are in
English and a model asked for Italian will occasionally answer in both.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class Why(StrEnum):
    """Which of the five reasons a phrase is on the list."""

    PRAISE = "praise"
    BLAME = "blame"
    HURRY = "hurry"
    SCORE = "score"
    MACHINERY = "machinery"


# Phrases, not stems. A stem catches more and explains less: "brav" would refuse
# "bravata", and the refusal a repair loop reads back has to name something a person can
# find in their own text.
_LIST: Final[tuple[tuple[Why, str], ...]] = (
    (Why.PRAISE, "bravo"),
    (Why.PRAISE, "brava"),
    (Why.PRAISE, "bravissimo"),
    (Why.PRAISE, "bravissima"),
    (Why.PRAISE, "complimenti"),
    (Why.PRAISE, "ottimo lavoro"),
    (Why.PRAISE, "ben fatto"),
    (Why.PRAISE, "perfetto"),
    (Why.PRAISE, "eccellente"),
    (Why.PRAISE, "fantastico"),
    (Why.PRAISE, "sei stato bravo"),
    (Why.PRAISE, "well done"),
    (Why.PRAISE, "good job"),
    (Why.PRAISE, "excellent"),
    (Why.PRAISE, "perfect"),
    (Why.BLAME, "sbagliato"),
    (Why.BLAME, "sbagliata"),
    (Why.BLAME, "hai sbagliato"),
    (Why.BLAME, "errore"),
    (Why.BLAME, "errato"),
    (Why.BLAME, "riprova"),
    (Why.BLAME, "non va bene"),
    (Why.BLAME, "peccato"),
    (Why.BLAME, "wrong"),
    (Why.BLAME, "mistake"),
    (Why.BLAME, "try again"),
    (Why.HURRY, "sbrigati"),
    (Why.HURRY, "affrettati"),
    (Why.HURRY, "fai in fretta"),
    (Why.HURRY, "in fretta"),
    (Why.HURRY, "fai veloce"),
    (Why.HURRY, "il piu veloce possibile"),
    (Why.HURRY, "tempo scaduto"),
    (Why.HURRY, "conto alla rovescia"),
    (Why.HURRY, "hurry"),
    (Why.HURRY, "quickly"),
    (Why.HURRY, "time is up"),
    (Why.HURRY, "countdown"),
    (Why.SCORE, "punteggio"),
    (Why.SCORE, "punti"),
    (Why.SCORE, "classifica"),
    (Why.SCORE, "record"),
    (Why.SCORE, "hai vinto"),
    (Why.SCORE, "hai perso"),
    (Why.SCORE, "vittoria"),
    (Why.SCORE, "sconfitta"),
    (Why.SCORE, "voto"),
    (Why.SCORE, "livello"),
    (Why.SCORE, "premio"),
    (Why.SCORE, "score"),
    (Why.SCORE, "points"),
    (Why.SCORE, "you win"),
    (Why.SCORE, "you lose"),
    (Why.SCORE, "leaderboard"),
    (Why.MACHINERY, "il sistema"),
    (Why.MACHINERY, "il modello"),
    (Why.MACHINERY, "intelligenza artificiale"),
    (Why.MACHINERY, "il computer"),
    (Why.MACHINERY, "il programma"),
    (Why.MACHINERY, "ho adattato"),
    (Why.MACHINERY, "adattato"),
    (Why.MACHINERY, "semplificato"),
    (Why.MACHINERY, "accorciato"),
    (Why.MACHINERY, "abbreviato"),
    (Why.MACHINERY, "tempo rimasto"),
    (Why.MACHINERY, "tempo rimanente"),
    (Why.MACHINERY, "minuti rimasti"),
    (Why.MACHINERY, "tuo padre"),
    (Why.MACHINERY, "tua madre"),
    (Why.MACHINERY, "i tuoi genitori"),
    (Why.MACHINERY, "il genitore"),
    (Why.MACHINERY, "mamma"),
    (Why.MACHINERY, "papa"),
    (Why.MACHINERY, "the system"),
    (Why.MACHINERY, "the model"),
    (Why.MACHINERY, "your parent"),
    (Why.MACHINERY, "time left"),
    (Why.MACHINERY, "shortened"),
    (Why.MACHINERY, "adapted"),
)

# Accents are folded away before matching, so "papà" is caught by "papa" and a model that
# drops an accent does not slip through a list written with one.
_ACCENTS: Final = str.maketrans("àáâäèéêëìíîïòóôöùúûüç", "aaaaeeeeiiiioooouuuuc")


@dataclass(frozen=True, slots=True)
class Blocked:
    """One phrase found, and why it is on the list."""

    phrase: str
    why: Why

    def __str__(self) -> str:
        return f"{self.phrase!r} ({self.why})"


def fold(text: str) -> str:
    """Text as it is compared: lower case, no accents, single spaces."""
    return " ".join(text.lower().translate(_ACCENTS).split())


def _pattern(phrase: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w]){re.escape(phrase)}(?![\w])")


_COMPILED: Final[tuple[tuple[re.Pattern[str], Blocked], ...]] = tuple(
    (_pattern(phrase), Blocked(phrase=phrase, why=why)) for why, phrase in _LIST
)


def blocked_in(text: str) -> tuple[Blocked, ...]:
    """Every phrase from the list this text uses. Empty means it may be said.

    All of them rather than the first, because at devise time the answer is handed to a
    model to repair and one phrase at a time is one round trip per word.
    """
    folded = fold(text)
    found = [entry for pattern, entry in _COMPILED if pattern.search(folded)]
    # Deduplicated on the phrase: the same word twice in a paragraph is one thing to fix.
    seen: dict[str, Blocked] = {}
    for entry in found:
        seen.setdefault(entry.phrase, entry)
    return tuple(seen.values())
