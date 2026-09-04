"""The research runs as one page a developer reads, built from the run directories.

    python -m research.reader        # writes build/research.html and says where

**Why this is not in the panel.** It used to be, and that was the mistake: axis means are a
developer's material and the panel belongs to a parent, who has no decision that changes
because `sheetStandsAlone` moved from 2.88 to 2.46. This repository's own rule is that a
string in the panel earns its place only if it changes what the parent does next.

**What it has to show, and why all three.** A score on its own cannot be acted on. To know
what to change you need the input that produced the afternoon — the household's settings,
what had already been offered there, the method drawn from `methods/` — and the output it
actually produced, and then the score with the judge's reason beside each axis. Any two of
the three leave you guessing at the third.

Self-contained: one HTML file, no server, no network, nothing to install. It goes to
`build/`, which is gitignored, because it is derived and rebuilt in under a second. The
definition stays `research/runs/`.

Older runs carry less than newer ones — the input block and the devised document were added
on 4 September 2026, and the method on 3 September. The page says *not recorded* rather than
pretending, because a blank that looks like an empty value is worse than a missing one.
"""

from __future__ import annotations

import html
import json
import webbrowser
from pathlib import Path
from typing import Any

from .report import IN_ORDER
from .scores import RUNS, collect

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "build" / "research.html"


def _rows(runs: Path) -> list[dict[str, Any]]:
    """Every afternoon of every run, newest run first, carrying its run's prompt."""
    found: list[dict[str, Any]] = []
    for folder in sorted((p for p in runs.glob("*") if p.is_dir()), reverse=True):
        where = folder / "afternoons.json"
        if not where.is_file():
            continue
        try:
            afternoons = json.loads(where.read_text(encoding="utf-8"))
        except ValueError:
            continue
        prompt = ""
        summary = folder / "summary.json"
        if summary.is_file():
            try:
                prompt = json.loads(summary.read_text(encoding="utf-8")).get("prompt") or ""
            except ValueError:
                prompt = ""
        label = folder.name.partition("Z-")[2] or folder.name
        for one in afternoons:
            found.append({**one, "run": label, "prompt": prompt})
    return found


_CSS = """
:root { --ink:#1a1a1a; --quiet:#6b6b6b; --edge:#e0ddd8; --paper:#faf9f7; --warm:#f3f0ea; }
* { box-sizing:border-box }
body { margin:0; background:var(--paper); color:var(--ink);
  font:15px/1.55 ui-sans-serif,-apple-system,Segoe UI,Roboto,sans-serif; }
header { padding:24px 32px; border-bottom:1px solid var(--edge); position:sticky; top:0;
  background:var(--paper); z-index:5 }
h1 { margin:0 0 6px; font-size:19px; font-weight:600 }
.quiet { color:var(--quiet); font-size:13px }
main { padding:24px 32px 80px; max-width:1180px }
table.runs { border-collapse:collapse; margin:8px 0 28px; font-size:13px }
table.runs th, table.runs td { padding:5px 14px 5px 0; text-align:right;
  border-bottom:1px solid var(--edge) }
table.runs th:first-child, table.runs td:first-child { text-align:left }
details.aft { border:1px solid var(--edge); border-radius:8px; margin:0 0 10px; background:#fff }
details.aft > summary { cursor:pointer; padding:11px 14px; display:grid;
  grid-template-columns:150px 1fr 120px 62px; gap:14px; align-items:baseline; list-style:none }
details.aft > summary::-webkit-details-marker { display:none }
summary .t { font-weight:600 }
summary .r { color:var(--quiet); font-size:12px }
summary .m { color:var(--quiet); font-size:12px; text-align:right }
.mean { font-variant-numeric:tabular-nums; text-align:right; font-weight:600 }
.body { padding:4px 14px 18px; display:grid; grid-template-columns:1fr 1fr; gap:20px }
.body h3 { font-size:12px; text-transform:uppercase; letter-spacing:.07em; color:var(--quiet);
  margin:14px 0 6px; font-weight:600 }
.wide { grid-column:1 / -1 }
pre { white-space:pre-wrap; word-break:break-word; background:var(--warm); padding:10px 12px;
  border-radius:6px; margin:0; font:12.5px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;
  max-height:420px; overflow:auto }
dl { margin:0; display:grid; grid-template-columns:auto 1fr; gap:2px 12px; font-size:13px }
dt { color:var(--quiet) } dd { margin:0 }
table.axes { border-collapse:collapse; width:100%; font-size:13px }
table.axes td { padding:5px 10px 5px 0; border-bottom:1px solid var(--edge); vertical-align:top }
table.axes td.n { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; width:26px }
.s1,.s2 { color:#a33 } .s4,.s5 { color:#2c6e49 }
.none { color:var(--quiet); font-style:italic }
.bad { background:#fdf3f2; border-left:3px solid #a33; padding:8px 12px; border-radius:4px;
  font-size:13px; margin-top:6px }
input[type=search] { padding:6px 10px; border:1px solid var(--edge); border-radius:6px;
  font:inherit; width:280px; background:#fff }
"""

