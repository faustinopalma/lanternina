# The capture station

> **Superseded as a premise, 25 August 2026.** This entry was written when the camera was a
> scanner pointed at paper: a fixed station, a printed hood, four markers in frame, and a
> rule that only the crop inside them was ever kept. None of that is the design any more.
> The camera is handheld — a battery, one button, no screen, carried around — faces will be
> in frame, and what protects somebody is what may be inferred and what can be deleted. The
> ranking below still holds for anyone who wants a fixed station for a different reason, and
> the measurements in it are still measurements. `vision/` is empty: `read_sheet.py` and the
> cell half of `shared/vision_contracts.py` are in `attic/`, and a page is read by handing a
> model the blank and what came back.

The flatbed scanner already in the house stays: with its lid closed it physically cannot see anything but the sheet, which is a stronger guarantee than any camera can give. The station below is for the things a flatbed cannot take — a model, a plasticine animal, a drawing too big for the glass.

---

## 0. ~~A mark by hand reads as an empty box~~ — **closed, 19 August 2026**

Both of the two things this entry was waiting for happened within an hour of each other, and on the same sheet. The text below is left as it was written, because the measurement in it is still the evidence; what happened is at the end.

**What it is.** The two numbers that decide whether a cell counts as marked. Today `INK_PRESENT` is 0.04 and `INK_UNCERTAIN` is 0.02, both chosen before anything had been scanned.

**Why it is parked.** Counting ink in a rectangle is not how this system is meant to read a page. The reading will be done by a visual model looking at the rectified crop, and that model does not have a threshold to tune — it is handed a picture and says what is on it. So moving these two constants is work on a path we do not intend to keep, and the measurement below has already done the part that is worth keeping: it says what the present reader does and where it is wrong, which is what anybody comparing the two approaches will want.

The numbers stay where they are until something real goes wrong with them — a sheet that comes back read incorrectly in front of somebody, rather than a page marked on purpose to find the edge. Until then this is a known limit of a component on its way out, written down next to the evidence.

**What was measured, 19 August 2026.** A calibration sheet was printed, marked by hand and read back — `tools/make_calibration_sheet.py` and `attic/measure_calibration.py`, which moved to the attic on 21 August 2026 with the arithmetic it measures, and can still be run from the repository root.

| | measured |
| --- | --- |
| eight untouched boxes, centre and edges | **0.0000**, every one |
| a mark made deliberately outside a box | 0.0000 |
| printed areas, 1% to 32% of the box | ratio to true area constant at **≈1.6** |
| a light pencil mark | **0.0000** |
| an ordinary mark | **0.0121** |
| a cross | **0.0196** |
| a circle | 0.0242 |
| a filled box | 0.2647 |

The instrument is understood: 1.6 is `1/0.64`, the 10% inset per axis that `ink_fraction` applies, and it holds across five doublings. The inset also does its job — a mark just outside the lines reads as nothing, so neither the printed outline nor a stray is counted.

**Why it matters.** An ordinary mark and a cross both fall *below* 0.02, so today they are reported as an empty box. Not "somebody should look at this": empty. That is the confident wrong answer the whole design is arranged to avoid, and it is the one failure a person cannot detect, because an unread answer looks exactly like an unanswered question.

**How, if it is ever unparked.** Two different fixes, and only the first is a number. The floor is zero, so `INK_PRESENT` around 0.010 and `INK_UNCERTAIN` around 0.003 would put every hand-made mark on the right side with a wide margin. The light mark at 0.0000 is not an area problem at all: the page-wide Otsu threshold came out at 179, fitted to paper against printed black, and pale graphite falls on the paper side before anything is counted. That needs a threshold that knows it is looking for pencil, not a smaller number.

**What it costs.** One sheet is one sample. Before moving a threshold it is worth a second page — a light mark from a different pencil, and a sheet that has been handled — because the floor being exactly zero on clean paper says nothing about paper that has been carried around a house. That is a second reason to park rather than tune: the change would need evidence we have not gathered, for a reader we do not plan to keep.

**Where it starts.** `vision/read_sheet.py`, the two constants and `page_ink_threshold`.

**Done when.** Either the visual model does the reading and these constants stop mattering, or a real sheet comes back wrong and this is unparked with that sheet as the evidence.

### What happened, 19 August 2026

The first hand-written experience in the catalogue (`07 §1`) printed a sheet, somebody ticked four boxes, and the display said no boxes had been ticked. Measured on that page: **0.0172, 0.0136, 0.0129, 0.0164**, against empty cells at exactly **0.0000**. Three sheets now agree — marks between 0.0121 and 0.0196, paper at zero — and this one was not marked to find an edge. It was somebody answering four questions.

The constants moved to **0.010 / 0.003**, the numbers this entry had already worked out, and the same physical sheet then read `sole, dentro, acqua, veloce` with nothing in doubt.

