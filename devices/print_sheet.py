"""Print an approved exercise, and remember the sheet so it can be read back.

The remembering is the point. A sheet can come back an hour later or on Thursday, and the
reader has to know where the boxes were; the QR on the page carries an id and nothing else,
so the spec has to be somewhere on the hub when the page returns. Without this the printed
sheet is a picture of an exercise rather than a thing that closes a loop.

Nothing here decides content. The words came from the content agent and were approved as
words; this chooses where they land and hands the result to CUPS.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from printing.layout import sheet_for
from printing.render import PageGeometry, build_drawing, drawing_to_pdf
from shared.ids import ExerciseId, SheetId
from shared.sheet import SheetSpec

# CUPS scales to fit by default, and a sheet scaled to fit is a sheet whose every cell is
# in the wrong place while still looking right.
PRINT_OPTIONS = ("-o", "media=A4", "-o", "print-scaling=none", "-o", "sides=one-sided")


def remember(directory: Path, spec: SheetSpec) -> Path:
    """Store the spec under its own id, which is what the QR code will hand back."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{spec.sheet_id}.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(spec.to_dict(), indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def recall(directory: Path, sheet_id: SheetId) -> SheetSpec:
    """The spec for a sheet that has come back. Missing is an error, not an empty page."""
    path = directory / f"{sheet_id}.json"
    return SheetSpec.from_dict(json.loads(path.read_text(encoding="utf-8")))


def lay_out_and_print(
    body: Mapping[str, Any],
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
    exercise_id: ExerciseId,
    printer: str,
    now: float = 0.0,
    send: bool = True,
) -> SheetSpec:
    """Lay the exercise out, remember it, and put it on paper."""
    spec = sheet_for(body, sheet_id=sheet_id, exercise_id=exercise_id, created_at=now)
    pdf = drawing_to_pdf(build_drawing(spec, PageGeometry()))
    remember(sheets_dir, spec)
    if send:
        subprocess.run(
            ["lp", "-d", printer, *PRINT_OPTIONS, "-t", f"lanternina-{sheet_id}", "-"],
            input=pdf,
            check=True,
        )
    return spec
