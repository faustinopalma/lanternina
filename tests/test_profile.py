"""Where an afternoon is pitched, and the two halves that work it out.

`docs/NON-GOALS.md`, 4 September 2026: a profile is kept, it reaches the two models that
write an afternoon, and it reaches nothing a person can read. These are the guarantees for
the first half of that sentence. The second half is in `test_boundaries.py` and in the
block-list tests below.

Every one of these was mutation-checked: the code was broken and the test was watched to
fail. The three that matter are named in their own docstrings, because a test that has
never been red is a test nobody has evidence for.
"""

from __future__ import annotations

from pathlib import Path

from shared.blocklist import Why, blocked_in
from shared.profile import (
    ENOUGH_TO_LEAN_ON,
    HIGHEST,
    LOWEST,
    PITCHES,
    WEIGHED,
    Axis,
    Band,
    Noticed,
    Profile,
    Ran,
    read_from,
)


def placed(*values: int) -> list[Noticed]:
    return [Noticed(at=float(n), where={Axis.LOAD: v, Axis.INK: v}) for n, v in enumerate(values)]


def test_a_house_with_too_little_behind_it_is_pitched_at_nothing() -> None:
    """Two afternoons that went badly are a fortnight, not a level.

    The deviser writes better with no sentence than with a wrong one, and the empty string
    is what leaves the block out of the prompt altogether — so this is also the guarantee
    that a brand new house gets a model inventing freely.
    """
    assert read_from().as_material() == ""
    assert not read_from(placed(1, 1)).knows_anything()
    assert read_from(placed(1, 1)).seen[Axis.LOAD] == 2

    leaning = read_from(placed(1, 1, 1))
    assert leaning.where[Axis.LOAD] is Band.LOW
    assert leaning.seen[Axis.LOAD] == ENOUGH_TO_LEAN_ON


def test_the_bands_are_the_scale_cut_in_three_and_not_three_chosen_numbers() -> None:
    """A house at the bottom of the scale is low, at the top is high, in between is middle."""
    assert read_from(placed(*([LOWEST] * 4))).where[Axis.LOAD] is Band.LOW
    assert read_from(placed(*([HIGHEST] * 4))).where[Axis.LOAD] is Band.HIGH
    assert read_from(placed(3, 3, 3, 3)).where[Axis.LOAD] is Band.MIDDLE


def test_one_page_cannot_move_a_house_across_a_band() -> None:
    """The window is the only damping there is, and this is the arithmetic that says so.

    The state is recomputed from the last few placements every time, with nothing carried
    over, so a single afternoon moves an axis by at most one part in the window. An
    afternoon somebody was ill during must not be able to walk a house down a band on its
    own — and hysteresis, which is the usual answer, cannot be checked by hand.
    """
    steady = placed(*([3] * WEIGHED))
    assert read_from(steady).where[Axis.LOAD] is Band.MIDDLE

    after_one_bad_day = read_from([*steady[1:], *placed(LOWEST)])
    assert after_one_bad_day.where[Axis.LOAD] is Band.MIDDLE


def test_a_sheet_that_never_came_back_is_not_a_sheet_that_came_back_blank() -> None:
    """Blank is an act: somebody carried the sheet to the glass. This is not.

    It reads as the bottom of the ink axis and says nothing about the other two, because a
    page nobody put on the glass cannot show how many things had to be held at once.
    """
    some_came_back = [
        *placed(HIGHEST, HIGHEST, HIGHEST),
        *[Noticed(at=9.0, came_back=False) for _ in range(3)],
    ]
    where = read_from(some_came_back)
    assert where.where[Axis.INK] is Band.MIDDLE, "three at the top and three at the bottom"
    assert where.where[Axis.LOAD] is Band.HIGH, "the missing sheets say nothing about load"
    assert where.seen[Axis.LOAD] == 3


