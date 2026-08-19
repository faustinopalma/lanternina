"""What is in this house, and what each thing is for — the hub's side of it.

The panel holds the list; this module is how the house finds things to put on it and how
it remembers what the parent decided. Three jobs, and they are separate on purpose.

Finding. A display announces itself by asking for something to show. A printer and a
scanner do not talk to us, so they are looked for over mDNS, on the status push the hub
already makes every five minutes rather than on a timer of its own. **An empty answer means
"found nothing this time", never "the list is now empty"**: the first scan after a quiet
spell has returned nothing and then found the device a minute later. Nothing is ever
removed from the list here.

Remembering. The choice is cached beside the rhythm, so a panel that cannot be reached
leaves the house working to the last known assignment rather than stopping.

Refusing a name. A device name is free text a parent typed, it reaches a model as material,
and "Sofia's printer" is exactly what somebody would naturally write. A person's name never
goes into a prompt. The check has to be here because this is the only side that knows the
name — it comes from the environment, and the cloud has nowhere to store it.

Stdlib only, because the hub has no virtualenv for this and should not need one.
"""

from __future__ import annotations

import json
import os
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

KIND_DISPLAY = "display"
KIND_PRINTER = "printer"
KIND_SCANNER = "scanner"

JOB_PICTURE = "picture"
JOB_SHEET = "sheet"
JOB_PRINT = "print"
JOB_SCAN = "scan"

# What each kind answers to. Both were read off the machine in the house on 4 August 2026:
# the Epson ET-2870 advertises `_ipp._tcp` for printing and `_uscan._tcp` for scanning.
SERVICES: dict[str, str] = {
    "_ipp._tcp": KIND_PRINTER,
    "_uscan._tcp": KIND_SCANNER,
}

# mDNS answers late. Long enough to be worth asking, short enough that a status push that
# runs every five minutes is never held up by it.
DISCOVERY_TIMEOUT_SECONDS = 12

# A name shorter than this is not distinctive enough to match on: a two-letter name would
# refuse half the words a parent might reasonably write.
SHORTEST_NAME_PART = 3


@dataclass(frozen=True, slots=True)
class Found:
    """One thing seen on the network. Identified by what it is and what it is called.

    The kind is part of the identity, not decoration. The Epson in this house answers both
    `_ipp._tcp` and `_uscan._tcp` from the hostname EPSOND59029.local, so a row keyed on
    the hostname alone made the second sighting overwrite the first: one box, one row, and
    no way for the parent to hand out the print job and the scan job separately. The
    address is never part of it — the printer moved from 192.168.0.138 to 192.168.0.5
    between 4 and 19 August 2026, and a list keyed on addresses would have grown a
    duplicate for each move.
    """

    id: str
    kind: str
    label: str
    address: str = ""
    model: str = ""

    def reported(self, seen_at: float) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "name": self.label,
            "address": self.address,
            "model": self.model,
            "lastSeen": seen_at,
        }


def _unescape(field: str) -> str:
    """Decode avahi's escapes: `\\;`, `\\\\`, and `\\NNN` for a byte written in decimal.

    One left-to-right pass rather than sequential replacements, because the two characters
    of an escaped backslash would otherwise be read as the opening of the next escape.
    """
    out: list[str] = []
    index = 0
    while index < len(field):
        if field[index] != "\\" or index + 1 >= len(field):
            out.append(field[index])
            index += 1
            continue
        digits = field[index + 1 : index + 4]
        if len(digits) == 3 and digits.isdigit() and int(digits) <= 0xFF:
            out.append(chr(int(digits)))
            index += 4
        else:
            out.append(field[index + 1])
            index += 2
    return "".join(out)


def _split(line: str) -> list[str]:
    """avahi-browse -p separates fields with `;` and escapes a literal one with `\\;`."""
    fields: list[str] = []
    current: list[str] = []
    escaped = False
    for character in line:
        if escaped:
            current.append("\\" + character)
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == ";":
            fields.append(_unescape("".join(current)))
            current = []
        else:
            current.append(character)
    fields.append(_unescape("".join(current)))
    return fields


def parse_browse(output: str, kind: str) -> list[Found]:
    """The resolved records in `avahi-browse -rpt` output, one per service.

    Only lines beginning with `=` carry a hostname and an address; `+` lines are the
    announcement before resolution and would give a row with no way to reach it.
    """
    found: dict[str, Found] = {}
    for line in output.splitlines():
        if not line.startswith("="):
            continue
        fields = _split(line)
        if len(fields) < 8:
            continue
        _, _, protocol, label, _, _, hostname, address = fields[:8]
        if protocol != "IPv4" or not hostname:
            continue
        txt = " ".join(fields[9:]) if len(fields) > 9 else ""
        # Keep the first sighting: a printer on two interfaces is one printer.
        found.setdefault(
            hostname,
            Found(
                id=f"{kind}:{hostname}",
                kind=kind,
                label=label or hostname,
                address=address,
                model=_txt_value(txt, "ty"),
            ),
        )
    return list(found.values())


