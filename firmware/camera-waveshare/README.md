# Waveshare camera firmware

This independent target runs on Waveshare ESP32-S3-CAM-OV5640, MAC `28:84:85:B1:6C:08`. The original [XIAO target](../camera/README.md) remains unchanged. The owner selected external controls through the unused LCD connector on 16 September 2026: GPIO1 for the shutter and GPIO2 for the LED. The [board guide](../../docs/macchina-fotografica/waveshare-ov5640.md#external-button-and-led) gives connector pin numbers and wiring. Those parts have not yet been connected or physically tested.

## Implementation

Revision `waveshare-2026-09-16-battery-timer` starts from an independent copy of the XIAO capture/receipt implementation. It changes the board pins, PSRAM/flash configuration and peripheral control, while retaining JPEG storage, authenticated HTTPS delivery, matching receipts, diagnostic capture commands and the three-image queue. The initial image size is 1600 x 1200 with JPEG quality 12 and two preliminary frames. The 750,000-byte JPEG limit remains sufficient for the two measured images, not a guarantee for every scene or full resolution.

The target uses PlatformIO `espressif32@6.10.0`, Arduino ESP32 2.0.17, QIO flash at 80 MHz and OPI PSRAM. This is a tested Lanternina port, not a build of Waveshare's Arduino 3.2.0 or ESP-IDF 5.5.1 examples. The separate package directory is `/srv/lanternina/tools/waveshare-platformio`; builds are in `/srv/lanternina/build/waveshare-cameras/<MAC without colons>`. Neither the XIAO nor display packages are upgraded. The 16 MiB partition layout contains two 3 MiB application slots and a 10,420,224-byte LittleFS partition; an OTA update mechanism has not been added.

The board initializes I2C on SDA8/SCL7 and keeps that bus owned by `Wire`. The camera borrows I2C controller 0 through `sccb_i2c_port`. Expander output `0x28` holds the battery latch on and puts the camera in standby; direction `0x7f` keeps charge detection as an input. Speaker amplification and the user indicator stay off. Capture clears EXIO3, initializes the OV5640 and returns it to standby after releasing the driver. Two captures without a reboot verified this sequence. A runtime identity check rejects a binary built for a different MAC.

The speaker and microphones are not initialized. Battery voltage uses eight two-byte little-endian readings from expander register `0x06`, a 10-bit ADC, a nominal 3.3 V reference and the schematic's 3:1 divider. A failed transfer, saturated reading or result outside 2.5-4.5 V produces null. The observed values around 4.05-4.11 V are nominal conversions, not voltmeter-calibrated measurements or charge percentages. USB connection does not establish charge state.

After work and feedback complete, battery operation enters deep sleep with camera standby requested. GPIO1 LOW wakes through EXT0 for a photograph. Onboard BOOT, GPIO0 LOW, wakes through EXT1 for a status connection without requesting a photograph. Both inputs use pull-ups. A brief BOOT press while awake requests a software restart after release and completion of active work. This requires responsive firmware; it cannot recover a stopped CPU or intercept the ROM downloader. PWR retains its hardware power function. Connecting a display conflicts with the chosen GPIO1/2 controls.

Optional battery updates are disabled initially, with a remembered interval of 60 minutes. The parent can choose 1-1440 minutes under Devices, using Battery updates and Every. The hub returns these settings through authenticated status responses; the camera stores them in NVS and receives changes on its next connection. Disabling preserves the interval and leaves BOOT wake available. Timer wake connects and reports status without initializing the sensor or delivering queued photographs. The interval measures sleep time, so successive reports also include connection and awake time. The API advertises these controls only for the supported Waveshare model.

## Build and update

The [Waveshare flashing command](../../deploy/flash-waveshare-camera.py) is separate from the XIAO command. From `/opt/lanternina` on the hub, run `sudo env PYTHONPATH=/opt/lanternina python3 deploy/flash-waveshare-camera.py --mac 28:84:85:B1:6C:08` for an update. `--build-only` compiles without flashing. `--first-install` was used once and is now refused for this camera, preserving its filesystem. The command requires a complete original backup and checksum, an enrolled identity, ESP32-S3, 16 MiB flash and 8 MB embedded PSRAM. It generates credentials from the selected camera's protected configuration and verifies authenticated status after upload.

First enrollment used the existing `deploy/setup-camera.py` path. The hub kept the XIAO's token, the TLS certificate and the other receiver settings unchanged. Both cameras have distinct credentials. Credential-bearing headers, builds and backups remain protected on the hub and outside Git. The original Waveshare flash is `/var/lib/lanternina/camera-backups/288485B16C08.bin`, 16,777,216 bytes, mode 0600, owned by root. Its SHA-256 is `b683fc737036715e63ce45c9528db47c5cecbc10dc4b993bc06fefd23316ec27`; esptool verified it against the full flash before the first write. The installation marker is `288485B16C08.waveshare-installed` in the same directory.

`sudo /srv/lanternina/tools/platformio-venv/bin/python /opt/lanternina/tools/camera_usb.py STATUS --mac 28:84:85:B1:6C:08` reads board identity, expander status, GPIO states, PSRAM heap, filesystem and queue. Replace `STATUS` with `CAPTURE` for an explicit USB diagnostic photograph. A diagnostic photograph is archived without advancing an activity. These commands require the camera to be awake on a USB data connection.

## Measured on 16 September 2026

The battery/timer build uses 50,864 bytes of static RAM and 1,019,005 bytes of application flash, as reported by PlatformIO. Esptool identified ESP32-S3 revision 0.2, 16 MiB flash and 8 MB embedded PSRAM. Arduino reported approximately 8,386,000 bytes of PSRAM heap, slightly below physical capacity because of allocator overhead. The status check therefore uses a 7-8 MiB heap bound alongside the independent physical identity check.

| Measurement | First USB capture | Second USB capture, same boot |
| --- | --- | --- |
| Sensor PID | `0x5640` | `0x5640` |
| Decoded JPEG dimensions | 1600 x 1200 pixels | 1600 x 1200 pixels |
| JPEG bytes | 217,010 | 216,842 |
| Sensor initialization | 762 ms | 762 ms |
| Selected framebuffer ready | 2,176 ms | 2,176 ms |
| Storage stage | 846 ms | 915 ms |
| Capture operation | 3,029 ms | 3,109 ms |
| Upload | 1,637 ms | 995 ms |
| Work through delivery feedback | 6,772 ms | 6,297 ms |
| Receipt and final queue | HTTP 201, matching ID, zero queued | HTTP 201, matching ID, zero queued |

The stored originals decoded successfully on the hub and matched their stored SHA-256 digests. Both records had a null activity target and state `done`. These checks establish two USB capture/delivery cycles; they do not measure focus quality, full-resolution performance or battery operation. The driver logged `gdma_disconnect` on teardown and a TLS read error around completed requests. Both requests still produced matching durable receipts. The warnings remain recorded rather than being treated as evidence of failure or removed without investigation.

A physical brief BOOT press on USB changed boot ID `d3523981` to `7cee3780` with reset reason `software`. After USB removal, a BOOT press produced boot ID `559da257`, wake cause `boot_button`, reset reason `deep_sleep`, a valid previous-sleep marker and 63 seconds of sleep. Both checks reported no capture request, no sensor initialization and an unchanged hub total of 143 photographs. Timer updates were disabled during both tests. These observations establish manual restart and one battery wake, not sleeping current.

The board has BOOT and PWR buttons, not a RESET button. Holding BOOT during power-on enters the ROM downloader. During bring-up, automated USB reset and pressing PWR did not leave that mode. Disconnecting both USB and battery, then reconnecting USB without holding BOOT, restored the application; the battery was reconnected afterward. Once the application is running, use a brief BOOT press for restart or wake.

A temporary one-minute setting returned by the hub produced boot ID `1036e91c` with wake cause `timer`, trigger `battery_timer`, a valid deep-sleep marker and 60 seconds of sleep. Sensor initialization and capture remained absent; the hub still contained 143 photographs. The hub then restored disabled updates and a 60-minute interval. A final timer wake, boot ID `ef786bb8`, received that setting; no report followed for an observed interval exceeding 122 seconds. The final USB readback after disabling was not performed. This proves one timed wake and an observed stop, not long-term clock accuracy or autonomy.

External shutter presses, visible LED timing, current consumption, charge behavior, offline retries on this board and preservation of a nonempty queue through a firmware update remain acceptance checks. The installed update preserved the mounted, empty filesystem and camera credentials. Do not solder or insert the flat-flex cable while USB or battery is connected.
