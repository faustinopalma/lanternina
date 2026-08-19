"""Everything in the house, with a job and a name — and what each display reports.

Two things live here. The inventory is one row per thing the house can use: a display, a
printer, a scanner. The row carries an identity, a job the parent chooses and a name the
parent writes. The status is what a display last said about itself, which only displays
have.

The charge is deliberately coarse. The board has no fuel gauge, so a percentage would be
arithmetic performed on a guess: the panel says "full", "half", "recharge it" or "on
mains", which is what a person can act on anyway.

Nothing here is about a person. A battery reading is a fact about a device, and a name is
a name the parent gave to an object.
"""

from __future__ import annotations

import re
import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from typing import Any, Protocol, runtime_checkable

# How long a display may stay silent before the panel says so. Two missed hours is well
# past any polling interval we set, so it means something is actually wrong.
SILENT_AFTER_SECONDS = 7200

# How a thing arrives is the only way the three kinds differ. A display announces itself,
# because its firmware is already asking the hub for something to show; a printer and a
# scanner have to be looked for over mDNS.
KIND_DISPLAY = "display"
KIND_PRINTER = "printer"
KIND_SCANNER = "scanner"
KINDS = (KIND_DISPLAY, KIND_PRINTER, KIND_SCANNER)

# The jobs the parent can hand out. Empty is the honest starting state: a display with no
# job shows its own id, so the row here and the object on the shelf can be matched.
JOB_NONE = ""
JOB_PICTURE = "picture"
JOB_SHEET = "sheet"
JOB_PRINT = "print"
JOB_SCAN = "scan"

JOBS_BY_KIND: dict[str, tuple[str, ...]] = {
    KIND_DISPLAY: (JOB_PICTURE, JOB_SHEET),
    KIND_PRINTER: (JOB_PRINT,),
    KIND_SCANNER: (JOB_SCAN,),
}

# The name is read on a display and put into a sentence a model builds, so it stays short.
# Measured against the notice renderer's body font, which has 728 px to work with: forty
# characters of ordinary Italian come to 692 px and stay on one line, forty capital Ws
# come to 1280 px and do not. The limit is a comfortable case, not a guarantee.
MAX_NAME_LENGTH = 40

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


@dataclass(frozen=True, slots=True)
class DeviceStatus:
    id: str
    household_id: str
    name: str
    last_seen: float
    # "mains", "ok", "low" or "critical" — decided by the hub, which knows the thresholds.
    level: str = "ok"
    voltage: float | None = None
    rssi: float | None = None
    firmware: str = ""
    model: str = ""

    def silent_for(self, now: float | None = None) -> float:
        return max(0.0, (now or time.time()) - self.last_seen)

    def to_public(self, now: float | None = None) -> dict[str, Any]:
        silent = self.silent_for(now)
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "voltage": self.voltage,
            "rssi": self.rssi,
            "firmware": self.firmware,
            "model": self.model,
            "lastSeen": self.last_seen,
            "silentSeconds": silent,
            # The panel is where a fault is allowed to appear. The display never says it.
            "silent": silent > SILENT_AFTER_SECONDS,
        }


@runtime_checkable
class DeviceStatusStore(Protocol):
    def record(self, status: DeviceStatus) -> DeviceStatus: ...

    def list(self, household_id: str) -> list[DeviceStatus]: ...


@dataclass
class InMemoryDeviceStatusStore:
    _rows: dict[tuple[str, str], DeviceStatus] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, status: DeviceStatus) -> DeviceStatus:
        with self._lock:
            self._rows[(status.household_id, status.id)] = status
        return status

    def list(self, household_id: str) -> list[DeviceStatus]:
        with self._lock:
            rows = [
                row
                for (household, _), row in self._rows.items()
                if household == household_id
            ]
        return sorted(rows, key=lambda row: row.name)


@dataclass(frozen=True, slots=True)
class Thing:
    """One object in the house: what it is, what it is for, what it is called.

    The identity is never an address. Between 4 and 19 August 2026 the printer moved from
    192.168.0.138 to 192.168.0.5 and the hub from .157 to .158; a list keyed on addresses
    would have grown a duplicate for each. So the key is the MAC for a display, and the
    kind together with the mDNS hostname for a printer or a scanner — one box answers both
    `_ipp._tcp` and `_uscan._tcp`, and the two are assigned separately. The address is
    carried alongside as something the hub happens to know today.
    """

    id: str
    household_id: str
    kind: str
    name: str = ""
    # What the thing calls itself: the friendly id a display puts on its own screen, or
    # the mDNS service name. Not the parent's to choose, and the only thing to match a row
    # against an object on a shelf before anybody has named it.
    label: str = ""
    job: str = JOB_NONE
    model: str = ""
    address: str = ""
    # The hub would not use this name: it carries the name of a person. Set by the house,
    # which is the only side that knows who lives there, and cleared when a new name is
    # written. Without it a refused name would look like a setting that saved and did
    # nothing.
    name_refused: bool = False
    last_seen: float = 0.0
    first_seen: float = 0.0

    def silent_for(self, now: float | None = None) -> float:
        return max(0.0, (now or time.time()) - self.last_seen)

    def to_public(self, now: float | None = None) -> dict[str, Any]:
        silent = self.silent_for(now)
        return {
            "id": self.id,
            "kind": self.kind,
            "name": self.name,
            "label": self.label,
            "job": self.job,
            "jobChoices": list(JOBS_BY_KIND.get(self.kind, ())),
            "model": self.model,
            "address": self.address,
            "nameRefused": self.name_refused,
            "lastSeen": self.last_seen,
            "silentSeconds": silent,
            # The panel is where a fault is allowed to appear. Nothing in the house says it.
            "silent": silent > SILENT_AFTER_SECONDS,
        }


