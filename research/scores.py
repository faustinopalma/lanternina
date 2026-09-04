"""Every run's summary in one file, and every afternoon of every run in another.

    python -m research.scores        # rebuild both from research/runs/

`research/runs/<stamp>/summary.json` is written by one run and knows nothing about the
others. What a person actually wants is the eight axes across every run, in order, with
the version of the prompt each one exercised — and that is a different file, small enough
to commit and to ship, and diffable, so a change in a score shows up in a review.

**And under that, the afternoons themselves.** A mean over twenty-four is a summary of a
summary: it says a run went worse without saying which afternoons went worse, what they
were built from, or which rule refused the ones that never arrived. `scores.json` answers
*how did this prompt do*; `afternoons.md` answers *which one, and why*. The per-run report
already writes each afternoon out in full — this is the same material across every run at
once, which is the view no single run directory can hold.

Both are written at the end of a run and can be rebuilt from the run directories, which is
how the three runs of 29 August got into it after the fact. Rebuilding is the definition:
if the two ever disagree, the directories are right.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .report import IN_ORDER

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
SCORES = HERE / "scores.json"
AFTERNOONS = HERE / "afternoons.md"

# The eight axes shortened to fit a table ninety-six rows long, in the order a run is read
# in. The full names stay in the legend under the table: abbreviating them in the file that
# people query would be a second vocabulary to learn.
SHORT: dict[str, str] = {
    "canBeStarted": "start",
    "sheetStandsAlone": "sheet",
    "oneThingAtATime": "one",
    "everyStepLeavesAMark": "mark",
    "questionHasAWrittenAnswer": "answer",
    "canBeAbandoned": "stop",
    "worthTheHour": "worth",
    "notASchoolSheet": "voice",
}

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


def every_afternoon(runs: Path = RUNS) -> list[dict[str, Any]]:
    """One row per afternoon, across every run, oldest run first.

    A refused afternoon is a row like any other, with the rule that refused it where its
    scores would be. Leaving them out would make a run look better the more often it failed,
    which is the reading the numbers exist to prevent.
    """
    found: list[dict[str, Any]] = []
    for folder in sorted(p for p in runs.glob("*") if p.is_dir()):
        where = folder / "afternoons.json"
        if not where.is_file():
            continue
        try:
            rows = json.loads(where.read_text(encoding="utf-8"))
        except ValueError:
            continue
        label = folder.name.partition("Z-")[2] or folder.name
        summary = folder / "summary.json"
        prompt = ""
        if summary.is_file():
            try:
                prompt = json.loads(summary.read_text(encoding="utf-8")).get("prompt") or ""
            except ValueError:
                prompt = ""
        for row in rows:
            refused = row.get("refused") or {}
            axes = (row.get("appraisal") or {}).get("axes") or {}
            found.append(
                {
                    "run": label,
                    "prompt": prompt,
                    "iteration": row.get("iteration"),
                    "household": row.get("household", ""),
                    "title": row.get("title", ""),
                    "ending": row.get("ending", ""),
                    "minutes": row.get("minutesPlayed"),
                    "built_from": (row.get("builtFrom") or {}).get("form", ""),
                    "refused_by": "; ".join(refused.get("rules", []))
                    or (refused.get("by", "") and f"{refused['by']}: ?"),
                    "axes": {axis: (axes.get(axis) or {}).get("score") for axis in IN_ORDER},
                }
            )
    return found


def as_a_table(rows: list[dict[str, Any]]) -> str:
    """The whole corpus as one Markdown table, committed so two runs diff against each other."""
    head = ["corsa", "prompt", "#", "casa", "pomeriggio", "fine", "min", "metodo"]
    head += [SHORT[axis] for axis in IN_ORDER]
    out = [
        "# Ogni pomeriggio di ogni corsa",
        "",
        "Generato da `python -m research.scores`. La definizione sono le cartelle in "
        "`research/runs/`: se questo file e una di quelle non concordano, ha ragione la "
        "cartella. Le motivazioni di ogni voto stanno nel README della corsa, che le scrive "
        "per esteso; qui c'è il quadro d'insieme che nessuna singola corsa può contenere.",
        "",
        f"{len(rows)} pomeriggi. Una riga senza voti è un pomeriggio rifiutato, e la colonna "
        "«fine» dice da quale regola.",
        "",
        "| " + " | ".join(head) + " |",
        "| " + " | ".join(["---"] * 7 + ["---"] + ["---:"] * len(IN_ORDER)) + " |",
    ]
    for row in rows:
        scores = ["" if row["axes"][axis] is None else str(row["axes"][axis]) for axis in IN_ORDER]
        cells = [
            row["run"],
            row["prompt"] or "—",
            str(row["iteration"] or ""),
            row["household"],
            row["title"] or "**rifiutato**",
            row["refused_by"] or row["ending"],
            "" if row["minutes"] is None else str(row["minutes"]),
            row["built_from"] or "—",
            *scores,
        ]
        out.append("| " + " | ".join(cells) + " |")
    out += [
        "",
        "Gli assi, per esteso: "
        + ", ".join(f"`{SHORT[axis]}` {axis}" for axis in IN_ORDER)
        + ". `research/README.md` dice che cosa prende ciascuno e che cosa non vuol dire.",
        "",
        "«metodo» è la forma di `methods/` da cui il pomeriggio è stato costruito. È vuota "
        "per le corse precedenti al 3 settembre 2026, quando la generazione non leggeva "
        "ancora il manuale.",
        "",
    ]
    return "\n".join(out)


def write(runs: Path = RUNS, to: Path = SCORES) -> list[dict[str, Any]]:
    history = collect(runs)
    to.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (to.parent / AFTERNOONS.name).write_text(
        as_a_table(every_afternoon(runs)), encoding="utf-8", newline="\n"
    )
    return history


if __name__ == "__main__":
    rows = write()
    for row in rows:
        axes = row.get("axes") or {}
        mean = round(sum(axes.values()) / len(axes), 2) if axes else 0
        print(f"{row['run']:44s} {row.get('prompt') or '—':>12}  {len(axes)} assi, media {mean}")
    print(f"\n{len(rows)} corse in {SCORES}")
    print(f"{len(every_afternoon())} pomeriggi in {AFTERNOONS}")
