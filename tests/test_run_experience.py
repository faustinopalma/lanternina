"""Running an afternoon: the branch, the ending, and the page nobody could read.

No hardware. The display is a file, the printer is a name with nothing sent to it, and
the glass is a function this module replaces — so what is checked here is the seam, which
is the part that is new. The experience is the real one in `experiences/`, not a fixture,
because a format that only runs on documents written for the test is not running.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from devices import run_experience
from devices.house import CannotRun, House
from devices.print_sheet import recall
from devices.run_experience import Afternoon, begin, came_back, carry_on, load_experience
from shared.experience import Came, Experience
from shared.ids import CellId, ExerciseId, SheetId
from shared.sheet import CellKind, SheetSpec
from shared.vision_contracts import CellReading, PageReading, ReadConfidence

THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")


@pytest.fixture
def house(tmp_path: Path) -> House:
    return House(
        printer="paper",
        scanner="glass",
        screen=tmp_path / "screen.bmp",
        sheets_dir=tmp_path / "sheets",
        panel="https://panel.example",
        household="hh_1",
        device_key="k",
    )


def an_experience() -> Experience:
    return load_experience(THE_AFTERNOON)


def last_sheet(house: House) -> SheetSpec:
    """The spec of the most recently printed sheet, which is what would be on the glass."""
    printed = sorted(house.sheets_dir.glob("sh_*.json"), key=lambda p: p.stat().st_mtime)
    return recall(house.sheets_dir, SheetId(printed[-1].stem))


def _reading(spec: SheetSpec, *, marks: bool, unsure: bool = False) -> PageReading:
    return PageReading(
        sheet_id=spec.sheet_id,
        exercise_id=spec.exercise_id,
        cells=tuple(
            CellReading(
                cell_id=CellId(str(cell.id)),
                kind=CellKind(cell.kind),
                value=cell.label if marks and index == 0 else None,
                confidence=ReadConfidence.UNSURE if unsure else ReadConfidence.LIKELY,
                needs_review=unsure,
            )
            for index, cell in enumerate(spec.cells)
        ),
        read_at=0.0,
    )


def glass(monkeypatch: pytest.MonkeyPatch, house: House, **how: Any) -> SheetSpec:
    """Put the sheet that was printed last on the scanner, read as ``how`` says."""
    spec = last_sheet(house)
    monkeypatch.setattr(run_experience, "_read", lambda _house: (spec, _reading(spec, **how)))
    return spec


def runs(house: House) -> list[Path]:
    return sorted((house.sheets_dir / "afternoons").glob("aft_*.json"))


def pointers(house: House) -> list[Path]:
    return sorted((house.sheets_dir / "afternoons" / "pages").glob("*.json"))


# ── Beginning ────────────────────────────────────────────────────────────────────────


def test_it_plays_up_to_the_first_page_and_waits(house: House) -> None:
    run_id = begin(house, an_experience(), now=0.0, send=False)

    assert run_id and run_id.startswith("aft_")
    assert house.screen is not None and house.screen.is_file(), "the display was written"
    assert len(runs(house)) == 1
    at = Afternoon.from_dict(json.loads(runs(house)[0].read_text(encoding="utf-8")))
    assert at.waiting_at == "come-e-tornato"
    # The paper points back at the afternoon, so two sheets in the house cannot be confused.
    assert [p.stem for p in pointers(house)] == [str(last_sheet(house).sheet_id)]


def test_a_house_without_the_equipment_is_not_offered_it(tmp_path: Path) -> None:
    bare = House(sheets_dir=tmp_path)
    with pytest.raises(CannotRun, match="cannot run"):
        begin(bare, an_experience(), now=0.0, send=False)


# ── What came back ───────────────────────────────────────────────────────────────────


def test_a_page_with_a_mark_takes_the_branch_that_was_written(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    begin(house, an_experience(), now=0.0, send=False)
    first = glass(monkeypatch, house, marks=True)

    said = carry_on(house, now=1.0, send=False)

    assert said == "waiting for a page at l-ultimo-foglio"
    second = last_sheet(house)
    assert second.sheet_id != first.sheet_id
    assert second.title == "La nuvola che non c'era"
    # Both pages now point at the one afternoon: either can come back next.
    assert len(pointers(house)) == 2


def test_a_blank_page_ends_the_afternoon_and_leaves_nothing(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    begin(house, an_experience(), now=0.0, send=False)
    glass(monkeypatch, house, marks=False)

    said = carry_on(house, now=1.0, send=False)

    assert said == "the afternoon is finished"
    assert runs(house) == [], "an afternoon that ended keeps no record that it happened"
    assert pointers(house) == []


def test_a_page_nobody_could_read_does_not_become_a_blank_one(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The failure this guards against closes an afternoon on a page that was filled in."""
    begin(house, an_experience(), now=0.0, send=False)
    glass(monkeypatch, house, marks=False, unsure=True)

    said = carry_on(house, now=1.0, send=False)

    assert "not clear enough" in said
    assert len(runs(house)) == 1, "the afternoon is still waiting where it was"


