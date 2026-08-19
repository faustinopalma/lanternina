"""The byte that decided whether a display drew anything.

A BMP palette entry is blue, green, red, and a fourth byte the format reserves and requires
to be zero. Pillow 11 on the hub writes 0xFF there. The TRMNL firmware refused those files
without saying so — it drew its own screen and kept polling, which reads exactly like "the
server sent nothing" and sent us looking at the wrong half of the system for an hour.

The test is worth having because nothing else in the stack notices: the file is a valid BMP
by every check we had, the right size, the right depth, and it round-trips through Pillow
perfectly. Only the firmware cared.
"""

from __future__ import annotations

from devices.epaper import render_notice_bmp
from devices.trmnl_byos import validate_screen


def _palette(bmp: bytes) -> bytes:
    header = int.from_bytes(bmp[14:18], "little")
    return bmp[14 + header : int.from_bytes(bmp[10:14], "little")]


def test_every_palette_entry_reserves_its_fourth_byte() -> None:
    bmp = render_notice_bmp("Un foglio ti aspetta", ["Prendilo dalla stampante."])
    palette = _palette(bmp)

    assert palette, "a 1-bit BMP carries a palette; without one there is nothing to check"
    assert len(palette) % 4 == 0
    reserved = palette[3::4]
    assert set(reserved) == {0}, (
        f"reserved palette bytes are {reserved.hex()}, not zero: the display will refuse this "
        "file and draw its own screen instead"
    )


def test_the_notice_is_still_the_geometry_the_firmware_expects(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "notice.bmp"
    path.write_bytes(render_notice_bmp("Fatto", ["Ho letto il foglio."]))
    assert len(validate_screen(path)) > 0
