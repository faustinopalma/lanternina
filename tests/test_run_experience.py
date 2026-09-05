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
from devices.print_page import recall
from devices.run_experience import Afternoon, begin, came_back, carry_on, load_experience
from shared.experience import Came, Experience
from shared.ids import SheetId
from shared.vision_contracts import WhatCameBack

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


@pytest.fixture(autouse=True)
def the_page_is_drawn(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every hand_over asks the panel for a page. Standing in for it here rather than in
    each test: a test that forgot would reach the network and fail slowly and confusingly."""
    import numpy as np

    monkeypatch.setattr(
        "devices.hands.draw_page",
        lambda page, **_: np.full((1536, 1024), 255, dtype=np.uint8),
    )


def an_experience() -> Experience:
    return load_experience(THE_AFTERNOON)


def last_sheet(house: House) -> SheetId:
    """The id of the most recently printed sheet, which is what would be on the glass."""
    from devices.print_page import waiting

    return waiting(house.sheets_dir)[-1]


def _reading(*, marks: bool, degraded: bool = False) -> WhatCameBack:
    return WhatCameBack(
        written=marks,
        same_sheet=True,
        describes=("una casa disegnata in alto",) if marks else (),
        read_at=0.0,
        degraded=degraded,
    )


def glass(monkeypatch: pytest.MonkeyPatch, house: House, **how: Any) -> SheetId:
    """Put the sheet that was printed last on the scanner, read as ``how`` says."""
    sheet_id = last_sheet(house)
    monkeypatch.setattr(
        run_experience, "_read", lambda _house, _run=None: (str(sheet_id), _reading(**how))
    )
    return sheet_id


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
    assert [p.stem for p in pointers(house)] == [str(last_sheet(house))]


def test_a_house_without_the_equipment_is_not_offered_it(tmp_path: Path) -> None:
    bare = House(sheets_dir=tmp_path)
    with pytest.raises(CannotRun, match="cannot run"):
        begin(bare, an_experience(), now=0.0, send=False)


def test_a_page_the_printer_never_took_is_filed_as_a_fault_with_its_reason(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The whole of 5 September 2026 in one test.

    The queue accepted two pages and the printer was on another network. The afternoon went
    on as if paper were on the table, the display climbed to the last rung of help for it,
    and the panel showed an afternoon that had gone as written. Now the page never counts as
    handed over, the words the afternoon carries for that case are what the room gets, and
    the reason reaches the parent instead of only the journal.
    """
    import subprocess as sub

    from devices import print_page as printing

    def never_takes(argv: list[str], **kw: object) -> sub.CompletedProcess[bytes]:
        if argv[0] == "lp":
            return sub.CompletedProcess(argv, 0, b"request id is Lanternina-19\n", b"")
        if argv[0] == "lpstat":
            return sub.CompletedProcess(argv, 0, b"Lanternina-19 fausto 100352\n", b"")
        return sub.CompletedProcess(argv, 0, b"", b"")

    monkeypatch.setattr(printing.subprocess, "run", never_takes)
    monkeypatch.setattr(printing.time, "sleep", lambda _: None)
    monkeypatch.setattr(printing, "TOOK_THE_PAGE_SECONDS", 0.0)

    filed: list[dict[str, Any]] = []
    monkeypatch.setattr(
        run_experience, "_tell_the_panel", lambda _h, _r, what: filed.append(what)
    )

    begin(house, an_experience(), now=0.0, send=True)

    from devices.print_page import waiting

    assert waiting(house.sheets_dir) == [], "no sheet is on the table, so none is waited for"
    faults = [one for one in filed if one["kind"] == "fault"]
    assert len(faults) == 1, "the parent is told once, on the afternoon it happened to"
    assert any("did not take the page" in line for line in faults[0]["lines"]), (
        "the reason has to say it was the printer, not that something went wrong"
    )


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
    assert second != first
    # A sheet is named by nothing printed on it, so what says which page this is is the
    # blank the house kept beside it. `ideas/10 §3`: expectation, and the page as evidence.
    assert recall(house.sheets_dir, second).shape == recall(house.sheets_dir, first).shape
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
    glass(monkeypatch, house, marks=False, degraded=True)

    said = carry_on(house, now=1.0, send=False)

    assert "not clear enough" in said
    assert len(runs(house)) == 1, "the afternoon is still waiting where it was"


def test_the_two_words_are_read_off_ink_and_nothing_else() -> None:
    """Written or not written, and nothing between. A reading the model could not make is
    neither: it stops the afternoon rather than closing it on a page that was filled in."""
    assert came_back(_reading(marks=False)) is Came.BLANK
    assert came_back(_reading(marks=True)) is Came.MARKS
    assert came_back(_reading(marks=True, degraded=True)) is None


def test_a_page_that_is_not_the_one_handed_over_is_still_read(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`ideas/10 §3`: somebody putting back an earlier sheet has not erred, and there is
    nothing here that may refuse a person's paper. The afternoon goes on from what is on it."""
    not_the_one = WhatCameBack(
        written=True, same_sheet=False, describes=("una casa",), read_at=0.0
    )

    assert came_back(not_the_one) is Came.MARKS


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
        # The house also files what it played, on a route of its own. This test is about
        # the ask, so the filing is answered and not looked at.
        if request.full_url.endswith("/experience"):
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
    assert asked["body"]["reading"]["written"] is True
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
        "devices.hands.show", lambda _h, heading, _lines: said.append(heading)
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
    sheet_id = glass(monkeypatch, house, marks=True)
    (house.sheets_dir / "afternoons" / "pages" / f"{sheet_id}.json").unlink()

    with pytest.raises(CannotRun, match="does not belong to an afternoon"):
        carry_on(house, now=1.0, send=False)
