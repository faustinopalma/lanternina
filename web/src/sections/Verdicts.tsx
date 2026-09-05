import { useApi } from "@/api/client";
import type { Finding, Judged } from "@/api/types";
import { Facts } from "@/components/Facts";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* What a reader made of each afternoon this house was offered.
 *
 * **Temporary, for the weeks the prompts are being changed.** `panel/routes/verdicts.py`
 * says what has to be true before it goes, and why showing this beside afternoons a parent
 * has not decided on yet is a property of a development instrument rather than a decision.
 *
 * The reader was shown the moments and not the script, so `question` and `answer` are what
 * somebody who read only what reaches the person worked out. Comparing that with what the
 * afternoon was meant to ask is the point of the page, and it is left to whoever is reading
 * — automating it would be another model call and another thing that can be wrong.
 */

/** Counts across every afternoon under one version of the prompt. */
function Tally({ rows }: { rows: Judged[] }) {
  const { t } = useWords();
  const named = new Map<string, number>();
  for (const row of rows) {
    for (const finding of row.findings) {
      named.set(finding.name, (named.get(finding.name) ?? 0) + 1);
    }
  }
  const silent = rows.filter((row) => row.canBeWrong && !row.question).length;

  return (
    <Facts
      className="mt-2"
      rows={[
        { label: t("verdicts.judged"), value: rows.length },
        { label: t("verdicts.open"), value: rows.filter((row) => !row.canBeWrong).length },
        { label: t("verdicts.silent"), value: silent },
        ...[...named.entries()]
          .sort((a, b) => b[1] - a[1])
          .map(([name, n]) => ({ label: name, value: `${n}/${rows.length}` })),
      ]}
    />
  );
}

function Said({ finding }: { finding: Finding }) {
  return (
    <li className="mt-2 border-l-2 border-edge pl-3">
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">
        {finding.name}
        {finding.where ? ` · ${finding.where}` : ""}
      </p>
      <p className="mt-1 mb-0 text-[0.9rem]">{finding.says}</p>
    </li>
  );
}

function Card({ row }: { row: Judged }) {
  const { t, dateTime } = useWords();

  return (
    <article className="mt-3.5 max-w-[42rem] rounded-control border border-edge bg-paper p-[18px] pb-4">
      <h3 className="text-[1.05rem] font-semibold">{row.title || row.experienceId}</h3>
      <Quiet className="mb-2">
        {dateTime(row.createdAt)} · {row.prompt || "—"} ·{" "}
        {row.canBeWrong ? t("verdicts.canBeWrong") : t("verdicts.nothingToGetWrong")}
      </Quiet>
      {row.degraded ? <Quiet className="mb-2">{t("verdicts.degraded")}</Quiet> : null}
      <Facts
        className="mt-2"
        rows={[
          { label: t("verdicts.question"), value: row.question || t("verdicts.couldNotSay") },
          { label: t("verdicts.answer"), value: row.answer || "—" },
        ]}
      />
      {row.findings.length === 0 ? (
        <Quiet className="mt-3">{t("verdicts.nothing")}</Quiet>
      ) : (
        <ul className="mt-3 list-none p-0">
          {row.findings.map((finding, at) => (
            <Said key={`${finding.name}-${at}`} finding={finding} />
          ))}
        </ul>
      )}
    </article>
  );
}

export function Verdicts({ alreadyOnTheTrail = [] }: { alreadyOnTheTrail?: string[] }) {
  const api = useApi();
  const { t } = useWords();
  const [state] = useLoad(() => api.verdicts());

  if (state.status === "loading") return <Quiet>{t("verdicts.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("verdicts.unreadable")}</Quiet>;
  /* An afternoon that ran carries its own reading inside its trail, filed as `judged` when
     the house said it had begun. Showing it here as well would put the same afternoon on
     the page twice under two headings, which is what merging the two sections revealed. */
  const rows = state.data.filter((row) => !alreadyOnTheTrail.includes(row.experienceId));
  if (rows.length === 0) return <Quiet>{t("verdicts.empty")}</Quiet>;

  return (
    <div>
      <Tally rows={rows} />
      {rows.map((row) => (
        <Card key={row.experienceId} row={row} />
      ))}
    </div>
  );
}
