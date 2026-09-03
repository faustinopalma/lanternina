"""Every prompt this system sends a model, whole, as the model receives it.

A prompt is two things joined: a standing instruction, which lives in the `.md` files beside
each agent, and the household's own material, which arrives at the moment of the call. The
`.md` files can be read on their own. What cannot be read on their own is the *join* — the
order the blocks go in, what the numbers came out as, where the parent's typed words land.
This prints that.

The household material here is invented, and obviously so: `docs/NON-GOALS.md` and the
working rules both say no personal data lives in this repository. Where a real call would
carry a real house, this carries two interests, one thing to avoid, and a sentence about
brushing teeth.

    python -m tools.prompts               # what there is, and how big
    python -m tools.prompts deviser       # one of them, whole
    python -m tools.prompts --all         # all of them, whole
    python -m tools.prompts --write       # into docs/prompts/, one file each

`--write` is what `tests/test_prompts_rendered.py` checks: a prompt changed in the code and
not rendered fails that test, so what is in `docs/prompts/` is what is being sent.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

RENDERED: Path = Path(__file__).resolve().parent.parent / "docs" / "prompts"

# Fixed rather than drawn at random, so that rendering the same code twice writes the same
# file and the test can tell a real change from a new roll of the dice.
_MANNER_FIELDS = {
    "drawn_with": "a fine dip pen",
    "seen_from": "from a little way off, with room around it",
    "the_light": "flat daylight with no shadow",
    "the_line": "confident and unhurried",
}


@dataclass(frozen=True, slots=True)
class Prompt:
    """One whole prompt, and where in the code it was assembled."""

    name: str
    sends: str
    text: str
    # What of it was invented for this rendering, so a reader is never in doubt about which
    # words came from the repository and which stood in for a house.
    invented: str
    # Twelve hex characters naming this version of the standing instruction, where the
    # sender computes one. It is what a line in the workspace carries, so a count of
    # afternoons under a fingerprint can be read against the text that produced them.
    fingerprint: str = ""


def every_prompt() -> list[Prompt]:
    from agents import (
        experience_continuer,
        experience_deviser,
        experience_judge,
        page_maker,
        page_reader,
        reminder_reader,
        reminder_wording,
    )
    from panel import painting
    from panel.guidelines import FIXED
    from shared.capabilities import HouseCapability
    from shared.manner import Manner
    from shared.page import Page, PageKind, Room, Space

    manner = Manner(**_MANNER_FIELDS)
    house = frozenset(
        {
            HouseCapability.PRINT_A4,
            HouseCapability.SHOW_800X480_1BIT,
            HouseCapability.SCAN_A4,
        }
    )
    page = Page(
        kind=PageKind.NOTEBOOK,
        title="Le nuvole del ventiquattro",
        note=("Questa pagina appartiene a chi guarda in alto.",),
        spaces=(
            Space(label="Che forma aveva", room=Room.A_LINE),
            Space(label="Disegnala", room=Room.A_BOX),
        ),
        illustration="a sky with three clouds of different shapes, seen from a window",
    )

    return [
        Prompt(
            "deviser",
            "agents/experience_deviser.py :: the_prompt()",
            experience_deviser.the_prompt(
                language="italiano",
                capabilities=house,
                interests=("le nuvole", "i treni"),
                avoid=("i ragni",),
                already=("Il quaderno del vento",),
            ),
            "the language, what the house can do, two interests, one thing to avoid, and "
            "one title already offered",
            fingerprint=experience_deviser.PROMPT_FINGERPRINT,
        ),
        Prompt(
            "continuer",
            "agents/experience_continuer.py :: the_prompt()",
            experience_continuer.the_prompt(
                experience={
                    "experience_id": "exp_invented",
                    "title": "Le nuvole del ventiquattro",
                    "moments": [{"id": "m1", "act": "collect"}],
                },
                after="m1",
                came="yes",
                reading={
                    "cells": [
                        {"cell_id": "c1", "label": "Che forma aveva", "value": "un cavallo"},
                        {"cell_id": "c2", "label": "Disegnala", "value": ""},
                    ]
                },
                bounds=FIXED,
                household_bounds="In questa casa si può uscire in giardino.",
            ),
            "an afternoon of one moment, a page that came back with one cell written and "
            "one left blank, and a line a parent might have typed",
        ),
        Prompt(
            "page-maker",
            "agents/page_maker.py :: asked_for()",
            page_maker.asked_for(page, manner),
            "a notebook page about clouds, with two places to write, and one manner",
        ),
        Prompt(
            "page-reader",
            "agents/page_reader.py :: _INSTRUCTION",
            page_reader._INSTRUCTION
            + "\nWhat the sheet asked for, for context only: Le nuvole del ventiquattro",
            "the line naming what the sheet asked for; two images go with it",
        ),
        Prompt(
            "judge",
            "agents/experience_judge.py :: _INSTRUCTION",
            experience_judge._INSTRUCTION
            + "\nThe afternoon, as the person receives it:\n"
            + '{"moments": [{"id": "m1", "act": "say", "lines": ["C\'è una lettera nel muro."]}]}',
            "one moment of an invented afternoon; a real call carries the whole of it, with "
            "the title, the overview, the themes, the script and the ten dimensions taken out",
        ),
        Prompt(
            "reminder-reader",
            "agents/reminder_reader.py :: _INSTRUCTION",
            reminder_reader._INSTRUCTION + '\n[{"id": "r1", "text": "lavarsi i denti dopo cena"}]',
            "one sentence a parent might have typed",
        ),
        Prompt(
            "reminder-bank",
            "agents/reminder_wording.py :: _INSTRUCTION",
            reminder_wording._INSTRUCTION
            + '\n{"at": "20:30", "text": "lavarsi i denti dopo cena"}',
            "the hour and the sentence",
        ),
        Prompt(
            "reminder-now",
            "agents/reminder_wording.py :: _NOW + _SUBJECT",
            reminder_wording._NOW
            + reminder_wording._SUBJECT
            + '\n{"at": "20:30", "text": "lavarsi i denti dopo cena"}',
            "the hour and the sentence",
        ),
        Prompt(
            "picture",
            "panel/painting.py :: PICTURE_PROMPT",
            f"{painting.PICTURE_PROMPT.format(theme='nuvole')} {manner.as_sentence()}",
            "a theme a parent might have approved, and one manner",
        ),
        Prompt(
            "decoration",
            "panel/painting.py :: DECORATION_PROMPT",
            painting.DECORATION_PROMPT.format(subject="a toothbrush"),
            "what a reminder might be about",
        ),
    ]


def _head(one: Prompt) -> str:
    return (
        f"{one.name}  —  {one.sends}\n"
        f"{len(one.text)} characters, {len(one.text.splitlines())} lines\n"
        + (f"fingerprint: {one.fingerprint}\n" if one.fingerprint else "")
        + f"invented for this rendering: {one.invented}\n"
    )


def rendered(one: Prompt) -> str:
    """One prompt as it is written to `docs/prompts/`, header and all."""
    return f"{_head(one)}{'=' * 78}\n{one.text}"


def write(where: Path = RENDERED) -> list[Path]:
    """Render every prompt to `<where>/<name>.txt`. Returns what was written."""
    where.mkdir(parents=True, exist_ok=True)
    written = []
    for one in every_prompt():
        path = where / f"{one.name}.txt"
        path.write_text(rendered(one), encoding="utf-8", newline="\n")
        written.append(path)
    return written


def main(argv: list[str]) -> int:
    if "--write" in argv:
        for path in write():
            print(path)
        return 0
    wanted = [name for name in argv if not name.startswith("-")]
    whole = "--all" in argv or bool(wanted)
    found = [one for one in every_prompt() if not wanted or one.name in wanted]
    if not found:
        print(f"no prompt called {wanted}; try one of:")
        print("  " + ", ".join(one.name for one in every_prompt()))
        return 1
    for one in found:
        print(f"\n{'=' * 78}\n{_head(one)}{'=' * 78}")
        if whole:
            print(one.text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
