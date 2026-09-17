# Waveshare ESP32-S3-CAM-OV5640

The owner purchased the Waveshare ESP32-S3-CAM-OV5640, SKU 33699, as a second camera on 16 September 2026. Both cameras will remain available for comparison. The owner confirmed that the camera and speaker were included and connected a 3000 mAh LiPo battery before attaching the board to lanternina hub by USB. A read-only esptool probe identified ESP32-S3 revision 0.2, MAC `28:84:85:B1:6C:08`, 16 MiB flash and 8 MiB embedded PSRAM. Two USB captures, nominal battery telemetry, a brief BOOT restart, a BOOT wake from battery-powered deep sleep and a one-minute timer wake were verified later that day. External controls and current consumption remain untested.

The existing XIAO implementation remains in [firmware/camera](../../firmware/camera/README.md), with its current configuration and toolchain unchanged. The independent [Waveshare firmware](../../firmware/camera-waveshare/README.md) was installed on 16 September 2026 with its own build directory, identity and credentials. Two USB diagnostic photographs reached the hub and decoded successfully. The [porting note](../../ideas/waveshare-camera-bringup.md) records the implementation boundary and remaining acceptance checks.

## Reference collection

The local collection is under `_reference/waveshare-esp32-s3-cam-ov5640/`, excluded by the existing `_reference/` rule in [.gitignore](../../.gitignore). It contains 28 downloaded files: documentation pages, eleven hardware PDFs, the Arduino settings image, two source archives and their commit metadata. The Waveshare source archive includes five factory firmware binaries. These are downloaded references, not firmware read from the purchased board.

The local `manifest.json` records the URL, retrieval time, byte count and SHA-256 of each download. `source/` contains the archives and extracted source, `hardware/` contains manuals, `web/` preserves original HTML, and `text/` contains searchable derivatives and a rendered schematic. Text extraction can omit rotated labels; the original PDFs remain authoritative. The local acquisition and extraction scripts support repeating the collection without installing anything into the project environment.

