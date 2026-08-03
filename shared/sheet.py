"""The printed-sheet contract.

This is the single most load-bearing agreement in the system: the print agent lays a sheet
out against it, and the vision pipeline reads a sheet back using it. If the two ever drift,
answers get attributed to the wrong questions — so the spec is versioned, and a sheet
carries its version in the QR code. The vision pipeline refuses a sheet whose
``spec_version`` it does not understand rather than guessing.

Geometry
--------
Four ArUco markers sit at the page corners. Everything else is expressed in **page
coordinates**: normalised (0.0–1.0) over the quadrilateral formed by the markers' *inner*
corners. That makes cell positions independent of paper size, printer margins, camera
distance and DPI. Rectification maps that quadrilateral onto a fixed-size canvas
(:data:`RECTIFIED_WIDTH` x :data:`RECTIFIED_HEIGHT`), after which a cell's pixel rectangle
is a pure multiplication.

    (0,0) ┌──────────────┐ (1,0)
          │  ▣ markers ▣ │
          │              │
          │   cells...   │
    (0,1) └──────────────┘ (1,1)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Final

from .ids import CellId, ExerciseId, SheetId

SHEET_SPEC_VERSION: Final = 1

# ArUco dictionary. 4x4_50 is the smallest dictionary with enough ids: small markers stay
# legible when printed at ~15 mm on a home inkjet, and detection is fast on a mini-PC CPU.
ARUCO_DICT_NAME: Final = "DICT_4X4_50"

# Marker ids are fixed per corner so orientation is unambiguous even if the sheet is
# placed upside down under the camera.
MARKER_ID_TOP_LEFT: Final = 0
MARKER_ID_TOP_RIGHT: Final = 1
MARKER_ID_BOTTOM_RIGHT: Final = 2
MARKER_ID_BOTTOM_LEFT: Final = 3
REQUIRED_MARKER_IDS: Final = (
    MARKER_ID_TOP_LEFT,
    MARKER_ID_TOP_RIGHT,
    MARKER_ID_BOTTOM_RIGHT,
    MARKER_ID_BOTTOM_LEFT,
)

# Canvas the rectified page is warped onto. Fixed so cell pixel maths is deterministic.
RECTIFIED_WIDTH: Final = 1240
RECTIFIED_HEIGHT: Final = 1754  # A4 portrait at ~150 dpi

MARKER_SIZE_MM: Final = 15.0
QUIET_ZONE_MM: Final = 5.0


class CellKind(StrEnum):
    """What a cell contains, which decides how the vision pipeline reads it."""

    CHECKBOX = "checkbox"  # filled / not filled — readable locally, no cloud needed
    CHOICE_BOX = "choice_box"  # one of N boxes ticked
    CHAR_BOX = "char_box"  # a single handwritten character
    WORD_LINE = "word_line"  # a handwritten word or short phrase
    DRAWING_AREA = "drawing_area"  # freeform; never auto-graded, only shown to the parent


# Which cell kinds the on-device pipeline can read without the cloud. Everything else
# degrades to "needs review" when Azure is unreachable, and is never silently guessed.
LOCALLY_READABLE: Final = frozenset({CellKind.CHECKBOX, CellKind.CHOICE_BOX})


@dataclass(frozen=True, slots=True)
class Rect:
    """A rectangle in page coordinates (normalised 0.0–1.0, origin top-left)."""

    x: float
    y: float
    w: float
    h: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.x <= 1.0 and 0.0 <= self.y <= 1.0):
            raise ValueError(f"rect origin out of page bounds: ({self.x}, {self.y})")
        if self.w <= 0 or self.h <= 0:
            raise ValueError("rect must have positive size")
        if self.x + self.w > 1.0001 or self.y + self.h > 1.0001:
            raise ValueError("rect extends past the page edge")

    def to_pixels(
        self, width: int = RECTIFIED_WIDTH, height: int = RECTIFIED_HEIGHT
    ) -> tuple[int, int, int, int]:
        """Return ``(x0, y0, x1, y1)`` in rectified-canvas pixels."""
        x0 = round(self.x * width)
        y0 = round(self.y * height)
        return x0, y0, x0 + round(self.w * width), y0 + round(self.h * height)

    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "w": self.w, "h": self.h}


@dataclass(frozen=True, slots=True)
class CellSpec:
    """One answerable region. Position and meaning are known before the sheet is read."""

    id: CellId
    kind: CellKind
    rect: Rect
    # Human-readable label for the parent panel, e.g. "question 3, option B".
    label: str = ""
    # The expected answer, if this cell is auto-checkable. Never printed on the sheet.
    expected: str | None = None
    # Cells in the same group form one multiple-choice question.
    group: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "kind": str(self.kind),
            "rect": self.rect.to_dict(),
            "label": self.label,
            "group": self.group,
        }


@dataclass(frozen=True, slots=True)
class SheetSpec:
    """Everything needed to print a sheet and, later, to read it back."""

    sheet_id: SheetId
    exercise_id: ExerciseId
    title: str
    cells: tuple[CellSpec, ...]
    qr_rect: Rect
    spec_version: int = SHEET_SPEC_VERSION
    created_at: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def cell(self, cell_id: CellId) -> CellSpec:
        for spec in self.cells:
            if spec.id == cell_id:
                return spec
        raise KeyError(f"no cell {cell_id!r} on sheet {self.sheet_id}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "sheet_id": str(self.sheet_id),
            "exercise_id": str(self.exercise_id),
            "title": self.title,
            "spec_version": self.spec_version,
            "qr_rect": self.qr_rect.to_dict(),
            "cells": [c.to_dict() for c in self.cells],
        }


@dataclass(frozen=True, slots=True)
class QrPayload:
    """What the QR code on the sheet actually encodes.

    Kept tiny (short keys, no free text) so the code stays low-density and decodes
    reliably from a desk camera at an angle. It identifies the sheet; it carries no
    content and no personal data — the sheet spec is looked up locally by id.
    """

    sheet_id: SheetId
    exercise_id: ExerciseId
    spec_version: int = SHEET_SPEC_VERSION

    def encode(self) -> str:
        return f"LNT1|{self.spec_version}|{self.sheet_id}|{self.exercise_id}"

    @staticmethod
    def decode(raw: str) -> "QrPayload":
        """Parse a scanned QR string. Raises ValueError on anything unrecognised."""
        parts = raw.strip().split("|")
        if len(parts) != 4 or parts[0] != "LNT1":
            raise ValueError(f"not a Lanternina sheet code: {raw!r}")
        try:
            version = int(parts[1])
        except ValueError as exc:
            raise ValueError(f"bad spec version in {raw!r}") from exc
        return QrPayload(
            sheet_id=SheetId(parts[2]), exercise_id=ExerciseId(parts[3]), spec_version=version
        )
