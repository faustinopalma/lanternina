from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from pathlib import Path

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
    print(f"OK {path.name}: {pages} pages, exact prompt text")
    return pages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-count", type=int, default=10)
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