@runtime_checkable
class InventoryStore(Protocol):
    def see(self, thing: Thing) -> Thing: ...

    def assign(
        self,
        household_id: str,
        thing_id: str,
        *,
        job: str | None = None,
        name: str | None = None,
    ) -> Thing: ...

    def list(self, household_id: str) -> list[Thing]: ...

    def forget(self, household_id: str, thing_id: str) -> None: ...


@dataclass
class InMemoryInventoryStore:
    _rows: dict[tuple[str, str], Thing] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def see(self, thing: Thing) -> Thing:
        """The hub reports what it found. What the parent wrote survives the report."""
        with self._lock:
            key = (thing.household_id, thing.id)
            known = self._rows.get(key)
            fresh = (
                thing
                if known is None
                else replace(
                    known,
                    kind=thing.kind or known.kind,
                    label=thing.label or known.label,
                    model=thing.model or known.model,
                    address=thing.address or known.address,
                    name_refused=thing.name_refused,
                    last_seen=max(thing.last_seen, known.last_seen),
                )
            )
            if known is None:
                fresh = replace(fresh, first_seen=fresh.first_seen or fresh.last_seen)
            self._rows[key] = fresh
            return fresh

    def assign(
        self,
        household_id: str,
        thing_id: str,
        *,
        job: str | None = None,
        name: str | None = None,
    ) -> Thing:
        with self._lock:
            current = self._rows[(household_id, thing_id)]
            if job is not None and job != JOB_NONE:
                # A job belongs to one thing. Handing it over takes it from whoever held
                # it, which is what a parent means by "this is the picture display now".
                for key, row in list(self._rows.items()):
                    if key[0] == household_id and key[1] != thing_id and row.job == job:
                        self._rows[key] = replace(row, job=JOB_NONE)
            updated = replace(
                current,
                job=current.job if job is None else job,
                name=current.name if name is None else name,
                # A new name is a new attempt: the house has not judged it yet.
                name_refused=current.name_refused if name is None else False,
            )
            self._rows[(household_id, thing_id)] = updated
            return updated

    def list(self, household_id: str) -> list[Thing]:
        with self._lock:
            rows = [row for (household, _), row in self._rows.items() if household == household_id]
        return sorted(rows, key=order_of)

    def forget(self, household_id: str, thing_id: str) -> None:
        with self._lock:
            self._rows.pop((household_id, thing_id), None)


def order_of(thing: Thing) -> tuple[int, str]:
    """Displays first, then printers, then scanners; within a kind, by what it is called."""
    kind_rank = KINDS.index(thing.kind) if thing.kind in KINDS else len(KINDS)
    return (kind_rank, (thing.name or thing.label or thing.id).lower())


def clean_name(raw: str) -> str:
    """Normalise the name the parent wrote. Raises ValueError if it cannot be used.

    An empty name is allowed and means the thing has not been named yet. Newlines and
    control characters are removed rather than refused: this text ends up inside a model
    prompt, and a line break is the cheapest way to make one line of a prompt look like a
    new instruction.
    """
    name = " ".join(_CONTROL.sub(" ", raw).split())
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"a name must be at most {MAX_NAME_LENGTH} characters")
    return name


def clean_job(kind: str, raw: str) -> str:
    """The job as the parent chose it. Raises ValueError if that kind cannot do it."""
    job = raw.strip()
    if job == JOB_NONE:
        return JOB_NONE
    if job not in JOBS_BY_KIND.get(kind, ()):
        raise ValueError(f"a {kind} cannot be given the job {job!r}")
    return job


def merged(
    things: Sequence[Thing], statuses: Sequence[DeviceStatus], now: float | None = None
) -> list[dict[str, Any]]:
    """One list of everything, with what a display reported folded into its row.

    A status with no row of its own still appears. Displays were reporting before the
    inventory existed, and dropping them here would make the panel look emptier than the
    house is.
    """
    by_id = {status.id: status for status in statuses}
    rows = list(things)
    known = {thing.id for thing in rows}
    rows.extend(
        Thing(
            id=status.id,
            household_id=status.household_id,
            kind=KIND_DISPLAY,
            label=status.name,
            model=status.model,
            last_seen=status.last_seen,
        )
        for status in statuses
        if status.id not in known
    )
    answer: list[dict[str, Any]] = []
    for thing in sorted(rows, key=order_of):
        row = thing.to_public(now)
        status = by_id.get(thing.id)
        if status is not None:
            row["lastSeen"] = max(row["lastSeen"], status.last_seen)
            row["silentSeconds"] = status.silent_for(now)
            row["silent"] = row["silentSeconds"] > SILENT_AFTER_SECONDS
            row["level"] = status.level
            row["voltage"] = status.voltage
            row["rssi"] = status.rssi
            row["firmware"] = status.firmware
            row["model"] = row["model"] or status.model
            row["label"] = row["label"] or status.name
        answer.append(row)
    return answer
