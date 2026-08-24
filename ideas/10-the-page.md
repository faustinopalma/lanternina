# 10. The page, defined before it is built

Started 24 August 2026, after a whole afternoon ran in the house and the parent looked at
what came out of the printer and said it was a form from a bureaucratic procedure. It is.

This document is written *before* the code, which is the correction that produced it. The
pages we have exist because early on, while the infrastructure was still being decided, the
work jumped to writing something that ran. What ran is a form, and it was going to be a form
from the first data structure onwards.

Nothing here is decided alone. The open questions at the end are the parts that need somebody
who has stood at the printer.

---

## 1. Why it is a form, and why prompting harder would not have helped

`shared/pagedesign.py` describes a page as a list of `marks`: a piece of text, a line to write
on, an area to draw in, a checkbox — each with a rectangle in normalised coordinates.

That vocabulary can only produce forms. A form *is* labelled fields at coordinates; that is
the definition. A model asked to design a page with those pieces can put the boxes in nicer
places, and it will still be a form, because the only thing it is allowed to say is "a field,
here". The bureaucratic feel is not a failure of the prompt or of the model. It is the data
model, faithfully rendered.

So the page is not fixed by better instructions. It is fixed by changing what a page is
allowed to be.

## 2. The layers

The parent's words: the AI defines the experience in layers — strategy first, then execution,
then content that is beautiful, functional and ecological.

One of these already exists and reaches nothing. `Experience.drawn` carries ten dimensions
along which an afternoon was conceived — its frame, its role, its mechanic, what the paper is
for, what the glass is for, its tone, its ending. **None of it reaches the page.** The page is
devised from the moment it belongs to and nothing else, which is why a page about a secret
mission and a page about a museum look identical.

The layers, and what each one is allowed to decide:

**Strategy** — what kind of thing this afternoon is, and therefore what kind of object the
paper is. A map. A dossier. A specimen label. A page from a catalogue. This is the layer that
decides the paper is *an artefact in a story* rather than a worksheet, and it is decided once
for the afternoon, not once per sheet.

**Execution** — the moments, which already exist and are not in question. What changes is that
a `hand_over` names the artefact the strategy chose rather than carrying a page design of its
own.

**The page** — the artefact itself: its composition, its illustration, its words, its ink. This
is the layer that does not exist yet in any useful form.

The value of separating them is not tidiness. It is that each layer can be checked before the
next one is paid for, and that a page can be refused without throwing away the afternoon.

## 3. What a page must carry, and it may be nothing at all

The page began this document carrying three things: four corner markers, a QR, and a declared
grid of cells. All three were removed by the parent in the space of an hour, each with an
argument, and what is left is worth stating carefully because it is close to nothing.

**The declared cells go.** A model can be given **the blank page and the filled page together**
and tell the difference. So a cell needs no rectangle, no kind, and no declared meaning for
what was written in it to be read. The reading becomes "what is on the second that is not on
the first", which is simpler and closer to what a person would say.

That removes cell kinds, normalised rectangles, `LOCALLY_READABLE`, the local ink arithmetic,
and the apparatus for saying where an answer is expected. It also removes a class of defect
this project has paid for twice: the arithmetic that read 45 % ink on an empty box, and the
inset that collapsed a word line to zero pixels and called it clean.

**The four corner markers go.** They exist to rectify perspective — to straighten a page
photographed at an angle. A flatbed with the lid closed has no perspective to correct: the
resolution is known, the page is flat, and the scan is rectified by construction. What is left
is rotation, from somebody laying the sheet the other way round, and scale; a QR carries three
finder patterns precisely so that both can be recovered. So the markers buy nothing on this
path and cost the four corners of the sheet, which is where a designed page most wants to
breathe.

> The rule they came with is about the camera, not the scanner: *keep only the rectified region
> inside the marker quadrilateral*. That is a privacy rule, and a flatbed with the lid down has
> no person in frame — `devices/scan_sheet.py` says so in its own docstring. If the camera path
> of `§9` is ever built, the markers come back with it and the rule with them.

**And then the QR goes too, because the page can be recognised by looking like itself.** The
parent's proposal: embed the scan, and the blank it was printed from is the nearest neighbour.
Identity without printing anything on the paper, which is exactly what a designed page wants.

An earlier draft of this section argued the QR could go because the house already knows which
sheet it is waiting for — one afternoon at a time, one `collect`, `run.printed` naming what was
handed out. That argument is weaker than it looked, and the parent said why: **the house knows
by expectation, not by reading the object.** When the expectation is wrong — an earlier sheet
put back on the glass — the afternoon carries on from false evidence, silently. An identifier
exists so as not to assume.

