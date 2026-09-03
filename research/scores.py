"""Every run's summary in one file, so the scores can be read as a history.

    python -m research.scores        # rebuild it from research/runs/

`research/runs/<stamp>/summary.json` is written by one run and knows nothing about the
others. What a person actually wants is the eight axes across every run, in order, with
the version of the prompt each one exercised — and that is a different file, small enough
to commit and to ship, and diffable, so a change in a score shows up in a review.

It is written at the end of a run and can be rebuilt from the run directories, which is
how the three runs of 29 August got into it after the fact. Rebuilding is the definition:
if the two ever disagree, the directories are right.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
SCORES = HERE / "scores.json"

# What of a summary goes into the history. Not the households: they are the same six every
# time and repeating them once per run makes the file unreadable for no gain.
KEPT = (
    "at",
    "prompt",
    "label",
    "iterations",
    "afternoons",
    "refused",
    "endings",
    "axes",
    "minutes",
)


def collect(runs: Path = RUNS) -> list[dict[str, Any]]:
    """Every run there is, oldest first. A directory without a summary is skipped."""
    history: list[dict[str, Any]] = []
    for folder in sorted(p for p in runs.glob("*") if p.is_dir()):
        summary = folder / "summary.json"
        if not summary.is_file():
            continue
        try:
            said = json.loads(summary.read_text(encoding="utf-8"))
        except ValueError:
            continue
        # The label is in the directory name and not in the summary, and it is the only
        # thing that says what a run was for. Split on the `Z-` that ends the stamp: the
        # first hyphen belongs to the date, and splitting there gave `09-03T090000Z-dopo`.
        label = folder.name.partition("Z-")[2]
        history.append({**{key: said.get(key) for key in KEPT}, "label": label, "run": folder.name})
    return history


def write(runs: Path = RUNS, to: Path = SCORES) -> list[dict[str, Any]]:
    history = collect(runs)
    to.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return history


if __name__ == "__main__":
    rows = write()
    for row in rows:
        axes = row.get("axes") or {}
        mean = round(sum(axes.values()) / len(axes), 2) if axes else 0
        print(f"{row['run']:44s} {row.get('prompt') or '—':>12}  {len(axes)} assi, media {mean}")
    print(f"\n{len(rows)} corse in {SCORES}")
