"""Misura l'enciclopedia: che cosa contiene di gia' strutturato, e quanto se ne salverebbe.

    python tools/enciclopedia_censimento.py

Esiste perche' `ideas/11-the-methods.md` cita dei numeri, e un numero senza lo script che
lo produce invecchia male: l'enciclopedia e' ferma, ma chi legge fra un anno deve poter
rifare il conto invece di crederci.

Due misure, e sono due domande diverse. La prima e' che cosa c'e' dentro la prosa che una
macchina puo' usare \u2014 i rimandi fra voci, le parti mobili, il peso delle sezioni. La
seconda e' quante voci dichiarano da sole di non arrivare su un foglio, e per quale
ragione: un taglio fatto senza sapere quante voci tocca e' una scelta presa al buio.

Le ragioni sono cercate con le parole che le voci usano davvero. Il conto e' quindi una
soglia inferiore: una voce che dice la stessa cosa con altre parole non viene contata.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

WHERE = Path(__file__).resolve().parents[1] / "enciclopedia"

RIMANDO = re.compile(r"voce (\d{1,3}), ([^\n.,;:—]+)", re.IGNORECASE)
PARTE_MOBILE = re.compile(r"^- \*\*([^*]+)\*\*", re.M)
SEZIONE = re.compile(r"^## (.+)$", re.M)

# Le ragioni per cui una forma non arriva su un foglio, dette come le dicono le voci.
RAGIONI = {
    "il muro delle lettere dentro le parole": re.compile(
        r"non sa manipolare le lettere|lettere dentro le parole", re.I
    ),
    "serve una seconda persona": re.compile(
        r"serve una seconda persona|serve un'altra persona|chi gioca da solo|"
        r"più di una persona|due persone",
        re.I,
    ),
    "niente suono": re.compile(r"nessun canale sonoro|non ha un suono|non porta un suono", re.I),
    "niente video o movimento": re.compile(
        r"nessun canale video|non porta un filmato|non vede muoversi", re.I
    ),
    "serve un oggetto": re.compile(r"non fabbrica oggetti|gli oggetti bisogna procurarseli", re.I),
    "costa a un adulto": re.compile(r"costa lavoro a un adulto|chi allestisce paga", re.I),
    "dichiara dove si romperebbe": re.compile(r"[Dd]ove si romperebbe|si romperebbe", re.I),
}


def sezioni(testo: str) -> dict[str, str]:
    titoli = SEZIONE.findall(testo)
    pezzi: dict[str, str] = {}
    for uno, dopo in zip(titoli, titoli[1:] + [None], strict=True):
        corpo = testo.split(f"## {uno}", 1)[1]
        pezzi[uno] = corpo.split(f"## {dopo}", 1)[0] if dopo else corpo
    return pezzi


def main() -> int:
    voci = sorted(WHERE.glob("*/*/README.md"))
    if not voci:
        print(f"nessuna voce sotto {WHERE}: non c'è niente da misurare", file=sys.stderr)
        return 2

    archi: set[tuple[str, str]] = set()
    citate: Counter[str] = Counter()
    parti = 0
    senza_parti = 0
    peso: Counter[str] = Counter()
    per_ragione: Counter[str] = Counter()
    per_capitolo: dict[str, Counter[str]] = {}
    quante: Counter[str] = Counter()

    for p in voci:
        testo = p.read_text(encoding="utf-8")
        pezzi = sezioni(testo)
        capitolo = p.parent.parent.name
        quante[capitolo] += 1
        per_capitolo.setdefault(capitolo, Counter())

        propri = set(RIMANDO.findall(testo))
        archi.update((p.parent.name, n) for n, _ in propri)
        for numero, _ in propri:
            citate[numero] += 1

        n = len(PARTE_MOBILE.findall(pezzi.get("Che cos'è", "")))
        parti += n
        senza_parti += n == 0

        for nome, corpo in pezzi.items():
            peso[nome] += len(corpo)

        for nome, pat in RAGIONI.items():
            if pat.search(testo):
                per_ragione[nome] += 1
                per_capitolo[capitolo][nome] += 1

    print(f"voci: {len(voci)} in {len(quante)} capitoli\n")

    print("== che cosa c'è già di strutturato")
    print(f"rimandi «voce N, nome»: {len(archi)} archi, {len(archi) / len(voci):.1f} per voce")
    print(f"   voci mai citate da nessun'altra: {len(voci) - len(citate)}")
    print(f"parti mobili: {parti}, {parti / len(voci):.1f} per voce")
    print(f"   voci che non ne elencano: {senza_parti}")
    print("peso delle sezioni:")
    tot = sum(peso.values())
    for nome, n in peso.most_common():
        print(f"   {n * 100 / tot:5.1f}%  {n // len(voci):5} car/voce   {nome}")

    print("\n== quante voci dichiarano da sole di non arrivare su un foglio")
    for nome, n in per_ragione.most_common():
        print(f"   {n:4}  {nome}")

    print("\n== per capitolo")
    for capitolo in sorted(quante):
        dette = ", ".join(f"{n}×{k}" for k, n in per_capitolo[capitolo].most_common(2)) or "—"
        print(f"   {capitolo:42} {quante[capitolo]:3} voci   {dette}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
