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
        ("nature-journaling", "https://en.wikipedia.org/wiki/Nature_journal"),
        ("origami", "https://en.wikipedia.org/wiki/Origami"),
        ("bookbinding", "https://en.wikipedia.org/wiki/Bookbinding"),
        ("cyanotype", "https://en.wikipedia.org/wiki/Cyanotype"),
        ("kitchen-chemistry", "https://en.wikipedia.org/wiki/Home_science"),
        ("cartography", "https://en.wikipedia.org/wiki/Cartography"),
        ("oral-history", "https://en.wikipedia.org/wiki/Oral_history"),
    ],
    # In italiano: la tassonomia dei giochi enigmistici non ha un corrispettivo inglese.
    "enigmistica": [
        ("it-enigmistica", "https://it.wikipedia.org/wiki/Enigmistica"),
        ("it-gioco-enigmistico", "https://it.wikipedia.org/wiki/Gioco_enigmistico"),
        ("it-crittografia-gioco", "https://it.wikipedia.org/wiki/Crittografia_(enigmistica)"),
        ("it-rebus", "https://it.wikipedia.org/wiki/Rebus"),
        ("it-sciarada", "https://it.wikipedia.org/wiki/Sciarada"),
        ("it-lucchetto", "https://it.wikipedia.org/wiki/Lucchetto_(enigmistica)"),
        ("it-zeppa", "https://it.wikipedia.org/wiki/Zeppa_(enigmistica)"),
        ("it-scarto", "https://it.wikipedia.org/wiki/Scarto_(enigmistica)"),
        ("it-cambio", "https://it.wikipedia.org/wiki/Cambio_(enigmistica)"),
        ("it-bifronte", "https://it.wikipedia.org/wiki/Bifronte_(enigmistica)"),
        ("it-incastro", "https://it.wikipedia.org/wiki/Incastro_(enigmistica)"),
        ("it-anagramma", "https://it.wikipedia.org/wiki/Anagramma"),
        ("it-palindromo", "https://it.wikipedia.org/wiki/Palindromo"),
        ("it-indovinello", "https://it.wikipedia.org/wiki/Indovinello"),
        ("it-settimana-enigmistica", "https://it.wikipedia.org/wiki/La_Settimana_Enigmistica"),
        ("it-cruciverba", "https://it.wikipedia.org/wiki/Cruciverba"),
        ("it-acrostico", "https://it.wikipedia.org/wiki/Acrostico"),
        ("it-scrittura-speculare", "https://it.wikipedia.org/wiki/Scrittura_speculare"),
        ("word-ladder", "https://en.wikipedia.org/wiki/Word_ladder"),
        ("ambigram", "https://en.wikipedia.org/wiki/Ambigram"),
        ("rebus-principle", "https://en.wikipedia.org/wiki/Rebus#Rebus_principle"),
    ],
    "matematica e percezione": [
        ("fermi-problem", "https://en.wikipedia.org/wiki/Fermi_problem"),
        ("martin-gardner", "https://en.wikipedia.org/wiki/Martin_Gardner"),
        ("recreational-mathematics", "https://en.wikipedia.org/wiki/Recreational_mathematics"),
        ("verbal-arithmetic", "https://en.wikipedia.org/wiki/Verbal_arithmetic"),
        ("magic-square", "https://en.wikipedia.org/wiki/Magic_square"),
        ("pigeonhole-principle", "https://en.wikipedia.org/wiki/Pigeonhole_principle"),
        ("invariant-mathematics", "https://en.wikipedia.org/wiki/Invariant_(mathematics)"),
        ("nim", "https://en.wikipedia.org/wiki/Nim"),
        ("proof-without-words", "https://en.wikipedia.org/wiki/Proof_without_words"),
        ("dissection-puzzle", "https://en.wikipedia.org/wiki/Dissection_puzzle"),
        ("monty-hall-problem", "https://en.wikipedia.org/wiki/Monty_Hall_problem"),
        ("cellular-automaton", "https://en.wikipedia.org/wiki/Cellular_automaton"),
        ("optical-illusion", "https://en.wikipedia.org/wiki/Optical_illusion"),
        ("multistable-perception", "https://en.wikipedia.org/wiki/Multistable_perception"),
        ("impossible-object", "https://en.wikipedia.org/wiki/Impossible_object"),
        ("anamorphosis", "https://en.wikipedia.org/wiki/Anamorphosis"),
        ("pareidolia", "https://en.wikipedia.org/wiki/Pareidolia"),
        ("change-blindness", "https://en.wikipedia.org/wiki/Change_blindness"),
        ("moire-pattern", "https://en.wikipedia.org/wiki/Moir%C3%A9_pattern"),
        ("mental-rotation", "https://en.wikipedia.org/wiki/Mental_rotation"),
        ("camouflage", "https://en.wikipedia.org/wiki/Camouflage"),
        ("forced-perspective", "https://en.wikipedia.org/wiki/Forced_perspective"),
    ],
    # Il capitolo 2 e' fatto di verbi cognitivi, e i verbi hanno una letteratura propria
    # che non passa da nessuna delle pagine sui giochi.
    "verbi del ragionamento": [
        ("deductive-reasoning", "https://en.wikipedia.org/wiki/Deductive_reasoning"),
        ("inductive-reasoning", "https://en.wikipedia.org/wiki/Inductive_reasoning"),
        ("abductive-reasoning", "https://en.wikipedia.org/wiki/Abductive_reasoning"),
        ("wason-selection-task", "https://en.wikipedia.org/wiki/Wason_selection_task"),
        ("confirmation-bias", "https://en.wikipedia.org/wiki/Confirmation_bias"),
        ("argument-from-silence", "https://en.wikipedia.org/wiki/Argument_from_silence"),
        ("categorization", "https://en.wikipedia.org/wiki/Categorization"),
        ("single-access-key", "https://en.wikipedia.org/wiki/Single-access_key"),
        ("twenty-questions", "https://en.wikipedia.org/wiki/Twenty_questions"),
        ("binary-search", "https://en.wikipedia.org/wiki/Binary_search"),
        ("mastermind-board-game", "https://en.wikipedia.org/wiki/Mastermind_(board_game)"),
        ("visual-search", "https://en.wikipedia.org/wiki/Visual_search"),
        ("spot-the-difference", "https://en.wikipedia.org/wiki/Spot_the_difference"),
        ("scientific-method", "https://en.wikipedia.org/wiki/Scientific_method"),
        ("design-of-experiments", "https://en.wikipedia.org/wiki/Design_of_experiments"),
        ("simulation", "https://en.wikipedia.org/wiki/Simulation"),
        ("engineering-design-process", "https://en.wikipedia.org/wiki/Engineering_design_process"),
        ("design-thinking", "https://en.wikipedia.org/wiki/Design_thinking"),
        ("prototype", "https://en.wikipedia.org/wiki/Prototype"),
        ("imagination", "https://en.wikipedia.org/wiki/Imagination"),
        ("worldbuilding", "https://en.wikipedia.org/wiki/Worldbuilding"),
        ("divergent-thinking", "https://en.wikipedia.org/wiki/Divergent_thinking"),
        ("torrance-tests", "https://en.wikipedia.org/wiki/Torrance_Tests_of_Creative_Thinking"),
        ("oblique-strategies", "https://en.wikipedia.org/wiki/Oblique_Strategies"),
        ("adaptation-arts", "https://en.wikipedia.org/wiki/Adaptation_(arts)"),
        ("exercises-in-style", "https://en.wikipedia.org/wiki/Exercises_in_Style"),
        ("variation-music", "https://en.wikipedia.org/wiki/Variation_(music)"),
        ("decision-making", "https://en.wikipedia.org/wiki/Decision-making"),
        ("overchoice", "https://en.wikipedia.org/wiki/Overchoice"),
        (
            "multiple-criteria-decision-analysis",
            "https://en.wikipedia.org/wiki/Multiple-criteria_decision_analysis",
        ),
        ("trolley-problem", "https://en.wikipedia.org/wiki/Trolley_problem"),
        ("peer-assessment", "https://en.wikipedia.org/wiki/Peer_assessment"),
        ("negotiation", "https://en.wikipedia.org/wiki/Negotiation"),
        ("fair-division", "https://en.wikipedia.org/wiki/Fair_division"),
        ("divide-and-choose", "https://en.wikipedia.org/wiki/Divide_and_choose"),
    ],
    # Prese apposta per verificare le cose che le schede portano ancora come «va verificato».
    "da verificare": [
        ("betty-edwards", "https://en.wikipedia.org/wiki/Betty_Edwards"),
        ("proofs-and-refutations", "https://en.wikipedia.org/wiki/Proofs_and_Refutations"),
        ("chart-of-biography", "https://en.wikipedia.org/wiki/A_Chart_of_Biography"),
        ("william-playfair", "https://en.wikipedia.org/wiki/William_Playfair"),
        ("john-snow", "https://en.wikipedia.org/wiki/John_Snow"),
        ("image-of-the-city", "https://en.wikipedia.org/wiki/The_Image_of_the_City"),
        ("on-being-the-right-size", "https://en.wikipedia.org/wiki/On_Being_the_Right_Size"),
        ("huzita-hatori-axioms", "https://en.wikipedia.org/wiki/Huzita%E2%80%93Hatori_axioms"),
        ("right-question-institute", "https://en.wikipedia.org/wiki/Right_Question_Institute"),
        ("photovoice", "https://en.wikipedia.org/wiki/Photovoice"),
        ("concept-map", "https://en.wikipedia.org/wiki/Concept_map"),
        ("dalcroze-eurhythmics", "https://en.wikipedia.org/wiki/Dalcroze_eurhythmics"),
        ("orff-schulwerk", "https://en.wikipedia.org/wiki/Orff_Schulwerk"),
        ("kodaly-method", "https://en.wikipedia.org/wiki/Kod%C3%A1ly_method"),
        ("murray-schafer", "https://en.wikipedia.org/wiki/R._Murray_Schafer"),
        ("history-of-the-metre", "https://en.wikipedia.org/wiki/History_of_the_metre"),
    ],
}


def fetch(name: str, url: str) -> tuple[str, int | str]:
    where = WHERE / f"{name}.html"
    if where.exists():
        return name, -1
    request = urllib.request.Request(
        url, headers={"User-Agent": "lanternina-research/1.0 (documentation gathering)"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as answer:
            body = answer.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return name, f"{type(exc).__name__}: {exc}"
    where.write_bytes(body)
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
            elif size < 0:
                lines.append(f"- `{got}.html` — {url} — già presente")
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
