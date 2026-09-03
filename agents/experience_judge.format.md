<!--
The shape of the answer. Separate from the instruction because the instruction is an argument and this is a contract, and the two get edited for different reasons.

The names in `finding` are closed on purpose. An open string would let a judge invent a category, and a category invented once cannot be counted across runs — which is the whole point of running this ten times rather than once.
-->
Answer with one JSON object and nothing else. No prose before it and none after.

    {
      "can_be_wrong": true,
      "question": "$max_line characters at most, or an empty string",
      "answer": "$max_line characters at most, or an empty string",
      "findings": [
        {"finding": "given_away", "where": "moments[2].lines[1]", "says": "what is wrong, in one or two sentences, quoting the line"}
      ]
    }

`finding` is one of exactly these words, and you may use each at most once except `a_beat_with_no_mark`, which may name several moments in one entry:

    given_away  no_question  not_worth_having  can_be_failed
    no_way_in  a_beat_with_no_mark  something_not_in_a_house  does_not_end_on_the_object

`where` names the place the way the document names it — `moments[3].way_out`, `moments[0].page.lines[2]` — so that somebody can go straight to it. Where a finding is about the whole afternoon, write `experience`.

`findings` is an empty list when there is nothing to report, and that is a normal answer.
