# Hardware

A catalogue of what this system could be made of, and what it must never be made of.

This is a **thinking document**, not a shopping list and not a plan. Most of what is
below will never be built. It exists so that selection is a choice among understood
options rather than a reaction to whatever appeared in a search result.

Written in English because this repository is destined to be public and the rest of
`docs/` is English. The reasoning is what matters; prices and availability go stale.

## How to read the status marks

| Mark | Means |
| --- | --- |
| ✅ **verified** | Fetched from a primary source during research. Price and dates as of 3 Aug 2026 and will drift. |
| 🔎 **candidate** | Real product, plausibly right, availability and price not verified. |
| 💡 **idea** | A direction, not a product. May need a different device entirely. |
| ⛔ **rejected** | Ruled out by the project's rules, not by cost or difficulty. Recorded so the reason survives. |

---

## 1. The filter

Before any device is interesting, it has to survive these. They come from
`.github/copilot-instructions.md` and they are not preferences.

**It must not watch a person.** Not with radar, not with a microphone, not with a wearable.
The camera in this system is handheld, and faces will be in frame — so the rule cannot be
about where the lens points. It is about two other things: a capture happens only because
the person holding the device pressed the button, and nothing infers anything about a person
from what comes back. Anything that senses *a person* without either of those — including
the entire category of devices marketed as "privacy-friendly presence detection" — is out.

**It must not judge a person.** No device whose output is a score, a level, a streak, a
percentage, a trend, or a comparison. No device whose appeal depends on somebody wanting to
keep it happy.

**It must not pull.** Nothing that notifies on inactivity. Nothing that gets brighter,
louder or more insistent the longer it is ignored. Stopping is a legitimate outcome, so
every device must be ignorable without consequence.

**It must fail toward the parent.** When a device is uncertain, flat, offline or broken,
the correct behaviour is to surface that to the parent — never to guess, and never to
show an error to the adolescent.

**It must not be able to render unscreened content.** Devices that receive a finished
bitmap are structurally safer than devices that hold fonts and compose text, because the
former physically cannot draw something the safety gate never saw. Prefer dumb renderers.

**It must be appropriate in a home.** A bare PCB with a ribbon cable taped to a wall is
not a thing you put in a family's kitchen. Enclosure is a requirement, not a finishing
touch.

**It must survive the parent losing interest for a week.** Anything needing weekly
maintenance will be maintained twice and then abandoned, and the system will go dark —
which is itself a violation.

---

## 2. Verified findings

Everything in this section was fetched from a primary source during research on
3 Aug 2026. Prices in EUR including VAT where the retailer showed them.

### 2.1 TRMNL (OG) — ✅ verified — the current front-runner

| | |
| --- | --- |
| What | 7.5" e-paper, 4 greyscale, ESP32, LiPo battery, injection-moulded enclosure |
| Price | €122,95 + €22,95 Clarity Kit (battery upgrade + developer edition + cable) |
| Availability | In stock, ships 1–2 business days, **free shipping to Europe** |
| Reviews | 4.6 ★ over 1087 |
| Enclosure | PC/ABS soft-touch, 7 colours, wall or desk mount |

**The protocol, from the official docs:**

> 1. Device wakes up and requests content from web server every *n* period
> 2. Web server generates a **1- or 2-bit PNG image**. Response JSON includes a link to
>    this image and timing instructions for the next refresh.
> 3. Device renders the content, then goes to sleep.

**BYOS is officially supported.** The documentation index lists a dedicated page:
*"BYOS (Build Your Own Server): Buy a TRMNL device, then point it at your own server."*
Also BYOD (own device, their server) and BYOD/S (own both). No firmware recompilation
needed to self-host. There is an ImageMagick guide for producing conformant images.

**Why this fits the architecture:**

- Rendering happens on the Pi with Pillow, which is exactly where `shared.delivery` lives.
  The device cannot draw anything except a PNG we produced after the seals were checked.
  The chokepoint stops being a convention and becomes topology.
- The accented-character problem disappears. Pillow with a TTF handles UTF-8 natively —
  no `fontconvert`, no U8g2, no Latin-1 byte juggling. This was a likely source of a late
  surprise.
