"""What a test run came to, in the few lines a person reads on the run page.

`pytest -q` prints its own summary and GitHub truncates a long log, so the answer to *did
this commit break anything* can end up scrolled off the end of the thing that is supposed
to answer it. This reads the JUnit XML instead and writes Markdown to the job summary,
where it sits at the top of the run whether the run was green or red.

    python tools/ci_summary.py tmp/tests.xml >> "$GITHUB_STEP_SUMMARY"

It prints something whatever it finds. A missing or malformed file means the suite died
before it could write one, which is a worse answer than a failure and must not be reported
as an empty table — `.github/workflows/tests.yml` calls this with `if: always()` precisely
for that case.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# How many failures to name. Beyond this the list stops being read and the file is there.
NAMED = 20


def summary(path: Path) -> str:
    if not path.is_file():
        return f"## tests\n\nNo results at `{path}`: the suite did not get as far as writing one.\n"
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return f"## tests\n\n`{path}` could not be read: {exc}\n"

    suites = [root] if root.tag == "testsuite" else list(root)
    total = sum(int(one.get("tests", 0)) for one in suites)
    failed = sum(int(one.get("failures", 0)) for one in suites)
    errored = sum(int(one.get("errors", 0)) for one in suites)
    skipped = sum(int(one.get("skipped", 0)) for one in suites)
    seconds = sum(float(one.get("time", 0.0)) for one in suites)
    passed = total - failed - errored - skipped

    bad = failed + errored
    lines = [
        "## tests",
        "",
        f"**{'all green' if not bad else f'{bad} failing'}** — "
        f"{passed} passed, {bad} failed, {skipped} skipped, in {seconds:.0f}s",
    ]
    if bad:
        lines += ["", "| what broke |", "| --- |"]
        for case in _broken(root)[:NAMED]:
            lines.append(f"| `{case}` |")
        if len(_broken(root)) > NAMED:
            lines.append(f"| … and {len(_broken(root)) - NAMED} more, in the artifact |")
    return "\n".join(lines) + "\n"


def _broken(root: ET.Element) -> list[str]:
    """Every case with a failure or an error under it, named class-and-method."""
    found = []
    for case in root.iter("testcase"):
        if case.find("failure") is not None or case.find("error") is not None:
            where = case.get("classname", "").replace(".", "/")
            found.append(f"{where}::{case.get('name', '?')}" if where else case.get("name", "?"))
    return found


def main(argv: list[str]) -> int:
    where = Path(argv[1]) if len(argv) > 1 else Path("tmp/tests.xml")
    sys.stdout.write(summary(where))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
