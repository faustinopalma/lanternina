import { useEffect, useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

export function Rhythm() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.rhythm());
  const [quietFrom, setQuietFrom] = useState("");
  const [quietUntil, setQuietUntil] = useState("");
  const [cadence, setCadence] = useState("");
  const [status, setStatus] = useState<MessageKey | null>(null);

  useEffect(() => {
    if (state.status !== "ready") return;
    setQuietFrom(state.data.quietFrom);
    setQuietUntil(state.data.quietUntil);
    setCadence(String(state.data.cadenceMinutes));
    setStatus(state.data.quietFrom === state.data.quietUntil ? "rhythm.quietOff" : null);
  }, [state]);

  if (state.status === "loading") return <Quiet>{t("rhythm.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("rhythm.unreadable")}</Quiet>;

  /* Saving persists a choice and returns. The house reads it on its next run and decides
   * for itself, so nothing here reaches into the room. */
  async function save(event: FormEvent) {
    event.preventDefault();
    try {
      await api.saveRhythm({ quietFrom, quietUntil, cadenceMinutes: Number(cadence) });
      setStatus("rhythm.saved");
    } catch {
      setStatus("rhythm.saveFailed");
    }
  }

  return (
    <>
      <form
        onSubmit={save}
        className="my-3.5 flex max-w-[42rem] flex-wrap items-center gap-x-4 gap-y-3 rounded-[--radius-control] border border-edge bg-paper p-4"
      >
        <span className="flex items-center gap-2">
          <Label htmlFor="quiet-from">{t("rhythm.quietFrom")}</Label>
          <Input
            id="quiet-from"
            type="time"
            required
            className="w-34"
            value={quietFrom}
            onChange={(event) => setQuietFrom(event.target.value)}
          />
        </span>
        <span className="flex items-center gap-2">
          <Label htmlFor="quiet-until">{t("rhythm.quietUntil")}</Label>
          <Input
            id="quiet-until"
            type="time"
            required
            className="w-34"
            value={quietUntil}
            onChange={(event) => setQuietUntil(event.target.value)}
          />
        </span>
        <span className="flex items-center gap-2">
          <Label htmlFor="cadence">{t("rhythm.cadence")}</Label>
          <Input
            id="cadence"
            type="number"
            required
            step={1}
            min={state.data.minCadenceMinutes}
            max={state.data.maxCadenceMinutes}
            className="w-26"
            value={cadence}
            onChange={(event) => setCadence(event.target.value)}
          />
          <span className="text-quiet">{t("rhythm.minutes")}</span>
        </span>
        <Button type="submit" variant="primary" className="ml-auto flex-none">
          {t("rhythm.save")}
        </Button>
      </form>
      <Quiet>{t("rhythm.wakeNote")}</Quiet>
      <Quiet aria-live="polite">{status === null ? "" : t(status)}</Quiet>
    </>
  );
}
