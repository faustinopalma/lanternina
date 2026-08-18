import { useApi } from "@/api/client";
import { Facts } from "@/components/Facts";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/** What the models consumed. Numbers about machines, never about her, and never a target
 *  to reach. */
export function Usage() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.usage());

  if (state.status === "loading") return <Quiet>{t("usage.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("usage.unreadable")}</Quiet>;

  const { usage, cap } = state.data;

  return (
    <Facts
      className="max-w-[34rem]"
      rows={[
        { label: t("usage.calls"), value: usage.calls },
        { label: t("usage.billed"), value: usage.billedCalls },
        { label: t("usage.inputTokens"), value: usage.inputTokens },
        { label: t("usage.cached"), value: usage.cachedInputTokens },
        { label: t("usage.outputTokens"), value: usage.outputTokens },
        { label: t("usage.reasoning"), value: usage.reasoningTokens },
        { label: t("usage.cap"), value: cap > 0 ? cap : t("usage.noCap") },
      ]}
    />
  );
}
