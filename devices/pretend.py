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

if TYPE_CHECKING:
    from devices.house import House

PRETEND_DIR_ENV: Final = "LANTERNINA_PRETEND_DIR"
# The switch, said as a word rather than as a path so that turning it off is turning off a
# flag and not remembering to unset a directory. Set it and the house is simulated in
# :data:`WHERE_BY_DEFAULT`; leave it, or set it to a false word, and the real house runs.
PRETEND_ENV: Final = "LANTERNINA_PRETEND"
WHERE_BY_DEFAULT: Final = "pretend"
_TRUE: Final = frozenset({"1", "true", "yes", "on"})

# The raster the page is kept as. The same 300 dpi the real scanner is configured for, so
# the markers land on the same number of pixels — 176 to 178 px on real paper, measured
# 4 August 2026, against 177.2 computed for 15 mm.
PAGE_DPI: Final = 300

# What a hand can be told to do, beyond naming the places one by one.
NOTHING: Final = "blank"
SOMETHING: Final = "marks"
EVERYTHING: Final = "all"

# A page has no declared boxes, so a hand writes in thirds of the sheet. Named rather than
# numbered so that a transcript reads as somewhere on the paper and not as an index.
BANDS: Final[tuple[str, ...]] = ("top", "middle", "bottom")


def pretend_in(env: Mapping[str, str]) -> Path | None:
    """The directory a simulated house writes into, or None for a house with equipment.

    Two ways to say yes and one of them is a plain flag, because a switch that is a path is
    a switch nobody is sure is off. Anything not in :data:`_TRUE` is off, so
    ``LANTERNINA_PRETEND=false`` is the real house and reads as one.
    """
    named = env.get(PRETEND_DIR_ENV, "").strip()
    if named:
        return Path(named)
    if env.get(PRETEND_ENV, "").strip().lower() in _TRUE:
        return Path(WHERE_BY_DEFAULT)
    return None


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


def hand_over(pretend: Pretend, sheet_id: SheetId, pdf: bytes, page: NDArray[np.uint8]) -> Path:
    """Put a sheet on the table: the PDF the printer would have had, and the page itself.

    Both, because they answer different questions. The PDF is what `lp` would have been
    given and is the thing to open when a page looks wrong. The raster is the sheet as an
    object — it is what gets written on and laid on the glass, so the page that comes back
    is the page that went out.
    """
    pretend.paper.mkdir(parents=True, exist_ok=True)
    page_pdf = pretend.paper / f"{sheet_id}.pdf"
    page_pdf.write_bytes(pdf)
    cv2.imwrite(str(pretend.paper / f"{sheet_id}.png"), page)
    note(pretend, "paper", sheet_id=str(sheet_id), file=page_pdf.name)
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


def which_places(asked: str) -> tuple[str, ...]:
    """Turn a word into the bands of the page that carry ink.

    A page has no declared places any more, so a hand writes in bands: the page in thirds,
    top to bottom, named so a transcript can say where the ink went. ``marks`` writes in one
    and no more — what a branch turns on is whether anything came back at all, and filling
    the page would be inventing an afternoon's worth of work nobody did.
    """
    if asked == NOTHING:
        return ()
    if asked == EVERYTHING:
        return BANDS
    if asked == SOMETHING:
        return BANDS[1:2]
    named = tuple(part.strip() for part in asked.split(",") if part.strip())
    unknown = [name for name in named if name not in BANDS]
    if unknown:
        raise ValueError(f"a page has no band called {unknown}; it has {list(BANDS)}")
    return named


def put_on_the_glass(
    pretend: Pretend, sheet_id: str, filled: Sequence[str], written: bytes = b""
) -> None:
    """Say which sheet is on the scanner, and what is on it.

    Two hands, and the difference is what the reading is being exercised against. ``filled``
    names bands of the paper and draws three polylines in them, which costs nothing and
    answers "is there ink". ``written`` is the whole sheet as somebody filled it in —
    `tools/handwriting.py` — which costs a model call and is the only one that puts real
    handwriting in front of the reader.
    """
    pretend.where.mkdir(parents=True, exist_ok=True)
    if written:
        (pretend.paper / f"{sheet_id}-written.png").write_bytes(written)
    pretend.glass.write_text(
        json.dumps({"sheet_id": sheet_id, "filled": list(filled), "by_hand": bool(written)})
        + "\n",
        encoding="utf-8",
    )


def off_the_glass(pretend: Pretend, house: House) -> tuple[str, NDArray[np.uint8]]:
    """The page laid on the glass, written on, as pixels the real reader would be handed.

    Everything from here down is the path the hub takes: the same blank, the same reading in
    the cloud, the same comparison. What is injected is one thing — what somebody wrote.

    Raises :class:`LookupError` when nothing was laid on the glass, which is the simulated
    equivalent of pressing the button with an empty scanner.
    """
    del house  # the reading happens in the runner now; this hands back pixels
    if not pretend.glass.is_file():
        raise LookupError("nothing is on the glass")
    asked = json.loads(pretend.glass.read_text(encoding="utf-8"))
    filled = [str(name) for name in asked.get("filled", [])]
    sheet_id = str(asked["sheet_id"])

    if asked.get("by_hand"):
        page = _page_image(pretend, f"{sheet_id}-written")
    else:
        page = _page_image(pretend, sheet_id)
        _by_hand(page, filled)
    # The sheet leaves the glass when it is read, exactly as a person picks it back up.
    pretend.glass.unlink(missing_ok=True)
    note(pretend, "glass", sheet_id=sheet_id, filled=filled, by_hand=bool(asked.get("by_hand")))
    return sheet_id, page


def _page_image(pretend: Pretend, sheet_id: str) -> NDArray[np.uint8]:
    path = pretend.paper / f"{sheet_id}.png"
    if not path.is_file():
        raise LookupError(f"there is no sheet {sheet_id!r} on the table")
    page = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if page is None:
        raise LookupError(f"the sheet {sheet_id!r} on the table is not an image")
    return np.asarray(page, dtype=np.uint8)


# Where a hand goes inside a band, as fractions of it. Three shapes rather than one, because
# a tick, a word and a drawing do not look alike, and a reader that only recognises one of
# them should fail here rather than in the house.
_TICK: Final = ((0.25, 0.55), (0.45, 0.80), (0.80, 0.20))
_WORD: Final = ((0.05, 0.70), (0.15, 0.30), (0.25, 0.70), (0.35, 0.35), (0.45, 0.70))
_DRAWING: Final = ((0.20, 0.80), (0.35, 0.25), (0.50, 0.75), (0.65, 0.20), (0.80, 0.70))

_SHAPES: Final = {"top": _WORD, "middle": _DRAWING, "bottom": _TICK}


def _by_hand(page: NDArray[np.uint8], filled: Sequence[str]) -> None:
    """Draw ink where somebody would have drawn it, in place, on the page itself.

    A page has no declared boxes, so the bands are thirds of the sheet and the shape drawn
    in each differs. That is deliberate: the reader has to describe what it sees rather than
    look up what was expected, and three different marks give it three different things to
    say.
    """
    height, width = page.shape[:2]
    for name in filled:
        if name not in BANDS:
            continue
        third = BANDS.index(name)
        top = height * (0.08 + 0.30 * third)
        band_h = height * 0.22
        left = width * 0.12
        band_w = width * 0.76
        points = [
            (round(left + across * band_w), round(top + down * band_h))
            for across, down in _SHAPES[name]
        ]
        cv2.polylines(
            page,
            [np.array(points, dtype=np.int32)],
            isClosed=False,
            color=40,
            thickness=max(2, round(min(band_w, band_h) / 40)),
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
