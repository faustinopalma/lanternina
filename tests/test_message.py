"""What a parent may say while an afternoon runs, and what it must never produce.

The interesting half of these is the refusals. A closed list is only a defence if nothing
can be said that is not on it, and an end hour that moves is only safe if nothing about it
reaches the person it affects.

The acceptance test of the whole design is here too — `ideas/09 §19` asks for an afternoon
run to a complete ending in a session where the end hour is moved forward halfway through,
with nothing in what the person saw that says anything was shortened.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pytest

from devices import pretend as simulated
from devices.house import House
from devices.run_experience import (
    Afternoon,
    begin,
    conclude_what_is_over,
    hear,
    offer_help,
    waiting_runs,
)
from shared.experience import Experience
from shared.message import Message, MessageError, Says, at_the_clock

THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")
MINUTE = 60.0
# A moment in the middle of an afternoon, named by the calendar rather than asserted.
WHEN = time.mktime((2026, 8, 24, 14, 0, 0, 0, 0, -1))


@pytest.fixture
def where(tmp_path: Path) -> Path:
    return tmp_path / "pretend"


@pytest.fixture
def house(where: Path) -> House:
    return House(sheets_dir=where / "state", pretend=where)


def an_experience() -> Experience:
    return Experience.from_dict(json.loads(THE_AFTERNOON.read_text(encoding="utf-8")))


def waiting(house: House) -> Afternoon:
    path = sorted((house.sheets_dir / "afternoons").glob("*.json"))[0]
    return Afternoon.from_dict(json.loads(path.read_text(encoding="utf-8")))


def said(house: House) -> list[dict[str, Any]]:
    pretend = house.pretending
    assert pretend is not None
    return [line for line in simulated.read_transcript(pretend) if line["what"] == "display"]


# ── The list is closed ───────────────────────────────────────────────────────────────


def test_there_are_two_things_a_parent_may_say() -> None:
    """A third is a decision, and the shortness is the design rather than an omission."""
    assert {str(s) for s in Says} == {"end_by", "close_now"}


def test_a_sentence_cannot_be_said_at_all() -> None:
    """The defence against free text is not screening it. It is having nowhere to put it."""
    with pytest.raises(MessageError, match="not something a parent may say"):
        Message.from_dict({"says": "he is being lazy, push him"})


def test_a_field_nobody_declared_is_refused() -> None:
    with pytest.raises(MessageError, match="note"):
        Message.from_dict({"says": "close_now", "note": "she seems tired"})


def test_an_hour_that_is_not_on_the_clock_is_refused() -> None:
    with pytest.raises(MessageError):
        Message(says=Says.END_BY, written_at=0.0, minutes=24 * 60)
    with pytest.raises(MessageError, match="not a time on the clock"):
        at_the_clock("25:00")
    assert at_the_clock("17:30") == 17 * 60 + 30


# ── Moving the end hour ──────────────────────────────────────────────────────────────


def test_an_end_hour_moved_earlier_brings_the_ending_forward(house: House) -> None:
    experience = an_experience()
    begin(house, experience, now=WHEN, send=False)
    was = waiting(house).over_at

    changed = hear(house, [Message(says=Says.END_BY, written_at=WHEN, minutes=15 * 60)], WHEN)

    assert changed and "15:00" in changed[0]
    assert waiting(house).over_at < was


def test_an_end_hour_moved_later_pushes_it_back(house: House) -> None:
    """One message and not two. A separate "more time" is a second way to say one thing."""
    experience = an_experience()
    begin(house, experience, now=WHEN, send=False)
    was = waiting(house).over_at

    hear(house, [Message(says=Says.END_BY, written_at=WHEN, minutes=21 * 60)], WHEN)

    assert waiting(house).over_at > was


def test_close_now_brings_the_ending_to_this_instant(house: House) -> None:
    """Not "stop". The afternoon still ends, by the way out and then its close."""
    begin(house, an_experience(), now=WHEN, send=False)

    hear(house, [Message(says=Says.CLOSE_NOW, written_at=WHEN)], WHEN)

    assert waiting(house).ending_starts_at <= WHEN


def test_an_afternoon_already_on_its_way_out_does_not_hear_it(house: House) -> None:
    """The way out is in somebody's hands; moving the hour under it cuts or strands it."""
    experience = an_experience()
    begin(house, experience, now=WHEN, send=False)
    conclude_what_is_over(house, WHEN + (experience.minutes - 20) * MINUTE, send=False)
    assert waiting(house).leaving_at
    was = waiting(house).over_at

    assert hear(house, [Message(says=Says.CLOSE_NOW, written_at=WHEN)], WHEN) == []
    assert waiting(house).over_at == was


