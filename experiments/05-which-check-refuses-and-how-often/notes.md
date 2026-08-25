# 05 — which check refuses, and how often

Three runs against `ca-lanternina-dev-api--0000054` (`panel:5120a4a`), 25 August 2026,
902 s for all three. This is the run that found the defect; the fix and its evidence are in
`06`.

## Why it was run

Experiment 03 stopped on `422 {"detail":"refused_by_the_checks"}` and nothing else, so
there was no way to tell which check refused or whether the transport change that morning
had caused it. The panel was changed to return the reason — the `502` beside it always
had — and this is the first run against that.

| | Outcome |
| --- | --- |
| try-01 | finished |
| try-02 | **refused** |
| try-03 | finished |

## What it said

> `refused_by_the_checks: moments[0].way_out.in_hand: the way out of 'join-the-skies'
> starts from 'il secondo foglio', which nothing before it ever mentions; an ending that
> reaches for an object nobody was given is the goodbye that is felt as a cut`

`il secondo foglio` was printed twelve minutes earlier, in the stretch before. So the
refusal was a false one, and it was not the transport: one in three matches the stop rate
seen on 24 August, before any of this week's changes.

## What it cost to find

Two deploys and about 30 minutes, almost all of it waiting for afternoons to play. The
whole cost was paid because a refusal said only that it had refused. That is the lesson
worth keeping: a message the house cannot act on is a message that has to be paid for twice.

## How it went

_Written after looking at the pages. What an assertion cannot say._
