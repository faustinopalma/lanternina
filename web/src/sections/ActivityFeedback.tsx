import { useId, useState } from "react";

import type { ActivityFeedback as Feedback } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Label, Textarea } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";

const REASONS: [string, MessageKey][] = [
  ["too_difficult", "feedback.tooDifficult"], ["too_easy", "feedback.tooEasy"],
  ["too_abstract", "feedback.tooAbstract"], ["too_closed", "feedback.tooClosed"],
  ["too_open", "feedback.tooOpen"], ["unclear", "feedback.unclear"],
  ["too_much_reading", "feedback.reading"], ["too_much_writing", "feedback.writing"],
  ["too_much_help", "feedback.help"], ["not_interesting", "feedback.interest"],
];
const OPPOSITE: Record<string, string> = {
  too_difficult: "too_easy", too_easy: "too_difficult",
  too_closed: "too_open", too_open: "too_closed",
};

export function ActivityFeedback({ busy, onSubmit, onCancel }: {
  busy: boolean; onSubmit: (feedback: Feedback) => void; onCancel: () => void;
}) {
  const { t } = useWords();
  const identifier = useId();
  const [reasons, setReasons] = useState<string[]>([]);
  const [note, setNote] = useState("");
  function toggle(reason: string, checked: boolean) {
    setReasons((current) => checked
      ? [...current.filter((value) => value !== OPPOSITE[reason]), reason]
      : current.filter((value) => value !== reason));
  }
  return <form className="mt-4 w-full border-t border-edge pt-3"
    onSubmit={(event) => { event.preventDefault(); onSubmit({ reasons, note: note.trim() }); }}>
    <fieldset disabled={busy}>
      <legend className="font-medium">{t("feedback.title")}</legend>
      <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
        {REASONS.map(([reason, label]) => <label key={reason} className="flex items-start gap-2">
          <input type="checkbox" className="mt-1" checked={reasons.includes(reason)}
            onChange={(event) => toggle(reason, event.target.checked)} />
          <span>{t(label)}</span>
        </label>)}
      </div>
      <div className="mt-3 flex flex-col gap-1.5">
        <Label htmlFor={identifier}>{t("feedback.comment")}</Label>
        <Textarea id={identifier} value={note} rows={3} maxLength={2000}
          placeholder={t("feedback.example")} onChange={(event) => setNote(event.target.value)} />
      </div>
      <Quiet className="mt-2">{t("feedback.note")}</Quiet>
      <div className="mt-3 flex flex-wrap gap-2">
        <Button type="submit" variant="primary" size="small">{t("feedback.submit")}</Button>
        <Button type="button" size="small" onClick={onCancel}>{t("steering.cancel")}</Button>
      </div>
    </fieldset>
  </form>;
}