def test_a_house_that_has_never_returned_a_sheet_is_not_walked_down_the_scale() -> None:
    """The one guard, and the reason it is here rather than in a comment.

    A sheet that never came back may mean what was asked was too much. It may equally mean
    the scanner is in another room, or unplugged, or that nobody has ever been shown where
    it is. Nothing in this system can tell those apart. Without this rule a house with a
    dead scanner is pitched at the bottom of every axis within a week and there is no
    symptom anybody could read.

    Broken to check: dropping the ``ever_came_back`` clause in `shared/profile._placed`
    makes this house sit at :attr:`Band.LOW` on ink with nothing behind it.
    """
    nothing_ever_returned = [Noticed(at=float(n), came_back=False) for n in range(6)]
    where = read_from(nothing_ever_returned)
    assert not where.knows_anything()
    assert where.seen[Axis.INK] == 0


def test_the_span_is_read_off_the_clock_and_never_off_a_page() -> None:
    """No page shows how long anybody sat, so this axis has no model in it at all.

    The numbers below are the arithmetic printed out rather than a guess at it. Of 120
    planned minutes: all of them and its own ending is 5; all of them ended by the clock is
    4; two thirds and its own ending is 4; two thirds ended by the clock is 3; a quarter is
    2 either way.

    So being brought to an end costs one point on the five and never a floor, which crosses
    a band in the middle of the range and not at the top. That is the intended shape: two
    hours spent is two hours spent, and an afternoon the clock finished is not the same
    thing as one abandoned after twenty minutes.
    """
    whole = [Ran(planned_minutes=120, minutes=120, carried_through=True)] * 3
    assert read_from(runs=whole).where[Axis.SPAN] is Band.HIGH

    barely = [Ran(planned_minutes=120, minutes=25, carried_through=False)] * 3
    assert read_from(runs=barely).where[Axis.SPAN] is Band.LOW

    most_of_it_then_the_clock = [
        Ran(planned_minutes=120, minutes=80, carried_through=False)
    ] * 3
    assert read_from(runs=most_of_it_then_the_clock).where[Axis.SPAN] is Band.MIDDLE

    most_of_it_and_its_own_ending = [
        Ran(planned_minutes=120, minutes=80, carried_through=True)
    ] * 3
    assert read_from(runs=most_of_it_and_its_own_ending).where[Axis.SPAN] is Band.HIGH

    unknown = [Ran(planned_minutes=0, minutes=90, carried_through=True)] * 3
    assert Axis.SPAN not in read_from(runs=unknown).where


def test_what_reaches_a_prompt_is_a_sentence_about_an_afternoon() -> None:
    """Not a number, not a band name, and not a noun phrase about a person.

    This is what makes the gate's job possible rather than merely stated. A prompt saying
    *this person holds two things at once* would produce, over enough afternoons, one that
    says so on a display; a prompt saying *two things that have to be put side by side*
    describes the material and has nothing to leak.
    """
    said = read_from(placed(*([HIGHEST] * 4)), [Ran(120, 120, True)] * 3).as_material()

    assert PITCHES[Axis.LOAD][Band.HIGH] in said
    assert PITCHES[Axis.SPAN][Band.HIGH] in said
    for shape_of_a_verdict in ("low", "middle", "high", "1", "2", "3", "4", "5"):
        assert shape_of_a_verdict not in said.split()


def test_the_pitch_is_never_a_field_on_anything_that_is_shown() -> None:
    """`Profile` has a `to_dict` for a store and no `to_public` for a panel.

    Every other record in `panel/` that a parent may read has one. The absence is the point:
    a route that wanted to show this would have to write the serialisation itself, which is
    a thing somebody has to decide to do rather than a thing that happens.
    """
    assert not hasattr(Profile(), "to_public")
    assert set(Profile().to_dict()) == {"where", "seen"}


