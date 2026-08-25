"""A house with nobody in it: what stays real, and what must never leak out of the folder.

The reading is stood in for here and only here, because it is the one call that leaves the
machine — `tests/test_run_experience.py` replaces the scanner, and this replaces the panel.
Everything between the two is the real thing: the page is composed, rasterised, its markers
are found, it is rectified, its QR is decoded and the ink drawn by hand is in it. That is
the part worth testing, because it is the part a simulator usually throws away.

Two of these are not about the simulator working. `test_a_pretend_house_writes_nothing_
outside_its_own_folder` is the guarantee the whole design rests on, and the transcript test
is the one that would notice a field about a person growing in a file that outlives the
afternoon.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from devices import pretend as simulated
from devices.house import House, hand_over, show
from devices.pretend import Pretend
from devices.print_page import recall
from devices.run_experience import begin, carry_on, conclude_what_is_over, waiting_runs
from shared.experience import Experience
from shared.ids import SheetId
from shared.vision_contracts import WhatCameBack

THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")


@pytest.fixture
def where(tmp_path: Path) -> Path:
    return tmp_path / "pretend"


@pytest.fixture
def house(where: Path) -> House:
    return House(
        sheets_dir=where / "state",
        panel="https://panel.example",
        household="hh_1",
        device_key="k",
        pretend=where,
    )


def an_experience() -> Experience:
    return Experience.from_dict(json.loads(THE_AFTERNOON.read_text(encoding="utf-8")))


def the_cloud(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    """Stand in for the panel, and keep the page the reader was handed.

    What is asserted about it is that the ink drawn by hand is in it, which is the only way
    to know that the page a person "wrote on" is the page the model would see.
    """
    seen: list[Any] = []

    def _draw(page: Any, **_: Any) -> Any:
        # A page a model would have drawn, stood in for by white paper: what is being
        # exercised here is the house, and a model call would measure the model.
        return np.full((1536, 1024), 255, dtype=np.uint8)

    def _read(blank: Any, came_back: Any, **_: Any) -> WhatCameBack:
        seen.append(came_back)
        written = bool((came_back < 90).any())
        return WhatCameBack(
            written=written,
            same_sheet=True,
            describes=("un segno sul foglio",) if written else (),
            read_at=0.0,
        )

    monkeypatch.setattr("devices.hands.draw_page", _draw)
    monkeypatch.setattr("devices.run_experience.read_page", _read)
    return seen


def _has_ink(page: Any) -> bool:
    """Whether anything darker than print-grey is on the sheet at all.

    No inset and no rectangle, because there are no declared places left to inset from. The
    old version of this needed one: the printed border of a box sat exactly on the cell
    rectangle, so a patch taken at the rectangle had a black frame around it and every place
    read as written in. That defect went to the attic with the boxes.
    """
    return bool((page < 90).any())


# ── The guarantee the design rests on ────────────────────────────────────────────────


def test_a_pretend_house_writes_nothing_outside_its_own_folder(
    where: Path, house: House, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Not a check that could be forgotten: the real paths are never built.

    A pretend house has no printer name, no scanner name and no screen file, so there is
    nothing for a misconfigured run to write to. This asserts the consequence, which is the
    thing that would actually be noticed if the branch moved.
    """
    elsewhere = tmp_path / "not-the-folder"
    elsewhere.mkdir()
    the_cloud(monkeypatch)

    begin(house, an_experience(), now=0.0, send=False)

    assert house.printer == "" and house.scanner == "" and house.screen is None
    assert list(elsewhere.iterdir()) == []
    written = {path for path in tmp_path.rglob("*") if path.is_file()}
    assert written, "it did something"
    assert all(where in path.parents for path in written)


def test_a_pretend_house_can_run_an_afternoon_a_real_one_could(house: House) -> None:
    """The capabilities are the three, so an experience is not skipped for want of paper."""
    assert an_experience().runnable_in(house.capabilities)


# ── What is real ─────────────────────────────────────────────────────────────────────


