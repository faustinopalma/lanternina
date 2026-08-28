# What the evidence says

This file exists because the rules in `.github/copilot-instructions.md` were written from judgement, and judgement is a bad thing to leave unexamined when the person on the other end of it is an adolescent who may find reading hard. It reads the literature that bears on what Lanternina offers and how it offers it, and says — for each finding — what it changes here, what it does not, and where it argues against something already built.

**One rule governs everything below, and it is not up for revision.** This is evidence about *design*, never about a person. Nothing here becomes a field, a setting per adolescent, a level, or an inference. Lanternina is built for adolescents without asking which ones (`docs/NON-GOALS.md`), and the way that stays true while the design gets better is that findings change what the system *makes*, and never what it *records*. A finding that could only be applied by first classifying somebody is a finding this project declines to use.

The sources are in `_reference/progettare-per-adolescenti/`, downloaded by `build/fetch_evidence.py` on 28 August 2026. That folder is gitignored: it is other people's text. What is committed is this reading of it.

---

## The sources, and how much weight each carries

| Source | What it is | Weight |
| --- | --- | --- |
| W3C, *Making Content Usable for People with Cognitive and Learning Disabilities* | A W3C Group Note: eight design objectives, user stories, patterns, ten personas. Written with people who have these disabilities in the working group. | The heaviest here. It is consensus guidance, aimed at design rather than at diagnosis, and it is the only source that speaks directly about the population this file is about. |
| Inclusion Europe, *Informazioni per tutti* (2010) | The European easy-to-read standards. Italian and English both kept: the two are not word-for-word and the Italian is stricter in places. | Concrete and checkable — line length, one idea per sentence, typeface, numbers. Its authority is convention, not experiment. |
| CAST, *UDL Guidelines 3.0* (2024) | Three principles — engagement, representation, action & expression — under which sit thirty-odd considerations. | A framework, not a finding. Useful as a checklist of what a design forgot; weak as evidence that any one choice is right. |
| Sweller and colleagues, cognitive load theory | Working memory as the binding constraint on learning. Intrinsic, extraneous and germane load; the split-attention, worked-example and expertise-reversal effects. | Experimental, replicated, and the effects below are the well-attested ones. The three-way split of load itself is contested (de Jong 2009). |
| Kirschner, Sweller & Clark (2006) | Argues that minimally guided instruction fails, and fails worst for those with least prior knowledge. | Strong on the direction, and it is a polemic: read the replies too. Not downloaded here. |
| Lepper, Greene & Nisbett (1973); Deci, Koestner & Ryan (1999) | The overjustification effect and its meta-analysis: expected tangible rewards reduce intrinsic motivation for an activity somebody already found interesting. | The finding is real and the boundaries matter more than the headline. See §4. |
| Cameron, Banko & Pierce (2001) | The rebuttal: the negative effect of rewards is narrow, not pervasive. | Kept on purpose. One side of a literature is not a source. |

Two were not downloaded — Sweller, van Merriënboer & Paas (1998) answered 404, Kalyuga et al. (2003) returned an empty file. They are cited below from the record, not from a copy on disk, and `_reference/progettare-per-adolescenti/SORGENTI.md` says so.

The addresses are here rather than only in `build/fetch_evidence.py`, because `build/` is gitignored and a source list that does not survive a clone is not a source list. Fetched 28 August 2026:

- <https://w3c.github.io/coga/content-usable/> — the working group's copy; `www.w3.org/TR/coga-usable/` answers 403 to a non-browser client.
- <https://www.inclusion-europe.eu/wp-content/uploads/2017/06/IT_Information_for_all.pdf> and the `EN_` file beside it.
- <http://www.inclusion-europe.eu/wp-content/uploads/2020/06/Easy-to-read-checklist-Inclusion-Europe.pdf>
- <https://udlguidelines.cast.org/> — read on the site; the printable organiser is on its downloads page.
- <https://research.ou.nl/ws/files/1015152/Why%20minimal%20guidance%20during%20instruction%20does%20not%20work.pdf>
- <http://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Motivation/Lepper_et_al_Undermining_Childrens_Intrinsic_Interest.pdf>
- <http://www.behavior.org/resources/331.pdf>

---

