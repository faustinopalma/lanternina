"""Editable activity guidance, separate from safety and equipment constraints."""

from __future__ import annotations

import json
from dataclasses import dataclass

from shared.prompts import beside

MAX_GUIDANCE_CHARS = 6000
MAX_SUMMARY_CHARS = 3000
SAYS = beside(__file__)


def defaults(language: str = "it") -> tuple[str, str]:
    chosen = language if language in {"it", "en"} else "it"
    return SAYS.text(f"default-{chosen}").strip(), SAYS.text(f"adaptive-{chosen}").strip()


def clean_text(value: object, limit: int) -> str:
    if not isinstance(value, str):
        raise ValueError("guidance must be text")
    text = value.strip()
    if len(text) > limit:
        raise ValueError(f"guidance must be at most {limit} characters")
    if any(ord(character) < 32 and character not in "\n\r\t" for character in text):
        raise ValueError("guidance contains control characters")
    return text


@dataclass(frozen=True, slots=True)
class Steering:
    instructions: str
    adaptive: str
    conduct: str = ""
    review: str = ""

    @classmethod
    def initial(cls, language: str = "it") -> Steering:
        chosen = language if language in {"it", "en"} else "it"
        return cls(
            *defaults(chosen),
            conduct=SAYS.text(f"conduct-{chosen}").strip(),
            review=SAYS.text(f"review-{chosen}").strip(),
        )

    def as_material(self) -> str:
        return json.dumps(
            {
                "parentInstructions": self.instructions,
                "conductInstructions": self.conduct,
                "reviewInstructions": self.review,
                "feedbackGuidance": self.adaptive,
            },
            ensure_ascii=False,
        )


def for_prompt(steering: Steering | None = None, language: str = "it") -> str:
    chosen = "en" if language.lower() in {"en", "english"} else "it"
    value = steering if steering is not None else Steering.initial(chosen)
    return SAYS.text("context", guidance=value.as_material())
