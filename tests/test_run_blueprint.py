"""Which display a run writes to.

One thing is checked here, because it is the one that went wrong. The sheet's notice used
to land wherever the caller said, and on 19 August 2026 the notes in this repository had
the two displays the wrong way round — so the correct argument was the opposite of the
obvious one, and nothing in the code could tell.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from devices.inventory import save_jobs
from devices.run_blueprint import _replace, screen_in, sheet_file

THE_HOUSE = [
    {"id": "94:A9:90:CF:7D:04", "label": "CF7D04", "job": "sheet"},
    {"id": "E8:3D:C1:FB:9F:18", "label": "FB9F18", "job": "picture"},
]


def test_the_notice_goes_to_the_display_that_holds_the_sheet(tmp_path: Path) -> None:
    shared = tmp_path / "screen.bmp"
    jobs = tmp_path / "jobs.json"
    save_jobs(jobs, THE_HOUSE)

    assert sheet_file(shared, jobs) == shared.with_name("screen-CF7D04.bmp")


def test_with_nobody_holding_the_sheet_the_notice_goes_where_it_always_did(
    tmp_path: Path,
) -> None:
    """An unreachable panel leaves the house working to what it knew, not stopped."""
    shared = tmp_path / "screen.bmp"
    assert sheet_file(shared, tmp_path / "absent.json") == shared

    jobs = tmp_path / "jobs.json"
    save_jobs(jobs, [{"id": "94:A9:90:CF:7D:04", "label": "CF7D04", "job": ""}])
    assert sheet_file(shared, jobs) == shared


def test_the_environment_is_read_the_way_the_picture_path_reads_it(tmp_path: Path) -> None:
    shared = tmp_path / "screen.bmp"
    jobs = tmp_path / "jobs.json"
    save_jobs(jobs, THE_HOUSE)

    resolved = screen_in({"TRMNL_SCREEN_FILE": str(shared), "LANTERNINA_JOBS_FILE": str(jobs)})

    assert resolved == shared.with_name("screen-CF7D04.bmp")
    # jobs.json sits beside the screen when nothing says otherwise, as it does on the hub.
    assert screen_in({"TRMNL_SCREEN_FILE": str(shared)}) == shared.with_name("screen-CF7D04.bmp")


def test_a_house_with_no_display_named_has_no_display(tmp_path: Path) -> None:
    """None is what `House` reads as "there is no display here", and it must survive the
    move from an argument to the environment."""
    assert screen_in({}) is None


@pytest.mark.skipif(os.name == "nt", reason="group permissions are a POSIX thing")
def test_a_screen_written_for_the_first_time_stays_writable_by_the_group(
    tmp_path: Path,
) -> None:
    """The defect of 19 August 2026. A run under sudo created `screen-CF7D04.bmp` as
    root:root; the display server could read it and the button path could not write it, so
    pressing the button on that display stopped changing anything."""
    fresh = tmp_path / "screen-CF7D04.bmp"

    _replace(fresh, b"BM-not-really")

    assert stat.S_IMODE(fresh.stat().st_mode) & stat.S_IWGRP


@pytest.mark.skipif(os.name == "nt", reason="group permissions are a POSIX thing")
def test_a_screen_that_already_exists_keeps_the_mode_it_had(tmp_path: Path) -> None:
    """Widening a file somebody already set is not this function's business."""
    existing = tmp_path / "screen.bmp"
    existing.write_bytes(b"old")
    existing.chmod(0o600)

    _replace(existing, b"new")

    assert stat.S_IMODE(existing.stat().st_mode) == 0o600
    assert existing.read_bytes() == b"new"
