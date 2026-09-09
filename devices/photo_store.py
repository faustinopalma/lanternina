"""Durable camera receipts and household photographs on the hub."""

from __future__ import annotations

import hashlib
import io
import json
import re
import sqlite3
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from PIL import Image

MAX_PHOTO_BYTES = 750_000
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024
PHOTO_ID = re.compile(r"[0-9a-f]{32}")


class PhotoStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
        self.path = path
        with self.connect() as database:
            database.execute(
                "CREATE TABLE IF NOT EXISTS photos ("
                "id TEXT PRIMARY KEY, camera TEXT NOT NULL, digest TEXT NOT NULL,"
                "jpeg BLOB, received REAL NOT NULL, captured REAL, target TEXT NOT NULL,"
                "state TEXT NOT NULL, detail TEXT NOT NULL DEFAULT '')"
            )
            database.execute(
                "CREATE TABLE IF NOT EXISTS photo_sync (id TEXT PRIMARY KEY, state TEXT)"
            )
        path.chmod(0o640)
        with self.connect() as database:
            database.execute(
                "CREATE TABLE IF NOT EXISTS camera_status (id TEXT PRIMARY KEY, report TEXT)"
            )

    def record_camera(self, report: dict[str, Any]) -> None:
        with self.connect() as database:
            database.execute(
                "INSERT OR REPLACE INTO camera_status VALUES (?, ?)",
                (report["id"], json.dumps(report)),
            )

    def cameras(self) -> list[dict[str, Any]]:
        with self.connect() as database:
            return [
                json.loads(row[0]) for row in database.execute("SELECT report FROM camera_status")
            ]

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA secure_delete=ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def accept(
        self,
        photo_id: str,
        camera: str,
        jpeg: bytes,
        *,
        captured: float | None,
        target: dict[str, Any] | None,
    ) -> bool:
        if not PHOTO_ID.fullmatch(photo_id):
            raise ValueError("invalid capture identifier")
        if not 0 < len(jpeg) <= MAX_PHOTO_BYTES:
            raise ValueError("invalid photograph size")
        with Image.open(io.BytesIO(jpeg)) as image:
            if image.format != "JPEG" or image.width * image.height > 12_000_000:
                raise ValueError("expected a JPEG of at most 12 megapixels")
            image.load()
        digest = hashlib.sha256(jpeg).hexdigest()
        with self.connect() as database:
            database.execute("BEGIN IMMEDIATE")
            old = database.execute("SELECT * FROM photos WHERE id=?", (photo_id,)).fetchone()
            if old:
                if old["camera"] != camera or old["digest"] != digest:
                    raise ValueError("capture identifier already belongs to different bytes")
                return False
            total, count = database.execute(
                "SELECT COALESCE(SUM(length(jpeg)),0), COUNT(*) FROM photos"
            ).fetchone()
            if total + len(jpeg) > MAX_ARCHIVE_BYTES or count >= 10000:
                raise OverflowError("the family photograph archive is full")
            database.execute(
                "INSERT INTO photos VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', '')",
                (photo_id, camera, digest, jpeg, time.time(), captured, json.dumps(target)),
            )
        return True

    def get(self, photo_id: str) -> dict[str, Any] | None:
        with self.connect() as database:
            row = database.execute("SELECT * FROM photos WHERE id=?", (photo_id,)).fetchone()
        return dict(row) if row else None

    def unsynced(self) -> list[dict[str, Any]]:
        with self.connect() as database:
            rows = database.execute(
                "SELECT photos.id, photos.state FROM photos LEFT JOIN photo_sync "
                "ON photos.id=photo_sync.id WHERE photo_sync.state IS NULL "
                "OR photo_sync.state != photos.state ORDER BY photos.received"
            ).fetchall()
        return [dict(row) for row in rows]

    def synced(self, photo_id: str, state: str) -> None:
        with self.connect() as database:
            database.execute("INSERT OR REPLACE INTO photo_sync VALUES (?, ?)", (photo_id, state))

    def listing(self) -> list[dict[str, Any]]:
        with self.connect() as database:
            rows = database.execute(
                "SELECT id, received, captured, state, detail FROM photos "
                "WHERE jpeg IS NOT NULL ORDER BY received DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    def delete(self, photo_id: str) -> None:
        with self.connect() as database:
            database.execute(
                "UPDATE photos SET jpeg=NULL, target='null', state='deleted', detail='' WHERE id=?",
                (photo_id,),
            )

    def claim(self) -> dict[str, Any] | None:
        with self.connect() as database:
            database.execute("BEGIN IMMEDIATE")
            row = database.execute(
                "SELECT * FROM photos WHERE state='pending' ORDER BY received LIMIT 1"
            ).fetchone()
            if not row:
                return None
            database.execute("UPDATE photos SET state='processing' WHERE id=?", (row["id"],))
        return dict(row)

    def finish(self, photo_id: str, state: str, detail: str) -> None:
        with self.connect() as database:
            database.execute(
                "UPDATE photos SET state=?, detail=? WHERE id=? AND state='processing'",
                (state, detail[:300], photo_id),
            )
