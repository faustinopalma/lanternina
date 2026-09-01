"""Which subject each display gets, when there is more than one display.

Two frames in the same room showing the same thing is the failure this guards against,
and a frame that keeps landing on the same subject is the other. Both come out of one
rule, so both are tested against the same simulated house rather than against the rule
stated twice.
"""

from __future__ import annotations

from panel.painting import FALLBACK_THEMES, choose_theme
from panel.pictures import PictureRecord, last_used, on_other_displays

THEMES = ["animali del bosco", "il sistema solare", "fiori di campo"]


def _record(theme: str, display: str, at: float, kind: str = "ok") -> PictureRecord:
    return PictureRecord(
        id=f"pic-{display}-{at:g}",
        household_id="h1",
        theme=theme,
        created_at=at,
        kind=kind,
        display=display,
    )


def _next(shown: list[PictureRecord], display: str) -> str:
    return choose_theme(
        list(THEMES),
        elsewhere=on_other_displays(shown, display),
        last_used=last_used(shown),
    )


def test_two_displays_never_hold_the_same_subject() -> None:
    shown: list[PictureRecord] = []
    wall: dict[str, str] = {}
    for clock, display in enumerate(["A", "B"] * 6, start=1):
        chosen = _next(shown, display)
        shown.append(_record(chosen, display, float(clock)))
        wall[display] = chosen
        assert len(set(wall.values())) == len(wall), wall


def test_three_displays_use_all_three_subjects() -> None:
    shown: list[PictureRecord] = []
    for clock, display in enumerate(["A", "B", "C"], start=1):
        shown.append(_record(_next(shown, display), display, float(clock)))
    assert {record.theme for record in shown} == set(THEMES)


def test_a_fourth_display_repeats_the_subject_painted_longest_ago() -> None:
    """With fewer subjects than displays something has to repeat, and which one it is is
    the only choice left: the one nobody has looked at for longest."""
    shown = [
        _record(THEMES[0], "A", 1.0),
        _record(THEMES[1], "B", 2.0),
        _record(THEMES[2], "C", 3.0),
    ]
    assert _next(shown, "D") == THEMES[0]


def test_one_display_goes_through_every_subject_before_any_comes_back() -> None:
    shown: list[PictureRecord] = []
    seen: list[str] = []
    for clock in range(1, 7):
        chosen = _next(shown, "A")
        shown.append(_record(chosen, "A", float(clock)))
        seen.append(chosen)
    assert set(seen[:3]) == set(THEMES)
    assert set(seen[3:]) == set(THEMES)


def test_a_battery_notice_is_not_a_subject() -> None:
    """What a notice covers is what that display will go back to, so it is what counts."""
    shown = [_record(THEMES[0], "B", 1.0), _record("", "B", 2.0, kind="low")]
    assert on_other_displays(shown, "A") == [THEMES[0]]


def test_a_row_that_names_no_display_says_nothing_about_any() -> None:
    """Every row written before 1 September 2026 is one of these."""
    assert on_other_displays([_record(THEMES[0], "", 1.0)], "A") == []


def test_a_house_with_no_subjects_yet_still_gets_a_picture() -> None:
    assert choose_theme([]) in FALLBACK_THEMES
