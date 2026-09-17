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
    run_experience._write(tmp_path / "sheets" / "activity-rhythm.json", {
        "afternoonDays": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        "afternoonFrom": "00:00", "afternoonUntil": "23:59", "timeZone": "UTC",
    })
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


def test_current_snapshot_follows_waiting_ending_and_removed_runs(house: House) -> None:
    from dataclasses import replace

    experience = an_experience()
    moment = next(one for one in experience.moments if str(one.act) == "collect")
    run = Afternoon("aft_live", experience, 100, moment.id, waited_since=120, over_at=2000)
    path = house.sheets_dir / "afternoons" / "aft_live.json"
    run_experience._write(path, run.to_dict())
    current = run_experience.current_runs(house.sheets_dir)
    assert current == [{
        "runId": "aft_live", "title": experience.title, "beganAt": 100,
        "experienceId": str(experience.experience_id),
        "endsAt": 0, "momentId": moment.id, "heading": moment.heading,
        "phase": "waiting", "waitingSince": 120,
        "receivedAt": 0,
    }]
    run_experience._write(path, replace(run, leaving_at=moment.id, left_at=400).to_dict())
    assert run_experience.current_runs(house.sheets_dir)[0]["phase"] == "ending"
    assert run_experience.current_runs(house.sheets_dir)[0]["waitingSince"] == 400
    path.unlink()
    assert run_experience.current_runs(house.sheets_dir) == []
    path.write_text("broken", encoding="utf-8")
    assert run_experience.current_runs(house.sheets_dir)[0]["phase"] == "unreadable"


