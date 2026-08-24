"""The checks that refuse an afternoon before it is saved, one test per check.

Each of these is written the way round that matters: it takes a document that passes
everything, breaks exactly one thing, and asserts the refusal. A test that only shows a
good plan passing would go on passing if the check were deleted, and a check nobody would
notice the absence of is not a check.

The split between this file and `test_experience.py` follows the split in the code. The
parser raises on a shape it cannot read, and those refusals are tested there. These are
properties of a whole document that reads perfectly — and they come back as a list, because
what is done with them is a repair request naming the fields that failed.
"""

from __future__ import annotations

from typing import Any

import afternoons as a
import pytest

from shared.blocklist import Why, blocked_in
from shared.experience import Continuation, Drawn, Experience, ExperienceError
from shared.experience_checks import (
    check,
    no_placeholder_is_left,
    not_the_same_afternoon_again,
    nothing_from_the_block_list,
    the_ending_is_written_down,
    the_short_version_fits,
    the_way_out_starts_from_something,
)


def an_experience(**changed: Any) -> Experience:
    return Experience.from_dict(a.an_afternoon(**changed))


def where(complaints: tuple[Any, ...]) -> list[str]:
    return [complaint.where for complaint in complaints]


def test_an_afternoon_that_is_right_has_nothing_wrong_with_it() -> None:
    """The floor under every other test here: a clean document produces no complaint."""
    assert check(an_experience()) == ()


# ── The way out starts from something already in hand ────────────────────────────────


def test_a_way_out_that_reaches_for_an_object_nobody_was_given_is_refused() -> None:
    """The recurring defect of a generated plan, and the reason the check exists.

    The parser already makes a way out name its own object, so a model can satisfy that by
    inventing one in the last sentence. This is what stops that: the object has to have
    been mentioned earlier, on a display or on a page.
    """
    moments = a.moments()
    moments[0]["way_out"] = a.way_out(in_hand="la chiave di ottone")

    complaints = the_way_out_starts_from_something(
        Experience.from_dict(a.an_afternoon(moments=moments)).moments
    )

    assert where(complaints) == ["moments[0].way_out.in_hand"]
    assert "goodbye that is felt as a cut" in complaints[0].says


def test_a_way_out_may_name_something_an_earlier_moment_mentioned() -> None:
    """Earlier, not only here: the object stays in hand across the moments after it."""
    moments = a.moments()
    moments[0]["weights"] = a.weights(lines=("Prendi la chiave di ottone.",))
    moments[0]["way_out"] = a.way_out(in_hand="la chiave di ottone")
    moments[2]["way_out"] = a.way_out(in_hand="la chiave di ottone")

    assert the_way_out_starts_from_something(
        Experience.from_dict(a.an_afternoon(moments=moments)).moments
    ) == ()


def test_a_way_out_can_start_from_something_printed_on_the_page() -> None:
    """A page is a surface somebody reads, so what it says counts as having been said."""
    moments = a.moments()
    moments[2]["way_out"] = a.way_out(in_hand="pioggia")

    assert the_way_out_starts_from_something(
        Experience.from_dict(a.an_afternoon(moments=moments)).moments
    ) == ()


def test_a_moment_with_no_way_out_at_all_never_gets_as_far_as_the_check() -> None:
    """The plan that cannot be shortened, refused one layer earlier and just as hard."""
    moments = a.moments()
    del moments[1]["way_out"]

    with pytest.raises(ExperienceError, match="no way out"):
        an_experience(moments=moments)


def test_a_way_out_longer_than_twenty_minutes_is_not_a_way_out() -> None:
    moments = a.moments()
    moments[1]["way_out"] = a.way_out(minutes=25)

    with pytest.raises(ExperienceError, match="must be 1 to 20"):
        an_experience(moments=moments)


# ── The short version fits the window ────────────────────────────────────────────────


def test_a_plan_whose_shortest_form_does_not_fit_is_refused() -> None:
    """There is nothing left to shorten, so it was never going to fit any way it ran."""
    moments = a.moments()
    for moment in moments:
        moment["weights"] = a.weights(50, 55, 60)

    complaints = the_short_version_fits(
        Experience.from_dict(a.an_afternoon(moments=moments, minutes=60))
    )

    assert where(complaints) == ["minutes"]
    assert "nothing left to shorten" in complaints[0].says


