# Firmware

ESP32 code for the devices in the house: e-paper displays, the LCD, and the physical
buttons.

Nothing is written yet. This directory holds the boundary, not an implementation.

## Rules for anything added here

- A device shows what it is told to show. It does not decide, generate, or cache content
  beyond the last message it received.
- The capture button is the only capture trigger in the entire system. No timer, no
  auto-trigger, no repeat.
- A device must never display an error code, a stack trace, or anything that implies the
  person reading it did something wrong. Faults go to the parent panel; the display either
  keeps its last content or shows something calm.
- Wi-Fi and broker credentials live in a gitignored `wifi_secrets.h` generated from a
  committed template. Never commit real values.

## TRMNL displays

The 7.5-inch OG DIY kits run the tagged TRMNL firmware with the patch in
`patches/trmnl-v1.8.12-mdns-byos.patch`. The patch makes the BYOS URL
`http://lanternina.local:8080` independent of the hub's DHCP address.

USB is provisioning only. The hub stores one Wi-Fi configuration in
`/etc/lanternina/trmnl-provisioning.json`; udev provisions a connected ESP32-S3 with the
common firmware and a per-device NVS partition. After that, the display wakes, fetches over
Wi-Fi, updates the paper and sleeps. It does not remain connected over USB.

The local BYOS server has no content-write endpoint. It accepts setup only for MAC addresses
registered by the physical USB provisioner and issues a different token to each display.
MAC-based bootstrap can still be spoofed by a peer already on the home LAN; this is the
remaining limit of the upstream TRMNL protocol, not a device identity proof.

## Open decisions — TODO(hackathon)

These block writing any of it, and are deliberately not guessed at:

- **Authentication beyond the TRMNL token.** There is no anonymous broker or write endpoint,
  but the setup exchange still identifies hardware by MAC. See T6 in
  [../docs/THREAT-MODEL.md](../docs/THREAT-MODEL.md).
- **Buttons**: how many, where, and whether their meaning is fixed or context-dependent.
  Context-dependent meanings change the protocol substantially.
- **Character set.** The previous system's embedded fonts covered ASCII only and silently
  dropped accented characters. If the interface language is Italian, fonts must be
  regenerated before any text is displayed — silently losing letters is not acceptable on a
  display someone is reading.
- **E-paper refresh behaviour**: partial vs full refresh, and what the display shows while
  the mini-PC is unreachable.
