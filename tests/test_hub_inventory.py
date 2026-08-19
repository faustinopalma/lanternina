"""The hub's side of the inventory: what it finds, what it remembers, what it refuses.

Three properties are worth pinning here, and each of them has already cost something.

Finding nothing is not finding an empty house. The first mDNS query after a quiet spell
has returned `SANE offers []` and then found the same scanner a minute later. A caller that
read that as "the list is now empty" would take the printer off the panel every night.

A person's name must not reach a model. This is the only side that knows the name, so it is
the only side that can refuse "la stampante di Sofia" — which is exactly what somebody
would write.

An unreachable panel leaves the house working. There are three answers to "what is this
display for", not two: a job, no job, and never mentioned. The third has to keep the house
behaving as it did, or a hub that cannot reach the panel turns every screen into an id card.
"""

from __future__ import annotations

import json
from pathlib import Path

from devices.inventory import (
    Found,
    holder,
    job_of,
    load_jobs,
    names_a_person,
    parse_browse,
    refused_ids,
    save_jobs,
    screen_names,
)

# One resolved record as `avahi-browse -rpt _ipp._tcp` writes it, from the printer in the
# house on 4 August 2026. The address in it moved to 192.168.0.5 a fortnight later, which
# is why the hostname and not the address is the key.
PRINTER_LINE = (
    "=;eth0;IPv4;EPSOND59029;_ipp._tcp;local;EPSOND59029.local;192.168.0.138;631;"
    '"txtvers=1" "ty=EPSON ET-2870 Series" "rp=ipp/print" "mopria-certified=2.1"'
)
ANNOUNCED_ONLY = "+;eth0;IPv4;EPSOND59029;_ipp._tcp;local"


def test_a_resolved_service_becomes_a_row_keyed_on_its_name() -> None:
    found = parse_browse(PRINTER_LINE, "printer")

    assert len(found) == 1
    assert found[0].id == "EPSOND59029.local"
    assert found[0].kind == "printer"
    assert found[0].model == "EPSON ET-2870 Series"
    assert found[0].address == "192.168.0.138"


def test_the_same_thing_on_two_interfaces_is_one_thing() -> None:
    wireless = PRINTER_LINE.replace(";eth0;", ";wlan0;")
    assert len(parse_browse(f"{PRINTER_LINE}\n{wireless}", "printer")) == 1


def test_an_announcement_without_an_address_is_not_a_row() -> None:
    """A `+` line says a service exists and gives no way to reach it. A row built from one
    would be a thing the house cannot use, indistinguishable from one it can."""
    assert parse_browse(ANNOUNCED_ONLY, "printer") == []


def test_a_semicolon_in_a_name_does_not_split_the_record() -> None:
    line = PRINTER_LINE.replace("EPSOND59029;_ipp", "EPSON\\;D59029;_ipp")
    found = parse_browse(line, "printer")
    assert len(found) == 1
    assert found[0].label == "EPSON;D59029"


def test_finding_nothing_says_nothing_about_the_house() -> None:
    """The whole point: an empty answer is a fact about this query, not about the house.
    Nothing downstream may remove a row, so there is no path from here to a shorter list."""
    assert parse_browse("", "printer") == []


def test_a_name_carrying_a_persons_name_is_refused() -> None:
    things = [
        {"id": "p1", "name": "la stampante di Sofia", "job": "print"},
        {"id": "p2", "name": "la stampante di sotto", "job": ""},
    ]

    kept, refused = screen_names(things, "Sofia")

    assert refused == ["p1"]
    assert kept[0]["name"] == ""
    # Blanked, not merely marked: a name still in the cache is a name something can reach.
    assert kept[0]["nameRefused"] is True
    assert kept[0]["job"] == "print"
    assert kept[1]["name"] == "la stampante di sotto"
    assert kept[1]["nameRefused"] is False


def test_the_refusal_survives_to_the_next_report() -> None:
    kept, _ = screen_names([{"id": "p1", "name": "Sofia", "job": ""}], "Sofia")
    assert refused_ids(kept) == {"p1"}


def test_a_name_is_matched_however_it_is_written() -> None:
    """Case, accents and word boundaries are all ways the same mistake gets through. The
    boundary one matters most: `sofiaprinter` is what a check on whole words would allow."""
    for written in ("SOFIA", "sofía", "sofiaprinter", "quadro-Sofia-2"):
        assert names_a_person(written, "Sofia Rossi"), written


def test_a_name_that_merely_contains_short_letters_is_left_alone() -> None:
    """A person's initial or a two-letter part would refuse half of what a parent might
    reasonably write, so only parts long enough to be distinctive are matched."""
    assert not names_a_person("la stampante di sotto", "Sofia Rossi")
    assert not names_a_person("il quadro grande", "Ada")
    assert names_a_person("il quadro di Ada", "Ada")


def test_with_nobody_named_nothing_is_refused() -> None:
    """A hub whose environment does not name anybody must not start refusing names it has
    no reason to refuse."""
    kept, refused = screen_names([{"id": "p1", "name": "Sofia", "job": ""}], "")
    assert refused == []
    assert kept[0]["name"] == "Sofia"


def test_the_cache_survives_a_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "jobs.json"
    things = [{"id": "94:A9:90:CF:7D:04", "label": "CF7D04", "job": "picture", "name": "il quadro"}]

    save_jobs(path, things)

    assert load_jobs(path) == things
    assert holder(load_jobs(path), "picture") == things[0]
    assert holder(load_jobs(path), "sheet") is None


def test_an_unusable_cache_reads_as_never_answered(tmp_path: Path) -> None:
    """None and [] are different answers. None means the panel has never been reached, and
    the house then carries on as before rather than deciding nothing has a job."""
    missing = tmp_path / "absent.json"
    assert load_jobs(missing) is None

    half_written = tmp_path / "half.json"
    half_written.write_text('{"things": [{"id": "a"', encoding="utf-8")
    assert load_jobs(half_written) is None

    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps({"things": []}), encoding="utf-8")
    assert load_jobs(empty) == []


def test_three_answers_to_what_a_display_is_for() -> None:
    things = [{"id": "known", "job": "picture"}, {"id": "idle", "job": ""}]

    assert job_of(things, "known") == "picture"
    assert job_of(things, "idle") == ""
    assert job_of(things, "stranger") is None
    assert job_of(None, "known") is None


def test_what_is_reported_upward_carries_no_address_as_its_identity() -> None:
    thing = Found(
        id="EPSOND59029.local", kind="printer", label="EPSOND59029", address="192.168.0.5"
    )

    reported = thing.reported(1_755_600_000.0)

    assert reported["id"] == "EPSOND59029.local"
    assert reported["address"] == "192.168.0.5"
