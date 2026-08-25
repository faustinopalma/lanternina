"""The wording asked for at the moment of a showing.

Two guarantees, both from a parent reading a real display on 25 August 2026. The prompt must
not be a function of the parent's sentence alone, or the same sentence comes back the same
every evening. And it must not ask for the clock time back: the hour was already read out
into its own field, and `devices/show_reminders.py` decides whether it appears at all.
"""

from __future__ import annotations

from agents import reminder_wording as wording


def test_the_prompt_is_not_a_function_of_the_sentence_alone() -> None:
    said = {wording._now(one) for one in wording.SAYINGS}

    assert len(said) == len(wording.SAYINGS) > 1


def test_every_saying_reads_on_from_say_it() -> None:
    for one in wording.SAYINGS:
        assert f"Say it {one}" in wording._now(one)


def test_the_clock_time_is_not_asked_for() -> None:
    """The old prompt carried `The hour: {at}` and told the model to leave nothing out."""
    said = wording._now(wording.SAYINGS[0])

    assert "The hour:" not in said
    assert "Leave the clock time out." in said
