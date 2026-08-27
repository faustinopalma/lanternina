import { useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import type { Preferences as Settings } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Label, Select, Textarea } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";
import { useUnsaved } from "@/lib/useUnsaved";

/* One entry per line, which is how the parent reads them back. The server flattens what is
 * left of a line break, so a pasted paragraph cannot become a second instruction. */
const asLines = (entries: string[]) => entries.join("\n");
const fromLines = (text: string) =>
  text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

interface Draft {
  interests: string;
  avoid: string;
  difficulty: string;
  variety: string;
  language: string;
  note: string;
}

/* The day the note stops being true, for the parent to read. Not a countdown: how many days
 * are left is not something anybody needs to watch. */
function until(at: number, locale: string) {
  return new Date(at * 1000).toLocaleDateString(locale, {
    day: "numeric",
    month: "long",
  });
}

function Form({ settings }: { settings: Settings }) {
  const { t, language } = useWords();
  const api = useApi();
  const [status, setStatus] = useState<MessageKey | null>(null);
  const [draft, setDraft] = useState<Draft>(() => ({
    interests: asLines(settings.interests),
    avoid: asLines(settings.avoid),
    difficulty: settings.difficulty,
    variety: settings.variety,
    language: settings.language,
    note: settings.note,
  }));

  const edit = (change: Partial<Draft>) => setDraft({ ...draft, ...change });
  const { changed, saved } = useUnsaved(draft);

  /* The words for each choice, written out rather than built from the value: a key that
   * only exists at runtime is a key no test can find missing. */
  const words: Record<string, string> = {
    gentle: t("preferences.gentle"),
    steady: t("preferences.steady"),
    stretch: t("preferences.stretch"),
    familiar: t("preferences.familiar"),
    balanced: t("preferences.balanced"),
    frequent: t("preferences.frequent"),
    it: t("preferences.italian"),
    en: t("preferences.english"),
  };

  /* The content language is saved here and read by the house. It is not the language of
   * this page: a parent switching their phone must not change what arrives on paper.
   * The body carries exactly the fields the settings are made of — there is no field for
   * a name, and the panel refuses a body that invents one. */
  async function save(event: FormEvent) {
    event.preventDefault();
    try {
      await api.savePreferences({
        interests: fromLines(draft.interests),
        avoid: fromLines(draft.avoid),
        difficulty: draft.difficulty,
        variety: draft.variety,
        language: draft.language,
        note: draft.note.trim(),
      });
      saved();
      setStatus("preferences.saved");
    } catch {
      setStatus("preferences.saveFailed");
    }
  }

  return (
    <>
      <form
        onSubmit={save}
        className="my-3.5 flex max-w-[42rem] flex-col gap-4 rounded-control border border-edge bg-paper p-4"
      >
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="pref-interests">{t("preferences.interests")}</Label>
          <Textarea
            id="pref-interests"
            rows={4}
            placeholder={t("preferences.oneEach")}
            value={draft.interests}
            onChange={(event) => edit({ interests: event.target.value })}
          />
        </div>
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="pref-avoid">{t("preferences.avoid")}</Label>
          <Textarea
            id="pref-avoid"
            rows={4}
            placeholder={t("preferences.oneEach")}
            value={draft.avoid}
            onChange={(event) => edit({ avoid: event.target.value })}
          />
        </div>

        <div className="flex flex-wrap items-center gap-x-4 gap-y-3">
          <span className="flex items-center gap-2">
            <Label htmlFor="pref-difficulty">{t("preferences.difficulty")}</Label>
            <Select
              id="pref-difficulty"
              value={draft.difficulty}
              onChange={(event) => edit({ difficulty: event.target.value })}
            >
              {settings.difficultyChoices.map((value) => (
                <option key={value} value={value}>
                  {words[value] ?? value}
                </option>
              ))}
            </Select>
          </span>
          <span className="flex items-center gap-2">
            <Label htmlFor="pref-variety">{t("preferences.variety")}</Label>
            <Select
              id="pref-variety"
              value={draft.variety}
              onChange={(event) => edit({ variety: event.target.value })}
            >
              {settings.varietyChoices.map((value) => (
                <option key={value} value={value}>
                  {words[value] ?? value}
                </option>
              ))}
            </Select>
          </span>
          <span className="flex items-center gap-2">
            <Label htmlFor="pref-language">{t("preferences.language")}</Label>
            <Select
              id="pref-language"
              value={draft.language}
              onChange={(event) => edit({ language: event.target.value })}
            >
              {settings.languageChoices.map((value) => (
                <option key={value} value={value}>
                  {words[value] ?? value}
                </option>
              ))}
            </Select>
          </span>
        </div>

        <Quiet className="m-0">{t("preferences.languageNote")}</Quiet>

        {/* The one place the parent writes rather than chooses, and the only setting that
         * expires. The label asks what is true of the house, not of the person: the grammar
         * of the question is most of what keeps the answer out of verdict territory. */}
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="pref-note">{t("preferences.note.label")}</Label>
          <Textarea
            id="pref-note"
            rows={3}
            placeholder={t("preferences.note.example")}
            value={draft.note}
            onChange={(event) => edit({ note: event.target.value })}
          />
          <Quiet className="m-0">
            {settings.noteUntil > 0 && draft.note.trim() === settings.note
              ? t("preferences.note.until", { day: until(settings.noteUntil, language) })
              : t("preferences.note.lasts", { days: String(settings.noteLastsDays) })}
          </Quiet>
        </div>

        {/* Grey means the house has what is on the screen. See `lib/useUnsaved.ts`. */}
        <span className="flex flex-wrap items-center gap-3">
          <Button type="submit" variant="primary" disabled={!changed} className="flex-none">
            {t("preferences.save")}
          </Button>
          <Quiet aria-live="polite" className="m-0">
            {status === null || (changed && status !== "preferences.saveFailed") ? "" : t(status)}
          </Quiet>
        </span>
      </form>
    </>
  );
}

export function Preferences() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.preferences());

  if (state.status === "loading") return <Quiet>{t("preferences.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("preferences.unreadable")}</Quiet>;
  return <Form settings={state.data} />;
}