- The **server** dictates the next poll interval in its response. So latency is a
  parameter we control per-response: fifteen minutes normally, sixty seconds when
  something is pending. The deep-sleep latency limit becomes tunable rather than fixed.
- Communication is one-way by design: *"Your TRMNL device pings our server, never the
  other way around."* No inbound path to the device, nothing on the home network to
  attack. Same shape as the camera rule: nothing outside the room can make a device act.
- Firmware is open source (`github.com/usetrmnl/firmware`) and modding it is explicitly
  permitted by their terms. So the escape hatch exists even though we shouldn't need it.

**Cautions:** by default it talks to their cloud, which is unacceptable here — BYOS is
mandatory, not optional. OTA updates should be disabled before flashing or configuring
anything custom, or a stock update could overwrite the configuration. Display-only: no
buttons on it, which is correct — buttons stay physical and separate.

### 2.2 ELECROW CrowPanel 5.79" — ✅ verified

| | |
| --- | --- |
| Price | €53,14 (deal, list €58,99) |
| Availability | Ships from Amazon, arrives in days |
| Panel | 792×272, mono, dual SSD1683, partial refresh |
| Physical | **13,9 × 4,8 cm** — a strip, 2.9:1 |
| Included | ESP32-S3 (8 MB flash + 8 MB PSRAM), acrylic backing, rotary + 4 buttons, BAT connector 2.2–3.7 V |
| Reviews | 4.0 over 31 — but 13% one-star |

The strip shape is a genuine design constraint and arguably a *feature*: it is the shape
of a single instruction, and it structurally prevents putting a list on it. But a
pictogram and a sentence have to fight for the same 9 cm.

