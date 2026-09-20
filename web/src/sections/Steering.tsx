import { useState } from "react";
import { RefreshCw, RotateCcw, Save, Trash2 } from "lucide-react";

import { useApi } from "@/api/client";
import type { Steering as Guidance, SteeringEdit } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Label, Textarea } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

const PROMPTS = [
  { field: "topics", label: "preferences.interests" },
  { field: "avoid", label: "preferences.avoid" },
  { field: "instructions", label: "steering.design" },
  { field: "conduct", label: "steering.conduct" },
  { field: "review", label: "steering.review" },
] as const;
const FIELDS = ["instructions", "conduct", "review", "topics", "avoid", "adaptive"] as const;
type Texts = Pick<Guidance, typeof FIELDS[number]>;

function Editor({ initial, language }: { initial: Guidance; language: string }) {
  const api = useApi();
  const { t } = useWords();
  const [kept, setKept] = useState(initial);
  const [texts, setTexts] = useState<Texts>(initial);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState<MessageKey | null>(null);
  const [confirm, setConfirm] = useState<SteeringEdit["action"] | null>(null);
  const changed = FIELDS.some((field) => texts[field] !== kept[field]);

  function accept(value: Guidance) {
    setKept(value);
    setTexts(value);
    setConfirm(null);
  }

  async function save(action: SteeringEdit["action"] = "save") {
    setBusy(true);
    setStatus(null);
    try {
      const change: SteeringEdit = { revision: kept.revision, action };
      if (action === "save") {
        for (const field of FIELDS) {
          if (texts[field] !== kept[field]) change[field] = texts[field];
        }
      }
      accept(await api.saveSteering(change, language));
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
    setStatus(retry ? "steering.synthesizing" : null);
    try {
      if (retry) await api.synthesizeSteering(language);
      const value = await api.steering(language);
      if (changed) {
        setTexts((current) => {
          const refreshed = { ...current };
          for (const field of FIELDS) {
            if (current[field] === kept[field]) refreshed[field] = value[field];
          }
          return refreshed;
        });
        setKept(value);
        setStatus("steering.reviewChanges");
      } else {
        accept(value);
        setStatus(retry && value.pendingCount === 0 ? "steering.synthesized" : null);
      }
    } catch (error) {
      if (retry) {
        const message = error instanceof Error ? error.message : "";
        setStatus(message.includes("synthesis_limit") ? "steering.synthesisLimit"
          : message.includes("guidance_changed") ? "steering.conflict" : "steering.synthesisFailed");
      } else {
        setStatus("steering.failed");
      }
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="max-w-[42rem] border-b border-edge pb-5">
      <form onSubmit={(event) => { event.preventDefault(); void save(); }}
        className="flex flex-col gap-4">
        {PROMPTS.map((prompt) => <div key={prompt.field} className="flex flex-col gap-2">
          <div className="flex items-center justify-between gap-2">
            <Label htmlFor={`steering-${prompt.field}`}>{t(prompt.label)}</Label>
            <Button type="button" size="small" disabled={busy || changed}
              aria-label={`${t("steering.restore")}: ${t(prompt.label)}`}
              title={`${t("steering.restore")}: ${t(prompt.label)}`}
              onClick={() => setConfirm(`restore_${prompt.field}`)}>
              <RotateCcw size={16} />
            </Button>
          </div>
          <Textarea id={`steering-${prompt.field}`} rows={prompt.field === "avoid" ? 3 : 8}
            value={texts[prompt.field]} maxLength={kept.instructionsLimit} disabled={busy}
            onChange={(event) => setTexts({ ...texts, [prompt.field]: event.target.value })} />
          {confirm === `restore_${prompt.field}` ? <div role="group"
            aria-label={t("steering.confirm")} className="border-l-2 border-edge pl-3">
            <p>{t("steering.restoreNote")}</p>
            <div className="mt-2 flex gap-2">
              <Button type="button" size="small" disabled={busy}
                onClick={() => void save(confirm)}>{t("steering.confirm")}</Button>
              <Button type="button" size="small" disabled={busy}
                onClick={() => setConfirm(null)}>{t("steering.cancel")}</Button>
            </div>
          </div> : null}
        </div>)}
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="steering-adaptive">{t("steering.adaptive")}</Label>
          <Quiet className="m-0">{t("steering.adaptiveNote")}</Quiet>
          <Textarea id="steering-adaptive" rows={5} value={texts.adaptive}
            maxLength={kept.adaptiveLimit} disabled={busy}
            onChange={(event) => setTexts({ ...texts, adaptive: event.target.value })} />
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
          {FIELDS.map((field) => <div key={field} className="mt-2">
            <h3>{t(field === "adaptive" ? "steering.adaptive"
              : PROMPTS.find((prompt) => prompt.field === field)!.label)}</h3>
            <p className="whitespace-pre-wrap break-words">{kept[field]}</p>
          </div>)}
        </details> : null}
      </form>
      <div className="mt-4 flex flex-wrap gap-2">
        <Button size="small" disabled={busy || changed}
          onClick={() => setConfirm("reset_adaptive")}>
          <Trash2 size={16} />{t("steering.reset")}
        </Button>
      </div>
      {confirm === "reset_adaptive" ? <div className="mt-3 border-l-2 border-edge pl-3" role="group"
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

function LanguageSteering({ language }: { language: string }) {
  const api = useApi();
  const { t } = useWords();
  const [state] = useLoad(() => api.steering(language));
  if (state.status === "loading") return <Quiet>{t("preferences.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("steering.failed")}</Quiet>;
  return <Editor initial={state.data} language={language} />;
}

export function Steering() {
  const { language } = useWords();
  return <LanguageSteering key={language} language={language} />;
}