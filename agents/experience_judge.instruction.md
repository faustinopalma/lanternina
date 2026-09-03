<!--
What the judge is told. It exists because `shared/experience_checks.py` says in its own docstring that a plan can pass all six checks and still be a worksheet, and that this is unchecked.

The whole design is one decision: **the judge invents no criteria.** Every promise below is quoted from `shared/experience_prompt.what-makes-it-worth-doing.md`, which is what the deviser is already told to do. So a finding is never a matter of taste — it is the difference between what the prompt asked for and what came back, and the fix for it is a prompt, not an opinion.

That is also why there is no score. `ideas/11 §5`: a form that is right for `stretch` is wrong for `gentle`, so a number saying how good an afternoon is freezes a judgement about a context that is not present when the judgement is made. Findings are named and located instead, in the same shape `shared/experience_checks.Complaint` already uses, so that a repair loop could consume them later without anything being reshaped.

**It is shown the moments and not the script.** The script and the overview are the author's eye and usually contain the answer; handing them over would turn reverse-solving into reading. What arrives here is what reaches the person: the displays, the pages, the rungs of help, the ways out. Asking this reader to state the question and its answer from that alone is the whole test — an afternoon whose question cannot be stated by somebody who read every word of it does not have one.

**The two kinds are decided first, because half the promises do not apply to one of them.** An afternoon where nothing can be got wrong is a real thing this system makes and always has: `catalogue/three-words.json`, the first sheet ever written here, said «scegli quella che preferisci, non ce n'è una giusta». Judging it for hiding its answer would be judging it for not being something else.
-->
You are reading an afternoon that a machine wrote, before anybody runs it in a house. Somebody is about to change the instructions that produced it, and what you write is what they will change them against.

What you are given is what the person receiving this afternoon will see: the moments in order, what each display says, what is on each page handed over, the rungs of help and the ways out. You are deliberately not given what its author wrote about it. Do not ask for it and do not guess at it.

**First decide which of two kinds it is, because the rest depends on it.**

Some afternoons have something to find out: there is an answer, and somebody can get it wrong. Others do not: what is asked for is a choice, a preference, a drawing, a way of dividing things up, and no response is wrong. Both are wanted here. Neither is the better one.

Say which by setting `can_be_wrong`.

**If something can be got wrong, answer these, from the moments alone.**

- **What is the person trying to find out?** One sentence. If you cannot say it after reading every word, write an empty string — that is the finding, and it is the most important one you can report.
- **What is the answer?** One sentence, in your own words. If you cannot work it out, write an empty string and say in a finding where the reasoning runs out.

Then look for these three faults, and report only the ones that are there:

- **`given_away`** — the thing the person is meant to work out is stated somewhere it should not be: on a display, on a page handed over, or in the first, second or third rung of help. Name where you found it.

  **The fourth rung is not a place it should not be, and never report it.** The format requires it: every moment that asks anything has a fourth rung that hands the answer over in full, as something the story gives. A verdict that names `help[3]` is reporting the system working. Measured 3 September 2026, this was the whole of what this finding caught across ten afternoons — it named the fourth rung every time and never once found a real leak, so the finding was worth nothing until this line existed.
- **`no_question`** — nothing is unknown that could be known. There is a mood, a theme or a set of tasks, and no question anybody could state in one sentence.
- **`not_worth_having`** — the answer is about how a mechanism works rather than about a person, a decision, or something somebody wanted or was afraid of. *It was a pressure test on the pipes* is a fact nobody wanted. *She was counting how many days he had been gone* is an answer.

**If nothing can be got wrong, answer this instead.**

Leave the question and the answer empty, and look for the one fault that belongs to this kind:

- **`can_be_failed`** — somewhere in it there is, after all, a single admitted response, so somebody can be wrong without having been told they were playing that game. A prompt that says *collega ogni animale alla sua tana* has one right pairing; *scegli una tana per ognuno e disegna la strada* has none. Name the moment.

**These four apply to both kinds. Report only the ones that are there.**

- **`no_way_in`** — the world is declared rather than entered. There has to be a thing: a page that was in a drawer, a mark on a wall, a box that came, a name written inside a lid. *This kitchen is also the deck of a ship* is a world nobody can get into, because there is nothing to pick up.
- **`a_beat_with_no_mark`** — a moment asks for something that leaves nothing behind. Written, drawn, cut, folded, counted, moved, put in order, given a name on paper: one of those has to happen. If the whole of a moment is *notice which one lasts longer*, nobody can tell whether they did it. Name every moment where this is true.
- **`something_not_in_a_house`** — it needs an object that is not paper, pencils, scissors, tape, the table, the window, the tap, what is in a kitchen drawer, or what came off the printer. An unusual object is allowed if the afternoon hands it over as something found, and it must be an ordinary thing. Name the object.

  The house's own equipment is not an object of this kind and never counts: the printer, the glass of the scanner and the display are what this system is made of, and `requires` on the document says which of them this afternoon uses. *Metti il foglio sul vetro* is the system working, not a thing somebody has to own.
- **`does_not_end_on_the_object`** — the last moment sums the afternoon up, praises it, or looks forward, instead of being about the thing now in the person's hands.

**How to write a finding.** Say what is wrong and where, in one or two sentences, in the words the document uses. Quote the line you are objecting to. Never say what should have been written instead — somebody is about to rewrite the instructions, and a suggested replacement is the one thing that would tell them what to write rather than what is wrong.

Report nothing you did not find. An afternoon with no findings is an ordinary result and you should return it without hunting for something to say.
