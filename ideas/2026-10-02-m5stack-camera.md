# M5Stack camera bring-up

The owner connected an M5Stack Timer Camera OV3660 to lanternina hub on 2 October 2026 and requested a third supported camera type. The owner then asked for autonomous preparation, deferred physical tests, and requested separate wake and shutter buttons on a camera-shaped printed enclosure. No photograph is required for installation verification.

## Hardware and source evidence

The hub enumerated FTDI VID:PID `0403:6001`, serial `5552517A38`, as `/dev/serial/by-id/usb-Hades2001_M5stack_5552517A38-if00-port0`. Esptool 4.9.0 identified ESP32-D0WDQ6-V3 revision 3.1, MAC `3C:8A:1F:D7:A7:B4`, flash manufacturer `46`, device `4016`, and 4 MB flash. These are measurements from the connected board. OV3660 and 8 MB physical PSRAM are vendor specifications until checked on the running unit.

The [M5Stack TimerCamera documentation](https://docs.m5stack.com/en/unit/timercam) maps the external HY2.0 connector to GPIO13, GPIO4, 5 V and GND. It maps the LED to GPIO2, the power latch to GPIO33, battery ADC to GPIO38, sensor reset to GPIO15, and the BM8563 bus to GPIO12/14. The [vendor source at ca24786e3cecdad060d86d6eb1cbc299685591b9](https://github.com/m5stack/TimerCam-arduino/tree/ca24786e3cecdad060d86d6eb1cbc299685591b9) supplies the camera map, power-hold implementation and an external GPIO4 deep-sleep example. The [ESP-IDF 4.4.7 sleep documentation](https://docs.espressif.com/projects/esp-idf/en/v4.4.7/esp32/api-reference/system/sleep_modes.html) confirms both GPIOs as RTC wake inputs and permits combined EXT0 and EXT1 wake sources.

## Controls and power choice

The firmware assigns GPIO13 to wake-only and GPIO4 to shutter. Each external normally open button closes its input to GND through 1 kohm. The GPIO4 button can wake and capture in one press; the wake-only button can be placed elsewhere on the enclosure. This makes the physical layout independent of the board edge and costs both external GPIOs, leaving that connector unavailable for another I2C peripheral.

The firmware retains the battery power latch during ESP32 deep sleep instead of using BM8563 complete power-off. This enables both GPIO buttons to wake the device and costs additional, unmeasured standby current. The vendor's 2 microamp power-off claim is not a current figure for this configuration. Battery-only cold-start and wake still require testing. A completely unpowered board cannot respond to these GPIO contacts.

The FTDI adapter does not expose the native S3 USB frame counter. The firmware therefore uses a 120-second idle window and leaves USB presence unknown. A battery voltage is also withheld until the battery and measurement are checked; a charger-fed ADC value alone would not establish a connected battery's state.

## Preparation

The implementation uses an independent `firmware/camera-m5stack` target, with the existing authenticated intake protocol and queue design. XIAO and Waveshare sources are not changed. The host model recognizer now accepts the explicit M5Stack board identifier and its firmware prefix while preserving generic fallback for unknown explicit board identifiers.

The first serial backup attempt at 460800 baud failed before data transfer. A subsequent 115200-baud attempt did not leave a complete file. The resumed 115200-baud read completed all 4,194,304 bytes in 375.7 seconds. Esptool's whole-flash digest verification passed before any write. The original is stored with mode 0600 at `/var/lib/lanternina/camera-backups/3C8A1FD7A7B4.bin`, with SHA256 `2b488e205e8f7a1f9f9dfff55df403a3ddd426d05bbb51ff45fc21a340293eef` and an adjacent checksum file.

The isolated firmware compile passed with PlatformIO Espressif32 6.10.0 and Arduino 2.0.17. Its initial compile-only image used 1,077,789 application bytes and 51,680 static RAM bytes; these are build measurements, not final installed-image hashes or runtime memory readings. The installation, inventory and serial unit checks initially passed 48 tests. Ruff and editor diagnostics reported no errors in the changed Python files.

## Installed and verified

The identity-bound flasher installed `m5stack-2026-10-02-external-controls` and the initial LittleFS filesystem. Esptool verified each written image. The original hub camera configuration and two changed runtime files are retained under `/var/lib/lanternina/camera-backups/3C8A1FD7A7B4-hub-before`. Existing camera tokens, TLS certificate/key, display registry and XIAO/Waveshare source hashes matched their pre-install values. The receiver was restarted after confirming that every existing photograph was already done or deleted.

| Check | Observed result |
| --- | --- |
| ESP32 mapped PSRAM heap | 4,192,123 bytes |
| LittleFS mounted | 2,555,904 bytes total; 8,192 bytes used |
| Serial identity | `3C:8A:1F:D7:A7:B4`, shutter GPIO4, wake GPIO13, LED GPIO2 |
| HTTPS status | HTTP 200 with the existing pinned certificate and a new camera-specific token |
| Fresh report | `usb_status`, `operation_complete`, received 2 October 2026 at 05:54:58 UTC |
| Capture state | `captureRequested=false`, `captureResult=not_requested`, `sensorInitMs=0`, queue 0 |
| Stored photographs from this camera | 0 |
| Authenticated panel inventory | `M5Stack Timer Camera OV3660`, periodic battery updates unsupported |
| Python regression tests | 50 passed across provisioning, serial commands and camera intake |
| Host C++ checks | 12 boot/input states, debounce, held/released shutter, wake priority and test-mode suppression passed |
| Negative control | Forcing every boot to request a photograph made the host check fail |

The installed source `src/main.cpp` is 22,091 bytes with SHA256 `d1af26b517e312d49fbb7566ab9a6d0282e3de625047389c0313bbedd5ebf310`. The generated firmware binary is 1,085,200 bytes with SHA256 `587ce15c5d058b8113444c05dbe72ba35d8da4410270e47f763fdbd396d3a876`. The binary contains provisioned credentials and remains in the private hub build directory; it is not a publication artifact. The original flash backup may also contain vendor configuration and remains private.

The host check in `firmware/check-m5stack.py` extracts and compiles the firmware's actual boot and button branches. These checks establish software decisions, not electrical wake, switch bounce on the assembled wires, power-latch retention on battery or image quality. The reported sensor-init time is zero because no capture was requested; sensor identity remains a vendor specification until the first authorised photograph.

## Deferred checks

The owner will perform the physical tests later. No USB capture command, image-quality test, artificial GPIO pulse or battery discharge test is part of this preparation. The pending acceptance checks are listed in the [firmware guide](../firmware/camera-m5stack/README.md#acceptance).
