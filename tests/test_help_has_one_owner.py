"""Help has one owner, and the two timers do not race for it.

`offer_help` writes the run file: it advances `helped` and puts a rung on the display. Two
processes doing that in the same second read the same `helped`, show the same rung, and
both write — a lost update on the file that holds where somebody is in their afternoon.

That is what happened on 25 August 2026 at 13:38:04, on `aft_78a067a8`: two lines, one
from `lanternina-help.service` and one from `lanternina-afternoon.service`, both saying
`read-dossier rung 1`. It had been harmless while the afternoon timer ran every ten
minutes and the help timer every one; moving the afternoon timer to a minute so a parent's
press would be picked up made the two collide on every single run.

Both tests fail on the version where the full run also offers help.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devices import afternoon as clock

REPO = Path(__file__).resolve().parent.parent
UNITS = REPO / "deploy"


def _timer_seconds(name: str) -> int:
    text = (UNITS / f"{name}.timer").read_text(encoding="utf-8")
    found = re.search(r"OnCalendar=\*:(?:0/)?(\d+|\*):00", text)
    assert found, f"{name}.timer has no OnCalendar this test understands"
    return 60 if found.group(1) == "*" else int(found.group(1)) * 60


def test_only_the_help_run_offers_help() -> None:
    """Read off the source, because the two callers are two systemd units and no test can
    run both. What is checked is that `offer_help` is reached under `--only-help` and
    nowhere else in `main`."""
    source = (REPO / "devices" / "afternoon.py").read_text(encoding="utf-8")
    body = source[source.index("def main("):]
    calls = [line for line in body.splitlines() if "offer_help(" in line]

    assert len(calls) == 1, f"main calls offer_help {len(calls)} times: {calls}"
    before = body[: body.index("offer_help(")]
    assert "if args.only_help:" in before, (
        "offer_help is reached without --only-help, so the afternoon unit offers a rung "
        "the help unit is already offering"
    )


def test_the_two_units_would_otherwise_collide_every_run() -> None:
    """Why the guard above is needed rather than merely tidy: both timers fire a minute
    apart, so a second caller is a second caller on every run and not occasionally."""
    assert _timer_seconds("lanternina-help") == 60
    assert _timer_seconds("lanternina-afternoon") == 60


def test_the_help_run_still_gives_a_rung_and_touches_no_network(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The guard must not have turned help off, and the reason it stays on its own unit is
    that it reaches a display on a house that cannot reach the panel at all."""
    given: list[str] = []

    def _rung(house: object, now: float, *, send: bool) -> list[str]:
        given.append("rung")
        return ["aft_1 somewhere rung 1"]

    monkeypatch.setattr(clock, "offer_help", _rung)
    for reached in ("the_rhythm", "listen", "conclude_what_is_over", "the_standing_request"):
        monkeypatch.setattr(
            clock,
            reached,
            lambda *a, name=reached, **k: pytest.fail(f"--only-help reached {name}"),
        )
    monkeypatch.setenv("LANTERNINA_SHEETS_DIR", str(tmp_path))
    monkeypatch.setenv("LANTERNINA_PANEL_URL", "https://panel.invalid")
    monkeypatch.setenv("LANTERNINA_HOUSEHOLD", "hh_1")
    monkeypatch.setenv("LANTERNINA_DEVICE_KEY", "k")

    assert clock.main(["--only-help", "--no-paper"]) == 0
    assert given == ["rung"]
