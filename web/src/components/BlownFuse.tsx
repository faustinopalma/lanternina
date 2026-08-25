/* The fuse, shown only when it has gone.
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

export function BlownFuse() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.usage());
  const [moved, setMoved] = useState<UsageAnswer | null>(null);
  const [wanted, setWanted] = useState("");
  const [failed, setFailed] = useState("");

  if (state.status !== "ready") return null;
  const fuse = moved ?? state.data;
  if (!fuse.reached && moved === null) return null;

  // Twice where it is now, which is the step that makes the difference obvious, kept
  // under the ceiling the panel is allowed to reach.
  const suggested = Math.min(fuse.cap * 2, fuse.maxCap);

  return (
    <div
      role="alert"
      className="mb-4 rounded-panel border border-alarm bg-alarm-soft p-[22px] text-ink"
    >
      <h2 className="mt-0 mb-2 text-[1.15rem] font-semibold tracking-tight text-alarm">
        {moved === null ? t("fuse.title") : t("fuse.done.title")}
      </h2>
      {moved === null ? (
        <>
          <p className="mt-0 mb-2 max-w-[38rem]">
            {t("fuse.what", { spent: fuse.spent, cap: fuse.cap })}
          </p>
          <p className="mt-0 mb-3.5 max-w-[38rem] text-quiet">{t("fuse.why")}</p>
          <div className="flex flex-wrap items-center gap-2.5">
            <Label htmlFor="fuse-calls">{t("fuse.raiseTo")}</Label>
            <Input
              id="fuse-calls"
              type="number"
              className="w-28"
              min={fuse.spent + 1}
              max={fuse.maxCap}
              value={wanted === "" ? String(suggested) : wanted}
              onChange={(event) => setWanted(event.target.value)}
            />
            <Button
              size="small"
              onClick={async () => {
                setFailed("");
                try {
                  setMoved(await api.raiseFuse(Number(wanted === "" ? suggested : wanted)));
                } catch {
                  setFailed(t("fuse.failed", { max: fuse.maxCap }));
                }
              }}
            >
              {t("fuse.raise")}
            </Button>
            <span className="text-quiet">{t("fuse.max", { max: fuse.maxCap })}</span>
          </div>
          {failed === "" ? null : (
            <p className="mt-2.5 mb-0 text-alarm" aria-live="polite">
              {failed}
            </p>
          )}
        </>
      ) : (
        <p className="mt-0 mb-0 max-w-[38rem]">{t("fuse.done", { cap: fuse.cap })}</p>
      )}
    </div>
  );
}
