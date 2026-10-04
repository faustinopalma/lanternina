# M5Stack Timer Camera

This target adds the M5Stack TimerCamera U082 with OV3660 as the third camera type. The [XIAO](../camera/README.md) and [Waveshare](../camera-waveshare/README.md) targets retain their own source and build configuration. All three use the authenticated camera receiver on lanternina hub.

## External controls

The HY2.0-4P connector carries GPIO13, GPIO4, 5 V and GND. The firmware uses GPIO13 for a wake-only button and GPIO4 for a shutter button. Both buttons can sit on the printed enclosure, connected by flexible wires. The onboard reset button is not the shutter.

| Control | Connection | Awake | Deep sleep |
| --- | --- | --- | --- |
| Wake | GPIO13 through 1 kohm to normally open button, then GND | Reports status without taking a photograph | Wakes and reports status |
| Shutter | GPIO4 through 1 kohm to normally open button, then GND | Takes one photograph | Wakes and takes one photograph |
| Both held | Same separate circuits | Gives wake priority | Gives wake priority while GPIO13 is asserted |

Each button needs a momentary, normally open dry contact, using `COM` and `NO` if it has three terminals. Internal pull-ups hold both inputs high. The two buttons may share the ground return. Leave the connector's 5 V conductor insulated and unused: ESP32 GPIO inputs are 3.3 V signals and must not receive 5 V. Identify conductors from the board labels and continuity, not cable colour or an assumed connector viewing direction. Disconnect USB and battery before wiring.

Use short flexible wires with strain relief and insulated joints inside the enclosure. The 1 kohm series resistors limit current if a signal is accidentally configured as an output; they do not make a 5 V connection safe. Confirm released and pressed levels with a meter before closing the enclosure. An additional pull-up would go to a verified 3.3 V point, never the connector's 5 V pin.

The shutter requires release before another shot. The software debounce interval is 30 ms. Photographs and network work run synchronously; additional button presses during an operation are not queued. Holding either button prevents sleep. The firmware sleeps after 120 seconds without a completed operation or serial command. Boot, reset, wake-only and status commands do not request photographs.

GPIO4 uses ESP32 EXT0 active-low wake. GPIO13 uses EXT1 with a single-pin `ALL_LOW` mask. The RTC peripheral domain stays powered for the pull-ups. GPIO33 keeps the power latch high, and GPIO15 holds the camera sensor in reset between photographs. This retains external GPIO wake at the cost of more standby current than the manufacturer's RTC-controlled complete power-off mode. Complete-board current and battery autonomy have not been measured.

These buttons wake a powered ESP32 from deep sleep. They cannot turn on a board whose power latch has been released, whose battery is disconnected, or whose battery is empty. This firmware does not release that latch or schedule BM8563 power-off. Keep access to USB for charging, maintenance and recovery. Battery-only cold-start and any separate master power switch need a physical test before the enclosure is finalised.

## Capture and status

The capture path requests JPEG at 1600 x 1200 pixels, quality 12, with two discarded warm-up frames. It checks for OV3660 when a photograph is requested. Startup keeps the sensor in reset, so a successful status report does not establish that the sensor or lens works.

The device verifies each saved JPEG against its framebuffer before publishing its queue metadata. It retains at most three photographs, each at most 750,000 bytes, in a 2,555,904-byte LittleFS partition. It removes a queued photograph only after receiving an authenticated HTTPS receipt with the same identifier. It retries queued delivery on a later operation; there is no periodic photograph timer. The 4 MiB flash layout reserves one 1.5 MiB application slot and does not provide OTA updates.

M5Stack specifies 8 MB physical PSRAM. The classic ESP32 Arduino configuration maps about 4 MiB into the normal heap; the installation guard checks that mapped heap, rather than interpreting it as the physical chip capacity.

The FTDI serial adapter does not provide the native USB frame counter used by the S3 targets. USB presence is reported as unknown. Battery voltage is also unknown until the battery connection and ADC conversion are validated. The firmware does not infer charge from the cable or advertise periodic battery reporting support.

## Build and install

