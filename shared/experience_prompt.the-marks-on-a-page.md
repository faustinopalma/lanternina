<!--
What a page is, described so a model can write one. The page is drawn whole from what it says it is: nothing here ever mentions where on the paper anything goes.

The "spaces" line closed with two braces until 25 August 2026, when moving this text out of Python showed why: the f-string had been split across three source lines and the third had no `f` prefix, so its `}}` stayed two braces instead of collapsing to one. The model had been reading an unbalanced JSON example. It is one brace here.
-->
PAGE CONTRACT
A page is {"kind": string, "title": string, "note": [strings], "spaces": [{"label": string, "room": string}], "illustration": string}.
kind is one of $kinds. A label permits at most one space; a notice permits none. Other kinds permit at most $max_spaces spaces. room is a_line, some_lines or a_box.
title has at most $max_title characters; note has at most $max_note_lines strings of at most $max_note_line characters; each label has at most $max_label characters. These are the printable words, in the activity's language.
illustration has at most $max_illustration characters and specifies visual content in English. Required words belong in the printable fields. The image cannot supply unspecified facts or guarantee exact measurements. The page maker sees only these fields. Choose the kind and content according to the configurable prompts; diagrams and factual worksheets are allowed.
