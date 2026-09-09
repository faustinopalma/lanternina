"""Create camera-only credentials and a pinned hub TLS certificate on the hub."""

from __future__ import annotations

import argparse
import grp
import json
import os
import secrets
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", required=True)
    parser.add_argument("--hub-address", required=True)
    parser.add_argument("--renew-certificate", action="store_true")
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
    mac = args.mac.upper()
    config["cameras"].setdefault(mac, secrets.token_urlsafe(32))
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8", newline="")
    group = grp.getgrnam("lanternina").gr_gid
    for path in (config_path, certificate, private_key):
        path.chmod(0o640)
        os.chown(path, 0, group)
    wifi = json.loads((root / "trmnl-provisioning.json").read_text())
    values = {
        "WIFI_SSID": wifi["ssid"],
        "WIFI_PASSWORD": wifi["password"],
        "HUB_URL": f"https://{args.hub_address}:8443",
        "CAMERA_TOKEN": config["cameras"][mac],
        "HUB_CA": certificate.read_text(),
    }
    header = Path("/srv/lanternina/build/camera/include/camera_secrets.h")
    header.write_text(
        "#pragma once\n"
        + "".join(
            f"static const char *{key} = {json.dumps(value)};\n" for key, value in values.items()
        ),
        encoding="utf-8",
        newline="",
    )
    import pwd

    owner = pwd.getpwnam("fausto")
    os.chown(header, owner.pw_uid, owner.pw_gid)
    header.chmod(0o600)
    header.parents[1].chmod(0o700)
    archive = Path("/srv/lanternina/photos")
    archive.mkdir(exist_ok=True, mode=0o750)
    os.chown(archive, owner.pw_uid, group)
    from devices.trmnl_byos import _write_devices, load_devices

    registry = root / "trmnl-devices.json"
    displays = load_devices(registry)
    if mac in displays and not displays[mac].provisioned:
        del displays[mac]
        _write_devices(registry, displays)
    print("Camera credentials ready; no display credentials or firmware changed.")


if __name__ == "__main__":
    main()
