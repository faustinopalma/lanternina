"""Vision contracts, including the retention rule expressed as a type.

The rule: **the full camera frame is never written to disk.** Only the rectified region
inside the ArUco quadrilateral is retained.

:class:`RawFrame` enforces this rather than documenting it. It refuses to be pickled,
copied or serialised, exposes no encoder, and is a context manager that wipes its buffer
on exit. The only way to get bytes out of the vision pipeline is
:class:`RectifiedPage`, which by construction contains just the rectified crop.

Capture is single-shot, on a physical button press. There is no streaming endpoint, no
timer, and no motion trigger anywhere in this package — see docs/NON-GOALS.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from .errors import RetentionViolation
from .ids import CellId, ExerciseId, SheetId
from .sheet import CellKind

if TYPE_CHECKING:  # keeps `shared` importable without numpy installed
    import numpy as np


class RawFrame:
    """A full camera frame. In-memory only, for the lifetime of one capture.

    Deliberately *not* a dataclass: it must not be frozen-copyable, comparable or
    serialisable. Every escape hatch Python would normally provide is closed.

    Use it as a context manager so the buffer is released as soon as rectification is
    done::

        with camera.capture_once() as frame:
            page = rectify(frame, spec)
        # frame's buffer is zeroed here; only `page` survives
    """

    __slots__ = ("_pixels", "_captured_at", "_released")

    def __init__(self, pixels: "np.ndarray", captured_at: float) -> None:
        self._pixels = pixels
        self._captured_at = captured_at
        self._released = False

    @property
    def pixels(self) -> "np.ndarray":
        """The BGR array. Valid only inside the capture scope; never persist this."""
        if self._released:
            raise RetentionViolation("this frame was already released")
        return self._pixels

    @property
    def captured_at(self) -> float:
        return self._captured_at

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(self._pixels.shape) if not self._released else ()

    def release(self) -> None:
        """Zero the buffer and mark the frame dead. Idempotent."""
        if not self._released:
            try:
                self._pixels[...] = 0
            except Exception:  # a non-writeable view is fine; dropping the ref is enough
                pass
            self._pixels = None  # type: ignore[assignment]
            self._released = True

    def __enter__(self) -> "RawFrame":
        return self

    def __exit__(self, *exc: object) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"<RawFrame {'released' if self._released else self.shape} — not persistable>"

    # -- every serialisation route, closed -------------------------------------------
    def __getstate__(self) -> Any:
        raise RetentionViolation("full camera frames must never be serialised or persisted")

    def __reduce__(self) -> Any:
        raise RetentionViolation("full camera frames must never be pickled")

    def __deepcopy__(self, memo: dict) -> Any:
        raise RetentionViolation("full camera frames must never be copied")

    def __copy__(self) -> Any:
        raise RetentionViolation("full camera frames must never be copied")


@dataclass(frozen=True, slots=True)
class MarkerDetection:
    """One located ArUco marker. Corners are in original-frame pixel coordinates."""

    marker_id: int
    corners: tuple[tuple[float, float], ...]


@dataclass(frozen=True, slots=True)
class RectifiedPage:
    """The rectified page crop — the only image this system is allowed to keep.

    It contains the area inside the marker quadrilateral and nothing else: no desk, no
    room, no hands, no faces.
    """

    sheet_id: SheetId
    exercise_id: ExerciseId
    png: bytes
    width: int
    height: int
    captured_at: float
    spec_version: int
    # Perspective transform used, kept for debugging a misread. 3x3, row-major.
    homography: tuple[float, ...] = ()

    def to_metadata(self) -> dict[str, Any]:
        """Everything except the pixels, for logs and the parent panel."""
        return {
            "sheet_id": str(self.sheet_id),
            "exercise_id": str(self.exercise_id),
            "width": self.width,
            "height": self.height,
            "captured_at": self.captured_at,
            "spec_version": self.spec_version,
            "png_bytes": len(self.png),
        }


class ReadConfidence(StrEnum):
    """Deliberately coarse. A false "certain" is worse than an honest "unsure"."""

    CERTAIN = "certain"
    LIKELY = "likely"
    UNSURE = "unsure"


@dataclass(frozen=True, slots=True)
class CellReading:
    """What was found in one cell. An observation, never a judgement about the person."""

    cell_id: CellId
    kind: CellKind
    value: str | None
    confidence: ReadConfidence
    # True when the parent must look at this cell before anything is said to the learner.
    needs_review: bool = False
    note: str = ""


@dataclass(frozen=True, slots=True)
class PageReading:
    """The structured result of reading one sheet."""

    sheet_id: SheetId
    exercise_id: ExerciseId
    cells: tuple[CellReading, ...]
    read_at: float
    # True when the cloud was unavailable and only locally-readable cells were attempted.
    degraded: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def needs_review(self) -> bool:
        return any(c.needs_review for c in self.cells)
