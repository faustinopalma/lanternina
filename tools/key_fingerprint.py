"""Compare copies of the shared keys without ever printing them.

Prints a salted digest and a length for each key, so two machines can be checked
against each other. The salt is public: this hides the value from a shoulder and
from a log, not from someone who can already guess it.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

NAMES = ("device_key", "approval_key", "safety_key")
SALT = b"lanternina-keycheck\x00"


def fingerprint(value: str) -> str:
    return hashlib.sha256(SALT + value.encode()).hexdigest()[:12]


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def from_yaml(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    found = {}
    for name in NAMES:
        match = re.search(rf"^\s*{name}\s*:\s*(.+?)\s*$", text, re.M)
        if match:
            found[name] = _unquote(match.group(1))
    return found


def from_env_file(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    found = {}
    for name in NAMES:
        pattern = rf"^\s*(?:export\s+)?LANTERNINA_{name.upper()}\s*=\s*(.*?)\s*$"
        match = re.search(pattern, text, re.M)
        if match:
            found[name] = _unquote(match.group(1))
    return found


def from_env() -> dict[str, str]:
    found = {}
    for name in NAMES:
        value = os.environ.get(f"LANTERNINA_{name.upper()}", "")
        if value:
            found[name] = value
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--yaml", type=Path, help="a secrets.local.yaml-shaped file")
    source.add_argument("--env-file", type=Path, help="a systemd EnvironmentFile")
    source.add_argument("--env", action="store_true", help="the current environment")
    args = parser.parse_args(argv)

    if args.yaml:
        label, found = str(args.yaml), from_yaml(args.yaml)
    elif args.env_file:
        label, found = str(args.env_file), from_env_file(args.env_file)
    else:
        label, found = "environment", from_env()

    print(f"source: {label}")
    for name in NAMES:
        value = found.get(name)
        if value is None:
            print(f"  {name:13} absent")
        else:
            print(f"  {name:13} len={len(value):<4} fp={fingerprint(value)}")
    return 0 if found else 1


if __name__ == "__main__":
    sys.exit(main())
