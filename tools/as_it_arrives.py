"""Read an afternoon the way somebody in the room meets it, and nothing else.

`tools/pretend.py` runs one for real and costs model calls. This reads a document already
written and prints only what would have reached a person: the words on the display, the
words lettered on the paper, and what each page asks for. Not the script, not the drawn
dimensions, not the reasoning — those are for us, and reading them is how a document that
nobody could follow keeps looking fine.

    python -m tools.as_it_arrives experiments/15-material-that-varies/03.json
    python -m tools.as_it_arrives experiments/15-material-that-varies --all

The one thing it adds is the count at the end, because the question it exists to answer is
whether a person could follow this: how many words arrive before anything is asked of them,
how long the sentences are, and how much of the whole thing is a display talking.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

BAR = "─" * 78


def _weight(moment: dict[str, Any], which: str = "standard") -> dict[str, Any]:
    weights = moment.get("weights") or {}
    if isinstance(weights, dict):
        return dict(weights.get(which) or weights.get("standard") or {})
    order = ("short", "standard", "extended")
    if not weights:
        return {}
    wanted = order.index(which) if which in order else 1
    return dict(weights[min(wanted, len(weights) - 1)])


def _help_lines(moment: dict[str, Any]) -> list[str]:
    """The ladder, which is what somebody stuck actually meets."""
    return [
        f"      ↳ dopo {rung.get('after_minutes', '?')} min: {' '.join(rung.get('lines') or ())}"
        for rung in moment.get("help") or ()
    ]


def _page_lines(page: dict[str, Any]) -> list[str]:
    """Everything lettered on one sheet, in the order a reader meets it."""
    said: list[str] = []
    if page.get("title"):
        said.append(f"    ┌─ {page['title']}")
    if page.get("illustration"):
        said.append(f"    │  (disegno: {page['illustration']})")
    for line in (*(page.get("note") or ()), *(page.get("lines") or ())):
        said.append(f"    │  {line}")
    for space in (*(page.get("spaces") or ()), *(page.get("cells") or ())):
        label = space.get("label") or ""
        room = space.get("room") or space.get("hint") or ""
        said.append(f"    │  [ {label}{f' — {room}' if room else ''} ]")
    return said


def read(document: dict[str, Any], *, weight: str = "standard") -> dict[str, Any]:
    """Print one afternoon as it arrives. Returns what was counted on the way."""
    print(BAR)
    print(f"  {document.get('title', '')}")
    print(f"  {document.get('overview', '')}")
    print(f"  {document.get('minutes', 0)} minuti")
    print(BAR)

    said_words = 0
    sentences: list[int] = []
    displays = 0
    pages = 0
    asked = 0
    first_ask: int | None = None

    for number, moment in enumerate(document.get("moments") or (), 1):
        act = moment.get("act", "")
        weighing = _weight(moment, weight)
        lines = list(weighing.get("lines") or ())
        heading = moment.get("heading", "")

        print(f"\n{number}. [{act}] {heading}")
        for line in lines:
            print(f"    {line}")
            said_words += len(line.split())
            sentences.append(len(line.split()))
        if act == "say":
            displays += 1
        page = moment.get("page")
        if page:
            pages += 1
            print("")
            for line in _page_lines(page):
                print(line)
            print("    └─")
        if act == "collect":
            asked += 1
            if first_ask is None:
                first_ask = said_words
            for outcome in moment.get("outcomes") or ():
                print(f"      · torna {outcome.get('when')} → {outcome.get('then')}")
        for rung in _help_lines(moment):
            print(rung)
        out = moment.get("way_out") or {}
        if out:
            print(f"      ⇥ via d'uscita, con «{out.get('in_hand', '')}»: {out.get('heading', '')}")

    print(f"\n{BAR}")
    counted = {
        "moments": len(document.get("moments") or ()),
        "displays": displays,
        "pages": pages,
        "asks": asked,
        "words": said_words,
        "longest_line": max(sentences) if sentences else 0,
        "median_line": int(statistics.median(sentences)) if sentences else 0,
        "words_before_the_first_ask": first_ask if first_ask is not None else said_words,
    }
    for name, value in counted.items():
        print(f"  {name:28} {value}")
    return counted


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="An afternoon as somebody in the room meets it.")
    parser.add_argument("where", type=Path)
    parser.add_argument("--weight", default="standard", choices=("short", "standard", "extended"))
    parser.add_argument("--all", action="store_true", help="every document in a directory")
    args = parser.parse_args(argv)

    paths = (
        sorted(args.where.glob("[0-9][0-9].json")) if args.all or args.where.is_dir()
        else [args.where]
    )
    every: list[dict[str, Any]] = []
    for path in paths:
        every.append(read(json.loads(path.read_text(encoding="utf-8")), weight=args.weight))

    if len(every) > 1:
        print(f"\n{BAR}\n  {len(every)} pomeriggi\n{BAR}")
        for name in every[0]:
            values = [one[name] for one in every]
            middle = int(statistics.median(values))
            print(f"  {name:28} {min(values)}–{max(values)}  mediana {middle}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
