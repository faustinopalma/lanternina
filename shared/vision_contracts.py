"""Vision contracts, left over from the marker-and-QR pipeline.

**Nothing in the running system constructs any of these.** A page is read by handing a
model the blank and what came back off the glass, and the rule these types were built to
enforce — only the rectified region inside the ArUco quadrilateral is ever retained — no
longer describes the product. The camera is handheld now, faces will be in frame, and what
protects somebody is what may be inferred and what can be deleted, not what was cropped.

:class:`RawFrame` is kept because the sealing technique is worth having on hand: a type
that refuses to be pickled, copied or serialised, exposing no encoder, releasing its buffer
on exit. If a retention rule is ever wanted again, it is written here already. Read it as a
technique, not as a guarantee the system currently makes.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Final

from .errors import RetentionViolation

if TYPE_CHECKING:  # keeps `shared` importable without numpy installed
    import numpy as np


class RawFrame:
    """A full camera frame. In-memory only, for the lifetime of one capture.

    Nothing constructs one. Deliberately *not* a dataclass: it must not be frozen-copyable,
    comparable or serialisable, and every escape hatch Python would normally provide is
    closed.

    Use it as a context manager so the buffer is released as soon as rectification is
    done::

        with camera.capture_once() as frame:
            page = rectify(frame, spec)
        # frame's buffer is zeroed here; only `page` survives
    """

    __slots__ = ("_pixels", "_captured_at", "_released")

    def __init__(self, pixels: np.ndarray, captured_at: float) -> None:
        self._pixels = pixels
        self._captured_at = captured_at
        self._released = False

    @property
    def pixels(self) -> np.ndarray:
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

    def __enter__(self) -> RawFrame:
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


# How many descriptions are kept. A page is one thing somebody did in an afternoon, and a
# list long enough to need scrolling is a model narrating rather than reporting.
MAX_DESCRIPTIONS: Final = 8
# One line each. Long enough for "a house drawn in the third box", short enough that there
# is no room for a sentence about the person who drew it.
MAX_DESCRIPTION_CHARS: Final = 120


@dataclass(frozen=True, slots=True)
class WhatCameBack:
    """What is on a page that was not on the blank it was printed from.

    `ideas/10 §3`. The reading that replaces :class:`PageReading` once a page stops being a
    grid of declared cells. The model is given two images — the blank and the one that came
    off the glass — and says what was added. No rectangles, no cell kinds, no ids: the
    difference between two pictures is a thing a model can see, and describing where the
    answer was supposed to go was only ever a way of asking it to look there.

    **It describes ink, never a person.** The same line the working rules draw and the same
    one `agents/sheet_reader.py` holds: "a house drawn in the third box" is a description of
    a page; anything about who drew it, how well, or whether it is right, is not. There is no
    field here for a verdict and there is not going to be one.

    ``same_sheet`` is a fact the model reports, not a gate it enforces. `§3` again, and it is
    the parent's correction: the model has to interpret what is on the paper anyway, so
    insisting on the right sheet before looking is a machine's anxiety. A page that is not the
    one handed over is still a page somebody worked on, and what the afternoon does about that
    is the afternoon's business.
    """

    written: bool
    same_sheet: bool
    describes: tuple[str, ...]
    read_at: float
    # True when the cloud would not answer and this is the little that could be said anyway.
    degraded: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "written": self.written,
            "same_sheet": self.same_sheet,
            "describes": list(self.describes),
            "read_at": self.read_at,
            "degraded": self.degraded,
            "metadata": dict(self.metadata),
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> WhatCameBack:
        return WhatCameBack(
            written=bool(values.get("written", False)),
            same_sheet=bool(values.get("same_sheet", True)),
            describes=tuple(str(line) for line in values.get("describes", ())),
            read_at=float(values.get("read_at", 0.0)),
            degraded=bool(values.get("degraded", False)),
            metadata=dict(values.get("metadata", {})),
        )
