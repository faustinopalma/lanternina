"""Controlla che le voci in `enciclopedia/` rispettino il contratto.

    python tools/enciclopedia_check.py

Serve perche' le voci sono state scritte in sessioni diverse e da chi non aveva letto le
altre, e la qualita' di un'enciclopedia sta nel fatto che ogni voce sia fatta come le
altre. Il controllo e' su quello che si puo' controllare a macchina: le sette sezioni ci
sono tutte, nell'ordine, e nessuna e' vuota; l'intestazione ha i suoi campi; un rimando a
un'altra voce porta il nome accanto al numero, perche' chi legge una voce sola non ha
l'elenco in mente; e non e' rimasto niente che il lettore non possa raggiungere.

Quest'ultima parte esiste perche' l'enciclopedia e' stata compilata come ricerca interna e
citava le pagine scaricate per nome di file locale, gli script di lavoro e i quaderni di
sessione. Sono tutte cose che stanno in cartelle gitignored: chi apre il repository non le
ha, e una citazione che non si puo' aprire non e' una citazione.

Quello che non si controlla a macchina — se una fonte e' stata letta davvero, se l'esempio
regge, se una frase riscritta dice ancora quello che diceva — resta il mestiere di chi
scrive.

Esce con codice 1 se qualcosa non torna e con 2 se non ha trovato nessuna voce, perche' un
controllo che puo' passare su zero file non e' un controllo.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WHERE = Path(__file__).resolve().parents[1] / "enciclopedia"

SECTIONS = (
    "Che cos'è",
    "Da dove viene",
    "Varianti e parenti",
    "Che cosa se ne sa",
    "Esempi trovati",
    "Un esempio giocabile",
    "Che cosa la rende interessante",
)

# Come si chiama, che cos'e' in una riga, e da dove viene quello che c'e' scritto.
FIELDS = ("Numero", "Si chiama anche", "In una riga", "Fonti")

FIELD = re.compile(r"^- \*\*([^*]+)\*\*\s*(.*)$")
BARE = re.compile(r"\b(?:voce|scheda)\s+\d{1,3}\b(?!\s*[(,]|\s*\u2014)")

# Quello che il lettore non puo' aprire, e che quindi non deve piu' essere citato.
# Il primo modello ammette le barre di proposito: alcune voci citavano la pagina con il
# percorso intero, `_reference/esercizi-e-sfide/nome.txt`, e un modello senza barre le
# lasciava passare.
UNREACHABLE = (
    (re.compile(r"`[\w./-]*[\w.-]+\.txt`"), "cita una pagina scaricata per nome di file"),
    (re.compile(r"`?build/[\w.-]+\.py`?"), "cita uno script di lavoro"),
    (re.compile(r"`?(?:ideas|docs|_reference)/[\w./-]+`?"), "cita un file che il lettore non ha"),
    (re.compile(r"OSSERVAZIONI\.md|COME-SI-LAVORA\.md"), "cita un quaderno di lavoro"),
    (re.compile(r"^- \*\*Stato della ricerca\*\*", re.M), "ha la riga «Stato della ricerca»"),
    (re.compile(r"^- \*\*Contratto\*\* voce breve$", re.M), "ha ancora la riga «Contratto»"),
    (re.compile(r"\brassegn[ae]\b", re.I), "nomina la rassegna, un momento di lavoro interno"),
)


def check(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8")
    where = page.parent.name
    wrong: list[str] = []

    found = [line for line in text.splitlines() if line.startswith("## ")]
    if [line[3:] for line in found] != list(SECTIONS):
        wrong.append(f"{where}: le sezioni non sono quelle previste, nell'ordine previsto")

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

    for pattern, why in UNREACHABLE:
        for match in pattern.finditer(text):
            wrong.append(f"{where}: {why} — «{match[0].strip()}»")
    return wrong


def main() -> int:
    pages = sorted(WHERE.rglob("*/README.md"))
    if not pages:
        print(f"nessuna voce sotto {WHERE}: non c'è niente da controllare", file=sys.stderr)
        return 2
    wrong = [one for page in pages for one in check(page)]
    for line in wrong:
        print(line)
    print(f"\n{len(pages)} voci esaminate, {len(wrong)} cose da sistemare")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
