"""Every instruction this system gives a model, printed as the model receives it.

The prompts are Python because two of them are generated from the format's own constants
and the rest carry the record of what was measured to arrive at them — see the module
docstring of `shared/experience_prompt.py` for the first and the comment above
`agents/experience_wording._VARIETY` for the second. That is a defensible place for them
to live and a bad place to read them from, so this prints them out.

Nothing here has a copy of anything. Each line is read from the module that sends it, so a
prompt changed in the code is changed here on the next run and cannot drift out of date.

    python -m tools.prompts               # what there is, and how big
    python -m tools.prompts deviser       # one of them, whole
    python -m tools.prompts --all         # all of them, whole
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Instruction:
    """One standing instruction, and what is added to it at the moment it is sent."""

    name: str
    sends: str
    text: str
    # What the caller appends per call. Named rather than shown, because it is the
    # household's own material and this file must not have any.
    then: str


def every_instruction() -> list[Instruction]:
    from agents import (
        experience_continuer,
        experience_deviser,
        page_maker,
        page_reader,
        reminder_reader,
        reminder_wording,
    )
    from panel import painting
    from panel.guidelines import FIXED

    return [
        Instruction(
            "deviser",
            "agents/experience_deviser.py :: _INSTRUCTION",
            experience_deviser._INSTRUCTION,
            "the language, what this house can do, the parent's interests and things to "
            "avoid, the titles already offered, and what those were drawn along",
        ),
        Instruction(
            "continuer",
            "agents/experience_continuer.py :: with_bounds()",
            experience_continuer.with_bounds(FIXED, "<what this household wrote>"),
            "the afternoon so far and what came back on the page",
        ),
        Instruction(
            "page-reader",
            "agents/page_reader.py :: _INSTRUCTION",
            page_reader._INSTRUCTION,
            "two images: the sheet as printed and the sheet as it came back",
        ),
        Instruction(
            "page-maker",
            "agents/page_maker.py :: asked_for()",
            page_maker._HOW_IT_IS_DRAWN + page_maker._ONLY_THESE_WORDS,
            "what kind of object the paper is, which room it is drawn for, and the words "
            "that must appear on it",
        ),
        Instruction(
            "reminder-reader",
            "agents/reminder_reader.py :: _INSTRUCTION",
            reminder_reader._INSTRUCTION,
            "the sentences the parent typed",
        ),
        Instruction(
            "reminder-bank",
            "agents/reminder_wording.py :: _INSTRUCTION",
            reminder_wording._INSTRUCTION,
            "the hour and the sentence",
        ),
        Instruction(
            "reminder-now",
            "agents/reminder_wording.py :: _NOW + _SUBJECT",
            reminder_wording._NOW + reminder_wording._SUBJECT,
            "the hour and the sentence",
        ),
        Instruction(
            "picture",
            "panel/painting.py :: PICTURE_PROMPT",
            painting.PICTURE_PROMPT,
            "the theme the parent approved, and one manner from shared/manner.py",
        ),
        Instruction(
            "decoration",
            "panel/painting.py :: DECORATION_PROMPT",
            painting.DECORATION_PROMPT,
            "what the reminder is about",
        ),
    ]


def main(argv: list[str]) -> int:
    wanted = [name for name in argv if not name.startswith("-")]
    whole = "--all" in argv or bool(wanted)
    found = [one for one in every_instruction() if not wanted or one.name in wanted]
    if not found:
        print(f"no instruction called {wanted}; try one of:")
        print("  " + ", ".join(one.name for one in every_instruction()))
        return 1
    for one in found:
        print(f"\n{'=' * 78}\n{one.name}  —  {one.sends}")
        print(f"{len(one.text)} characters, {len(one.text.splitlines())} lines")
        print(f"then, per call: {one.then}\n{'=' * 78}")
        if whole:
            print(one.text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
