"""Try a prompt against the real service and see what it would put in a room.

`tools/devise_many.py` runs the whole devising path, checks and gate included, and takes
two minutes an afternoon. This is the short loop: one call, one document, printed as
somebody in the room meets it, with an override so a fragment of the prompt can be changed
on disk and tried without touching the repository's own.

    python -m tools.try_prompt                          the prompt as it stands
    python -m tools.try_prompt --swap worth=try/a.md    with that fragment replaced
    python -m tools.try_prompt --times 3 --keep b       write them to experiments/b/

**What it measures is whether somebody could do it.** The afternoons that came back before
were not impossible, they were undoable in a way that reads as fine on the page: asking for
a discrimination nobody can reliably make (*which sound lasts longer*), naming a material
nobody said was there, or asking for something with no result the person can see. So the
counts at the end are about that, and they are counts and not judgements — the judgement is
still somebody reading the thing.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from agents import experience_deviser as deviser
from shared.capabilities import HouseCapability
from shared.experience import Experience

# What a house certainly has, and what a script may therefore ask for without saying where
# it came from. Anything else has to be named in the afternoon itself as something found.
CERTAINLY_HERE = (
    "carta", "foglio", "matita", "penna", "pennarello", "forbici", "nastro",
    "tavolo", "finestra", "porta", "luce", "acqua", "rubinetto",
)

# Verbs that ask for a perception rather than an action. A person cannot tell whether they
# did it, so they cannot tell whether they are doing the afternoon right — and that is the
# feeling the whole design is trying not to produce.
UNCHECKABLE = re.compile(
    r"\b(ascolt\w*|senti\w*|annus\w*|odor\w*|percep\w*|nota\s+quale|riconosc\w*|"
    r"distingu\w*|confront\w+\s+il\s+suono|lascia\s+spegnere)\b",
    re.IGNORECASE,
)

# What a person does that leaves a mark somebody can point at afterwards.
LEAVES_A_MARK = re.compile(
    r"\b(scriv\w*|disegn\w*|segn\w*|traccia\w*|ritagli\w*|piega\w*|incoll\w*|"
    r"metti\w*|posa\w*|apri\w*|conta\w*|misur\w*|elenc\w*|nomin\w*)\b",
    re.IGNORECASE,
)


# There is no count of how much a person has to hold in their head, and there was one for an
# hour. It matched every capitalised word, which in Italian means every imperative opening a
# line — Prendi, Metti, Scrivi — and reported eighteen proper nouns in an afternoon that had
# one. Corrected to skip sentence openings it reported nought to six, across afternoons that
# read as wildly different to follow, so it was measuring nothing either way. What makes
# 'Il verbale del quarto colpo' unfollowable is a 1931 survey, a register, an abbreviation,
# a bell code, a pressure test and a covered word — concepts to relate, not names to recall,
# and a regular expression does not see those. Somebody reading it is still the measure.


def _things_to_remember(lines: list[str]) -> set[str]:
    """Gone. See the note above: it measured Italian grammar, not difficulty."""
    raise NotImplementedError("there is no honest count of this yet")


def _lines_of(document: dict[str, Any]) -> list[str]:
    """Every line that reaches a display or a page, at the standard weight."""
    said: list[str] = []
    for moment in document.get("moments") or ():
        weights = moment.get("weights") or {}
        weighing = weights.get("standard") or {}
        said.extend(str(one) for one in (weighing.get("lines") or ()))
        page = moment.get("page") or {}
        said.extend(str(one) for one in (page.get("note") or ()))
        for rung in moment.get("help") or ():
            said.extend(str(one) for one in (rung.get("lines") or ()))
    return said


def counted(document: dict[str, Any]) -> dict[str, Any]:
    """The shape, how much of it somebody could do, and how much they must hold."""
    moments = document.get("moments") or []
    lines = _lines_of(document)
    pages = [m.get("page") for m in moments if m.get("page")]
    on_paper = sum(len(p.get("note") or ()) for p in pages)
    return {
        "moments": len(moments),
        "pages": len(pages),
        "words_said": sum(len(one.split()) for one in lines),
        "lines_on_paper": on_paper,
        "uncheckable": sum(1 for one in lines if UNCHECKABLE.search(one)),
        "leaves_a_mark": sum(1 for one in lines if LEAVES_A_MARK.search(one)),
        "script_chars": len(document.get("script") or ""),
    }


async def once(
    *,
    language: str,
    capabilities: frozenset[HouseCapability],
    shape: str = "",
    distance: str = "",
    note: str = "",
    words_per_line: int = deviser.DEFAULT_WORDS_PER_LINE,
) -> dict[str, Any]:
    """One call, parsed, with nothing screened and nothing checked. Raises what it raises."""
    import os
    import secrets

    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
    from shared.agents import AgentContext
    from shared.domain import LearnerId
    from shared.seal import Sealer, SealPurpose

    environment = dict(os.environ)
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=time.time()
    )
    try:
        answer = await deviser.ExperienceDeviser().ask(
            context,
            capabilities=capabilities,
            language=language,
            shape=shape,
            distance=distance,
            note=note,
            words_per_line=words_per_line,
        )
    finally:
        await gate.aclose()
    return deviser.experience_in(answer)


def swap(pairs: list[str]) -> None:
    """Replace a rendered prompt fragment for this process only.

    By substitution into the assembled instruction rather than by rebuilding it: the
    deviser composes its prompt from module constants at import time, and a variant that
    had to re-run that composition would be testing my reassembly and not the prompt.
    Nothing is written back, so a variant can be tried without a commit.
    """
    import shared.experience_prompt as fragments

    known = {"worth": fragments.WHAT_MAKES_IT_WORTH_DOING}
    for pair in pairs:
        name, _, path = pair.partition("=")
        if name not in known:
            raise SystemExit(f"non so che cos'è {name!r}; conosco {sorted(known)}")
        instead = Path(path).read_text(encoding="utf-8")
        before = deviser._INSTRUCTION
        after = before.replace(known[name], instead)
        if after == before:
            raise SystemExit(f"{name!r} non compare nell'istruzione assemblata")
        deviser._INSTRUCTION = after  # type: ignore[misc]
        print(f"  (sostituito {name}: {len(known[name])} → {len(instead)} caratteri)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One prompt, one afternoon, read as it arrives.")
    parser.add_argument("--times", type=int, default=1)
    parser.add_argument("--language", default="italiano")
    parser.add_argument("--swap", action="append", default=[], help="worth=path/to/file.md")
    parser.add_argument("--keep", default="", help="write the documents under experiments/<name>")
    parser.add_argument(
        "--shape",
        default=deviser.DEFAULT_DIFFICULTY,
        choices=sorted(deviser.SHAPES),
        help="what the parent chose under how it should be made",
    )
    parser.add_argument("--words-per-line", type=int, default=deviser.DEFAULT_WORDS_PER_LINE)
    parser.add_argument(
        "--variety",
        default=deviser.DEFAULT_VARIETY,
        choices=sorted(deviser.DISTANCES),
        help="how far to go from the afternoons already offered",
    )
    parser.add_argument("--note", default="", help="what is true in the house at the moment")
    args = parser.parse_args(argv)

    if args.swap:
        swap(args.swap)

    capabilities = frozenset(
        {
            HouseCapability.PRINT_A4,
            HouseCapability.SCAN_A4,
            HouseCapability.SHOW_800X480_1BIT,
        }
    )
    where = Path("experiments") / args.keep if args.keep else None
    if where:
        where.mkdir(parents=True, exist_ok=True)

    from tools.as_it_arrives import read

    every: list[dict[str, Any]] = []
    for n in range(1, args.times + 1):
        began = time.time()
        try:
            experience: Experience = asyncio.run(
                once(
                    language=args.language,
                    capabilities=capabilities,
                    shape=deviser.SHAPES[args.shape],
                    distance=deviser.DISTANCES[args.variety],
                    note=args.note,
                    words_per_line=args.words_per_line,
                )
            )
        except Exception as exc:  # noqa: BLE001 - a probe reports and carries on
            print(f"{n:02d} rifiutato: {type(exc).__name__}: {exc}")
            continue
        document = experience.to_dict()
        if where:
            (where / f"{n:02d}.json").write_text(
                json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        read(document)
        one = counted(document)
        one["seconds"] = int(time.time() - began)
        every.append(one)
        print("  " + "  ".join(f"{k}={v}" for k, v in one.items()))

    if len(every) > 1:
        print("\n" + "─" * 78)
        for name in every[0]:
            values = [one[name] for one in every]
            print(f"  {name:20} {min(values)}–{max(values)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
