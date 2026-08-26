"""What the panel says about itself, and what it must never say.

The second half is the one worth a test. A log line is read by whoever can reach the
workspace, which is a wider set than the people a household chose, so the vocabulary is ids,
counts, durations and outcomes — never a page that came back, never a reminder's words.
"""

from __future__ import annotations

import logging
from pathlib import Path

import panel.observability as watching


def test_logging_is_configured_so_a_written_line_is_not_dropped() -> None:
    """Every `logger.info` in the routes went nowhere until this ran, because nothing
    configured a handler. A refusal that explains a quiet afternoon is exactly the line
    that was being lost."""
    watching._started = False
    try:
        watching.watch()
        assert logging.getLogger().handlers
        assert logging.getLogger("panel.devising").isEnabledFor(logging.INFO)
    finally:
        watching._started = False


def test_the_transport_is_held_quiet() -> None:
    """The Azure SDKs log every request at INFO. Left alone that is thousands of lines an
    hour saying a token was fetched, against a workspace capped at a gigabyte a day."""
    watching._started = False
    try:
        watching.watch()
        for name in watching.NOISY:
            assert not logging.getLogger(name).isEnabledFor(logging.INFO), name
    finally:
        watching._started = False


def test_starting_twice_does_not_say_everything_twice() -> None:
    watching._started = False
    try:
        watching.watch()
        before = len(logging.getLogger().handlers)
        watching.watch()
        assert len(logging.getLogger().handlers) == before
    finally:
        watching._started = False


def test_no_hub_line_describes_what_somebody_did() -> None:
    """The two that did are named here, because both were shipped and both read as
    harmless. One said which cells came back written on; the other said what a household
    asked to be reminded of. A journal is read by whoever can reach the machine — and,
    once a hub ships its journal anywhere, by whoever can reach that.
    """
    forbidden = (
        "came.written",
        "came.same_sheet",
        "{words}",
        "reading",
        "came.cells",
    )
    said: list[str] = []
    for path in sorted(Path("devices").glob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped.startswith("print(") and "print(f" not in stripped:
                continue
            for word in forbidden:
                if word in stripped:
                    said.append(f"{path}:{number} {stripped}")

    assert said == []
