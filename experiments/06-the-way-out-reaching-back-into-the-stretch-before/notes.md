# 06 — the way out reaching back into the stretch before

Three runs against `ca-lanternina-dev-api--0000055` (`panel:0a62e51`), 25 August 2026,
908 s for all three.

## What this was testing

Experiment 05 stopped one run in three on `422 refused_by_the_checks`, and the deployed
panel had just been changed to say which check. The reason it gave:

> `moments[0].way_out.in_hand`: the way out of `'join-the-skies'` starts from
> `'il secondo foglio'`, which nothing before it ever mentions

The second sheet had been printed twelve minutes earlier, in the stretch before. So the
refusal was wrong, and the cause was that `the_way_out_starts_from_something` walks a
plan's own moments from the beginning — correct for a whole afternoon, and wrong for a
continuation, which starts in the middle by definition and had nothing before its first
moment. `check()` now takes `already_said`; `panel/continuing.py` passes the words of every
moment up to and including the one being continued from.

## What happened

| | Stretches | Pages | Outcome |
| --- | ---: | ---: | --- |
| try-01 | 3 | 3 | finished |
| try-02 | 2 | 2 | finished |
| try-03 | 2 | 2 | finished |

Three of three reached their ending. Before the fix it was two of three here and one of
three on 24 August, both hitting this check.

The handwriting hand took 23.8–49.1 s per page across the eight pages of these runs, on the
`openai` client rather than the hand-rolled `httpx` loop it used until today. No 429 was
observed in these runs, which is not evidence the retry works — the deployment is capacity
2 and it simply was not busy.

## The limit next to the claim

Three runs is three runs. What it establishes is that the refusal these runs used to hit is
gone; it does not establish a rate for anything else, and two of the three afternoons ran
the same two-stretch shape, so the three-stretch path was exercised once.

## How it went

_Written after looking at the pages. What an assertion cannot say._