def _txt_value(txt: str, key: str) -> str:
    """The value of one TXT record, e.g. `ty=EPSON ET-2870 Series`."""
    for chunk in txt.split('" "'):
        entry = chunk.strip('" ')
        name, sep, value = entry.partition("=")
        if sep and name == key:
            return value
    return ""


def discover(timeout: float = DISCOVERY_TIMEOUT_SECONDS) -> list[Found]:
    """Everything on the network we know how to look for.

    Returns what was seen this time. An empty list is not a statement that the house is
    empty — avahi has answered `[]` and then found the same printer a minute later — so no
    caller may use it to remove anything.
    """
    seen: list[Found] = []
    for service, kind in SERVICES.items():
        try:
            done = subprocess.run(
                ["avahi-browse", "-rpt", service],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            # A hub without avahi, or a query that took too long. Both mean "nothing this
            # time", which is a state this function is allowed to be in.
            continue
        seen.extend(parse_browse(done.stdout, kind))
    return seen


def _flatten(value: str) -> str:
    """Casefolded and stripped of accents, so `Sofía` and `SOFIA` compare equal."""
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()


def person_parts(person: str) -> tuple[str, ...]:
    """The pieces of a person's name worth matching on, longest first."""
    parts = [part for part in _flatten(person).split() if len(part) >= SHORTEST_NAME_PART]
    return tuple(sorted(parts, key=len, reverse=True))


def names_a_person(name: str, person: str) -> bool:
    """Whether this device name carries the person's name.

    Substring rather than whole word: "stampante di Sofia" and "sofiaprinter" are the same
    mistake, and the second is the one a word-boundary check would let through.
    """
    if not person.strip():
        return False
    flat = _flatten(name)
    return any(part in flat for part in person_parts(person))


def learner_name() -> str:
    """Who lives here. Read from the environment, never from the panel."""
    return os.environ.get("LANTERNINA_LEARNER_NAME", "")


def screen_names(
    things: list[dict[str, Any]], person: str
) -> tuple[list[dict[str, Any]], list[str]]:
    """Drop every device name that carries the person's name.

    Returns the things with the offending names blanked and marked, and the ids they
    belonged to. Blanked rather than kept and marked: a name that is still in the cache is
    a name something can still reach for. The mark is what lets the parent be told why,
    which is the difference between a refusal and a setting that silently does nothing.
    """
    kept: list[dict[str, Any]] = []
    refused: list[str] = []
    for thing in things:
        name = str(thing.get("name") or "")
        if name and names_a_person(name, person):
            refused.append(str(thing.get("id") or ""))
            kept.append({**thing, "name": "", "nameRefused": True})
        else:
            kept.append({**thing, "nameRefused": False})
    return kept, refused


def refused_ids(things: list[dict[str, Any]] | None) -> set[str]:
    """Which things had their name refused, as the last answer was screened."""
    return {
        str(thing.get("id") or "")
        for thing in things or ()
        if isinstance(thing, dict) and thing.get("nameRefused")
    }


def save_jobs(path: Path, things: list[dict[str, Any]]) -> None:
    """Keep the assignment beside the rhythm, atomically."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps({"things": things}), encoding="utf-8")
    temporary.replace(path)


def load_jobs(path: Path) -> list[dict[str, Any]] | None:
    """The last assignment the panel gave us, or None if there is no usable copy.

    None is not an error. It is the state of a hub that has never reached the panel, and
    the callers treat it as "carry on as before" rather than "nothing has a job" — which
    is what keeps an unreachable panel from stopping the house.
    """
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    things = saved.get("things")
    return things if isinstance(things, list) else None


def holders(things: list[dict[str, Any]] | None, job: str) -> list[dict[str, Any]]:
    """Everything that holds this job. A job may be held by several things at once.

    Sorted by id so that a caller picking between them starts from a stable order and a
    random choice is the only thing that varies.
    """
    found = [thing for thing in things or () if isinstance(thing, dict) and job in _jobs(thing)]
    return sorted(found, key=lambda thing: str(thing.get("id") or ""))


def jobs_of(things: list[dict[str, Any]] | None, thing_id: str) -> tuple[str, ...] | None:
    """What this thing is for: its jobs, an empty tuple for none, or None if it is not on
    the list.

    The three answers are different. Not on the list means the panel has never mentioned
    it, and the caller must carry on as it did before rather than treat it as unassigned.
    """
    for thing in things or ():
        if isinstance(thing, dict) and thing.get("id") == thing_id:
            return _jobs(thing)
    return None


def _jobs(thing: dict[str, Any]) -> tuple[str, ...]:
    """The jobs on one cached row, whichever way the panel spelled them.

    A cache written before 19 August 2026 carries a single `job`. Reading both means the
    hub can be updated before the panel without a house in between where nothing holds
    anything — which would put an id card on every display.
    """
    stored = thing.get("jobs")
    if isinstance(stored, list):
        return tuple(str(job) for job in stored if str(job))
    single = str(thing.get("job") or "")
    return (single,) if single else ()