def test_it_measures_the_longest_path_and_not_the_sum_of_the_branches() -> None:
    """Branches are alternatives. Adding them together refuses documents that run fine."""
    moments = [
        a.say(weights=a.weights(10, 15, 20)),
        a.hand_over(weights=a.weights(10, 15, 20)),
        a.collect(on_marks="chiude-lungo", on_blank="fine", if_no_page="fine",
                  weights=a.weights(10, 15, 20)),
        a.close(moment_id="chiude-lungo", heading="Basta", weights=a.weights(40, 45, 50)),
        a.close(weights=a.weights(40, 45, 50)),
    ]

    # Every moment added together is 110 minutes. The longest single path is 70: three
    # moments of ten, and then one close or the other.
    assert the_short_version_fits(
        Experience.from_dict(a.an_afternoon(moments=moments, minutes=75))
    ) == ()


# ── An ending somebody wrote ─────────────────────────────────────────────────────────


def test_an_afternoon_whose_only_ending_is_unwritten_is_refused() -> None:
    """Every branch says ask, so what the parent reads is a beginning."""
    moments = [a.say(), a.hand_over(), a.collect(on_marks="ask", on_blank="ask", if_no_page="ask")]

    complaints = the_ending_is_written_down(
        Experience.from_dict(
            a.an_afternoon(moments=moments, requires=["print_a4", "scan_a4", "show_800x480_1bit"])
        ).moments
    )

    assert where(complaints) == ["moments"]
    assert "no ending in what the parent reads" in complaints[0].says


def test_a_branch_cannot_be_written_that_strands() -> None:
    """There is no check for stranding, and this is the argument that there need not be.

    Edges only ever point forward, so every path arrives at the last moment; and the last
    moment closes, or is a collect whose branches can only say ``ask``. Both are refusals
    the parser already makes. A moment that is reached and then never reaches an ending is
    therefore not something this format can express — which is why the walk that would have
    proved it was taken out rather than left in as a check nobody can fail.

    What is left over is the plan whose every ending is unwritten, and
    :func:`the_ending_is_written_down` is what refuses that.
    """
    trails_off = [
        a.say(),
        a.hand_over(),
        a.collect(on_marks="e-poi", on_blank="e-poi", if_no_page="e-poi"),
        a.say(moment_id="e-poi", heading="E poi"),
    ]
    with pytest.raises(ExperienceError, match="trails off"):
        an_experience(moments=trails_off)

    with pytest.raises(ExperienceError, match="a loop is a program"):
        an_experience(moments=a.moments(on_marks="inizio"))


# ── Nothing from the block list ──────────────────────────────────────────────────────


def test_praise_in_a_line_of_a_weight_is_refused() -> None:
    moments = a.moments()
    moments[3]["weights"] = a.weights(lines=("Bravo, il foglio è finito.",))

    complaints = nothing_from_the_block_list(
        Experience.from_dict(a.an_afternoon(moments=moments))
    )

    assert where(complaints) == ["moments[3]"]
    assert "bravo" in complaints[0].says


def test_a_word_about_the_machinery_in_a_rung_of_help_is_refused() -> None:
    """`ideas/09 §8`: nothing generated may carry a trace of the parent's channel."""
    moments = a.moments()
    moments[0]["help"] = [
        {"after_minutes": 3, "lines": ["Il foglio è lì."]},
        {"after_minutes": 6, "lines": ["Ho accorciato il pomeriggio."]},
        {"after_minutes": 10, "lines": ["Il foglio è lì."]},
        {"after_minutes": 15, "lines": ["Il foglio è lì."]},
    ]

    complaints = nothing_from_the_block_list(
        Experience.from_dict(a.an_afternoon(moments=moments))
    )

    assert where(complaints) == ["moments[0]"]
    assert "accorciato" in complaints[0].says


def test_the_overview_the_parent_reads_is_on_the_same_list() -> None:
    complaints = nothing_from_the_block_list(
        an_experience(overview="Un pomeriggio con un punteggio alla fine.")
    )

    assert where(complaints) == ["overview"]


def test_the_block_list_says_which_of_the_five_reasons_it_is() -> None:
    """The reason travels with the phrase, because a repair prompt has to explain itself."""
    assert {found.why for found in blocked_in("bravo")} == {Why.PRAISE}
    assert {found.why for found in blocked_in("hai perso")} == {Why.SCORE}
    assert {found.why for found in blocked_in("sbrigati")} == {Why.HURRY}
    assert {found.why for found in blocked_in("hai sbagliato")} >= {Why.BLAME}
    assert {found.why for found in blocked_in("il sistema ha deciso")} == {Why.MACHINERY}