_JS = """
const box = document.getElementById('find');
box.addEventListener('input', () => {
  const q = box.value.toLowerCase();
  let shown = 0;
  for (const el of document.querySelectorAll('details.aft')) {
    const hit = !q || el.dataset.hay.includes(q);
    el.style.display = hit ? '' : 'none';
    if (hit) shown++;
  }
  document.getElementById('count').textContent = shown;
});
"""


def _esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def _pre(value: Any) -> str:
    if value in (None, "", [], {}):
        return '<p class="none">non registrato</p>'
    said = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    return f"<pre>{_esc(said)}</pre>"


def _axes_table(appraisal: dict[str, Any]) -> str:
    axes = appraisal.get("axes") or {}
    if not axes:
        return '<p class="none">nessun punteggio: il pomeriggio non è arrivato</p>'
    out = ["<table class='axes'>"]
    for axis in IN_ORDER:
        said = axes.get(axis)
        if not said:
            continue
        score = said.get("score")
        out.append(
            f"<tr><td>{_esc(axis)}</td><td class='n s{_esc(score)}'>{_esc(score)}</td>"
            f"<td>{_esc(said.get('says', ''))}</td></tr>"
        )
    out.append("</table>")
    worst = appraisal.get("worstLine")
    if worst:
        out.append(f"<div class='bad'><b>La riga da cambiare:</b> «{_esc(worst)}»</div>")
    change = appraisal.get("whatToChangeInThePrompt")
    if change:
        out.append(f"<div class='bad'><b>Al prompt:</b> {_esc(change)}</div>")
    return "".join(out)


