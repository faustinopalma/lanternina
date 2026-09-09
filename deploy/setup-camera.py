"""Create camera-only credentials and a pinned hub TLS certificate on the hub."""

from __future__ import annotations

import argparse
import grp
import json
import os
import secrets
import subprocess
from pathlib import Path

from devices.camera_provision import camera_mac, provisioning_lock


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", required=True)
    parser.add_argument("--hub-address", required=True)
    parser.add_argument("--renew-certificate", action="store_true")
    parser.add_argument("--build-user", default="fausto")
    args = parser.parse_args()
    root = Path("/etc/lanternina")
    certificate = root / "camera-cert.pem"
    private_key = root / "camera-key.pem"
    config_path = root / "camera.json"
    os.umask(0o077)
    if not certificate.exists() or args.renew_certificate:
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-days",
                "3650",
                "-keyout",
                str(private_key),
                "-out",
                str(certificate),
                "-subj",
                "/CN=lanternina.local",
                "-addext",
                (
                    f"subjectAltName=DNS:lanternina.local,DNS:{args.hub_address},"
                    f"IP:{args.hub_address}"
                ),
                "-addext",
                "basicConstraints=critical,CA:TRUE",
            ],
            check=True,
            capture_output=True,
        )
    config = (
        json.loads(config_path.read_text())
        if config_path.exists()
        else {
            "database": "/srv/lanternina/photos/photos.db",
            "certificate": str(certificate),
            "private_key": str(private_key),
            "family_password": secrets.token_urlsafe(24),
            "cameras": {},
        }
    )
    mac = camera_mac(args.mac)
    config["cameras"].setdefault(mac, secrets.token_urlsafe(32))
    config["hub_address"] = args.hub_address
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8", newline="")
    group = grp.getgrnam("lanternina").gr_gid
    for path in (config_path, certificate, private_key):
        path.chmod(0o640)
        os.chown(path, 0, group)
    import pwd

    owner = pwd.getpwnam(args.build_user)
    archive = Path("/srv/lanternina/photos")
    archive.mkdir(parents=True, exist_ok=True, mode=0o750)
    os.chown(archive, owner.pw_uid, group)
    from devices.trmnl_byos import _write_devices, load_devices

    registry = root / "trmnl-devices.json"
    displays = load_devices(registry)
    if mac in displays and not displays[mac].provisioned:
        del displays[mac]
        _write_devices(registry, displays)
    print("Camera credentials ready; no display credentials or firmware changed.")


if __name__ == "__main__":
    with provisioning_lock():
        main()