def test_current_report_sends_empty_state_and_tolerates_an_unreachable_panel(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    import urllib.error
    from contextlib import nullcontext

    sent = []

    def post(request, timeout):
        sent.append(request)
        assert timeout == run_experience.FILE_TIMEOUT_SECONDS
        return nullcontext()

    monkeypatch.setattr(run_experience.urllib.request, "urlopen", post)
    run_experience.report_current(house)
    assert len(sent) == 1
    assert sent[0].full_url == "https://panel.example/api/device/hh_1/trail-current"
    assert json.loads(sent[0].data) == {"runs": []}
    assert sent[0].get_header("X-device-key") == "k"

    def offline(*args, **kwargs):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(run_experience.urllib.request, "urlopen", offline)
    run_experience.report_current(house)


def test_camera_advances_the_activity_without_touching_the_scanner(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tests.test_photo_store import jpeg

    begin(house, an_experience(), now=0.0, send=False)
    target = run_experience.camera_target(house.sheets_dir, 1.0)
    assert target is not None
    original = recall(house.sheets_dir, last_sheet(house))
    monkeypatch.setattr(run_experience, "_read", lambda *_: pytest.fail("scanner called"))
    seen = []
    monkeypatch.setattr(
        run_experience, "read_page",
        lambda blank, image, **kwargs: seen.append((image.shape, kwargs, blank))
        or _reading(marks=False),
    )
    result = carry_on(house, now=2.0, send=False, photograph=jpeg(), target=target)
    assert seen[0][0] == (48, 64, 3)
    assert "Camera return" in seen[0][1]["about"]
    assert seen[0][1]["photograph"] is True
    assert seen[0][2] is not None
    assert seen[0][2].shape == original.shape
    assert (seen[0][2] == original).all()
    assert result == "the afternoon is finished"


def test_old_or_undated_photo_does_not_advance_a_new_moment(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    begin(house, an_experience(), now=100.0, send=False)
    assert run_experience.camera_target(house.sheets_dir, None) is None
    assert run_experience.camera_target(house.sheets_dir, 99.0) is None
    monkeypatch.setattr(run_experience, "read_page", lambda *_args, **_kw: pytest.fail("read"))
    result = carry_on(house, now=101.0, photograph=b"old", target={
        "run": "previous", "moment": "previous", "since": 99.0,
    })
    assert "archived" in result


def test_explicit_photo_target_advances_only_that_activity(house, monkeypatch):
    from tests.test_photo_store import jpeg

    begin(house, an_experience(), run_id="aft_first", now=100, send=False)
    with pytest.raises(CannotRun, match="open-activity limit"):
        begin(house, an_experience(), now=101, send=False)
    begin(house, an_experience(), run_id="aft_second", now=101, send=False, max_open=2)
    first_path = run_experience._run_file(house.sheets_dir, "aft_first")
    first_bytes = first_path.read_bytes()
    targets = run_experience.camera_target(house.sheets_dir, 102)
    assert len(targets["candidates"]) == 2
    selected = next(target for target in targets["candidates"] if target["run"] == "aft_second")
    seen = []
    monkeypatch.setattr(run_experience, "read_page", lambda *args, **kw:
                        seen.append(kw) or _reading(marks=False))
    monkeypatch.setattr(run_experience, "_read", lambda *_: pytest.fail("scanner called"))
    assert "several activities" in carry_on(house, now=102, send=False)
    assert carry_on(house, now=103, send=False, photograph=jpeg(), target=selected) == (
        "the afternoon is finished"
    )
    assert first_path.read_bytes() == first_bytes
    assert run_experience.waiting_runs(house.sheets_dir) == ["aft_first"]
    assert "archived" in carry_on(house, now=104, photograph=jpeg(), target=selected)
    assert len(seen) == 1


def test_scanner_does_not_read_outside_activity_hours(house, monkeypatch):
    run_experience._write(house.sheets_dir / "activity-rhythm.json", {
        "afternoonDays": [], "afternoonFrom": "15:00", "afternoonUntil": "19:00",
    })
    monkeypatch.setattr(run_experience, "_read", lambda *_: pytest.fail("scanner called"))
    assert carry_on(house, now=100) == "the scanner is waiting for activity hours"


def test_unreadable_activity_remains_open_until_explicit_termination(house):
    from shared.message import Message, Says

    path = run_experience._run_file(house.sheets_dir, "aft_broken")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("broken", encoding="utf-8")
    assert run_experience.conclude_what_is_over(house, 86400, send=False) == []
    assert run_experience.waiting_runs(house.sheets_dir) == ["aft_broken"]
    run_experience.hear(house, [Message(Says.TERMINATE, 86400, run_id="aft_broken")], 86400)
    assert run_experience.waiting_runs(house.sheets_dir) == []


def test_camera_only_activity_needs_no_printer_or_scanner(house, monkeypatch):
    from dataclasses import replace

    from shared.capabilities import HouseCapability
    from tests.test_photo_store import jpeg

    experience = Experience.from_dict(a.an_afternoon(
        requires=["photograph_table", "show_800x480_1bit"],
        moments=[a.say(), a.collect(source="camera"), a.close()],
    ))
    camera_house = replace(house, scanner="", printer="", camera=True)
    assert HouseCapability.PHOTOGRAPH_TABLE in camera_house.capabilities
    begin(camera_house, experience, now=100, send=False)
    target = run_experience.camera_target(house.sheets_dir, 101)
    monkeypatch.setattr(run_experience, "read_page", lambda *args, **kw: _reading(
        marks=True, degraded=True,
    ))
    assert "not clear enough" in carry_on(
        camera_house, now=102, photograph=jpeg(), target=target, send=False,
    )
    assert run_experience.camera_target(house.sheets_dir, 101) == target
    monkeypatch.setattr(run_experience, "read_page", lambda *args, **kw: _reading(marks=True))
    assert carry_on(camera_house, now=103, photograph=jpeg(), target=target,
                    send=False) == "the afternoon is finished"


def test_return_choice_is_named_saved_and_kept_through_help(house, monkeypatch):
    from devices.inventory import save_jobs

    jobs = house.sheets_dir.parent / "jobs.json"
    monkeypatch.setenv("LANTERNINA_JOBS_FILE", str(jobs))
    save_jobs(jobs, [
        {"id": "CAM-A", "kind": "camera", "name": "Rossa", "jobs": ["scan"]},
        {"id": "CAM-B", "kind": "camera", "name": "Verde", "jobs": ["scan"]},
        {"id": "scanner", "kind": "scanner", "jobs": ["scan"], "model": "glass"},
    ])
    monkeypatch.setattr("devices.inventory.random.choice", lambda candidates: candidates[1])
    shown = []
    monkeypatch.setattr(
        "devices.hands.say", lambda _house, heading, lines, **kw: shown.append(lines),
    )
    begin(house, an_experience(), now=100, send=False)
    run = Afternoon.from_dict(json.loads(runs(house)[0].read_text()))
    assert run.return_device["id"] == "CAM-B"
    assert shown[-1][-1] == "Verde"
    assert "fotografa" in shown[-1][-2]
    previous = run.moments[run_experience._index_of(run, run.waiting_at) - 1]
    assert shown[-1][:-2] == list(previous.at(run.weight).lines)
    assert run_experience.camera_target(house.sheets_dir, 101, "CAM-A") is None
    assert run_experience.camera_target(house.sheets_dir, 101, "CAM-B") is not None
    assert run_experience._one_rung_on(run).return_device == run.return_device
    assert run_experience._over_at(run, 2000).return_device == run.return_device
    monkeypatch.setattr(run_experience, "_read", lambda *_: pytest.fail("scanner called"))
    assert carry_on(house, now=102) == "the afternoon is waiting for a photograph"


def test_selected_scanner_is_the_one_read(house, monkeypatch):
    from devices.inventory import save_jobs

    jobs = house.sheets_dir.parent / "jobs.json"
    monkeypatch.setenv("LANTERNINA_JOBS_FILE", str(jobs))
    save_jobs(jobs, [
        {"id": "scanner-a", "kind": "scanner", "jobs": ["scan", "return"],
         "model": "first"},
        {"id": "scanner-b", "kind": "scanner", "jobs": ["scan", "return"],
         "model": "second"},
    ])
    monkeypatch.setattr("devices.inventory.random.choice", lambda candidates: candidates[-1])
    begin(house, an_experience(), now=100, send=False)
    assert run_experience.camera_target(house.sheets_dir, 101, "CAM-A") is None
    seen = []
    monkeypatch.setattr(run_experience, "_read", lambda selected: (
        seen.append(selected.scanner) or str(last_sheet(house)), _reading(marks=False)
    ))
    assert carry_on(house, now=102, send=False) == "the afternoon is finished"
    assert seen == ["second"]


def test_camera_assigned_to_read_paper_can_run_without_scanner(house, monkeypatch):
    from dataclasses import replace

    from devices.inventory import save_jobs
    from tests.test_photo_store import jpeg

    jobs = house.sheets_dir.parent / "jobs.json"
    monkeypatch.setenv("LANTERNINA_JOBS_FILE", str(jobs))
    save_jobs(jobs, [
        {"id": "CAM", "kind": "camera", "jobs": ["scan", "return"], "name": "Verde"},
    ])
    camera_house = replace(house, scanner="", camera=True)
    begin(camera_house, an_experience(), now=100, send=False)
    target = run_experience.camera_target(house.sheets_dir, 101, "CAM")
    assert target is not None
    seen = []
    monkeypatch.setattr(run_experience, "read_page", lambda blank, image, **kwargs: (
        seen.append(blank) or _reading(marks=False)
    ))
    assert carry_on(camera_house, now=102, photograph=jpeg(), target=target,
                    send=False) == "the afternoon is finished"
    assert seen[0] is not None


def test_return_instruction_uses_the_parent_language_and_unassigned_means_disabled(
    house, monkeypatch,
):
    from devices.inventory import save_jobs
    from shared.capabilities import HouseCapability

    jobs = house.sheets_dir.parent / "jobs.json"
    monkeypatch.setenv("LANTERNINA_JOBS_FILE", str(jobs))
    save_jobs(jobs, [
        {"id": "CAM", "kind": "camera", "jobs": ["return", "scan"], "name": "Green"},
    ], language="en")
    begin(house, an_experience(), now=100, send=False)
    run = Afternoon.from_dict(json.loads(runs(house)[0].read_text()))
    assert run_experience._return_lines(run) == [
        "When finished, photograph the work with:", "Green",
    ]
    save_jobs(jobs, [{"id": "CAM", "kind": "camera", "jobs": []}])
    assert HouseCapability.PHOTOGRAPH_TABLE not in house.capabilities
    assert HouseCapability.SCAN_A4 not in house.capabilities
    assert run.return_device["id"] == "CAM"


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


def test_a_page_can_resume_an_open_activity_three_days_later(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    from devices.run_experience import camera_target, conclude_what_is_over

    said: list[str] = []
    monkeypatch.setattr(
        "devices.hands.show", lambda _h, heading, _lines: said.append(heading)
    )
    experience = an_experience()
    begin(house, experience, now=0.0, send=False)
    glass(monkeypatch, house, marks=True)

    when = 3 * 24 * 60 * 60
    assert conclude_what_is_over(house, when, send=False) == []
    assert len(runs(house)) == 1
    assert camera_target(house.sheets_dir, when) is not None
    told = carry_on(house, now=when, send=False)

    assert told == "waiting for a page at l-ultimo-foglio"
    resumed = Afternoon.from_dict(json.loads(runs(house)[0].read_text(encoding="utf-8")))
    assert resumed.waiting_at == "l-ultimo-foglio"
    assert resumed.answered == ("come-e-tornato:marks",)


def test_a_page_from_no_afternoon_is_refused(
    house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    begin(house, an_experience(), now=0.0, send=False)
    sheet_id = glass(monkeypatch, house, marks=True)
    (house.sheets_dir / "afternoons" / "pages" / f"{sheet_id}.json").unlink()

    with pytest.raises(CannotRun, match="does not belong to an afternoon"):
        carry_on(house, now=1.0, send=False)
