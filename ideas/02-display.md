# The e-paper displays

## 1. Quiet hours — built

**What it is.** The picture changes on a spacing the parent chooses, but not at night. The
parent sets both ends of the pause, to the minute, and how many minutes pass between one
picture and the next.

**Why.** E-paper emits no light, so it does not disturb sleep — but a night-time update
spends battery on an image nobody will look at, and battery is the scarce resource. It is
also the right way to say that the system follows the rhythm of the house rather than its
own clock.

**How it was done.** The choice lives in Cosmos and is written from the panel's *Rhythm*
section. The decision stays on the hub: `devices/pull_picture.py` reads the choice, and
inside the quiet window it does not ask for a picture at all. Spacing is enforced against
the screen file's own timestamp, so there is no second copy of the truth. If the panel
cannot be reached the hub keeps working to its last known shape.

**What it cost.** The spacing is a count of minutes and both ends of the pause are written
to the minute, so the timer had to become the thing that can honour them: it fires once a
minute instead of once an hour. That is one small request to the panel per minute when no
picture is due — 1440 a day, computed from the period and not measured — which is what a
spacing of thirteen minutes costs. The comparison keeps a tolerance, now thirty seconds
rather than ten minutes: without one, a run landing a second early skips its turn and
thirteen minutes silently becomes fourteen. One limit is not ours to fix: on battery the
display wakes about every ten minutes, so below that spacing some pictures are generated
and nobody sees them. The panel says so next to the field rather than refusing the choice.

---

## 2. The freshness mark

**What it is.** A very small, discreet mark on the picture — a dot, a stroke — that changes
with every update.

**Why.** It addresses the **silent liveness** gap: if the hub dies, the e-paper keeps its
last image forever and everything looks normal. Nobody notices, and the system is dead
without saying so.

**How.** Three options, in increasing order of intrusiveness: (a) nothing on the display,
and the signal lives only in the parent's panel; (b) a stroke in the corner whose position
varies, meaningless to a reader and meaningful to the parent; (c) a second observer — the
Quieter 4C is already in the house and powered — that raises a flag when the hub goes
quiet.

**What it costs.** Option (b) puts visual noise on an image meant to be pleasant. Option (a)
is useless if the parent does not look at the panel. Option (c) is the only one that works
without asking anything of anybody, and it costs one more service to maintain. Deciding is
the parent's call, not a technical one.

---

## 3. Actually calibrating the battery

**What it is.** Discharging one cell once, recording the voltage every ten minutes, and
deriving the real curve of this hardware.

**Why.** Today the 20% and 10% thresholds come from a generic LiPo curve. With this cell,
this power draw and this firmware they could be off by a lot — and getting them wrong means
either a warning that arrives far too early, or a display that dies without having said
anything. It is the only thing in the whole system we can turn from an estimate into a
measurement with one night of passive work.

**How.** The BYOS server already records `batteryVoltage` on every request. It is enough to
let the display run on battery until it shuts down and then read the file. The only change
needed is dropping the wake interval to ten minutes even at low charge, for that one run.

**What it costs.** One night, and a full discharge cycle on the cell. It should be done on
the second kit when it arrives, not on the one in use.

---

## 4. Answer the press while the finger is still on the button — done, 19 August 2026

**What it was.** A press started a scan, and nothing on the display changed for about a
minute. The answer arrived at the display's *next* poll.

**Why it was first.** Measured on 19 August 2026: press at 14:33:06, scan finished 14:33:32,
display fetched at 14:34:11 and drew a few seconds later. Twenty-six seconds of that was the
scanner and could not go; the rest was waiting for a poll. Somebody who presses and sees
nothing does the obvious thing — presses again and holds it down — and holding is what wipes
the Wi-Fi credentials (see §5). So this was not comfort. It removed the reason for the
dangerous gesture, and it went before the firmware change rather than after.

**How it was done.** `devices/trmnl_byos.py` already read `Update-Source`, which is `EXT0` on
the very request the press caused. Two things follow from that, and both are in the same
response. The server serves a waiting screen held in memory instead of the file on disk, so
the display changes on the press itself; and it answers that request with a short
`refresh_rate`, so the result arrives shortly after the scan rather than at the next ordinary
poll. The device goes back to its usual spacing by itself, because the rate is decided per
request. The press stops being outstanding as soon as the display has been given something
other than the waiting screen, and in any case after two minutes, so a scan that dies without
writing anything cannot leave a display polling fast for ever.

The two paths were going to fight over the same file: the scan writes its own "Sto leggendo"
about a second after the press. They now render from one definition — `render_waiting_bmp()`
in `devices/epaper.py` — so the bytes are identical and the display has no reason to redraw
between the two. The server compares the bytes rather than the timestamp for exactly this.

**What was measured, 19 August 2026, on the hub with the real scanner.** Press at 15:04:16,
answered in that same response with the waiting screen and `refresh_rate=5`; scan finished
15:04:40; the result was served at 15:04:42. Twenty-six seconds from press to answer, of
which twenty-four are the scanner. Before the change the same chain took 65 s and 71 s on the
two units, and the difference was all poll waiting.

