# Adding the Waveshare camera

Recorded on 16 September 2026 after the owner purchased ESP32-S3-CAM-OV5640, SKU 33699. The owner wants two cameras available for comparison. The initial work collected documentation; later that day the owner connected the new board to lanternina hub and authorized configuration. The independent Waveshare firmware was installed and two diagnostic captures were verified. The XIAO implementation and its credentials remain unchanged.

## Starting point

The [public board note](../docs/macchina-fotografica/waveshare-ov5640.md) names the sources, pin map, audio hardware and recovery requirements. The vendor material stays in the ignored `_reference/waveshare-esp32-s3-cam-ov5640/` archive. Source revisions and public download links allow another checkout to retrieve the same source even without that local collection.

The existing [XIAO camera project](../firmware/camera/README.md) remains the reference implementation. Its operational guide distinguishes current source from installed revisions and physical acceptance. Do not infer physical wiring or installed firmware from an older assembly diagram.

## Implementation boundary

Add a separate Waveshare firmware project or independently selected board target when implementation starts. Keep the existing target, its partition layout, pins, package versions and build output unchanged. This preserves an independently runnable comparison device at the cost of maintaining two board configurations. Factor shared behavior only after both implementations work and tests demonstrate that the extraction preserves the XIAO behavior.

The receiver already supports separate camera identities. Enroll the Waveshare under its own verified MAC and token, preserve the XIAO enrollment, and select a board-specific build and complete-flash backup by identity. An ESP32-S3 USB vendor/product ID alone does not distinguish these boards. The current flash command deliberately checks 8 MiB and must not be made permissive merely to accept the Waveshare's 16 MiB.

Preserve the upload contract: household authentication, distinct camera credentials, stable capture identifiers, durable matching receipts, retry behavior, deletion semantics and useful diagnostics. Measure full-resolution JPEG sizes before choosing the new queue's capacity. The current 750,000-byte limit is an engineering bound, not a measured limit for the new sensor.

The first board-specific work covered I2C/expander initialization, camera standby, PSRAM capture and identification. Two USB-powered camera checks established this path before battery behavior, optional display or audio are added. The onboard power button participates in the battery latch, so external controls use the separately selected LCD pins.

