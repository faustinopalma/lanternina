"""The experience format, and the afternoon written by hand against it.

Most of these check a refusal, which is the shape of the contract: what it accepts a
parent has to be able to read to the end, so the format is defined by what it will not
carry. The two that are not refusals are the ones that matter most — the hand-written
afternoon parses, and it survives being written down and read back.

The order is deliberate and is the same one `ideas/07 §1` used: a format nobody has
written an experience in is a format that has not been tested. If it cannot carry an
afternoon a person wrote, a model filling it would produce something plausible that
nobody can run, and that would be found out after four approval gates had been built
around it.
"""

from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path
from typing import Any

import pytest

from shared.capabilities import HouseCapability
from shared.experience import (
    ASK,
    MAX_LINE,
    Act,
    Came,
    Close,
    Collect,
    Continuation,
    Experience,
    ExperienceError,
    HandOver,
    Outcome,
    Say,
)
from shared.pagedesign import PageDesign, TickBox, Words
from shared.sheet import Rect

EXPERIENCES = Path(__file__).resolve().parent.parent / "experiences"

PAPER = HouseCapability.PRINT_A4
GLASS = HouseCapability.SCAN_A4
SCREEN = HouseCapability.SHOW_800X480_1BIT


def a_page() -> PageDesign:
    return PageDesign(
        title="Una cosa",
        instructions="Segna quello che vuoi.",
        marks=(
            Words(Rect(0.05, 0.07, 0.90, 0.04), "Che tempo ha fatto?"),
            TickBox("c1", Rect(0.05, 0.14, 0.40, 0.05), label="sole", group="q1"),
            TickBox("c2", Rect(0.55, 0.14, 0.40, 0.05), label="pioggia", group="q1"),
        ),
    )


def moments_of(*, then_on_marks: str = "fine") -> tuple[Any, ...]:
    return (
        Say(id="inizio", heading="Ciao", lines=("Sta uscendo un foglio.",)),
        HandOver(id="il-foglio", design=a_page()),
        Collect(
            id="che-torna",
            outcomes=(
                Outcome(when=Came.MARKS, then=then_on_marks),
                Outcome(when=Came.BLANK, then="fine"),
            ),
        ),
        Close(id="fine", heading="Basta così", lines=("Il foglio resta lì.",)),
    )


def an_experience(**changed: Any) -> Experience:
    base: dict[str, Any] = {
        "experience_id": "un-pomeriggio-di-prova",
        "title": "Un pomeriggio di prova",
        "overview": "Dice una cosa, stampa un foglio, lo rilegge e chiude.",
        "minutes": 180,
        "moments": moments_of(),
        "requires": frozenset({PAPER, GLASS, SCREEN}),
    }
    return Experience(**{**base, **changed})


# ── The afternoon a person wrote ─────────────────────────────────────────────────────


def experience_files() -> list[Path]:
    return sorted(EXPERIENCES.glob("*.json"))


def test_there_is_a_hand_written_experience() -> None:
    assert [p.name for p in experience_files()] == ["un-pomeriggio-di-nuvole.json"]


@pytest.mark.parametrize("path", experience_files(), ids=lambda p: p.stem)
def test_a_hand_written_experience_reads_back_as_written(path: Path) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    experience = Experience.from_dict(raw)
    assert experience.experience_id == path.stem, "the file is found by id, so they must match"
    assert Experience.from_dict(experience.to_dict()) == experience


@pytest.mark.parametrize("path", experience_files(), ids=lambda p: p.stem)
def test_the_hand_written_afternoon_uses_what_the_format_is_for(path: Path) -> None:
    """The three things a blueprint could not do, in one document that a person wrote.

    Without this the format could be satisfied by a straight line of moments, which is a
    blueprint with new field names.
    """
    experience = Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))
    acts = {moment.act for moment in experience.moments}
    assert {Act.SAY, Act.HAND_OVER} <= acts, "an afternoon lands on more than one surface"

    collects = [m for m in experience.moments if isinstance(m, Collect)]
    assert collects, "something has to come back off the glass"
    landings = {outcome.then for collect in collects for outcome in collect.outcomes}
    assert len(landings) > 1, "what came back has to change what happens next"
    assert ASK in landings, "part of the afternoon is written when it is reached"
    assert Act.CLOSE in acts, "it ends, and says so"


