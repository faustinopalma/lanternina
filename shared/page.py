"""What a page is: an object in a story, composed of things we know how to draw.

This replaces :mod:`shared.pagedesign`, which described a page as labelled rectangles at
coordinates — the definition of a form, faithfully rendered. `ideas/10` says why that could
not be fixed by asking a model more nicely, and what takes its place.

**A kind, and words.** The kind is closed and the words are free. The kind decides the
composition: where the illustration sits, where the heading sits, what furniture surrounds
them — a border and a legend for a map, a rule and a block of fields for a dossier. The
words decide what any of it is about. This is the split a device already makes with its jobs
and its name: closed where code has to understand it, open where only a person reads it.

The reason it is closed is not caution. **We draw the words** — `ideas/10 §5`: text baked
into an image reaches a person having passed no safety gate — so we compose the page, and a
kind of object the renderer cannot draw produces nothing at all.

**There are no coordinates here, and no cell has an identity.** A page says how much room to
leave beside a label, in three sizes, and the layout turns that into millimetres. Nothing
downstream needs to know where anything landed: a page is read by handing a model the blank
and what came back off the glass, and asking what is different.

**Ink is a number, declared here and measured on the rendered page.** :data:`INK_BUDGET`
is the fraction of the paper a finished page may cover. The number below is honest about
where it comes from and it is not yet the right one — see its own comment.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final


class PageError(ValueError):
    """A page that cannot be drawn, or that asks for something this format does not have."""


class PageKind(StrEnum):
    """What kind of object the paper is. Four, chosen by the parent on 24 August 2026.

    Each one is a layout somebody has written and looked at, so the list is short and grows
    by an ordinary change. A catalogue page was offered and left out.

    :attr:`NOTICE` is the fifth, added 28 August 2026. The strongest page of a long design
    exercise asked for nothing at all — a heading, some prose, a drawing, no place to write
    — and it is read standing up. ``NOTEBOOK`` with no spaces comes near it and does not
    reach it, because a margin rule and a sketch in the corner say somebody sat down.
    """

    MAP = "map"
    DOSSIER = "dossier"
    LABEL = "label"
    NOTEBOOK = "notebook"
    NOTICE = "notice"


class Room(StrEnum):
    """How much space to leave beside a label. Not how much space in millimetres.

    The layout decides the size, because the same label wants a different amount of paper
    on a museum label and in a field notebook. What the composition says is only whether
    somebody writes a few words, several, or draws.
    """

    A_LINE = "a_line"
    SOME_LINES = "some_lines"
    A_BOX = "a_box"


# A title is read across the room; the note is the prose under it; a label sits beside the
# place it names. All three chosen rather than measured, and all three sit inside what
# `printing.page_layout` can set without the words colliding — a test walks them.
MAX_TITLE: Final = 48
MAX_NOTE_LINE: Final = 72
MAX_NOTE_LINES: Final = 4
MAX_LABEL: Final = 40
MAX_SPACES: Final = 8
# What the picture shows, in words, and it is a prompt rather than something anybody reads.
MAX_ILLUSTRATION: Final = 200

# The fraction of the paper a finished page may cover in ink.
#
# ⚠ This is not yet the measured number `ideas/10 §4` asks for. That one has to be taken on
# the ET-2870 in the house, on a page somebody liked and a page they did not, and nobody has
# stood at the printer yet. What is here instead is a measurement that does exist: the sheet
# this format replaces, rasterised at 150 dpi on 20 August 2026, covers 2.78 % of an A4 page
# — 1734 mm² of 62370 — and that page is one the house already prints and accepts.
#
# So the budget refuses anything heavier than what is already being printed, which is a
# defensible floor and a placeholder for a ceiling. Replacing it is one constant and the
# tests that quote it.
INK_BUDGET: Final = 0.0278

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def plain(raw: object, limit: int, what: str) -> str:
    """One line of text as it may be drawn, or raise.

    Control characters go rather than being refused, for the reason
    :func:`shared.experience.plain` gives: this text was written by a model, and a line
    break is the cheapest way to make one line look like a new instruction.
    """
    if not isinstance(raw, str):
        raise PageError(f"{what} must be text, not {type(raw).__name__}")
    text = " ".join(_CONTROL.sub(" ", raw).split())
    if len(text) > limit:
        raise PageError(f"{what} is {len(text)} characters; at most {limit}")
    return text


@dataclass(frozen=True, slots=True)
class Space:
    """A labelled place to write, and how much of it there is."""

    label: str
    room: Room

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "room": str(self.room)}

    @staticmethod
    def from_dict(values: object) -> Space:
        if not isinstance(values, Mapping):
            raise PageError("a place to write is an object with a label and a room")
        _only(values, {"label", "room"}, "a place to write")
        try:
            room = Room(str(values.get("room", "")))
        except ValueError as exc:
            rooms = ", ".join(str(one) for one in Room)
            raise PageError(f"{str(values.get('room'))[:20]!r} is not one of {rooms}") from exc
        return Space(label=plain(values.get("label", ""), MAX_LABEL, "a label"), room=room)


@dataclass(frozen=True, slots=True)
class Page:
    """One printable object: what kind it is, what it says, and what the picture shows.

    ``illustration`` is the only field nobody in the house reads. It goes to the image
    model and its answer is placed by the layout; the words on the paper are ``title``,
    ``note`` and the labels, and every one of them is drawn by us from a string that came
    through the gate.
    """

    kind: PageKind
    title: str
    illustration: str
    note: tuple[str, ...] = ()
    spaces: tuple[Space, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": str(self.kind),
            "title": self.title,
            "illustration": self.illustration,
            "note": list(self.note),
            "spaces": [space.to_dict() for space in self.spaces],
        }

    def words(self) -> tuple[str, ...]:
        """Every string that will be printed, for the gate to screen in one pass.

        The illustration is not among them: it is never drawn as text, and screening it
        here would say a page is safe because a prompt was.
        """
        return (self.title, *self.note, *(space.label for space in self.spaces))

    @staticmethod
    def from_dict(values: object) -> Page:
        if not isinstance(values, Mapping):
            raise PageError("a page is an object")
        _only(values, {"kind", "title", "illustration", "note", "spaces"}, "a page")
        try:
            kind = PageKind(str(values.get("kind", "")))
        except ValueError as exc:
            kinds = ", ".join(str(one) for one in PageKind)
            raise PageError(f"{str(values.get('kind'))[:20]!r} is not one of {kinds}") from exc

        note = values.get("note") or ()
        if isinstance(note, str) or not isinstance(note, Sequence):
            raise PageError("the note is a list of lines")
        if len(note) > MAX_NOTE_LINES:
            raise PageError(f"{len(note)} lines of note; at most {MAX_NOTE_LINES}")

        spaces = values.get("spaces") or ()
        if isinstance(spaces, str) or not isinstance(spaces, Sequence):
            raise PageError("the places to write are a list")
        if len(spaces) > MAX_SPACES:
            raise PageError(
                f"{len(spaces)} places to write; a page a person can take in holds "
                f"{MAX_SPACES}"
            )

        page = Page(
            kind=kind,
            title=plain(values.get("title", ""), MAX_TITLE, "the title"),
            illustration=plain(
                values.get("illustration", ""), MAX_ILLUSTRATION, "the illustration"
            ),
            note=tuple(plain(line, MAX_NOTE_LINE, "a line of the note") for line in note),
            spaces=tuple(Space.from_dict(one) for one in spaces),
        )
        if not page.title:
            raise PageError("a page with no title is not an object, it is a sheet")
        if not page.illustration:
            raise PageError("a page says what its picture shows, even when none arrives")
        return page


def _only(values: Mapping[str, Any], allowed: set[str], what: str) -> None:
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise PageError(f"{what} carries {unknown}, which this format does not define")
