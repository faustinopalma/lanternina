"""The sheet layer has an ending, so a display that showed an afternoon goes back to its
picture.

Found in the house twice. On 24 August 2026 both displays had been showing the words of a
moment for three days. On 25 August it happened again from a two-minute afternoon: the
activity ended at 13:39 and by 15:16 the screens had not moved, while the picture layer
underneath had been repainted at 15:02 and 15:16 and nobody could see it.

The cause is an ordering with no ending in it: `current_screen` serves remind, then sheet,
then picture, and the sheet layer was a file that nothing ever removed. The picture layer
was given an ending on 20 August for the same reason and the sheet layer was not.

What is pinned here is the property, not the mechanism: after an afternoon reaches its
ending the display comes back on its own, and it does not come back so fast that nobody
reads the ending.
"""

from __future__ import annotations

from pathlib import Path

from devices.house import SHEET_LAYER_MINUTES, House, show, the_sheet_layer_is_done
from devices.trmnl_byos import sheet_layer_is_over, sheet_layer_until

WHEN = 1_756_000_000.0


def a_house(tmp_path: Path) -> House:
    screen = tmp_path / "screen-CF7D04.bmp"
    return House(screen=screen, sheets_dir=tmp_path / "sheets")


def test_a_house_that_never_ran_an_afternoon_serves_its_sheet_layer(tmp_path: Path) -> None:
    """No marker is not an expired marker: a display must not start out suppressed."""
    assert sheet_layer_is_over(tmp_path / "screen.bmp", WHEN) is False


def test_the_ending_stays_up_and_then_the_display_comes_back(tmp_path: Path) -> None:
    house = a_house(tmp_path)
    the_sheet_layer_is_done(house, WHEN)

    shared = tmp_path / "screen.bmp"
    # Somebody in another room still finds the ending.
    assert sheet_layer_is_over(shared, WHEN + 60.0) is False
    assert sheet_layer_is_over(shared, WHEN + (SHEET_LAYER_MINUTES - 1) * 60.0) is False
    # And then the wall stops being a museum.
    assert sheet_layer_is_over(shared, WHEN + SHEET_LAYER_MINUTES * 60.0) is True


def test_one_marker_covers_every_display_that_held_the_job(tmp_path: Path) -> None:
    """A run's moments land on whichever display the process picked, so clearing only
    the last one used would leave the others showing an afternoon that is over."""
    the_sheet_layer_is_done(a_house(tmp_path), WHEN)

    for label in ("CF7D04", "FB9F18"):
        assert sheet_layer_is_over(tmp_path / f"screen-{label}.bmp", WHEN + 3600.0) is True


def test_writing_the_sheet_layer_makes_it_current_again(tmp_path: Path) -> None:
    """Otherwise the next afternoon would be suppressed by the last one's ending."""
    house = a_house(tmp_path)
    the_sheet_layer_is_done(house, WHEN)
    assert sheet_layer_until(tmp_path / "screen.bmp").exists()

    show(house, "Una cosa", ["e poi un'altra"])

    assert sheet_layer_is_over(tmp_path / "screen.bmp", WHEN + 3600.0) is False


def test_an_unreadable_marker_does_not_blank_a_display(tmp_path: Path) -> None:
    """Failing toward "keep showing something" rather than toward "show nothing"."""
    sheet_layer_until(tmp_path / "screen.bmp").write_text("not a time", encoding="utf-8")

    assert sheet_layer_is_over(tmp_path / "screen.bmp", WHEN) is False
