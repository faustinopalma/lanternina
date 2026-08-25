import { render, type RenderResult } from "@testing-library/react";
import type { ReactNode } from "react";

import { ApiProvider } from "@/api/client";
import type { Api } from "@/api/types";
import { Dashboard } from "@/components/Dashboard";
import { Shell } from "@/components/Shell";
import { LanguageProvider } from "@/i18n";

/** The panel as a parent meets it, in Italian, with a fake API behind it. The language is
 *  pinned so a test never depends on the machine it runs on.
 *
 *  Given children, one section on its own: the provider is here rather than only inside
 *  the dashboard, so a section that shares a page with another can still be tested apart
 *  from it. */
export function renderPanel(api: Api, children?: ReactNode): RenderResult {
  window.localStorage.setItem("lanternina.language", "it");
  return render(
    <LanguageProvider>
      <Shell
        lede={null}
        account={{ username: "genitore@example.invalid", onSignOut: () => undefined }}
      >
        {children === undefined ? (
          <Dashboard api={api} />
        ) : (
          <ApiProvider api={api}>{children}</ApiProvider>
        )}
      </Shell>
    </LanguageProvider>,
  );
}
