# The capture station

The camera in this system is a scanner pointed at paper. It is not an observer: it looks at
a tray, it fires on a button press, and what it can see is limited by a printed hood rather
than by a promise in the code.

`vision/` is empty today. `shared/vision_contracts.py` already holds the shape of the
answer — `RawFrame` refuses to be pickled, copied or serialised and wipes its buffer on
exit; only `RectifiedPage` gets out. What is missing is everything that produces a frame.

The flatbed scanner already in the house stays: with its lid closed it physically cannot
see anything but the sheet, which is a stronger guarantee than any camera can give. The
station below is for the things a flatbed cannot take — a model, a plasticine animal, a
drawing too big for the glass.

---

## 1. The rig before the electronics

**What it is.** An inclined tray with a slot for the sheet, a fixed column, a hood over the
lens, and one large button.

**Why.** Every hard problem in this pipeline is solved by geometry rather than by software.
Fixed distance removes focus. A fixed tray removes framing, and with it the question of
what else might be in the picture. A known light angle removes glare. A slot and a button
remove the instructions.

**How.** Printed in matt black PETG, on a 2020 aluminium column so the height is rigid and
adjustable during the first fitting, then fixed. The hood is the part that matters most: it
restricts what the lens can see to the tray, so "it cannot see the room" stops depending on
where somebody left it pointing.

**What it costs.** A day of printing and fitting, and the loss of the free-hand use — a
drawing still on the wall does not go into a tray. That case is a different device and a
different decision, recorded in the hardware notes.

**Where it starts.** `printing/` has nothing to do with this; it is CAD plus
`shared/sheet.py` for the sheet dimensions the tray has to hold.

**Done when.** A sheet dropped in the slot lands in the same place twice, and a person
standing beside the station does not appear in the frame.

---

## 2. Geometry, computed

The camera is a Raspberry Pi Camera Module 3, standard field of view. From the Raspberry Pi
documentation, read 18 August 2026: sensor IMX708, 4608 × 2592, image area 6.45 × 3.63 mm,
focal length 4.74 mm, **66° horizontal × 41° vertical**, F1.8, focus from about 10 cm.

The binding axis is the vertical one, because A4 is 210 mm across it:

| Quantity | Value | Where it comes from |
| --- | --- | --- |
| Lens height above the tray | **330 mm** | chosen, see below |
| Frame covered at that height | 429 × 247 mm | computed, `2·d·tan(FoV/2)` |
| A4 margin inside the frame | 66 mm long side, 18 mm short side | computed |
| Scale | **10,6 px/mm** | computed, 4608 px / 429 mm |
| ArUco module at 15 mm marker | 2,5 mm → **26 px** | computed; detection wants 4–5 px |

330 mm is not a minimum: 281 mm is the height at which A4 exactly fills the short axis,
with no margin at all. The extra 49 mm buys the margin, and costs 2 px/mm of scale that we
do not need. Focus is far outside the 10 cm limit, so autofocus can be locked once and left.

For comparison, the same page on the flatbed scanner already gives markers of 176–178 px
against 177,2 expected, measured earlier in this project. The camera path does not have to
beat that; it has to be good enough that detection never becomes the interesting problem.

---

## 3. Bill of materials

Prices are deliberately absent. Nothing here was chosen on cost, and the figures would be
stale before they were useful. Availability is not verified either: these are properties
and part names, to be checked against a supplier when ordering.

### The camera and the computer

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 1 | Raspberry Pi Camera Module 3, **standard** FoV | 1 | 66°×41° gives the geometry above. The Wide (102°) would need a lower column and would put the room's edges in frame — the opposite of what the hood is for. |
| 2 | Raspberry Pi Zero 2 W | 1 | Fixed station, always on, one toolchain with the hub. ArUco detection is classical vision, not a model, so it may run here; that keeps "only the crop leaves the device" true without an exception. |
| 3 | Camera cable, **Standard–Mini, 22-pin**, 300 mm | 1 | Every Pi Zero uses the mini 22-pin connector, confirmed in the Raspberry Pi documentation. The cable in the camera's box is the wrong one. |
| 4 | microSD, A2, high-endurance, 32 GB | 2 | One spare. The root filesystem is read-only, so endurance matters less than it looks, but a card that dies is the commonest way a Pi disappears. |
| 5 | Heatsink for Zero 2 W | 1 | Continuous idle with a camera attached; passive is enough. |