Run provisioning on the hub, with the repository under `/opt/lanternina`. Keep tokens, certificates, generated headers and binaries on the hub. The installed M5Stack serial adapter is `/dev/serial/by-id/usb-Hades2001_M5stack_5552517A38-if00-port0`; this identifies the FTDI adapter, so every installation also checks the ESP32 MAC `3C:8A:1F:D7:A7:B4`.

Before first installation, read all 4,194,304 bytes with esptool at 115200 baud, verify them against the device, and retain the root-only backup at `/var/lib/lanternina/camera-backups/3C8A1FD7A7B4.bin`, with its SHA256 in the adjacent `.bin.sha256` file. The flasher refuses a missing, partial, unchecksummed or non-private backup. It rechecks original flash before the first write.

```sh
cd /opt/lanternina
sudo env PYTHONPATH=/opt/lanternina python3 deploy/setup-camera.py \
  --mac 3C:8A:1F:D7:A7:B4 --hub-address 192.168.0.158
sudo env PYTHONPATH=/opt/lanternina python3 deploy/flash-m5stack-camera.py \
  --mac 3C:8A:1F:D7:A7:B4 \
  --port /dev/serial/by-id/usb-Hades2001_M5stack_5552517A38-if00-port0 \
  --first-install
```

The receiver must load the newly enrolled token before the authenticated installation check. Enrollment preserves all existing tokens and the existing certificate unless renewal is explicitly requested. Restart only the camera receiver, after checking that it has no photographs being processed. On subsequent firmware updates omit `--first-install`; the flasher then preserves the photograph filesystem. `--build-only` compiles without writing flash.

The isolated PlatformIO core is `/srv/lanternina/tools/m5stack-platformio`. The build directory is `/srv/lanternina/build/m5stack-cameras/3C8A1FD7A7B4`. The platform is pinned to Espressif32 6.10.0, Arduino 2.0.17, with the `m5stack-timer-cam` board definition. Upload uses 115200 baud.

## Serial maintenance

`tools/camera_usb.py` accepts `--port` for this FTDI device. It requests and verifies the camera identity before issuing the selected command. `STATUS` reads local state. `REPORT` sends fresh authenticated status without a photograph. `CAPTURE` is an explicit development photograph and must be chosen separately.

```sh
sudo env PYTHONPATH=/opt/lanternina /srv/lanternina/tools/platformio-venv/bin/python \
  tools/camera_usb.py REPORT --mac 3C:8A:1F:D7:A7:B4 \
  --port /dev/serial/by-id/usb-Hades2001_M5stack_5552517A38-if00-port0
```

The command requires the ESP32 to be awake. Serial traffic alone cannot wake it from deep sleep. Before external buttons are fitted, an explicit esptool reset over the connected FTDI adapter can restart it without a photograph. The adapter can remain enumerated while the ESP32 sleeps; its presence is not proof that firmware is awake.

```sh
sudo /srv/lanternina/tools/platformio-venv/bin/python -m esptool \
  --chip esp32 --baud 115200 \
  --port /dev/serial/by-id/usb-Hades2001_M5stack_5552517A38-if00-port0 \
  --before default_reset --after hard_reset run
```

`USB_TEST_ON` suppresses physical shutter requests for the current awake session, until `USB_TEST_OFF`, sleep or reset. It does not infer USB disconnection and does not suppress the wake-only button. Explicit `CAPTURE` commands remain available; none was issued during this installation.

## Acceptance

The 2 October installation passed exact identity, flash-write verification, PSRAM, filesystem, authenticated HTTPS status and authenticated panel-inventory checks. The host control test and 50 Python regression tests passed. The camera had zero stored photographs at the end of verification.

The owner deferred photographs and physical tests on 2 October 2026. The [bring-up record](../../ideas/2026-10-02-m5stack-camera.md) separates completed software checks from installation and physical acceptance. The remaining checks cover an actual OV3660 JPEG and receipt, each external button awake and asleep, held-button and simultaneous-button behaviour, offline delivery, battery-only wake, power-latch retention and complete-board current. The enclosure should remain serviceable until these pass.