Then the other exit condition was taken as well, because tuning was the wrong answer: the reader is now a vision model. `agents/sheet_reader.py` is the first implementation of the `VisionAgent` protocol, reached through a new panel route because the hub holds no Azure credential. On the same sheet it returned the same four choices and marked nothing doubtful, in **13.0 s** against the scanner's 37 s.

So the arithmetic is no longer the reader. It was what the house said when the cloud could not be reached, marked `degraded`, and on 21 August 2026 it stopped being that too: it is in `attic/`, and the rule is now **no cloud, no reading** — a page that comes back while the panel is unreachable waits. The two constants are recorded there with the sheets they were measured on.

**What is still true and still unfixed.** A light pencil mark read 0.0000 in the arithmetic, and no area threshold reached it: the page-wide Otsu threshold is fitted to printed black. That was the second reason to retire it. The model has not been tested on pencil, on a handled page, or on handwriting — it has been tested on one sheet, in pen, where it agreed with arithmetic that was also right. That is evidence the path works, not evidence it reads better.

---

## 1. The rig before the electronics

**What it is.** An inclined tray with a slot for the sheet, a fixed column, a hood over the lens, and one large button.

**Why.** Every hard problem in this pipeline is solved by geometry rather than by software. Fixed distance removes focus. A fixed tray removes framing, and with it the question of what else might be in the picture. A known light angle removes glare. A slot and a button remove the instructions.

**How.** Printed in matt black PETG, on a 2020 aluminium column so the height is rigid and adjustable during the first fitting, then fixed. The hood is the part that matters most: it restricts what the lens can see to the tray, so "it cannot see the room" stops depending on where somebody left it pointing.

**What it costs.** A day of printing and fitting, and the loss of the free-hand use — a drawing still on the wall does not go into a tray. That case is a different device and a different decision, recorded in the hardware notes.

**Where it starts.** `printing/` has nothing to do with this; it is CAD plus `shared/sheet.py` for the sheet dimensions the tray has to hold.

**Done when.** A sheet dropped in the slot lands in the same place twice, and a person standing beside the station does not appear in the frame.

---

## 2. Geometry, computed

The camera is a Raspberry Pi Camera Module 3, standard field of view. From the Raspberry Pi documentation, read 18 August 2026: sensor IMX708, 4608 × 2592, image area 6.45 × 3.63 mm, focal length 4.74 mm, **66° horizontal × 41° vertical**, F1.8, focus from about 10 cm.

The binding axis is the vertical one, because A4 is 210 mm across it:

| Quantity | Value | Where it comes from |
| --- | --- | --- |
| Lens height above the tray | **330 mm** | chosen, see below |
| Frame covered at that height | 429 × 247 mm | computed, `2·d·tan(FoV/2)` |
| A4 margin inside the frame | 66 mm long side, 18 mm short side | computed |
| Scale | **10,6 px/mm** | computed, 4608 px / 429 mm |
| ArUco module at 15 mm marker | 2,5 mm → **26 px** | computed; detection wants 4–5 px |

330 mm is not a minimum: 281 mm is the height at which A4 exactly fills the short axis, with no margin at all. The extra 49 mm buys the margin, and costs 2 px/mm of scale that we do not need. Focus is far outside the 10 cm limit, so autofocus can be locked once and left.

For comparison, the same page on the flatbed scanner already gives markers of 176–178 px against 177,2 expected, measured earlier in this project. The camera path does not have to beat that; it has to be good enough that detection never becomes the interesting problem.

---

## 3. Bill of materials

Prices are deliberately absent. Nothing here was chosen on cost, and the figures would be stale before they were useful. Availability is not verified either: these are properties and part names, to be checked against a supplier when ordering.

### The camera and the computer

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 1 | Raspberry Pi Camera Module 3, **standard** FoV | 1 | 66°×41° gives the geometry above. The Wide (102°) would need a lower column and would put the room's edges in frame — the opposite of what the hood is for. |
| 2 | Raspberry Pi Zero 2 W | 1 | Fixed station, always on, one toolchain with the hub. ArUco detection is classical vision, not a model, so it may run here; that keeps "only the crop leaves the device" true without an exception. |
| 3 | Camera cable, **Standard–Mini, 22-pin**, 300 mm | 1 | Every Pi Zero uses the mini 22-pin connector, confirmed in the Raspberry Pi documentation. The cable in the camera's box is the wrong one. |
| 4 | microSD, A2, high-endurance, 32 GB | 2 | One spare. The root filesystem is read-only, so endurance matters less than it looks, but a card that dies is the commonest way a Pi disappears. |
| 5 | Heatsink for Zero 2 W | 1 | Continuous idle with a camera attached; passive is enough. |

**The alternative worth knowing about.** HQ Camera (IMX477, 4056 × 3040, 4:3) with a 6 mm CS lens gives about 13 px/mm at a similar height, a sensor whose shape wastes less on a portrait page, and a focus ring that is locked mechanically rather than in software. It costs a heavier head, a stiffer column and a lens to choose. The gain is real but small: both are far above what ArUco needs. Take it if determinism is worth more than simplicity.

