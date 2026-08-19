import { MsalProvider } from "@azure/msal-react";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { AdminApp } from "@/admin/AdminApp";
import { adminMsal } from "@/admin/msal";
import { adminConfig } from "@/config";
import { LanguageProvider } from "@/i18n";

import "../index.css";

const root = createRoot(document.getElementById("root")!);

const render = () =>
  root.render(
    <StrictMode>
      <MsalProvider instance={adminMsal}>
        <LanguageProvider>
          <AdminApp />
        </LanguageProvider>
      </MsalProvider>
    </StrictMode>,
  );

/* initialize() must finish before anything else: after returning from the identity
 * provider the authorisation code is sitting in the URL and is consumed exactly once.
 * With no application registered there is nothing to initialise, and the page says so
 * rather than failing on a client id that is the empty string. */
if (adminConfig.configured) {
  void adminMsal.initialize().then(render);
} else {
  render();
}
