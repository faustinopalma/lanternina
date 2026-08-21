# The attic

Code that worked, answered a question nobody is asking any more, and is kept because
the reasoning in it is worth more than the disk it costs. Nothing here is packaged
(`pyproject.toml` lists the packages by name and this directory is not one of them) and
nothing here runs in the ordinary test run (`testpaths = ["tests"]`).

The tests that came up with their modules still run, from the repository root:

    pytest attic

They are kept runnable rather than commented out because a test that cannot be run is a
claim nobody can check.

## What is here, and what replaced it

| | retired | replaced by |
| --- | --- | --- |
| `layout.py` | 21 Aug 2026 | `shared/pagedesign.py` and `printing/compose.py` — a model designs the page instead of filling a template of four questions and four boxes |
| `test_layout.py` | 21 Aug 2026 | `tests/test_blueprint.py` checks the same property one layer up: every answerable place is on the paper and none of them is a sliver |
| `ink_arithmetic.py` | 21 Aug 2026 | `agents/sheet_reader.py` — a vision model reads the page |
| `test_ink_arithmetic.py` | 21 Aug 2026 | nothing offline; see below |
| `measure_calibration.py`, `probe_sheet_ink.py` | 21 Aug 2026 | nothing — both existed to look at the two thresholds `ink_arithmetic.py` used |

## Why the arithmetic went, when it worked

It read ink out of rectangles a template had declared, which kept the paper path alive
with no cloud at all. It paid for that by making a sheet a form: the only pages it can
read are pages made of boxes in known places. Decided on 21 August 2026 that the price is
too high, and the consequence is stated once rather than discovered — **no cloud, no
reading**. A page that comes back while the panel is unreachable waits.

Its own limit is recorded in the module and is the second reason: a light pencil mark
reads 0.0000, and no threshold fixes that, because the grey threshold is Otsu over the
whole page and is therefore set by print black.

## The copy that is still live, and why

`tools/check_scan.py` holds its own older copy of the same arithmetic, with thresholds of
0.04 and 0.02. It is a diagnostic for a scan — is this page flat, are the four markers
there, does the QR decode — and three tests in `tests/test_printing.py` use its cell
report to check that the renderer's geometry survives a noisy scan. That is a guarantee
about printing, and it is still wanted for the camera work, so the copy stays where it is.
Nothing in the running loop imports it.