**The alternative worth knowing about.** HQ Camera (IMX477, 4056 × 3040, 4:3) with a 6 mm
CS lens gives about 13 px/mm at a similar height, a sensor whose shape wastes less on a
portrait page, and a focus ring that is locked mechanically rather than in software. It
costs a heavier head, a stiffer column and a lens to choose. The gain is real but small:
both are far above what ArUco needs. Take it if determinism is worth more than simplicity.

### The trigger and what it says back

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 6 | Arcade button, 60 mm, momentary, with LED ring, 5 V | 1 | Unmistakable, satisfying, and impossible to press by accident. The ring is the answer to "how do you know it worked" without a screen. |
| 7 | 2-pin JST leads, Dupont jumpers, heat-shrink | 1 set | GPIO with an internal pull-up. |
| 8 | Momentary button, 12 mm, panel mount | 1 | A shutdown button for the parent. Pulling power from a running Pi is how filesystems die. |

The ring says three things and no more: steady when ready, one slow pulse when the picture
was taken, a slow amber when it could not be sent. Never a code, never red, never blaming.

There is no local retry, because there is no local storage — that is the point. So "it did
not go" has to be visible immediately, and the answer is to press again.

### Light

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 9 | LED strip, **CRI ≥ 95**, 4000 K, 24 V constant voltage | 1 m | High CRI because the crop may be looked at by a person, and colour that lies is a poor record of a drawing. |
| 10 | 24 V PSU, **no PWM dimming** | 1 | The sensor has a rolling shutter. PWM at a few hundred hertz writes bands across the frame that look exactly like a bad exposure. A plain constant-voltage supply avoids the whole class of fault. |
| 11 | Aluminium LED channel with **frosted** cover | 2 × 250 mm | Diffusion is what stops the ink from producing a specular highlight straight into the lens. |
| 12 | Inline switch, 24 V | 1 | Light off is a legitimate state; nothing should be lit when nobody is there. |

Both channels sit at about 45° from the tray, on opposite sides. That angle is chosen to
put the specular reflection outside the lens, and it is the one number worth re-measuring
on the bench with a printed sheet rather than trusting from here.

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

Printed parts to design: tray with an A4 registration corner and a slot; column brackets;
camera cradle; **lens hood**, the piece that decides what can be seen; two 45° light
mounts; button housing; a cover for the Pi.

### Power and network

| # | Item | Qty | Why this one |
| --- | --- | --- | --- |
| 20 | 5 V 3 A micro-USB supply | 1 | The Zero 2 W is micro-USB, not USB-C. |
| 21 | micro-USB OTG → Ethernet adapter | 1 | Optional but preferred: a fixed station on a cable does not go missing when the Wi-Fi does. |
| 22 | Flat Ethernet cable | 1 | |

**The one-cable variant.** Raspberry Pi 5 with a PoE HAT and the same mini 22-pin cable
gives power and network on one wire, and removes any doubt about memory when OpenCV is
loaded. It costs a bigger box, active cooling and a PoE switch. Worth it if the station
ends up somewhere without a socket.

### Consumables already in the house

Paper 80–90 g/m² matte, black-only printing at normal quality, and the ET-2870. All of this
was settled earlier: the print → scan → detect chain is already proven end to end.

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

**The button as a power switch.** The CSI connector carries `CAM_IO0`, documented as an
active-high power enable, so cutting the sensor's power between shots is not obviously
impossible. It is also not obviously safe: the enable is driven by the host as part of a
sequence, and a button in that path may simply produce a camera that fails to probe. Until
somebody measures it, the hood is the guarantee and the button is only consent in software.
Saying which of the two is load-bearing matters more than having both.

**Read-only root.** Overlayfs plus tmpfs makes "the station stores nothing" a property of
the filesystem rather than of our care. It also removes the commonest cause of a dead Pi.
The consequence is that a failed send is lost, which is why the button's ring has to say so.
