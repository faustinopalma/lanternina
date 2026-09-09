from __future__ import annotations

import sys

import pytest

from tools import camera_usb


class Port:
    def __init__(self, lines):
        self.lines = iter(lines)
        self.sent = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def reset_input_buffer(self):
        pass

    def write(self, data):
        self.sent.append(data)

    def readline(self):
        return next(self.lines).encode()


def test_capture_check_requires_receipt_and_subsequent_empty_queue(monkeypatch, capsys):
    port = Port(
        [
            "usb=1 button=1 busy=0 filesystem=1 queued=0",
            "command=CAPTURE accepted",
            "capture=example bytes=134520 saved=1",
            "upload=example status=201 accepted=1",
            "usb=1 button=1 busy=1 filesystem=1 queued=-1",
            "usb=1 button=1 busy=0 filesystem=1 queued=0",
        ]
    )
    monkeypatch.setattr(camera_usb, "open_port", lambda name: port)
    monkeypatch.setattr(sys, "argv", ["camera_usb", "CAPTURE"])
    camera_usb.main()
    assert port.sent == [b"CAPTURE\n"]
    assert "VERDICT: photograph acknowledged" in capsys.readouterr().out


@pytest.mark.parametrize(
    "failure",
    [
        "command=BUSY",
        "capture_failed=frame_or_storage",
        "upload=id status=400 accepted=0",
    ],
)
def test_capture_check_does_not_confuse_progress_with_success(monkeypatch, failure):
    port = Port(["command=CAPTURE accepted", failure])
    monkeypatch.setattr(camera_usb, "open_port", lambda name: port)
    monkeypatch.setattr(sys, "argv", ["camera_usb", "CAPTURE"])
    with pytest.raises(RuntimeError):
        camera_usb.main()


@pytest.mark.parametrize("command,reply", [
    ("USB_TEST_ON", "usb_test=on button_triggers_disabled_until_disconnect"),
    ("USB_TEST_OFF", "usb_test=off"),
])
def test_usb_mode_requires_matching_acknowledgement(monkeypatch, command, reply):
    port = Port(["usb=1 button=1 busy=0", reply])
    monkeypatch.setattr(camera_usb, "open_port", lambda name: port)
    monkeypatch.setattr(sys, "argv", ["camera_usb", command])
    camera_usb.main()
    assert port.sent == [(command + "\n").encode("ascii")]


def test_installation_requires_fresh_authenticated_status(monkeypatch, capsys):
    port = Port([
        "status usb=1 busy=1 filesystem=1 identity=94:A9:90:D0:9D:D0",
        "status_http=200 phase=operation_complete",
    ])
    fresh = iter([False, True])
    monkeypatch.setattr(camera_usb, "open_port", lambda name: port)
    monkeypatch.setattr(camera_usb, "authenticated_since", lambda *args: next(fresh))
    monkeypatch.setattr(sys, "argv", ["camera_usb", "STATUS", "--authenticated-since", "100"])
    camera_usb.main()
    assert "fresh authenticated status verified" in capsys.readouterr().out
