# What gets printed

The printer is an Epson ET-2870 reached over IPP Everywhere, with no driver. The
print → scan → detect chain has already been proven end to end: the ruler on the sheet
measures exactly 50 mm, and the markers land between 176 and 178 px against 177.2 expected.
So the geometry is no longer a risk: the ideas below are about the content.

---

## 1. Closed: multiple-choice sheets for the offline path

**What it was.** A family of sheets made only of boxes to tick. The sheet contract declares
five cell kinds, but only two can be read without the network: `CHECKBOX` and `CHOICE_BOX`.
If the link drops, choice sheets keep closing the loop and the others do not.

**How it was closed, 19 August 2026.** `printing/layout.py` turns an exercise body into a
`SheetSpec`: one `CHOICE_BOX` per choice, grouped per question so a mark can be attributed
to the question it answers, positioned in the marker frame. It refuses rather than
squeezing — more than four questions, or a question with fewer than two choices, raises
`SheetTooFull` instead of reaching for a smaller font.

Two things had to be added underneath. A sheet needs printed words, and a cell is a place
an answer can be, which a question is not: `SheetSpec` gained `headings`, text drawn on the
page that the reader never looks at. And the sheet had to reach paper: `drawing_to_pdf`
writes the PDF by hand in millimetres, because the printer does not accept PDF and CUPS
rasterises it at 360 dpi — about 35 pixels to an ArUco module — while every converter in
the path is another chance for "fit to page".

**What it cost.** The first layout ran the title straight through both upper markers. The
renderer refused it, which is why the refusal exists; the second put the choice word on top
of the question, which no test could catch and only looking at the sheet did.

**How it was checked.** A three-question sheet was laid out, drawn, printed at 100% on the
ET-2870, and the boxes are where the spec says. The tests hold the part the renderer cannot
see: no two boxes overlap, since a mark inside an overlap answers two questions at once.

**What is still open.** Reading it back. `tools/check_scan.py` has done it once from a
scanned file; nothing yet does it on its own.

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
is already known: if a different one is used at school, ours would be a second language to
learn rather than a continuation.

---

## 3. The sheet that asks, instead of assigning

**What it is.** A sheet with three or four boxes: "what would you like to do?". A box is
ticked, the camera reads it, and the chosen thing arrives.

**Why.** Everything else in the system proposes, and the adolescent accepts or walks away.
This is the one point where the initiative passes to them, using the mechanism that already
works — a ticked box, the only thing readable offline. Nothing new is needed: what is needed
is reversing the direction of a sheet we already know how to print and read.

**How.** The same `SheetSpec` as the multiple-choice sheets, with a different meaning for
the cells: not answers but requests.

**What it costs.** It has to be decided what happens if nothing is ticked, or everything
is. The right answer is: nothing special, and no insisting.

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

**What it is.** Two boxes at the foot of a sheet, to tick once it is finished.

**Why.** Everything the system offers is chosen by somebody else. These two boxes are the
cheapest way for the person doing the work to say what comes next. The system may also work
this out on its own from what came back — that is allowed now — but a stated request does
not have to be right about anybody: it is not a guess that can be wrong, it is an answer.

**How.** Two more cells in the same `SheetSpec` as the multiple-choice sheets. The reader
already knows how to tell a ticked box from an empty one, offline. What the tick does is
pick the next sheet from content the parent has already approved; it changes no setting.

**What it costs.** It has to be decided what happens when both boxes are ticked, or
neither: nothing special, and no asking again. And what is kept has to stay a record of a
request made on a day, not a standing property of the person — "asked for another like this"
rather than "prefers this".

**Where it starts.** `shared/sheet.py` for the cells, the layout agent that does not exist
yet (see item 1), `vision/` for the reading side.

**Done when.** A printed sheet with a ticked box is read back, and the next sheet offered
is of the kind that was asked for, chosen from already-approved content.
