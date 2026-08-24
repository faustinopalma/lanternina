"""Running an afternoon: the branch, the ending, and the page nobody could read.

No hardware. The display is a file, the printer is a name with nothing sent to it, and
the glass is a function this module replaces — so what is checked here is the seam, which
is the part that is new. The experience is the real one in `experiences/`, not a fixture,
because a format that only runs on documents written for the test is not running.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import afternoons as a
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


# ── The press goes to the afternoon ──────────────────────────────────────────────────


def _a_press(house: House, tmp_path: Path) -> tuple[Path, list[str]]:
    """The button file the display server writes, and a place to record where it went."""
    button = tmp_path / "button.json"
    button.write_text(json.dumps({"friendlyId": "CF7D04"}), encoding="utf-8")
    return button, []


def test_a_press_while_an_afternoon_waits_goes_to_the_afternoon(
    house: House, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`ideas/09 §24`. Measured in the house on 24 August 2026: a page was read correctly
    and the afternoon stood still, because the press went to the standalone reader."""
    from devices import scan_sheet

    begin(house, an_experience(), now=0.0, send=False)
    button, went = _a_press(house, tmp_path)
    monkeypatch.setattr(scan_sheet, "_to_the_afternoon", lambda *a, **k: went.append("run") or 0)
    monkeypatch.setattr(
        scan_sheet, "find_scanner", lambda *a: went.append("scanner") or "glass"
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_sheet", str(button), str(house.sheets_dir), str(tmp_path / "s.bmp"), "glass"],
    )

    assert scan_sheet.main() == 0
    assert went == ["run"]


def test_a_press_with_no_afternoon_reads_the_sheet_on_its_own(
    house: House, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The other half of the same decision: a sheet on the glass with nothing running is
    still described the way it always was."""
    from devices import scan_sheet

    house.sheets_dir.mkdir(parents=True, exist_ok=True)
    button, went = _a_press(house, tmp_path)
    monkeypatch.setattr(scan_sheet, "_to_the_afternoon", lambda *a, **k: went.append("run") or 0)
    monkeypatch.setattr(
        scan_sheet,
        "find_scanner",
        lambda *a: went.append("scanner") or (_ for _ in ()).throw(OSError("no scanner")),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_sheet", str(button), str(house.sheets_dir), str(tmp_path / "s.bmp"), "glass"],
    )

    assert scan_sheet.main() == 0
    assert went == ["scanner"]


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
        "format_version": 2,
        "experience_id": "un-pomeriggio-di-nuvole",
        "after": after,
        "moments": [
            a.close(
                moment_id="la-terza-nuvola",
                heading="Le hai fatte tutte e due",
                weights=a.weights(lines=("Il foglio resta sul tavolo.",)),
            )
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


def test_a_page_arriving_after_the_ending_is_due_takes_the_way_out(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The ending is the hour's decision, and the page is the moment it becomes visible.

    Before 23 August 2026 this returned "that afternoon is over" and deleted the run: an
    afternoon that stopped without ending, on the branch where somebody had just done the
    thing and walked over with it. Now the way out of wherever it got to goes on the
    display, and the run stays until the close follows it.
    """
    said: list[str] = []
    monkeypatch.setattr(
        run_experience, "show", lambda _h, heading, _lines: said.append(heading)
    )
    experience = an_experience()
    begin(house, experience, now=0.0, send=False)
    glass(monkeypatch, house, marks=True)

    # Twenty minutes before the end hour, which is ten minutes past when the ending is due.
    when = (experience.minutes - 20) * 60
    told = carry_on(house, now=when, send=False)

    assert told == "that afternoon is on its way to the ending"
    assert said[-1] == experience.moment("come-e-tornato").way_out.heading
    assert len(runs(house)) == 1, "it ends properly, so it is not gone yet"


def test_a_page_from_no_afternoon_is_refused(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    begin(house, an_experience(), now=0.0, send=False)
    spec = glass(monkeypatch, house, marks=True)
    (house.sheets_dir / "afternoons" / "pages" / f"{spec.sheet_id}.json").unlink()

    with pytest.raises(CannotRun, match="does not belong to an afternoon"):
        carry_on(house, now=1.0, send=False)
