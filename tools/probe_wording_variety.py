"""One-off: ask the real model for wordings under two or three prompts, and say how much
the four it returns differ from each other.

The four wordings exist so that a reminder shown once a day does not arrive in the same
words within the week. On 20 August 2026 the first real run showed them arriving close
together — "Metti / Sistema / Riponi / Inserisci il libro di storia nella cartella" differ
by a verb — which is not a fault and is not what the four are for. This asks whether
saying so in the prompt changes anything, against the deployment rather than by reasoning
about it.

Two figures per set of four, both computed from the wordings themselves and neither
measured with an instrument:

- **distinct openings**, out of four: how many different first words the four start with.
  Across the twelve sets of 20 August 2026 this was four out of four every time, under
  every prompt, so it separated nothing. Kept because that is itself the answer to "do
  they all start the same way", which was the first guess.
- **shared words**, a mean over the six pairs: of the words in either wording of a pair,
  the fraction in both. One means identical word sets, zero means nothing in common. The
  subject of the reminder is in every wording, so this never reaches zero and the figure
  is only worth reading against another figure from the same sentence.

The wordings still go out through ``panel.wording.word_sentence``, so the gate screens
them exactly as it does in the reminders route. The instruction is swapped on the module
that holds it, which is the only part of this that a test could not do.

    $env:LANTERNINA_FOUNDRY_ENDPOINT=...        # and ACCOUNT_ENDPOINT, DEPLOYMENT
    $env:LANTERNINA_CONTENT_SAFETY_ENDPOINT=...
    python tools/probe_wording_variety.py

The credential is whatever ``DefaultAzureCredential`` finds, which on a development
machine is the Azure CLI login. The sentences are synthetic and belong to nobody.
"""

from __future__ import annotations

import asyncio
import itertools
import re
import time

from agents import reminder_wording
from agents.reminder_wording import MAX_WORDING_CHARS, WORDINGS_PER_SENTENCE
from panel.wording import word_sentence

# What the prompt was before 20 August 2026: the whole of it except the paragraph that
# says why four are wanted. Taken from the module rather than copied, so the comparison
# cannot drift away from the prompt actually in use.
BEFORE = reminder_wording._BASE

# Names the shape instead of the reason, which is the part a model can act on directly.
SAY_HOW = BEFORE + (
    f"Build the {WORDINGS_PER_SENTENCE} differently from one another: no two may begin "
    "with the same word, and no two may have the same grammatical shape. Among them use "
    "at least one that states what is about to happen rather than asking for it.\n"
)

VARIANTS: list[tuple[str, str]] = [
    ("before", BEFORE),
    ("say why", reminder_wording._INSTRUCTION),
    ("say how", SAY_HOW),
]

SENTENCES: list[tuple[str, str]] = [
    ("07:30", "Metti in cartella il libro di storia."),
    ("20:00", "Annaffia il basilico sul davanzale della cucina."),
]

_WORD = re.compile(r"\w+", re.UNICODE)


def words_of(wording: str) -> set[str]:
    return {match.group().lower() for match in _WORD.finditer(wording)}


def opening_of(wording: str) -> str:
    found = _WORD.search(wording)
    return found.group().lower() if found else ""


def shared_words(wordings: tuple[str, ...]) -> float:
    """Mean over every pair: of the words in either, the fraction in both."""
    pairs = list(itertools.combinations(wordings, 2))
    if not pairs:
        return 0.0
    fractions = []
    for one, other in pairs:
        left, right = words_of(one), words_of(other)
        union = left | right
        fractions.append(len(left & right) / len(union) if union else 0.0)
    return sum(fractions) / len(fractions)


async def main() -> None:
    for name, instruction in VARIANTS:
        reminder_wording._INSTRUCTION = instruction
        print(f"\n=== {name} " + "=" * (60 - len(name)))
        for at, text in SENTENCES:
            print(f"\n{at}  {text}")
            started = time.monotonic()
            try:
                wordings, spent = await word_sentence(text, at, now=time.time())
            except Exception as exc:  # noqa: BLE001 - a probe reports a failure, it does not raise
                took = time.monotonic() - started
                print(f"  failed after {took:.1f} s: {type(exc).__name__}: {exc}")
                continue
            took = time.monotonic() - started
            if not wordings:
                print("  nothing parsed out of the answer")
                continue
            for wording in wordings:
                over = " OVER" if len(wording) > MAX_WORDING_CHARS else ""
                print(f"  {len(wording):3d}{over}  {wording}")
            openings = len({opening_of(one) for one in wordings})
            print(
                f"  distinct openings {openings}/{len(wordings)}   "
                f"shared words {shared_words(wordings):.2f}   took {took:.1f} s"
            )
            if spent is None:
                print("  the backend reported no usage")
            else:
                print(
                    f"  in {spent.input_tokens} out {spent.output_tokens} "
                    f"(reasoning {spent.reasoning_tokens})"
                )


asyncio.run(main())