def test_the_pitch_reaches_two_prompts_and_no_route_a_parent_can_call() -> None:
    """Structural, because the wording rule cannot be checked on text nobody has generated.

    `docs/NON-GOALS.md` allows the profile to reach the model that devises an afternoon and
    the model that runs one, and nothing else. Those are two call sites. Every other route
    in `panel/routes/` answers a browser or a house, so a third one reading the pitch is the
    shape of the leak this is written against — and it would be added by somebody being
    helpful rather than by somebody deciding.

    Broken to check: calling ``as_material()`` in any route that returns to a browser makes
    this red on the file that does it.
    """
    routes = Path(__file__).resolve().parents[1] / "panel" / "routes"
    reading_it = {
        path.name
        for path in routes.rglob("*.py")
        if "_pitch_for" in path.read_text(encoding="utf-8")
    }
    assert reading_it == {"experience.py"}

    # And in that file it is used twice: devising an afternoon, and continuing one.
    written = (routes / "experience.py").read_text(encoding="utf-8")
    assert written.count("_pitch_for(request, household_id)") == 2


def test_the_model_that_places_a_page_is_shown_nothing_that_could_confirm_a_state() -> None:
    """The split the parent asked for, checked on the text rather than promised in a comment.

    A model handed the current state and asked whether it still holds will agree with it,
    because agreeing with its context is what a model does, and a series of agreements is a
    state that stopped being measured after its first entry. So this prompt names one page
    and never a house, a history, a band or another afternoon.
    """
    from agents.page_judge import _INSTRUCTION

    said = _INSTRUCTION.lower()
    for absent in (
        "household",
        "house",
        "profile",
        "before",
        "usually",
        "last time",
        "previous",
        "band",
        "level",
    ):
        assert absent not in said, f"the page judge is told about {absent!r}"
    assert "span" not in said, "no page shows how long anybody sat"


# ── The gate ────────────────────────────────────────────────────────────────────────


def test_a_sentence_saying_the_afternoon_was_sized_for_the_reader_is_refused() -> None:
    """The whole reason the profile is allowed to exist, made mechanical.

    `docs/NON-GOALS.md` says the prompt asking for this is not the protection and the gate
    is. These are the sentences a model handed a pitch eventually writes, and every one of
    them tells the reader that a decision was taken about them behind the afternoon.

    Broken to check: removing the `Why.FITTED` block from `shared/blocklist._RULES` leaves
    all nine of these passing the gate.
    """
    fitted = [
        "Questa pagina è pensata apposta per te.",
        "Oggi è più facile del solito.",
        "L'ultima volta hai lasciato il foglio in bianco.",
        "Ormai lo sai, quindi si va avanti.",
        "Sei pronto per qualcosa di più lungo.",
        "Un compito adatto al tuo livello.",
        "This one is easier.",
        "Last time you left it blank.",
        "It was written just for you.",
    ]
    for said in fitted:
        found = blocked_in(said)
        assert found, f"{said!r} tells the reader the afternoon was sized for them"
        assert Why.FITTED in {one.why for one in found}


def test_the_gate_refuses_the_sizing_and_not_the_second_person() -> None:
    """The failure this family was written to avoid, and it is the module's own argument.

    Second person with a past tense is most of the dialogue in most fiction. A rule that
    caught it would take every character who speaks out of every afternoon, which is what
    the list of 78 literal phrases did to `errore`, `livello` and `mamma` before it was
    replaced by patterns carrying a person.
    """
    ordinary = [
        "Il capitano disse: hai la chiave, apri la porta.",
        "La scorsa volta il faro si spense alle nove.",
        "Ormai la marea saliva sopra il molo.",
        "Il pozzo era più profondo del fiume.",
        "Nel registro c'era un errore di trascrizione.",
        "Scrivi tre parole nella colonna di destra.",
        "La nonna scriveva a mano ogni domenica.",
        "Questa scatola è stata fatta per contenere sei uova.",
    ]
    for said in ordinary:
        assert not blocked_in(said), f"{said!r} is a sentence somebody meant to write"
