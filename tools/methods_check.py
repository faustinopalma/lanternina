"""Controlla il manuale: che ogni record stia nel contratto e non prometta cose che non sono.

    python tools/methods_check.py

Il manuale nasce in parallelo, molte voci alla volta, e un artefatto scritto in parallelo
sbaglia in modo uniforme: la stessa svista in trenta file. Questo strumento e' quello che
si legge prima di credere all'insieme.

Non giudica se un metodo sia buono. Controlla il contratto, che i nomi non si ripetano —
un nome che si ripete e' esattamente cio' che il manuale esiste per evitare — e che i
rimandi all'enciclopedia portino a voci che esistono davvero.

Esce 2 se non trova nessun record: un controllo che puo' passare su zero file non e' un
controllo.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parents[1]
METHODS = HERE / "methods"
ENCICLOPEDIA = HERE / "enciclopedia"

ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,47}$")

FIELDS: dict[str, type | tuple[type, ...]] = {
    "format_version": int,
    "method_id": str,
    "kind": str,
    "name": str,
    "also": list,
    "one_line": str,
    "from_entries": list,
    "how": str,
    "knobs": list,
    "where_the_work_is": str,
    "breaks": str,
    "adult_cost": str,
    "verification": str,
    "comes_back": str,
    "people": int,
    "letters_inside_words": str,
    "goes_with": list,
}

ENUMS: dict[str, set[Any]] = {
    "kind": {"form", "move"},
    "adult_cost": {"none", "prepare", "take_part"},
    # `in_the_object` esiste perche' il capitolo 13 lo ha preteso: le forbici, il compasso e
    # una striscia di carta decidono da soli, senza il foglio e senza nessuno. Scriverlo
    # `in_the_sheet` faceva contraddire il record con il proprio campo `breaks`.
    "verification": {"in_the_sheet", "in_the_object", "needs_a_person", "nowhere"},
    "comes_back": {"nothing", "a_sheet", "a_photograph"},
    # Chi compone non e' chi risolve. Un crittarismo si risolve facendo una somma e non
    # guardando dentro le parole; comporlo e' una ricerca dentro le parole, ed e' quella che
    # un modello sbaglia. Un booleano solo non sapeva dirlo.
    #
    # Dei quattro valori ne resta ammesso uno. Il 3 settembre 2026 i 24 record che valevano
    # `to_solve`, `to_compose` o `both` sono stati tolti: il manuale dichiara di raccogliere
    # «metodi che si possono davvero eseguire in casa», e di questi nessuna delle due meta'
    # si puo'. Comporre e' l'operazione che un modello linguistico sbaglia senza potersene
    # accorgere; risolvere e' quella che `shared/experience_prompt.only-what-you-can-answer.md`
    # non chiede a un lettore, per un motivo che viene da W3C COGA e non da un modello.
    # Il campo resta, con un valore solo, perche' e' il controllo che impedisce di rimetterli:
    # `shared/methods.py` li filtrerebbe comunque in silenzio, e un record che nessuno serve
    # e' un record che nessuno corregge.
    "letters_inside_words": {"no"},
    "people": {1, 2},
}

# Perche' questi numeri: `name` deve stare in `Drawn.mechanic`, che tronca a 60 caratteri.
# Gli altri vengono da come sono venuti i record, non da un budget. Misurati su 157 record il
# 3 settembre 2026: `how` ha mediana 643 e massimo 818, il totale mediana 2 292 e massimo
# 2 814. I tetti stanno sopra il massimo osservato di proposito — tenuti piu' bassi facevano
# da bersaglio, e il novantesimo percentile finiva a tre caratteri dal tetto.
LIMITS: dict[str, tuple[int, int]] = {
    "name": (8, 60),
    "one_line": (20, 160),
    "how": (150, 850),
    "where_the_work_is": (40, 300),
}


def entries() -> set[int]:
    found: set[int] = set()
    for d in ENCICLOPEDIA.glob("*/*/"):
        head = d.name.split("-", 1)[0]
        if head.isdigit():
            found.add(int(head))
    return found


def folded(text: str) -> str:
    return " ".join(text.lower().split())


def one(path: Path, known: set[int], said: dict[str, str]) -> list[str]:
    bad: list[str] = []
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"non si legge come JSON: {exc}"]
    if not isinstance(record, dict):
        return ["un record è un oggetto JSON"]

    missing = [k for k in FIELDS if k not in record]
    if missing:
        bad.append(f"campi che mancano: {', '.join(missing)}")
    extra = [k for k in record if k not in FIELDS]
    if extra:
        bad.append(f"campi che non esistono nel contratto: {', '.join(extra)}")

    for key, want in FIELDS.items():
        if key in record and not isinstance(record[key], want):
            bad.append(
                f"«{key}» dovrebbe essere {want.__name__ if isinstance(want, type) else want}"
            )

    if record.get("format_version") != 1:
        bad.append("format_version deve essere 1")

    mid = record.get("method_id", "")
    if isinstance(mid, str):
        if not ID.match(mid):
            bad.append(f"method_id «{mid}» non è minuscole, cifre e trattini fra 3 e 48 caratteri")
        if mid != path.stem:
            bad.append(f"il file si chiama «{path.stem}» e il method_id è «{mid}»")

    for key, allowed in ENUMS.items():
        if key in record and record[key] not in allowed:
            bad.append(f"«{key}» = {record[key]!r}, e i valori sono {sorted(map(str, allowed))}")

    for key, (lo, hi) in LIMITS.items():
        value = record.get(key)
        if isinstance(value, str) and not lo <= len(value) <= hi:
            bad.append(f"«{key}» è lungo {len(value)}, e deve stare fra {lo} e {hi}")

    breaks = record.get("breaks")
    if isinstance(breaks, str) and len(breaks) > 600:
        bad.append(f"«breaks» è lungo {len(breaks)}, e il massimo è 600")

    name = record.get("name")
    if isinstance(name, str) and name.strip():
        key = folded(name)
        if key in said:
            bad.append(
                f"il nome «{name}» è già di {said[key]}: "
                "due metodi con lo stesso nome non si distinguono"
            )
        else:
            said[key] = path.name

    knobs = record.get("knobs")
    if isinstance(knobs, list):
        if not 2 <= len(knobs) <= 5:
            bad.append(f"«knobs» ne ha {len(knobs)}, e ne servono fra 2 e 5")
        for i, k in enumerate(knobs, 1):
            if not isinstance(k, dict) or set(k) != {"knob", "effect"}:
                bad.append(f"il knob {i} deve avere esattamente «knob» e «effect»")
                continue
            if len(str(k["effect"])) < 40:
                bad.append(
                    f"il knob {i} dice che c'è una manopola e non che cosa succede a girarla"
                )
            if len(str(k["effect"])) > 280:
                bad.append(f"il knob {i} è lungo {len(str(k['effect']))}, e il massimo è 280")

    for key in ("from_entries", "goes_with"):
        value = record.get(key)
        if isinstance(value, list):
            for n in value:
                if not isinstance(n, int):
                    bad.append(f"«{key}» contiene {n!r}, che non è un numero di voce")
                elif n not in known:
                    bad.append(f"«{key}» rimanda alla voce {n}, che non esiste")

    if record.get("verification") == "needs_a_person" and record.get("adult_cost") == "none":
        bad.append("dice che la verifica ha bisogno di una persona e che l'adulto non paga niente")

    if isinstance(record.get("also"), list) and not record["also"]:
        bad.append("«also» è vuoto: senza gli altri nomi non si arriva qui dall'enciclopedia")

    # Il tetto non e' il budget del prompt, ed e' stato scambiato per quello una volta. Un
    # record e' lungo quanto serve a costruire la cosa: quello sul moire' porta il passo in
    # millimetri, la costante che ne discende e il fatto che stampare al 94% falsa ogni
    # angolo, e sta in 2 570 caratteri senza una parola in piu'. Il prompt si fa stare
    # servendo meno record, non record piu' corti. Questo tetto serve solo a impedire che un
    # record diventi un saggio.
    if not bad:
        knobs_len = sum(len(k["knob"]) + len(k["effect"]) for k in record["knobs"])
        whole = (
            len(record["name"])
            + len(record["one_line"])
            + len(record["how"])
            + knobs_len
            + len(record["where_the_work_is"])
            + len(record["breaks"])
        )
        if whole > 2900:
            bad.append(f"la metà da mettere nel prompt è {whole} caratteri, e il massimo è 2900")

    return bad


def main() -> int:
    files = sorted(METHODS.glob("*.json"))
    if not files:
        print(f"nessun record sotto {METHODS}: non c'è niente da controllare", file=sys.stderr)
        return 2

    known = entries()
    said: dict[str, str] = {}
    complaints = 0
    prompt_chars: list[int] = []

    for path in sorted(files):
        bad = one(path, known, said)
        if bad:
            complaints += len(bad)
            print(f"\n{path.relative_to(HERE)}")
            for line in bad:
                print(f"   {line}")
        else:
            record = json.loads(path.read_text(encoding="utf-8"))
            knobs = sum(len(k["knob"]) + len(k["effect"]) for k in record["knobs"])
            prompt_chars.append(
                len(record["name"])
                + len(record["one_line"])
                + len(record["how"])
                + knobs
                + len(record["where_the_work_is"])
                + len(record["breaks"])
            )

    print(f"\n{len(files)} record, {complaints} cose da sistemare")
    if prompt_chars:
        media = sum(prompt_chars) // len(prompt_chars)
        print(
            f"metà da mettere nel prompt: media {media} car, "
            f"min {min(prompt_chars)}, max {max(prompt_chars)} — "
            f"cinque fanno {media * 5 / 1024:.1f} kB"
        )
    return 1 if complaints else 0


if __name__ == "__main__":
    raise SystemExit(main())
