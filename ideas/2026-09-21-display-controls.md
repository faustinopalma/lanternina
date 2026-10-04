# Display Controls And Wi-Fi Recovery

The Lanternina firmware was installed on displays CF7D04 and FB9F18 on 21 September 2026. Both report `1.8.12-lanternina-20260921` through authenticated requests, with unchanged registry tokens. The firmware retries Wi-Fi indefinitely and assigns fixed, non-destructive actions to three programmable buttons. The fourth button is a hardware reset. On CF7D04, the owner confirmed the status screen, its automatic return to content, an 18-second KEY1 press without Wi-Fi setup, and KEY3 starting the paper-reading workflow. FB9F18 recovered from two interrupted USB writes and reconnected at 16:14:52 local hub time; no repeated physical acceptance tests were requested. A real Wi-Fi outage/recovery test has not been performed.

## Reason For The Change

The owner reported the upstream maximum-retries screen and requested USB-only maintenance, preserved Wi-Fi settings, Lanternina messages and useful functions for all four physical buttons. The earlier long-press patch removed two destructive actions, but the retry function still stopped its timer after three failures. Its message continued to tell the reader to hold a button to reset Wi-Fi.

The retry function now sleeps for 60 seconds, 180 seconds and then 300 seconds on subsequent failures. The counter saturates at three and a successful connection resets it. This preserves automatic recovery while bounding connection attempts; connection time is additional and energy consumption has not been measured. Wi-Fi failures retain the visible content. KEY2 provides connection information on request.

## Controls

