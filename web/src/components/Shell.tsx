import type { ReactNode } from "react";

import { Quiet } from "@/components/ui/card";
import { Select } from "@/components/ui/field";
import { LANGUAGES, LANGUAGE_NAMES, useWords, type MessageKey } from "@/i18n";

function LanguageChooser() {
  const { t, language, setLanguage } = useWords();
  return (
    <div className="flex items-baseline gap-1.5 text-[0.85rem] text-quiet">
      <label htmlFor="lang">{t("language.label")}</label>
      <Select
        id="lang"
        className="min-h-0 rounded border-edge bg-transparent px-1 py-0.5 text-[0.85rem]"
        value={language}
        onChange={(event) => setLanguage(event.target.value)}
      >
        {LANGUAGES.map((code) => (
          <option key={code} value={code}>
            {LANGUAGE_NAMES[code] ?? code}
          </option>
        ))}
      </Select>
    </div>
  );
}

/** The page around whichever view is showing: the name, the language of this page, and one
 *  line saying where the parent is. */
export function Shell({ lede, children }: { lede: MessageKey; children: ReactNode }) {
  const { t } = useWords();
  return (
    <main className="mx-auto max-w-[78rem] px-5 pt-10 pb-18 wide:px-7">
      <header className="mb-6">
        <div className="flex items-baseline justify-between gap-4">
          <h1 className="mb-1 text-[1.7rem] font-semibold tracking-tight">Lanternina</h1>
          <LanguageChooser />
        </div>
        <Quiet>{t(lede)}</Quiet>
      </header>
      {children}
    </main>
  );
}
