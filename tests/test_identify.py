"""Saying which display is which, and the only thing that can end it.

Two identical boxes on two walls and one row in the panel: the parent needs the box to say
which one it is. What makes this different from every other screen the house shows is how
it ends. Nothing the panel does can prove the right box was found — only somebody standing
in front of the right one, pressing its button, can. So the card stays up until that press,
and the press writes nothing down: a record of who pressed what and when is a log about a
person, and the way that stays untrue is that there is nowhere for it to go.
"""

from __future__ import annotations

import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from devices.push_status import REQUEST_IDENTIFY, label_of
from devices.trmnl_byos import (
    Config,
    identify_for,
    make_handler,
    register_device,
    screen_for,
)
from panel.requests import KIND_IDENTIFY, KINDS
from tools.make_trmnl_test_screen import make_screen

MAC = "94:A9:90:CF:7D:04"


def get(url: str, headers: dict[str, str] | None = None) -> bytes:
    with urllib.request.urlopen(
        urllib.request.Request(url, headers=headers or {}), timeout=10
    ) as answer:
        return bytes(answer.read())


def test_the_house_knows_the_kind_the_panel_writes() -> None:
    """Two files name it. A kind the panel accepts and the hub ignores is a button that
    does nothing, and nothing would say so."""
    assert REQUEST_IDENTIFY == KIND_IDENTIFY
    assert KIND_IDENTIFY in KINDS


def test_the_display_is_found_by_what_it_calls_itself() -> None:
    """The panel asks about a MAC; the screen files are named after the friendly id."""
    things = [{"id": MAC, "label": "CF7D04"}, {"id": "other", "label": "FB9F18"}]

    assert label_of(things, MAC) == "CF7D04"
    # Something this house has no screen for: the card goes up nowhere rather than
    # anywhere.
    assert label_of(things, "a-printer") == ""
    assert label_of(None, MAC) == ""


def test_the_card_outranks_the_job_and_the_press_gives_the_display_back(
    tmp_path: Path,
) -> None:
    """A display with a job would otherwise carry on showing it, and the parent standing
    at the wall would learn nothing. The press is the only way back, and what comes back
    is what was underneath: nobody kept a copy of it."""
    shared = tmp_path / "screen.bmp"
    make_screen(shared)
    registry = tmp_path / "devices.json"
    device = register_device(registry, MAC)
    own = screen_for(shared, device.friendly_id)
    make_screen(own)
    own.write_bytes(own.read_bytes()[:-2] + b"\x00\x00")

    httpd = ThreadingHTTPServer(
        ("127.0.0.1", 0), make_handler(Config("http://127.0.0.1", shared, registry))
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    screen = f"http://127.0.0.1:{httpd.server_port}/screen/{device.token}.bmp"
    display = f"http://127.0.0.1:{httpd.server_port}/api/display"
    asked = identify_for(shared, device.friendly_id)
    try:
        assert get(screen) == own.read_bytes()

        asked.write_text("", encoding="utf-8")
        card = get(screen)
        assert card != own.read_bytes()

        # A poll that is not a press leaves the card exactly where it is: the question is
        # "which box is this", and only the right box can answer it.
        get(display, {"ID": MAC, "Access-Token": device.token})
        assert asked.exists()
        assert get(screen) == card

        get(display, {"ID": MAC, "Access-Token": device.token, "Update-Source": "EXT0"})
        assert not asked.exists()
        assert get(screen) == own.read_bytes()
    finally:
        httpd.shutdown()
        thread.join()


def test_nothing_about_the_press_is_written_down(tmp_path: Path) -> None:
    """The press ends the card and leaves no trace. Not when, not by whom, not that it
    happened: a tally of presses is an adherence record about a person under another name.
    """
    shared = tmp_path / "screen.bmp"
    make_screen(shared)
    registry = tmp_path / "devices.json"
    device = register_device(registry, MAC)
    httpd = ThreadingHTTPServer(
        ("127.0.0.1", 0), make_handler(Config("http://127.0.0.1", shared, registry))
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    asked = identify_for(shared, device.friendly_id)
    asked.write_text("", encoding="utf-8")
    before = sorted(path.name for path in tmp_path.iterdir())
    try:
        get(
            f"http://127.0.0.1:{httpd.server_port}/api/display",
            {"ID": MAC, "Access-Token": device.token, "Update-Source": "EXT0"},
        )
    finally:
        httpd.shutdown()
        thread.join()

    after = sorted(path.name for path in tmp_path.iterdir())
    # The card is gone and nothing took its place.
    assert set(before) - set(after) == {asked.name}
    assert set(after) - set(before) == set()