def test_the_block_list_folds_accents_and_case_away() -> None:
    """A model that drops an accent must not slip through a list that was written with one."""
    assert blocked_in("Chiedi a papà")
    assert blocked_in("CHIEDI A PAPA")


def test_an_ordinary_afternoon_says_nothing_off_the_list() -> None:
    """The other half of a block list: what it costs when it is wrong."""
    assert blocked_in("Guarda il cielo e disegna quello che vedi.") == ()


# ── Nothing left to decide ───────────────────────────────────────────────────────────


def test_a_bracketed_blank_that_would_go_on_the_display_is_refused() -> None:
    """It reads as a finished document and the fourth moment says `[nome dell'oggetto]`."""
    moments = a.moments()
    moments[0]["weights"] = a.weights(lines=("Prendi [nome dell'oggetto].",))

    complaints = no_placeholder_is_left(
        Experience.from_dict(a.an_afternoon(moments=moments))
    )

    assert where(complaints) == ["moments[0]"]
    assert "square brackets" in complaints[0].says


def test_two_options_with_a_slash_between_them_are_still_a_decision() -> None:
    complaints = no_placeholder_is_left(an_experience(title="Un pomeriggio rosso / blu"))

    assert where(complaints) == ["title"]


def test_an_ellipsis_is_ordinary_italian_and_is_not_a_placeholder() -> None:
    """The cost of the check, bounded where it would bite: a real page prints one."""
    moments = a.moments()
    moments[0]["weights"] = a.weights(lines=("Le nuvole di oggi sono...",))

    assert no_placeholder_is_left(Experience.from_dict(a.an_afternoon(moments=moments))) == ()


# ── Not the same afternoon again ─────────────────────────────────────────────────────


def test_three_of_the_ten_dimensions_shared_with_a_recent_one_is_refused() -> None:
    before = Drawn.from_dict(a.drawn())
    now = Drawn.from_dict(a.drawn(frame="un balcone", role="chi guarda", mechanic="ascoltare"))

    complaints = not_the_same_afternoon_again(now, [before])

    assert where(complaints) == ["drawn"]
    assert "7 of the ten dimensions" in complaints[0].says


def test_two_shared_dimensions_are_a_coincidence_and_are_allowed() -> None:
    before = Drawn.from_dict(a.drawn())
    now = Drawn.from_dict(
        a.drawn(
            frame="un balcone",
            role="chi guarda",
            mechanic="ascoltare",
            progress="a domande",
            paper="una mappa",
            glass="niente",
            displays="il tempo che passa",
            camera="una foto del tavolo",
        )
    )

    assert not_the_same_afternoon_again(now, [before]) == ()


def test_the_first_afternoon_a_house_ever_gets_is_compared_with_nothing() -> None:
    assert not_the_same_afternoon_again(Drawn.from_dict(a.drawn()), []) == ()


def test_an_afternoon_that_says_nothing_about_how_it_was_drawn_is_refused() -> None:
    """Variety from a seed cannot be checked. Ten written phrases can."""
    with pytest.raises(ExperienceError, match="which ten dimensions"):
        an_experience(drawn=None)


def test_a_dimension_left_blank_is_refused() -> None:
    with pytest.raises(ExperienceError, match="were not drawn"):
        an_experience(drawn=a.drawn(camera=""))


# ── A continuation is held to the same list ──────────────────────────────────────────


def test_the_half_nobody_approved_passes_the_same_checks() -> None:
    """The parent read an overview and not this, so this is where the checks earn most."""
    moments = [a.say(moment_id="ancora", heading="Ancora una cosa"), a.close()]
    moments[0]["weights"] = a.weights(lines=("Ottimo lavoro, il foglio è finito.",))

    complaints = check(Continuation.from_dict(a.a_continuation(moments=moments)))

    assert where(complaints) == ["moments[0]"]


def test_a_continuation_is_not_measured_against_a_window_it_does_not_have() -> None:
    """It carries no minutes, and inventing one to check against would be arithmetic."""
    assert check(Continuation.from_dict(a.a_continuation())) == ()
