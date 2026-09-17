# Waveshare camera firmware

This independent target runs on Waveshare ESP32-S3-CAM-OV5640, MAC `28:84:85:B1:6C:08`. The original [XIAO target](../camera/README.md) remains unchanged. The owner selected external controls through the unused LCD connector on 16 September 2026: GPIO1 for the shutter and GPIO2 for the LED. The [board guide](../../docs/macchina-fotografica/waveshare-ov5640.md#external-button-and-led) gives connector pin numbers and wiring. Those parts have not yet been connected or physically tested.

## Implementation

Revision `waveshare-2026-09-17-pwr-audio-sleep` starts from an independent copy of the XIAO capture/receipt implementation. It changes the board pins, PSRAM/flash configuration and peripheral control, while retaining JPEG storage, authenticated HTTPS delivery, matching receipts, diagnostic capture commands and the three-image queue. The initial image size is 1600 x 1200 with JPEG quality 12 and two preliminary frames. The 750,000-byte JPEG limit remains sufficient for the measured images, not a guarantee for every scene or full resolution.

The target uses PlatformIO `espressif32@6.10.0`, Arduino ESP32 2.0.17, QIO flash at 80 MHz and OPI PSRAM. This is a tested Lanternina port, not a build of Waveshare's Arduino 3.2.0 or ESP-IDF 5.5.1 examples. The separate package directory is `/srv/lanternina/tools/waveshare-platformio`; builds are in `/srv/lanternina/build/waveshare-cameras/<MAC without colons>`. Neither the XIAO nor display packages are upgraded. The 16 MiB partition layout contains two 3 MiB application slots and a 10,420,224-byte LittleFS partition; an OTA update mechanism has not been added.

The board initializes I2C on SDA8/SCL7 and keeps that bus owned by `Wire`. The camera borrows I2C controller 0 through `sccb_i2c_port`. Expander output `0x28` holds the battery latch on and puts the camera in standby; direction `0x7f` keeps charge detection as an input. Speaker amplification is disabled and the external indicator stays off while idle. The onboard power LED also receives current from 3.3 V through R24, independently of its EXIO6 control through R25. Driving EXIO6 LOW does not establish that the LED is dark; the owner observed it lit on battery. Capture clears EXIO3, initializes the OV5640 and returns it to standby after releasing the driver. Repeated captures verified this sequence. A runtime identity check rejects a binary built for a different MAC.

Audio streaming is not initialized. At each boot, the firmware explicitly stops the ES7210 audio ADC at I2C address `0x40` using the register sequence in Espressif's ESP-ADF v2.7 driver. It checks all nine readbacks and prints `audio_adc_standby=1` only when writes and readbacks succeed. Failure is logged without preventing the camera from operating or sleeping. ES8311 remains at its observed power-down defaults and the amplifier remains disabled. This verifies configuration, not a measured reduction in complete-board current; the external microphones and other components still have supply connections. The [evidence record](../../docs/EVIDENCE.md#waveshare-power-and-controls-17-september-2026) gives the source and limits.

Battery voltage uses eight two-byte little-endian readings from expander register `0x06`, a 10-bit ADC, a nominal 3.3 V reference and the schematic's 3:1 divider. A failed transfer, saturated reading or result outside 2.5-4.5 V produces null. The observed values around 4.05-4.11 V are nominal conversions, not voltmeter-calibrated measurements or charge percentages. USB connection does not establish charge state.

After work and feedback complete and all buttons are released, battery operation enters deep sleep with camera standby requested. GPIO1 LOW wakes through EXT0 for a photograph. Onboard PWR, GPIO15 LOW, wakes through EXT1 for a photograph; onboard BOOT, GPIO0 LOW, uses the same EXT1 mask for a status connection without requesting a photograph. The recorded wake mask distinguishes them; BOOT takes precedence if both wake bits are present. All three inputs use pull-ups. PWR and the external shutter share a debounced, release-to-rearm capture path while awake, so holding either does not repeat photographs. GPIO15 remains an input and the battery latch remains enabled. Firmware adds no long-press shutdown action.

A brief BOOT press while awake requests a software restart after release and completion of active work. This requires responsive firmware; it cannot recover a stopped CPU or intercept the ROM downloader. PWR is also connected to the hardware power circuit; its new input use preserves that circuit. GPIO15 is not exposed on the LCD connector: contact 15 carries `TP_INT`, not GPIO15. The external shutter remains GPIO1 on contact 5, through 1 kohm to a normally open button and GND on contact 3. Connecting a display conflicts with the chosen GPIO1/2 controls.

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

## Measured on 17 September 2026

The installed PWR/audio-sleep build uses 50,864 bytes of static RAM and 1,019,941 bytes of application flash, reported by PlatformIO. Its source SHA-256 is `00a7477216ef597755096cfdf8b6e33b3572d9f5d303fb3587ef20a49ec4a779`, matching the hub source. The original backup was verified before each upload; the mounted filesystem and authenticated status passed after upload. The XIAO source checksum remained unchanged.

Before explicit audio shutdown, ES7210 registers `0x01/0x06/0x40/0x47` read `0x20/0x00/0x80/0x00`. Afterward they read `0x7f/0x07/0xc0/0x3f`. The writes to `0x47-0x4c` are `0xff`; this board reads back `0x3f/0x1f/0x3f/0x1f/0xff/0xff`. The validation compares these observed per-register values rather than assuming every written bit is readable. All nine checks passed; clock and power registers remained in the stopped state after a camera capture. ES8311 read `0xfc` at `0x0d` and `0x02` at `0x12` before and after the change.

| Physical check | Observed result |
| --- | --- |
| PWR held for approximately 2 seconds on USB | One photograph, 117,402 bytes, 1600 x 1200 pixels, 2,835 ms capture, 1,030 ms upload, HTTP 201, zero queued |
| PWR after USB removal and sleep | Confirmed 19-second deep sleep; one photograph, 66,633 bytes, 1600 x 1200 pixels, 2,776 ms capture, 635 ms upload, HTTP 201, zero queued |
| Additional PWR press confirmed by owner | Separate wake and photograph, 58,138 bytes, HTTP 201, zero queued |
| BOOT after those captures | `boot_button` wake, previous sleep confirmed, no capture or sensor initialization |

The first two JPEGs decoded on the hub and matched their stored SHA-256 digests. The owner photographed a glass and reported that a protective film still covered the lens; these checks do not assess focus or image quality. The count changed from 143 to 146 across the three intentional PWR captures. BOOT then reported no capture. The final battery-only report at 07:31:52 CEST on 17 September read 4.063306332 V nominal, with periodic updates disabled and the remembered interval still 60 minutes. USB charging, firmware updates and these captures ended the preceding overnight comparison. Use this new report as a separate reference, not as evidence of an autonomy improvement.
