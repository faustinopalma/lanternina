# The e-paper displays

## 1. Quiet hours — built

**What it is.** The picture changes on a spacing the parent chooses, but not at night. The parent sets both ends of the pause, to the minute, and how many minutes pass between one picture and the next.

**Why.** E-paper emits no light, so it does not disturb sleep — but a night-time update spends battery on an image nobody will look at, and battery is the scarce resource. It is also the right way to say that the system follows the rhythm of the house rather than its own clock.

**How it was done.** The choice lives in Cosmos and is written from the panel's *Rhythm* section. The decision stays on the hub: `devices/pull_picture.py` reads the choice, and inside the quiet window it does not ask for a picture at all. Spacing is enforced against the screen file's own timestamp, so there is no second copy of the truth. If the panel cannot be reached the hub keeps working to its last known shape.

**What it cost.** The spacing is a count of minutes and both ends of the pause are written to the minute, so the timer had to become the thing that can honour them: it fires once a minute instead of once an hour. That is one small request to the panel per minute when no picture is due — 1440 a day, computed from the period and not measured — which is what a spacing of thirteen minutes costs. The comparison keeps a tolerance, now thirty seconds rather than ten minutes: without one, a run landing a second early skips its turn and thirteen minutes silently becomes fourteen. One limit is not ours to fix: on battery the display wakes about every ten minutes, so below that spacing some pictures are generated and nobody sees them. The panel says so next to the field rather than refusing the choice.

---

## 2. The freshness mark

**What it is.** A very small, discreet mark on the picture — a dot, a stroke — that changes with every update.

**Why.** It addresses the **silent liveness** gap: if the hub dies, the e-paper keeps its last image forever and everything looks normal. Nobody notices, and the system is dead without saying so.

**How.** Three options, in increasing order of intrusiveness: (a) nothing on the display, and the signal lives only in the parent's panel; (b) a stroke in the corner whose position varies, meaningless to a reader and meaningful to the parent; (c) a second observer — the Quieter 4C is already in the house and powered — that raises a flag when the hub goes quiet.

**What it costs.** Option (b) puts visual noise on an image meant to be pleasant. Option (a) is useless if the parent does not look at the panel. Option (c) is the only one that works without asking anything of anybody, and it costs one more service to maintain. Deciding is the parent's call, not a technical one.

---

## 3. Actually calibrating the battery

**What it is.** Discharging one cell once, recording the voltage every ten minutes, and deriving the real curve of this hardware.

**Why.** Today the 20% and 10% thresholds come from a generic LiPo curve. With this cell, this power draw and this firmware they could be off by a lot — and getting them wrong means either a warning that arrives far too early, or a display that dies without having said anything. It is the only thing in the whole system we can turn from an estimate into a measurement with one night of passive work.

**How.** The BYOS server already records `batteryVoltage` on every request. It is enough to let the display run on battery until it shuts down and then read the file. The only change needed is dropping the wake interval to ten minutes even at low charge, for that one run.

**What it costs.** One night, and a full discharge cycle on the cell. It should be done on the second kit when it arrives, not on the one in use.

---

## 4. Answer the press while the finger is still on the button — done, 19 August 2026

**What it was.** A press started a scan, and nothing on the display changed for about a minute. The answer arrived at the display's *next* poll.

**Why it was first.** Measured on 19 August 2026: press at 14:33:06, scan finished 14:33:32, display fetched at 14:34:11 and drew a few seconds later. Twenty-six seconds of that was the scanner and could not go; the rest was waiting for a poll. Somebody who presses and sees nothing does the obvious thing — presses again and holds it down — and holding is what wipes the Wi-Fi credentials (see §5). So this was not comfort. It removed the reason for the dangerous gesture, and it went before the firmware change rather than after.

**How it was done.** `devices/trmnl_byos.py` already read `Update-Source`, which is `EXT0` on the very request the press caused. Two things follow from that, and both are in the same response. The server serves a waiting screen held in memory instead of the file on disk, so the display changes on the press itself; and it answers that request with a short `refresh_rate`, so the result arrives shortly after the scan rather than at the next ordinary poll. The device goes back to its usual spacing by itself, because the rate is decided per request. The press stops being outstanding as soon as the display has been given something other than the waiting screen, and in any case after two minutes, so a scan that dies without writing anything cannot leave a display polling fast for ever.

The two paths were going to fight over the same file: the scan writes its own "Sto leggendo" about a second after the press. They now render from one definition — `render_waiting_bmp()` in `devices/epaper.py` — so the bytes are identical and the display has no reason to redraw between the two. The server compares the bytes rather than the timestamp for exactly this.

**What was measured, 19 August 2026, on the hub with the real scanner.** Press at 15:04:16, answered in that same response with the waiting screen and `refresh_rate=5`; scan finished 15:04:40; the result was served at 15:04:42. Twenty-six seconds from press to answer, of which twenty-four are the scanner. Before the change the same chain took 65 s and 71 s on the two units, and the difference was all poll waiting.

