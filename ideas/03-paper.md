# What gets printed

The printer is an Epson ET-2870 reached over IPP Everywhere, with no driver. The
print → scan → detect chain has already been proven end to end: the ruler on the sheet
measures exactly 50 mm, and the markers land between 176 and 178 px against 177.2 expected.
So the geometry is no longer a risk: the ideas below are about the content.

---

## 1. Multiple-choice sheets, and only those, for the offline path

**What it is.** A family of sheets made only of boxes to tick.

**Why.** The sheet contract declares five cell kinds, but **only two can be read without
the network**: `CHECKBOX` and `CHOICE_BOX`. A handwriting sheet needs the cloud to be read
back. If the link drops, choice sheets keep closing the loop and the others do not. This is
not a pedagogical preference: it is the only format that works when everything else is off.

**How.** The content agent already produces multiple-choice exercises and the prompt asks
for choices without symbols. What is missing is the layout agent, which turns an exercise
into a `SheetSpec` with the cells in the right places.

**What it costs.** Layout is the part we have never written, and the most tedious:
normalised positions, no overlap with the QR code or the markers, and a test that checks
every declared cell really is where the reader will look for it.

---

## 2. Routine cards

**What it is.** One large pictogram and one word, to cut out and stick where it is needed.

**Why.** The display shows one step at a time; a card goes where the step happens — on the
wardrobe, in the bathroom, on the school bag. This is the case where paper beats a screen,
because it is in the right place rather than in one place.

**How.** ARASAAC has a public API with Italian, and an endpoint that turns a sentence into a
sequence of pictograms without calling any model. The whole set can be downloaded and kept
locally, so it works offline too.

**What it costs.** The licence is CC BY-NC-SA: attribution required, non-commercial use
only. For a personal project that is fine, and it belongs in the README now rather than
being discovered later. It is also worth checking with the parent **which** pictogram system
she already knows: if she uses a different one at school, ours would be a second language to
learn rather than a continuation.

---

## 3. The sheet that asks, instead of assigning

**What it is.** A sheet with three or four boxes: "what would you like to do?". She ticks,
the camera reads, and the chosen thing arrives.

**Why.** Everything else in the system proposes and she accepts or walks away. This is the
one point where the initiative passes to her, using the mechanism that already works — a
ticked box, the only thing readable offline. Nothing new is needed: what is needed is
reversing the direction of a sheet we already know how to print and read.

**How.** The same `SheetSpec` as the multiple-choice sheets, with a different meaning for
the cells: not answers but requests.

**What it costs.** It has to be decided what happens if she ticks nothing, or ticks
everything. The right answer is: nothing special, and no insisting.

---

## 4. Printing in batches, while the printer is on

**What it is.** Approved sheets pile up; they are all printed together when somebody turns
the printer on.

**Why.** The printer is off almost always — it is off right now. A system that assumes a
printer is on fails every day. A 250-sheet tray turns paper from a per-use chore into a
monthly one, and takes the parent out of the critical path without taking them out of the
decision.

**How.** A local queue on the hub and an IPP check: when the printer answers, whatever is
waiting gets printed. No new service; `lp` does the rest.

**What it costs.** Automatic duplex is a trap: a sheet printed on both sides would be read
from one side only. Simplex has to be forced in the print path, and written into the code
rather than remembered.

---

## 5. "Another like this" and "something different"

**What it is.** Two boxes at the foot of a sheet she can tick when she has finished it.

**Why.** Everything the system offers is chosen by somebody else. These two boxes let her
say what comes next without anybody having to interpret anything: it is a request she
makes, once, in words, not a preference inferred from how fast she worked or from what she
left blank. That distinction is the whole point — the inferred version is the thing this
project refuses to build.

**How.** Two more cells in the same `SheetSpec` as the multiple-choice sheets. The reader
already knows how to tell a ticked box from an empty one, offline. What the tick does is
pick the next sheet from content the parent has already approved; it changes no setting.

**What it costs.** It has to be decided what happens when both boxes are ticked, or
neither: nothing special, and no asking again. And it must not accumulate — a tick applies
to the next sheet and is then forgotten, otherwise it becomes a profile of her built one
box at a time.

**Where it starts.** `shared/sheet.py` for the cells, the layout agent that does not exist
yet (see item 1), `vision/` for the reading side.

**Done when.** A printed sheet with a ticked box is read back, and the next sheet offered
is of the kind she asked for, chosen from already-approved content.
