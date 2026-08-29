"""What is kept about an afternoon, and what cannot be.

`panel/what_happened.py` is the relaxation of 28 August 2026: the system keeps what its
afternoons came to, so the next one can be written from it. What bounds it is the shape,
and that is what these check — a field for a score or a level would have to be added here
before it could be written anywhere, and adding it makes a test fail.
"""

from __future__ import annotations

import json
from dataclasses import fields, replace

from panel.what_happened import (
    CLOSED,
    LESS,
    MORE,
    STEADY,
    STOPPED,
    WAY_OUT,
    Afternoon,
    Answered,
    InMemoryWhatHappenedStore,
    as_material,
    clean_reading,
    how_it_has_gone,
    remembered,
    the_ground,
)

A_DOCUMENT = {
    "experience_id": "le-nuvole",
    "title": "Un pomeriggio di nuvole",
    "themes": ["il cielo", "una finestra"],
}


def an_afternoon(run_id: str = "run-1", **changed: object) -> Afternoon:
    made = remembered(
        household_id="h1",
        run_id=run_id,
        experience=A_DOCUMENT,
        at=100.0,
        weight="standard",
        minutes=95,
        reached="il-foglio",
        ending=CLOSED,
        answered=(Answered(moment_id="il-foglio", came="marks", reading="tre righe scritte"),),
    )
    return made if not changed else replace(made, **changed)  # type: ignore[arg-type]


def test_what_is_kept_is_what_happened_and_never_who_somebody_is() -> None:
    """The list is written out. A field about a person has to be added here first, and
    adding it fails this."""
    assert {one.name for one in fields(Afternoon)} == {
        "household_id",
        "run_id",
        "experience_id",
        "title",
        "at",
        "themes",
        "weight",
        "minutes",
        "reached",
        "ending",
        "answered",
    }
    assert {one.name for one in fields(Answered)} == {"moment_id", "came", "reading"}


def test_an_ending_nobody_agreed_on_is_dropped() -> None:
    """The vocabulary is closed so nothing can file a judgement under a new name."""
    assert remembered(
        household_id="h1", run_id="r", experience=A_DOCUMENT, at=1.0, ending="did_badly"
    ).ending == ""


def test_a_reading_is_one_line_and_bounded() -> None:
    assert clean_reading("due  righe\nscritte") == "due righe scritte"
    assert len(clean_reading("x" * 900)) == 400
    assert clean_reading(None) == ""


def test_the_same_afternoon_reported_twice_is_one_row() -> None:
    store = InMemoryWhatHappenedStore()
    store.remember(an_afternoon())
    store.remember(an_afternoon(ending=STOPPED))

    kept = store.list("h1")
    assert len(kept) == 1
    assert kept[0].ending == STOPPED


def test_the_parent_can_delete_all_of_it() -> None:
    store = InMemoryWhatHappenedStore()
    store.remember(an_afternoon())

    store.forget("h1")

    assert store.list("h1") == []


def test_every_subject_ever_offered_comes_back_once_each_in_order() -> None:
    """Kept for the band it lands in: a subject from last week is a repeat and the same
    subject from long ago is somewhere to return to."""
    ground = the_ground([("il cielo",), ("una finestra",), ("il rumore",)])

    assert ground.just_used == ("il cielo", "una finestra", "il rumore")
    assert ground.used_lately == ()
    assert ground.used_before == ()


def test_a_subject_lands_in_the_band_of_the_last_time_it_was_used() -> None:
    """Used long ago and again yesterday is not old ground."""
    before = [("il cielo",)] + [(f"altro-{n}",) for n in range(12)] + [("il cielo",)]

    ground = the_ground(before)

    assert "il cielo" in ground.just_used
    assert "il cielo" not in ground.used_before


def test_the_oldest_band_is_compacted_and_keeps_the_ruts() -> None:
    """A flat list of everything stops fitting in a prompt. What is dropped is the
    subjects used once, not the ones this house keeps being given."""
    old = [("la rotaia",) if n % 2 == 0 else (f"una-volta-{n}",) for n in range(40)]
    ground = the_ground(old + [("oggi",)] * 11)

    assert len(ground.used_before) == 12
    assert ground.used_before[0] == "la rotaia"


def test_a_house_with_no_history_is_told_nothing_about_the_ground() -> None:
    assert the_ground([]).anything() is False


def test_how_much_to_ask_for_is_read_off_the_runs_and_not_stored() -> None:
    carried = [
        an_afternoon(f"run-{n}", ending=CLOSED) for n in range(4)
    ]
    assert how_it_has_gone(carried).direction() == MORE

    gave_up = [
        replace(an_afternoon(f"run-{n}"), ending=STOPPED, answered=()) for n in range(4)
    ]
    assert how_it_has_gone(gave_up).direction() == LESS

    mixed = [
        replace(an_afternoon("a"), ending=CLOSED),
        replace(an_afternoon("b"), ending=WAY_OUT),
        replace(an_afternoon("c"), ending=CLOSED, answered=(
            Answered(moment_id="x", came="blank"),
        )),
    ]
    assert how_it_has_gone(mixed).direction() == STEADY


def test_two_runs_are_not_enough_to_lean_on() -> None:
    """Every instinct says to move after one bad afternoon. One afternoon is a Tuesday."""
    two = [replace(an_afternoon(f"run-{n}"), ending=STOPPED) for n in range(2)]

    assert how_it_has_gone(two).direction() == STEADY


def test_the_counts_carry_no_level_and_no_name() -> None:
    counted = how_it_has_gone([an_afternoon()]).to_dict()

    assert set(counted) == {
        "afternoonsRun",
        "ranToTheEnd",
        "endedEarly",
        "stopped",
        "sheetsWrittenOn",
        "sheetsBlank",
    }


def test_what_reaches_the_prompt_carries_no_identifier() -> None:
    """Run ids name nothing a model can use, and a household id in a prompt is the one
    thing that could tie a story to a person."""
    said = as_material([an_afternoon()])
    rows = json.loads(said)

    assert rows[0]["title"] == "Un pomeriggio di nuvole"
    assert rows[0]["sheets"] == [{"came": "marks", "onIt": "tre righe scritte"}]
    assert "run-1" not in said
    assert "h1" not in said


def test_a_house_that_has_run_nothing_says_nothing() -> None:
    """An empty list rather than an empty history: a model handed 'nothing happened yet'
    finds a way to make the afternoon about that."""
    assert as_material([]) == ""


def test_the_prompt_gets_the_recent_ones_and_the_store_keeps_them_all() -> None:
    store = InMemoryWhatHappenedStore()
    for number in range(12):
        store.remember(an_afternoon(f"run-{number}"))

    assert len(store.list("h1")) == 12
    assert len(json.loads(as_material(store.list("h1")))) == 8
