# The methods

One record per method that can actually be run in a house with a printer, a scanner and a small display. Each says what it is, how to build one, which parts of it move and what happens when they are moved, where the part that does the work sits, and where it breaks.

It is the operational half of [enciclopedia/](../enciclopedia/README.md), which is research and is frozen. The encyclopedia asks *what forms exist*; this asks *how do I build one of these, here, tonight*. The two are not one-to-one and are not meant to be: several entries collapse into one record when they are the same thing under different names, one entry becomes two records when it holds a form and a move, and a record may exist that no entry describes.

## Why it exists

`agents/experience_deviser.py` devises an afternoon from nothing. Nothing in its prompt says what forms exist, so it reaches for the ten anybody reaches for. The encyclopedia's own statement of purpose is the statement of purpose here too: *chi deve proporre qualcosa da fare ne conosce una decina e usa sempre quelle.* A record in the prompt is how one of the other three hundred gets a turn.

It does not all fit. Measured 3 September 2026: the three sections of an entry that teach construction average 5 503 characters, so 327 of them are 1 799 kB against a rendered prompt of 25 330 bytes. A record's prompt-facing half turned out to average 2 316 characters — the first estimate was 800 and was wrong by nearly three times — so five records are 11.3 kB, which is 45% of the prompt as it stands. That settles the serving: a prompt gets a long list of names and one or two records in full, not five. `ideas/11-the-methods.md` holds the argument for why the choice of which is made in code rather than by similarity.

## What is in it, measured

204 records, written 3 September 2026 from 323 of the 395 entries.

| | |
| --- | --- |
| kind | 136 `form`, 68 `move` |
| verification | 93 `in_the_sheet`, 68 `nowhere`, 34 `in_the_object`, 9 `needs_a_person` |
| adult_cost | 182 `none`, 17 `take_part`, 5 `prepare` |
| comes_back | 173 `a_sheet`, 21 `nothing`, 10 `a_photograph` |
| letters_inside_words | 180 `no`, 16 `to_compose`, 5 `both`, 3 `to_solve` |
| people | 183 need one, 21 need two |
| entries per record | 112 records from one entry, 58 from two, 34 from three or more, one from nine |

The collapse is real but smaller than expected: 112 of 204 records come from a single entry. The chapter that folded hardest is 12, classical Italian word puzzles, where 48 entries became 22 records and nine of them became one — nine named letter operations that all give a builder the same three instructions.

**72 entries have no record, and the reasons are not equal.** Chapter 3's ten leave whole and by kind: they are a taxonomy of what a request arrives on, not techniques, and their content is the schema of properties instead. Chapter 9 lost five to a rule rather than to a failing — a run of days, a variable-ratio reward, an inactivity notice, a progress bar and a campaign across twelve afternoons all work by making it hard to stop, which this system refuses. Chapter 11 lost one ending for the same reason. Entry 289 was discarded because it is documentation of a product wearing the vocabulary of a form; it had already survived one automated check that way.

The rest is thinness rather than judgement, and should be said plainly: **chapter 4, how a request is packaged, has 17 of its 27 entries untaken, and chapter 7, formal constraints, has 13 of 18.** Those are the two chapters to write next, and chapter 4 is the one that matters most, because it is the catalogue of wrappers and the deviser's prompt already asks for an afternoon that begins in the middle of something.

## Two kinds

**`form`** — produces something somebody does. A cut-up text to reorder, a chain of estimates, a grid to fill.

**`move`** — does not produce anything on its own; it is applied to a form and changes it. A thing put where somebody will look that turns out to do nothing. Asking for the same quantity twice by different roads. A move declares what it costs when applied, and its `comes_back` is what it adds, which is usually nothing.

The distinction was found by writing the third record: entry 185, *rossa aringa*, is described by the encyclopedia as «l'unica forma raccolta finora il cui contenuto è zero». A schema with only forms in it had nowhere to put that, and would have thrown away the entries that are most reusable.

## The rule that decides what a record says

**A record describes the version worth building, not the family.** The encyclopedia is neutral because a map that shows only the roads people take does not say where you are. A manual is not neutral: it fixes the knobs that have a right answer and says why.

Entry 359 is where this was found. A chain of estimates has its verification nowhere — there is no answer to check. Asking for the same quantity by two independent roads, and declaring that they agree when the larger over the smaller is under ten, puts the verification inside the sheet and costs one line. The record therefore says `"verification": "in_the_sheet"` and its `how` tells you to ask twice. Recording `nowhere` would have been true of the family and useless to whoever has to build one tonight.

Where a knob moves a declared property, the record fixes the knob, and `how` says what was fixed.

## What a record holds

One JSON file per method, `<method_id>.json`.

