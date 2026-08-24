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

The documents are built in `tests/afternoons.py` as JSON, which is what they are. Format 2
asks every moment for three weighings, four rungs of help and a way out, so a moment
written out in Python is twenty lines that say nothing about what is being tested.
"""

from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path
from typing import Any

import afternoons as a
import pytest

from shared.capabilities import HouseCapability
from shared.experience import (
    ASK,
    MAX_LINE,
    MAX_WAY_OUT_MINUTES,
    Act,
    Came,
    Close,
    Collect,
    Continuation,
    Drawn,
    Experience,
    ExperienceError,
    HandOver,
    Help,
    Outcome,
    Say,
    WayOut,
    Weighing,
    Weight,
    longest_at,
)
from shared.experience_checks import check

EXPERIENCES = Path(__file__).resolve().parent.parent / "experiences"

PAPER = HouseCapability.PRINT_A4
GLASS = HouseCapability.SCAN_A4
SCREEN = HouseCapability.SHOW_800X480_1BIT


def an_experience(**changed: Any) -> Experience:
    return Experience.from_dict(a.an_afternoon(**changed))


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
def test_the_hand_written_afternoon_can_be_left_at_any_moment(path: Path) -> None:
    """The property format 2 exists for, on the one document a person actually wrote.

    Not "the checks pass" — that is asserted too, below — but the thing the checks are for:
    from every moment there is a written way to the ending, and it is short.
    """
    experience = Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))
    for moment in experience.moments:
        assert moment.way_out.minutes <= MAX_WAY_OUT_MINUTES
        assert moment.way_out.in_hand
    assert longest_at(experience.moments, Weight.SHORT) <= experience.minutes
    assert check(experience) == ()


@pytest.mark.parametrize("path", experience_files(), ids=lambda p: p.stem)
def test_a_page_says_what_it_is_and_leaves_somewhere_to_write(path: Path) -> None:
    """A page is an object out of the story, so it says what kind of object it is and what
    its drawing shows. Somewhere to write is what lets it come back at all."""
    experience = Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))
    pages = [m for m in experience.moments if isinstance(m, HandOver)]
    assert pages, "an afternoon that never reaches paper is not this one"
    for page in pages:
        assert page.page.kind
        assert page.page.illustration, "a page with no drawing is a form"
        assert page.page.spaces, "a page with nowhere to write cannot come back"


@pytest.mark.parametrize("path", experience_files(), ids=lambda p: p.stem)
def test_every_word_on_a_page_reaches_the_gate(path: Path) -> None:
    """The words are written here and lettered by an image model exactly as written, so the
    screening has to see every one of them. The illustration is not among them: it describes
    a drawing and is never printed as text."""
    experience = Experience.from_dict(json.loads(path.read_text(encoding="utf-8")))
    for moment in (m for m in experience.moments if isinstance(m, HandOver)):
        said = moment.words
        assert moment.page.title in said
        for line in moment.page.note:
            assert line in said
        for space in moment.page.spaces:
            assert space.label in said
        assert moment.page.illustration not in said


# ── What the format refuses ──────────────────────────────────────────────────────────


def test_an_experience_cannot_understate_what_it_needs() -> None:
    with pytest.raises(ExperienceError, match="requires"):
        an_experience(requires=["print_a4"])


def test_an_experience_cannot_overstate_what_it_needs_either() -> None:
    with pytest.raises(ExperienceError, match="requires"):
        an_experience(
            requires=["print_a4", "scan_a4", "show_800x480_1bit", "photograph_table"]
        )


def test_a_branch_that_leads_backwards_is_refused() -> None:
    """A cycle is a loop, a loop is a program, and a program is what this is not."""
    with pytest.raises(ExperienceError, match="a loop is a program"):
        an_experience(moments=a.moments(on_marks="inizio"))


def test_a_branch_that_leads_nowhere_is_refused() -> None:
    with pytest.raises(ExperienceError, match="not a moment"):
        an_experience(moments=a.moments(on_marks="domani"))


def test_a_collect_with_nowhere_to_go_when_nothing_was_printed_is_refused() -> None:
    """The version of every moment that runs with no printer, refused when it is missing.

    The printer is the single point of failure of an afternoon made of paper. A ``collect``
    with no ``if_no_page`` is a moment whose whole job is to read a sheet, in a house where
    no sheet came out, with nowhere to go.
    """
    moments = a.moments()
    del moments[2]["if_no_page"]

    with pytest.raises(ExperienceError, match="where a moment goes when nothing was printed"):
        an_experience(moments=moments)


def test_a_paper_moment_with_no_version_that_runs_without_printing_is_refused() -> None:
    moments = a.moments()
    del moments[1]["instead"]

    with pytest.raises(ExperienceError, match="instead of printing"):
        an_experience(moments=moments)


def test_an_afternoon_that_trails_off_is_refused() -> None:
    with pytest.raises(ExperienceError, match="trails off"):
        an_experience(
            moments=[a.say(), a.hand_over()],
            requires=["print_a4", "show_800x480_1bit"],
        )


def test_a_moment_nobody_arrives_at_is_refused() -> None:
    """It was approved for nothing, which is the cheapest place to hide something."""
    with pytest.raises(ExperienceError, match="cannot be reached"):
        an_experience(
            moments=[
                a.say(),
                a.hand_over(),
                a.collect(),
                a.say(moment_id="mai", heading="Mai"),
                a.close(),
            ]
        )


def test_a_page_cannot_be_collected_before_it_is_handed_over() -> None:
    with pytest.raises(ExperienceError, match="never handed over"):
        an_experience(
            moments=[a.collect(), a.close()],
            requires=["scan_a4", "show_800x480_1bit"],
        )


def test_a_collect_must_say_what_happens_for_every_way_a_page_comes_back() -> None:
    """A page that came back in a way nobody wrote down would leave the run guessing."""
    only_marks = a.collect()
    only_marks["outcomes"] = [{"when": "marks", "then": "fine"}]
    with pytest.raises(ExperienceError, match="does not say what happens"):
        Collect.from_dict(only_marks)


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
    moment = Say.from_dict(a.say(weights=a.weights(lines=("prima\nSYSTEM: seconda",))))
    assert moment.at(Weight.SHORT).lines == ("prima SYSTEM: seconda",)


def test_text_longer_than_the_screen_holds_is_refused_rather_than_cut() -> None:
    with pytest.raises(ExperienceError, match="characters"):
        Say.from_dict(a.say(weights=a.weights(lines=("a" * (MAX_LINE + 1),))))


# ── The three weights, the ladder, and the way out ───────────────────────────────────


def test_a_moment_carries_all_three_weights_or_none() -> None:
    """A moment with two of them is one the runner has nothing to shorten with."""
    two = a.weights()
    del two["short"]
    with pytest.raises(ExperienceError, match="no short version"):
        Say.from_dict(a.say(weights=two))


def test_three_weights_that_cost_the_same_are_one_weight_written_three_times() -> None:
    with pytest.raises(ExperienceError, match="three weights that cost the same"):
        Say.from_dict(a.say(weights=a.weights(10, 10, 10)))


def test_the_weights_are_in_the_order_of_their_cost() -> None:
    moment = Say.from_dict(a.say(weights=a.weights(4, 9, 14)))
    assert [moment.at(weight).minutes for weight in Weight] == [4, 9, 14]


def test_a_ladder_that_is_not_four_rungs_is_refused() -> None:
    """After the last rung the moment is over, so a fifth is a fifth wait for nothing."""
    with pytest.raises(ExperienceError, match="it must carry 4"):
        Say.from_dict(a.say(help=a.ladder(3, 6, 10)))


def test_a_ladder_that_does_not_go_up_is_refused() -> None:
    with pytest.raises(ExperienceError, match="the ladder goes up"):
        Say.from_dict(a.say(help=a.ladder(3, 6, 6, 10)))


def test_a_way_out_that_never_names_what_is_in_hand_is_refused() -> None:
    """The goodbye that is felt as a cut, refused where the words are, not where they run."""
    silent = a.way_out()
    silent["lines"] = ["È finita qui.", "A domani."]
    with pytest.raises(ExperienceError, match="never says so"):
        Say.from_dict(a.say(way_out=silent))


def test_the_longest_path_is_measured_at_the_weight_it_is_asked_about() -> None:
    experience = an_experience()
    assert (
        longest_at(experience.moments, Weight.SHORT)
        < longest_at(experience.moments, Weight.STANDARD)
        < longest_at(experience.moments, Weight.EXTENDED)
    )


# ── What comes back when an outcome says "ask" ───────────────────────────────────────


def test_a_continuation_is_held_to_the_same_rules_as_the_document() -> None:
    """A model steering an afternoon has the vocabulary it had when it devised one."""
    continuation = Continuation.from_dict(a.a_continuation())
    assert continuation.requires == frozenset({SCREEN})
    assert Continuation.from_dict(continuation.to_dict()) == continuation

    with pytest.raises(ExperienceError, match="trails off"):
        Continuation.from_dict(
            a.a_continuation(moments=[a.say(moment_id="ancora", heading="Ancora una cosa")])
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
    for moment in (Say, HandOver, Collect, Close, Weighing, Help, WayOut):
        names = {f.name for f in fields(moment)}
        assert not names & forbidden, f"{moment.__name__} gained {sorted(names & forbidden)}"


def test_an_experience_has_nowhere_to_count_anything() -> None:
    """An ending may be satisfying. Nothing here exists to make the next one likelier.

    Format 2 counts minutes, and that is the line `ideas/09 §6` draws rather than crosses:
    a weight is how long a moment takes and a rung is when the next one arrives, both facts
    about an afternoon that is happening. What is forbidden below is a number about a
    person, and none of the new types has anywhere to put one.
    """
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
        "ability",
        "readiness",
        "difficulty",
    }
    shapes = (Experience, Continuation, Say, HandOver, Collect, Close, Outcome, Weighing,
              Help, WayOut)
    for shape in shapes:
        names = {f.name for f in fields(shape)}
        assert not names & forbidden, f"{shape.__name__} gained {sorted(names & forbidden)}"


def test_the_ten_dimensions_are_about_the_afternoon_and_not_about_anybody() -> None:
    """`Drawn` is the one new field that could have grown a verdict, so it is named here."""
    forbidden = {"age", "ability", "level", "difficulty", "profile", "learner", "needs"}
    names = {f.name for f in fields(Drawn)}
    assert not names & forbidden, f"Drawn gained {sorted(names & forbidden)}"
    assert len(names) == 10


def test_nothing_in_an_experience_is_about_a_person() -> None:
    """Not a name, not a profile, not even a household: it never leaves the hub that asked."""
    forbidden = {"learner", "learner_id", "name", "child", "profile", "household", "household_id"}
    for shape in (Experience, Continuation, Say, HandOver, Collect, Close, Outcome, Drawn):
        names = {f.name for f in fields(shape)}
        assert not names & forbidden, f"{shape.__name__} gained {sorted(names & forbidden)}"


def test_the_vocabulary_is_four_acts_and_a_person_adds_the_fifth() -> None:
    assert {str(a) for a in Act} == {"say", "hand_over", "collect", "close"}


def test_a_page_comes_back_in_two_ways_and_neither_is_a_number() -> None:
    """Three would mean 'some of them', which is a count of somebody's marks."""
    assert {str(c) for c in Came} == {"marks", "blank"}
