"""The score history: one file built from the run directories.

Rebuilding from the directories is the definition of the file, so a run directory that
appears must reach it. Nothing here is served to anybody: the reader is
`python -m research.reader`, which is a developer's tool and not part of the product.
"""

from __future__ import annotations

import json
from pathlib import Path

from research.scores import collect, write

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
