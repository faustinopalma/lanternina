# XIAO camera firmware

This project targets the assembled XIAO ESP32S3 Sense, USB serial 94:A9:90:D0:9D:D0, with 8 MiB flash and 8 MiB PSRAM. The shutter connects D3/GPIO4 to ground. The external LED connects D2/GPIO3 through its series resistor to ground. The microphone is not initialized.

PlatformIO 6.10.0 and Arduino ESP32 2.0.17 build this project on lanternina hub. Its package directory is `/srv/lanternina/tools/camera-platformio`, and its working copy is `/srv/lanternina/build/camera`. The existing PlatformIO executable is reused without upgrading it; e-paper packages and builds remain in their original directories.

## Build And Flash

The root-only `/etc/lanternina/camera.json` configuration contains a per-camera token, TLS paths and the family gallery credential. The build header is generated on the hub by `deploy/setup-camera.py`; it is excluded from Git. Firmware binaries contain credentials and remain in the protected build directory.

Run `sudo python3 deploy/setup-camera.py --mac 94:A9:90:D0:9D:D0 --hub-address 192.168.0.158` from the installed source tree to provision configuration. The hub address must be reserved in DHCP or regenerated when changed. The certificate contains the configured IP and `lanternina.local` and is pinned by the camera. Changing it requires rebuilding the firmware.

The certificate includes the numeric host as both an IP SAN and a DNS SAN because the installed Arduino/mbedTLS verifier rejected an IP-only SAN. This compatibility fix was tested on the board: the authenticated status request returned HTTP 200. Use `--renew-certificate` only when explicitly rotating the certificate, then rebuild and reflash every camera that pins it. Individual camera tokens remain unchanged.

Run `sudo python3 deploy/flash-camera.py --mac 94:A9:90:D0:9D:D0 --first-install` only for first installation. Subsequent updates omit `--first-install`, preserving queued photographs. The script checks enrollment, selects the port by USB identity, requires an 8 MiB backup and rejects repeated filesystem initialization. The original backup is `/var/lib/lanternina/camera-backups/94A990D09DD0.bin` and measured 8,388,608 bytes on 9 September 2026.

USB-triggered e-paper provisioning uses `--registered-only`. A camera or unknown board is ignored, including a board accidentally entered in the display registry before provisioning completed. Explicit enrollment and reflashing of e-paper displays remain available through `devices.trmnl_provision`.

## Capture And Power

A stable press produces one acceptance pulse and one capture. Wi-Fi association starts before camera initialization; JPEG capture and persistence do not wait for the network. Camera initialization occurs for each capture, with two warm-up frames, 1600 x 1200 JPEG output and one PSRAM framebuffer. Alternating-subject tests are still needed to establish framing, focus and freshness on the physical unit.

LittleFS holds at most three pending JPEGs of at most 750,000 bytes each. These are engineering limits, not measured typical image sizes. Writes are read back before promotion. Incomplete files are discarded at boot. Missing or damaged filesystems are not automatically formatted. Failed uploads preserve the JPEG and identifier; acknowledgements must match that identifier before two confirmation pulses and deletion from the device queue.

A USB data host is detected from USB frame activity, independently of whether a serial monitor is open. Without a live bus, the device enters deep sleep after work and LED feedback complete and the button is released. GPIO4 wakes it for a capture. A USB charger without data cannot be distinguished from battery power by this method; guaranteed charger detection needs an additional VBUS sensing circuit. No timer wakes the camera on battery. Pending uploads retry at the next capture or while connected to USB.

The camera synchronizes its clock without capture after a cold boot. If its clock was not set at capture time, the hub archives the image but does not guess which activity it belongs to. Battery deep sleep preserves the RTC; complete power loss does not.

The base board cannot measure its battery without extra wiring. Status reports therefore carry a null voltage. The optional 2:1 divider and disabled `CAMERA_BATTERY_GPIO` setting are documented in `docs/macchina-fotografica/README.md`. USB presence does not prove a battery is charging.

## Hub And Parent Panel

`lanternina-camera.service` receives authenticated HTTPS uploads on port 8443. SQLite commits the JPEG and immutable receipt before success is returned. A background worker passes correctly dated photos to the matching activity moment or renders them for a photo display. Activity changes share a process lock with scanner and timer operations. A worker interrupted after claiming a photo does not replay physical actions automatically; its processing state remains visible for diagnosis.

The parent panel has a Photographs section. The hub synchronizes originals and processing state through its existing device credential. The family can view, download and delete individual photographs, a confirmed inclusive date range or all photographs in a previewed selection. New photos arriving after the preview are excluded. Deleted identifiers remain as receipts without image bytes to prevent reuploads. Hub copies and photo display files are removed at the next successful synchronization; an offline e-paper device keeps its old pixels until it reconnects. Downloads already made by a person and any infrastructure backups are outside this deletion path.

The Devices section lists the camera, USB state, last device contact and measured battery voltage when hardware supports it. On the current board it explicitly reports the unavailable battery measurement. Sleeping on battery does not generate repeated camera heartbeats.

`sudo env PYTHONPATH=/opt/lanternina python3 tools/verify_camera.py` checks existing authenticated camera telemetry and creates, duplicates and deletes one synthetic JPEG in the live cloud archive. It does not trigger the camera, alter family photographs or test focus. On 9 September 2026 this check passed against the published API; the API, panel and Python CI workflows for commit f9cd5a4 also succeeded.