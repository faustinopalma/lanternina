"""Controlla che le schede in `forme/` rispettino il contratto.

    python tools/forme_check.py

Serve perche' le schede vengono scritte in sessioni diverse e da chi non ha letto le
altre, e la qualita' di un'enciclopedia sta nel fatto che ogni voce sia fatta come le
altre. Il controllo e' su quello che si puo' controllare a macchina: le sezioni ci sono
tutte, nell'ordine, e nessuna e' vuota; l'intestazione ha i suoi campi; e un rimando a
un'altra voce porta il nome accanto al numero, perche' chi legge una voce sola non ha
l'elenco in mente.

Quello che non si controlla a macchina — se una fonte e' stata letta davvero, se
l'esempio regge — resta il mestiere di chi scrive.

Esce con codice 1 se qualcosa non torna, cosi' puo' stare in un test o in una pipeline.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WHERE = Path(__file__).resolve().parents[1] / "forme"

SECTIONS = (
    "Che cos'è",
    "Da dove viene",
    "Varianti e parenti",
    "Che cosa se ne sa",
    "Esempi trovati",
    "Una nostra versione",
    "Da riprendere alla rassegna",
)

# Ogni scheda finita porta questi campi. Sono pochi di proposito: quello che una voce
# d'enciclopedia deve dire di se' e' come si chiama, che cos'e' in una riga, e da dove
# viene quello che c'e' scritto.
FIELDS = (
    "Numero",
    "Si chiama anche",
    "In una riga",
    "Fonti",
    "Stato della ricerca",
)

FIELD = re.compile(r"^- \*\*([^*]+)\*\*\s*(.*)$")
BARE = re.compile(r"\b(?:voce|scheda)\s+\d{1,3}\b(?!\s*[(,]|\s*\u2014)")


def done(text: str) -> bool:
    return "**Stato della ricerca** non ancora fatta" not in text


def check(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8")
    where = page.parent.name
    wrong: list[str] = []

    found = [line for line in text.splitlines() if line.startswith("## ")]
    if [line[3:] for line in found] != list(SECTIONS):
        wrong.append(f"{where}: le sezioni non sono quelle previste, nell'ordine previsto")

    if not done(text):
        return wrong

    fields = {m[1]: m[2] for line in text.splitlines() if (m := FIELD.match(line))}
    for name in FIELDS:
        if name not in fields:
            wrong.append(f"{where}: manca il campo «{name}»")
        elif not fields[name].strip():
            wrong.append(f"{where}: il campo «{name}» è vuoto")

    for one, next_one in zip(found, found[1:] + ["## fine"], strict=True):
        body = text.split(one, 1)[1].split(next_one, 1)[0].strip()
        if not body:
            wrong.append(f"{where}: la sezione «{one[3:]}» è vuota")

    for match in BARE.finditer(text):
        wrong.append(f"{where}: «{match[0]}» non porta il nome accanto, e da sola non dice niente")
    return wrong


def main() -> int:
    pages = sorted(WHERE.rglob("*/README.md"))
    wrong = [one for page in pages for one in check(page)]
    finished = sum(1 for page in pages if done(page.read_text(encoding="utf-8")))
    for line in wrong:
        print(line)
    print(f"\n{finished}/{len(pages)} schede fatte, {len(wrong)} cose da sistemare")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
