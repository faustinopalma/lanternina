"""Put one designed sheet on paper, from the JSON a design was saved as.

Runs on the hub, because that is where the printer is. It is the same call the house will
make for itself once the blueprint verb carries a design — `ideas/03 §6` step 2 — so a
failure here is a failure there.

    python3 -m tools.print_design design.json /var/lib/lanternina/state/sheets Lanternina

Add `--dry-run` to write the PDF beside the design and send nothing. The sheet's spec is
remembered either way, so a page that comes back is found and read.
"""

from __future__ import annotations

import json
import pathlib
import sys
import time

from devices.print_sheet import compose_and_print
from shared.ids import ExerciseId, SheetId, new_id
from shared.pagedesign import PageDesign


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 3:
        print(__doc__)
        return 2
    design_file, sheets_dir, printer = pathlib.Path(args[0]), pathlib.Path(args[1]), args[2]
    send = "--dry-run" not in argv

    design = PageDesign.from_dict(json.loads(design_file.read_text(encoding="utf-8")))
    sheet_id = SheetId(str(new_id("sh")))
    spec = compose_and_print(
        design,
        sheets_dir=sheets_dir,
        sheet_id=sheet_id,
        exercise_id=ExerciseId(str(new_id("ex"))),
        printer=printer,
        now=time.time(),
        send=send,
    )
    print(f"{spec.title!r}")
    print(f"sheet {spec.sheet_id}, {len(spec.cells)} answerable places")
    print(f"remembered in {sheets_dir}/{spec.sheet_id}.json")
    print("sent to " + printer if send else "not sent (--dry-run)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