def test_the_end_hour_survives_being_written_down_and_read_back(house: House) -> None:
    """`ideas/09 §6` calls the current end hour one of the things a runner rebuilds from."""
    begin(house, an_experience(), now=WHEN, send=False)
    hear(house, [Message(says=Says.END_BY, written_at=WHEN, minutes=16 * 60)], WHEN)

    kept = waiting(house)
    again = Afternoon.from_dict(json.loads(json.dumps(kept.to_dict())))

    assert again.over_at == kept.over_at
    assert again.over_at != again.started_at + again.experience.minutes * MINUTE


def test_a_run_written_before_the_hour_could_move_still_has_one(house: House) -> None:
    begin(house, an_experience(), now=WHEN, send=False)
    path = sorted((house.sheets_dir / "afternoons").glob("*.json"))[0]
    older = json.loads(path.read_text(encoding="utf-8"))
    del older["over_at"]

    run = Afternoon.from_dict(older)

    assert run.over_at == run.started_at + run.experience.minutes * MINUTE


# ── What it must never produce ───────────────────────────────────────────────────────


def test_hearing_a_message_draws_nothing(house: House) -> None:
    """`ideas/09 §8`: no text a parent sends may reveal that the channel exists.

    The way to be sure is that the function draws nothing at all, so this counts screens.
    """
    begin(house, an_experience(), now=WHEN, send=False)
    quiet = len(said(house))

    hear(house, [Message(says=Says.END_BY, written_at=WHEN, minutes=15 * 60)], WHEN)
    hear(house, [Message(says=Says.CLOSE_NOW, written_at=WHEN)], WHEN)

    assert len(said(house)) == quiet


def test_a_message_carries_nothing_about_a_person() -> None:
    from dataclasses import fields

    forbidden = {"note", "text", "reason", "who", "name", "learner", "child", "mood", "why"}
    assert not {f.name for f in fields(Message)} & forbidden


# ── The acceptance test of the whole design ──────────────────────────────────────────


def test_an_afternoon_whose_hour_moves_halfway_still_ends_the_same_way(house: House) -> None:
    """`ideas/09 §19`, "done when", less the parent's own channel and the approval.

    Begun, helped, its end hour pulled forward halfway through, and run to its written
    close — with nothing on any screen that says a word about shortening, adapting, hurrying
    or time remaining.
    """
    experience = an_experience()
    begin(house, experience, now=WHEN, send=False)
    at = experience.moment(waiting(house).waiting_at)

    offer_help(house, WHEN + at.help[0].after_minutes * MINUTE, send=False)
    hear(house, [Message(says=Says.END_BY, written_at=WHEN, minutes=15 * 60)], WHEN)

    # Over by 15:00, so the ending is due at 14:30 and not a minute before it. Nothing
    # happens at 14:20, and that is the arithmetic working rather than the message failing.
    assert conclude_what_is_over(house, WHEN + 20 * MINUTE, send=False) == []
    assert said(house)[-1]["heading"] == at.heading

    conclude_what_is_over(house, WHEN + 35 * MINUTE, send=False)
    assert said(house)[-1]["heading"] == at.way_out.heading, "the way out, not a goodbye"

    ended = conclude_what_is_over(house, WHEN + 45 * MINUTE, send=False)
    assert len(ended) == 1
    assert said(house)[-1]["heading"] == experience.moment("basta-cosi").heading
    assert waiting_runs(house.sheets_dir) == []

    from shared.blocklist import blocked_in

    for line in said(house):
        found = blocked_in(" ".join([line["heading"], *line["lines"]]))
        assert not found, f"{[str(f) for f in found]} reached a display"
