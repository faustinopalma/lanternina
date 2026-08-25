/* The limit, shown only when the house has reached it.
 *
 * It sits above every section rather than inside the usage page, because the parent who
 * needs it is not looking for it: they came to find out why nothing is happening. Until
 * this existed the only sign was that the house went quiet.
 */
import { useState } from "react";

import { useApi } from "@/api/client";
import type { UsageAnswer } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Input, Label } from "@/components/ui/field";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

export function LimitReached() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.usage());
  const [moved, setMoved] = useState<UsageAnswer | null>(null);
  // null while the parent has not touched the field, so clearing it leaves it clear.
  const [wanted, setWanted] = useState<string | null>(null);
  const [failed, setFailed] = useState("");

  if (state.status !== "ready") return null;
  const now = moved ?? state.data;
  if (!now.reached && moved === null) return null;

  // Twice where it is, which is the step that makes the difference obvious, kept under
  // the ceiling the panel is allowed to reach.
  const suggested = Math.min(now.limit * 2, now.maxLimit);

  return (
    <div
      role="alert"
      className="mb-4 rounded-panel border border-alarm bg-alarm-soft p-[22px] text-ink"
    >
      <h2 className="mt-0 mb-2 text-[1.15rem] font-semibold tracking-tight text-alarm">
        {moved === null ? t("limit.title") : t("limit.done.title")}
      </h2>
      {moved === null ? (
        <>
          <p className="mt-0 mb-2 max-w-[38rem]">
            {t("limit.what", { spent: now.spent, limit: now.limit })}
          </p>
          <p className="mt-0 mb-3.5 max-w-[38rem] text-quiet">{t("limit.why")}</p>
          <div className="flex flex-wrap items-center gap-2.5">
            <Label htmlFor="limit-calls">{t("limit.raiseTo")}</Label>
            <Input
              id="limit-calls"
              type="number"
              className="w-28"
              min={now.spent + 1}
              max={now.maxLimit}
              value={wanted ?? String(suggested)}
              onChange={(event) => setWanted(event.target.value)}
            />
            <Button
              size="small"
              onClick={async () => {
                setFailed("");
                try {
                  setMoved(await api.setLimit(Number(wanted ?? suggested)));
                } catch {
                  setFailed(t("limit.failed", { max: now.maxLimit }));
                }
              }}
            >
              {t("limit.raise")}
            </Button>
            <span className="text-quiet">{t("limit.max", { max: now.maxLimit })}</span>
          </div>
          {failed === "" ? null : (
            <p className="mt-2.5 mb-0 text-alarm" aria-live="polite">
              {failed}
            </p>
          )}
        </>
      ) : (
        <p className="mt-0 mb-0 max-w-[38rem]">{t("limit.done", { limit: now.limit })}</p>
      )}
    </div>
  );
}
