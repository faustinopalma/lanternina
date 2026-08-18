import { render, type RenderResult } from "@testing-library/react";
import type { ReactNode } from "react";

import type { Api } from "@/api/types";
import { Dashboard } from "@/components/Dashboard";
import { Shell } from "@/components/Shell";
import { LanguageProvider } from "@/i18n";

/** The panel as a parent meets it, in Italian, with a fake API behind it. The language is
 *  pinned so a test never depends on the machine it runs on. */
export function renderPanel(api: Api, children?: ReactNode): RenderResult {
  window.localStorage.setItem("lanternina.language", "it");
  return render(
    <LanguageProvider>
      <Shell lede={null}>
        {children ?? (
          <Dashboard api={api} username="genitore@example.invalid" onSignOut={() => undefined} />
        )}
      </Shell>
    </LanguageProvider>,
  );
}