| field | what it is |
| --- | --- |
| `format_version` | `1` |
| `method_id` | the file's name: lowercase, digits and hyphens, 3 to 48 characters |
| `kind` | `form` or `move` |
| `name` | at most 60 characters, a phrase saying what somebody does. This is the label two afternoons using this method would both be written into, which is what makes them comparable |
| `also` | the other names, including the Italian ones, so a person coming from the encyclopedia finds it |
| `one_line` | what it is, in one sentence, at most 160 characters |
| `from_entries` | the encyclopedia entries this came from, by number. Many allowed, none allowed when the record is new |
| `how` | how to build one, 150 to 700 characters. Written to somebody who has to make one and has not seen it before |
| `knobs` | 2 to 5 parts that move, each `knob` and `effect`. The effect is the half that matters: not that there is a knob, but what happens at each setting |
| `where_the_work_is` | which part of it does the work, so that whoever cuts something cuts the right thing |
| `breaks` | where it fails on a printed sheet, a scanned page or eight hundred by four-eighty pixels. Empty string when nothing was found, and that is a claim |
| `adult_cost` | `none`, `prepare`, `take_part` |
| `verification` | `in_the_sheet`, `in_the_object`, `needs_a_person`, `nowhere` |
| `comes_back` | `nothing`, `a_sheet`, `a_photograph` |
| `people` | the fewest it works with, `1` or `2`. Some methods take more and are better with more; the field says the floor, not the number |
| `letters_inside_words` | `no`, `to_solve`, `to_compose`, `both`. Which side of the method rests on looking inside words, which is the operation a language model cannot do reliably |
| `goes_with` | encyclopedia entry numbers that sit well beside it. Numbers and not method ids, so that a record written on its own never points at nothing |

A knob's `effect` describes every setting, including the one `how` has just told you not to use. That is deliberate: the reason a choice was made is the part that teaches, and a record that only describes the chosen setting cannot be argued with.

## What the first chapter changed

The contract above is version 1 as revised on 3 September 2026, after chapter 13 was written against the first draft of it. Four things were wrong and the records found them.

**`verification` had no value for *the object settles it*.** Scissors counting whole paper rings, a compass closing on a heptagon, a soap film pulling into the shortest network: none of those is checked by the sheet, by a person, or by nothing. Written as `in_the_sheet` — the nearest of the three that existed — a record contradicted its own `breaks` field, which said in the same file that the sheet could not catch a wrong row. `in_the_object` is the fourth value, and the distinction it carries is one a builder needs: an object that cannot lie, against a sheet that can be filled in wrongly.

**`moments` was removed.** It was meant to say how few moments of an afternoon a method needs. Sixteen records were written and all sixteen said `one`, because nothing in the research says how long anything takes. A field with one value carries no information, and each of those values was a guess written in the grammar of a declaration.

**`needs_letters_inside_words` became `letters_inside_words`, with four values.** A cryptarithm is solved by doing a sum and never by reading the words — the entry says it can be solved without knowing the language. Composing one is a search inside words, and that is the half a model gets wrong. One boolean could not say which side the difficulty was on, so the flag was set to the wrong answer whichever way it went.

**`breaks` went from 400 characters to 600.** There are three surfaces — a printed sheet, a page scanned and read back, eight hundred by four-eighty pixels in one bit — and several methods break differently on each. Four hundred characters bought roughly one sentence, so the weakest of the three was being dropped.

What did not change, and was complained about: `comes_back` still has no value for *an object stays on the table*, and `people` still cannot say *two, and better with four*. Both are known and neither has yet cost a record its meaning.

**Two length ceilings were wrong twice, in the same direction.** They were first set from the prompt budget — how much room five records could have — which is a different constraint from how long a record has to be to teach the thing. The record on moiré patterns carries a line pitch of 1.016 mm, the constant that follows from it, and the fact that printing at 94% falsifies every angle read off the sheet while the bands still appear exactly as promised. That is 2 570 characters with nothing spare in it.

The ceilings now sit above the measured maximum, and the measurement is the point. Across 157 records written before they were raised: `how` had a median of 643 and a maximum of 818 against a ceiling of 700, and the ninetieth percentile was 697 — three characters under it. Writers were being shaped by the number rather than caught by it, which is the same failure the prompt notes record about stating a number of sheets. `how` is now capped at 850 and a whole record at 2 900. The prompt is made to fit by serving fewer records, never by writing shorter ones.

## Why English, when the research is Italian

Every prompt block in this repository is English, and the content language is a household setting rather than a property of the machinery — the decision recorded as #4 in [ideas/README.md](../ideas/README.md). A manual written in Italian would be machinery that assumes the house speaks Italian. The Italian names stay in `also`, which is the line somebody uses to get from an encyclopedia entry to its record.

What this costs: every record is a translation as well as a compression, and a translation loses. The Italian playable examples are not carried over at all — they are the encyclopedia's, and a record points back with `from_entries` rather than restating them.

## Verify

```
python tools/methods_check.py
```

It checks the contract, that `name` is unique across the corpus, that every `from_entries` and every `goes_with` names an entry that exists, and that a record does not say its verification needs a person while also saying the adult pays nothing — if somebody has to check it, somebody is taking part. It fails if it finds no records: a check that can pass on zero files is not a check.
