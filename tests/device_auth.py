from __future__ import annotations

from dataclasses import replace

from fastapi.testclient import TestClient


def bind_household(client: TestClient, household: str) -> str:
    settings = client.app.state.settings
    assert not settings.device_household or settings.device_household == household
    client.app.state.settings = replace(settings, device_household=household)
    return household