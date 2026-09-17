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

### Morning reading, 17 September 2026

The owner pressed BOOT on the morning of 17 September. The hub received the new `sleep_planned` report at 06:53:11.772668 CEST (04:53:11.772668 UTC). The report was read at 06:55:03 CEST, approximately 112 seconds after reception. Both voltage readings below come from the same report phase; no remote capture, reset or firmware update was requested for the comparison.

| Comparison field | Result |
| --- | --- |
| Baseline, 16 September 22:44:09.419109 CEST | 4.042741776 V nominal |
| Morning, 17 September 06:53:11.772668 CEST | 3.970161438 V nominal |
| Elapsed time between hub receipts | 29,342.353559 seconds, or 8 hours 9 minutes 2 seconds |
| Voltage decrease | 0.072580338 V, approximately 72.6 mV |
| Mean voltage decrease per elapsed hour | 8.90485 mV/hour |
| Morning boot | `9bd1dbe5`, previous boot `ef786bb8`, wake cause `boot_button` |
| Sleep evidence | Reset reason `deep_sleep`, previous marker confirmed, wake count increased from 4 to 5 |
| Morning final report | USB absent, no capture, zero sensor initialization, zero queued photographs |
| Periodic updates | Disabled, remembered interval 60 minutes |

The retained diagnostic history contains the baseline and then the morning BOOT reports, with no intervening report. The matching previous boot ID and increment of one in the wake counter support one overnight deep-sleep interval. The camera reported 29,492 seconds of sleep, about 150 seconds more than the interval between hub receipts. Use the hub timestamps for this comparison; the RTC duration has not been calibrated. Early morning reports mark USB present within the firmware's initial two-second detection grace period; the final report marks it absent. Those early flags alone do not establish a cable connection.

These two readings do not determine standby autonomy or consumed mAh. Voltage is nonlinear with remaining charge, the cell was recently charging before the baseline, and temperature, relaxation and the awake reporting load remain unmeasured. As an illustration only, choosing an unverified endpoint of 3.5 V and assuming the same constant voltage slope gives `(3.970161438 - 3.5) / 0.0089048486`, approximately 53 further hours. Neither that endpoint nor a constant slope has been established for this board and cell, so this number is not a measured or reliable remaining runtime.

A capacity-based estimate requires complete-board standby current and usable battery capacity: runtime in hours is usable capacity in mAh divided by mean current in mA. The advertised 3000 mAh is not a measured usable capacity at the board's cutoff. Measuring standby current would give a first estimate; a discharge test through the actual operational cutoff would establish runtime. Additional battery-only BOOT readings can show whether the observed voltage slope persists without claiming a percentage from voltage alone.

## PWR shutter and audio shutdown, 17 September 2026

The owner requested a firmware update to improve standby where justified and to use PWR for experiments before the external shutter is wired. PWR is read-only on GPIO15; it shares the power circuit, so the firmware keeps the existing battery latch enabled and adds no shutdown action. Its awake press uses the existing debounced capture path and requires release before rearming. The EXT1 mask includes GPIO0 and GPIO15; BOOT wins if both wake bits are present and continues to request status without capture. GPIO1 EXT0 remains the external shutter. This makes the onboard button usable immediately at the cost of a small control that is less accessible than the planned external button. GPIO15 is absent from the LCD connector; contact 15 is `TP_INT`, and the external shutter still belongs on contact 5/GPIO1.

The power LED has a fixed resistor path from 3.3 V as well as an expander-controlled path. The output was already LOW; the owner confirmed the LED remains visible on battery. Turning off the full battery latch would also prevent the existing sleep/wake behavior. No LED or resistor was altered. The improvement pursued in firmware was the unused ES7210 audio ADC: live register reads showed a different state from Espressif's documented stop sequence. The new firmware applies that sequence and verifies per-register readback. ES8311 already showed its expected power-down defaults, so it was left unchanged. The [evidence record](../docs/EVIDENCE.md#waveshare-power-and-controls-17-september-2026) links the source and identifies the measured limits. A different register state does not by itself demonstrate reduced current.

Installed revision `waveshare-2026-09-17-pwr-audio-sleep` passed build, upload hash, backup, filesystem and fresh authenticated-status checks. Source SHA-256 `00a7477216ef597755096cfdf8b6e33b3572d9f5d303fb3587ef20a49ec4a779` matches the installed hub source. All nine ES7210 readbacks passed; status retained the stopped state after capture. The XIAO source remained `ed21d9a8cba8e7d18745c0ede4818ff3aff36081045a2dec31083ffd28c4ddc1`. All six provisioning guard tests passed. Settings remain disabled with 60 minutes remembered, and no credential, filesystem format or cloud application change was made for this firmware update.

The owner's approximately two-second PWR press on USB produced one 117,402-byte JPEG, ID `d6021b6c002e198f77bf0dc4293fd301`. A battery-only press after 19 seconds of confirmed deep sleep produced one 66,633-byte JPEG, ID `3c14f1e503c73019dd2acef59d77c5e0`. Both decoded at 1600 x 1200 and matched stored digests, received HTTP 201 and left zero queued images. An additional 58,138-byte photograph, ID `242d4b206a493f1ebfa078a75d057d79`, initially failed the expected-count check; the event history showed another PWR wake, and the owner confirmed a separate intentional press. BOOT then woke as `boot_button` without capture or sensor initialization. The three intentional photographs increased the hub total from 143 to 146. The owner photographed a glass with protective film still on the lens; these are control and delivery checks, not an optical comparison.

The last battery-only `sleep_planned` report was received at 07:31:52.267252 CEST on 17 September, with nominal voltage 4.063306332 V, boot `1121a721` and periodic updates disabled. It follows USB charging, flashing and three captures and therefore starts a separate observation. The earlier overnight decline must not be compared directly as evidence of an improvement. The next battery reading can test a new voltage trend; measuring full-board sleep current or a discharge through the operating cutoff is still required to quantify autonomy. The external GPIO1 button and LED remain unwired and physically untested.