def _one(row: dict[str, Any]) -> str:
    appraisal = row.get("appraisal") or {}
    axes = appraisal.get("axes") or {}
    scores = [one.get("score") for one in axes.values() if isinstance(one.get("score"), int)]
    mean = f"{sum(scores) / len(scores):.2f}" if scores else "—"
    refused = row.get("refused") or {}
    title = row.get("title") or "rifiutato"
    given = row.get("input") or {}
    built = row.get("builtFrom") or {}

    facts = [
        ("casa", row.get("household", "")),
        ("interessi", ", ".join(given.get("interests", [])) or "—"),
        ("da evitare", ", ".join(given.get("avoid", [])) or "—"),
        ("forma", given.get("difficulty", "")),
        ("varietà", given.get("variety", "")),
        ("fogli", given.get("sheets", "")),
        ("nota", given.get("note") or "—"),
        ("umore", row.get("mood", "")),
        ("peso", row.get("weight", "")),
        ("metodo", built.get("form") or "—"),
        ("mossa", built.get("move") or "—"),
        ("prompt", row.get("prompt") or "—"),
    ]
    listed = "".join(
        f"<dt>{_esc(k)}</dt><dd>{_esc(v)}</dd>" for k, v in facts if v not in (None, "")
    )
    if not given:
        listed += "<dt>—</dt><dd class='none'>input non registrato in questa corsa</dd>"

    hay = " ".join(
        str(x).lower()
        for x in (title, row.get("household"), row.get("run"), built.get("form"))
        if x
    )

    how = "rifiutato" if refused else row.get("ending", "")
    parts = [
        f"<details class='aft' data-hay=\"{_esc(hay)}\">",
        "<summary>",
        f"<span class='r'>{_esc(row.get('run', ''))} · {_esc(row.get('iteration', ''))}</span>",
        f"<span class='t'>{_esc(title)}</span>",
        f"<span class='m'>{_esc(how)}</span>",
        f"<span class='mean'>{mean}</span>",
        "</summary>",
        "<div class='body'>",
        "<div><h3>input — che cosa ha deciso questo pomeriggio</h3>",
        f"<dl>{listed}</dl>",
        "<h3>già offerti qui</h3>",
        _pre(given.get("already")),
        "</div>",
        "<div><h3>punteggio, con la motivazione del giudice</h3>",
        _axes_table(appraisal),
        "</div>",
    ]
    if refused:
        parts += [
            "<div class='wide'><h3>rifiutato</h3>",
            f"<div class='bad'>{_esc(refused.get('by'))}: {_esc(refused.get('says'))}</div></div>",
        ]
    parts += [
        "<div class='wide'><h3>output — la sintesi che un genitore legge</h3>",
        _pre(row.get("overview")),
        "</div>",
        "<div><h3>output — il copione</h3>",
        _pre(row.get("script")),
        "</div>",
        "<div><h3>i passaggi — l'afternoon giocato</h3>",
        _pre(row.get("transcript")),
        "</div>",
        "<div class='wide'><h3>output — il documento come è stato scritto</h3>",
        _pre(row.get("experience")),
        "</div>",
        "</div></details>",
    ]
    return "".join(parts)


def page(runs: Path = RUNS) -> str:
    history = collect(runs)
    rows = _rows(runs)
    head = ["<tr><th>corsa</th><th>prompt</th><th>pomeriggi</th><th>rifiutati</th>"]
    head += [f"<th>{axis[:9]}</th>" for axis in IN_ORDER]
    head.append("<th>media</th></tr>")
    body = []
    for one in reversed(history):
        axes = one.get("axes") or {}
        mean = sum(axes.values()) / len(axes) if axes else 0
        cells = [
            f"<tr><td>{_esc(one.get('label'))}</td><td>{_esc(one.get('prompt') or '—')}</td>",
            f"<td>{_esc(one.get('afternoons'))}</td><td>{_esc(one.get('refused'))}</td>",
        ]
        cells += [f"<td>{axes[a]:.2f}</td>" if a in axes else "<td>—</td>" for a in IN_ORDER]
        cells.append(f"<td><b>{mean:.2f}</b></td></tr>")
        body.append("".join(cells))
    return (
        "<!doctype html><html lang='it'><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Corse di ricerca</title>"
        f"<style>{_CSS}</style>"
        "<header><h1>Corse di ricerca</h1>"
        "<p class='quiet'>Input, output e punteggio di ogni pomeriggio. Generato da "
        "<code>python -m research.reader</code>; la definizione sono le cartelle in "
        "<code>research/runs/</code>. Niente qui riguarda una persona: le case sono inventate."
        "</p>"
        "<p><input type='search' id='find' placeholder='cerca titolo, casa, metodo, corsa…'> "
        f"<span class='quiet'><span id='count'>{len(rows)}</span> pomeriggi</span></p>"
        "</header><main>"
        f"<table class='runs'>{''.join(head)}{''.join(body)}</table>"
        + "".join(_one(row) for row in rows)
        + f"</main><script>{_JS}</script></html>"
    )


def write(runs: Path = RUNS, to: Path = OUT) -> Path:
    to.parent.mkdir(parents=True, exist_ok=True)
    to.write_text(page(runs), encoding="utf-8", newline="\n")
    return to


if __name__ == "__main__":
    where = write()
    print(f"{where}  ({where.stat().st_size // 1024} kB)")
    webbrowser.open(where.as_uri())