## 1. The defect we found by hand on 28 August has a name

Three afternoons were written by hand and their pages drawn by the real model (`private/`, gitignored). One page did not work: an acquisition sheet whose premise — *go and find something in the house that no longer works* — was only ever said on the display. The paper assumed somebody had read the display and remembered it.

That is the **split-attention effect** (Chandler & Sweller 1992): when two sources of information are each incomprehensible alone and must be held together, working memory pays for the integration, and the payment comes out of the same pool the task needs. It is the textbook case of extraneous load — load that the design imposed and the design can remove.

**W3C COGA says the same thing twice**, from the user's side. Objective 5, *help users focus*: after attention is lost, somebody needs to restore the context. Objective 6, *ensure processes do not rely on memory*. A display shows one thing for a few minutes; a sheet lies on a table for forty-five. Putting the premise on the display and the task on the paper is a process that relies on memory, in a system whose whole design is otherwise built not to.

**What this changes.** The first sheet an afternoon hands over carries its own premise and its own first physical step. Later sheets may lean on the sheets already on the table, because those are still there. This is not a matter of taste and it is not about good writing — it is about which of the two objects survives the ten minutes after it is read.

## 2. Two sheets are better than one crowded sheet

COGA objective 3, on clear content, asks for *"small or short chunks of content"* and *"a good use of white space, so that the chunks are clear and the page does not get overwhelming."* Kwame, one of its personas, is written around this: complex, content-heavy presentation *"shuts his brain down"*.

The easy-to-read standards go further and are checkable: one idea per sentence, one sentence per line where the layout allows it, never split a sentence across two pages, left-align rather than justify.

Measured on the eight pages drawn on 28 August: ink covered 1.79 % to 4.57 % of the sheet, mean 3.1 %. The two heaviest were the two that asked for four things; the two lightest asked for one. The page judged best asked for nothing at all — it was a notice to be read standing up, and the sheet to be filled in came after it.

**What this changes.** An afternoon may print more than one sheet, and where the alternative is one crowded page it should. The bound is the person's attention, not a rule, and "not an encyclopedia every time" is the other half of the same sentence.

## 3. A question with one right answer is allowed. A wrong answer with a consequence is not

Kirschner, Sweller & Clark (2006) argue that minimally guided instruction — discover it yourself, work it out — is the format that fails hardest for people with the least prior knowledge, because it loads working memory with search instead of with the thing being learnt. The remedy they give is the **worked example**: show one done, then ask for the next.

This cuts against a reading of Lanternina's own rules that nobody wrote but everybody could reach: that because *nothing can be failed*, nothing may have an answer. That reading produces afternoons where every question is open, every answer is accepted, and nothing is ever actually asked. It is the failure `ideas/08 §15` describes from the other direction.

**What this changes.** *Nothing can be failed* is about **consequence**, not about the existence of a right answer. An afternoon may pose a question that has one — a thing to work out, a code to break, a shape that fits — provided that getting it wrong costs nothing, that the ending stays reachable from wherever it got to, and that the way through is written down and given rather than left to be discovered. The seventh property already required this and was reading as though it did not.

## 4. Why there are no streaks, stated with its limit

Lepper, Greene & Nisbett (1973) gave children who already enjoyed drawing an expected reward for drawing; afterwards they drew less than children who got nothing. Deci, Koestner & Ryan's 1999 meta-analysis found the same across 128 experiments: expected, tangible, task-contingent rewards reduce intrinsic motivation.

**The boundary is where the argument actually lives, and it does not favour us as much as the headline does.** The effect is strongest when initial interest is *high*. Where initial interest is low, the same literature finds rewards can raise engagement (Cameron, Banko & Pierce 2001), and the 1999 meta-analysis itself reports that verbal, informational feedback — as opposed to controlling feedback — does not undermine and may help. The effect is also reported as stronger in children than in adults.

**What this changes: nothing, and now the reason is written.** Lanternina offers a thing somebody is expected to find interesting, to an adolescent, unprompted. That is precisely the cell of the design space where the undermining effect is best attested. Points, streaks and unlockables would be buying attendance with the thing attendance is for. The honest limit: for an activity nobody wants to start, this literature says a reward can be the way in, and we are declining a tool that works in a case we have chosen not to be in. If Lanternina were ever asked to get somebody through something they did not want to do, this paragraph would have to be rewritten rather than pointed at.

