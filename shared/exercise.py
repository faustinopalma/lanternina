"""The exercise body a content agent produces, and how to read one.

The keys are English so that the household's content language stays a setting rather than
a property of the data. A sheet generated in English and one generated in Italian are the
same document with different words inside the same fields.

Bodies generated before 18 August 2026 carry Italian keys: ``titolo``, ``istruzioni``,
``esercizi``, ``domanda``, ``scelte``, ``risposta``, ``perche``. They are not rewritten,
and the choice is not a matter of taste. The safety seal covers ``body`` byte for byte and
the approval seal covers the payload that holds it, so renaming a key inside stored
content invalidates both, and re-sealing would mint an approval the parent never gave.
Readers therefore accept both spellings; generation asks for one. That costs this module
and a lookup per field, and it buys the survival of everything already approved.

The same fallback exists in TypeScript, in ``web/src/lib/sheet.ts``: the panel reads these
bodies too, and a body that renders on the display has to render there as well.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

TITLE: Final = "title"
INSTRUCTIONS: Final = "instructions"
EXERCISES: Final = "exercises"
QUESTION: Final = "question"
CHOICES: Final = "choices"
ANSWER: Final = "answer"
RATIONALE: Final = "rationale"

# Read only. Nothing writes an Italian key; these exist so that content approved before
# the rename still renders.
LEGACY_KEYS: Final[Mapping[str, str]] = {
    TITLE: "titolo",
    INSTRUCTIONS: "istruzioni",
    EXERCISES: "esercizi",
    QUESTION: "domanda",
    CHOICES: "scelte",
    ANSWER: "risposta",
    RATIONALE: "perche",
}


def field(body: Mapping[str, Any], name: str, default: Any = None) -> Any:
    """Read one field of an exercise body, or of one exercise inside it.

    ``name`` is one of the constants above; an unknown name raises `KeyError`, because a
    field this module does not know has no legacy spelling to fall back to.
    """
    if name in body:
        return body[name]
    return body.get(LEGACY_KEYS[name], default)