**The floor, stated with the numbers.** The immediate part is the waiting screen, not the result. Asking for a shorter cycle does not buy an instant one: with `refresh_rate=60` the two displays came back after 65 s and 71 s, so the firmware's own wake and reconnect costs 5 s to 11 s on top of whatever is requested. A press asks for 5 s, which means the result lands about ten seconds after the scan finishes.

**What it cost.** A screen that exists only while it is being served, so the file on disk and what the display shows disagree for one cycle. And one more file to keep on the hub — `/opt/lanternina/trmnl-waiting.bmp`, rendered from `render_waiting_bmp()` and pointed at by `TRMNL_WAITING_FILE`. Without it the press still shortens the poll; it just has nothing to put up straight away.

**Measured with a finger, 19 August 2026, on both units after the reflash.** Press at 16:34:22 on CF7D04: the waiting screen was served in that same second, the scan finished at 16:34:48 and the result was served at 16:34:57 — thirty-five seconds. Press at 16:40:53 on FB9F18: waiting screen in the same second, scan done at 16:41:20, result served at 16:41:29 — thirty-six seconds. Twenty-six and twenty-seven seconds of those are the scanner.

**The floor, corrected.** The nine seconds between the scan finishing and the result being served are one wake cycle. A press asks for five and the firmware adds six or seven of wake and reconnect, so the display comes back about every twelve seconds and the result waits for whichever of those lands first. The twenty-six seconds measured earlier over HTTP was the same chain with the scan finishing two seconds before a poll — a good draw, not the floor. The floor is the scanner plus up to one wake cycle: twenty-six to thirty-eight seconds. What is immediate is the waiting screen, and that part held with a finger on both units.

---

## 5. Take the button's two destructive presses away — done, 19 August 2026

**What it is.** In the stock firmware, holding KEY3 wipes the Wi-Fi credentials, and holding it longer wipes the device credentials. Both had to go from our build.

```c
case LongPress:   WifiCaptivePortal.resetSettings();
case SoftReset:   resetDeviceCredentials();
```

**Why now, and not as a matter of tidiness.** A short press is what starts a scan, and until §4 the answer to it arrived at the display's *next* poll — up to seventy seconds later. So the person who pressed saw nothing happen. The natural response, and a child's response in particular, is to press again and hold it down, because perhaps it did not register. That gesture is `LongPress`. The two defects were not independent: our own latency made the destructive press the likely one.

What it costs when it happens is not a rendering glitch. The display leaves the network and cannot come back without a USB cable and somebody who knows how to use it. Whoever pressed the button caused it and has no way to know that, or to undo it.

**What was done.** `firmware/patches/trmnl-v1.8.12-no-button-reset.patch` replaces both cases with a log line and a `break`. It applies to the same tree as the mDNS patch with `patch --binary -p1` — plain `patch` strips the carriage returns and then refuses every hunk, because the vendor's `bl.cpp` is CRLF. Built on the hub for `TRMNL_7inch5_OG_DIY_Kit`: RAM 17.2%, flash 72.0%, 1 415 105 bytes of 1 966 080. The check on the image itself is that the string `WiFi reset` is no longer in `firmware.bin` and `long press ignored` and `extra-long press ignored` are. The merged image is staged on the hub as `/opt/lanternina/firmware/trmnl-7inch5-og-diy-kit-no-button-reset.bin`.

The two remaining calls in the file are not reachable from the button: one is guarded by `BOARD_SEEED_XIAO_ESP32C3`, which this board is not, and the other is the reset the server can order with `reset_firmware`, which our server never sets and which is the way back rather than a hazard.

**What was proved, 19 August 2026.** Both units were reflashed, and both were then held down for about ten seconds — twice the five at which the stock firmware calls `WifiCaptivePortal.resetSettings()`. Neither left the network. CF7D04 went on answering from 192.168.0.140 at 16:34:34, 16:34:46 and 16:34:57; FB9F18 from 192.168.0.7 at 16:41:05, 16:41:17 and 16:41:29. The long press did the harmless thing in place of the destructive one: it woke the board, `Update-Source` came back `EXT0`, and a scan started. Nothing shows on the screen while the button is held, so the proof is the server's record rather than anything the person pressing can see.

**How a firmware change is made, because there will be more.** Both displays are wired to the hub over USB permanently, but a running unit is on the bus only while it is awake — measured on 19 August, about eight seconds in every sixty-seven. The two are never present at the same moment, which is why each takes the name `/dev/ttyACM0` in turn and why the port has to be found under `/dev/serial/by-id/...<MAC>-if00` and never by number.

The window is caught once rather than held open. `--wait-seconds N` polls for the port every 100 ms and starts esptool the instant it appears; the first connection leaves the chip in the ROM bootloader, where it does not sleep, so the rest of the flash has all the time it needs. Both units were caught on the first attempt. The whole gesture is one command:

```
cd /opt/lanternina && sudo python3 -m devices.trmnl_provision \
  --port /dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_<MAC>-if00 \
  --firmware /opt/lanternina/firmware/<image>.bin --force --wait-seconds 180
sudo /srv/lanternina/tools/platformio-venv/bin/python -m esptool --chip esp32s3 \
  --port /dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_<MAC>-if00 \
  --before default_reset --after hard_reset chip_id
```