## 5. Metaphor is a per-household matter, not a house style

COGA is direct about it: *"People with social or communication disabilities may need clear literal language and may not understand metaphors or non-literal text."* Amy, its autistic persona, is written around exactly this: images that do not directly represent something make her uneasy; *"the wheels of justice turn slowly"* is a sentence she would rather not have been written. The easy-to-read standards say the same in one line: do not use metaphors.

The afternoons written so far lean the other way. *La stanza che qualcuno ha descritto male* is a figure held for ninety minutes; *il museo delle cose che non hanno funzionato* is an inversion, and the inversion is the game.

**Both are right and they are about different households.** This is not a rule to be applied to everybody, because applying it to everybody would remove from every adolescent something some of them enjoy — the same mistake in the opposite direction. It is a setting a parent already has: `panel/preferences.py` carries `difficulty` and a standing note. What is missing is a way to say *literal, please*, and that is a legitimate thing to add.

**What this changes.** A new content setting, phrased about the material and never about the person: whether an afternoon may be built on a figure, or should say what it means. Default is the current behaviour; the parent moves it. It reaches the deviser prompt the way `shape` and `distance` already do.

## 6. Things that are simply checkable, and are not checked

From the easy-to-read standards, and each of these is a line in a checker rather than a line in a prompt:

- **One sentence per line, where the line allows it.** The display cap is 44 characters, measured: 44 characters of ordinary Italian come to 681 px in the body font, against 728 px of usable width. Nothing today refuses a display line that is half a sentence.
- **Never split a word across a line break.** Nothing checks this.
- **Sans-serif type.** `agents/page_maker.kind-label.md` produced a serif, printed-looking page on 28 August, while `how-it-is-drawn.md` two files away asks for hand-drawn. That is now a documented defect rather than a matter of taste.
- **Numbers as digits, not words** — *3*, not *tre* — and avoid percentages and large numbers entirely. Jonathan, COGA's persona with dyscalculia, needs *"words rather than numbers"*; the easy-to-read standards want digits where a number is unavoidable. The two are not in conflict: prefer no number, and where one is needed write the digit.
- **Say what a task needs before it starts.** COGA objective 7, task management: *"I need to know how to start a task, and what is involved: the steps, a time estimate, any materials I may need."* The format has no field for the materials an afternoon needs, and a moment that asks for scissors in a house with no scissors is a moment that fails silently.

## 7. One way to answer is one way too few

UDL 4.1 asks a design to *vary and honour the methods for response*. Every moment in the format today is answered the same way: write or draw on paper, put the paper on the glass. The house has a display with buttons and a scanner, and a sheet returned the other way up is a different answer through the same equipment at no cost.

This is a framework's suggestion, not a finding, and it is written here as one.

---

## What the evidence does not say

- **Nothing here is about adolescents specifically.** COGA's personas are adults; the cognitive-load work is mostly on students and school-age children; the overjustification work spans both and reports the effect differs by age. Reading any of it as though it were about a fifteen-year-old at a kitchen table is an extrapolation, and it is stated here so that it does not quietly become a citation.
- **Nothing here validates a single afternoon.** These are constraints on form. Whether *il turno delle 15:40* is worth an hour of somebody's Saturday is a question no literature answers, and the only way to find out is the one already in use: run it, and look at the paper.
- **Nothing here supports grading the person to fit the material.** The expertise-reversal effect (Kalyuga et al. 2003) says support that helps somebody with little prior knowledge harms somebody with a lot — which is a real argument for adapting, and would be a bad argument for storing an estimate of anybody. What it supports is what is already built: three written weights, four rungs of help, and a parent who moves the setting.

## Where this is meant to be used

By whoever writes the prompts in `agents/`, and by whoever reviews an afternoon before it is offered. It is not a specification and nothing in it is enforced. Where a finding here has become a rule, the rule is in `.github/copilot-instructions.md` and says so; where it has become a check, the check is in `shared/experience_checks.py` or `shared/page.py`. Everything else in this file is an argument, and arguments are for reading.