The owner chose an LCD breakout over the four-pin UART connection to retain deep sleep. The selected GPIO1 shutter and GPIO2 LED occupy LCD contacts 5 and 6, with ground on contact 3. This leaves camera, audio and microSD signals available, but prevents using a display on those same signals. The [wiring instructions](../docs/macchina-fotografica/waveshare-ov5640.md#external-button-and-led) require checking the cable's contact orientation and continuity before power. The board alone was verified; no external button or LED has been attached yet.

The implemented port uses the existing Arduino 2.0.17 camera API in a separately installed PlatformIO package directory. This retains the tested delivery behavior at the cost of not reproducing Waveshare's newer example environment. The physical 8 MB PSRAM declaration and Arduino's usable heap are different quantities: the first acceptance check incorrectly demanded exactly 8,388,608 heap bytes and was replaced by a bounded heap check, with a regression test using the observed 8,386,199 bytes. Esptool still independently checks the physical memory declaration.

Audio is an available capability, not a selected user-facing feature. Keep the amplifier controllable and retain the ES8311, ES7210 and NS4150B references. Playback and microphone capture can be evaluated separately. The future choice should depend on whether audible feedback helps the person taking the photograph and what it costs in current, latency and complexity.

## Acceptance

1. Record board revision, camera ribbon marking, lens mechanism, USB identity, MAC, detected flash and PSRAM. Verify the original backup's length and checksum before the first flash.
2. Verify successful initialization and sensor identification, returned JPEG format and dimensions, decoded originals, camera standby, failure reporting and restart recovery on USB power.
3. Compare the two cameras on the same subjects at fixed distance and lighting. Start with 1600 x 1200 output on both, then test each available maximum separately. Record firmware, settings, warm-up, focus, exposure, JPEG bytes and timings with each original. More pixels alone do not establish more usable detail.
4. Check that each camera uploads under its own identity, receives matching durable receipts, retries without duplicate processing, preserves queued images across an update and honors requested deletion. Keep authentication and household isolation intact.
5. Test physical shutter behavior, visible feedback and battery wake separately. Measure active and sleeping current at the complete board and calibrate battery voltage. A software sleep event is not a current measurement.
6. Test playback at a bounded volume only if audio is selected for evaluation. Check camera and audio coexistence before attributing failures to optics or exposure.

This preparation is complete when the source archive is verified and ignored, the public note identifies reproducible sources and untested claims, and the existing camera files remain unchanged. Hardware acceptance is a later task with the delivered board.

The [firmware operations guide](../firmware/camera-waveshare/README.md) records the complete 16 MiB original backup, installed revision and both USB capture measurements. The originals decoded at 1600 x 1200, with matching storage digests, HTTP 201 receipts and empty device queues. Both camera identities remain present on the receiver. External controls, timer wake and consumption, charging compatibility, full-resolution quality and offline/nonempty-queue update acceptance remain open. The connected 3000 mAh cell is above Waveshare's recommendation; its listing does not provide a consistent charging-current specification.

## Battery reporting and manual recovery

On 16 September the owner requested the correct camera name, battery reporting, optional periodic connections and recovery through at least one onboard button. The receiver previously labeled every camera as XIAO; it now selects the model from the reported board identity, with a firmware-prefix fallback for existing cameras. The Waveshare reports its expander ADC voltage through the existing authenticated status request. Nominal scaling makes a useful voltage available before calibration, at the cost of an unknown measurement error. The panel does not invent a remaining-charge percentage.

Periodic updates are disabled by default and retain a configurable 1-1440-minute interval in NVS. The parent choice passes through the inventory API and hub cache to the next camera status response. This preserves operation while the cloud is unavailable, but an already sleeping camera cannot receive a new choice until it reconnects. Timer wake reports status without capturing or draining the photograph queue. BOOT remains a separate manual wake even when the timer is disabled. PWR remains part of the hardware power circuit.

The firmware and receiver are installed. A brief BOOT press on USB produced a software restart; a subsequent battery-only press produced an EXT1 wake with a confirmed previous deep sleep of 63 seconds. No photograph was requested and the hub count remained 143. Battery conversion reported approximately 4.05-4.11 V. The XIAO source checksum remained `ed21d9a8cba8e7d18745c0ede4818ff3aff36081045a2dec31083ffd28c4ddc1`. The local API, inventory, transport and provisioning regression suite passed 41 tests; two focused interface tests and the production frontend build passed. The disable test first reproduced an invalid zero-minute request after clearing the draft; disabling now retains the saved interval.

A temporary one-minute setting produced an authenticated timer wake after 60 seconds of confirmed deep sleep, with no capture or sensor initialization and the same 143 photographs. After the hub restored disabled updates and the original 60-minute interval, no further report arrived for more than 122 seconds. The final USB readback was not performed. The owner approved publishing only these camera changes through the existing GitHub workflows, then explicitly authorized commit and push. An isolated staged-source copy passed 41 camera regression tests, repository-wide Ruff, two battery-form tests and the production build. Browser checks at 1440 and 390 pixels verified the supported-camera control, save and disable behavior, and no horizontal overflow. Current consumption and voltage calibration remain separate hardware measurements.

## Overnight battery observation, 16-17 September 2026

The owner left the camera disconnected from USB on the evening of 16 September and requested a comparison the next morning. This record was taken at 22:49:00 CEST (20:49:00 UTC). The latest authenticated reading was received at 22:44:09 CEST (20:44:09 UTC), 290.8 seconds before the record was made; no new measurement or wake was requested.

| Baseline field | Recorded value |
| --- | --- |
| Camera | Waveshare B16C08, MAC `28:84:85:B1:6C:08` |
| Battery | YUNIQUE 103665, advertised 1S 3.7 V, 3000 mAh |
| Firmware | `waveshare-2026-09-16-battery-timer` |
| Nominal voltage at 22:44:09 CEST | 4.042741776 V, approximately 4.043 V |
| Supply during the reading | USB absent; battery connected |
| Last boot and report | `ef786bb8`, timer wake, `sleep_planned` |
| Previous sleep | Confirmed deep-sleep marker, 61 seconds |
| Capture and queue | No capture requested, no sensor initialization, zero queued photographs |
| Hub battery setting | Updates disabled; remembered interval 60 minutes |
| Observation after the last report | No further report for 290.8 seconds |

The voltage is the firmware's nominal ADC conversion, not a calibrated charge percentage. The reported `ok` level uses generic voltage thresholds and does not quantify remaining capacity. Temperature, cell relaxation after charging and the load during transmission affect voltage; a voltage difference alone cannot establish consumed mAh or complete-board sleep current. The sleep-planned report also does not prove continuous sleep throughout the observation.

On the morning of 17 September, keep USB disconnected and press BOOT briefly once. Read the new authenticated battery-only report from the hub, record its timestamp and voltage, and compare the same report phase where possible. Calculate elapsed hours from the baseline reading at 22:44:09 CEST, then record the voltage difference and average mV per hour with these limitations. Record any intervening USB connection, button press or photograph because it changes the comparison. Leave the timer disabled overnight and do not flash, restart or otherwise wake the camera remotely during this observation.
