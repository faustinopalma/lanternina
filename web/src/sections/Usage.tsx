import { useState, type ReactNode } from "react";

import { useApi } from "@/api/client";
import type { UsageAnswer, UsageTotals } from "@/api/types";
import { Facts } from "@/components/Facts";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/** What the models consumed. Numbers about machines, never about a person, and never a target
 *  to reach.
 *
 *  Split by kind, because a picture, a wording and a reading consume different things: a
 *  single figure covering them would keep the name it had when it only counted pictures. */
export function Usage() {
  const { t, dateTime } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.usage());
  const [moved, setMoved] = useState<UsageAnswer | null>(null);
  // null while the parent has not touched the field. An empty string is a parent who
  // cleared it, and falling back to the saved figure there put the new number on the end
  // of the old one.
  const [wanted, setWanted] = useState<string | null>(null);
  const [said, setSaid] = useState("");

  if (state.status === "loading") return <Quiet>{t("usage.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("usage.unreadable")}</Quiet>;

  const answer = moved ?? state.data;
  const { usage, limit, reached, changedAt, changedBy, spent, maxLimit } = answer;
  const kinds = [
    { kind: "image", title: t("usage.kind.image") },
    { kind: "text", title: t("usage.kind.text") },
    { kind: "read", title: t("usage.kind.read") },
  ];

  const detail = (totals: UsageTotals) => [
    { label: t("usage.calls"), value: totals.calls },
    { label: t("usage.billed"), value: totals.billedCalls },
    { label: t("usage.inputTokens"), value: totals.inputTokens },
    { label: t("usage.cached"), value: totals.cachedInputTokens },
    { label: t("usage.outputTokens"), value: totals.outputTokens },
    { label: t("usage.reasoning"), value: totals.reasoningTokens },
  ];

  return (
    <div className="max-w-[34rem]">
      {kinds.map(({ kind, title }) => {
        const totals = usage.byKind[kind];
        return totals ? (
          <section key={kind} className="mt-5 first:mt-0">
            <Heading>{title}</Heading>
            <Facts rows={detail(totals)} />
          </section>
        ) : null;
      })}
      <section className="mt-5">
        <Heading>{t("usage.total")}</Heading>
        <Facts
          rows={[
            { label: t("usage.calls"), value: usage.total.calls },
            { label: t("usage.billed"), value: usage.total.billedCalls },
          ]}
        />
      </section>
      <section className="mt-5">
        <Heading>{t("usage.limit")}</Heading>
        {/* Shown as a state and not as a budget: it stops a runaway loop, and a limit
            somebody moved must never look like one that was always there. */}
        <Quiet className="mb-1.5">{t("usage.limit.note")}</Quiet>
        <Facts
          rows={[
            {
              label: t("usage.limit.moved"),
              value:
                changedAt > 0
                  ? t("usage.limit.movedOn", { when: dateTime(changedAt), who: changedBy })
                  : t("usage.limit.asConfigured"),
            },
            ...(reached
              ? [{ label: t("usage.limit.state"), value: t("usage.limit.gone") }]
              : []),
          ]}
        />
        <div className="mt-2.5 flex flex-wrap items-center gap-2.5">
          <Label htmlFor="usage-limit">{t("usage.limit.at")}</Label>
          <Input
            id="usage-limit"
            type="number"
            className="w-28"
            min={spent + 1}
            max={maxLimit}
            value={wanted ?? String(limit)}
            onChange={(event) => {
              setWanted(event.target.value);
              setSaid("");
            }}
          />
          <Button
            size="small"
            disabled={wanted === null || wanted === "" || Number(wanted) === limit}
            onClick={async () => {
              try {
                const now = await api.setLimit(Number(wanted));
                setMoved(now);
                setWanted(null);
                setSaid(t("usage.limit.saved", { calls: now.limit }));
              } catch {
                setSaid(t("usage.limit.refused", { spent, max: maxLimit }));
              }
            }}
          >
            {t("usage.limit.save")}
          </Button>
          <span className="text-quiet">{t("usage.limit.bounds", { max: maxLimit })}</span>
        </div>
        {said === "" ? null : (
          <p className="mt-2 mb-0 text-quiet" aria-live="polite">
            {said}
          </p>
        )}
      </section>
    </div>
  );
}

function Heading({ children }: { children: ReactNode }) {
  return <h3 className="text-[1rem] font-semibold tracking-tight">{children}</h3>;
}
