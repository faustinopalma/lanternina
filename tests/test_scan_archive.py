from __future__ import annotations

import subprocess

import cv2
import numpy as np

from devices.scan_archive import ScanStore
from devices.scan_sheet import scan_page


def test_scan_is_durable_before_returning_to_the_reader(tmp_path, monkeypatch):
    database = tmp_path / "scans.db"
    monkeypatch.setenv("LANTERNINA_SCAN_DATABASE", str(database))
    pixels = np.arange(1200, dtype=np.uint8).reshape(40, 30)
    _, image = cv2.imencode(".png", pixels)
    monkeypatch.setattr("devices.scan_sheet.subprocess.run", lambda *args, **kwargs:
                        subprocess.CompletedProcess([], 0, image.tobytes(), b""))
    scanned = scan_page("scanner-test")
    assert np.array_equal(scanned, pixels)
    store = ScanStore(database)
    rows = store.listing()
    assert len(rows) == 1
    row = store.get(rows[0]["id"])
    assert row["state"] == "done"
    assert np.array_equal(cv2.imdecode(np.frombuffer(row["jpeg"], dtype=np.uint8),
                                     cv2.IMREAD_GRAYSCALE), pixels)
    store.delete(row["id"])
    assert not store.accept(row["id"], "scanner-test", row["jpeg"],
                            captured=row["captured"], target=None)
    assert store.get(row["id"])["jpeg"] is None