"""Estrae il testo leggibile dalle pagine scaricate in `_reference/esercizi-e-sfide/`.

    python tools/forme_text.py

Scrive un `.txt` accanto a ogni `.html`. Serve a poter leggere una fonte a pezzi invece
che intera: una pagina di Wikipedia sta fra i 400 kB e 1.6 MB di HTML e fra i 30 kB e i
120 kB di testo, e la differenza e' quello che si legge senza pagarlo tutto.

Nessuna libreria esterna: e' uno stripper, non un parser, e sbaglia sulle tabelle. Va
bene, perche' quello che si cerca qui sono i paragrafi.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

WHERE = Path(__file__).resolve().parents[1] / "_reference" / "esercizi-e-sfide"

# Wikipedia mette il corpo in <div id="mw-content-text">; fuori c'e' solo navigazione.
BODY = re.compile(r'<div [^>]*id="mw-content-text".*?>(.*)', re.S)
DROP = re.compile(r"<(script|style|table|figure|sup|noscript)\b.*?</\1>|<!--.*?-->", re.S | re.I)
BREAK = re.compile(r"</(p|li|h[1-6]|dd|dt|div)>", re.I)
HEADING = re.compile(r"<h([2-6])\b[^>]*>", re.I)
TAG = re.compile(r"<[^>]+>")
BLANK = re.compile(r"\n{3,}")


def strip(raw: str) -> str:
    if match := BODY.search(raw):
        raw = match[1]
    raw = DROP.sub(" ", raw)
    raw = HEADING.sub(lambda m: "\n\n" + "#" * int(m[1]) + " ", raw)
    raw = BREAK.sub("\n", raw)
    text = html.unescape(TAG.sub("", raw))
    text = "\n".join(line.strip() for line in text.splitlines())
    return BLANK.sub("\n\n", text).strip()


def main() -> int:
    pages = sorted(WHERE.glob("*.html"))
    for page in pages:
        text = strip(page.read_text(encoding="utf-8", errors="replace"))
        page.with_suffix(".txt").write_text(text, encoding="utf-8")
    total = sum(len(one.with_suffix(".txt").read_text(encoding="utf-8")) for one in pages)
    print(f"{len(pages)} pagine, {total // 1024} kB di testo in {WHERE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
