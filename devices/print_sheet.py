"""Print an approved exercise, and remember the sheet so it can be read back.

The remembering is the point. A sheet can come back an hour later or on Thursday, and the
reader has to know where the boxes were; the QR on the page carries an id and nothing else,
so the spec has to be somewhere on the hub when the page returns. Without this the printed
sheet is a picture of an exercise rather than a thing that closes a loop.

Nothing here decides content. The design came from somewhere that was approved; this
composes it, measures its ink and hands the result to CUPS.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from printing.render import drawing_to_pdf
from shared.ids import ExerciseId, SheetId
from shared.pagedesign import PageDesign
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


def compose_sheet(
    design: PageDesign,
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
    exercise_id: ExerciseId,
    now: float = 0.0,
) -> tuple[Any, bytes]:
    """Compose a designed page, remember it, and return the sheet and its PDF.

    Split out on 24 August 2026 so a house with no printer can be handed the same bytes
    `lp` would have been handed, and can also raster the very same ``Drawing``. Remembering
    the spec belongs on this side of the split: a page that comes back is found by its id,
    and whether it went to a printer or to a folder does not change that.

    ``printing.compose`` is imported here rather than at the top because it pulls in OpenCV
    to measure the ink, and every other function in this module runs without it.
    """
    from printing.compose import compose

    sheet = compose(design, sheet_id=sheet_id, exercise_id=exercise_id, created_at=now)
    remember(sheets_dir, sheet.spec)
    return sheet, drawing_to_pdf(sheet.drawing)


def compose_and_print(
    design: PageDesign,
    *,
    sheets_dir: Path,
    sheet_id: SheetId,
    exercise_id: ExerciseId,
    printer: str,
    now: float = 0.0,
    send: bool = True,
) -> SheetSpec:
    """Compose a designed page, remember it, and put it on paper.

    What is remembered is a ``SheetSpec``, so a page that comes back on Thursday is found
    and read exactly as it was before a model designed anything.
    """
    sheet, pdf = compose_sheet(
        design,
        sheets_dir=sheets_dir,
        sheet_id=sheet_id,
        exercise_id=exercise_id,
        now=now,
    )
    if send:
        subprocess.run(
            ["lp", "-d", printer, *PRINT_OPTIONS, "-t", f"lanternina-{sheet_id}", "-"],
            input=pdf,
            check=True,
        )
    spec: SheetSpec = sheet.spec
    return spec
