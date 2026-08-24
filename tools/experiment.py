"""One experiment on the simulated house, kept where somebody can look at it.

    python -m tools.experiment run "the second afternoon" --by teenager
    python -m tools.experiment run "no hand" --times 3

Each run gets its own folder under `experiments/`, numbered so they read in order, and
inside it the whole flow in sequence: every screen the display showed, every sheet as it was
handed over, every sheet as it came back. `notes.md` holds what was measured and a place to
write what it looked like — the part no assertion covers, and the reason these are kept.

**Nothing is deleted, including the runs that went badly.** A run that failed is the only
evidence of how it failed, and this project has twice been saved by looking at one.

The images are large and are not committed; `.gitignore` keeps the notes and drops the
pixels. What survives in the repository is what was measured and what somebody thought of it.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import time
from pathlib import Path
from typing import Any

from devices.pretend import Pretend
from printing.paper import ink_fraction
from tools.handwriting import HANDS

WHERE = Path("experiments")


def next_folder(root: Path, name: str) -> Path:
    """The next numbered folder. Two digits, so `ls` and a file browser agree on the order."""
    root.mkdir(parents=True, exist_ok=True)
    used = [int(m.group(1)) for p in root.iterdir() if (m := re.match(r"(\d+)-", p.name))]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "run"
    return root / f"{max(used, default=0) + 1:02d}-{slug}"


def flow_of(where: Path, into: Path) -> list[dict[str, Any]]:
    """Copy everything that happened into one numbered sequence, and say what it was.

    The transcript is already in order, so this is a walk rather than a sort. A page appears
    twice — as it was handed over and as it came back — because the pair is the reading, and
    seeing one without the other says nothing.
    """
    pretend = Pretend(where)
    into.mkdir(parents=True, exist_ok=True)
    steps: list[dict[str, Any]] = []
    for number, line in enumerate(_transcript(pretend), start=1):
        what = str(line.get("what", ""))
        if what == "display":
            source = pretend.display / str(line.get("file", ""))
            _copy(source, into / f"{number:02d}-screen.png")
            steps.append(
                {
                    "step": number,
                    "what": "screen",
                    "heading": line.get("heading", ""),
                    "lines": line.get("lines", []),
                }
            )
        elif what == "paper":
            sheet = str(line.get("sheet_id", ""))
            _copy(pretend.paper / f"{sheet}.png", into / f"{number:02d}-page-handed-over.png")
            _copy(pretend.paper / f"{sheet}.pdf", into / f"{number:02d}-page-handed-over.pdf")
            steps.append({"step": number, "what": "page", "sheet": sheet})
        elif what == "glass":
            sheet = str(line.get("sheet_id", ""))
            written = pretend.paper / f"{sheet}-written.png"
            if written.is_file():
                _copy(written, into / f"{number:02d}-page-came-back.png")
            steps.append(
                {
                    "step": number,
                    "what": "came back",
                    "sheet": sheet,
                    "by_hand": bool(line.get("by_hand")),
                    "filled": line.get("filled", []),
                }
            )
        else:
            steps.append({"step": number, "what": what, **_without(line, ("at", "what"))})
    return steps


def _transcript(pretend: Pretend) -> list[dict[str, Any]]:
    if not pretend.transcript.is_file():
        return []
    lines = pretend.transcript.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def _without(line: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: value for key, value in line.items() if key not in keys}


def _copy(source: Path, target: Path) -> None:
    if source.is_file():
        shutil.copy2(source, target)


def ink_in(folder: Path) -> dict[str, float]:
    """How much of each sheet is covered, so a page that would empty a cartridge is visible."""
    import cv2
    import numpy as np

    measured: dict[str, float] = {}
    for page in sorted(folder.glob("*-page-*.png")):
        image = cv2.imread(str(page), cv2.IMREAD_GRAYSCALE)
        if image is not None:
            measured[page.name] = round(
                ink_fraction(np.asarray(image, dtype=np.uint8)) * 100, 2
            )
    return measured


def write_notes(
    folder: Path, *, asked: dict[str, Any], steps: list[dict[str, Any]], seconds: float
) -> None:
    """What was measured, and a heading for what has to be looked at rather than measured."""
    ink = ink_in(folder / "flow")
    screens = [s for s in steps if s["what"] == "screen"]
    pages = [s for s in steps if s["what"] == "page"]
    lines = [
        f"# {folder.name}",
        "",
        f"Run on {time.strftime('%d %B %Y, %H:%M')}, in {seconds:.0f} s.",
        "",
        "## What was asked for",
        "",
        *(f"- **{key}**: {value}" for key, value in asked.items()),
        "",
        "## What happened",
        "",
        f"{len(screens)} screens, {len(pages)} pages handed over, "
        f"{len([s for s in steps if s['what'] == 'came back'])} back off the glass.",
        "",
    ]
    for step in steps:
        if step["what"] == "screen":
            said = " / ".join(str(one) for one in step["lines"])
            lines.append(f"{step['step']:02d}. **screen** — *{step['heading']}* — {said}")
        elif step["what"] == "page":
            lines.append(f"{step['step']:02d}. **page** {step['sheet']} handed over")
        elif step["what"] == "came back":
            how = "written on by the model" if step["by_hand"] else f"bands {step['filled']}"
            lines.append(f"{step['step']:02d}. **came back** {step['sheet']} — {how}")
        else:
            lines.append(f"{step['step']:02d}. {step['what']} {_without(step, ('step',))}")
    lines += [
        "",
        "## Ink",
        "",
        *(f"- {name}: {share} % of the sheet" for name, share in ink.items()),
        "",
        "## How it went",
        "",
        "_Written after looking at the pages. What an assertion cannot say._",
        "",
    ]
    (folder / "notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(name: str, *, by: str, hand: str, times: int, step: float, pause: float) -> int:
    from tools.pretend import PAUSE_SECONDS, load_experience, play

    folder = next_folder(WHERE, name)
    the_afternoon = load_experience(Path("experiences/un-pomeriggio-di-nuvole.json"))
    waited = PAUSE_SECONDS if pause < 0 and by else max(0.0, pause)

    worst = 0
    for number in range(1, times + 1):
        one = folder if times == 1 else folder / f"try-{number:02d}"
        print(f"\n-- {one} --")
        began = time.monotonic()
        outcome = play(one / "house", the_afternoon, hand, step, by, waited)
        seconds = time.monotonic() - began
        worst = max(worst, outcome)
        steps = flow_of(one / "house", one / "flow")
        write_notes(
            one,
            asked={
                "afternoon": "un-pomeriggio-di-nuvole",
                "hand": by or f"drawn bands ({hand})",
                "outcome": "reached an ending" if outcome == 0 else "stopped early",
            },
            steps=steps,
            seconds=seconds,
        )
        print(f"   {one / 'notes.md'}")
    return worst


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an experiment on the simulated house.")
    verbs = parser.add_subparsers(dest="verb", required=True)
    running = verbs.add_parser("run", help="play an afternoon and keep everything it made")
    running.add_argument("name", help="what this experiment is trying")
    running.add_argument("--by", default="", help=f"a hand: {', '.join(HANDS)}")
    running.add_argument("--hand", default="marks", help="drawn bands, when --by is not given")
    running.add_argument("--times", type=int, default=1)
    running.add_argument("--step", type=float, default=0.0, help="minutes between pages")
    running.add_argument("--pause", type=float, default=-1.0)
    asked = parser.parse_args(argv)
    return run(
        asked.name,
        by=asked.by,
        hand=asked.hand,
        times=asked.times,
        step=asked.step,
        pause=asked.pause,
    )


if __name__ == "__main__":
    raise SystemExit(main())
