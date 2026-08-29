"""The research loop, checked without spending a model call.

What is worth holding down here is not the scores — those are the output — but the two
things that would make a run silently meaningless: the driver reaching the real devising
path rather than a copy of it, and the player walking an afternoon the way the house does.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import tests.afternoons as a
from research import run as driver
from research.calls import _json_in
from research.play import CLOSED, STOPPED, WENT_WRONG, play
from research.report import IN_ORDER, write_report
from shared.experience import Experience, Weight


def an_afternoon() -> Experience:
    return Experience.from_dict(
        a.an_afternoon(
            moments=[
                a.say(),
                a.hand_over("il-foglio"),
                a.collect(on_marks="fine", on_blank="fine", if_no_page="fine"),
                a.close(),
            ]
        )
    )


class Pretend:
    """Stands in for the stand-in. No network, and it records what it was shown."""

    def __init__(self, came: str = "marks", stop: bool = False) -> None:
        self.came, self.stop, self.shown = came, stop, []

    async def what_they_did(self, ctx, **asked):  # noqa: ANN001, ANN003
        self.shown.append(asked)
        return {"came": self.came, "onIt": "tre parole", "stop": self.stop, "why": "così"}


def test_the_driver_devises_through_the_real_path_and_not_a_copy() -> None:
    """The whole apparatus is worth nothing if it exercises its own prompt. This fails if
    somebody inlines a prompt here to make a run cheaper or faster."""
    import panel.devising

    assert driver.devise_experience is panel.devising.devise_experience


@pytest.mark.asyncio
async def test_an_afternoon_played_through_reaches_its_close(monkeypatch) -> None:  # noqa: ANN001
    fake = Pretend()
    monkeypatch.setattr("research.play.what_they_did", fake.what_they_did)

    played = await play(
        None, experience=an_afternoon(), household="h", weight=Weight.STANDARD, mood="normale"
    )

    assert played.ending == CLOSED
    assert played.sheets[0]["came"] == "marks"
    assert "il foglio torna: marks" in played.transcript()


@pytest.mark.asyncio
async def test_the_sheet_reaches_the_stand_in_as_the_words_on_it(monkeypatch) -> None:  # noqa: ANN001
    """Not the JSON. What is being measured is whether a page says what to do, and braces
    around a title are our storage showing through."""
    fake = Pretend()
    monkeypatch.setattr("research.play.what_they_did", fake.what_they_did)

    await play(
        None, experience=an_afternoon(), household="h", weight=Weight.STANDARD, mood="normale"
    )

    sheet = fake.shown[0]["sheet"]
    assert "Una cosa" in sheet
    assert "{" not in sheet


@pytest.mark.asyncio
async def test_stopping_is_an_ending_and_the_way_out_is_played(monkeypatch) -> None:  # noqa: ANN001
    """Stopping costs nothing and is a legitimate outcome, so the loop has to record it as
    one rather than as a run that failed."""
    fake = Pretend(came="blank", stop=True)
    monkeypatch.setattr("research.play.what_they_did", fake.what_they_did)

    played = await play(
        None, experience=an_afternoon(), household="h", weight=Weight.SHORT, mood="storta"
    )

    assert played.ending == STOPPED
    assert "via d'uscita" in played.transcript()


@pytest.mark.asyncio
async def test_a_branch_that_leads_nowhere_is_a_defect_and_is_written_down(monkeypatch) -> None:  # noqa: ANN001
    """The format forbids it, so reaching it means something upstream is wrong and the run
    has to say so rather than looping."""
    fake = Pretend()
    monkeypatch.setattr("research.play.what_they_did", fake.what_they_did)
    document = a.an_afternoon(
        moments=[
            a.say(),
            a.hand_over("il-foglio"),
            a.collect(on_marks="fine", on_blank="fine", if_no_page="fine"),
            a.close(),
        ]
    )
    document["moments"][2]["outcomes"][0]["then"] = "fine"
    experience = Experience.from_dict(document)
    object.__setattr__(experience.moments[2].outcomes[0], "then", "non-esiste")

    played = await play(
        None, experience=experience, household="h", weight=Weight.STANDARD, mood="normale"
    )

    assert played.ending == WENT_WRONG
    assert "DIFETTO" in played.transcript()


def test_an_answer_wrapped_in_a_fence_is_still_read() -> None:
    assert _json_in('```json\n{"came": "marks"}\n```')["came"] == "marks"
    with pytest.raises(ValueError, match="no object"):
        _json_in("non c'è niente qui")


def test_the_report_is_written_even_when_an_afternoon_was_refused(tmp_path: Path) -> None:
    """A refusal is a result. A run that dropped them would hide the checks doing their
    job, which is the thing most worth seeing after a prompt changes."""
    summary = {
        "at": "x",
        "iterations": 1,
        "households": ["h"],
        "afternoons": 1,
        "refused": 1,
        "endings": {"closed": 0, "way_out": 0, "stopped": 0, "went_wrong": 0},
        "axes": {},
        "minutes": 0.1,
    }
    rows = [{"iteration": 1, "household": "h", "refused": {"by": "checks", "says": "troppa carta"}}]

    write_report(tmp_path, summary, rows)

    said = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "rifiutato dai checks" in said
    assert "troppa carta" in said


def test_every_axis_the_judge_is_asked_for_is_one_the_report_knows() -> None:
    """Two files that have to agree: a ninth axis added to the prompt and not to the report
    would be scored and then not shown."""
    asked = (Path("research") / "calls.appraisal.md").read_text(encoding="utf-8")
    for axis in IN_ORDER:
        assert f'"{axis}"' in asked


def test_the_axes_are_the_eight_that_are_documented() -> None:
    said = (Path("research") / "README.md").read_text(encoding="utf-8")
    for axis in IN_ORDER:
        assert f"`{axis}`" in said
    assert len(IN_ORDER) == 8


def test_the_summary_averages_only_what_was_scored() -> None:
    rows = [
        {"appraisal": {"axes": {"canBeStarted": {"score": 5}}}},
        {"appraisal": {"axes": {"canBeStarted": {"score": 2}}}},
        {"refused": {"by": "checks", "says": "…"}},
    ]

    assert driver._averages(rows) == {"canBeStarted": 3.5}


def test_a_household_carries_no_person(tmp_path: Path) -> None:
    """The real prompt has nowhere to put a name, so a fixture with one would be testing a
    path that does not exist."""
    from dataclasses import fields

    from research.households import HOUSEHOLDS, Household

    assert {one.name for one in fields(Household)} == {
        "name",
        "interests",
        "avoid",
        "difficulty",
        "variety",
        "language",
        "sheets",
        "note",
        "guidelines",
    }
    assert len(HOUSEHOLDS) == 6
    assert json.dumps([one.name for one in HOUSEHOLDS])
