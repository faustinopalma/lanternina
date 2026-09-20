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
  { field: "topics", label: "steering.topics" },
  { field: "instructions", label: "steering.design" },
  { field: "conduct", label: "steering.conduct" },
  { field: "review", label: "steering.review" },
] as const;
const FIELDS = ["instructions", "conduct", "review", "topics", "adaptive"] as const;
type Texts = Pick<Guidance, typeof FIELDS[number]>;

function Editor({ initial, language }: { initial: Guidance; language: string }) {
  const api = useApi();
  const { t } = useWords();
  const [kept, setKept] = useState(initial);
  const [texts, setTexts] = useState<Texts>(initial);
  const [selected, setSelected] = useState(1);
  const active = PROMPTS[selected]!;
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
        <Quiet className="m-0">{t("steering.instructionsNote")}</Quiet>
        <div role="tablist" aria-label={t("steering.instructions")}
          className="grid grid-cols-2 sm:grid-cols-4 border-b border-edge">
          {PROMPTS.map((prompt, index) => <button key={prompt.field} type="button"
            role="tab" id={`prompt-tab-${prompt.field}`} aria-selected={selected === index}
            aria-controls="prompt-editor" tabIndex={selected === index ? 0 : -1}
            className={`min-w-0 border-b-2 px-2 py-2 text-sm ${selected === index
              ? "border-accent text-ink" : "border-transparent text-quiet"}`}
            onClick={() => { setSelected(index); setConfirm(null); }}
            onKeyDown={(event) => {
              let next = index;
              if (event.key === "ArrowRight") next = (index + 1) % PROMPTS.length;
              else if (event.key === "ArrowLeft") next = (index + PROMPTS.length - 1) % PROMPTS.length;
              else if (event.key === "Home") next = 0;
              else if (event.key === "End") next = PROMPTS.length - 1;
              else return;
              event.preventDefault();
              setSelected(next);
              setConfirm(null);
              document.getElementById(`prompt-tab-${PROMPTS[next]!.field}`)?.focus();
            }}>{t(prompt.label)}</button>)}
        </div>
        <div id="prompt-editor" role="tabpanel" aria-labelledby={`prompt-tab-${active.field}`}
          className="flex flex-col gap-2">
          <Label htmlFor="steering-instructions">{t(active.label)}</Label>
          <Textarea id="steering-instructions" rows={12} value={texts[active.field]}
            maxLength={kept.instructionsLimit} disabled={busy}
            onChange={(event) => setTexts({ ...texts, [active.field]: event.target.value })} />
          <Button type="button" size="small" disabled={busy || changed}
            className="self-start" onClick={() => setConfirm(`restore_${active.field}`)}>
            <RotateCcw size={16} />{t("steering.restore")}
          </Button>
        </div>
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