The [Seeed Arduino guide](https://wiki.seeedstudio.com/ogdiy_kit_works_with_arduino/) describes three programmable buttons on D1, D2 and D4 plus a reset. Page 5 of the [vendor schematic](https://files.seeedstudio.com/wiki/XIAO_Gadget/TRMNL_Kit_Pic/XIAO_ePaper_driver_board_sch.pdf) connects BUTTON1 to GPIO2, BUTTON2 to GPIO3 and BUTTON3 to GPIO5. RESET connects to processor reset. The schematic's K1 is RESET; K2 through K4 are BUTTON1 through BUTTON3. An earlier conversation called RESET KEY4; that designation was corrected after reading the drawing. Identify RESET by its label.

| Control | Signal | Action |
| --- | --- | --- |
| KEY1 | GPIO2, BUTTON1 | Fetch and redraw the current content. |
| KEY2 | GPIO3, BUTTON2 | Show Lanternina, Wi-Fi signal, hub result, battery voltage and display identity. Request a return to content after a 60-second sleep. |
| KEY3 | GPIO5, BUTTON3 | Request the existing paper-reading workflow. |
| RESET | Processor reset | Restart with stored configuration intact. Holding it keeps the processor stopped until release. |

These choices retain the established paper workflow and add two local controls without changing the hub protocol. KEY1 and KEY2 send `lanternina-refresh` and `lanternina-status`. KEY3 retains `EXT0`, which the hub recognizes as a paper-reading request. The ESP32-S3 uses EXT1 ANY_LOW to wake from the three GPIOs. A button held at sleep entry is omitted from that wake mask to prevent immediate repeated wakes; it is rearmed at a later scheduled wake after release. Other buttons and the timer remain available. Presses during active work are not queued. Failed KEY3 requests are not saved for later replay.

The target bypasses the upstream press-duration interpreter, captive portal, remote configuration reset and network firmware update. Maintenance uses explicit USB provisioning. The hub continues to supply images and polling intervals over Wi-Fi. Missing Wi-Fi configuration shows a Lanternina instruction to connect USB to the hub. Battery readings use the existing ADC path and report volts, not a calibrated percentage. The status screen remains visible until a successful later poll restores content.

## Rebuild And Verify

Start from upstream commit `57fa074c280418b5b2729613ce0c181d552b72a7` and apply these patches in order. `--ignore-space-change` accommodates historical CRLF context:

```sh
git apply --ignore-space-change /path/to/firmware/patches/trmnl-v1.8.12-mdns-byos.patch
git apply --ignore-space-change /path/to/firmware/patches/trmnl-v1.8.12-no-button-reset.patch
git apply --ignore-space-change /path/to/firmware/patches/trmnl-v1.8.12-real-battery.patch
git apply --ignore-space-change /path/to/firmware/patches/trmnl-v1.8.12-lanternina-controls.patch
python3 /path/to/firmware/check-trmnl.py .
PATH=/srv/lanternina/tools/platformio-venv/bin:$PATH pio run -e TRMNL_7inch5_OG_DIY_Kit
```

The host check requires `g++`. It executes extracted firmware functions with fake hardware boundaries: 1,000 consecutive Wi-Fi failures, six stale counter values, all eight held-button masks, three commands, the legacy KEY3 fallback and framebuffer allocation success/failure. A deliberately mutated button-only sleep path fails the same check. The HTTP regression `python -m pytest tests/test_trmnl_byos.py -q -k short_press` confirms that timer, refresh and status do not create scanner requests, while KEY3 does. The test and Python lint passed. These checks do not emulate the radio or e-paper panel.

All four patches applied to an isolated upstream archive. The five files changed by the new patch matched the compiled tree after line-ending normalization; the real-battery header differed only in an older comment. The binary contained the Lanternina version and title and no old maximum-retries or hold-to-reset instructions. The actual display library defines `BBEP_SUCCESS` as zero; the renderer compares the allocation result explicitly. Wi-Fi RSSI is captured before the image downloader switches off the radio.

The build used Espressif32 6.12.0, Arduino ESP32 2.0.17 and esptool 4.9.0 on the hub. The application occupied 1,281,973 bytes of its 1,966,080-byte partition, with 55,776 bytes of static RAM. These are build measurements, not peak runtime memory. The separate build directory is `/srv/lanternina/build/trmnl-lanternina-20260921`. The previous build and battery-patched image remain unchanged.

## Installation Evidence

The hub identified `94:A9:90:CF:7D:04` on USB at 13:55:51 local hub time on 21 September 2026; it disconnected eight seconds later when it slept. Earlier RESET attempts produced no USB event. Reconnecting the cable and pressing RESET made identification possible. The original backup has 16,777,216 bytes, mode 0600 and SHA-256 `21f02f7b2085cca56267336415dff1c566eadf1229795b0875baea97e2841eca`. The registry was copied to the root-only `/var/lib/lanternina/trmnl-devices-before-20260921.json` before flashing. Wi-Fi configuration and the mDNS hub URL were validated without printing secrets.

The installed merged image is `/opt/lanternina/firmware/trmnl-7inch5-lanternina-20260921.bin`, SHA-256 `7ed1fe02881f21cfd8c50539e1f75af4544f73fb8191bc006bf9e75c9c1d59fe`. The existing provisioner targeted the MAC-specific USB path with `--force --registered-only --wait-seconds 240`. Esptool verified 1,347,984 bytes at `0x0` and 20,480 bytes of generated Wi-Fi NVS at `0x9000`. The explicit `--before usb_reset --after hard_reset run` followed. The hub then received firmware `1.8.12-lanternina-20260921`, RSSI -46 dBm and battery voltage 4.15 V. The full registry matched its pre-flash copy, including both device tokens. FB9F18 continued reporting `1.8.12`.

The owner confirmed that KEY2 displayed Lanternina, Wi-Fi, battery and identity. The owner then held KEY1 for 18 seconds and confirmed that content returned without Wi-Fi setup. The hub recorded `lanternina-refresh` with the new version and served the display and bitmap endpoints with HTTP 200. The owner also confirmed that KEY2 returned automatically to content without another press, and that KEY3 started paper reading. The final check at 15:47:11 local hub time found the registry and original backup unchanged and CF7D04 still reporting the new version. These checks establish the three physical commands and preserved connectivity after that long press. They do not establish every possible button combination or a real outage recovery.

### Second Display

The hub identified `E8:3D:C1:FB:9F:18` on USB at 15:51:49 local hub time. Its original backup, `/var/lib/lanternina/trmnl-backups/E83DC1FB9F18.bin`, has 16,777,216 bytes, mode 0600 and SHA-256 `67a0c7e2772ebb601b38d471956ccc8f2efa3b6c6dbb189e75bff9aa8e70b511`. The root-only registry snapshot is `/var/lib/lanternina/trmnl-devices-before-FB9F18-20260921.json`. Enrollment, Wi-Fi configuration, hub URL and the release image hash were checked before writing.

An initial 240-second wait expired without writing. A later attempt caught USB at 16:03:42 but lost the connection at 96% of the merged-image write. A second attempt after reconnecting the cable lost USB at 17%. Neither attempt reached NVS provisioning. Kernel events confirmed the disconnections; they do not establish whether the first interruption coincided with a physical reset. The hub reported no undervoltage flags, and the automatic provisioning service did not force updates of enrolled displays.

The intermediate USB hub `4-1` had runtime power control `auto` and was suspended. Setting its `power/control` to `on` at 16:10:20 was followed by enumeration at 16:10:21 and continuous USB presence through the next check at 16:14:03. The target USB device's power control was also set to `on` before the successful write. This sequence supports disabling USB runtime suspension during recovery; it is not a controlled proof of the cause of both interruptions. The owner's board had no physical button at the module's B marking. An instruction inferred from a vendor photograph to press that marking was withdrawn. Recovery used USB programming without a confirmed manual BOOT sequence.

The existing provisioner then verified the complete 1,347,984-byte merged image at `0x0` and the 20,480-byte generated NVS at `0x9000`. The explicit bootloader-exit command completed at 16:14:31. Setup and bitmap requests returned HTTP 200 at 16:14:46. An authenticated display request and another bitmap request returned HTTP 200 at 16:14:52, with firmware `1.8.12-lanternina-20260921`, RSSI -49 dBm and battery voltage 4.16 V. The full registry matched the second pre-flash snapshot and the original backup hash was unchanged. CF7D04 still reported the same release. The hub's original `auto` power policy was restored and no provisioning process remained at 16:15:09. These times are measured hub-local times on 21 September 2026.

## Maintenance And Remaining Checks

For future FB9F18 maintenance, explicitly select `/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_E8:3D:C1:FB:9F:18-if00`, verify its original backup and enrollment, and use the checked image with the existing provisioner. Keep physical buttons and the cable untouched while a provisioner is armed or writing: a timer wake can start the flash before a manual wake is attempted. Always write the generated NVS after the merged image, leave the ROM bootloader explicitly, compare registry identities and check authenticated telemetry. If USB drops during writing, inspect runtime suspension on the identified device and its parent hub before retrying, record prior settings and restore temporary changes after recovery. The older wrapper defaults to the previous build path and must not be used unchanged for this release. Do not update udev defaults or flash an unknown device.

A real Wi-Fi outage/recovery trial remains to be recorded. No router-wide interruption was performed. The firmware's retries are verified by executing its logic beyond the old stopping point; that is not a measured radio recovery trial.