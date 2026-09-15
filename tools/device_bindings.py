"""Produce household key digests without exposing the hub's raw credential."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

from panel.config import Settings, _device_key_hashes


def bindings_from(path: Path, existing: str = "{}") -> dict[str, str]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        household, key = data["household"], data["device_key"]
        if not isinstance(key, str) or len(key) < 32 or not key.isascii():
            raise ValueError
        bindings = Settings(
            dev_auth=False, bootstrap_contact="", device_key_hashes=_device_key_hashes(existing),
        ).bound_device_keys
        digest = hashlib.sha256(key.encode()).hexdigest()
        if household in bindings and bindings[household] != digest:
            raise ValueError
        bindings[household] = digest
        checked = Settings(
            dev_auth=False, bootstrap_contact="", device_key_hashes=tuple(bindings.items()),
        )
        return checked.bound_device_keys
    except (OSError, KeyError, ValueError, TypeError, yaml.YAMLError):
        raise ValueError(
            "cannot produce device bindings from the protected configuration"
        ) from None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--existing", default="{}")
    arguments = parser.parse_args()
    try:
        print(json.dumps(bindings_from(arguments.path, arguments.existing), separators=(",", ":")))
    except ValueError as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()