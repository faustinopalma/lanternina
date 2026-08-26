"""Devise a handful of afternoons against the real service and write them down.

What a test cannot tell you: whether the things that come back are any good. This runs the
whole devising path — prompt, model, parse, checks, one repair — as many times as asked, and
puts each answer in `experiments/NN-name/` where it can be read.

    $env:PYTHONPATH="."
    .\.venv\Scripts\python.exe -m tools.devise_many "material-that-varies" --times 10

It reads the panel's own environment so the numbers are the ones production pays. Nothing
about a household goes in: the interests and the language below are invented, because
`experiments/` is gitignored but the habit is not.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent.parent
WHERE = HERE / "experiments"

# Invented, and the point of them is only that they are not empty.
LANGUAGE = "italiano"
INTERESTS = ("le mappe", "gli oggetti trovati", "il tempo che cambia")
AVOID = ("i ragni",)


async def once(
    already: tuple[str, ...], recent: tuple[Any, ...], subjects: tuple[str, ...]
) -> dict[str, Any]:
    from panel.devising import devise_experience
    from shared.capabilities import HouseCapability

    began = time.time()
    try:
        experience, spent = await devise_experience(
            capabilities=frozenset(
                {
                    HouseCapability.PRINT_A4,
                    HouseCapability.SHOW_800X480_1BIT,
                    HouseCapability.SCAN_A4,
                }
            ),
            language=LANGUAGE,
            interests=INTERESTS,
            avoid=AVOID,
            already=already,
            recent=recent,
            now=began,
        )
    except Exception as exc:  # noqa: BLE001 - a failed run is a result worth recording
        return {"seconds": round(time.time() - began, 1), "failed": f"{type(exc).__name__}: {exc}"}
    return {
        "seconds": round(time.time() - began, 1),
        "spent": getattr(spent, "total_tokens", None),
        "experience": experience.to_dict(),
    }


async def run(name: str, times: int) -> int:
    from shared.experience import Drawn

    folder = WHERE / f"{_next_number():02d}-{name}"
    folder.mkdir(parents=True, exist_ok=True)
    already: list[str] = []
    # Carried forward, because this is what makes each afternoon unlike the last and a run
    # that does not carry it is measuring a house with no history nine times over. The
    # first nine of these were run without it and came back as one afternoon with nine
    # titles: light, a map, an object on a table. `DRAWN_BEFORE` is what the panel uses.
    drawn: list[Any] = []
    # And what they were about, which is what the dimensions cannot see.
    subjects: list[str] = []
    rows: list[dict[str, Any]] = []
    for turn in range(1, times + 1):
        got = await once(tuple(already), tuple(drawn[-5:]), tuple(subjects[-25:]))
        rows.append(got)
        document = got.get("experience")
        if document:
            already.append(str(document.get("title", "")))
            drawn.append(Drawn.from_dict(document.get("drawn")))
            (folder / f"{turn:02d}.json").write_text(
                json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(
                f"{turn:2d}  {got['seconds']:6.1f}s  {document.get('minutes')} min  "
                f"script {len(document.get('script') or '')}  "
                f"{len(document.get('moments') or [])} moments  {document.get('title')}"
            )
        else:
            print(f"{turn:2d}  {got['seconds']:6.1f}s  {got.get('failed')}")
    (folder / "runs.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _summarise(rows, folder)
    return 0


def _summarise(rows: list[dict[str, Any]], folder: Path) -> None:
    made = [row["experience"] for row in rows if row.get("experience")]
    if not made:
        print(f"\nnothing came back; {len(rows)} attempts")
        return
    scripts = [len(one.get("script") or "") for one in made]
    minutes = [int(one.get("minutes") or 0) for one in made]
    moments = [len(one.get("moments") or []) for one in made]
    seconds = [row["seconds"] for row in rows if row.get("experience")]
    print(
        f"\n{len(made)}/{len(rows)} came back\n"
        f"  seconds   {min(seconds):.1f}–{max(seconds):.1f}, "
        f"median {statistics.median(seconds):.1f}\n"
        f"  script  {min(scripts)}–{max(scripts)} chars, median "
        f"{int(statistics.median(scripts))}\n"
        f"  minutes   {sorted(set(minutes))}\n"
        f"  moments   {min(moments)}–{max(moments)}\n"
        f"  written to {folder}"
    )


def _next_number() -> int:
    used = [
        int(one.name[:2])
        for one in WHERE.glob("[0-9][0-9]-*")
        if one.is_dir() and one.name[:2].isdigit()
    ]
    return max(used, default=0) + 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--times", type=int, default=10)
    args = parser.parse_args(argv)
    return asyncio.run(run(args.name, args.times))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
