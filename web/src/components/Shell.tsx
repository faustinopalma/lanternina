import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Select } from "@/components/ui/field";
import { LANGUAGES, LANGUAGE_NAMES, useWords, type MessageKey } from "@/i18n";

export interface SignedIn {
  username: string;
  onSignOut: () => void;
}

function LanguageChooser() {
  const { t, language, setLanguage } = useWords();
  return (
    <span className="flex items-center gap-1.5">
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
    </span>
  );
}

/** The page around whichever view is showing.
 *
 *  Who is signed in and how to leave sit together at the top right, where a reader looks
 *  for them, and they are the same in every view — so no card has to carry a way out.
 */
export function Shell({
  lede,
  account,
  children,
}: {
  lede: MessageKey | null;
  account: SignedIn | null;
  children: ReactNode;
}) {
  const { t } = useWords();
  return (
    <main className="mx-auto max-w-[78rem] px-5 pt-10 pb-18 wide:px-7">
      <header className="mb-6">
        <div className="flex flex-wrap items-center justify-between gap-x-5 gap-y-3">
          <h1 className="text-[1.7rem] font-semibold tracking-tight">Lanternina</h1>
          <div className="flex grow flex-wrap items-center justify-end gap-x-4 gap-y-2 text-[0.85rem] text-quiet">
            <LanguageChooser />
            {account === null ? null : (
              <>
                {account.username ? (
                  // The address itself, not a sentence about it. Truncated because it is an
                  // identifier, and the whole of it is one hover away.
                  <span
                    className="max-w-[15rem] truncate"
                    title={account.username}
                    aria-label={t("account.aria")}
                  >
                    {account.username}
                  </span>
                ) : null}
                <Button size="small" onClick={account.onSignOut}>
                  {t("signout")}
                </Button>
              </>
            )}
          </div>
        </div>
        {lede === null ? null : <Quiet className="mt-1">{t(lede)}</Quiet>}
      </header>
      {children}
    </main>
  );
}
