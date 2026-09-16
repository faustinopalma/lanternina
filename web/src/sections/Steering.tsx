import { useState } from "react";
import { RefreshCw, RotateCcw, Save, Trash2 } from "lucide-react";

import { useApi } from "@/api/client";
import type { Steering as Guidance, SteeringEdit } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Label, Textarea } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

function Editor({ initial }: { initial: Guidance }) {
  const api = useApi();
  const { t } = useWords();
  const [kept, setKept] = useState(initial);
  const [instructions, setInstructions] = useState(initial.instructions);
  const [adaptive, setAdaptive] = useState(initial.adaptive);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState<MessageKey | null>(null);
  const [confirm, setConfirm] = useState<SteeringEdit["action"] | null>(null);
  const changed = instructions !== kept.instructions || adaptive !== kept.adaptive;

  function accept(value: Guidance) {
    setKept(value);
    setInstructions(value.instructions);
    setAdaptive(value.adaptive);
    setConfirm(null);
  }

  async function save(action: SteeringEdit["action"] = "save") {
    setBusy(true);
    setStatus(null);
    try {
      const change: SteeringEdit = { revision: kept.revision, action };
      if (action === "save") {
        if (instructions !== kept.instructions) change.instructions = instructions;
        if (adaptive !== kept.adaptive) change.adaptive = adaptive;
      }
      accept(await api.saveSteering(change));
      setStatus("steering.saved");
    } catch (error) {
      setStatus(error instanceof Error && error.message.includes("guidance_changed")
        ? "steering.conflict" : "steering.failed");
    } finally {
      setBusy(false);
    }
  }

  async function refresh(retry = false) {
    setBusy(true);
    setStatus(null);
    try {
      if (retry) await api.synthesizeSteering();
      const value = await api.steering();
      if (changed) {
        if (instructions === kept.instructions) setInstructions(value.instructions);
        if (adaptive === kept.adaptive) setAdaptive(value.adaptive);
        setKept(value);
        setStatus("steering.reviewChanges");
      } else {
        accept(value);
      }
    } catch {
      setStatus("steering.failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="max-w-[42rem] border-b border-edge pb-5">
      <form onSubmit={(event) => { event.preventDefault(); void save(); }}
        className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="steering-instructions">{t("steering.instructions")}</Label>
          <Quiet className="m-0">{t("steering.instructionsNote")}</Quiet>
          <Textarea id="steering-instructions" rows={8} value={instructions}
            maxLength={kept.instructionsLimit} disabled={busy}
            placeholder={t("steering.example")}
            onChange={(event) => setInstructions(event.target.value)} />
        </div>
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="steering-adaptive">{t("steering.adaptive")}</Label>
          <Quiet className="m-0">{t("steering.adaptiveNote")}</Quiet>
          <Textarea id="steering-adaptive" rows={5} value={adaptive}
            maxLength={kept.adaptiveLimit} disabled={busy}
            onChange={(event) => setAdaptive(event.target.value)} />
          <Quiet className="m-0">{t("steering.feedbackCount", { count: kept.feedbackCount })}</Quiet>
          {kept.pendingCount > 0 ? <div className="flex flex-wrap items-center gap-2">
            <Quiet>{t("steering.pending", { count: kept.pendingCount })}</Quiet>
            <Button type="button" size="small" disabled={busy || changed}
              onClick={() => void refresh(true)}><RefreshCw size={16} />{t("steering.retry")}</Button>
          </div> : null}
        </div>
        <div className="flex flex-wrap gap-2">
          <Button type="submit" variant="primary" disabled={busy || !changed}>
            <Save size={16} />{t("steering.save")}
          </Button>
          <Button type="button" disabled={busy} onClick={() => void refresh()}>
            <RefreshCw size={16} />{t("steering.refresh")}
          </Button>
        </div>
        <Quiet aria-live="polite" className="m-0">{status ? t(status) : ""}</Quiet>
        {status === "steering.reviewChanges" ? <details>
          <summary className="cursor-pointer">{t("steering.savedVersion")}</summary>
          <p className="mt-2 whitespace-pre-wrap break-words">{kept.instructions}</p>
          <p className="mt-2 whitespace-pre-wrap break-words">{kept.adaptive}</p>
        </details> : null}
      </form>
      <div className="mt-4 flex flex-wrap gap-2">
        <Button size="small" disabled={busy || changed}
          onClick={() => setConfirm("restore_instructions")}>
          <RotateCcw size={16} />{t("steering.restore")}
        </Button>
        <Button size="small" disabled={busy || changed}
          onClick={() => setConfirm("reset_adaptive")}>
          <Trash2 size={16} />{t("steering.reset")}
        </Button>
      </div>
      {confirm ? <div className="mt-3 border-l-2 border-edge pl-3" role="group"
        aria-label={t("steering.confirm")}>
        <p>{t(confirm === "reset_adaptive" ? "steering.resetNote" : "steering.restoreNote")}</p>
        <div className="mt-2 flex gap-2">
          <Button size="small" disabled={busy} onClick={() => void save(confirm)}>
            {t("steering.confirm")}
          </Button>
          <Button size="small" disabled={busy} onClick={() => setConfirm(null)}>
            {t("steering.cancel")}
          </Button>
        </div>
      </div> : null}
    </section>
  );
}

export function Steering() {
  const api = useApi();
  const { t } = useWords();
  const [state] = useLoad(() => api.steering());
  if (state.status === "loading") return <Quiet>{t("preferences.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("steering.failed")}</Quiet>;
  return <Editor initial={state.data} />;
}