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

---

## 6. A sheet a model designs, instead of a template it fills — half built, 20 August 2026

**What it is.** The sheet the house prints is the kind of short piece of practice an
adolescent is given now and then. Until now its shape was decided by arithmetic: four
questions, four boxes each, always in the same places. Now a model designs the page — where
things go, what is drawn on it, where there is room to write.

**Why.** Two reasons, and the second is the one that matters. A page laid out by arithmetic
is a form, and nothing about it is ever a pleasure to receive. And the format it was laid
out in could only express one kind of exercise, so every idea that was not four
multiple-choice questions had nowhere to go.

**How it stays frugal, which is the whole engineering problem.** A model that can draw will
spend ink, and ink on a home inkjet is slow, wet and expensive. So the vocabulary it draws
in — `shared/pagedesign.py` — **has no mark that fills an area**. Not a discouraged fill: no
fill. A drawing is strokes, so a heavy page is unreachable rather than merely asked against,
and the only remaining way to spend ink is a great many strokes, which is measured and
refused above a budget.

Six marks, and an administrator can read a design to the end: `stroke`, `circle`, `words`,
`tick_box`, `write_line`, `draw_area`. Coordinates are normalised over the marker
quadrilateral exactly as `shared/sheet.py` is, so a design carries no paper size, and
`PageDesign.to_sheet_spec()` produces the same `SheetSpec` the vision pipeline already
reads. That seam is what made this cheap: the page got more interesting and the reading
contract did not move.

**The numbers, measured on 20 August 2026.** Everything below is measured, not estimated.
The baseline is the sheet this replaces, rasterised at 150 dpi on A4:

| | ink | of the page |
| --- | --- | --- |
| the scaffold every sheet pays — four markers, QR, ruler | 940 mm² | 1.51% |
| the sheet this replaces: scaffold + 16 tick boxes | 1734 mm² | 2.78% |

Three sheets the deployed model designed, `gpt-5.6-sol-2026-07-09`, third run — the one
with every fix below in it:

| topic | marks | stroke ink | measured | seconds | out tokens |
| --- | --- | --- | --- | --- | --- |
| le tabelline del 6 e del 7 | 36 | 80 mm² | 2.290% | 52.3 | 3701 (2109 reasoning) |
| i nomi delle nuvole | 24 | 76 mm² | 2.611% | 60.5 | 4567 (3317 reasoning) |
| mettere in ordine i fatti di una giornata | 29 | 55 mm² | 1.933% | 38.4 | 2877 (1536 reasoning) |

All three are **lighter than the form they replace**, with a drawing on them. Input was
about 930 tokens each. The budget is 800 mm² of stroke ink and the heaviest sheet across
three runs spent 204, so the budget is not currently what shapes these pages — it is there
for the run that decides to hatch a sky.

Nine sheets were asked for in total, across three runs. One was refused, for a reason that
turned out to be ours rather than the model's — see below.

**Two ink figures, and they do not agree.** `stroke_ink_mm2` is length times width — the
area a pen would wet, and the figure the budget is applied to. `ink_coverage` rasterises
and counts dark pixels. Measured on a single line across the frame, the raster reads
**0.85 to 1.70 times** the arithmetic, because a stroke width is rounded to whole pixels:
0.3 mm at 150 dpi is 1.77 pixels drawn as 2. Neither is wrong and they are not
interchangeable, so the budget uses the first and the second is only reported.

**What it cost, and what it caught.** Four defects, three of them found by looking at a
rendered page rather than by a test:

- Labels were drawn above their cell, which is where the question is. On a page a model
  laid out there is nothing keeping the two apart, and `La mia:` landed on top of `Inventa
  una moltiplicazione`. Labels now go beside a tick box, under a writing line, above a
  drawing area.
- A drawing area's label ran off the right-hand edge of the paper, because a drawing area
  is most of the page's width and the label was placed beside it.
- `MAX_LABEL` was 24 characters and refused a whole sheet for `Scrivi qui il nome della
  nuvola`, which is 31. Now 48, and chosen rather than measured — what a label may safely
  be is a width in millimetres and nothing checks that yet.
- `tests/test_boundaries.py` refused the word `points` for a polyline's vertices, because
  it is gamification vocabulary. It was right to; the field is `vertices`.

**The limits, next to the claims.**

- **The old path is still the one that runs.** `printing/layout.py` is superseded and says
  so in its docstring, but the blueprint runner's `print_sheet` verb carries questions and
  choices rather than a design, so deleting it would take the working paper loop with it.
  The order is below.
- **No model has yet used a `tick_box`.** All the sheets across four runs chose writing
  lines. Tick boxes are the only cells readable without the cloud, so a page of handwriting
  reads as nothing at all when the cloud is unreachable — the degraded path silently gets
  worse as the pages get better. The prompt now says so; whether it changes anything is
  measured below.
- **Text is not in the ink figure.** `drawing_to_array` draws words only when a caller asks
  for a preview, so a page of long sentences costs more than it reports.

### On paper, 20 August 2026

`sh_48a85f58`, "Sei e sette in rotta", printed on the Epson ET-2870 through
`devices/print_sheet.py:compose_and_print` — the hub's own path, not a laptop. The ruler
measured **exactly 50 mm** against a real ruler, so the geometry the reader depends on
survived CUPS at 360 dpi. The page was then scanned back at 300 dpi to look at it.

Three things the raster had not shown, and only paper did:

- **Every accent and every times sign printed as `?`.** `6 × 2 =` came out `6 ? 2 =` and
  `attività` as `attivit?`. Not the font: `drawing_to_pdf` encoded the content stream as
  ASCII with `"replace"`, undoing the cp1252 filtering `_pdf_text` had already done, while
  the font is declared `/WinAnsiEncoding` — which is cp1252. One word changed. It had been
  wrong for as long as the PDF writer has existed and no test had ever looked.
- **A writing line's label printed as a caption under an empty rule.** `6 × 2 = ______` is
  one line and it printed as two unrelated things. The label now sits on the rule's own
  baseline and the rule starts after it, using Helvetica's real advance widths so the gap
  is known rather than guessed. This is the third placement this label has had in one day:
  above the cell collided with the question, under it read as a caption.
- **The page was still a form.** Two columns of identical ruled lines with a label in
  front of each. The model designed it freely — nothing computed that layout — so this is
  a fault in what it was asked for, not in what it can do. The prompt now says plainly
  that a grid of ruled lines is a form, asks the drawing to carry part of the work rather
  than decorate a corner, and points at tick boxes.

**Where it starts.** `shared/pagedesign.py` for the vocabulary, `printing/compose.py` for
millimetres and the budget, `agents/sheet_designer.py` for the prompt,
`panel/designing.py` for the cloud call, `tools/probe_sheet_design.py` to try it,
`tools/print_design.py` to send one to the printer from the hub.

**Done when — the order for retiring the old path.** Each step leaves the loop working:

1. The `print_sheet` verb in `shared/blueprint.py` carries a design instead of questions
   and choices, and the two catalogue experiences are rewritten in it.
2. ~~`devices/print_sheet.py` composes a design instead of calling `sheet_for`~~ — done,
   20 August 2026: `compose_and_print` sits beside `lay_out_and_print` and what it
   remembers is a `SheetSpec` either way.
3. `printing/layout.py` and `tests/test_layout.py` move to `attic/`, out of packaging and
   out of the test run, with a note saying what replaced them.
4. A designed sheet is printed, filled in by hand, and read back. **Half done**: printed
   and scanned, but nothing has been written on one and put on the glass.
