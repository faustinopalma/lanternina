"""One research run: devise, play, score, write it down.

    python -m research.run --iterations 4

Every household in `research/households.py` gets one afternoon per iteration. Within a run
a household accumulates a memory, so the second iteration is devised knowing how the first
went — which is the mechanism `panel/what_happened.py` added and the one thing a single
afternoon cannot exercise.

What it costs, per afternoon: one devise call, one call per sheet collected, one appraisal.
Measured at about two minutes and roughly a cent and a half of tokens.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import random
import time
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from panel.devising import RefusedByTheChecks, devise_experience
from panel.what_happened import Answered, as_material, how_it_has_gone, remembered, the_ground
from shared.capabilities import HouseCapability
from shared.experience import Drawn, ExperienceError, Weight

from .calls import a_context, appraise
from .households import HOUSEHOLDS, Household, Memory
from .play import play

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"

# What every synthetic house can do. The same three the real houses declare.
CAN = frozenset(
    {
        HouseCapability("print_a4"),
        HouseCapability("scan_a4"),
        HouseCapability("show_800x480_1bit"),
    }
)

# How the day is going, drawn per afternoon. Three, because the blank branch is the one a
# willing simulation never reaches and the one the format most needs exercised.
MOODS = (
    "una giornata normale, c'è voglia di fare qualcosa",
    "una giornata storta: poca voglia, e niente di lungo",
    "una giornata buona, c'è tempo e curiosità",
)

# Which weight the clock would have picked. Drawn rather than fixed, so a run covers the
# short column as well as the standard one.
WEIGHTS = (Weight.SHORT, Weight.STANDARD, Weight.STANDARD, Weight.EXTENDED)


async def one_afternoon(
    ctx: Any, house: Household, memory: Memory, dice: random.Random
) -> dict[str, Any]:
    """Devise, play and score one. Returns the row that goes into the run's JSON."""
    began = time.monotonic()
    ran = list(memory.ran)
    going = how_it_has_gone(ran)  # type: ignore[arg-type]
    ground = the_ground(memory.offered)
    row: dict[str, Any] = {"household": house.name}
    try:
        experience, spent = await devise_experience(
            capabilities=CAN,
            language=house.language,
            interests=house.interests,
            avoid=house.avoid,
            difficulty=house.difficulty,
            variety=house.variety,
            sheets=house.sheets,
            note=house.note,
            already=tuple(one.title for one in ran if getattr(one, "title", "")),  # type: ignore[attr-defined]
            recent=_drawn(memory),
            happened=as_material(ran),  # type: ignore[arg-type]
            counts=json.dumps(going.to_dict(), ensure_ascii=False),
            direction=going.direction(),
            ground=json.dumps(ground.to_dict(), ensure_ascii=False) if ground.anything() else "",
            now=time.time(),
        )
    except RefusedByTheChecks as exc:
        row["refused"] = {"by": "checks", "says": str(exc)}
        return row
    except ExperienceError as exc:
        row["refused"] = {"by": "format", "says": str(exc)}
        return row

    mood = dice.choice(MOODS)
    played = await play(
        ctx,
        experience=experience,
        household=house.name,
        weight=dice.choice(WEIGHTS),
        mood=mood,
    )
    scored: dict[str, Any] = {}
    try:
        scored = await appraise(ctx, transcript=played.transcript())
    except (ValueError, KeyError) as exc:
        scored = {"failed": f"{type(exc).__name__}: {exc}"}

    memory.offered.append(list(experience.themes))
    memory.ran.append(
        remembered(
            household_id=house.name,
            run_id=experience.experience_id,
            experience=experience.to_dict(),
            at=time.time(),
            weight=played.weight,
            minutes=played.minutes,
            reached=played.reached,
            ending=played.ending,            answered=tuple(
                Answered(
                    moment_id=str(one.get("momentId", "")),
                    came=str(one.get("came", "blank")),
                    reading=str(one.get("reading", "")),
                )
                for one in played.sheets
                if "came" in one
            ),
        )
    )

    row.update(
        {
            "title": experience.title,
            "experienceId": experience.experience_id,
            "themes": list(experience.themes),
            "minutes": experience.minutes,
            "moments": len(experience.moments),
            "mood": mood,
            "weight": played.weight,
            "ending": played.ending,
            "reached": played.reached,
            "minutesPlayed": played.minutes,
            "sheets": played.sheets,
            "appraisal": scored,
            "seconds": round(time.monotonic() - began, 1),
            "spent": None if spent is None else asdict(spent),
            "transcript": played.transcript(),
            "overview": experience.overview,
            "script": experience.script,
        }
    )
    return row


def _drawn(memory: Memory) -> tuple[Drawn, ...]:
    out: list[Drawn] = []
    for one in memory.ran[-5:]:
        try:
            out.append(Drawn.from_dict(getattr(one, "drawn", None)))
        except (ExperienceError, AttributeError):
            continue
    return tuple(out)


def _averages(rows: list[dict[str, Any]]) -> dict[str, float]:
    """Mean per axis over the afternoons that were scored. Two decimals, no weighting."""
    totals: dict[str, list[float]] = {}
    for row in rows:
        for axis, said in (row.get("appraisal", {}).get("axes") or {}).items():
            score = said.get("score")
            if isinstance(score, (int, float)):
                totals.setdefault(axis, []).append(float(score))
    return {axis: round(sum(got) / len(got), 2) for axis, got in sorted(totals.items())}


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--households", type=str, default="")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--label", type=str, default="")
    asked = parser.parse_args()

    wanted = [one for one in HOUSEHOLDS if not asked.households or one.name in asked.households]
    dice = random.Random(asked.seed)
    ctx = a_context(time.time())
    memories = {one.name: Memory() for one in wanted}

    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H%M%SZ")
    where = RUNS / (f"{stamp}-{asked.label}" if asked.label else stamp)
    where.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    began = time.monotonic()
    for iteration in range(1, asked.iterations + 1):
        for house in wanted:
            print(f"  {iteration}/{asked.iterations}  {house.name} …", flush=True)
            row = await one_afternoon(ctx, house, memories[house.name], dice)
            row["iteration"] = iteration
            rows.append(row)
            print(
                f"      {row.get('title', row.get('refused', {}).get('by', '?'))}"
                f"  ·  {row.get('ending', '—')}  ·  {row.get('seconds', 0)}s",
                flush=True,
            )
            (where / "afternoons.json").write_text(
                json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    summary = {
        "at": stamp,
        "iterations": asked.iterations,
        "households": [one.name for one in wanted],
        "afternoons": len(rows),
        "refused": sum(1 for one in rows if "refused" in one),
        "endings": {
            ending: sum(1 for one in rows if one.get("ending") == ending)
            for ending in ("closed", "asked", "stopped", "way_out", "went_wrong")
        },
        "axes": _averages(rows),
        "minutes": round((time.monotonic() - began) / 60, 1),
    }
    (where / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    from .report import write_report

    write_report(where, summary, rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n{where}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