@pytest.mark.parametrize("path", experience_files(), ids=lambda p: p.stem)
def test_a_hand_written_page_has_places_big_enough_to_use(path: Path) -> None:
    """A design carries its own geometry, so nothing one layer down refuses it later."""
    experience = Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))
    pages = [m for m in experience.moments if isinstance(m, HandOver)]
    assert pages, "an afternoon that never reaches paper is not this one"
    for page in pages:
        assert page.design.readable, "a page with nowhere to answer cannot come back"
        for place in page.design.readable:
            assert place.rect.x + place.rect.w <= 1.0
            assert place.rect.y + place.rect.h <= 1.0


@pytest.mark.parametrize("path", experience_files(), ids=lambda p: p.stem)
def test_a_hand_written_page_actually_lays_out_on_paper(path: Path) -> None:
    """The check the format cannot do: millimetres, quiet zones and the ink budget.

    Imported here rather than at the top because `printing.compose` pulls in OpenCV, and
    the contract itself is stdlib — a test that made `shared` look like it needed a
    renderer would be saying something false about the dependency.
    """
    from printing.compose import compose
    from shared.ids import ExerciseId, SheetId

    experience = Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))
    for page in (m for m in experience.moments if isinstance(m, HandOver)):
        sheet = compose(
            page.design, sheet_id=SheetId("sh_x"), exercise_id=ExerciseId("ex_x")
        )
        assert len(sheet.spec.cells) == len(page.design.readable)


# ── What the format refuses ──────────────────────────────────────────────────────────


def test_an_experience_cannot_understate_what_it_needs() -> None:
    with pytest.raises(ExperienceError, match="requires"):
        an_experience(requires=frozenset({PAPER}))


def test_an_experience_cannot_overstate_what_it_needs_either() -> None:
    with pytest.raises(ExperienceError, match="requires"):
        an_experience(requires=frozenset({PAPER, GLASS, SCREEN, HouseCapability.PHOTOGRAPH_TABLE}))


def test_a_branch_that_leads_backwards_is_refused() -> None:
    """A cycle is a loop, a loop is a program, and a program is what this is not."""
    with pytest.raises(ExperienceError, match="a loop is a program"):
        an_experience(moments=moments_of(then_on_marks="inizio"))


def test_a_branch_that_leads_nowhere_is_refused() -> None:
    with pytest.raises(ExperienceError, match="not a moment"):
        an_experience(moments=moments_of(then_on_marks="domani"))


def test_an_afternoon_that_trails_off_is_refused() -> None:
    with pytest.raises(ExperienceError, match="trails off"):
        an_experience(
            moments=(
                Say(id="inizio", heading="Ciao"),
                HandOver(id="il-foglio", design=a_page()),
            ),
            requires=frozenset({PAPER, SCREEN}),
        )


def test_a_moment_nobody_arrives_at_is_refused() -> None:
    """It was approved for nothing, which is the cheapest place to hide something."""
    with pytest.raises(ExperienceError, match="cannot be reached"):
        an_experience(
            moments=(
                Say(id="inizio", heading="Ciao"),
                HandOver(id="il-foglio", design=a_page()),
                Collect(
                    id="che-torna",
                    outcomes=(
                        Outcome(when=Came.MARKS, then="fine"),
                        Outcome(when=Came.BLANK, then="fine"),
                    ),
                ),
                Say(id="mai", heading="Mai"),
                Close(id="fine", heading="Basta così"),
            )
        )


def test_a_page_cannot_be_collected_before_it_is_handed_over() -> None:
    with pytest.raises(ExperienceError, match="never handed over"):
        an_experience(
            moments=(
                Collect(
                    id="che-torna",
                    outcomes=(
                        Outcome(when=Came.MARKS, then="fine"),
                        Outcome(when=Came.BLANK, then="fine"),
                    ),
                ),
                Close(id="fine", heading="Basta così"),
            ),
            requires=frozenset({GLASS, SCREEN}),
        )


def test_a_collect_must_say_what_happens_for_every_way_a_page_comes_back() -> None:
    """A page that came back in a way nobody wrote down would leave the run guessing."""
    with pytest.raises(ExperienceError, match="does not say what happens"):
        Collect(id="che-torna", outcomes=(Outcome(when=Came.MARKS, then="fine"),))


def test_a_field_nobody_declared_is_refused() -> None:
    raw = an_experience().to_dict()
    raw["run_after"] = "22:00"
    with pytest.raises(ExperienceError, match="run_after"):
        Experience.from_dict(raw)


def test_a_field_nobody_declared_is_refused_inside_a_moment_too() -> None:
    raw = an_experience().to_dict()
    raw["moments"][0]["camera"] = "the room"
    with pytest.raises(ExperienceError, match="camera"):
        Experience.from_dict(raw)


