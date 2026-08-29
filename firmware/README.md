# Firmware

ESP32 code for the devices in the house: e-paper displays, the LCD, and the physical buttons.

Nothing is written yet. This directory holds the boundary, not an implementation.

## Rules for anything added here

- A device shows what it is told to show. It does not decide, generate, or cache content beyond the last message it received.
- The capture button is the only capture trigger in the entire system. No timer, no auto-trigger, no repeat.
- A device must never display an error code, a stack trace, or anything that implies the person reading it did something wrong. Faults go to the parent panel; the display either keeps its last content or shows something calm.
- Wi-Fi and broker credentials live in a gitignored `wifi_secrets.h` generated from a committed template. Never commit real values.

## TRMNL displays

The 7.5-inch OG DIY kits run the tagged TRMNL firmware with the three patches in `patches/`. `trmnl-v1.8.12-mdns-byos.patch` makes the BYOS URL `http://lanternina.local:8080` independent of the hub's DHCP address. `trmnl-v1.8.12-no-button-reset.patch` takes the two destructive presses off the button: upstream wipes the Wi-Fi credentials after five seconds of holding and the device credentials after fifteen, and holding is what somebody does when a press seems not to have registered.

`trmnl-v1.8.12-real-battery.patch` makes the board read its battery. Upstream defines `FAKE_BATTERY_VOLTAGE` for `BOARD_XIAO_EPAPER_DISPLAY` in `src/DEV_Config.h`, with its own comment saying to take it out after testing, and `readBatteryVoltage()` therefore returns the constant `4.2f` and never touches the ADC. Both units in the house reported exactly 4.2 V for as long as anybody looked, and the panel said "batteria carica" about a display that had been off the cable for a fortnight. Everything downstream was dead with it: the 3.70 V and 3.60 V thresholds in `devices/trmnl_byos.py` could not fire, `LOW_BATTERY_REFRESH` and `CRITICAL_BATTERY_REFRESH` never applied, and the low-battery screens could not appear. The real read is in the same function, a few lines below the fake one — `PIN_VBAT_SWITCH` 6 on, eight samples of `PIN_BATTERY` 3, averaged and doubled for the divider.

**Take the reading with a meter on the same cell before trusting the numbers.** The thresholds are derived from a generic single-cell LiPo curve, not measured on these cells, and a LiPo sags under load and recovers after, so one sample can read low with charge left. `ideas/02 §3` is the calibration that has not been done.

Both apply with `patch --binary -p1`. The `--binary` is not optional: the vendor's `bl.cpp` has CRLF line endings, and plain `patch` strips the carriage returns out of the patch and then refuses every hunk.

### Flashing, and the two ways it goes wrong

Both displays were flashed with the battery patch on 29 August 2026 and came back reading 4.06 V and 4.16 V, against exactly 4.2 on both before it. Getting there cost an evening and one display that looked lost, and both faults are worth writing down because neither announces itself.

**Use `devices/trmnl_provision.py`, not esptool by hand.** It writes twice: the merged image at `0x0` and a per-device NVS at `0x9000`. Writing only the first is what a plain `write_flash 0x0` does, and it leaves the display with no Wi-Fi credentials and no token — it boots, joins nothing, and goes quiet. That reads exactly like a bricked board. `/opt/lanternina/devices/provision-one.sh` wraps it: it picks the port by MAC, because both displays are on the cable and `ttyACM0` and `ttyACM1` swap depending on which woke first.

**esptool's reset does nothing on these boards.** It prints `Hard resetting via RTS pin...` and the XIAO ESP32-S3 speaks USB-Serial/JTAG, where there is no RTS. The chip stays in the ROM bootloader: permanently enumerated, never sleeping, never reporting. The tell is `/dev/ttyACM*` sitting there for minutes when a healthy display appears for about nine seconds every sixty-seven. `esptool --before usb_reset --after hard_reset run` leaves it, and so does unplugging the cable.

The proven binary is kept at `/opt/lanternina/firmware/trmnl-7inch5-og-diy-kit-real-battery.bin`, beside the two it succeeds. Going back is one `provision-one.sh` run with `--firmware` pointing at the older one.

Recovery does not depend on the button: the hub keeps 16 MiB of original flash per unit in `/var/lib/lanternina/trmnl-backups/` and reprovisions over USB, which is the same cable the reset would have forced anyway.

USB is provisioning only. The hub stores one Wi-Fi configuration in `/etc/lanternina/trmnl-provisioning.json`; udev provisions a connected ESP32-S3 with the common firmware and a per-device NVS partition. After that, the display wakes, fetches over Wi-Fi, updates the paper and sleeps. It does not remain connected over USB.

The local BYOS server has no content-write endpoint. It accepts setup only for MAC addresses registered by the physical USB provisioner and issues a different token to each display. MAC-based bootstrap can still be spoofed by a peer already on the home LAN; this is the remaining limit of the upstream TRMNL protocol, not a device identity proof.

## Open decisions — TODO(hackathon)

These block writing any of it, and are deliberately not guessed at:

- **Authentication beyond the TRMNL token.** There is no anonymous broker or write endpoint, but the setup exchange still identifies hardware by MAC. See T6 in [../docs/THREAT-MODEL.md](../docs/THREAT-MODEL.md).
- **Buttons**: how many, where, and whether their meaning is fixed or context-dependent. Context-dependent meanings change the protocol substantially.
- **Character set.** The previous system's embedded fonts covered ASCII only and silently dropped accented characters. If the interface language is Italian, fonts must be regenerated before any text is displayed — silently losing letters is not acceptable on a display someone is reading.
- **E-paper refresh behaviour**: partial vs full refresh, and what the display shows while the mini-PC is unreachable.