### Identity is a question inside the reading, not a gate before it

Then the parent moved the frame again, and this one is the correction that matters most: **the
model has to interpret what is on the paper anyway, so it should not first insist on the right
sheet being there.**

Everything above treats identity as a precondition — establish which sheet this is, refuse if
it is not the expected one, and only then read. That is a machine's anxiety and not a person's
need, and it is also against this project's own rules. Today an unrecognised page produces
*Questo foglio non è di Lanternina*: a refusal, aimed at a person, for a mistake that the
working rules say cannot exist. Somebody putting back an earlier sheet, or a drawing from
school, has not erred. The calm answer is to look at what is there and go on from it.

So the shape is: the scan goes to the model together with what the afternoon handed out and
what this moment is about, and the model answers **what happened on this paper**. Whether it is
the expected sheet is one of the things it can say, in the same breath, and the afternoon takes
a branch that blames nobody — the way `if_no_page` already exists for a sheet the printer never
produced.

That demotes the embedding from mechanism to convenience. It earns its place when there are
several blanks and handing the model the right one keeps the call small, or when a set of
designs needs checking for distinctiveness. It is not what makes the reading possible.
`embed-v-4-0` stays deployed: it costs nothing until it is called, and the margin it reports is
useful on its own.

**What is left undecided by this, and it is real:** a `collect` branches on what came back, and
a branch taken on a page that is not the one the branch is about is a wrong turn taken
confidently. The answer is probably that such a moment goes the way it would go with no page at
all, which is written already. Probably is not decided.

### Built and measured, 24 August 2026

`shared/vision_contracts.WhatCameBack` and `agents/page_reader.py`: two images in — the blank
and what came off the glass — and out comes whether anything was added, whether it looks like
the sheet that was handed over, and a few short descriptions of the ink. No rectangles, no
cell kinds, no ids, nothing printed on the paper. `tests/test_page_reader.py` holds the
refusals; `tools/probe_page_read.py` asks the real service, because this project has been
caught by tests that passed against a fake model while three defects waited in the real one.

Against `gpt-5.6-sol`, on pages rendered by the real renderer with a house drawn in one box and
three lines in another:

| what was asked | written | same sheet | said | seconds |
| --- | --- | --- | --- | --- |
| a page written on | yes | yes | *a house with a triangular roof and door drawn in the left box*; *three horizontal lines added at the top of the right box* | 5.48 |
| the same page, untouched | no | yes | nothing | 4.42 |
| a different page | no | no | nothing | 4.47 |

Three for three. What it drew is what it said, it invented nothing on the untouched page, and
the page that was not the one handed over came back as a fact rather than a complaint.

**And it said nothing about the person**, which is the line this reader exists on the right side
of. Not "neatly drawn", not "a good attempt": a house, in the left box.

> One thing the measurement exposes rather than settles: the descriptions came back in English.
> They are read by code and by the continuation prompt, not by anybody in the house, so it may
> not matter — but "may not matter" is how the language defect in `ideas/09 §24` got in, and it
> should be decided rather than left.

**An embedding replaces the code, and it was measured before being believed.** The trick is
the parent's: a page with handwriting on it is a small perturbation of the blank it was printed
from, so its vector sits nearest that blank and the nearest neighbour says which sheet came
back. `embed-v-4-0` — Cohere Embed 4, the only model in swedencentral that represents an image
— was deployed on 24 August 2026 and `tools/probe_embed.py` put three real rendered pages and
three scribbled copies through it.

```
                   una       due       tre
 una scritta    0.8369    0.7760    0.8354   -> una
 due scritta    0.7705    0.7922    0.7744   -> due
 tre scritta    0.8231    0.7676    0.8383   -> tre
```

**Three out of three, and a smallest margin of +0.0015.** It works, and by an amount that is
not an identifier: `una` beat `tre` by a thousandth and a half. The reason is the whole point of
this document. These pages are white sheets with black rectangles on them, and to an embedding
one form looks like another form. A treasure map, a dossier and a museum label would separate
by a great deal more.

So the visual redesign and the identification are not two pieces of work. **They are the same
piece of work**: pages worth looking at are also pages that can be told apart. And the margin is
the measurement that says whether a set of designs is distinctive enough — a number to check,
not a matter of taste.