The Waveshare source is pinned to [72af9302030bb6f018d5c21b1225005481e09fda](https://github.com/waveshareteam/ESP32-S3-CAM-OVxxxx/tree/72af9302030bb6f018d5c21b1225005481e09fda). The supplementary Espressif camera driver is pinned to [3fb41a99d61a853313d1cd5543ebf2c109ef7c0e](https://github.com/espressif/esp32-camera/tree/3fb41a99d61a853313d1cd5543ebf2c109ef7c0e). This second archive documents the current driver API; it is not evidence that the Arduino package bundles that revision.

The commercial product page was initially blocked by Cloudflare and became readable later through the shared browser. The three board photograph/interface/dimension image URLs on `www.waveshare.net` returned verification HTML instead of images and were excluded from the verified downloads. The complete schematic and its pin-assignment table were downloaded and inspected. The owner confirmed the included camera and speaker; physical dimensions and the supplied lens mechanism still need confirmation from the delivered unit or Waveshare.

## Board and sensor

Waveshare specifies an ESP32-S3R8 dual-core processor up to 240 MHz, 8 MB of stacked PSRAM and 16 MB of external flash. The board has 2.4 GHz Wi-Fi, Bluetooth LE, USB-C, a 24-pin DVP camera connector, an 18-pin SPI/QSPI display connector, microSD, two microphones and an external speaker connector. The radio normally uses the onboard antenna; selecting the IPEX external antenna requires moving a resistor, not a firmware setting.

The supplied sensor is OV5640. Waveshare lists 2592 x 1944 pixels, a 1/4-inch optical format, a 4.1 mm lens at f/2.8, and fields of view of 68 degrees diagonal, 55 degrees horizontal and 42 degrees vertical. These are vendor specifications, not measured framing or image quality. The OmniVision datasheet and Espressif driver confirm JPEG support even though the Waveshare overview's OV5640 format row omits it.

Autofocus requires an AF-capable lens module as well as sensor support. The archived current `esp32-camera` driver supplies an optional autofocus helper and loads the sensor's AF firmware over SCCB. Neither the name OV5640 nor an AF-capable connector establishes that the purchased module contains the actuator. Verify the ribbon marking, module construction and actual near/far focus before promising autofocus or a minimum working distance.

## Camera connections

The following ESP32 GPIO assignments agree between the Waveshare schematic, its Arduino camera example and its ESP-IDF board header. D0-D7 here name camera data bits, not XIAO board labels.

| Signal | ESP32 GPIO |
| --- | --- |
| Camera D0, D1, D2, D3 | 45, 47, 48, 46 |
| Camera D4, D5, D6, D7 | 42, 40, 39, 21 |
| XCLK | 38 |
| PCLK | 41 |
| VSYNC | 17 |
| HREF | 18 |
| SCCB/I2C SDA | 8 |
| SCCB/I2C SCL | 7 |

The Arduino example uses a 20 MHz camera XCLK. Its `camera_pins.h` places this Waveshare-specific mapping under `CAMERA_MODEL_ESP_EYE`. A generic ESP-EYE definition from another package is not interchangeable. The example sets direct reset and power-down GPIOs to `-1`; the schematic nevertheless connects `CAM_PWDN` to the external I/O controller. Account for that controller when starting or sleeping the camera.

The CH32V003F4U6 runs Waveshare's I/O-expander protocol at I2C address `0x24`. Its Arduino driver uses registers `0x02` for direction, `0x03` for outputs, `0x04` for inputs, `0x05` for PWM and `0x06` for ADC. These are firmware-defined registers, not a standard CH32V003 peripheral register map. The chip datasheet alone cannot replace the supplied driver.

| Schematic signal | Connection | Porting consequence |
| --- | --- | --- |
| CAM_PWDN | EXIO3 | Manage camera standby through the expander |
| PA_CTRL | EXIO4 | Enable or mute the speaker amplifier explicitly |
| BAT_EN | EXIO5 | Preserve the battery power-latch behavior |
| PWR_LED | EXIO6 | The camera demo drives this output high during setup |
| CHG_DET | EXIO7 | Treat this as an input; establish its polarity on the board |
| BAT_ADC | Expander ADC | Read through the vendor protocol and calibrate voltage conversion |
| BOOT | GPIO0 | A brief press restarts or wakes Lanternina; holding it during power-on enters the ROM downloader |
| PWR_KEY | GPIO15 and power circuit | Lanternina reads it as an input-only shutter; preserve the hardware latch |

Some Arduino expander comments describe unrelated SD or CAN functions, and its initializer marks all eight lines as outputs. The schematic and the more selective ESP-IDF initialization are the reference for electrical direction and signal ownership. Do not carry those comments or the blanket direction setting into a board abstraction without checking each signal.

Since 17 September, onboard PWR also requests one photograph in Lanternina, while awake or from deep sleep. The GPIO remains an input, the power latch stays enabled and holding the button does not repeat photographs. A held USB press and brief battery-only presses were physically verified. BOOT remains the status-only wake. GPIO15/PWR_KEY is not exposed on the LCD FPC: connector contact 15 is `TP_INT`. An external shutter can use the independently supported GPIO1 on contact 5; it does not need to share GPIO15.

## Development configuration

The pinned Waveshare archive uses `examples/Arduino-v3.2.0/` and `examples/ESP-IDF-v5.5.1/`. The documentation requires ESP-IDF 5.5.1 or later for these examples. Start with the named versions and their lockfiles before considering an upgrade.

The Arduino settings image selects `ESP32S3 Dev Module`, 16 MB flash, OPI PSRAM, 240 MHz CPU, hardware CDC/JTAG USB mode and UART0/hardware CDC upload. It shows QIO flash at 120 MHz. The ESP-IDF video example instead configures 80 MHz flash and 80 MHz octal PSRAM. Preserve each example's own configuration when reproducing it; these differing settings are not a reason to retune the existing camera. The Arduino screenshot disables USB CDC on boot, so verify how diagnostics reach the selected USB/serial path before relying on serial acceptance checks.

The Arduino guide recommends a 16 MB partition scheme without a speech model for ordinary examples, and the ESP-SR scheme only for examples requiring model storage. Lanternina needs its own reviewed partition layout for application updates and queued JPEGs. A stock demo partition scheme does not establish compatibility with the existing queue or update process.

| Starting point in the vendor archive | Purpose |
| --- | --- |
| `examples/Arduino-v3.2.0/examples/02_CameraWebServer/` | DVP pins, SCCB and `esp_camera` initialization |
| `examples/Arduino-v3.2.0/examples/03_audio_out_no_tf/` | ES8311 and I2S playback without a memory card |
| `examples/Arduino-v3.2.0/examples/04_SDMMC_Test/` | One-bit SDMMC wiring and filesystem access |
| `examples/Arduino-v3.2.0/examples/05_audio_out_tf/` | Playback from microSD |
| `examples/Arduino-v3.2.0/examples/06_esp_sr/` | ES7210 microphone initialization and optional speech processing |
| `examples/ESP-IDF-v5.5.1/01_simple_video_server/` | `esp_video`/V4L2 camera path and network demonstration |
| `examples/ESP-IDF-v5.5.1/04_dvp_camera_display/components/waveshare__esp32_s3_cam_ovxxxx/` | Board support package and shared peripheral controls |
| `examples/ESP-IDF-v5.5.1/06_usb_host_uvc/` | USB webcam device example, despite the directory's `host` wording |
| `Firmware/` | Generic factory binary and four display-specific factory binaries |

The ESP-IDF video example locks `esp_video` to 1.4.1, `esp_cam_sensor` to 1.7.0 and `waveshare/custom_io_expander_ch32v003` to 1.0.1. It is a different camera API from Arduino's `esp_camera`; pin values can be checked across both, but initialization code cannot simply be mixed. The archives include local source and lockfiles, not a complete offline ESP-IDF package cache or installed toolchain.

The Arduino camera demo starts at QVGA, JPEG quality 12, one framebuffer in internal DRAM. On initialization failure it retries RGB565. This proves neither full-resolution JPEG capture nor a working fallback: its second initialization result is unchecked. A Lanternina implementation must report failure explicitly and verify the returned format, dimensions and JPEG decoding. Use PSRAM for larger captures and measure warm-up, allocation failures and JPEG size. The current XIAO queue's 750,000-byte per-photo limit must not be assumed sufficient at 2592 x 1944.

## Audio and storage

Playback follows ESP32 I2S to ES8311, then NS4150B and the external speaker. Waveshare specifies a 3 W output into 4 ohms; achievable output depends on supply and distortion, and was not measured. The schematic exposes differential `PA_OUTL+` and `PA_OUTL-`: connect the speaker across those terminals, not from either output to ground. The owner confirmed that a speaker was included in this package on 16 September 2026.

The two microphones feed ES7210. The schematic includes an analog playback-reference path for acoustic echo cancellation, but useful cancellation also requires software and testing. Playback can be evaluated independently of microphone capture. Audio remains an available option; this collection adds no playback, recording or speech feature to Lanternina.

| I2S signal | ESP32 GPIO |
| --- | --- |
| MCLK | 10 |
| BCLK/SCLK | 11 |
| LRCLK/WS | 12 |
| Data from microphone ADC to ESP32 | 13 |
| Data from ESP32 to playback DAC | 14 |

The codecs and expander share the camera's I2C bus on SDA 8 and SCL 7. Coordinate bus ownership and clock initialization rather than creating conflicting controllers. The one-bit SDMMC pins are CLK 16, CMD 43 and D0 44. GPIO43/44 are also routed to the UART header, so serial use and SD use require deliberate coordination. A card is needed only for examples that access it.

## Power and recovery

Waveshare specifies one 3.7 V lithium cell on the GH1.25 battery connector and recommends a capacity of 2000 mAh or less. Check connector polarity and the cell's permitted charge current before connection. The ETA6098 datasheet describes charger capabilities; the assembled board's programming components determine the actual charge current. The schematic's BAT_ADC divider uses 200 kohms above 100 kohms, a nominal 3:1 voltage ratio calculated from the resistor values. ADC reference, scaling, error and charge-detection polarity still need measurement.

The owner connected one YUNIQUE GREEN-CLEAN-POWER 103665 battery, advertised as 1S, 3.7 V, 3000 mAh with protection, from [Amazon ASIN B0GSZRFYBD](https://www.amazon.it/dp/B0GSZRFYBD). This exceeds Waveshare's capacity recommendation. Capacity alone does not increase the charger's programmed current. The schematic shows R44 = 160 kohms at ETA6098 ISET; the datasheet describes CC/CV charging to 4.2 V, with 1.2 A specified at 150 kohms. The actual current at 160 kohms has not been measured. The listing's claim `1C approximately 1.5 A` is inconsistent with 3000 mAh, for which 1C is 3 A by calculation, and does not establish an allowed charging current. Confirm the cell's charging specification, polarity and thermal behavior; do not treat the seller's generic ESP32 compatibility statement as that evidence. Keep early charging supervised and disconnect power if there is swelling, odor or abnormal heating.

An ESP32 deep-sleep call does not establish low board current. Camera, codecs, amplifier, LED, regulator and CH32V003 can remain powered. The Waveshare FAQ warns that OV5640 warms during continuous capture and recommends stopping capture or entering standby while idle. Measure complete-board current on battery, including peripheral shutdown and wake behavior; no autonomy estimate is established here.

The owner observed a small LED remaining lit on battery. The schematic's LED2 anode has two paths: 3.3 V through R24 (3 kohms) and `PWR_LED` through R25 (3 kohms), with the cathode grounded. The firmware already drives `PWR_LED` LOW; that does not remove the fixed supply path. This is distinct from LED3 driven by the charger's status output. No resistor, LED or power-latch modification has been made. The new firmware explicitly places ES7210 in its documented stopped state and verifies register readback. ES8311 and amplifier settings remain unchanged. The reduction in board current, if any, still needs measurement; neither a lit LED nor a register value quantifies autonomy.

Before the first write, identify the new board by its own USB identity and MAC, confirm ESP32-S3 and the detected flash size, and preserve a complete original flash backup with a checksum outside public Git. A confirmed 16 MiB device requires 16,777,216 backup bytes. The existing `deploy/flash-camera.py` flow validates an 8 MiB XIAO and is not a Waveshare flashing procedure. Do not bypass its guard or reuse a credential-bearing XIAO binary.

If USB is not recognized, hold BOOT while connecting the USB data cable, then release BOOT. Close any serial monitor before flashing. Waveshare documents offset `0x00` for its merged factory binaries; ordinary application-only binaries follow their build's offsets. Restart or power-cycle after flashing. The UVC example occupies the programming USB interface, so returning to the downloader may require BOOT again. The four named LCD images target 1.83-, 2-, 2.8- and 3.5-inch displays; the generic image's headless behavior remains unverified.

The delivered board has BOOT and PWR, not RESET. A brief BOOT press restarts responsive Lanternina firmware after ongoing work completes, or wakes it from deep sleep without requesting a photograph. This was physically verified with periodic updates disabled. If the board remains in the ROM downloader, the application cannot handle the button: disconnect USB and battery, reconnect USB without BOOT held, then reconnect the battery. That full power cycle restored this unit during bring-up when automatic reset and PWR did not.

The installed firmware reads expander ADC register `0x06` and averages eight samples. Its nominal conversion uses 10-bit scaling, a 3.3 V reference and the 3:1 divider; readings around 4.05-4.11 V have reached the hub under the correct Waveshare identity. Failed or implausible readings remain null. A voltmeter comparison is still needed to establish voltage accuracy; neither remaining capacity nor battery life has been measured. Optional periodic updates and their current publication status are described in the [firmware guide](../../firmware/camera-waveshare/README.md).

## External button and LED

The owner selected the unused LCD FPC connector on 16 September 2026 to retain an RTC-capable shutter pin for deep sleep. Use a passive 18-position FFC/FPC breakout with numbered 2.54 mm pads or terminals, plus a matching 18-conductor flat-flex cable. The compatible Waveshare display family uses 0.5 mm pitch; [this inspection of the 2.8-inch module](https://www.circuitstate.com/tutorials/interfacing-waveshare-2-8-inch-capacitive-touch-lcd-with-arduino/) records an 18-pin, 0.5 mm cable. Verify the pitch and contact orientation against the actual camera connector and selected breakout before ordering. A 15- or 22-pin Raspberry Pi camera cable is not a substitute. Same-side and opposite-side contact cables can map breakout numbering differently; determine continuity before power is applied.

| LCD connector pin on this board | Signal | Connection |
| --- | --- | --- |
| 3 | GND | Common return for the button and LED cathode |
| 5 | GPIO1, LCD MOSI/QSPI D0 | Through 1 kohm to a normally open button, then GND |
| 6 | GPIO2, LCD MISO/QSPI D1 | Through 470 ohms to LED anode; LED cathode to GND |
| 1 | 3.3 V | Leave disconnected for this assembly |
| Other pins | Other display/peripheral signals | Leave disconnected |

These are connector contact numbers, not a left/right instruction for an unspecified viewing angle. The camera schematic and the [Waveshare display pin table](https://docs.waveshare.com/1.83inch_Touch_LCD_Module) independently place GND at contact 3 and MOSI at contact 5. GPIO2 on contact 6 comes from this camera's schematic; a display-only adapter might omit MISO, so choose a breakout exposing every contact. Disconnect USB and battery before inserting the cable, soldering or measuring continuity. With the cable fitted, verify the breakout's ground connection and map contacts 5 and 6 end to end. Mount the breakout and provide strain relief so button presses cannot pull on the connector.

```text
LCD contact 5 / GPIO1 --- 1 kohm --- normally open button --- GND
LCD contact 6 / GPIO2 --- 470 ohms --- LED anode
LED cathode ---------------------------------------------- GND
LCD contact 3 -------------------------------------------- GND
```

The firmware enables the GPIO1 pull-up; a press reads LOW and is also the configured EXT0 wake level. The 1 kohm resistor limits accidental pin-drive current but is not complete ESD protection. Use an ordinary low-current LED, not a 5 V or 12 V indicator module. With an assumed 1.8-2.2 V LED drop, the calculated current through 470 ohms at 3.3 V is 2.3-3.2 mA. The firmware keeps the LED on during capture and uses two flashes for a matching receipt; physical visibility and timing still need testing after assembly. The display cannot share the selected GPIO1/2 signals while these controls are connected.

The four-pin UART header exposes GPIO43/44 and ground, but those GPIOs are outside the ESP32-S3 RTC range used for EXT0 deep-sleep wake. The I2C header is shared with camera and audio control. Neither is the selected connection for this assembly. Leave the onboard BOOT and PWR buttons intact for recovery and power control.

## Source links

- [Waveshare board overview](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx?variant=ESP32-S3-CAM-OV5640), [resources](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/Resources-And-Documents), [user guide](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/Instructions-For-Use), [Arduino](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/Arduino), [ESP-IDF](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/ESP-IDF), [flashing](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/Firmware-Flashing), [FAQ](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/FAQ) and [support](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx/Technical-Support).
- [Board schematic](https://files.waveshare.com/wiki/ESP32-S3-CAM-OVxxxx/ESP32-S3-CAM-XXXX-schematic.pdf).
- [OV5640 full datasheet, SparkFun mirror](https://cdn.sparkfun.com/assets/4/0/4/6/5/OV5640-Datasheet.pdf) and [OmniVision product brief, Digi-Key mirror](https://media.digikey.com/pdf/Data%20Sheets/OmniVision%20PDFs/OV5640_PB_3-4-11.pdf).
- [ESP32-S3 datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf) and [technical reference manual](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf).
- [ES8311 datasheet](https://files.waveshare.com/wiki/common/ES8311.DS.pdf), [ES8311 user guide](https://files.waveshare.com/wiki/common/ES8311.user.Guide.pdf), [ES7210 datasheet](https://files.waveshare.com/wiki/common/ES7210-datasheet.pdf) and [NS4150B manual, Espressif mirror](https://dl.espressif.com/dl/schematics/NS4150B.pdf).
- [ETA6098 datasheet](https://files.waveshare.com/wiki/common/ETA6098.pdf) and [CH32V003 datasheet](https://www.wch-ic.com/download/file?id=359).
- [ESP-IDF 5.5.1 setup](https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32s3/get-started/index.html), [sleep modes](https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32s3/api-reference/system/sleep_modes.html), [USB Serial/JTAG](https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32s3/api-guides/usb-serial-jtag-console.html) and [esptool read/write commands](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/esptool/basic-commands.html).