def test_the_sheet_on_the_glass_is_the_sheet_that_was_handed_over(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The page is drawn, put on A4, written to a PDF and rasterised, and the raster is what
    is laid on the glass. None of that is stood in for: a simulator that handed the runner a
    page object directly would never notice a sheet that comes out at the wrong size.
    """
    the_cloud(monkeypatch)
    begin(house, an_experience(), now=0.0, send=False)
    pretend = Pretend(where)
    sheet_id = simulated.sheets_on_the_table(pretend)[-1]

    simulated.put_on_the_glass(pretend, sheet_id, [])
    came_from, page = simulated.off_the_glass(pretend, house)

    assert came_from == sheet_id
    assert page.shape == recall(house.sheets_dir, SheetId(sheet_id)).shape
    assert not pretend.glass.is_file(), "the sheet leaves the glass when it is read"


def test_ink_drawn_by_hand_is_in_the_page_the_reader_is_given(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The injected half, and the only injected half: where the marks are."""
    seen = the_cloud(monkeypatch)
    begin(house, an_experience(), now=0.0, send=False)
    pretend = Pretend(where)
    sheet_id = simulated.sheets_on_the_table(pretend)[-1]

    simulated.put_on_the_glass(pretend, sheet_id, ["middle"])
    carry_on(house, now=60.0, send=False)

    assert _has_ink(seen[-1]), "the ink is on the page the reader was handed"


def test_a_sheet_laid_back_untouched_reads_as_nothing(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Stopping is a legitimate outcome, and it has to be reachable without paper."""
    seen = the_cloud(monkeypatch)
    begin(house, an_experience(), now=0.0, send=False)
    pretend = Pretend(where)
    sheet_id = simulated.sheets_on_the_table(pretend)[-1]

    simulated.put_on_the_glass(pretend, sheet_id, [])
    carry_on(house, now=60.0, send=False)

    assert not _has_ink(seen[-1])


def test_the_display_shows_the_pixels_the_real_display_would(where: Path, house: House) -> None:
    """Same renderer, so text that wraps badly wraps badly here."""
    from devices.epaper import render_notice_png

    show(house, "Guarda fuori", ["Fra poco esce un foglio."])

    drawn = (Pretend(where).display / "latest.png").read_bytes()
    assert drawn == render_notice_png("Guarda fuori", ["Fra poco esce un foglio."])


def test_the_pdf_on_the_table_is_the_one_the_printer_would_have_had(
    where: Path, house: House
) -> None:
    drawn = np.full((1536, 1024), 255, dtype=np.uint8)

    hand_over(house, drawn, sheet_id=SheetId("sh_test"))

    on_the_table = Pretend(where).paper / "sh_test.pdf"
    assert on_the_table.read_bytes().startswith(b"%PDF")
    assert (Pretend(where).paper / "sh_test.png").is_file(), "and the page itself"


# ── An afternoon, from beginning to ending, with nobody in the room ──────────────────


def test_a_whole_afternoon_runs_to_its_close(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A page with marks takes the written branch; a blank one closes it kindly."""
    the_cloud(monkeypatch)
    experience = an_experience()
    begin(house, experience, now=0.0, send=False)
    pretend = Pretend(where)

    first = simulated.sheets_on_the_table(pretend)[-1]
    simulated.put_on_the_glass(pretend, first, ["middle"])
    assert carry_on(house, now=60.0, send=False) == "waiting for a page at l-ultimo-foglio"

    second = simulated.sheets_on_the_table(pretend)[-1]
    assert second != first
    simulated.put_on_the_glass(pretend, second, [])
    assert carry_on(house, now=120.0, send=False) == "the afternoon is finished"
    assert waiting_runs(house.sheets_dir) == []


def test_the_ending_arrives_when_the_clock_is_moved_past_it(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Three hours in two commands, which is the reason the clock can be moved at all."""
    the_cloud(monkeypatch)
    experience = an_experience()
    begin(house, experience, now=simulated.the_time(Pretend(where)), send=False)
    pretend = Pretend(where)

    simulated.move_on(pretend, (experience.minutes - 20) * 60.0)
    assert conclude_what_is_over(house, simulated.the_time(pretend), send=False) == []
    said = [line for line in simulated.read_transcript(pretend) if line["what"] == "display"]
    assert said[-1]["heading"] == experience.moment("come-e-tornato").way_out.heading

    simulated.move_on(pretend, 20 * 60.0)
    assert len(conclude_what_is_over(house, simulated.the_time(pretend), send=False)) == 1
    said = [line for line in simulated.read_transcript(pretend) if line["what"] == "display"]
    assert said[-1]["heading"] == experience.moment("basta-cosi").heading
    assert waiting_runs(house.sheets_dir) == []


# ── The transcript, and the line it must not cross ───────────────────────────────────


def test_the_transcript_records_what_the_house_did(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    the_cloud(monkeypatch)
    begin(house, an_experience(), now=0.0, send=False)
    pretend = Pretend(where)
    sheet_id = simulated.sheets_on_the_table(pretend)[-1]
    simulated.put_on_the_glass(pretend, sheet_id, [])
    simulated.off_the_glass(pretend, house)

    what = [line["what"] for line in simulated.read_transcript(pretend)]

    assert what[:3] == ["display", "display", "paper"]
    assert "glass" in what


def test_the_transcript_has_nowhere_to_put_a_verdict_about_a_person(
    where: Path, house: House, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The one file here that outlives the afternoon, so the one that has to be looked at.

    It may hold what happened — this place carries ink, this screen said that. It may not
    hold a claim about who somebody is, and the way to keep that true is that no line ever
    carries a word for one.
    """
    the_cloud(monkeypatch)
    begin(house, an_experience(), now=0.0, send=False)
    pretend = Pretend(where)
    sheet_id = simulated.sheets_on_the_table(pretend)[-1]
    simulated.put_on_the_glass(pretend, sheet_id, [])
    simulated.off_the_glass(pretend, house)

    forbidden = {
        "score",
        "grade",
        "rank",
        "level",
        "ability",
        "readiness",
        "difficulty",
        "correct",
        "wrong",
        "learner",
        "child",
        "name",
        "age",
        "streak",
        "attempts",
    }
    for line in simulated.read_transcript(pretend):
        found = sorted(set(line) & forbidden)
        assert not found, f"{found} in a {line['what']} line"


def test_nothing_is_recorded_when_the_house_is_real(tmp_path: Path) -> None:
    """One flag, not two: the recording is the pretend house, so a real run cannot record.

    A house with equipment has no ``pretend`` directory, and every function that writes a
    transcript takes one. There is no setting that turns recording on for a real afternoon,
    which is what keeps this on the right side of the rule rather than merely off by default.
    """
    real = House(printer="paper", scanner="glass", screen=tmp_path / "s.bmp", sheets_dir=tmp_path)

    assert real.pretend is None
    assert real.pretending is None