**The floor, stated with the numbers.** The immediate part is the waiting screen, not the
result. Asking for a shorter cycle does not buy an instant one: with `refresh_rate=60` the
two displays came back after 65 s and 71 s, so the firmware's own wake and reconnect costs
5 s to 11 s on top of whatever is requested. A press asks for 5 s, which means the result
lands about ten seconds after the scan finishes.

**What it cost.** A screen that exists only while it is being served, so the file on disk and
what the display shows disagree for one cycle. And one more file to keep on the hub —
`/opt/lanternina/trmnl-waiting.bmp`, rendered from `render_waiting_bmp()` and pointed at by
`TRMNL_WAITING_FILE`. Without it the press still shortens the poll; it just has nothing to
put up straight away.

**The limit.** The press in the measurement above was made over HTTP with the header the
firmware sends, not with a finger. The physical part of the chain — KEY3 wakes the board and
`Update-Source` comes back as `EXT0` — was measured on 19 August and is not what changed.
Somebody should still press the button once and watch the screen.

---

## 5. Take the button's two destructive presses away — patched and built, 19 August 2026, not yet flashed

**What it is.** In the stock firmware, holding KEY3 wipes the Wi-Fi credentials, and holding
it longer wipes the device credentials. Both had to go from our build.

```c
case LongPress:   WifiCaptivePortal.resetSettings();
case SoftReset:   resetDeviceCredentials();
```

**Why now, and not as a matter of tidiness.** A short press is what starts a scan, and until
§4 the answer to it arrived at the display's *next* poll — up to seventy seconds later. So
the person who pressed saw nothing happen. The natural response, and a child's response in
particular, is to press again and hold it down, because perhaps it did not register. That
gesture is `LongPress`. The two defects were not independent: our own latency made the
destructive press the likely one.

What it costs when it happens is not a rendering glitch. The display leaves the network and
cannot come back without a USB cable and somebody who knows how to use it. Whoever pressed
the button caused it and has no way to know that, or to undo it.

**What was done.** `firmware/patches/trmnl-v1.8.12-no-button-reset.patch` replaces both cases
with a log line and a `break`. It applies to the same tree as the mDNS patch with
`patch --binary -p1` — plain `patch` strips the carriage returns and then refuses every hunk,
because the vendor's `bl.cpp` is CRLF. Built on the hub for `TRMNL_7inch5_OG_DIY_Kit`: RAM
17.2%, flash 72.0%, 1 415 105 bytes of 1 966 080. The check on the image itself is that the
string `WiFi reset` is no longer in `firmware.bin` and `long press ignored` and `extra-long
press ignored` are. The merged image is staged on the hub as
`/opt/lanternina/firmware/trmnl-7inch5-og-diy-kit-no-button-reset.bin`.

The two remaining calls in the file are not reachable from the button: one is guarded by
`BOARD_SEEED_XIAO_ESP32C3`, which this board is not, and the other is the reset the server
can order with `reset_firmware`, which our server never sets and which is the way back rather
than a hazard.

**What is left, and it is physical.** The staged image is deliberately *not* the one the
provisioner uses. udev flashes a display the moment it is plugged in, so swapping the file
first would turn the next cable into a decision nobody took. The order is: swap
`/opt/lanternina/firmware/trmnl-7inch5-og-diy-kit.bin`, plug in one display, check it comes
back on the network and still scans, hold the button ten seconds and check it is still there,
and only then the second unit. Recovery does not depend on any of that going well: the hub
holds 16 MiB of original flash for both units in `/var/lib/lanternina/trmnl-backups/`, and
`trmnl_provision.py` reprovisions over USB.

**What it costs.** A reflash of two devices that currently work, which is why it waited until
the paper loop was running. And it is a fork of the vendor's behaviour: somebody expecting a
TRMNL to reset the way TRMNLs do will not find it. That is the intended trade.

**Done when.** Holding KEY3 for ten seconds leaves the display on the network, and a short
press still starts a scan.

---

## 6. The two displays do two jobs

**What it is.** One holds the day — the steps of the routine, the next big thing. The other
holds the thing happening now, or the picture.

**Why.** They run on two different clocks: the day changes a few times and is glanced at;
the picture changes often and is looked at for pleasure. Putting them on the same screen
means every new picture erases the day.

**How.** The hub already decides which image each display is served; what is missing is
somewhere to record what a display is for. A `role` field on the device record would do it:
`panel/devices.py` holds id, name, charge, signal and firmware today, and nothing about the
display's job. The rest of the chain does not change.

**What it costs.** The second display is now connected and doing a job of its own — it
stands by the printer and says what the sheet is for — but it does so because a file with
its name on it exists, not because anything records what it is for. Writing the `role`
field is worth it only because it costs one line; building the rest is not.

---

## 7. The display does not know what an error is

**What it is.** A rule already written, worth making impossible to break: no codes, no stack
traces, no "connection failed", no red icons ever appear on the display.

**Why.** That screen is the one in the room. An error message says something is wrong and
that it might be the reader's fault, and gives them nothing to do with that information.
Faults are the parent's business.

**How.** Today it holds by construction: the device shows only an image the server produced.
The defence worth adding is a test that fails if a rendering path is handed text that looks
like an error — or, more simply, one that keeps the renderer accepting only content that has
already been screened, as it does today.

**What it costs.** Nothing. It confirms a choice already made, and the value is in it still
being true in six months.