The second command is not a recovery step. After writing, esptool prints `Hard resetting via RTS pin`, but on USB-JTAG that reset does not take: the chip stays in the bootloader, silent, with its port present and unmoving. CF7D04 looked dead for eight minutes that way. The tell is the port: a running unit makes it come and go, a stuck one leaves it there. The proof of life is the MAC in `/var/lib/lanternina/state/trmnl-status.json`, not the serial port.

`--force` is what makes the reflash a decision somebody took. Without it the provisioner returns "already provisioned" and writes nothing, which is what the udev rule runs when a cable is plugged in — so the re-enumeration that follows a flash cannot start a second flash with the older image. There is nothing to disarm beforehand and nothing to remember to put back. The registry is not edited: the token is left where it is, and `register_device` returns the one already there.

**Why not a development flag in the firmware that keeps the board awake.** It was considered and refused for three reasons. Installing it needs a flash, so the window has to be caught first anyway, and once that is done the flag adds nothing. It changes the thing under measurement: the wake overhead and `Update-Source: EXT0` exist because the board sleeps, so a board that stays awake stops being evidence about the loop we run. And a flag left on is invisible — on a display running from its cell it costs the battery, quietly, and the battery is the scarce resource.

**What it costs.** A reflash of two devices that currently work, which is why it waited until the paper loop was running. And it is a fork of the vendor's behaviour: somebody expecting a TRMNL to reset the way TRMNLs do will not find it. That is the intended trade.

**Done.** Both units flashed on 19 August 2026 with `trmnl-7inch5-og-diy-kit-no-button-reset.bin`, sha256 `c583a746a1b2…`, hash verified on each write. Ten seconds of holding leaves the display on the network, and a short press still starts a scan. The stock image stays on the hub as `trmnl-7inch5-og-diy-kit.bin` and the two 16 MiB original flashes stay in `/var/lib/lanternina/trmnl-backups/`.

---

## 6. The two displays do two jobs

**What it is.** One holds the day — the steps of the routine, the next big thing. The other holds the thing happening now, or the picture.

**Why.** They run on two different clocks: the day changes a few times and is glanced at; the picture changes often and is looked at for pleasure. Putting them on the same screen means every new picture erases the day.

**How.** The hub already decides which image each display is served; what is missing is somewhere to record what a display is for. A `role` field on the device record would do it: `panel/devices.py` holds id, name, charge, signal and firmware today, and nothing about the display's job. The rest of the chain does not change.

**What the first press showed, 19 August 2026.** A display's own file is created the first time it answers a press, and from then on it takes priority over the shared picture for good: `screen_for()` in `devices/trmnl_byos.py` says in as many words that a display with a job of its own stops following the picture. So one press converted the display that shows pictures into the display that shows sheets, permanently. The picture was never overwritten — it sat in `screen.bmp`, untouched, and nobody was looking at it any more. The file was removed by hand to put the picture back, and it will happen again at every press until a role exists. That is not a bug in the press: the answer belongs on the display somebody just pressed, because that is where they are looking. What is missing is anything that puts it back.

**The shape decided, 19 August 2026.** A display with no job assigned shows its own id, and nothing else. The parent sees the same ids listed in the panel and picks a job for each one, so matching a row to a thing on a shelf needs no cable, no log and no guessing — which is exactly what it cost today, when telling the two apart meant fetching both screen files off the hub and looking at them. The display learns its job when it next reaches the hub and acts on it from there. The role is set in the panel and pulled by the hub the way the rhythm already is, cached beside `rhythm.json`, so a panel that cannot be reached leaves the last known job in place.

What the role decides is only which display each producer writes for. The picture writes for the display whose job is the picture, and that is also what clears a leftover answer. Adding a third job later means adding a producer, not changing anything on the path to the glass.

**What it costs.** The second display is now connected and doing a job of its own — it stands by the printer and says what the sheet is for — but it does so because a file with its name on it exists, not because anything records what it is for. Writing the `role` field is worth it only because it costs one line; building the rest is not. The id on an unassigned screen is one more thing that has to be rendered, and it is the only screen in the system whose content is about the machine rather than about the person reading it. It earns that by being visible for as long as it takes the parent to choose, and no longer.

---

## 7. The display does not know what an error is

**What it is.** A rule already written, worth making impossible to break: no codes, no stack traces, no "connection failed", no red icons ever appear on the display.

**Why.** That screen is the one in the room. An error message says something is wrong and that it might be the reader's fault, and gives them nothing to do with that information. Faults are the parent's business.

**How.** Today it holds by construction: the device shows only an image the server produced. The defence worth adding is a test that fails if a rendering path is handed text that looks like an error — or, more simply, one that keeps the renderer accepting only content that has already been screened, as it does today.

**What it costs.** Nothing. It confirms a choice already made, and the value is in it still being true in six months.
