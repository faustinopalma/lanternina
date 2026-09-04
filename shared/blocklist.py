"""What an afternoon does not say, in one place because it is checked twice.

`ideas/09 §7` puts a filter at two different times, and they have to hold the same rules or
they are two policies. Before an afternoon is saved, every written word in the document is
checked against this and a document that fails is repaired rather than stored. While the
afternoon runs, every string heading for a display or a printer is checked against the
same rules, and one that fails is replaced by the text already written in the plan.

**This used to be a list of 78 literal phrases.** It caught the common failures for
nothing, and it also refused `errore` in a sentence about a draughtsman dead for fifty
years (`ideas/10 §11`), `livello` in *the water level*, `vittoria` in any account of a
battle, and `mamma` and `papà` everywhere at once — which took the family out of fiction in
order to keep one fact out of it. The concern was never the vocabulary. It was **who the
sentence is about**.

So the rules are patterns with a person in them. What is refused is the second person
carrying a judgement — *hai sbagliato*, *sei stato bravo*, *il tuo punteggio* — and the
machine speaking about its own operation to the reader — *ho semplificato*, *tuo padre ha
scelto*, *ti restano dieci minuti*. A ledger may contain an error, a keeper may leave in a
hurry, a battle may be won, and a grandmother may write a letter.

Five groups, and the reason each is here is the same reason stated five ways: none of them
is about the words being unpleasant. They are the ways a text stops being the thing
somebody is doing and becomes a remark about them, or about the machine.

* **Praise and blame** turn an afternoon into an assessment. Praise is a verdict with a
  friendly face, and it is a verdict only when it is addressed to somebody.
* **Hurry** is a countdown by another name. Nothing here can be failed, and nothing can be
  failed for being slow either — which is about telling the reader to be quick, not about a
  character who hurried.
* **Score** is the field this project must never grow, appearing as a sentence instead of
  as a column. A tally inside the story is not that; *your score* is.
* **The machinery** is the one that is easy to lose. A text that tells the person that
  something was adapted, shortened or chosen for them says that a decision was made about
  them behind the afternoon. `ideas/09 §8` is emphatic that the parent's channel must never
  be revealed; this is where that becomes code.

**A sixth group arrived on 4 September 2026 and it is the one with the most behind it.**
Since that date the prompt of the model that devises an afternoon, and of the model that
writes the rest of one, carries a pitch: where this house sits on three axes, worked out
from what came back off the glass. `docs/NON-GOALS.md` allows that and refuses one thing
about it — that it may never surface in anything a person reads — and says in as many words
that a review gate is what enforces it rather than the prompt asking nicely. **Fitted** is
that gate: a sentence telling the reader the afternoon was sized for them, or referring to
how their last one went. It is the narrowest family here, because second person with a past
tense is most of the dialogue in most fiction, so each pattern has to carry the sizing
itself — *pensato apposta per te*, *più facile del solito*, *l'ultima volta hai* — and never
the mere fact of somebody being addressed.

**What this is not.** It is not a safety classifier, and it does not replace
:mod:`orchestrator.safety` — that gate looks for harm, this looks for who a sentence is
about. Nor is it a guarantee: a model can write a verdict without matching any pattern
here. What patterns buy over a word list is that the false refusals fall where nobody meant
to write, instead of falling on half the nouns in the language.

The patterns are Italian first because that is what the house speaks, with the English
equivalents beside them because the prompts, the tests and half the repository are in
English and a model asked for Italian will occasionally answer in both.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class Why(StrEnum):
    """Which of the six reasons a sentence is refused."""

    PRAISE = "praise"
    BLAME = "blame"
    HURRY = "hurry"
    SCORE = "score"
    MACHINERY = "machinery"
    FITTED = "fitted"


# Written against folded text: lower case, accents removed, single spaces. Every pattern
# carries the person it is about, because that is the thing being refused.
_RULES: Final[tuple[tuple[Why, str], ...]] = (
    # praise: a judgement handed to the reader
    (Why.PRAISE, r"\b(sei|eri|sarai) (stat[oa] )?(brav\w*|perfett\w+|eccellente|fantastic\w+)\b"),
    # A vocative: "bravo," and "bravo!" are addressed to somebody, "un bravo falegname" is not.
    (Why.PRAISE, r"\bbrav[oaie]\w*\s*[,!]"),
    (Why.PRAISE, r"^brav\w*\b"),
    (Why.PRAISE, r"^(brav\w*|perfetto|eccellente|fantastico|ottimo)\s*[!.]?$"),
    (Why.PRAISE, r"\b(brav\w*|perfetto|eccellente|fantastico|ottimo)\s*!"),
    (Why.PRAISE, r"(^|[.!?] )(perfetto|eccellente|fantastico|ottimo)\s*,"),
    (Why.PRAISE, r"\bcomplimenti\b"),
    (Why.PRAISE, r"\b(ottimo|bel) lavoro\b"),
    (Why.PRAISE, r"\bben fatto\b"),
    (Why.PRAISE, r"\b(hai|avete) fatto (benissimo|un ottimo lavoro)\b"),
    (Why.PRAISE, r"\b(well done|good job|nicely done|you did (great|well))\b"),
    # blame: the same thing with the sign turned round
    (Why.BLAME, r"\b(hai|avete|ha) sbagliat\w+\b"),
    (Why.BLAME, r"\b(hai|avete) (fatto|commesso) un errore\b"),
    (Why.BLAME, r"\bnon (hai|avete) (capito|fatto bene|indovinato)\b"),
    (Why.BLAME, r"\b(la tua|questa) risposta (e |non e )?(sbagliat\w+|errat\w+)\b"),
    (Why.BLAME, r"\briprova\b"),
    (Why.BLAME, r"\bnon e (quello|quella) (giusto|giusta)\b"),
    (Why.BLAME, r"\b(you are|you're|that is|that's) wrong\b"),
    (Why.BLAME, r"\btry again\b"),
    # hurry: told to the reader, not narrated about somebody
    (Why.HURRY, r"\b(sbrigati|affrettati|sbrigatevi|affrettatevi)\b"),
    (Why.HURRY, r"\bfai (in fretta|veloce|presto)\b"),
    (Why.HURRY, r"\b(piu|il piu) (veloce|in fretta) possibile\b"),
    (Why.HURRY, r"\b(hai|avete) (solo )?\d+ (minuti|secondi)\b"),
    (Why.HURRY, r"\btempo scaduto\b"),
    (Why.HURRY, r"\bconto alla rovescia\b"),
    (Why.HURRY, r"\b(hurry up|be quick|as fast as you can|time is up|countdown)\b"),
    # score: a number about the reader
    (Why.SCORE, r"\b(hai|avete) (vinto|perso|totalizzato|guadagnato)\b"),
    (Why.SCORE, r"\b(il )?tuo (punteggio|voto|record|livello|risultato)\b"),
    (Why.SCORE, r"\b(punteggio|voto) finale\b"),
    (Why.SCORE, r"\b(hai|avete) (fatto|ottenuto) \d+ punti\b"),
    (Why.SCORE, r"\bsei (al|in) (primo|secondo|terzo|\d+)[o]? (posto|livello)\b"),
    (Why.SCORE, r"\b(your (score|level|rank)|you (win|lose|won|lost)|leaderboard)\b"),
    # machinery: the system, and the channel behind it
    (Why.MACHINERY, r"\b(ho|abbiamo) (adattato|semplificato|accorciato|abbreviato)\b"),
    (Why.MACHINERY, r"\b(ho|abbiamo|ha) (scelto|deciso|preparato) per te\b"),
    (Why.MACHINERY, r"\b(questo|il) (sistema|programma|modello|computer) (ha|ti|sa|decide)\b"),
    (Why.MACHINERY, r"\bintelligenza artificiale\b"),
    (
        Why.MACHINERY,
        r"\b(tuo|tua|i tuoi) (padre|madre|genitori)\b[^.]{0,40}?"
        r"\b(ha|hanno) (scelto|deciso|impostato|chiesto|preparato|voluto)\b",
    ),
    (
        Why.MACHINERY,
        r"\b(mamma|papa|il genitore)\b[^.]{0,40}?"
        r"\b(ha|hanno) (scelto|deciso|impostato|preparato)\b",
    ),
    (Why.MACHINERY, r"\bti (restano|rimangono)\b"),
    (Why.MACHINERY, r"\b(tempo riman\w+|tempo rimasto|minuti rimasti)\b"),
    (Why.MACHINERY, r"\b(the (system|model) (has|chose|decided)|your parent (chose|set))\b"),
    (Why.MACHINERY, r"\b(shortened|simplified|adapted) (it )?for you\b"),
    # fitted: the afternoon telling the reader it was sized for them. The narrowest family
    # here on purpose — second person plus a past tense is most of the dialogue in most
    # fiction, so every pattern has to carry the sizing itself and not merely the address.
    (
        Why.FITTED,
        r"\b(pensat|fatt|scelt|preparat|adattat|studiat|costruit|cucit)\w* "
        r"(apposta |proprio |su misura )?per te\b",
    ),
    (Why.FITTED, r"\b(su misura|a (tua )?misura) per te\b"),
    (
        Why.FITTED,
        r"\b(piu|meno) (facile|difficile|semplice|lungo|corto|impegnativ\w+|complicat\w+) "
        r"(per te|del solito|dell'? ?ultima volta|di quello di ieri)\b",
    ),
    (Why.FITTED, r"\b(l'? ?ultima|la scorsa) volta [^.!?]{0,40}\b(hai|avevi|sei|eri)\b"),
    (Why.FITTED, r"\b(hai|avevi) (gia )?(fatto|visto|provato) qualcosa (del genere|di simile)\b"),
    (Why.FITTED, r"\bormai (lo )?(sai|conosci|ci riesci)\b"),
    (Why.FITTED, r"\b(sei|ormai sei) (ormai )?pront\w+ (per|a)\b"),
    (Why.FITTED, r"\b(al|per il|adatto al) tuo livello\b"),
    (Why.FITTED, r"\b(questa volta|oggi) (e |sara )?(piu|meno) (facile|difficile|semplice)\b"),
    (Why.FITTED, r"\b(made|chosen|picked|designed|written|built) (just )?for you\b"),
    (Why.FITTED, r"\blast time you\b"),
    (Why.FITTED, r"\byou (already )?(know|can do) this (one|by now)\b"),
    (Why.FITTED, r"\byou'? ?(are|re) ready (for|to)\b"),
    (Why.FITTED, r"\b(at|for) your level\b"),
    (Why.FITTED, r"\bthis (one|time) is (easier|harder|shorter|longer)\b"),
)

# Accents are folded away before matching, so "papà" is caught by "papa" and a model that
# drops an accent does not slip through a rule written with one.
_ACCENTS: Final = str.maketrans("àáâäèéêëìíîïòóôöùúûüç", "aaaaeeeeiiiioooouuuuc")


@dataclass(frozen=True, slots=True)
class Blocked:
    """One thing found, and why it is refused.

    ``phrase`` is the text that actually matched rather than the rule that matched it, so a
    repair request names something the writer can find in their own sentence.
    """

    phrase: str
    why: Why

    def __str__(self) -> str:
        return f"{self.phrase!r} ({self.why})"


def fold(text: str) -> str:
    """Text as it is compared: lower case, no accents, single spaces."""
    return " ".join(text.lower().translate(_ACCENTS).split())


_COMPILED: Final[tuple[tuple[re.Pattern[str], Why], ...]] = tuple(
    (re.compile(pattern), why) for why, pattern in _RULES
)


def blocked_in(text: str) -> tuple[Blocked, ...]:
    """Everything here that is a remark about the reader. Empty means it may be said.

    All of them rather than the first, because at devise time the answer is handed to a
    model to repair and one thing at a time is one round trip per phrase.
    """
    folded = fold(text)
    seen: dict[str, Blocked] = {}
    for pattern, why in _COMPILED:
        for match in pattern.finditer(folded):
            found = match.group(0).strip()
            seen.setdefault(found, Blocked(phrase=found, why=why))
    return tuple(seen.values())
