import { MsalProvider } from "@azure/msal-react";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "@/App";
import { warmUp } from "@/api/client";
import { msalInstance } from "@/auth/msal";
import { LanguageProvider } from "@/i18n";
import { portalEntry } from "@/portal/session";

import "./index.css";

const root = createRoot(document.getElementById("root")!);
const isPortal = portalEntry();

/* A way to look at the panel without an identity provider and without a household: the
 * fake API and synthetic content. Removed from the production bundle by the DEV guard —
 * `npm run build` is checked for the fixture text. */
if (import.meta.env.DEV && new URLSearchParams(window.location.search).has("preview")) {
  void Promise.all([
    import("@/components/Dashboard"),
    import("@/components/Shell"),
    import("@/test/fakeApi"),
    import("@/portal/Portal"),
  ]).then(([{ Dashboard }, { Shell }, { fakeApi, fakePortalApi }, { PhotoPortal }]) => {
    root.render(
      <StrictMode>
        <LanguageProvider>
          <Shell
            lede={null}
            account={{ username: isPortal ? "adolescente@example.invalid" : "genitore@example.invalid",
              onSignOut: () => undefined }}
          >
            {isPortal ? <PhotoPortal api={fakePortalApi()} /> : <Dashboard api={fakeApi()} />}
          </Shell>
        </LanguageProvider>
      </StrictMode>,
    );
  });
} else {
  /* initialize() must finish before anything else: after returning from the identity
   * provider the authorisation code is sitting in the URL and is consumed exactly once. */
  void msalInstance.initialize().then(async () => {
    warmUp();
    const Entry = isPortal ? (await import("@/portal/Portal")).Portal : App;
    root.render(
      <StrictMode>
        <MsalProvider instance={msalInstance}>
          <LanguageProvider>
            <Entry />
          </LanguageProvider>
        </MsalProvider>
      </StrictMode>,
    );
  });
}
