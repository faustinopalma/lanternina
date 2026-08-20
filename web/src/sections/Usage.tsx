import type { ReactNode } from "react";

import { useApi } from "@/api/client";
import type { UsageTotals } from "@/api/types";
import { Facts } from "@/components/Facts";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/** What the models consumed. Numbers about machines, never about a person, and never a target
 *  to reach.
 *
 *  Split by kind, because a picture, a wording and a reading consume different things: a
 *  single figure covering them would keep the name it had when it only counted pictures. */
export function Usage() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.usage());

  if (state.status === "loading") return <Quiet>{t("usage.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("usage.unreadable")}</Quiet>;

  const { usage, cap } = state.data;
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
            { label: t("usage.cap"), value: cap > 0 ? cap : t("usage.noCap") },
          ]}
        />
      </section>
    </div>
  );
}

function Heading({ children }: { children: ReactNode }) {
  return <h3 className="text-[1rem] font-semibold tracking-tight">{children}</h3>;
}
