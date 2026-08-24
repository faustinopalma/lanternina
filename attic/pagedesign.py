"""What a designed sheet is: a closed vocabulary of marks, and no way to spend much ink.

The sheet that came before this was arithmetic over a fixed template — four questions,
four boxes each, always in the same places. It read back reliably and it looked like a
form. This is the other half of the trade: a model designs the page, and what it may draw
is bounded here rather than by asking it nicely.

Three properties, and each one is a decision that cost something:

* **There is no fill.** Not a discouraged fill, not a fill with a limit — the vocabulary
  has no mark that covers an area. A drawing is strokes, so "no large areas to colour" is
  true by construction, and a page cannot be made heavy by a model that meant well. What
  it costs is that shading and solid silhouettes are unreachable, and some drawings want
  them.
* **Ink is a number with units.** :meth:`PageDesign.stroke_ink_mm2` is length times width
  summed over every stroke, and the caller refuses a design that spends more than it is
  allowed. The measured sheet this replaces puts 1734 mm² of ink on an A4 page, of which
  940 mm² is the scaffold every sheet pays — four markers, the QR and the ruler. So the
  budget below is not a round number somebody liked.
* **Positions are normalised over the marker quadrilateral**, exactly as
  :mod:`shared.sheet` is, so a design carries no paper size and the reader's geometry is
  untouched. :meth:`PageDesign.to_sheet_spec` produces the same ``SheetSpec`` the vision
  pipeline already reads, which is why a page can get more interesting without the reading
  contract moving at all.

Text on a design is text. It arrives from a model, it is stripped of control characters,
and nothing anywhere treats it as an instruction.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar, Final

from .ids import CellId, ExerciseId, SheetId
from .sheet import SHEET_SPEC_VERSION, CellKind, CellSpec, Heading, Rect, SheetSpec

# ── What a design may spend ──────────────────────────────────────────────────────────

# Measured, 20 August 2026, on the sheet this format replaces: rasterised at 150 dpi, an
# A4 page of four markers, a QR, the ruler and sixteen tick boxes is 2.78% ink, 1734 mm²
# of 62370. The scaffold alone is 1.51%, 940 mm². A design may add about as much again as
# the boxes did — 800 mm² — which keeps a finished sheet near 3% and well away from the
# coverage at which an inkjet slows down and paper cockles.
MAX_STROKE_INK_MM2: Final = 800.0

# A hairline on an inkjet breaks up; wider than this and line art starts to look like a
# marker pen and spends ink fast. Both ends chosen, not measured.
MIN_STROKE_MM: Final = 0.2
MAX_STROKE_MM: Final = 0.6

# A page a person can take in, and a prompt a model can fill without inventing filler.
MAX_MARKS: Final = 120
MAX_STROKE_POINTS: Final = 40
MAX_READABLE: Final = 24

MAX_TITLE: Final = 60
MAX_INSTRUCTIONS: Final = 160
MAX_WORDS: Final = 80
# A hint beside a box or under a line. 24 was the first guess and it refused a whole sheet
# a model designed — "Scrivi qui il nome della nuvola" is 31 — for nothing anybody would
# have minded. Chosen, not measured: what a label may safely be is a width in millimetres,
# and nothing checks that yet.
MAX_LABEL: Final = 48

MIN_TEXT_MM: Final = 2.5
MAX_TEXT_MM: Final = 8.0

# A tick box below this is hard to aim a pencil at, and a writing line below it is hard to
# write on. Both are fractions of the marker quadrilateral, which on A4 with the standard
# margins is about 178 x 251 mm — so 0.02 of the height is 5 mm.
MIN_BOX_SIDE: Final = 0.02

_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{1,31}$")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class DesignError(ValueError):
    """A design that cannot be drawn, or that says one thing and does another."""


def plain(raw: object, limit: int, what: str) -> str:
    """One line of text as it may be printed, or raise.

    Control characters are removed rather than refused, for the reason
    :mod:`shared.blueprint` gives: this text comes from a model and a line break is the
    cheapest way to make one line of a page look like a new instruction.
    """
    if not isinstance(raw, str):
        raise DesignError(f"{what} must be text, not {type(raw).__name__}")
    text = " ".join(_CONTROL.sub(" ", raw).split())
    if len(text) > limit:
        raise DesignError(f"{what} is {len(text)} characters; at most {limit}")
    return text


def _identifier(raw: object, what: str) -> str:
    if not isinstance(raw, str) or not _ID.match(raw):
        raise DesignError(f"{what} must be 2 to 32 characters of a-z, 0-9, hyphen or underscore")
    return raw


def _number(raw: object, what: str) -> float:
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        raise DesignError(f"{what} must be a number")
    value = float(raw)
    if not math.isfinite(value):
        raise DesignError(f"{what} must be a finite number")
    return value


def _unit(raw: object, what: str) -> float:
    """A coordinate on the page, where 0 is one edge of the marker frame and 1 the other."""
    value = _number(raw, what)
    if not 0.0 <= value <= 1.0:
        raise DesignError(f"{what} is {value}, which is off the page")
    return value


def _width(raw: object) -> float:
    value = _number(raw, "a stroke width")
    if not MIN_STROKE_MM <= value <= MAX_STROKE_MM:
        raise DesignError(
            f"a stroke width of {value} mm is outside {MIN_STROKE_MM}–{MAX_STROKE_MM} mm"
        )
    return value


def _only(values: Mapping[str, Any], allowed: set[str], what: str) -> None:
    """Refuse a key nobody declared, so what was not read cannot reach paper."""
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise DesignError(f"{what} carries {unknown}, which this format does not define")


def _rect(values: Any, what: str) -> Rect:
    if not isinstance(values, Mapping):
        raise DesignError(f"{what} must be an object with x, y, w and h")
    _only(dict(values), {"x", "y", "w", "h"}, what)
    try:
        rect = Rect(
            _unit(values.get("x"), f"{what} x"),
            _unit(values.get("y"), f"{what} y"),
            _number(values.get("w"), f"{what} width"),
            _number(values.get("h"), f"{what} height"),
        )
    except ValueError as exc:  # Rect enforces the page edge itself
        raise DesignError(f"{what}: {exc}") from exc
    return rect


# ── The marks ────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Stroke:
    """A run of straight segments. The only way anything curved reaches the page, and the
    only way ink is spent on a drawing at all."""

    mark: ClassVar[str] = "stroke"

    vertices: tuple[tuple[float, float], ...]
    width_mm: float = 0.3

    def __post_init__(self) -> None:
        if len(self.vertices) < 2:
            raise DesignError("a stroke needs at least two vertices")
        if len(self.vertices) > MAX_STROKE_POINTS:
            raise DesignError(
                f"a stroke has {len(self.vertices)} vertices; at most {MAX_STROKE_POINTS}"
            )

    def length(self, quad_w_mm: float, quad_h_mm: float) -> float:
        total = 0.0
        for (x0, y0), (x1, y1) in zip(self.vertices, self.vertices[1:], strict=False):
            total += math.hypot((x1 - x0) * quad_w_mm, (y1 - y0) * quad_h_mm)
        return total

    def to_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "vertices": [[x, y] for x, y in self.vertices],
            "width_mm": self.width_mm,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Stroke:
        _only(values, {"mark", "vertices", "width_mm"}, "a stroke")
        raw = values.get("vertices")
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise DesignError("a stroke's vertices must be a list")
        vertices = []
        for item in raw:
            if not isinstance(item, Sequence) or isinstance(item, str) or len(item) != 2:
                raise DesignError("each vertex is a pair [x, y]")
            vertices.append((_unit(item[0], "a vertex x"), _unit(item[1], "a vertex y")))
        return Stroke(tuple(vertices), _width(values.get("width_mm", 0.3)))


@dataclass(frozen=True, slots=True)
class Circle:
    """An outline circle. The radius is a fraction of the frame's width, so a circle stays
    a circle on paper instead of becoming an ellipse on a page that is not square."""

    mark: ClassVar[str] = "circle"

    cx: float
    cy: float
    r: float
    width_mm: float = 0.3

    def __post_init__(self) -> None:
        if self.r <= 0:
            raise DesignError("a circle needs a positive radius")
        if self.r > 0.5:
            raise DesignError(f"a circle of radius {self.r} is wider than the page")

    def length(self, quad_w_mm: float, _quad_h_mm: float) -> float:
        return 2.0 * math.pi * self.r * quad_w_mm

    def to_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "cx": self.cx,
            "cy": self.cy,
            "r": self.r,
            "width_mm": self.width_mm,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Circle:
        _only(values, {"mark", "cx", "cy", "r", "width_mm"}, "a circle")
        return Circle(
            _unit(values.get("cx"), "a circle cx"),
            _unit(values.get("cy"), "a circle cy"),
            _number(values.get("r"), "a circle radius"),
            _width(values.get("width_mm", 0.3)),
        )


@dataclass(frozen=True, slots=True)
class Words:
    """Text printed on the page. The reader never looks at it: it is not a place an answer
    can be, which is the distinction :class:`~shared.sheet.Heading` already draws."""

    mark: ClassVar[str] = "words"

    rect: Rect
    text: str
    size_mm: float = 4.0

    def __post_init__(self) -> None:
        if not MIN_TEXT_MM <= self.size_mm <= MAX_TEXT_MM:
            raise DesignError(
                f"text at {self.size_mm} mm is outside {MIN_TEXT_MM}–{MAX_TEXT_MM} mm"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "rect": self.rect.to_dict(),
            "text": self.text,
            "size_mm": self.size_mm,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> Words:
        _only(values, {"mark", "rect", "text", "size_mm"}, "a line of words")
        return Words(
            _rect(values.get("rect"), "a line of words"),
            plain(values.get("text", ""), MAX_WORDS, "a line of words"),
            _number(values.get("size_mm", 4.0), "a text size"),
        )


@dataclass(frozen=True, slots=True)
class TickBox:
    """A box to put a mark in. Becomes a cell the reader is asked about.

    ``group`` is what attributes a mark to the thing it answers: boxes sharing a group are
    the choices of one question. It carries no expected answer, because nothing on a sheet
    ever does.
    """

    mark: ClassVar[str] = "tick_box"
    kind: ClassVar[CellKind] = CellKind.CHOICE_BOX

    id: str
    rect: Rect
    label: str = ""
    group: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "id": self.id,
            "rect": self.rect.to_dict(),
            "label": self.label,
            "group": self.group,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> TickBox:
        _only(values, {"mark", "id", "rect", "label", "group"}, "a tick box")
        return TickBox(
            _identifier(values.get("id"), "a tick box id"),
            _rect(values.get("rect"), "a tick box"),
            plain(values.get("label", ""), MAX_LABEL, "a tick box label"),
            plain(values.get("group", ""), MAX_LABEL, "a tick box group"),
        )


@dataclass(frozen=True, slots=True)
class WriteLine:
    """A ruled line to write on. Drawn as its baseline and not as a box, which is both
    less ink and closer to what a line to write on looks like."""

    mark: ClassVar[str] = "write_line"
    kind: ClassVar[CellKind] = CellKind.WORD_LINE

    id: str
    rect: Rect
    label: str = ""
    group: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "id": self.id,
            "rect": self.rect.to_dict(),
            "label": self.label,
            "group": self.group,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> WriteLine:
        _only(values, {"mark", "id", "rect", "label", "group"}, "a writing line")
        return WriteLine(
            _identifier(values.get("id"), "a writing line id"),
            _rect(values.get("rect"), "a writing line"),
            plain(values.get("label", ""), MAX_LABEL, "a writing line label"),
            plain(values.get("group", ""), MAX_LABEL, "a writing line group"),
        )


@dataclass(frozen=True, slots=True)
class DrawArea:
    """Somewhere to draw. Never graded and never scored — what comes back is shown to the
    parent and described as marks on paper, which is all anybody here may say about it."""

    mark: ClassVar[str] = "draw_area"
    kind: ClassVar[CellKind] = CellKind.DRAWING_AREA

    id: str
    rect: Rect
    label: str = ""
    group: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "mark": self.mark,
            "id": self.id,
            "rect": self.rect.to_dict(),
            "label": self.label,
            "group": self.group,
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> DrawArea:
        _only(values, {"mark", "id", "rect", "label", "group"}, "a drawing area")
        return DrawArea(
            _identifier(values.get("id"), "a drawing area id"),
            _rect(values.get("rect"), "a drawing area"),
            plain(values.get("label", ""), MAX_LABEL, "a drawing area label"),
            plain(values.get("group", ""), MAX_LABEL, "a drawing area group"),
        )


Mark = Stroke | Circle | Words | TickBox | WriteLine | DrawArea
Readable = TickBox | WriteLine | DrawArea

_READERS: Final[Mapping[str, Any]] = {
    Stroke.mark: Stroke.from_dict,
    Circle.mark: Circle.from_dict,
    Words.mark: Words.from_dict,
    TickBox.mark: TickBox.from_dict,
    WriteLine.mark: WriteLine.from_dict,
    DrawArea.mark: DrawArea.from_dict,
}

MARK_NAMES: Final = tuple(_READERS)


def mark_from_dict(values: Mapping[str, Any]) -> Mark:
    if not isinstance(values, Mapping):
        raise DesignError("a mark must be an object")
    name = values.get("mark")
    reader = _READERS.get(str(name))
    if reader is None:
        raise DesignError(f"{name!r} is not a mark this format defines; {list(MARK_NAMES)}")
    return reader(values)  # type: ignore[no-any-return]


# ── The page ─────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class PageDesign:
    """One sheet as a model designed it, in marks this format defines and nothing else."""

    title: str
    instructions: str
    marks: tuple[Mark, ...]

    def __post_init__(self) -> None:
        if not self.marks:
            raise DesignError("a design with no marks is a blank page")
        if len(self.marks) > MAX_MARKS:
            raise DesignError(f"{len(self.marks)} marks; at most {MAX_MARKS}")

        readable = self.readable
        if not readable:
            raise DesignError(
                "a sheet nobody can answer is not this system's sheet: give it a box, a "
                "line to write on or somewhere to draw"
            )
        if len(readable) > MAX_READABLE:
            raise DesignError(f"{len(readable)} answerable places; at most {MAX_READABLE}")

        seen: set[str] = set()
        for item in readable:
            if item.id in seen:
                raise DesignError(f"two answerable places share the id {item.id!r}")
            seen.add(item.id)
            if item.rect.w < MIN_BOX_SIDE or item.rect.h < MIN_BOX_SIDE:
                raise DesignError(
                    f"{item.id!r} is {item.rect.w:.3f} x {item.rect.h:.3f} of the page, "
                    f"under {MIN_BOX_SIDE} on a side and too small to use"
                )

        for first, second in _overlapping(readable):
            raise DesignError(
                f"{first!r} and {second!r} overlap; a mark inside both answers two things"
            )

    @property
    def readable(self) -> tuple[Readable, ...]:
        return tuple(m for m in self.marks if isinstance(m, TickBox | WriteLine | DrawArea))

    @property
    def strokes(self) -> tuple[Stroke | Circle, ...]:
        return tuple(m for m in self.marks if isinstance(m, Stroke | Circle))

    @property
    def words(self) -> tuple[Words, ...]:
        return tuple(m for m in self.marks if isinstance(m, Words))

    def stroke_ink_mm2(self, quad_w_mm: float, quad_h_mm: float) -> float:
        """The ink the drawing spends, length times width over every stroke.

        This is the physical figure and the one the budget is applied to: it is the area a
        pen laying that line would wet. It counts a corner twice and ignores that a joint
        overlaps itself, so it reads high on a drawing full of short segments.

        It is not the same number a raster of the page gives back, and the difference is
        not error in either: rounding a stroke width to whole pixels moves the rasterised
        figure by up to 70% at the widths this format allows. Measured, 20 August 2026, on
        a single line across the frame — the raster reads 0.85 to 1.70 times this, by width
        and resolution.
        """
        return sum(m.length(quad_w_mm, quad_h_mm) * m.width_mm for m in self.strokes)

    def to_sheet_spec(
        self,
        *,
        sheet_id: SheetId,
        exercise_id: ExerciseId,
        qr_rect: Rect,
        created_at: float = 0.0,
    ) -> SheetSpec:
        """The same contract the vision pipeline already reads.

        This is the seam that makes the whole change cheap: a page may become as
        interesting as a model can design it, and the reader still receives a list of
        rectangles with ids, which is what it has always received.
        """
        cells = tuple(
            CellSpec(
                id=CellId(item.id),
                kind=item.kind,
                rect=item.rect,
                label=item.label,
                group=item.group,
            )
            for item in self.readable
        )
        headings = tuple(
            Heading(rect=w.rect, text=w.text, size_mm=w.size_mm) for w in self.words
        )
        return SheetSpec(
            sheet_id=sheet_id,
            exercise_id=exercise_id,
            title=self.title,
            cells=cells,
            qr_rect=qr_rect,
            spec_version=SHEET_SPEC_VERSION,
            created_at=created_at,
            headings=headings,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "instructions": self.instructions,
            "marks": [m.to_dict() for m in self.marks],
        }

    @staticmethod
    def from_dict(values: Mapping[str, Any]) -> PageDesign:
        if not isinstance(values, Mapping):
            raise DesignError("a design must be an object")
        _only(dict(values), {"title", "instructions", "marks"}, "a design")
        raw = values.get("marks", [])
        if not isinstance(raw, Sequence) or isinstance(raw, str):
            raise DesignError("marks must be a list")
        return PageDesign(
            title=plain(values.get("title", ""), MAX_TITLE, "a title"),
            instructions=plain(
                values.get("instructions", ""), MAX_INSTRUCTIONS, "the instructions"
            ),
            marks=tuple(mark_from_dict(m) for m in raw),
        )


def _overlapping(items: Sequence[Readable]) -> list[tuple[str, str]]:
    """Answerable places that share paper. One pair is enough to refuse the design."""
    clashes = []
    for index, first in enumerate(items):
        for second in items[index + 1 :]:
            a, b = first.rect, second.rect
            if (
                a.x < b.x + b.w
                and b.x < a.x + a.w
                and a.y < b.y + b.h
                and b.y < a.y + a.h
            ):
                clashes.append((first.id, second.id))
    return clashes
