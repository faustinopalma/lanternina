import { useApi } from "@/api/client";
import type { ResearchRun } from "@/api/types";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* Every research run there has been, oldest on the left.
 *
 * **Temporary, beside the readings and for the same reason.** `research/` is an apparatus
 * and not part of the product: it devises afternoons with the real prompts, plays them
 * against a model standing in for an adolescent, and gives each of eight axes a number from
 * 1 to 5, where 3 is "does the job". `research/README.md` says what each axis catches and
 * what the number does not mean — the shortest version is that a model standing in for an
 * adolescent is a genre and not a person, so a high figure means an afternoon survived a
 * plausible reading.
 *
 * **The numbers here are about afternoons and never about anybody**, and the vocabulary this
 * file uses says so: an axis, and a mean over afternoons. `tests/test_boundaries.py` forbids
 * the vocabulary of assessment anywhere in this panel, without exceptions, because an
 * exception is the thing that would be easy to add and hard to notice.
 *
 * One axis per row and one run per column, because what is being read is a difference along
 * a row, not the value in a cell. The denominator is in the header and not in a footnote:
 * a mean over 24 afternoons and a mean over 4 are not the same number.
 */

/** Every axis any run gave a number to, so a run that gained one does not silently drop it. */
function axesOf(runs: ResearchRun[]): string[] {
  const seen = new Set<string>();
  for (const run of runs) for (const axis of Object.keys(run.axes)) seen.add(axis);
  return [...seen].sort();
}

/** The highest figure on this row, so the eye can find where a change landed. */
function highest(runs: ResearchRun[], axis: string): number {
  return Math.max(...runs.map((run) => run.axes[axis] ?? 0));
}

export function Research() {
  const api = useApi();
  const { t } = useWords();
  const [state] = useLoad(() => api.research());

  if (state.status === "loading") return <Quiet>{t("research.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("research.unreadable")}</Quiet>;
  if (state.data.length === 0) return <Quiet>{t("research.empty")}</Quiet>;

  const runs = state.data;
  const axes = axesOf(runs);

  return (
    <div className="max-w-full overflow-x-auto">
      <table className="w-full border-collapse text-[0.92rem]">
        <thead>
          <tr>
            <th className="border-b border-edge py-2 pr-4 text-left font-normal text-quiet">
              {t("research.axis")}
            </th>
            {runs.map((run) => (
              <th key={run.run} className="border-b border-edge px-3 py-2 text-right align-bottom">
                <span className="block font-semibold">{run.label || run.at}</span>
                <span className="block font-normal text-quiet">{run.prompt || "—"}</span>
                <span className="block font-normal text-quiet">
                  {t("research.afternoons", { n: run.afternoons })}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {axes.map((axis) => {
            const top = highest(runs, axis);
            return (
              <tr key={axis}>
                <td className="border-b border-edge py-2 pr-4 [overflow-wrap:anywhere]">{axis}</td>
                {runs.map((run) => {
                  const figure = run.axes[axis];
                  return (
                    <td
                      key={run.run}
                      className={
                        "border-b border-edge px-3 py-2 text-right tabular-nums" +
                        (figure !== undefined && figure === top ? " font-semibold" : "")
                      }
                    >
                      {figure === undefined ? "—" : figure.toFixed(2)}
                    </td>
                  );
                })}
              </tr>
            );
          })}
          <tr>
            <td className="border-b border-edge py-2 pr-4">{t("research.refused")}</td>
            {runs.map((run) => (
              <td
                key={run.run}
                className="border-b border-edge px-3 py-2 text-right tabular-nums"
              >
                {run.refused}
              </td>
            ))}
          </tr>
          <tr>
            <td className="py-2 pr-4">{t("research.closed")}</td>
            {runs.map((run) => (
              <td key={run.run} className="px-3 py-2 text-right tabular-nums">
                {run.endings.closed ?? 0}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
      <Quiet className="mt-4">{t("research.means")}</Quiet>
    </div>
  );
}
