"""Format-2 afternoons for the tests to take apart, built as the documents they are.

Dicts rather than objects, and one module rather than a copy per test file. Format 2 asks
every moment for three weighings, four rungs of help and a way out, so a moment written by
hand is now twenty lines of JSON — and six test files each with their own idea of what a
valid one looks like is six places to update the next time the format moves.

Everything here is deliberately valid and deliberately dull. A test that wants a document
missing a field takes one of these and removes the field, which is the shape the whole
suite is written in: the interesting half of any of these tests is what happens when
something is taken away.
"""

from __future__ import annotations

from typing import Any

# Every default text mentions the sheet, because a way out has to name something the
# afternoon already put in somebody's hands and the check that says so reads the words.
IN_HAND = "il foglio"


def weights(
    short: int = 5,
    standard: int = 10,
    extended: int = 15,
    *,
    lines: tuple[str, ...] = ("Sul tavolo c'è il foglio.",),
) -> dict[str, Any]:
    return {
        "short": {"minutes": short, "lines": list(lines)},
        "standard": {"minutes": standard, "lines": list(lines)},
        "extended": {"minutes": extended, "lines": list(lines)},
    }


def ladder(*after: int) -> list[dict[str, Any]]:
    rungs = after or (3, 6, 10, 15)
    return [
        {"after_minutes": minutes, "lines": [f"Il foglio è lì, ancora {minutes}."]}
        for minutes in rungs
    ]


def way_out(in_hand: str = IN_HAND, minutes: int = 10) -> dict[str, Any]:
    return {
        "in_hand": in_hand,
        "heading": "Basta così",
        "lines": [f"Posa {in_hand} sul tavolo.", "Il pomeriggio finisce qui."],
        "minutes": minutes,
    }


def _common(moment_id: str, heading: str, **changed: Any) -> dict[str, Any]:
    common: dict[str, Any] = {
        "id": moment_id,
        "heading": heading,
        "weights": weights(),
        "help": ladder(),
        "way_out": way_out(),
    }
    common.update(changed)
    return common


def say(moment_id: str = "inizio", heading: str = "Ciao", **changed: Any) -> dict[str, Any]:
    return {"act": "say", **_common(moment_id, heading, **changed)}


def close(moment_id: str = "fine", heading: str = "Basta così", **changed: Any) -> dict[str, Any]:
    return {"act": "close", **_common(moment_id, heading, **changed)}


def a_page() -> dict[str, Any]:
    return {
        "kind": "dossier",
        "title": "Una cosa",
        "illustration": "a single cloud over a roof",
        "note": ["Segna quello che vuoi."],
        "spaces": [
            {"label": "Che tempo ha fatto", "room": "a_line"},
            {"label": "Disegnalo", "room": "a_box"},
        ],
    }


def hand_over(
    moment_id: str = "il-foglio", heading: str = "Esce un foglio", **changed: Any
) -> dict[str, Any]:
    return {
        "act": "hand_over",
        **_common(moment_id, heading, **changed),
        "page": changed.get("page", a_page()),
        "instead": changed.get("instead", ["Oggi il foglio non esce.", "Tienilo a mente."]),
    }


def collect(
    moment_id: str = "che-torna",
    heading: str = "Mettilo sul vetro",
    *,
    on_marks: str = "fine",
    on_blank: str = "fine",
    if_no_page: str = "fine",
    **changed: Any,
) -> dict[str, Any]:
    return {
        "act": "collect",
        **_common(moment_id, heading, **changed),
        "outcomes": [
            {"when": "marks", "then": on_marks},
            {"when": "blank", "then": on_blank},
        ],
        "if_no_page": if_no_page,
    }


def drawn(**changed: Any) -> dict[str, Any]:
    ten = {
        "frame": "una cucina di pomeriggio",
        "role": "chi tiene il registro",
        "mechanic": "guardare e riportare",
        "progress": "un foglio alla volta",
        "paper": "il registro",
        "glass": "consegnare il foglio",
        "displays": "la voce che dice cosa fare",
        "camera": "nessuna",
        "tone": "asciutto",
        "ending": "il foglio resta lì",
    }
    ten.update(changed)
    return ten


def moments(*, on_marks: str = "fine") -> list[dict[str, Any]]:
    return [say(), hand_over(), collect(on_marks=on_marks), close()]


def an_afternoon(**changed: Any) -> dict[str, Any]:
    document: dict[str, Any] = {
        "format_version": 2,
        "experience_id": "un-pomeriggio-di-prova",
        "title": "Un pomeriggio di prova",
        "overview": "Dice una cosa, stampa un foglio, lo rilegge e chiude.",
        "minutes": 180,
        "requires": ["print_a4", "scan_a4", "show_800x480_1bit"],
        "drawn": drawn(),
        "moments": moments(),
    }
    document.update(changed)
    return document


def a_continuation(**changed: Any) -> dict[str, Any]:
    document: dict[str, Any] = {
        "format_version": 2,
        "experience_id": "un-pomeriggio-di-prova",
        "after": "che-torna",
        "moments": [say(moment_id="ancora", heading="Ancora una cosa"), close()],
    }
    document.update(changed)
    return document
