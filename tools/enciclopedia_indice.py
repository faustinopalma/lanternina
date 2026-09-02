"""Riscrive `enciclopedia/INDICE.md` a partire da `docs/EXERCISE-FORMS.md`.

    python tools/enciclopedia_indice.py

L'elenco in `docs/EXERCISE-FORMS.md` resta l'unica lista: una cartella dell'enciclopedia
esiste perche' una voce esiste la'. Questo script non scrive voci, riscrive solo l'indice,
e fallisce rumorosamente se una voce dell'elenco non ha la sua cartella.

Prima costruiva anche gli stub delle voci mancanti. Adesso le 395 ci sono tutte, e quel
pezzo scriveva un'intestazione che non e' piu' quella giusta: e' stato tolto invece di
essere aggiornato, perche' era una macchina per un lavoro finito.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "EXERCISE-FORMS.md"
WHERE = ROOT / "enciclopedia"

CHAPTER = re.compile(r"^## (\d+)\. (.+)$")
SECTION = re.compile(r"^### (\d+)\.(\d+) (.+)$")
METHOD = re.compile(r"^(\d+)\. \*\*(.+?)\*\* — (.+)$")


@dataclass(frozen=True)
class Method:
    number: int
    name: str
    gloss: str
    chapter: int
    chapter_name: str
    section: str


def slug(text: str) -> str:
    flat = unicodedata.normalize("NFKD", text.lower())
    flat = "".join(ch for ch in flat if not unicodedata.combining(ch))
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", flat)).strip("-")


def read() -> list[Method]:
    chapter, chapter_name, section = 0, "", ""
    found: list[Method] = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if match := CHAPTER.match(line):
            chapter, chapter_name, section = int(match[1]), match[2], ""
        elif match := SECTION.match(line):
            section = match[3]
        elif (match := METHOD.match(line)) and chapter:
            found.append(Method(int(match[1]), match[2], match[3], chapter, chapter_name, section))
    return found


def folder(method: Method) -> Path:
    return (
        WHERE
        / f"{method.chapter:02d}-{slug(method.chapter_name)}"
        / (f"{method.number:03d}-{slug(method.name)}")
    )


def write_index(methods: list[Method]) -> None:
    lines = [
        "# Le voci, in ordine",
        "",
        f"{len(methods)} voci in {methods[-1].chapter} capitoli. Generato da "
        "`tools/enciclopedia_indice.py`; non si modifica a mano.",
        "",
    ]
    chapter = 0
    for method in methods:
        if method.chapter != chapter:
            chapter = method.chapter
            lines += ["", f"## {chapter}. {method.chapter_name}", ""]
        where = folder(method).relative_to(WHERE).as_posix()
        lines.append(f"{method.number}. [{method.name}]({where}/README.md) — {method.gloss}")
    (WHERE / "INDICE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    methods = read()
    if not methods:
        print(f"nessuna voce letta da {SOURCE}", file=sys.stderr)
        return 2
    mancanti = [one for one in methods if not (folder(one) / "README.md").exists()]
    for one in mancanti:
        print(f"manca la cartella della voce {one.number}, {one.name}", file=sys.stderr)
    if mancanti:
        return 1
    write_index(methods)
    print(f"{len(methods)} voci, indice riscritto")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
