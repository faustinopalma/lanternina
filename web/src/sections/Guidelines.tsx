import { useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import { ApiError, type Guidelines as Written } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* Limits a parent may want and would not think to write. They fill the field and nothing
 * else: pressing one is reading it, and adding it is still a second press. A house that
 * presses none has the fixed bounds and nothing narrower, which is the default.
 *
 * They sat unlabelled under the form until 28 August 2026, three sentences in boxes that
 * looked exactly like the controls beside them, and the parent read them as three things
 * already in force. What they are has to be written down; the styling cannot say it.
 *
 * They were also the wrong three. "The scissors are in the first drawer" is a fact about
 * the house and not a limit on anything, and it was there because this page used to hold
 * permissions. One each for where, with what, and when. */
const SUGGESTED: MessageKey[] = [
  "guidelines.suggestOutside",
  "guidelines.suggestBlades",
  "guidelines.suggestNoise",
];

/* What we wrote, shown beside what the parent writes. There is no control here on purpose:
 * these hold in every household, and a switch would be offering to remove the reason this
 * system exists.
 *
 * The panel says them in the parent's language and the API says them in the model's, so
 * these are two copies of one rule and they can drift. What is kept honest is the count —
 * a bound added to the prompt and not to the panel shows up as the API's own English line
 * rather than disappearing, which is the failure worth seeing. */
const OURS: MessageKey[] = [
  "guidelines.ours1",
  "guidelines.ours2",
  "guidelines.ours3",
  "guidelines.ours4",
  "guidelines.ours5",
];

function Ours({ fixed }: { fixed: string[] }) {
  const { t } = useWords();
  return (
    <div className="mt-5 max-w-[42rem] rounded-control border border-edge bg-paper p-4">
      <Quiet>{t("guidelines.oursNote")}</Quiet>
      <ul className="mt-2 list-disc pl-5">
        {fixed.map((line, index) => (
          <li key={line} className="text-quiet">
            {OURS[index] === undefined ? line : t(OURS[index])}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function Guidelines() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.guidelines());
  const [written, setWritten] = useState<string[] | null>(null);
  const [line, setLine] = useState("");
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState<MessageKey | null>(null);

  if (state.status === "loading") return <Quiet>{t("guidelines.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("guidelines.unreadable")}</Quiet>;

  const kept: Written = state.data;
  const lines = written ?? kept.lines;

  async function save(wanted: string[], onDone: () => void) {
    setBusy(true);
    setProblem(null);
    try {
      const back = await api.saveGuidelines(wanted);
      setWritten(back.lines);
      onDone();
    } catch (error) {
      setProblem(
        error instanceof ApiError && error.rejected
          ? "guidelines.badLine"
          : "guidelines.saveFailed",
      );
    } finally {
      setBusy(false);
    }
  }

  async function add(event: FormEvent) {
    event.preventDefault();
    const wanted = line.trim();
    if (!wanted) return;
    await save([...lines, wanted], () => setLine(""));
  }

  return (
    <>
      <Quiet>{t("guidelines.laterNote")}</Quiet>
      <form
        onSubmit={add}
        className="my-3.5 flex max-w-[42rem] gap-2.5 rounded-control border border-edge bg-paper p-4"
      >
        <Input
          className="min-w-0 flex-auto"
          maxLength={kept.lineLimit}
          autoComplete="off"
          aria-label={t("guidelines.aria")}
          placeholder={t("guidelines.placeholder")}
          value={line}
          onChange={(event) => setLine(event.target.value)}
        />
        <Button
          type="submit"
          variant="primary"
          className="flex-none"
          disabled={busy || lines.length >= kept.maxLines}
        >
          {t("guidelines.add")}
        </Button>
      </form>

      <div className="mb-3.5 max-w-[42rem]">
        <Quiet className="m-0">{t("guidelines.suggestNote")}</Quiet>
        <div className="mt-2 flex flex-wrap gap-2">
          {SUGGESTED.map((key) => (
            <Button
              key={key}
              size="small"
              title={t("guidelines.suggestTitle", { line: t(key) })}
              onClick={() => setLine(t(key))}
            >
              {t(key)}
            </Button>
          ))}
        </div>
      </div>

      {problem === null ? <></> : <Quiet>{t(problem)}</Quiet>}

      <div aria-live="polite">
        {lines.length === 0 ? (
          <Quiet>{t("guidelines.empty")}</Quiet>
        ) : (
          lines.map((one) => (
            <div
              key={one}
              className="mt-2 flex max-w-[42rem] items-center justify-between gap-3 rounded-control border border-edge bg-paper py-2 pr-2 pl-3.5"
            >
              <span>{one}</span>
              <Button
                size="small"
                disabled={busy}
                title={t("guidelines.removeTitle", { line: one })}
                onClick={() =>
                  void save(
                    lines.filter((kept_line) => kept_line !== one),
                    () => undefined,
                  )
                }
              >
                {t("guidelines.remove")}
              </Button>
            </div>
          ))
        )}
      </div>

      <Ours fixed={kept.fixed} />
    </>
  );
}
