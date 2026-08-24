"""The house without the person: everything real except the hand that fills the sheet.

This is not a mock of the system. It is the system, with one thing missing — somebody in
the room. What that person does is four things, and all four are what this module injects:
they look at the display, they take the sheet off the printer, they put marks on it and lay
it on the glass, and they let time pass.

**What is real when this is on**, and it is nearly everything:

* the devising model, the checks and the repair loop, against the same Foundry deployment
  the hub reaches;
* the page, composed by ``printing.compose``, laid out by the same renderer and rasterised
  from the same ``Drawing`` the PDF comes from — markers, quiet zones, QR and all;
* marker detection, rectification and QR decoding, on that raster;
* **the reading of the page, by the vision model in the cloud**, over the same device-key
  route the hub uses;
* the safety gate, the outgoing filter, the runner, the graph, the ending at T-30.

**What is not real**: paper, a printer queue, a scanner, a display on a wall, and a person.
The ink on the page is drawn by :func:`_by_hand` where somebody would have drawn it, and
the display is a PNG rather than a panel that has to wake up. So this exercises everything
above the hardware and nothing of the hardware, which is exactly the division it is for:
whether the toner is in and the scanner answers is checked by standing in the room, and
whether the afternoon reads well is checked here.

**Where the switch lives.** :class:`~devices.house.House` carries a ``pretend`` directory,
or does not. Nothing above the house knows: the runner has no branch on it, because the
moment a runner can tell the difference the two have stopped being one system. Every path a
pretend house writes is inside that directory, so a misconfigured pretend run cannot touch a
real display — not because something checks, but because the real paths are never built.

**Why the recording is allowed here and would not be allowed in a house.** The working rules
say nothing the system keeps may be a record about a person, and `ideas/09 §6` draws the line
at what is happening now, discarded when the afternoon ends. A transcript of an afternoon on
disk is exactly a durable record of what somebody did. It is written here because the person
on the other side is whoever typed the commands, and it is bound to the simulation rather
than being a setting of its own: there is no way to record a real run, because the recording
belongs to the pretend house and a pretend house has no printer. One flag, not two.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.ids import SheetId
from shared.sheet import RECTIFIED_HEIGHT, RECTIFIED_WIDTH, CellKind, CellSpec, SheetSpec
from shared.vision_contracts import PageReading

if TYPE_CHECKING:
    from devices.house import House

PRETEND_DIR_ENV: Final = "LANTERNINA_PRETEND_DIR"

# The raster the page is kept as. The same 300 dpi the real scanner is configured for, so
# the markers land on the same number of pixels — 176 to 178 px on real paper, measured
# 4 August 2026, against 177.2 computed for 15 mm.
PAGE_DPI: Final = 300

# What a hand can be told to do, beyond naming the places one by one.
NOTHING: Final = "blank"
SOMETHING: Final = "marks"
EVERYTHING: Final = "all"


def pretend_in(env: Mapping[str, str]) -> Path | None:
    """The directory a simulated house writes into, or None for a house with equipment."""
    named = env.get(PRETEND_DIR_ENV, "").strip()
    return Path(named) if named else None


@dataclass(frozen=True, slots=True)
class Pretend:
    """Where a simulated house keeps what it would have done."""

    where: Path

    @property
    def display(self) -> Path:
        return self.where / "display"

    @property
    def paper(self) -> Path:
        return self.where / "paper"

    @property
    def glass(self) -> Path:
        """What has been laid on the scanner and not yet read. Absent means nothing has."""
        return self.where / "glass.json"

    @property
    def transcript(self) -> Path:
        return self.where / "transcript.jsonl"

    @property
    def clock(self) -> Path:
        """How far the afternoon has been moved on by hand.

        A real afternoon reaches its ending after three hours. Waiting three hours to find
        out whether the ending reads well is the reason nobody checks the ending.
        """
        return self.where / "clock.json"


def note(pretend: Pretend, what: str, **fields: Any) -> None:
    """One line of the transcript. It records what the house did, never who did it.

    The vocabulary is the format's own — a heading, a sheet id, which places carry ink.
    There is nothing here that could become a claim about a person, and that is a property
    of the fields rather than a promise about how they are used.
    """
    pretend.where.mkdir(parents=True, exist_ok=True)
    line = json.dumps({"at": time.time(), "what": what, **fields}, ensure_ascii=False)
    with pretend.transcript.open("a", encoding="utf-8") as out:
        out.write(line + "\n")


def read_transcript(pretend: Pretend) -> list[dict[str, Any]]:
    if not pretend.transcript.is_file():
        return []
    lines = pretend.transcript.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


# ── What the person would have looked at ─────────────────────────────────────────────


def show(pretend: Pretend, heading: str, lines: list[str]) -> Path:
    """Draw what the display would have drawn, and keep every screen it drew.

    ``latest.png`` is the display: one thing at a time, overwritten, which is what a screen
    on a wall is. The numbered copies beside it are the afternoon in order, and they are
    what makes this worth having — a change of course that reads badly is visible by looking
    at five files rather than by sitting through three hours.

    The pixels come from the same renderer the real display is fed, so text that wraps
    awkwardly wraps awkwardly here too.
    """
    from devices.epaper import render_notice_png

    pretend.display.mkdir(parents=True, exist_ok=True)
    drawn = render_notice_png(heading, lines)
    seen = len(sorted(pretend.display.glob("[0-9]*.png")))
    numbered = pretend.display / f"{seen + 1:03d}.png"
    numbered.write_bytes(drawn)
    (pretend.display / "latest.png").write_bytes(drawn)
    note(pretend, "display", heading=heading, lines=lines, file=numbered.name)
    return numbered


# ── What the person would have picked up ─────────────────────────────────────────────


def hand_over(pretend: Pretend, spec: SheetSpec, pdf: bytes, page: NDArray[np.uint8]) -> Path:
    """Put a sheet on the table: the PDF the printer would have had, and the page itself.

    Both, because they answer different questions. The PDF is what `lp` would have been
    given and is the thing to open when a layout looks wrong. The raster is the sheet as an
    object — it is what gets marks drawn on it and laid on the glass, so the page that comes
    back is the page that went out, markers and QR included.
    """
    pretend.paper.mkdir(parents=True, exist_ok=True)
    page_pdf = pretend.paper / f"{spec.sheet_id}.pdf"
    page_pdf.write_bytes(pdf)
    cv2.imwrite(str(pretend.paper / f"{spec.sheet_id}.png"), page)
    note(
        pretend,
        "paper",
        sheet_id=str(spec.sheet_id),
        title=spec.title,
        places=[f"{cell.id}: {cell.label}" for cell in spec.cells],
        file=page_pdf.name,
    )
    return page_pdf


def sheets_on_the_table(pretend: Pretend) -> list[str]:
    """Every sheet handed over, oldest first.

    By when it came out and not by its name: two sheets on the table are told apart by which
    one the printer produced last, and a sheet id is a random hex string that sorts however
    it likes. Picking the alphabetically last one gave the second half of an afternoon the
    first half's sheet, which read as a page that had already been read.
    """
    return [
        path.stem
        for path in sorted(pretend.paper.glob("*.pdf"), key=lambda page: page.stat().st_mtime)
    ]


# ── What the person would have written, and laid on the glass ────────────────────────


def which_places(spec: SheetSpec, asked: str) -> tuple[str, ...]:
    """Turn a word into the places that carry ink.

    ``marks`` fills one place and no more. What a branch turns on is whether anything came
    back at all, and filling every box would be inventing an afternoon's worth of work
    nobody did.
    """
    answerable = [str(cell.id) for cell in spec.cells]
    if asked == NOTHING:
        return ()
    if asked == EVERYTHING:
        return tuple(answerable)
    if asked == SOMETHING:
        return tuple(answerable[:1])
    named = tuple(part.strip() for part in asked.split(",") if part.strip())
    unknown = [name for name in named if name not in answerable]
    if unknown:
        raise ValueError(f"this sheet has no place called {unknown}; it has {answerable}")
    return named


def put_on_the_glass(pretend: Pretend, sheet_id: str, filled: Sequence[str]) -> None:
    """Say which sheet is on the scanner and which of its places somebody wrote in."""
    pretend.where.mkdir(parents=True, exist_ok=True)
    pretend.glass.write_text(
        json.dumps({"sheet_id": sheet_id, "filled": list(filled)}) + "\n", encoding="utf-8"
    )


def off_the_glass(pretend: Pretend, house: House) -> tuple[SheetSpec, PageReading]:
    """The page laid on the glass, read by the model that reads real pages.

    Everything from here down is the path the hub takes. The raster of the sheet is
    rectified against its own markers, the QR is decoded to find out which sheet it is, the
    spec is recalled, and the crop goes to the panel where a vision model looks at it. What
    was injected is one thing: where the ink is.

    Raises :class:`LookupError` when nothing was laid on the glass, which is the simulated
    equivalent of pressing the button with an empty scanner.
    """
    from devices.print_sheet import recall
    from devices.read_page import read_page
    from vision.read_sheet import detect_markers, read_qr, rectify

    if not pretend.glass.is_file():
        raise LookupError("nothing is on the glass")
    asked = json.loads(pretend.glass.read_text(encoding="utf-8"))
    filled = [str(name) for name in asked.get("filled", [])]

    page = _page_image(pretend, str(asked["sheet_id"]))
    rectified = rectify(page, detect_markers(page))
    spec = recall(house.sheets_dir, SheetId(read_qr(rectified).sheet_id))
    _by_hand(rectified, spec, filled)
    reading = read_page(
        rectified,
        spec,
        panel=house.panel,
        household=house.household,
        key=house.device_key,
    )
    # The sheet leaves the glass when it is read, exactly as a person picks it back up.
    pretend.glass.unlink(missing_ok=True)
    note(
        pretend,
        "glass",
        sheet_id=str(spec.sheet_id),
        filled=filled,
        read=[
            {"place": str(cell.cell_id), "ink": bool(cell.value), "sure": str(cell.confidence)}
            for cell in reading.cells
        ],
    )
    return spec, reading


def _page_image(pretend: Pretend, sheet_id: str) -> NDArray[np.uint8]:
    path = pretend.paper / f"{sheet_id}.png"
    if not path.is_file():
        raise LookupError(f"there is no sheet {sheet_id!r} on the table")
    page = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if page is None:
        raise LookupError(f"the sheet {sheet_id!r} on the table is not an image")
    return np.asarray(page, dtype=np.uint8)


# Where a hand goes inside a place, as fractions of it. Three shapes rather than one,
# because a tick, a word and a drawing do not look alike and a reader that only recognises
# one of them should fail here rather than in the house.
_TICK: Final = ((0.25, 0.55), (0.45, 0.80), (0.80, 0.20))
_WORD: Final = ((0.05, 0.70), (0.15, 0.30), (0.25, 0.70), (0.35, 0.35), (0.45, 0.70))
_DRAWING: Final = ((0.20, 0.80), (0.35, 0.25), (0.50, 0.75), (0.65, 0.20), (0.80, 0.70))


def _by_hand(rectified: NDArray[np.uint8], spec: SheetSpec, filled: Sequence[str]) -> None:
    """Draw ink where somebody would have drawn it, in place, on the rectified page.

    After rectification rather than before, because after it the sheet's own coordinates are
    the image's coordinates and no mapping has to be reinvented here. What it costs is that
    the ink does not go through the perspective transform, which for a sheet lying flat under
    a lid is a transform that does nothing anyway.
    """
    places = {str(cell.id): cell for cell in spec.cells}
    for name in filled:
        cell = places.get(name)
        if cell is None:
            continue
        if cell.kind in (CellKind.CHECKBOX, CellKind.CHOICE_BOX):
            _stroke(rectified, cell, _TICK)
        elif cell.kind is CellKind.WORD_LINE:
            _stroke(rectified, cell, _WORD)
        else:
            _stroke(rectified, cell, _DRAWING)


def _stroke(
    rectified: NDArray[np.uint8], cell: CellSpec, path: Sequence[tuple[float, float]]
) -> None:
    points = [
        (
            round((cell.rect.x + across * cell.rect.w) * RECTIFIED_WIDTH),
            round((cell.rect.y + down * cell.rect.h) * RECTIFIED_HEIGHT),
        )
        for across, down in path
    ]
    across_px = cell.rect.w * RECTIFIED_WIDTH
    down_px = cell.rect.h * RECTIFIED_HEIGHT
    cv2.polylines(
        rectified,
        [np.array(points, dtype=np.int32)],
        isClosed=False,
        color=40,
        thickness=max(2, round(min(across_px, down_px) / 12)),
        lineType=cv2.LINE_AA,
    )


# ── What the person would have waited for ────────────────────────────────────────────


def moved_on(pretend: Pretend) -> float:
    """How many seconds the afternoon has been pushed forward by hand."""
    try:
        return float(json.loads(pretend.clock.read_text(encoding="utf-8"))["seconds"])
    except (OSError, ValueError, KeyError):
        return 0.0


def move_on(pretend: Pretend, seconds: float) -> float:
    total = moved_on(pretend) + seconds
    pretend.where.mkdir(parents=True, exist_ok=True)
    pretend.clock.write_text(json.dumps({"seconds": total}) + "\n", encoding="utf-8")
    note(pretend, "clock", added_seconds=seconds, total_seconds=total)
    return total


def the_time(pretend: Pretend | None) -> float:
    """Now, plus whatever was added by hand. Real time when nothing is pretended."""
    return time.time() + (moved_on(pretend) if pretend else 0.0)
