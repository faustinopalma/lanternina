"""Costruisce l'albero di `forme/` a partire da `docs/EXERCISE-FORMS.md`.

    python tools/forme_scaffold.py            # crea le cartelle mancanti
    python tools/forme_scaffold.py --index    # riscrive solo forme/INDICE.md

L'enciclopedia resta l'unica lista: una cartella qui esiste perche' una voce esiste la',
e cambiare l'elenco significa cambiare quel file e rieseguire questo. Le cartelle gia'
scritte non vengono mai toccate — lo script aggiunge, non sovrascrive.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "EXERCISE-FORMS.md"
WHERE = ROOT / "forme"

CHAPTER = re.compile(r"^## (\d+)\. (.+)$")
SECTION = re.compile(r"^### (\d+)\.(\d+) (.+)$")
METHOD = re.compile(r"^(\d+)\. \*\*(.+?)\*\* — (.+)$")

MARKS = {"✗": "chiuso", "⚠": "costoso", "⊘": "irraggiungibile"}


@dataclass(frozen=True)
class Method:
    number: int
    name: str
    gloss: str
    chapter: int
    chapter_name: str
    section: str

    @property
    def mark(self) -> str:
        for sign, word in MARKS.items():
            if sign in self.gloss:
                return f"{sign} {word}"
        return "aperto"


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


TEMPLATE = """# {name}

- **Numero** {number} nell'enciclopedia, capitolo {chapter} — {chapter_name}{section}
- **Come la classifica l'enciclopedia** {mark}
- **In una riga** {gloss}
- **Stato della ricerca** non ancora fatta

## Che cos'è

## Da dove viene

## Che cosa se ne sa

## Esempi trovati

## Una nostra versione

## Che cosa cambia per noi
"""


def write_one(method: Method) -> bool:
    where = folder(method)
    page = where / "README.md"
    if page.exists():
        return False
    where.mkdir(parents=True, exist_ok=True)
    page.write_text(
        TEMPLATE.format(
            name=method.name,
            number=method.number,
            chapter=method.chapter,
            chapter_name=method.chapter_name,
            section=f", sezione «{method.section}»" if method.section else "",
            mark=method.mark,
            gloss=method.gloss,
        ),
        encoding="utf-8",
    )
    return True


def write_index(methods: list[Method]) -> None:
    done = sum(1 for one in methods if "non ancora fatta" not in _state(one))
    lines = [
        "# Indice delle forme",
        "",
        f"{len(methods)} forme, {done} con la ricerca fatta. "
        "Generato da `tools/forme_scaffold.py --index`; non si modifica a mano.",
        "",
    ]
    chapter = 0
    for method in methods:
        if method.chapter != chapter:
            chapter = method.chapter
            lines += ["", f"## {chapter}. {method.chapter_name}", ""]
        where = folder(method).relative_to(WHERE).as_posix()
        state = "fatta" if "non ancora fatta" not in _state(method) else "—"
        lines.append(
            f"{method.number}. [{method.name}]({where}/README.md) · {method.mark} · {state}"
        )
    (WHERE / "INDICE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _state(method: Method) -> str:
    page = folder(method) / "README.md"
    if not page.exists():
        return "non ancora fatta"
    for line in page.read_text(encoding="utf-8").splitlines():
        if line.startswith("- **Stato della ricerca**"):
            return line
    return "non ancora fatta"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", action="store_true", help="riscrive solo l'indice")
    only_index = parser.parse_args().index
    methods = read()
    made = 0 if only_index else sum(write_one(one) for one in methods)
    write_index(methods)
    print(f"{len(methods)} forme lette da {SOURCE.name}, {made} cartelle nuove")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