> A limit of that probe, stated rather than glossed: the simulated handwriting was the same kind
> of random scribble on all three, which pushes them together. Real handwriting differs page to
> page and the margin would probably improve. Probably is not measured.

**The one case an embedding cannot answer** is two blanks that are visually identical — the same
design handed out twice in one afternoon. Nothing visual can separate those. There the house's
own expectation is the tie-break: it knows which sheet it is waiting for. Expectation as the
tie-break and the page as the evidence is the right way round; expectation alone was what this
document proposed before the parent pointed out that it means never reading the object.

**The blank page has to be reproducible, not stored.** The house can re-render it from the same
description the printed one came from; `devices/pretend.py` already does exactly this. Nothing
new is kept on disk, and a page keeps no copy of what somebody wrote on it.

**So a page carries nothing but what it is for.** No code, no markers, no grid — an object in a
story, recognised by looking like itself.

## 4. Ink is a number

"Ecological" is the most useful word in the brief, because it is the only one that can be
measured. A page is ink on paper, and ink runs out in a house.

The example page the parent produced is decorated on all four edges and behind every heading.
On an inkjet that is a page a parent stops printing, and it is also — not coincidentally — a
page that is harder to read.

**The proposal: an ink budget, declared in the format, measured on the rendered page before it
is saved, and refused above it.** The same shape as the six checks in
`shared/experience_checks.py`, which return a list of complaints rather than raising, so that a
refusal can be handed back as a repair request naming what failed.

*The number is not proposed here.* It has to be measured on the ET-2870 that is in the house,
on a page that is liked and a page that is not, and the answer stated with its provenance.
Guessing it would be the same mistake this document exists to correct. `attic/ink_arithmetic.py`
has the machinery for measuring coverage and can come back out for this.

## 5. The words are ours

A model that draws pages will write text into the pixels. The example page shows what that is
worth: a heading that reads **`L'OISONITÀ DUI VHRNA.......`**, and `Merenda` twice in a
four-item checklist. Image models cannot spell, in Italian or in anything else.

That alone would be a reason to draw the text ourselves. It is not the important one.

**Every word an adolescent reads passes one safety gate.** Text baked into an image does not
pass it — it arrives as pixels, is printed, and is read by a person, having been screened by
nothing. That is not a quality problem, it is the single chokepoint the working rules require,
with a hole in it.

So: **the model composes and illustrates; the words are drawn by us, from strings that came
through the gate.** This is not a compromise on beauty. It is how printed matter has always
been made, and it is the only version of this that can be allowed near a person.

What that implies for the artefact: the model's output is not a finished page. It is a
composition — where the illustration goes, where the words go, what the words are *for* — and
the rendering puts real text into it.

## 6. What goes to the attic, and when

The parent's instruction is that a few days of a system that does not work is acceptable,
because nobody is using it, and that the past is not worth being tied to. That changes the
answer from "when the new page can do the old loop" to "now".

To the attic, together, when the new page format is written: `shared/pagedesign.py`, the cell
half of `shared/sheet.py`, the QR contract and the marker detection in `vision/read_sheet.py`,
and the parts of `printing/render.py` that draw fields, markers and codes. `attic/README.md`
already holds things kept for their argument rather than their use, and this is that.

What does not go: the scanner, the print queue, and the whole afternoon — moments, weights,
help, ways out, the ending. None of that is about how a page looks.

## 7. What is not decided here

1. **What the strategy layer is allowed to say.** A closed list of artefact kinds is checkable
   and narrow; free description is expressive and unbounded. The project's habit is closed
   lists, and the habit exists for good reasons, but a closed list of "kinds of object a page
   can be" may be exactly the thing that produces ten afternoons that look the same.
2. **Whether the illustration is generated per page or drawn once and reused.** A generated
   illustration is a model call and money per page; a set of drawn elements composed
   differently each time is cheaper and more consistent, and less surprising. This is a cost
   question with a real number behind it and nobody has measured it.
3. **The ink budget**, above.
4. **What a page looks like when the printer is black and white only**, which the ET-2870 is
   not, but a house might be.
5. **Whether the page is A4 at all.** Nothing requires it except the printer in this house.
6. **What happens to a page nobody brings back.** With no code on it, a sheet that surfaces
   after its afternoon has ended is a drawing and nothing else. That may be the right answer —
   the afternoon is over and there is nothing to continue — but it is a decision and it should
   be made on purpose rather than discovered.

---

*Nothing in this document has been built. It is here to be corrected first.*
