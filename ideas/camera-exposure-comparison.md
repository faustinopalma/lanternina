# Camera Exposure Comparison

## Continue With D8 On The Existing Board

Later on 10 September 2026 the owner chose to retain camera `94:A9:90:D0:9D:D0` and move the shutter to another pin, preferring D7, D8 or D9. This supersedes the replacement-only instructions below. The selected pin is D8/GPIO7, an RTC GPIO usable for EXT0 deep-sleep wakeup. D9/GPIO8 also has RTC capability; D7/GPIO44 does not support this wakeup mechanism. See [Seeed's pin map](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/#hardware-overview) and [Espressif's sleep documentation](https://docs.espressif.com/projects/esp-idf/en/v4.4.7/esp32s3/api-reference/system/sleep_modes.html#external-wakeup-ext0). D8 shares the Sense microSD clock, so the slot must remain empty and SD must remain disabled. The current firmware does not initialize SD. Choosing D8 retains deep sleep but reserves that SPI signal for the shutter.

Revision `camera-2026-09-10-d8-autoexposure` uses GPIO7 for awake presses and EXT0 wakeup, preserving the pull-up, debounce, LED and autoexposure behavior. It makes the newly retired GPIO2 an input with digital and RTC pulls disabled, alongside the previously retired GPIO4 and GPIO3. STATUS now reads GPIO7's mux and separately reports retired GPIO2. The intended connection is D8, a 1 kohm series resistor near the GPIO, the normally open shutter, then GND. The resistor adds current limiting, not proof against another fault. The owner will solder with USB and battery disconnected; wiring has not been physically accepted.

Compilation passed with 50,072 bytes of RAM and 992,629 bytes of program flash reported. The guarded updater verified hardware identity, backup, flash hashes, mounted filesystem and fresh authenticated HTTP 200 telemetry without formatting LittleFS. Post-flash STATUS showed GPIO7 HIGH, pull-up enabled, pull-down disabled, input enabled and output disabled. GPIO2 and GPIO4 reported inputs with both pulls and output disabled. No capture was requested; the authenticated boot report showed queue zero. Physical shutter, LED feedback, battery wakeup and long-term reliability remain unverified on D8. The previous source is backed up on the hub at `/var/lib/lanternina/camera-backups/main-before-d8-20260910.cpp`. The root cause of the earlier low inputs remains unproven.

## Resume With A New Board

On 10 September 2026 the owner stopped testing and explicitly requested preserving the current firmware for a replacement board. Do not install a minimal diagnostic firmware, revert autoexposure, change shutter pins or resume tests on the old board without a new request. The next intended operation is first installation on a new camera when the owner connects it. The firmware source remains `firmware/camera/src/main.cpp`, revision `camera-2026-09-10-autoexposure`, also installed in the hub source tree at `/opt/lanternina/firmware/camera/src/main.cpp`. It uses D1/GPIO2 for the shutter and D4/GPIO5 for the LED; verify the new board's actual wiring before installation. The old board's disconnected wires do not establish the replacement's wiring.

Follow [Build And Flash](../firmware/camera/README.md#build-and-flash). Identify the replacement's own USB MAC and compatible hardware before running `sudo env PYTHONPATH=/opt/lanternina python3 deploy/flash-camera.py --mac <NEW_MAC> --hub-address 192.168.0.158 --first-install` from `/opt/lanternina` on the hub. The hub address was used successfully in this session; recheck reachability in the next session. The guarded procedure enrolls the selected camera, requires its original flash backup and builds with its own generated credentials in `/srv/lanternina/build/cameras/<NEW_MAC_WITHOUT_COLONS>`. Use `--first-install` only for a genuinely new board whose filesystem may be initialized. Never copy the old board's credential-bearing binary, token, filesystem or MAC to the replacement. Keep the old enrollment and archived photographs unless the owner requests their removal. Secrets and binaries stay in protected hub directories.

The old camera MAC is `94:A9:90:D0:9D:D0`. Its complete original backup remains `/var/lib/lanternina/camera-backups/94A990D09DD0.bin`; the source before autoexposure was also copied to `/var/lib/lanternina/camera-backups/main-before-autoexposure-20260910.cpp`. The ordinary USB capture on the autoexposure revision passed, as recorded below. Battery operation and image quality across lighting conditions are not accepted for this revision. On the replacement, verify firmware identity, mounted filesystem, authenticated telemetry, an explicitly authorized capture with matching receipt and empty queue, and then physical shutter/LED and battery sleep/wake with the owner. No new captures or hardware operations are authorized merely by this handoff.

The camera changes were initially left uncommitted on 10 September. On 11 September the owner requested committing and pushing `firmware/camera/src/main.cpp`, `firmware/camera/README.md`, `tools/camera_usb.py` and this note. The modified scanner/panel files and new scan archive files in the working tree are unrelated work and remain outside the camera commit.

## Starting Point

On 10 September 2026 the owner reported dark photographs and positioned the camera in a dim scene for a stationary USB comparison. The installed firmware identified itself as `camera-2026-09-09-capture-led`, and the sensor reported PID `3660`. The ordinary capture saves the first JPEG after sensor initialization. The existing `CAPTURE_SETTLED` diagnostic discards two frames, with an 80 ms delay after each, before selecting the JPEG. Its name does not certify exposure convergence.

The Espressif [OV3660 driver](https://github.com/espressif/esp32-camera/blob/v2.0.4/sensors/ov3660.c) implements automatic exposure, automatic gain and automatic white balance controls. The installed firmware does not report exposure or gain register values. This comparison measures image output, not shutter duration or calibrated ISO sensitivity.

## Observations

Both explicit USB captures produced 1600 x 1200 JPEGs, received HTTP 201 with matching identifiers, and finished idle with an empty queue. The camera was not moved deliberately between captures. Lighting stability was not independently measured.

| Measurement | First Frame | After Two Preliminary Frames |
| --- | ---: | ---: |
| Sensor initialization | 363 ms | 363 ms |
| Time from capture start to selected framebuffer | 542 ms | 830 ms |
| Verified local storage | 1,104 ms | 2,812 ms |
| JPEG size | 67,299 bytes | 184,688 bytes |
| Mean grayscale value, scale 0 to 255 | 47.41 | 111.86 |
| Median grayscale value, scale 0 to 255 | 40 | 98 |
| Pixels with grayscale value at most 15 | 27.835% | 0.533% |
| Pixels with grayscale value at least 250 | 0% | 7.088% |

The grayscale measurements use Pillow `convert("L")` on the decoded originals and cover the whole image. These are encoded image values, not linear light measurements or exposure stops. The first capture identifier is `8a0202de3536793efdcb5c0e4a4c1d5a`; the second is `4659ea1ba3899965b98484c926d5ce19`. Both JPEGs have no EXIF entries. Local copies and the unadjusted side-by-side preview are under `private/camera-exposure-20260910/`, excluded from Git.

Visual inspection showed more visible shadow detail and a reduced green cast in the second image, alongside increased visible color noise and lost highlight detail. The additional wait to the selected framebuffer was 288 ms. Total acquisition and storage also increased because the second JPEG was larger; the 288 ms difference is not the entire delivery cost.

## Next Check

The result supports allowing automatic controls to adapt before selecting the photograph. It does not establish that two preliminary frames are sufficient across scenes or that both exposure time and gain changed in this pair. A firmware experiment should read the live exposure and gain registers across successive frames, confirm automatic-control enable bits, and compare dim and bright scenes before choosing the ordinary capture policy. Any conversion to milliseconds must use the verified sensor line timing; gain must not be labeled with invented ISO values.

The USB CLI now accepts `CAPTURE_SETTLED`, using the same delivery checks as `CAPTURE`. Its real-device execution passed. No firmware was changed or flashed during this comparison.

## Installed Update

Later on 10 September the owner requested installing automatic operation before testing the camera on battery. Revision `camera-2026-09-10-autoexposure` explicitly enables AEC, AGC and AWB and uses two preliminary frames for every capture path. This buys the shadow improvement observed above at the cost of additional acquisition time, storage work for larger JPEGs and potentially more noise or lost highlights. It is a fixed preliminary-frame policy, not an exposure-convergence detector. The firmware retains the driver's exposure target and gain limit rather than introducing unmeasured tuning values.

The PlatformIO build passed with 50,072 bytes of RAM and 992,485 bytes of program flash reported. The guarded updater verified the camera identity and backup, wrote and hash-verified the firmware, preserved LittleFS and confirmed fresh authenticated telemetry. An ordinary USB capture then reported `aec=1 agc=1 awb=1 warmup_frames=2`; its 82,116-byte 1600 x 1200 JPEG had identifier `acbbaedb21f2289b6d323b4609df91eb`. Sensor initialization took 365 ms, the selected framebuffer was ready at 831 ms, verified storage took 1,444 ms and upload took 776 ms. HTTP 201, a matching receipt, idle state and queue zero were observed. The door was open for this capture, so its lighting differs from the earlier comparison. Register-level exposure and gain measurement remains unimplemented, and physical battery tests remain with the owner.

## Button Failure After Installation

Later on 10 September the owner reported that pressing the shutter no longer started a capture. The camera was visible on USB and responded with `busy=0`, `queued=0` and `usb_test=0`. GPIO2 read LOW with pull-up enabled, pull-down disabled, input enabled and output disabled (`mux=0x1b00`). The owner confirmed that the physical button was released. The eight most recent inspected telemetry events also reported `buttonPressed=true`; these were retry/status operations with `captureRequested=false`, not eight new photographs.

A USB reset without a firmware write left GPIO2 LOW. At that point `last_capture=not_requested`, so the sensor and automatic controls had not been initialized since reset. One further physical press and full release, confirmed by the owner, left GPIO2 LOW and `last_capture=not_requested`. The firmware requires a released HIGH state before accepting a new falling edge while awake. These observations explain the rejected presses but do not locate a defective switch, wire or pin. The update did not change GPIO configuration or debounce. No polarity change or additional firmware flash was performed during diagnosis. Electrical isolation of the D1/GPIO2 shutter connection remains necessary; battery acceptance is unresolved.

The owner subsequently disconnected the shutter and confirmed that both USB and battery were disconnected for resistance measurements. They measured approximately 5 kohm between GPIO2 and GND; other pins read approximately 2 Mohm or 30 kohm, and the previously abandoned GPIO4 read approximately 0.2 Mohm, higher than an earlier reading. With power restored and the shutter still disconnected, GPIO2 remained around 0.9 V, including a battery-powered check. The owner clarified that USB VBUS measured 5 V and the regulated 3V3 output measured 3.3 V. These are user measurements, not instrument readings acquired by software. Resistance readings through an unpowered chip do not by themselves identify a failed component. The owner found no visible solder bridge and cleaned the board with isopropyl alcohol. No post-cleaning electrical test or minimal-firmware test was completed. A hardware fault is suspected but its location and cause remain unproven; prolonged USB connection has not been established as the cause.