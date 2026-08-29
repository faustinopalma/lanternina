"""Scarica le fonti per `docs/EXERCISE-FORMS.md` in una cartella locale.

    python tools/fetch_exercise_sources.py

Le pagine finiscono in `_reference/esercizi-e-sfide/`, che e' gitignored: sono testi di
altri, e quello che entra nel repository e' il documento che ne ricava una tassonomia. Il
file `SOURCES.md` accanto alle pagine dice da dove viene ognuna e quando e' stata presa.

Se una pagina non risponde, il download va avanti: una fonte in meno e' una voce in meno,
non una corsa fallita.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

WHERE = Path(__file__).resolve().parents[1] / "_reference" / "esercizi-e-sfide"

# Raggruppate per il capitolo che alimentano. Un nome di file per fonte, cosi' il documento
# puo' citarlo senza ambiguita'.
SOURCES: dict[str, list[tuple[str, str]]] = {
    "puzzle e enigmi": [
        ("puzzle", "https://en.wikipedia.org/wiki/Puzzle"),
        ("list-of-puzzle-topics", "https://en.wikipedia.org/wiki/List_of_puzzle_topics"),
        ("riddle", "https://en.wikipedia.org/wiki/Riddle"),
        ("lateral-thinking-puzzle", "https://en.wikipedia.org/wiki/Situation_puzzle"),
        ("logic-puzzle", "https://en.wikipedia.org/wiki/Logic_puzzle"),
        ("mechanical-puzzle", "https://en.wikipedia.org/wiki/Mechanical_puzzle"),
        ("word-game", "https://en.wikipedia.org/wiki/Word_game"),
        ("cryptic-crossword", "https://en.wikipedia.org/wiki/Cryptic_crossword"),
        ("nikoli-puzzle-types", "https://en.wikipedia.org/wiki/List_of_Nikoli_puzzle_types"),
        ("metapuzzle", "https://en.wikipedia.org/wiki/Metapuzzle"),
        ("puzzlehunt", "https://en.wikipedia.org/wiki/Puzzlehunt"),
        ("cipher", "https://en.wikipedia.org/wiki/Cipher"),
        ("steganography", "https://en.wikipedia.org/wiki/Steganography"),
        ("rebus", "https://en.wikipedia.org/wiki/Rebus"),
        ("charades", "https://en.wikipedia.org/wiki/Charades"),
        ("droodles", "https://en.wikipedia.org/wiki/Droodles"),
        ("koan", "https://en.wikipedia.org/wiki/K%C5%8Dan"),
        ("dilemma-story", "https://en.wikipedia.org/wiki/Dilemma_story"),
        ("induction-puzzles", "https://en.wikipedia.org/wiki/Induction_puzzles"),
    ],
    "stanze e cacce": [
        ("escape-room", "https://en.wikipedia.org/wiki/Escape_room"),
        ("scavenger-hunt", "https://en.wikipedia.org/wiki/Scavenger_hunt"),
        ("treasure-hunt", "https://en.wikipedia.org/wiki/Treasure_hunt_(game)"),
        ("geocaching", "https://en.wikipedia.org/wiki/Geocaching"),
        ("letterboxing", "https://en.wikipedia.org/wiki/Letterboxing_(hobby)"),
        ("orienteering", "https://en.wikipedia.org/wiki/Orienteering"),
        ("alternate-reality-game", "https://en.wikipedia.org/wiki/Alternate_reality_game"),
        ("pervasive-game", "https://en.wikipedia.org/wiki/Pervasive_game"),
        ("live-action-role-playing", "https://en.wikipedia.org/wiki/Live_action_role-playing_game"),
        ("immersive-theatre", "https://en.wikipedia.org/wiki/Immersive_theater"),
        ("legend-tripping", "https://en.wikipedia.org/wiki/Legend_tripping"),
    ],
    "valutazione e didattica": [
        ("educational-assessment", "https://en.wikipedia.org/wiki/Educational_assessment"),
        ("multiple-choice", "https://en.wikipedia.org/wiki/Multiple_choice"),
        ("cloze-test", "https://en.wikipedia.org/wiki/Cloze_test"),
        ("essay", "https://en.wikipedia.org/wiki/Essay"),
        ("rubric", "https://en.wikipedia.org/wiki/Rubric_(academic)"),
        ("formative-assessment", "https://en.wikipedia.org/wiki/Formative_assessment"),
        ("blooms-taxonomy", "https://en.wikipedia.org/wiki/Bloom%27s_taxonomy"),
        ("problem-based-learning", "https://en.wikipedia.org/wiki/Problem-based_learning"),
        ("project-based-learning", "https://en.wikipedia.org/wiki/Project-based_learning"),
        ("inquiry-based-learning", "https://en.wikipedia.org/wiki/Inquiry-based_learning"),
        ("worked-example-effect", "https://en.wikipedia.org/wiki/Worked-example_effect"),
        ("spaced-repetition", "https://en.wikipedia.org/wiki/Spaced_repetition"),
        ("testing-effect", "https://en.wikipedia.org/wiki/Testing_effect"),
        ("jigsaw-classroom", "https://en.wikipedia.org/wiki/Jigsaw_(teaching_technique)"),
        ("socratic-method", "https://en.wikipedia.org/wiki/Socratic_method"),
        ("webquest", "https://en.wikipedia.org/wiki/WebQuest"),
        ("montessori-education", "https://en.wikipedia.org/wiki/Montessori_education"),
        ("reggio-emilia", "https://en.wikipedia.org/wiki/Reggio_Emilia_approach"),
        (
            "zone-of-proximal-development",
            "https://en.wikipedia.org/wiki/Zone_of_proximal_development",
        ),
        ("scaffolding", "https://en.wikipedia.org/wiki/Instructional_scaffolding"),
    ],
    "gioco e meccaniche": [
        ("game-mechanics", "https://en.wikipedia.org/wiki/Game_mechanics"),
        ("gamification", "https://en.wikipedia.org/wiki/Gamification"),
        ("serious-game", "https://en.wikipedia.org/wiki/Serious_game"),
        ("game-based-learning", "https://en.wikipedia.org/wiki/Educational_game"),
        ("tabletop-role-playing-game", "https://en.wikipedia.org/wiki/Tabletop_role-playing_game"),
        ("gamebook", "https://en.wikipedia.org/wiki/Gamebook"),
        ("interactive-fiction", "https://en.wikipedia.org/wiki/Interactive_fiction"),
        ("flow-psychology", "https://en.wikipedia.org/wiki/Flow_(psychology)"),
        ("self-determination-theory", "https://en.wikipedia.org/wiki/Self-determination_theory"),
        ("overjustification-effect", "https://en.wikipedia.org/wiki/Overjustification_effect"),
    ],
    "scrittura e vincolo": [
        ("oulipo", "https://en.wikipedia.org/wiki/Oulipo"),
        ("constrained-writing", "https://en.wikipedia.org/wiki/Constrained_writing"),
        ("ekphrasis", "https://en.wikipedia.org/wiki/Ekphrasis"),
        ("exquisite-corpse", "https://en.wikipedia.org/wiki/Exquisite_corpse"),
        ("found-poetry", "https://en.wikipedia.org/wiki/Found_poetry"),
        ("blackout-poetry", "https://en.wikipedia.org/wiki/Blackout_poetry"),
        ("mad-libs", "https://en.wikipedia.org/wiki/Mad_Libs"),
    ],
    "mani e mondo": [
        ("citizen-science", "https://en.wikipedia.org/wiki/Citizen_science"),
        ("nature-journaling", "https://en.wikipedia.org/wiki/Nature_journaling"),
        ("origami", "https://en.wikipedia.org/wiki/Origami"),
        ("bookbinding", "https://en.wikipedia.org/wiki/Bookbinding"),
        ("cyanotype", "https://en.wikipedia.org/wiki/Cyanotype"),
        ("kitchen-chemistry", "https://en.wikipedia.org/wiki/Home_science"),
        ("cartography", "https://en.wikipedia.org/wiki/Cartography"),
        ("oral-history", "https://en.wikipedia.org/wiki/Oral_history"),
    ],
}


def fetch(name: str, url: str) -> tuple[str, int | str]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "lanternina-research/1.0 (documentation gathering)"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as answer:
            body = answer.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return name, f"{type(exc).__name__}: {exc}"
    (WHERE / f"{name}.html").write_bytes(body)
    return name, len(body)


def main() -> int:
    WHERE.mkdir(parents=True, exist_ok=True)
    taken = datetime.now(UTC).strftime("%Y-%m-%d")
    lines = [f"# Fonti scaricate il {taken}", ""]
    missing = 0
    for chapter, sources in SOURCES.items():
        print(f"\n{chapter}")
        lines += [f"## {chapter}", ""]
        for name, url in sources:
            got, size = fetch(name, url)
            if isinstance(size, str):
                print(f"  ✗ {got}: {size}")
                lines.append(f"- ✗ `{got}` — {url} — {size}")
                missing += 1
            else:
                print(f"  ✓ {got}  {size // 1024} kB")
                lines.append(f"- `{got}.html` — {url} — {size // 1024} kB")
            time.sleep(0.4)
        lines.append("")
    (WHERE / "SOURCES.md").write_text("\n".join(lines), encoding="utf-8")
    total = sum(len(one) for one in SOURCES.values())
    print(f"\n{total - missing}/{total} in {WHERE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