def test_the_two_words_are_read_off_ink_and_nothing_else() -> None:
    """A page with no cells at all is blank: there was nowhere for a mark to be."""
    empty = PageReading(SheetId("sh_1"), ExerciseId("ex_1"), (), 0.0)
    assert came_back(empty) is Came.BLANK


# ── Asking ───────────────────────────────────────────────────────────────────────────


class _Answer:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def __enter__(self) -> _Answer:
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode()


def a_continuation(after: str = "l-ultimo-foglio", **changes: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "format_version": 1,
        "experience_id": "un-pomeriggio-di-nuvole",
        "after": after,
        "moments": [
            {
                "act": "close",
                "id": "la-terza-nuvola",
                "heading": "Le hai fatte tutte e due",
                "lines": ["Il pomeriggio finisce qui."],
            }
        ],
    }
    payload.update(changes)
    return payload


def reach_the_ask(house: House, monkeypatch: pytest.MonkeyPatch) -> None:
    begin(house, an_experience(), now=0.0, send=False)
    glass(monkeypatch, house, marks=True)
    carry_on(house, now=1.0, send=False)
    glass(monkeypatch, house, marks=True)


def test_an_ask_is_answered_inside_the_reply_and_then_played(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    reach_the_ask(house, monkeypatch)
    asked: dict[str, Any] = {}

    def _post(request: Any, timeout: int = 0) -> _Answer:
        asked["url"] = request.full_url
        asked["body"] = json.loads(request.data)
        return _Answer(a_continuation())

    monkeypatch.setattr(run_experience.urllib.request, "urlopen", _post)

    said = carry_on(house, now=2.0, send=False)

    assert said == "the afternoon is finished"
    assert asked["url"] == "https://panel.example/api/device/hh_1/experience"
    assert asked["body"]["after"] == "l-ultimo-foglio"
    assert asked["body"]["came"] == "marks"
    # What came back goes up: which boxes carry a mark is what the format cannot say.
    assert asked["body"]["reading"]["sheet_id"] == str(last_sheet(house).sheet_id)
    assert runs(house) == []


def test_a_continuation_for_another_afternoon_is_refused(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    reach_the_ask(house, monkeypatch)
    monkeypatch.setattr(
        run_experience.urllib.request,
        "urlopen",
        lambda request, timeout=0: _Answer(a_continuation(experience_id="un-altro")),
    )

    with pytest.raises(CannotRun, match="is for 'un-altro'"):
        carry_on(house, now=2.0, send=False)


def test_a_continuation_for_a_branch_that_was_not_taken_is_refused(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    reach_the_ask(house, monkeypatch)
    monkeypatch.setattr(
        run_experience.urllib.request,
        "urlopen",
        lambda request, timeout=0: _Answer(a_continuation(after="come-e-tornato")),
    )

    with pytest.raises(CannotRun, match="follows 'come-e-tornato'"):
        carry_on(house, now=2.0, send=False)


def test_with_no_panel_the_afternoon_stops_rather_than_carrying_on_by_itself(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    alone = House(
        printer="paper",
        scanner="glass",
        screen=tmp_path / "screen.bmp",
        sheets_dir=tmp_path / "sheets",
    )
    reach_the_ask(alone, monkeypatch)

    with pytest.raises(CannotRun, match="nobody to ask"):
        carry_on(alone, now=2.0, send=False)


# ── Stopping ─────────────────────────────────────────────────────────────────────────


def test_an_afternoon_whose_hours_ran_out_is_over_when_the_page_arrives(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Nothing here runs on a timer, so the hours are noticed when somebody comes back."""
    begin(house, an_experience(), now=0.0, send=False)
    glass(monkeypatch, house, marks=True)

    said = carry_on(house, now=180 * 60 + 1, send=False)

    assert said == "that afternoon is over"
    assert runs(house) == []
    assert pointers(house) == []


def test_a_page_from_no_afternoon_is_refused(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    begin(house, an_experience(), now=0.0, send=False)
    spec = glass(monkeypatch, house, marks=True)
    (house.sheets_dir / "afternoons" / "pages" / f"{spec.sheet_id}.json").unlink()

    with pytest.raises(CannotRun, match="does not belong to an afternoon"):
        carry_on(house, now=1.0, send=False)
