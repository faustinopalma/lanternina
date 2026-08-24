"""The ladder, and the two lines it does not cross.

Every one of these is written the way round that matters: it puts an afternoon at a moment,
moves the clock, and asserts what appeared on the display. A test that only checked the
bookkeeping would pass on a version that never drew anything, and until 24 August 2026 that
version was the one that shipped — four rungs in every moment, checked before saving, shown
to the parent, and nothing anywhere that could reach them.

The two refusals are the interesting half. There is no fifth rung, and nothing ends an
afternoon because nobody came back.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from devices import pretend as simulated
from devices import run_experience
from devices.house import House
from devices.run_experience import Afternoon, begin, conclude_what_is_over, offer_help
from shared.experience import HELP_LEVELS, Experience

THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")
MINUTE = 60.0


@pytest.fixture
def where(tmp_path: Path) -> Path:
    return tmp_path / "pretend"


@pytest.fixture
def house(where: Path) -> House:
    return House(sheets_dir=where / "state", pretend=where)


def an_experience() -> Experience:
    return Experience.from_dict(json.loads(THE_AFTERNOON.read_text(encoding="utf-8")))


def said(house: House) -> list[dict[str, Any]]:
    pretend = house.pretending
    assert pretend is not None
    return [line for line in simulated.read_transcript(pretend) if line["what"] == "display"]


def waiting(house: House) -> Afternoon:
    path = sorted((house.sheets_dir / "afternoons").glob("*.json"))[0]
    return Afternoon.from_dict(json.loads(path.read_text(encoding="utf-8")))


def at_a_moment(house: House) -> tuple[Experience, Any]:
    """An afternoon begun at zero and waiting at its first collect."""
    experience = an_experience()
    begin(house, experience, now=0.0, send=False)
    return experience, experience.moment(waiting(house).waiting_at)


# ── The rungs arrive ─────────────────────────────────────────────────────────────────


def test_nothing_is_offered_before_the_first_rung_is_due(house: House) -> None:
    _, moment = at_a_moment(house)
    before = len(said(house))

    assert offer_help(house, moment.help[0].after_minutes * MINUTE - 1, send=False) == []
    assert len(said(house)) == before, "nothing went on the display"


def test_the_first_rung_arrives_when_its_minutes_have_passed(house: House) -> None:
    _, moment = at_a_moment(house)

    given = offer_help(house, moment.help[0].after_minutes * MINUTE, send=False)

    assert given and moment.id in given[0]
    last = said(house)[-1]
    assert last["lines"] == list(moment.help[0].lines)
    assert last["heading"] == moment.heading, "a rung is this moment speaking, not a new one"


def test_a_rung_is_offered_once(house: House) -> None:
    """The counter is what stops a minute-by-minute timer saying the same thing sixty times."""
    _, moment = at_a_moment(house)
    due = moment.help[0].after_minutes * MINUTE

    assert offer_help(house, due, send=False)
    assert offer_help(house, due + MINUTE, send=False) == []
    assert waiting(house).helped == 1


def test_the_rungs_are_counted_from_arriving_and_not_from_the_rung_before(
    house: House,
) -> None:
    """3, 6, 10, 15 means the answer at fifteen minutes, not at thirty-four.

    That reading is what makes the format's refusal of a ladder that does not go up mean
    something, so it is asserted here rather than left to the docstring.
    """
    _, moment = at_a_moment(house)

    for rung in range(HELP_LEVELS):
        due = moment.help[rung].after_minutes * MINUTE
        assert offer_help(house, due, send=False), f"rung {rung + 1} was not due at {due / 60} min"
        assert said(house)[-1]["lines"] == list(moment.help[rung].lines)


def test_a_long_silence_does_not_pour_out_the_whole_ladder_at_once(house: House) -> None:
    """One rung per look. Four screens in one second is the ladder shouting."""
    _, moment = at_a_moment(house)
    much_later = moment.help[-1].after_minutes * MINUTE * 10

    assert len(offer_help(house, much_later, send=False)) == 1
    assert waiting(house).helped == 1


# ── The two lines it does not cross ──────────────────────────────────────────────────


def test_there_is_no_fifth_rung(house: House) -> None:
    _, moment = at_a_moment(house)
    for rung in range(HELP_LEVELS):
        offer_help(house, moment.help[rung].after_minutes * MINUTE, send=False)
    quiet = len(said(house))

    assert offer_help(house, moment.help[-1].after_minutes * MINUTE * 100, send=False) == []
    assert len(said(house)) == quiet


def test_the_last_rung_does_not_end_the_afternoon(house: House) -> None:
    """`ideas/09 §4` says the moment is over and the afternoon moves on.

    Here the only moment an afternoon waits at is a collect, so moving on would mean ending
    the afternoon because nobody came back — an action triggered by silence, which the
    working rules forbid. The ending stays with the clock at T-30.
    """
    experience, moment = at_a_moment(house)
    for rung in range(HELP_LEVELS):
        offer_help(house, moment.help[rung].after_minutes * MINUTE, send=False)

    long_after = moment.help[-1].after_minutes * MINUTE + MINUTE
    assert conclude_what_is_over(house, long_after, send=False) == []
    assert run_experience.waiting_runs(house.sheets_dir), "the afternoon is still there"
    assert long_after < experience.moment(moment.id).way_out.minutes * MINUTE + MINUTE * 60


def test_no_rung_says_that_time_has_passed(house: House) -> None:
    """A rung is the same words somebody would get for asking, which is `§4`'s own rule.

    It can only be the same words if it never mentions waiting, so nothing here adds any.
    """
    _, moment = at_a_moment(house)
    for rung in range(HELP_LEVELS):
        offer_help(house, moment.help[rung].after_minutes * MINUTE, send=False)

    drawn = [line for line in said(house) if line["lines"]]
    for line in drawn[-HELP_LEVELS:]:
        assert line["lines"] in [list(rung.lines) for rung in moment.help], (
            "a rung went out with something added to it"
        )


def test_an_afternoon_on_its_way_to_the_ending_is_not_offered_help(house: House) -> None:
    """It is finishing, not stuck. A nudge on top of a goodbye is the seam showing."""
    experience, moment = at_a_moment(house)
    conclude_what_is_over(house, (experience.minutes - 20) * MINUTE, send=False)
    assert waiting(house).leaving_at

    much_later = (experience.minutes - 20) * MINUTE + moment.help[-1].after_minutes * MINUTE
    assert offer_help(house, much_later, send=False) == []


# ── The record, and what it may not become ───────────────────────────────────────────


def test_arriving_at_a_moment_resets_its_ladder(house: House) -> None:
    """A rung given at the moment before has nothing to do with this one.

    Carrying the count forward would be the beginning of a tally, which is the field this
    project must not grow.
    """
    _, moment = at_a_moment(house)
    offer_help(house, moment.help[0].after_minutes * MINUTE, send=False)
    assert waiting(house).helped == 1

    run = waiting(house)
    moved_on = Afternoon(
        run_id=run.run_id,
        experience=run.experience,
        started_at=run.started_at,
        waiting_at=run.waiting_at,
        weight=run.weight,
        printed=run.printed,
        waited_since=999.0,
    )

    assert moved_on.helped == 0, "a fresh moment starts with a fresh ladder"


def test_what_is_written_down_says_nothing_about_a_person(house: House) -> None:
    """The run file outlives a moment, so it is the one to look at.

    It may hold what is happening now — which moment, since when, how many rungs. It may
    not hold anything that survives the afternoon or reads as a claim, and the way to keep
    that true is that no field is ever named for one.
    """
    _, moment = at_a_moment(house)
    offer_help(house, moment.help[0].after_minutes * MINUTE, send=False)

    path = sorted((house.sheets_dir / "afternoons").glob("*.json"))[0]
    kept = json.loads(path.read_text(encoding="utf-8"))
    forbidden = {
        "score",
        "grade",
        "level",
        "ability",
        "readiness",
        "difficulty",
        "attempts",
        "helped_total",
        "help_history",
        "learner",
        "name",
        "streak",
    }

    assert not set(kept) & forbidden
    assert kept["helped"] == 1
    assert "waited_since" in kept


def test_the_ladder_is_gone_when_the_afternoon_is(house: House) -> None:
    """Nothing about a moment outlives the afternoon it belonged to."""
    experience, _ = at_a_moment(house)
    offer_help(house, 3 * MINUTE, send=False)

    conclude_what_is_over(house, (experience.minutes - 20) * MINUTE, send=False)
    conclude_what_is_over(house, experience.minutes * MINUTE, send=False)

    assert run_experience.waiting_runs(house.sheets_dir) == []
    assert not list((house.sheets_dir / "afternoons").glob("*.json"))
