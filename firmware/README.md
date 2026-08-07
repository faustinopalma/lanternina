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

## Open decisions — TODO(hackathon)

These block writing any of it, and are deliberately not guessed at:

- **Transport**: USB serial, Wi-Fi/MQTT, or both. Supporting both doubles the surface.
- **Authentication on the device bus.** An anonymous broker means anyone on the home Wi-Fi
  can put text on a screen she reads. See T6 in [../docs/THREAT-MODEL.md](../docs/THREAT-MODEL.md).
- **Buttons**: how many, where, and whether their meaning is fixed or context-dependent.
  Context-dependent meanings change the protocol substantially.
- **Character set.** The previous system's embedded fonts covered ASCII only and silently
  dropped accented characters. If the interface language is Italian, fonts must be
  regenerated before any text is displayed — silently losing letters is not acceptable on a
  display someone is reading.
- **E-paper refresh behaviour**: partial vs full refresh, and what the display shows while
  the mini-PC is unreachable.
