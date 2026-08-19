"""Themes: the subjects the parent is willing to let a picture be about.

A theme is the unit of approval for pictures. It exists because approving one image an
hour is not something a person will keep doing, and the alternative — no approval at all —
was worse. What it buys is an hourly picture; what it costs is that a picture is seen that
no adult has seen, bounded only by the subject and the safety gate.

Removing a theme is therefore as important as adding one, and is a first-class operation
rather than an edit buried in a settings page.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# A theme is read by a person and put into a prompt, so it stays short and plain.
MAX_LABEL_LENGTH = 80


@dataclass(frozen=True, slots=True)
class Theme:
    id: str
    household_id: str
    label: str
    created_at: float
    created_by: str = ""
    active: bool = True

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "createdAt": self.created_at,
            "active": self.active,
        }


@runtime_checkable
class ThemeStore(Protocol):
    def add(self, theme: Theme) -> Theme: ...

    def list(self, household_id: str, *, active_only: bool = True) -> list[Theme]: ...

    def remove(self, household_id: str, theme_id: str) -> Theme: ...


@dataclass
class InMemoryThemeStore:
    _rows: dict[tuple[str, str], Theme] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, theme: Theme) -> Theme:
        with self._lock:
            return self._rows.setdefault((theme.household_id, theme.id), theme)

    def list(self, household_id: str, *, active_only: bool = True) -> list[Theme]:
        with self._lock:
            rows = [
                row
                for (household, _), row in self._rows.items()
                if household == household_id and (row.active or not active_only)
            ]
        return sorted(rows, key=lambda row: row.created_at)

    def remove(self, household_id: str, theme_id: str) -> Theme:
        with self._lock:
            current = self._rows[(household_id, theme_id)]
            # Kept rather than deleted: a picture already shown should stay traceable to
            # the thing the parent once said yes to.
            removed = Theme(
                id=current.id,
                household_id=current.household_id,
                label=current.label,
                created_at=current.created_at,
                created_by=current.created_by,
                active=False,
            )
            self._rows[(household_id, theme_id)] = removed
            return removed


def clean_label(raw: str) -> str:
    """Normalise what the parent typed. Raises ValueError if it is not usable.

    Free text from a person goes into a model prompt, so newlines are removed here: they
    are the cheapest way to make one line of a prompt look like a new instruction.
    """
    label = " ".join(raw.split())
    if not label:
        raise ValueError("a theme needs some words")
    if len(label) > MAX_LABEL_LENGTH:
        raise ValueError(f"a theme must be at most {MAX_LABEL_LENGTH} characters")
    return label


def new_theme_id() -> str:
    import secrets

    return f"th_{secrets.token_hex(4)}"


def make_theme(household_id: str, label: str, created_by: str) -> Theme:
    return Theme(
        id=new_theme_id(),
        household_id=household_id,
        label=clean_label(label),
        created_at=time.time(),
        created_by=created_by,
    )
