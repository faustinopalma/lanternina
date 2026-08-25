"""What the deviser copies out of a model's answer.

`experience_in` builds the document field by field rather than passing the model's object
through, and that is right — a field nobody asked for cannot arrive that way. The cost is
that a field added to the format and not added here is dropped in silence, which is what
happened to `themes` and `strategy`: ten runs against the real service came back with the
strategy empty and nothing said so.

So this walks the format's own fields and asserts each one survives.
"""

from __future__ import annotations

import json

from agents.experience_deviser import experience_in
from tests import afternoons as a


def test_every_field_the_model_writes_survives_the_parse() -> None:
    said = dict(a.an_afternoon())
    said["themes"] = ["un registro", "pesi impossibili"]
    said["strategy"] = "THE WORLD. Un ufficio pesi e misure.\nTHE QUESTION. Chi ha firmato."
    for ours in ("format_version", "experience_id", "requires"):
        said.pop(ours, None)

    got = experience_in(json.dumps(said))

    assert got.themes == ("un registro", "pesi impossibili")
    assert got.strategy.startswith("THE WORLD.")
    assert got.title == said["title"]
    assert got.overview == said["overview"]
    assert got.minutes == said["minutes"]


def test_a_field_the_model_did_not_write_is_simply_absent() -> None:
    """A document with no strategy still runs: the moments were always a whole plan."""
    said = dict(a.an_afternoon())
    for ours in ("format_version", "experience_id", "requires"):
        said.pop(ours, None)

    got = experience_in(json.dumps(said))

    assert got.themes == ()
    assert got.strategy == ""


def test_what_the_model_may_not_write_is_not_taken_from_it() -> None:
    """The id, the format version and what the house needs are ours."""
    said = dict(a.an_afternoon())
    said["experience_id"] = "not-yours"
    said["format_version"] = 99
    said["requires"] = ["photograph_table"]

    got = experience_in(json.dumps(said), experience_id="aftn-1234")

    assert got.experience_id == "aftn-1234"
    assert "photograph_table" not in {str(one) for one in got.requires}
