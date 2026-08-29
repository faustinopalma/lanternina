"""One run as a page somebody reads, beside the JSON somebody diffs.

Markdown rather than HTML: this is committed, so what matters is that two runs can be
compared with `git diff` and that the axes are legible in a pull request.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# The order the axes are read in, which is the order an afternoon fails in: it has to be
# startable before anything else matters, and it has to sound right last.
IN_ORDER = (
    "canBeStarted",
    "sheetStandsAlone",
    "oneThingAtATime",
    "everyStepLeavesAMark",
    "questionHasAWrittenAnswer",
    "canBeAbandoned",
    "worthTheHour",
    "notASchoolSheet",
)


def _bar(score: float) -> str:
    return "█" * int(round(score)) + "·" * (5 - int(round(score)))


def write_report(where: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    out: list[str] = []
    out.append(f"# Corsa {summary['at']}")
    out.append("")
    out.append(
        f"{summary['afternoons']} pomeriggi · {summary['iterations']} giri · "
        f"{len(summary['households'])} case · {summary['minutes']} minuti · "
        f"{summary['refused']} rifiutati dai controlli"
    )
    out.append("")
    out.append("## Assi, media")
    out.append("")
    out.append("| asse | media | |")
    out.append("| --- | ---: | --- |")
    axes = summary.get("axes", {})
    for axis in IN_ORDER:
        if axis in axes:
            out.append(f"| {axis} | {axes[axis]:.2f} | `{_bar(axes[axis])}` |")
    for axis, score in axes.items():
        if axis not in IN_ORDER:
            out.append(f"| {axis} | {score:.2f} | `{_bar(score)}` |")
    out.append("")
    out.append("## Come sono finiti")
    out.append("")
    for ending, count in summary["endings"].items():
        out.append(f"- {ending}: {count}")
    out.append("")

    changes = [
        one["appraisal"]["whatToChangeInThePrompt"]
        for one in rows
        if one.get("appraisal", {}).get("whatToChangeInThePrompt")
    ]
    if changes:
        out.append("## Che cosa direbbe diversamente al prompt")
        out.append("")
        out += [f"- {one}" for one in changes]
        out.append("")

    out.append("## I pomeriggi")
    out.append("")
    for row in rows:
        if "refused" in row:
            out.append(
                f"### {row['iteration']} · {row['household']} — rifiutato dai "
                f"{row['refused']['by']}"
            )
            out.append("")
            out.append(f"> {row['refused']['says']}")
            out.append("")
            continue
        out.append(f"### {row['iteration']} · {row['household']} — {row['title']}")
        out.append("")
        out.append(
            f"*{', '.join(row['themes'])}* · {row['weight']} · {row['ending']} · "
            f"{row['minutesPlayed']} min giocati su {row['minutes']} previsti"
        )
        out.append("")
        out.append(f"> {row['overview']}")
        out.append("")
        scored = row.get("appraisal", {}).get("axes") or {}
        if scored:
            out.append("| asse | | dice |")
            out.append("| --- | ---: | --- |")
            for axis in IN_ORDER:
                said = scored.get(axis)
                if not said:
                    continue
                out.append(f"| {axis} | {said.get('score', '?')} | {said.get('says', '')} |")
            out.append("")
        worst = row.get("appraisal", {}).get("worstLine")
        if worst:
            out.append(f"**La riga da cambiare:** «{worst}»")
            out.append("")
        for sheet in row.get("sheets", []):
            if "came" not in sheet:
                continue
            out.append(f"- foglio *{sheet['momentId']}* → **{sheet['came']}** — {sheet['reading']}")
        out.append("")
    (where / "README.md").write_text("\n".join(out), encoding="utf-8")