**Cautions:** reviews report fragility ("BE AWARE THAT THE SIDE SWITCH AND SCREEN ARE
FRAGILE" — a unit broke falling off a stand). The dual-SSD1683 wiring means the vendor
library, not stock GxEPD2; ESPHome needed a custom driver. The BAT input is LiPo range,
so the AA plan does not apply to this board.

### 2.3 Waveshare 7.5" + ESP32 driver board — ✅ verified

ASIN `B07MB7SVHQ`. Bundle contains panel, ESP32 driver board, adapter, 24-pin FFC.

| | |
| --- | --- |
| Price | €72,50 + €3,50 shipping |
| Delivery | **12–19 August** — slow, reseller Coolwell, not FBA |
| Active area | **163,6 × 98 mm** — 2.5× the CrowPanel's area |
| Refresh | 5 s full (Waveshare figure), **1.6 s differential** via GxEPD2 |
| Power | 38 mW refreshing, **<0.017 mW standby** |

Library support is the best of the three. GxEPD2 (1.5k stars, v1.6.9, 67 releases,
8 years) supports both `GDEW075T7` and `GDEY075T7`, and ships a dedicated example named
`GxEPD2_WS_ESP32_Driver` for exactly this board. It also ships
`GxEPD2_U8G2_Fonts_Example` specifically for accented characters ("ÄÖÜäéöü").

**Gotchas found in the wild:** the panel ribbon is fragile and one reviewer tore it off
the panel during assembly (unrepairable). If the image comes out washed out, flip the
board's config switch — one French reviewer solved exactly this with "switch de gauche
sur A", contradicting Waveshare's own table. `init(115200, true, 2, false)` is needed for
boards with the "clever" reset circuit. A German reviewer got **4–5 weeks on an 18650**
with half-hourly updates, and reports an **IKEA frame fits the panel exactly** (~5 mm
covered top and bottom) — which is the cheapest solution to the enclosure problem found
so far.

### 2.4 Waveshare ESP32-S3 Smart 86 Box — ✅ verified — parked

4" 480×480 capacitive touch, €47,99, sold by Waveshare, ships from Amazon, arrives in days.
3.7 ★ over 23 with 27% negative and a "frequently returned" badge; documentation is the
known weakness ("Beware — abandonware!"), though two independent reviewers report it works
well with ESPHome.

Designed to mount **flush in a wall switch box**. Interesting as a *parent* panel — a
thing you tap while passing to approve something, which makes supervision physical instead
of a task to remember. Not a surface for the adolescent: a backlit rectangle on a wall
invites poking, which is the engagement drift the project exists to avoid.

⚠️ The "86 box" is the Chinese 86 × 86 mm standard. **Italian wall boxes are 503
(rectangular) or 502 (round).** Verify before assuming it mounts.

### 2.5 Ruled out during research

- **LilyGO T5-4.7-S3** (`B0DRBHDY21`) — ✅ verified, €46 + €12 shipping, but **delivery
  4–16 September**, sold and shipped by LILYGO from China. Arrives inside the hack week.
  One review, one star, "the GitHub examples don't work".
- **Colour e-paper (Spectra 6, ACeP 7-colour)** — refresh 15–30 s with prolonged
  flashing. Beautiful for a static picture, wrong for a prompt someone is waiting on.
- **Displays ≤ 2.9"** — unreadable at any useful distance.

### 2.6 The printer question — resolved

Laser was recommended and then **rejected on the user's objection, correctly**. Laser
printers emit ultrafine particles and ozone during toner fusing; in a home, running often,
in an occupied room, that trade is not worth a marginal gain in marker sharpness.

The marker argument that used to sit here is retired with the marker pipeline: a page is
read against the blank it was printed from, and nothing on it is there for a machine. What
survives is about ink and paper, not about detection:

What actually matters, all free:
- Print **black only**. Modern inkjet black is usually pigment, water- and smudge-resistant
  once dry; colour inks are dye and smudge under a resting hand.
- **Normal quality, not high** — less ink means less paper cockling, and the homography
  assumes a plane.
- **80–90 g/m² matte** paper. Never glossy.
- Page geometry is a printing concern only. There is no detection to keep robust, so a page
  is laid out for whoever is looking at it and for nothing else.

**Use the printer already in the house.** Zero purchases, zero fumes.

---

## 3. Ideas, organised by what they do to a day

Organised by the experience, not the technology, because organising by technology
produces catalogues and organising by experience produces ideas.

### 3.1 Things that appear

**Thermal receipt printer** — 💡 idea, and the simplest one in this document.
ESC/POS 58 or 80 mm, ~€25–40, no ink, no toner, no fumes, no cartridges ever. A prompt or
a tiny exercise prints *instantly* with a sound, and it gets torn off. Paper as an event
rather than a document. It sidesteps the whole inkjet/laser question for short content,
and a torn-off strip is a physical object that can be carried to where the task is,
stuck on a fridge, or thrown away — all without any of it being recorded. Thermal paper
fades over months, which is a *feature*: nothing accumulates.
Worth prototyping before the A4 loop, because it is dramatically simpler.

**Label printer** (Brother P-touch, Niimbot) — 💡 idea. Prints something adhesive.
"This drawer" / "these go here". Turns the system into something that improves the
*house* rather than instructing the person, which is a subtly different and gentler
posture.

**LED matrix panels** (Divoom Pixoo 64, Ulanzi TC001, WLED on HUB75) — 🔎 candidate,
~€60–90. 64×64 pixels of colour. Too low-resolution for text, which is exactly why it is
interesting: it forces pictograms. Warm, toy-like, not screen-like. Downside: it is
emissive and always lit, so it needs to be dimmable to nearly nothing at night and must
never pulse or animate to attract attention.

**Split-flap display** — 💡 idea. The mechanical clatter of an airport board. Vestaboard
is ~€3000 and out of scope, but DIY split-flap modules exist and single-word units are
buildable. The sound *is* the notification, and it happens once, and then it is quiet.
That matches "announce, then stop".

**Flip-dot panel** — 💡 idea, same family. Mechanical, audible, holds state with no power.
Salvaged bus-sign panels turn up secondhand.

**Nixie or VFD tubes** — 💡 idea. Warm, analogue, beautiful, and genuinely non-digital in
feel. Realistically only useful for numbers — a countdown, a time, a quantity.

**Smart bulb / ambient light** (Hue, WLED strip) — 💡 idea. Colour as a calm ambient
signal: the hallway is warm amber in the morning routine window, neutral otherwise.
⚠️ Dangerous near the rules: light that *changes because something has not been done* is a
nag with better manners. Only acceptable as a *time* signal, never as a *behaviour* signal.

**Projection** — 💡 idea. A tiny projector throwing a pictogram onto a wall or the floor
where the task is. Removes the object entirely — nothing to mount, nothing to break.
Practical problems: ambient light, focus, fan noise, and a lamp that runs hot.

**Large e-paper** (9.7"–13.3", IT8951 controller) — 🔎 candidate, €150–300. If the 7.5"
turns out to be too small for pictogram *and* text, this is the escape. Expensive and
slow, and GxEPD2 supports the IT8951 HAT family.

### 3.2 Things that can be touched

**Arcade buttons** — 🔎 candidate, ~€3 each. 60 mm, real click, unambiguous. This is how
anything gets answered in the house: confirm, ask for help, say done. Buy several: one will
break, and a second action will turn out to be needed.

**NFC tags and a reader** (PN532 / RC522, ~€10, tags ~€0.30) — 💡 **idea worth serious
attention.** A physical token placed on a pad *is* a command. No reading required, no
menu, no screen, no literacy. A wooden disc with a picture on it means "I want to do
this one". A card in a slot means "this is the one for today". It makes choosing tangible,
and tangible choosing is not the same experience as tapping glass — for someone with a
cognitive disability it may be a much better one. It also produces beautiful physical
objects that live on a shelf rather than in an app.

**Rotary encoder / dial** (M5Dial, ~€30) — 🔎 candidate. Analogue feel, continuous, no
wrong answer. Good for "how much" or "which of these", bad for anything precise.

**Wireless buttons** (Flic, Aqara, IKEA Rodret/Styrbar via Zigbee) — 🔎 candidate,
€10–30 each. Battery, stick-anywhere, no wiring. Would need a Zigbee coordinator dongle
(~€25) on the Pi. Attractive because it makes *placement* free — a button can live where
the action is instead of where the wires reach.

**Load cell / weight pad** — 💡 idea. Put an object down and something acknowledges it.
Wordless. ⚠️ Careful: this is one step from measuring compliance. Only acceptable if the
response is an acknowledgement, never a record.

**Reed switch and magnet** — 💡 idea. A box that knows it was opened; a door that knows it
was closed. Cheap, invisible, no power. ⚠️ Same caution — this is very close to
surveillance of a person by proxy. Probably rejected, kept here to be argued about.

**Conductive paint / Makey Makey style contacts** — 💡 idea. Turn a drawing, a piece of
fruit, or a strip of foil into a switch. Charming, and physically fragile.

### 3.3 Time made physical

**A Time Timer** (the red disappearing disc) — 🔎 candidate, ~€30–40. Not a gadget: it is
a standard tool in special education because it makes duration *visible* without numbers
or reading. Worth buying one as a reference object even if nothing electronic is built —
understanding why it works is worth more than most of this document.

**A servo-driven pointer on a physical dial** — 💡 idea. A real needle moving across a
printed arc. Duration as position, not as a countdown. No digits, no urgency, no alarm.

**A sand timer** — 💡 idea, and possibly the correct answer. Zero electronics, zero
failure modes, never dark, and the passage of time is legible from across a room. Listed
seriously: sometimes the right hardware is not hardware.

### 3.4 Sound

**Speaker + DAC, with Azure Speech for TTS** — 🔎 candidate. A calm voice reading the
prompt aloud removes the reading requirement entirely, which may matter more than any
display in this document. Fits the cloud-only inference rule — the synthesis happens in
Azure, the Pi plays a file.
⚠️ The voice itself must be a *setting the parent chose* — the system may change what it
says, not who appears to be saying it — and speech must never be the only channel, because
a spoken prompt cannot be ignored the way a display can.

**A solenoid striking a real bell or chime** — 💡 idea. One physical sound, once, that
does not repeat and cannot escalate. Nicer than any speaker for "something is ready".

**A music box mechanism** — 💡 idea. Wind-up, mechanical, warm.

### 3.5 Movement

**A servo raising a small flag or opening a small door** — 💡 idea. Something changed in
the room. Legible at a glance from any angle, unlike a screen.

**A stepper moving a marker along a physical strip of the day** — 💡 idea. A wall-mounted
timeline where a marker moves with the actual time. The day as a place rather than a list.

**Vibration** — ⛔ rejected. Requires a wearable. See below.

### 3.6 The parent's presence

**A wall-mounted panel** (see 2.4) — 🔎 candidate. Turns approval from "remember to open
the app" into "see it while making coffee". The point is not automation; the point is
lowering the cost of staying involved.

**A physical approve button for the parent** — 💡 idea. A single button that approves
whatever is waiting. Simple to build, and it turns the parent's role into a gesture rather
than a chore.

**A shared token** — 💡 idea. An object the parent physically places to mean "this one,
today". Steering becomes something you do with your hands, in the room, in front of the
person it is for, rather than something configured in an interface they never see.

### 3.7 Infrastructure

- **CM5 + carrier + NVMe** — ✅ **owned, settled, no longer a blocker.**
  Raspberry Pi CM5, 8 GB RAM, 16 GB eMMC, **no onboard radio**; Waveshare CM5 IO Board
  (PoE variant) with case and PSU; Patriot P300 256 GB NVMe. Overspecified for the job,
  which is the right direction to be wrong in. Three notes that follow from it:
  - **Boot from eMMC, put writes on NVMe.** The OS on soldered eMMC cannot be knocked
    loose and needs no NVMe-boot bootloader configuration. `/var/log`, the ARASAAC cache,
    the approved-content reserve and the rectified crops go on the NVMe, which keeps the
    write-heavy paths off the eMMC and away from its wear limit.
  - **Fit the passive heatsink, leave the fan disconnected.** See §3.7.1 — this is a
    design decision, not an assembly detail.
  - **A USB Bluetooth dongle is required**, not optional — see §3.7.2.
  - ✅ **IO-VREF jumper confirmed on `3V3`** (verified on the board, 2026-08-04). GPIO
    logic is 3.3 V, so the §3.8 switch jack wires directly with a pull-up and no level
    shifting. The board also offers `1V8` — if that jumper ever moves, the jack breaks.
- ⚠️ **Superseded.** The three entries that follow — **Camera Module 3 Wide (102°)**, the
  **22-pin to 15-pin adapter cable**, and **a gooseneck or desk arm** — were the fixed
  capture station: a camera held at a known height over an A4, so that four printed markers
  were always in frame. The scanner does that job now, and the camera that replaced this is
  handheld, battery-powered and carried around. Kept because the sizing arithmetic is
  correct and somebody may want a fixed station for a different reason.
- **Camera Module 3, Wide (102°)** — autofocus matters at 30–40 cm; the v2
  is fixed-focus. Wide covers an A4 at ~25–30 cm, standard needs ~50 cm.
- **⚠️ 22-pin to 15-pin camera adapter cable** — CM5 carriers use 22-pin; the Camera
  Module 3 ships with 15-pin. **They do not connect.** The €2 part that costs an evening.
- **A gooseneck or desk arm** to hold the camera at a fixed height over a defined area.
  Without it nothing can be tested repeatably.
- **Diffuse light** under the arm. Pencil on white paper in evening shade otherwise
  produces low confidence readings, which correctly escalate to the parent — but you do
  not want that on every scan.
- **A UPS or battery hat** — 💡 idea, in service of "never dark". A power cut should not
  take the system down mid-routine.
- **Zigbee coordinator dongle** (~€25) if any wireless buttons are used.

#### 3.7.1 The box must be silent, and it can be

Reviewers of this exact carrier bundle report a bad thermal design: no air inlet, an
exhaust roughly 40% blocked by decorative fins, a cheap fan, and not enough clearance to
fit a heatsink *and* the fan together. One owner describes the noise as *"an unpleasant
noise, similar to a tinnitus"*. Another measured **38–48 °C at low CPU utilisation using
the passive heatsink alone**, and concluded that on a CM5 passive-only and fan-only cool
about equally well.

This matters more than it looks. A device that whines in a hallway is a device someone
unplugs, and an unplugged device is a dead system. No amount of correct software prevents
that.

The fix is free, and it falls out of a rule the project already has. Because **nothing
infers on the device** — every model call goes to Foundry — the thermal envelope here is
trivial: rendering PNGs with Pillow, driving a printer and a scanner, some HTTP. So the box
runs **passive, fanless, silent**, and the constraint that looked like a limitation buys
back the thing that keeps the system alive in a home.

Record it as a requirement, not a preference: **the central node must be inaudible at one
metre.** Any future change that needs a fan is a change that needs re-justifying.

#### 3.7.2 The module has no radio — a dongle closes the gap, silicon does not

The CM5 variant owned is the no-wireless industrial one. For the surfaces this is
harmless: TRMNL and any ESP32 join the house WiFi and reach the node through the router,
so a wired node is fine. The problem is **Bluetooth**, and it is not a small one — §3.8
found that a real part of the assistive-switch world is wireless (Blue2 FT, Jelly Beamer,
Flic). Losing BLE would quietly delete an entire input category.

It is recoverable: the carrier has USB, so a **USB Bluetooth dongle (~€10)** restores it.
Prefer an **RTL8761B**-based dongle — well supported by current kernels — over the cheap
CSR8510 clones, which are widely counterfeited and flaky on Linux. Buy it early enough
that BLE input can actually be tried, not late enough that it becomes a "next version"
feature.

### 3.8 The assistive-technology ecosystem — ✅ verified

There is an entire industry that has spent forty years designing physical controls for
people with disabilities, and I had been about to specify a €3 arcade button without
looking at it. Prices below from AbleNet, the sector's reference manufacturer.

| Switch | Surface | Force | Price |
| --- | --- | --- | --- |
| Jelly Bean — *"long considered the standard in the industry"* | 6.4 cm | — | $75 |
| Big Red — *"tactile and auditory feedback"* | **12.7 cm** | 156 g | $75 |
| Big Buddy Button | 11.5 cm | 150 g | $75 |
| Buddy Button IC — interchangeable coloured caps | 6.4 cm | slightest touch | $75 |
| Micro Light Switch | small | **11.3 g** | $95 |
| Specs IC — mountable or wearable | 3.5 cm | — | $75 |
| Pillow Switch — foam, head or cheek activation | — | — | $140 |
| Mini Cup Switch — **IP67, submersible** | 2.5 cm | — | $85 |
| Jelly Beamer — wireless, 9 m, non-interfering | 6.4 cm | — | $145 + $120 receiver |
| Blue2 FT / BIG Candy Corn 2 — **proximity**, no contact needed | — | 0 g | $255–260 |

**Four things a maker catalogue does not record:**

**Actuation force is a published specification.** 156 g, 150 g, 11.3 g. No arcade button
lists this, because for a general audience it does not matter. Here it is *the*
accessibility parameter, and a button that is too stiff is a button that silently excludes
someone. I do not know what force is right here — the parent does.

**Tactile *and auditory* feedback is named as a feature**, not a side effect. The click is
a confirmation channel, and it is the reason a physical button beats a glass rectangle for
someone who may not be certain whether a tap registered. This was an instinct earlier in
the conversation; here it is a design principle with a vocabulary.

**Interchangeable coloured caps.** Colour is not decoration, it is identity — how you tell
two switches apart without reading. Any button in this system should be recolourable
without tools.

**🔑 And the one that changes the architecture: these switches all terminate in a mono
3.5 mm jack.** It is the de-facto standard of the entire field.

> **If the system exposes a 3.5 mm switch jack instead of a soldered button, it accepts any
> switch built to that connector** — feather-touch, proximity, foam, submersible,
> head-operated, wireless. The physical interface stops being a thing we chose for somebody
> and becomes a thing they can be met at, whatever their motor ability is today or in five
> years.

That is a one-euro socket and a pull-up resistor. It costs nothing, it is trivially
testable, and it widens the set of people the device works for. It also lets the parent buy
a switch from any therapy supplier without us being involved — which is the "parent steers"
posture, expressed in hardware.

Recommendation: **put a 3.5 mm jack on everything that takes a press.** Keep a cheap arcade
button for development, and let real switches be plugged in later. Cheap Chinese
equivalents of these switches exist at €10–20 for prototyping; buy the real one once the
shape of the interaction is known.

### 3.9 Pictograms — ✅ verified — ARASAAC

`https://api.arasaac.org` — a full public REST API from the **Gobierno de Aragón**, the
regional government of Aragón, Spain. Free, institutional, and the de-facto standard AAC
symbol set across European special education and speech therapy.

Endpoints that matter:

| Endpoint | Does |
| --- | --- |
| `GET /pictograms/{language}/search/{text}` | find pictograms for a word |
| `GET /pictograms/{language}/bestsearch/{text}` | single best match |
| `GET /pictograms/{language}/all` | the entire set, for local caching |
| `GET /keywords/{language}` | the controlled vocabulary |
| **`GET /phrases/flex/{language}/{phrase}`** | **turns a sentence into a pictogram sequence** |
| `GET /pictograms/{lang}/wordnet/{wordnet}/id/{synset}` | WordNet synset mapping |

Italian is supported.

**Why this matters.**

The system does not have to invent a visual language. It can use one that may already have
been taught. ARASAAC pictograms are what Italian speech therapists, special-education
teachers and AAC apps use. If somebody has ever used a communication book, a visual schedule
at school, or a PECS-style board, these are very likely the exact images they already read.
A prompt drawn in ARASAAC is not a new thing to learn — it is a continuation of something
already known, made by people who are not us.

That changes the display question. We are not designing icons. We are rendering a public,
standard symbol set that predates this project and will outlive it.

**Three architectural consequences:**

1. **The whole set can be cached locally.** `/pictograms/{language}/all` plus the image
   files is a finite download. That means pictograms are available with no network, which
   feeds `CACHED_FALLBACK` directly — the offline reserve becomes larger than a handful of
   pre-approved sheets, which is what "never dark" depends on.
2. **`phrases/flex` is doing exactly the job the content agent needs** — sentence in,
   pictogram sequence out — with no model call, no cloud round trip, and no risk of an LLM
   inventing an image. Deterministic, inspectable, and it can be reviewed by the parent
   before anything is shown.
3. **It works for the printed sheet too**, not just the display. Same symbols on paper and
   on the e-paper means one visual language across the whole system.

⚠️ **Licence:** ARASAAC is **CC BY-NC-SA**. Attribution is required, and **non-commercial**.
For an open-source personal project this is fine and the attribution belongs in the README.
It would be a real constraint on anything commercial, and that should be recorded now
rather than discovered later. Author credit: Sergio Palao / ARASAAC / Gobierno de Aragón.

---

## 4. Rejected, and why

The reasons matter more than the list. These are rejected by the project's rules, not by
cost or difficulty, and a future contributor should have to argue with the reason rather
than rediscover it.

| Category | Why it is out |
| --- | --- |
| ⛔ Any camera that captures without a press | The camera here wakes on its own button and nothing else. No remote trigger, no timer, no motion. Presence, person or face detection is forbidden even as an intermediate step, and that matters more now that faces are in frame. |
| ⛔ mmWave / radar / PIR presence sensors | Marketed as privacy-friendly because they don't record images. They still infer where a person is and what they are doing. That is a sensor pointed at a person. |
| ⛔ Wearables — watches, bands, trackers, rings | Biometrics, explicitly forbidden. Also the one device category nobody can walk away from. |
| ⛔ Always-on microphones | Voice-stress and affect inference are forbidden, and an always-listening device in a child's home is not defensible regardless of what it does with the audio. |
| ⛔ Eye tracking, gaze, attention estimation | Explicitly forbidden. The system may learn from work that comes back; it may not point an instrument at a person to read them. |
| ⛔ Emotion / affect recognition cameras | Explicitly forbidden. The inference it claims to make is also not well supported by evidence. |
| ⛔ Sleep trackers, smart scales, health devices | Health surveillance of a minor by a system that has no clinical role. |
| ⛔ Any display of a streak, a score, a level, a percentage, a trend | Rule 1. The device would be fine; what we would put on it would not. |
| ⛔ Anything that escalates when ignored | Ignorability is a requirement. A device that gets louder is a device that punishes stopping. |
| ⛔ Voice assistants (Alexa, Google) as a component | Cloud services outside our control, always listening, and their business model is engagement. |

**A note on the tempting ones.** Presence sensing and reed switches keep looking useful
because they would let the system be *responsive* — the display could change when somebody
enters the room. That is exactly why they are dangerous. Responsiveness to a person is
observation of a person, and the pleasant version of it is still the thing the rules
forbid. If the system needs to know something changed, the answer is a button somebody
pressed on purpose.

---

## 5. Open questions blocking orders

1. ~~**CM5: Lite or eMMC, how much RAM, which exact carrier?**~~ ✅ **Resolved** — owned:
   8 GB / 16 GB eMMC / no radio, on the Waveshare PoE IO Board, with a 256 GB NVMe. See
   §3.7. The open sub-question is now only the **USB Bluetooth dongle**, which is a €10
   part, not a decision.
2. ~~**Has the CM5 already been ordered?**~~ ✅ **Resolved** — already in the house. The
   item expected to take longest was already done.
3. **Which printer is already in the house?** Determines whether anything needs buying
   at all, and whether the thermal-printer idea should be prototyped first.
4. **Reading distance for the routine prompt.** Decides 5.79" vs 7.5" vs larger. Cannot be
   answered from a desk.
5. **Is the interactive LCD needed at all?** Possibly answered by building the paper loop
   first and seeing what is missing.
6. **Does the reader read?** Not recorded anywhere in this repo and must not be. But it
   decides whether text, pictograms or speech is the primary channel — and it is the
   parent's answer to give, verbally, once.
7. **Has a pictogram system already been taught?** ARASAAC, PECS, Widgit, something
   from school or therapy? If yes, the system should use that one and no other. It costs
   one conversation to answer and it decides what everything else renders.
8. **What kind of press works?** A stiff arcade button, a light-touch switch, a
   proximity switch, something mounted rather than held? Do not guess — but design so the
   answer can change, which is what the 3.5 mm jack buys.

---

## 6. What I would do

If the answers were mine to give:

**Order tonight.** TRMNL OG + Clarity Kit (~€146, arrives in days, BYOS confirmed) as the
ambient surface. It eliminates firmware, fonts, battery engineering and the enclosure
problem in one purchase, and it puts rendering on the Pi where the seals already live.

**Nothing to order — assemble what is already here.** The CM5 stack is owned. Build it
with the **heatsink and no fan**, install to eMMC, mount the NVMe for logs and cache, and
confirm it is inaudible before anything else gets attached to it. Add a **USB Bluetooth
dongle (~€10)** so the wireless-switch category stays open.

**Order tonight, cheap.** Two arcade buttons and a diffuse light. The camera line of this
list — Camera Module 3 Wide, the 22-to-15-pin adapter, a desk arm — was for the fixed
capture station and is superseded: the household scanner reads paper, and the camera that
replaced it is handheld and not yet designed.

**Buy one thermal printer** (~€30) and try it before committing to the A4 pipeline. If a
torn-off strip turns out to be a better object than a printed sheet, that changes the
design in a good direction and it is cheap to find out.

**Buy one Time Timer** (~€35), not to integrate but to study.

**Buy an NFC reader and a handful of tags** (~€15) and try making three wooden discs that
mean three things. If tangible choosing works, it may matter more than any screen in this
document.

**Put a 3.5 mm jack on every input**, from the first prototype. It costs one euro and it
makes the system accept switches from the whole assistive-switch industry. It is the
cheapest decision here with the widest effect, and it has nothing to do with what we buy.

**Cache the ARASAAC set locally before writing any rendering code.** It is free, it is
finite, it makes the offline reserve real, and it means the system speaks a visual language
that may already have been taught rather than one we invented.

**Do not buy** the 86 Box, the LED matrix, the large e-paper, or the second display until
the first loop runs end to end.

---

## 7. The thought I keep returning to

Every hour of this research pushed in the same direction: the interesting part of this
system is not the screen.

The screen was where we spent the day because it is the part that looks like a product.
But a display shows a prompt, and a prompt is the least of it. What the research turned up
— the assistive switch that meets somebody wherever their hands are, the pictogram set they
may already read, the token they can put down instead of a menu they have to navigate, the
strip of paper they can tear off and carry to the room where the thing happens — those are
the parts that belong to a person rather than to a wall.

And almost all of them are cheap. The €146 device is the least interesting purchase on
this list.
