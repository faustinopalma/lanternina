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

## 4. Answer the press while the finger is still on the button

**What it is.** A press starts a scan, and nothing on the display changes for about a
minute. The answer arrives at the display's *next* poll.

**Why it is first.** Measured on 19 August 2026: press at 14:33:06, scan finished 14:33:32,
display fetched at 14:34:11 and drew a few seconds later. Twenty-six seconds of that is the
scanner and cannot go; the rest is waiting for a poll and can. Somebody who presses and sees
nothing does the obvious thing — presses again and holds it down — and holding is what wipes
the Wi-Fi credentials (see §5). So this is not comfort. It is what removes the reason for
the dangerous gesture, and it goes before the firmware change rather than after.

**How.** The server already knows: `devices/trmnl_byos.py` reads `Update-Source` and sees
`EXT0` on the very request the press caused. Two things follow from that. It can serve a
"sto leggendo" screen in that same response instead of the one on disk, so the display
changes on the press itself. And it can answer that one request with a short
`refresh_rate` — a few seconds rather than thirty — so the result arrives shortly after the
scan instead of at the next ordinary poll. The device goes back to its usual spacing on the
following cycle by itself, because the rate is decided per request.

**What it costs.** A screen that exists only in the moment it is served, so the file on disk
and what the display shows disagree for one cycle. Worth watching: the scan writes the same
"sto leggendo" screen a moment later, and the two paths must not fight over the file.

**Where it starts.** `devices/trmnl_byos.py`, the `_display` handler where the press is
already recorded.

**Done when.** Pressing KEY3 changes the display within one refresh of the e-paper, and the
result appears without waiting for the ordinary poll.

---

## 5. Take the button's two destructive presses away

**What it is.** In the stock firmware, holding KEY3 wipes the Wi-Fi credentials, and holding
it longer wipes the device credentials. Both have to go from our build.

```c
case LongPress:   WifiCaptivePortal.resetSettings();
case SoftReset:   resetDeviceCredentials();
```

**Why now, and not as a matter of tidiness.** A short press is what starts a scan, and the
answer to it arrives at the display's *next* poll — up to seventy seconds later. So the
person who pressed sees nothing happen. The natural response, and a child's response in
particular, is to press again and hold it down, because perhaps it did not register. That
gesture is `LongPress`. The two defects are not independent: our own latency makes the
destructive press the likely one.

What it costs when it happens is not a rendering glitch. The display leaves the network and
cannot come back without a USB cable and somebody who knows how to use it. Whoever pressed
the button caused it and has no way to know that, or to undo it.

**How.** Two things, in this order, because the first removes the reason for the second to
happen. Answer the press immediately: `devices/trmnl_byos.py` already sees `Update-Source`,
so it can serve a "sto leggendo" screen in the same response rather than at the next poll,
and the firmware's own refresh rate can be shortened for one cycle after a press. Then take
the two cases out in `firmware/patches/`, where we already carry a patch of our own for
mDNS — replace both with `break`, and rebuild. Recovery does not disappear with them: the
hub holds every unit's 16 MiB original flash and can reprovision over USB, which is the
same cable the reset would have forced anyway.

**What it costs.** A firmware rebuild and a reflash of both units — an operation with real
risk on two devices that currently work, which is why it waits until the paper loop is
running rather than going first. And it is a fork of the vendor's behaviour: somebody
expecting a TRMNL to reset the way TRMNLs do will not find it. That is the intended trade.

**Where it starts.** `_reference/trmnl-firmware-v1.8.12/src/bl.cpp` around line 916, and
`firmware/patches/`.

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
