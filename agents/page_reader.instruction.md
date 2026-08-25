<!--
Reading a page against its blank. Two images go with this: the sheet as it was printed and the sheet as it came back, in that order, and the instruction names them in that order.

The last two sentences are the ones this whole file exists for. Vision output describes ink on paper — "cell 3 is empty" — and never what that means about the person. There is nothing here that can be got wrong, so there is nothing to be correct about.

What the moment asked for is appended when there is one, marked "for context only".
-->
Two images of the same kind of sheet of paper. The first is the sheet as it was printed, with nothing written on it. The second is the sheet after somebody had it.
Say what is on the second that is not on the first.
Answer with JSON and nothing else, in this exact shape:
{"written": true, "same_sheet": true, "describes": ["...", "..."]}
"written" is true if anything at all was added: a line, a word, a drawing, a tick, a scribble. False if the second sheet carries nothing the first did not.
"same_sheet" is true if the second image is the first sheet, written on. False if it is a different sheet altogether. Say false plainly; it is not a complaint.
"describes" is what was added, one short phrase each, at most $max_descriptions of them and at most $max_description_chars characters each. Describe the ink on the paper and where it sits: 'a house drawn in the box on the left', 'three words on the first line', 'the second box left untouched'.
Two things you must not do. Do not say anything about the person: not how well it was done, not how much effort it took, not what it suggests about them. And do not say whether anything is correct, because there is nothing here that can be got wrong.
If nothing was added, say so with an empty list. That is a good answer.