### The trigger and what it says back

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 6 | Arcade button, 60 mm, momentary, with LED ring, 5 V | 1 | Unmistakable, satisfying, and impossible to press by accident. The ring is the answer to "how do you know it worked" without a screen. |
| 7 | 2-pin JST leads, Dupont jumpers, heat-shrink | 1 set | GPIO with an internal pull-up. |
| 8 | Momentary button, 12 mm, panel mount | 1 | A shutdown button for the parent. Pulling power from a running Pi is how filesystems die. |

The ring says three things and no more: steady when ready, one slow pulse when the picture was taken, a slow amber when it could not be sent. Never a code, never red, never blaming.

There is no local retry, because there is no local storage — that is the point. So "it did not go" has to be visible immediately, and the answer is to press again.

### Light

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 9 | LED strip, **CRI ≥ 95**, 4000 K, 24 V constant voltage | 1 m | High CRI because the crop may be looked at by a person, and colour that lies is a poor record of a drawing. |
| 10 | 24 V PSU, **no PWM dimming** | 1 | The sensor has a rolling shutter. PWM at a few hundred hertz writes bands across the frame that look exactly like a bad exposure. A plain constant-voltage supply avoids the whole class of fault. |
| 11 | Aluminium LED channel with **frosted** cover | 2 × 250 mm | Diffusion is what stops the ink from producing a specular highlight straight into the lens. |
| 12 | Inline switch, 24 V | 1 | Light off is a legitimate state; nothing should be lit when nobody is there. |

Both channels sit at about 45° from the tray, on opposite sides. That angle is chosen to put the specular reflection outside the lens, and it is the one number worth re-measuring on the bench with a printed sheet rather than trusting from here.

### Structure

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 13 | 2020 aluminium extrusion, 500 mm | 1 | The column. Rigid, and it lets the height be tuned once during fitting and then fixed. |
| 14 | 2020 T-nuts M5 + button-head screws | 20 | |
| 15 | M2.5 heat-set inserts + screws, 6 mm | 20 | The Pi and the camera into printed parts. |
| 16 | M3 heat-set inserts + screws | 30 | Everything structural. |
| 17 | PETG filament, **matt black** | 1 kg | Matt black inside the hood: any glossy internal surface becomes a second light source pointed at the page. |
| 18 | TPU filament | 250 g | Feet, so the station does not walk on the table. |
| 19 | Adhesive rubber feet, non-slip mat | 1 | The tray must not move between the sheet going in and the button being pressed. |

Printed parts to design: tray with an A4 registration corner and a slot; column brackets; camera cradle; **lens hood**, the piece that decides what can be seen; two 45° light mounts; button housing; a cover for the Pi.

### Power and network

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 20 | 5 V 3 A micro-USB supply | 1 | The Zero 2 W is micro-USB, not USB-C. |
| 21 | micro-USB OTG → Ethernet adapter | 1 | Optional but preferred: a fixed station on a cable does not go missing when the Wi-Fi does. |
| 22 | Flat Ethernet cable | 1 | |

**The one-cable variant.** Raspberry Pi 5 with a PoE HAT and the same mini 22-pin cable gives power and network on one wire, and removes any doubt about memory when OpenCV is loaded. It costs a bigger box, active cooling and a PoE switch. Worth it if the station ends up somewhere without a socket.

### Consumables already in the house

Paper 80–90 g/m² matte, black-only printing at normal quality, and the ET-2870. All of this was settled earlier: the print → scan → detect chain is already proven end to end.

---

## 4. What is deliberately not on the list

| Not buying | Why not |
| --- | --- |
| Any camera that streams, or a doorbell-style module | The device must be a scanner. A camera that can stream is an observer whose software currently behaves. |
| PIR or radar presence sensor | There is no event in this system called "somebody is there". |
| Microphone, of any kind | Out of scope, and it must not arrive by accident inside a module bought for something else. |
| IR illuminator, NoIR camera | Nothing here needs to see in the dark. A camera that works with the lights off is a camera that works when nobody meant it to. |
| Jetson or any accelerator | Excluded by rule, not by cost: no model runs on the device. |
| Motorised anything — turntable, focus, pan | Movement invites watching. The station holds still. |

---

## 5. Two things left open

**The button as a power switch.** The CSI connector carries `CAM_IO0`, documented as an active-high power enable, so cutting the sensor's power between shots is not obviously impossible. It is also not obviously safe: the enable is driven by the host as part of a sequence, and a button in that path may simply produce a camera that fails to probe. Until somebody measures it, the hood is the guarantee and the button is only consent in software. Saying which of the two is load-bearing matters more than having both.

**Read-only root.** Overlayfs plus tmpfs makes "the station stores nothing" a property of the filesystem rather than of our care. It also removes the commonest cause of a dead Pi. The consequence is that a failed send is lost, which is why the button's ring has to say so.
