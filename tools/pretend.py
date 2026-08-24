"""Run an afternoon in a house with no person in it, and see what happened.

Every verb here stands for something somebody would have done: taking the sheet, writing on
it, laying it on the glass, waiting. Nothing here stands for something the system does — the
model, the checks, the page, the reading and the runner are the real ones, and the reason is
in :mod:`devices.pretend`.

    python -m tools.pretend devise                    ask the real service for one
    python -m tools.pretend begin                     play it until it wants a page
    python -m tools.pretend look                      what the display says, what is on the table
    python -m tools.pretend hand marks                write in one place and lay it on the glass
    python -m tools.pretend hand blank                lay it back untouched
    python -m tools.pretend hand all                  fill every place
    python -m tools.pretend hand c1,una-parola        fill the places named
    python -m tools.pretend wait 150                  let a hundred and fifty minutes pass
    python -m tools.pretend play --hand marks         all of the above, until it ends
    python -m tools.pretend transcript                what happened, in order
    python -m tools.pretend forget                    throw the afternoon away and start again

``play`` is the one that matters when nobody is at the keyboard: it begins, hands the sheet
back however it was told to, and keeps going until the afternoon closes or asks for
something it was not told how to answer. What it costs is the model calls it makes on the
way, which are real and are paid for.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

from devices import pretend as simulated
from devices.house import CannotRun, House
from devices.pretend import Pretend
from devices.print_sheet import recall
from devices.run_experience import (
    Afternoon,
    begin,
    carry_on,
    conclude_what_is_over,
    load_experience,
    waiting_runs,
)
from shared.capabilities import HouseCapability
from shared.experience import Experience, ExperienceError
from shared.ids import SheetId

WHERE = Path(os.environ.get(simulated.PRETEND_DIR_ENV, "") or "pretend")

# How many pages one `play` will hand back before it stops. An afternoon has at most twelve
# moments and a collect cannot repeat, so more than a dozen means something is looping and
# the loop is more interesting than the afternoon.
MOST_PAGES = 12

# Where the panel URL, the household and the device key live on a development machine.
# Read here rather than exported into a shell, because a shell that fails while setting an
# environment variable prints the value it was setting — which is how a device key ends up
# in a terminal transcript. This file is gitignored and never leaves the machine.
SECRETS = Path("secrets.local.yaml")


def _the_panel() -> tuple[str, str, str]:
    """The panel URL, household and device key: from the environment, or from the file.

    The environment wins, so the same tool runs on a machine that has no such file.
    Nothing here is printed, and the key is never put in an argument.
    """
    panel = os.environ.get("LANTERNINA_PANEL_URL", "").rstrip("/")
    household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
    key = os.environ.get("LANTERNINA_DEVICE_KEY", "")
    if panel and household and key:
        return panel, household, key
    try:
        import yaml  # type: ignore[import-untyped]

        kept = yaml.safe_load(SECRETS.read_text(encoding="utf-8")) or {}
    except (OSError, ValueError, ImportError):
        return panel, household, key
    return (
        panel or str(kept.get("panel_url", "")).rstrip("/"),
        household or str(kept.get("household", "")),
        key or str(kept.get("device_key", "")),
    )


def a_house(where: Path) -> House:
    """A house with no equipment and a directory to write into.

    The panel, the household and the device key are the real ones, because the page is read
    by the real model. Without them the afternoon stops at its first collect, which is what
    a house with no cloud does.
    """
    panel, household, key = _the_panel()
    return House(
        sheets_dir=where / "state",
        panel=panel,
        household=household,
        device_key=key,
        pretend=where,
    )


def _kept(where: Path) -> Path:
    return where / "afternoon.json"


def _the_afternoon(where: Path) -> Experience:
    path = _kept(where)
    if not path.is_file():
        raise SystemExit(f"there is no afternoon in {where}; run `devise` or pass --experience")
    return load_experience(path)


# ── Asking the real service for one ──────────────────────────────────────────────────


def devise(where: Path, language: str, interests: tuple[str, ...], avoid: tuple[str, ...]) -> int:
    """Devise, check, repair and screen one afternoon, against the deployment the hub uses."""
    from panel.devising import RefusedByTheChecks, devise_experience

    # The refusals and the repairs are logged at INFO and are the most interesting thing
    # this verb produces: a check that fires every time is a defect in the prompt. Only
    # that logger — the Azure SDKs log every request header at INFO and bury it.
    logging.basicConfig(level=logging.WARNING, format="  %(message)s")
    logging.getLogger("panel.devising").setLevel(logging.INFO)

    began = time.monotonic()
    try:
        experience, spent = asyncio.run(
            devise_experience(
                capabilities=frozenset(
                    {
                        HouseCapability.SHOW_800X480_1BIT,
                        HouseCapability.PRINT_A4,
                        HouseCapability.SCAN_A4,
                    }
                ),
                language=language,
                interests=interests,
                avoid=avoid,
                already=(),
                now=time.time(),
            )
        )
    except RefusedByTheChecks as exc:
        print(f"refused after its repair: {exc}")
        return 1
    except (ExperienceError, ValueError, RuntimeError) as exc:
        print(f"no afternoon: {type(exc).__name__}: {exc}")
        return 1
    took = time.monotonic() - began
    where.mkdir(parents=True, exist_ok=True)
    _kept(where).write_text(
        json.dumps(experience.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    simulated.note(
        Pretend(where),
        "devised",
        experience_id=experience.experience_id,
        title=experience.title,
        seconds=round(took, 1),
    )
    print(f"{experience.title} — {len(experience.moments)} moments, {experience.minutes} min")
    print(f"  {took:.1f} s, spent {spent}")
    print(f"  written to {_kept(where)}")
    return 0


# ── Playing it ───────────────────────────────────────────────────────────────────────


def start(where: Path, experience: Experience) -> int:
    house = a_house(where)
    if waiting_runs(house.sheets_dir):
        print("an afternoon is already under way; `forget` first")
        return 1
    run_id = begin(house, experience, now=simulated.the_time(Pretend(where)), send=False)
    print(f"{experience.title}: {run_id or 'closed without asking for paper'}")
    return 0


def look(where: Path) -> int:
    house = a_house(where)
    pretend = Pretend(where)
    lines = [line for line in simulated.read_transcript(pretend) if line["what"] == "display"]
    if lines:
        last = lines[-1]
        print("the display says:")
        print(f"  {last['heading']}")
        for line in last["lines"]:
            print(f"  {line}")
        print(f"  ({pretend.display / 'latest.png'})")
    on_the_table = simulated.sheets_on_the_table(pretend)
    print(f"on the table: {', '.join(on_the_table) or 'nothing'}")
    for sheet_id in on_the_table:
        try:
            spec = recall(house.sheets_dir, SheetId(sheet_id))
        except (OSError, ValueError):
            continue
        print(f"  {sheet_id}: {spec.title}")
        for cell in spec.cells:
            print(f"    {cell.id} ({cell.kind}) {cell.label}")
    for run_id in waiting_runs(house.sheets_dir):
        run = _run(house, run_id)
        if run is None:
            continue
        left = (run.over_at - simulated.the_time(pretend)) / 60.0
        print(f"waiting at {run.waiting_at!r} on the {run.weight} weight, {left:.0f} min left")
        if run.leaving_at:
            print(f"  the ending has begun, from {run.leaving_at!r}")
    return 0


def _run(house: House, run_id: str) -> Afternoon | None:
    path = house.sheets_dir / "afternoons" / f"{run_id}.json"
    try:
        return Afternoon.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, ExperienceError):
        return None


def hand(where: Path, asked: str) -> int:
    """Write in the places asked for and lay the sheet on the glass, then carry on."""
    house = a_house(where)
    pretend = Pretend(where)
    on_the_table = simulated.sheets_on_the_table(pretend)
    if not on_the_table:
        print("there is no sheet on the table")
        return 1
    sheet_id = on_the_table[-1]
    spec = recall(house.sheets_dir, SheetId(sheet_id))
    try:
        filled = simulated.which_places(spec, asked)
    except ValueError as exc:
        print(exc)
        return 1
    simulated.put_on_the_glass(pretend, sheet_id, filled)
    print(f"{sheet_id} on the glass, ink in {list(filled) or 'nothing'}")
    try:
        print(carry_on(house, now=simulated.the_time(pretend), send=False))
    except (CannotRun, ExperienceError, OSError) as exc:
        print(f"it stopped: {exc}")
        return 1
    return 0


def wait(where: Path, minutes: float) -> int:
    """Let time pass, and give the house its ten-minute look while it does.

    The look is the point: the ending starts by itself thirty minutes before the end hour,
    and nothing else in this file would ever reach it.
    """
    house = a_house(where)
    pretend = Pretend(where)
    simulated.move_on(pretend, minutes * 60.0)
    for run_id in conclude_what_is_over(house, simulated.the_time(pretend), send=False):
        print(f"{run_id} reached its ending and is over")
    print(f"{minutes:.0f} minutes later")
    return 0


def play(where: Path, experience: Experience, asked: str, step_minutes: float) -> int:
    """Begin, and keep handing pages back until the afternoon ends.

    Stops of its own accord when there is nothing on the table and nothing waiting, which is
    an afternoon that closed. Stops with a word when it has handed back more pages than an
    afternoon can have, which is a loop.
    """
    house = a_house(where)
    pretend = Pretend(where)
    if waiting_runs(house.sheets_dir):
        print("an afternoon is already under way; `forget` first")
        return 1
    if start(where, experience) != 0:
        return 1

    for _ in range(MOST_PAGES):
        if not waiting_runs(house.sheets_dir):
            print("the afternoon is over")
            return 0
        if step_minutes:
            simulated.move_on(pretend, step_minutes * 60.0)
            for run_id in conclude_what_is_over(house, simulated.the_time(pretend), send=False):
                print(f"{run_id} reached its ending and is over")
            if not waiting_runs(house.sheets_dir):
                print("the afternoon is over")
                return 0
        if hand(where, asked) != 0:
            return 1
    print(f"it handed back {MOST_PAGES} pages and is still going; something is looping")
    return 1


# ── Looking at what happened ─────────────────────────────────────────────────────────


def transcript(where: Path) -> int:
    began = 0.0
    for line in simulated.read_transcript(Pretend(where)):
        began = began or float(line["at"])
        when = float(line["at"]) - began
        print(f"{when:7.1f}s {line['what']:9s} {_said(line)}")
    return 0


def _said(line: dict[str, Any]) -> str:
    what = line["what"]
    if what == "display":
        return f"{line['heading']} | {' / '.join(line['lines'])}"
    if what == "paper":
        return f"{line['sheet_id']} {line['title']} [{', '.join(line['places'])}]"
    if what == "glass":
        inked = [place["place"] for place in line["read"] if place["ink"]]
        return (
            f"{line['sheet_id']} written in {line['filled']}, "
            f"read as ink in {inked or 'nothing'}"
        )
    if what == "clock":
        return f"+{float(line['added_seconds']) / 60:.0f} min"
    if what == "devised":
        return f"{line['title']} in {line['seconds']} s"
    rest = {key: value for key, value in line.items() if key not in ("at", "what")}
    return json.dumps(rest, ensure_ascii=False)


def forget(where: Path) -> int:
    """Throw away the run, the paper and the transcript. The afternoon document stays."""
    import shutil

    for part in (Pretend(where).display, Pretend(where).paper, where / "state"):
        shutil.rmtree(part, ignore_errors=True)
    for part in (Pretend(where).glass, Pretend(where).clock, Pretend(where).transcript):
        part.unlink(missing_ok=True)
    print(f"{where} is empty again")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an afternoon with nobody in the house.")
    parser.add_argument("--where", type=Path, default=WHERE)
    parser.add_argument("--experience", type=Path, help="a document, instead of the devised one")
    verbs = parser.add_subparsers(dest="verb", required=True)

    devising = verbs.add_parser("devise", help="ask the real service for an afternoon")
    devising.add_argument("--language", default="italiano")
    devising.add_argument("--interests", default="")
    devising.add_argument("--avoid", default="")

    verbs.add_parser("begin", help="play it until it wants a page back")
    verbs.add_parser("look", help="what the display says and what is on the table")

    handing = verbs.add_parser("hand", help="write on the sheet and lay it on the glass")
    handing.add_argument("how", help="marks, blank, all, or a comma-separated list of places")

    waiting = verbs.add_parser("wait", help="let minutes pass, and let the house look")
    waiting.add_argument("minutes", type=float)

    playing = verbs.add_parser("play", help="begin and keep going until it ends")
    playing.add_argument("--hand", default="marks")
    playing.add_argument("--step", type=float, default=0.0, help="minutes between pages")

    verbs.add_parser("transcript", help="what happened, in order")
    verbs.add_parser("forget", help="throw the run away and start again")

    args = parser.parse_args(argv)
    where: Path = args.where

    if args.verb == "devise":
        return devise(
            where,
            args.language,
            tuple(w.strip() for w in args.interests.split(",") if w.strip()),
            tuple(w.strip() for w in args.avoid.split(",") if w.strip()),
        )
    if args.verb == "look":
        return look(where)
    if args.verb == "transcript":
        return transcript(where)
    if args.verb == "forget":
        return forget(where)
    if args.verb == "wait":
        return wait(where, args.minutes)
    if args.verb == "hand":
        return hand(where, args.how)

    chosen = load_experience(args.experience) if args.experience else _the_afternoon(where)
    if args.verb == "begin":
        return start(where, chosen)
    return play(where, chosen, args.hand, args.step)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("stopped", file=sys.stderr)
        raise SystemExit(130) from None
