MOMENT CONTRACT
Every moment has:
- id: 2-32 lowercase ASCII letters, digits or hyphens, unique in this activity.
- heading: at most $max_heading characters.
- weights: {"short": W, "standard": W, "extended": W}. W is {"minutes": integer, "lines": [strings]}. Minutes must increase strictly from short to extended, within $min_weight_minutes-$max_weight_minutes. The variants must all permit completion.
- help: exactly $help_levels objects {"after_minutes": integer, "lines": [strings]}, with strictly increasing times in 1-$max_help_after. These are available messages; choose their content from the configurable conduct and review prompts.
- way_out: {"in_hand": string, "heading": string, "lines": [strings], "minutes": integer}. in_hand has at most $max_in_hand characters; minutes is 1-$max_way_out_minutes. Name that material in the way_out lines and in earlier visible content. Describe how to finish from the current state using material actually available.
Every lines list contains 1-$max_lines strings of at most $max_line characters. All headings use the same heading limit.
$acts
