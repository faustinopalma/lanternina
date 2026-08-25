<!--
Every bound the format refuses rather than trims, stated once so a model has a chance of
writing something that parses. shared/experience.py is what actually enforces them.
-->
A line is at most $max_line characters and there are at most $max_lines lines in any list of lines. Every list of lines has at least one line in it.
A weight takes $min_weight_minutes to $max_weight_minutes minutes. A rung of help arrives after 1 to $max_help_after minutes. A way out takes at most $max_way_out_minutes minutes, and what is in_hand is at most $max_in_hand characters.
On a page: its title is at most $max_title characters, a line of its note at most $max_note_line, and a label at most $max_label. These are refused, not trimmed.
At most $max_note_lines lines of note and at most $max_spaces places to write.
