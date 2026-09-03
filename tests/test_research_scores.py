"""The score history: one file built from the run directories, and the route that serves it.

Two things are worth a test rather than a look. Rebuilding from the directories is the
definition of the file, so a run directory that appears must reach it. And the panel must
answer with an empty history rather than an error when the file was not shipped — the
image copies one small file, and a route that fell over without it would take the whole
section with it for a reason nobody could see.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from research.scores import collect, write

PARENT = "parent@example.test"

A_RUN = {
    "at": "2026-08-29T072645Z",
    "prompt": "",
    "iterations": 4,
    "afternoons": 24,
    "refused": 3,
    "endings": {"closed": 0, "way_out": 10, "stopped": 11},
    "axes": {"canBeStarted": 4.57, "sheetStandsAlone": 1.95},
    "minutes": 57.9,
}


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT)
    return TestClient(create_app(store=InMemoryAccountStore(), settings=settings))


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def a_run(runs: Path, name: str, **changes: object) -> None:
    folder = runs / name
    folder.mkdir(parents=True)
    (folder / "summary.json").write_text(
        json.dumps({**A_RUN, **changes}, ensure_ascii=False), encoding="utf-8"
    )


def test_the_history_is_rebuilt_from_the_run_directories(tmp_path: Path) -> None:
    """The directories are the definition. A run that exists and is not in the file is the
    failure this rebuild exists to make impossible."""
    a_run(tmp_path, "2026-08-29T072645Z-prima-corsa")
    a_run(tmp_path, "2026-09-03T090000Z-dopo", prompt="d427131c594e", refused=0)
    # A directory a run never finished writing. Skipped, not raised on.
    (tmp_path / "2026-09-03T100000Z-interrotta").mkdir()

    history = collect(tmp_path)

    assert [row["label"] for row in history] == ["prima-corsa", "dopo"]
    assert [row["prompt"] for row in history] == ["", "d427131c594e"]
    # The households are the same six every time and are left out on purpose.
    assert "households" not in history[0]


def test_writing_the_history_leaves_a_file_that_reads_back(tmp_path: Path) -> None:
    a_run(tmp_path, "2026-08-29T072645Z-prima-corsa")
    to = tmp_path / "scores.json"

    write(tmp_path, to)

    assert json.loads(to.read_text(encoding="utf-8")) == collect(tmp_path)


def test_the_panel_serves_the_history_behind_the_parents_login(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a_run(tmp_path, "2026-09-03T090000Z-dopo", prompt="d427131c594e")
    scores = tmp_path / "scores.json"
    write(tmp_path, scores)
    monkeypatch.setattr("panel.routes.research.HISTORY", scores)
    client = client_for()

    assert client.get("/api/research").status_code != 200

    rows = client.get("/api/research", headers=headers()).json()["runs"]
    assert [row["label"] for row in rows] == ["dopo"]
    assert rows[0]["axes"]["sheetStandsAlone"] == 1.95
    assert rows[0]["afternoons"] == 24


def test_a_panel_shipped_without_the_file_answers_with_no_runs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """One small file is copied into the image. A route that fell over without it would
    take the section down for a reason nobody reading the page could see."""
    monkeypatch.setattr("panel.routes.research.HISTORY", tmp_path / "not-here.json")
    client = client_for()

    answer = client.get("/api/research", headers=headers())

    assert answer.status_code == 200
    assert answer.json() == {"runs": []}
