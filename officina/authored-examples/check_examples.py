from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from itertools import permutations, product
from pathlib import Path
from statistics import mean

from shared.page import Page

ROOT = Path(__file__).resolve().parent
SECTIONS = (
    "Household brief",
    "Parent output",
    "Script output",
    "Cycle 1",
    "Closing output",
    "Alternative returns",
    "Comparison checks",
)


def inspect_example(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    for heading in SECTIONS:
        if f"## {heading}\n" not in text:
            raise ValueError(f"{path.name}: missing {heading}")
    if not text.endswith("\n"):
        raise ValueError(f"{path.name}: no final newline")
    cycles = re.findall(r"^## (Cycle \d+|Final page)\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    pages = 0
    for heading, cycle in cycles:
        blocks = re.findall(r"```json\n(.*?)\n```", cycle, re.S)
        if len(blocks) != 1:
            raise ValueError(f"{path.name}: {heading} needs one page object")
        page = Page.from_dict(json.loads(blocks[0]))
        prompts = re.findall(
            r"### Image prompt(?: - (?:cycle \d+|final page))?\n\n```text\n(.*?)\n```",
            cycle,
            re.S,
        )
        if len(prompts) != 1:
            raise ValueError(f"{path.name}: {heading} needs one image prompt")
        quoted = re.findall(r'"([^"\n]+)"', prompts[0])
        if Counter(quoted) != Counter(page.words()):
            raise ValueError(
                f"{path.name}: {heading} prompt words differ from page.words(): "
                f"expected={page.words()!r}, quoted={quoted!r}"
            )
        display = re.search(r"^### Display(?: - cycle \d+)?$", cycle, re.M)
        if heading.startswith("Cycle") and display is None:
            raise ValueError(f"{path.name}: {heading} has no display output")
        pages += 1
    if pages == 0:
        raise ValueError(f"{path.name}: no pages")
    all_page_blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    if len(all_page_blocks) != pages:
        raise ValueError(f"{path.name}: a page exists outside checked sections")
    for phrase in ("photograph", "unchanged", "stop"):
        alternative = text.split("## Alternative returns\n", 1)[1].lower()
        if phrase not in alternative:
            raise ValueError(f"{path.name}: alternative cases omit {phrase}")
    check_reasoning(path, text)
    print(f"OK {path.name}: {pages} pages, exact prompt text")
    return pages


def check_reasoning(path: Path, text: str) -> None:
    if not path.name.startswith(("11-", "12-", "13-", "14-")):
        return
    page = Page.from_dict(json.loads(re.findall(r"```json\n(.*?)\n```", text, re.S)[0]))
    if path.name.startswith("11-"):
        cards_needed, clips_needed, budget = map(int, re.findall(r"\d+", page.note[0]))
        cards_small, cards_price, cards_large, cards_large_price = map(
            int, re.findall(r"\d+", page.note[1])
        )
        clips_small, clips_price, clips_large, clips_large_price = map(
            int, re.findall(r"\d+", page.note[2])
        )
        prices = (cards_price, cards_large_price, clips_price, clips_large_price)
        feasible = []
        for counts in product(*(range(budget // price + 1) for price in prices)):
            if cards_small * counts[0] + cards_large * counts[1] < cards_needed:
                continue
            if clips_small * counts[2] + clips_large * counts[3] < clips_needed:
                continue
            cost = sum(count * price for count, price in zip(counts, prices, strict=True))
            if cost <= budget:
                feasible.append((cost, counts))
        cheapest = min(cost for cost, _ in feasible)
        winners = [counts for cost, counts in feasible if cost == cheapest]
        if (cheapest, winners) != (17, [(3, 0, 1, 1)]):
            raise ValueError(f"{path.name}: claimed unique 17-euro minimum is not supported")
    elif path.name.startswith("12-"):
        conditions = "A segue subito C. D precede C. B non apre e non chiude."
        if page.note[1] != conditions:
            raise ValueError(f"{path.name}: update the proof check for changed conditions")
        solutions = [
            order
            for order in permutations("ABCD")
            if order.index("A") == order.index("C") + 1
            and order.index("D") < order.index("C")
            and order.index("B") in (1, 2)
        ]
        if solutions != [tuple("DBCA")]:
            raise ValueError(f"{path.name}: claimed unique order is not supported")
    elif path.name.startswith("13-"):
        averages = [mean(map(int, re.findall(r"\d+", line))) for line in page.note[1:3]]
        if averages != [27, 24] or averages[0] - averages[1] != 3:
            raise ValueError(f"{path.name}: claimed means or difference are not supported")
    else:
        returned = text.split("### Hypothetical return - cycle 1\n", 1)[1]
        passage = re.search(r"```text\n(.*?)\n```", returned, re.S)
        if passage is None or len(passage[1].split()) != 88:
            raise ValueError(f"{path.name}: claimed 88-word transcription is not supported")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-count", type=int, default=14)
    arguments = parser.parse_args()
    paths = sorted(ROOT.glob("[0-9][0-9]-*.md"))
    if len(paths) < arguments.min_count:
        raise ValueError(f"Expected {arguments.min_count} examples, found {len(paths)}")
    pages = sum(inspect_example(path) for path in paths)
    print(f"Verified {len(paths)} examples and {pages} page/prompt pairs; no model calls.")


if __name__ == "__main__":
    started = time.perf_counter()
    try:
        main()
    finally:
        print(f"elapsed: {time.perf_counter() - started:.2f}s")
