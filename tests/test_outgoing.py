"""The filter every word passes on its way to a display or a printer.

Two halves, and the second is the one that is easy to leave out. The first is that a text
that should not go out does not. The second is that something goes out anyway — the
pre-written text from the plan — because a filter that can leave a display blank has
replaced one failure with a worse one.

The counter is tested as a measuring instrument rather than as bookkeeping: `ideas/09 §7`
says a slot refused often is a defect in the devising prompt, and a count nobody can read
off cannot say that.
"""

from __future__ import annotations

from orchestrator.outgoing import Outgoing, why_not
from shared.experience import MAX_HEADING, MAX_LINE


def test_an_ordinary_line_goes_out_as_it_was_written() -> None:
    said = Outgoing()

    assert said.line("uno", "Guarda il cielo.", written="Guarda fuori.") == "Guarda il cielo."
    assert said.refusals == {}


def test_praise_is_replaced_by_the_text_the_plan_already_carried() -> None:
    """The fallback is why the written texts are mandatory in the first place."""
    said = Outgoing()

    out = said.line("uno", "Bravo, hai finito.", written="Il foglio resta lì.")

    assert out == "Il foglio resta lì."
    assert said.refusals["uno"] == 1


def test_a_line_that_names_the_machinery_does_not_go_out() -> None:
    """`ideas/09 §8`: nothing generated may carry a trace of the parent's channel."""
    said = Outgoing()

    out = said.line("due", "Ho accorciato il pomeriggio.", written="Ne resta uno.")

    assert out == "Ne resta uno."
    assert "accorciato" in said.reasons[0].why


def test_a_line_too_long_for_the_screen_does_not_go_out() -> None:
    said = Outgoing()

    out = said.line("tre", "a" * (MAX_LINE + 1), written="Va bene.")

    assert out == "Va bene."
    assert f"the limit is {MAX_LINE}" in said.reasons[0].why


def test_a_heading_is_held_to_the_shorter_limit() -> None:
    said = Outgoing()
    long_enough_for_a_line = "a" * (MAX_HEADING + 1)

    assert said.heading("uno", long_enough_for_a_line, written="Ciao") == "Ciao"
    assert said.line("due", long_enough_for_a_line, written="Ciao") == long_enough_for_a_line


def test_a_screenful_is_refused_as_one_thing() -> None:
    """Half a screenful reads as if a sentence went missing, which is the seam this whole
    design is trying not to show."""
    said = Outgoing()
    written = ("Il foglio resta lì.",)

    out = said.lines("uno", ("Guarda il cielo.", "Bravo."), written=written)

    assert out == written
    assert "line 2" in said.reasons[0].why


def test_a_screenful_with_nothing_in_it_falls_back_too() -> None:
    said = Outgoing()

    assert said.lines("uno", (), written=("Va bene.",)) == ("Va bene.",)
    assert said.refusals["uno"] == 1


def test_the_tally_names_the_slots_that_were_refused_most() -> None:
    """A slot refused often is a defect in the devising prompt, not a case to handle."""
    said = Outgoing()
    for _ in range(3):
        said.line("il-finale", "Bravo.", written="Va bene.")
    said.line("l-inizio", "Bravo.", written="Va bene.")

    assert said.tally().startswith("texts refused, by slot: il-finale 3")


def test_a_run_with_nothing_refused_says_nothing() -> None:
    """A journal line every afternoon is a journal line nobody reads."""
    assert Outgoing().tally() == ""


def test_the_reason_is_the_first_one_that_applies_and_costs_least() -> None:
    assert why_not("", limit=MAX_LINE) == "it says nothing"
    assert "the limit is" in why_not("a" * 200, limit=MAX_LINE)
    assert "bravo" in why_not("Bravo.", limit=MAX_LINE)
    assert why_not("Guarda il cielo.", limit=MAX_LINE) == ""
