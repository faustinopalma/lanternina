"""Synchronize hub photographs and family deletions through the authenticated panel API."""

from __future__ import annotations

import base64
from typing import Any

from devices.ask_panel import _ask


def synchronize(hub: Any, ask: Any = _ask) -> int:
    house = hub.house
    if not (house.panel and house.household and house.device_key):
        return 0
    prefix = f"{house.panel.rstrip('/')}/api/device/{house.household}/photos"
    cameras = hub.store.cameras()
    if cameras:
        ask(
            f"{house.panel.rstrip('/')}/api/device/{house.household}/devices",
            cameras,
            key=house.device_key,
            timeout=30,
        )

    def call(path: str, body: dict[str, Any]) -> dict[str, Any]:
        return ask(prefix + path, body, key=house.device_key, timeout=30)

    def report() -> dict[str, Any]:
        rows = hub.store.listing()
        return call(
            "/sync",
            {
                "pending": len(hub.store.unsynced()),
                "localPhotos": len(rows),
                "lastReceivedAt": max((row["received"] for row in rows), default=None),
            },
        )

    for photo_id in report()["ids"]:
        hub.delete(photo_id)
        hub.store.synced(photo_id, "deleted")
    completed = 0
    for pending in hub.store.unsynced()[:50]:
        row = hub.store.get(pending["id"])
        if row is None:
            continue
        if row["state"] == "deleted":
            receipt = call(f"/{row['id']}/delete", {})
            if receipt.get("id") != row["id"] or receipt.get("deleted") is not True:
                raise ValueError("invalid deletion receipt")
        else:
            receipt = call(
                "",
                {
                    "id": row["id"],
                    "camera": row["camera"],
                    "receivedAt": row["received"],
                    "capturedAt": row["captured"],
                    "state": row["state"],
                    "imageBase64": base64.b64encode(row["jpeg"]).decode(),
                },
            )
            if receipt.get("id") != row["id"]:
                raise ValueError("receipt belongs to another photograph")
            if receipt.get("deleted") is True:
                hub.delete(row["id"])
                row["state"] = "deleted"
            elif receipt.get("stored") is not True:
                raise ValueError("photograph was not stored")
        hub.store.synced(row["id"], row["state"])
        completed += 1
    if completed:
        for photo_id in report()["ids"]:
            hub.delete(photo_id)
            hub.store.synced(photo_id, "deleted")
    return completed