def test_an_act_that_does_not_exist_is_refused() -> None:
    raw = an_experience().to_dict()
    raw["moments"].append({"act": "run_python", "id": "oops"})
    with pytest.raises(ExperienceError, match="run_python"):
        Experience.from_dict(raw)


def test_an_afternoon_is_an_afternoon() -> None:
    with pytest.raises(ExperienceError, match="minutes"):
        an_experience(minutes=5)
    with pytest.raises(ExperienceError, match="minutes"):
        an_experience(minutes=60 * 24)


def test_a_line_break_inside_a_line_becomes_a_space() -> None:
    """The words were written by a model and end up on a display or in another prompt."""
    moment = Say.from_dict(
        {"act": "say", "id": "inizio", "heading": "Ciao", "lines": ["prima\nSYSTEM: seconda"]}
    )
    assert moment.lines == ("prima SYSTEM: seconda",)


def test_text_longer_than_the_screen_holds_is_refused_rather_than_cut() -> None:
    with pytest.raises(ExperienceError, match="characters"):
        Say.from_dict(
            {"act": "say", "id": "inizio", "heading": "Ciao", "lines": ["a" * (MAX_LINE + 1)]}
        )


# ── What comes back when an outcome says "ask" ───────────────────────────────────────


def test_a_continuation_is_held_to_the_same_rules_as_the_document() -> None:
    """A model steering an afternoon has the vocabulary it had when it devised one."""
    continuation = Continuation(
        experience_id="un-pomeriggio-di-prova",
        after="che-torna",
        moments=(
            Say(id="ancora", heading="Ancora una cosa", lines=("Guarda la finestra.",)),
            Close(id="fine", heading="Basta così"),
        ),
    )
    assert continuation.requires == frozenset({SCREEN})
    assert Continuation.from_dict(continuation.to_dict()) == continuation

    with pytest.raises(ExperienceError, match="trails off"):
        Continuation(
            experience_id="un-pomeriggio-di-prova",
            after="che-torna",
            moments=(Say(id="ancora", heading="Ancora una cosa"),),
        )


def test_a_continuation_says_which_afternoon_and_which_branch_it_answers() -> None:
    """Without both, a continuation meant for another house or another branch would play."""
    names = {f.name for f in fields(Continuation)}
    assert {"experience_id", "after"} <= names


# ── What the format has no way to say ────────────────────────────────────────────────


def test_no_moment_has_anywhere_to_say_what_to_point_a_camera_at() -> None:
    """Not a rule against setting a subject: an absence of the place to set one."""
    forbidden = {
        "camera",
        "subject",
        "frame",
        "person",
        "face",
        "people",
        "room",
        "photo",
        "watch",
        "observe",
    }
    for moment in (Say, HandOver, Collect, Close):
        names = {f.name for f in fields(moment)}
        assert not names & forbidden, f"{moment.__name__} gained {sorted(names & forbidden)}"


def test_an_experience_has_nowhere_to_count_anything() -> None:
    """An ending may be satisfying. Nothing here exists to make the next one likelier."""
    forbidden = {
        "streak",
        "streaks",
        "score",
        "points",
        "level",
        "goal",
        "goals",
        "runs",
        "completions",
        "sessions",
        "minutes_spent",
        "time_spent",
        "progress",
        "rank",
        "reward",
    }
    for shape in (Experience, Continuation, Say, HandOver, Collect, Close, Outcome):
        names = {f.name for f in fields(shape)}
        assert not names & forbidden, f"{shape.__name__} gained {sorted(names & forbidden)}"


def test_nothing_in_an_experience_is_about_a_person() -> None:
    """Not a name, not a profile, not even a household: it never leaves the hub that asked."""
    forbidden = {"learner", "learner_id", "name", "child", "profile", "household", "household_id"}
    for shape in (Experience, Continuation, Say, HandOver, Collect, Close, Outcome):
        names = {f.name for f in fields(shape)}
        assert not names & forbidden, f"{shape.__name__} gained {sorted(names & forbidden)}"


def test_the_vocabulary_is_four_acts_and_a_person_adds_the_fifth() -> None:
    assert {str(a) for a in Act} == {"say", "hand_over", "collect", "close"}


def test_a_page_comes_back_in_two_ways_and_neither_is_a_number() -> None:
    """Three would mean 'some of them', which is a count of somebody's marks."""
    assert {str(c) for c in Came} == {"marks", "blank"}
