"""The registry has two halves, and nothing works if they drift apart.

`shared/capabilities.py` says what a device is called and what it takes; `devices/hands.py`
says what happens in the room. Between them sit the jobs a parent hands out and the
vocabulary a deviser is given. Each of these tests fails on exactly one kind of
half-finished device, which is the point: adding one should be a file and a line, and
forgetting the line should be loud rather than quiet.

Written the day the registry replaced four hand-written tables, 25 August 2026. Each was
checked by deleting the entry it is about and watching it fail.
"""

from __future__ import annotations

import pytest

from devices import hands
from shared.capabilities import (
    HANDS,
    JOBS_BY_KIND,
    KINDS,
    NEEDS,
    REACHABLE,
    Act,
    provided_by,
)
from shared.experience_prompt import THE_ACTS


def test_every_verb_the_document_can_use_has_a_hand() -> None:
    """An act with no entry is a verb an experience can be devised around and never run."""
    assert {hand.act for hand in HANDS} == set(Act)


def test_every_hand_is_carried_out_by_something() -> None:
    """The other half. A hand described but never registered fails in the room, at the
    moment somebody is standing in front of it, which is the worst possible time."""
    assert hands.registered() == {hand.act for hand in HANDS}


def test_what_a_verb_needs_is_read_off_the_registry() -> None:
    assert NEEDS == {hand.act: hand.needs for hand in HANDS}
    assert set(NEEDS) == set(Act)


def test_a_hands_job_is_one_a_parent_can_actually_hand_out() -> None:
    """A hand naming a job the panel never offers is a capability no house can ever have.

    The panel writes its list from `JOBS_BY_KIND`, so a job spelled only here would be a
    device that works in the tests and is unreachable in every real house.
    """
    for hand in HANDS:
        assert hand.kind in KINDS, f"{hand.act} names a kind of thing that does not exist"
        assert hand.job in JOBS_BY_KIND[hand.kind], (
            f"{hand.act} wants the {hand.job!r} job, which no {hand.kind} can be given"
        )


def test_the_job_that_provides_a_capability_is_the_hands_own() -> None:
    for hand in HANDS:
        assert provided_by(hand.kind, hand.job) is hand.needs


def test_a_pretend_house_can_do_everything_a_verb_asks_for() -> None:
    """Simulation is where a device is tried before it exists in the hall.

    A capability reachable from a document but missing from `REACHABLE` is a device that
    cannot be exercised without buying the hardware first.
    """
    assert REACHABLE == set(NEEDS.values())
    assert all(hand.needs in REACHABLE for hand in HANDS)


def test_the_deviser_is_told_about_every_verb() -> None:
    """A hand the prompt never mentions is a device nothing will ever ask for."""
    for hand in HANDS:
        assert f'"act": "{hand.act}"' in THE_ACTS, f"{hand.act} is missing from the prompt"
        assert hand.describe in THE_ACTS, f"{hand.act} is in the prompt with no description"


def test_a_hand_describes_what_it_does_rather_than_naming_the_machine() -> None:
    """The sentence goes to a model devising for houses whose equipment it cannot know.

    "the Epson in the hall" would produce an afternoon that only runs in this house, which
    is the whole reason capabilities are named by what they do.
    """
    for hand in HANDS:
        assert hand.describe, f"{hand.act} has no description"
        assert hand.describe[0].islower(), f"{hand.describe!r} should read after 'It '"
        assert not hand.describe.endswith("."), f"{hand.describe!r} ends its own sentence"


def test_a_verb_with_no_hand_says_so_rather_than_falling_through() -> None:
    """The failure that a dispatch chain of if-statements used to produce silently.

    Before the registry the last branch caught everything, so an unhandled act put its
    heading on the display and moved on as though it had been carried out.
    """
    kept = dict(hands._MOVES)
    try:
        del hands._MOVES[Act.SAY]
        with pytest.raises(Exception, match="knows how to say"):
            hands.play(None, _AMoment(), None, None, False)  # type: ignore[arg-type]
    finally:
        hands._MOVES.clear()
        hands._MOVES.update(kept)


class _AMoment:
    act = Act.SAY
    id = "somewhere"
