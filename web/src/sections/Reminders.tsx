import { useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import { ApiError, type Reminder } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

function Row({
  reminder,
  textLimit,
  onRemoved,
  onFailed,
}: {
  reminder: Reminder;
  textLimit: number;
  onRemoved: () => void;
  onFailed: (problem: MessageKey) => void;
}) {
  const { t } = useWords();
  const api = useApi();
  const [text, setText] = useState(reminder.text);
  const [saved, setSaved] = useState(reminder.text);
  const [busy, setBusy] = useState(false);
  return (
    <div className="flex flex-col gap-1.5 border-b border-edge py-3.5 last:border-b-0">
      <div className="flex flex-wrap items-center gap-2.5">
        <Input
          className="min-w-0 flex-auto"
          maxLength={textLimit}
          autoComplete="off"
          aria-label={t("reminders.textAria")}
          value={text}
          onChange={(event) => setText(event.target.value)}
          onBlur={async () => {
            /* The parent's words stay the only copy: correcting a sentence the house
             * could not place is an edit here, not a field somewhere else. */
            const wanted = text.trim();
            if (wanted === saved || !wanted) return;
            try {
              const changed = await api.rewriteReminder(reminder.id, wanted);
              setSaved(changed.text);
              setText(changed.text);
            } catch (error) {
              onFailed(
                error instanceof ApiError && error.rejected
                  ? "reminders.badText"
                  : "reminders.saveFailed",
              );
            }
          }}
        />
        <Button
          size="small"
          className="flex-none"
          disabled={busy}
          title={t("reminders.removeTitle", { text: saved })}
          onClick={async () => {
            setBusy(true);
            try {
              await api.removeReminder(reminder.id);
              onRemoved();
            } catch {
              setBusy(false);
              onFailed("reminders.removeFailed");
            }
          }}
        >
          {t("reminders.remove")}
        </Button>
      </div>
      <Placed reminder={reminder} />
      <Wordings reminder={reminder} />
    </div>
  );
}

/* The ways the house will say it. Shown because what the parent approves is the reminder
 * and not each sentence, so the least this owes them is that the sentences are readable
 * here rather than only on the display. There is nothing to press: approving them one by
 * one is the thing nobody will do four times a day. */
function Wordings({ reminder }: { reminder: Reminder }) {
  const { t } = useWords();
  if (!reminder.at || reminder.words.length === 0) return null;
  return (
    <Quiet>
      {t("reminders.words")} {reminder.words.map((one) => `«${one}»`).join(" ")}
    </Quiet>
  );
}

/* What the house made of the sentence, in one line. Deliberately not a form: the parent's
 * words are the only copy, so a wrong hour is corrected by changing the sentence above. */
function Placed({ reminder }: { reminder: Reminder }) {
  const { t, weekday } = useWords();
  if (!reminder.read) return <Quiet>{t("reminders.notRead")}</Quiet>;
  if (reminder.at) {
    const when =
      reminder.days.length === 0
        ? t("reminders.everyDay")
        : reminder.days.map(weekday).join(", ");
    return <Quiet>{t("reminders.due", { at: reminder.at, days: when })}</Quiet>;
  }
  /* A sentence the house could not place. The question is the model's, in the language the
   * parent wrote in; when there is none, the panel says the plain thing in its own words. */
  return (
    <Quiet>
      {reminder.question ? t("reminders.asks", { question: reminder.question }) : t("reminders.noHour")}
    </Quiet>
  );
}

export function Reminders() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.reminders());
  const [added, setAdded] = useState<Reminder[]>([]);
  const [removed, setRemoved] = useState<string[]>([]);
  const [text, setText] = useState("");
  const [problem, setProblem] = useState<MessageKey | null>(null);

  async function add(event: FormEvent) {
    event.preventDefault();
    const wanted = text.trim();
    if (!wanted) return;
    setProblem(null);
    try {
      const reminder = await api.addReminder(wanted);
      setAdded((seen) => [...seen, reminder]);
      setText("");
    } catch (error) {
      setProblem(
        error instanceof ApiError && error.rejected ? "reminders.badText" : "reminders.addFailed",
      );
    }
  }

  if (state.status === "loading") return <Quiet>{t("reminders.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("reminders.unreadable")}</Quiet>;

  const { textLimit } = state.data;
  const showing = [...state.data.reminders, ...added].filter(
    (reminder) => !removed.includes(reminder.id),
  );

  return (
    <>
      <Quiet>{t("reminders.laterNote")}</Quiet>
      <form
        onSubmit={add}
        className="my-3.5 flex max-w-[42rem] gap-2.5 rounded-control border border-edge bg-paper p-4"
      >
        <Input
          className="min-w-0 flex-auto"
          maxLength={textLimit}
          autoComplete="off"
          aria-label={t("reminders.aria")}
          placeholder={t("reminders.placeholder")}
          value={text}
          onChange={(event) => setText(event.target.value)}
        />
        <Button type="submit" variant="primary" className="flex-none">
          {t("reminders.add")}
        </Button>
      </form>
      {problem === null ? <></> : <Quiet>{t(problem)}</Quiet>}
      <div aria-live="polite">
        {showing.length === 0 ? (
          <Quiet>{t("reminders.empty")}</Quiet>
        ) : (
          showing.map((reminder) => (
            <Row
              key={reminder.id}
              reminder={reminder}
              textLimit={textLimit}
              onRemoved={() => setRemoved((seen) => [...seen, reminder.id])}
              onFailed={setProblem}
            />
          ))
        )}
      </div>
    </>
  );
}
