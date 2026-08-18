import { InteractionStatus } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { useEffect, useState } from "react";

import { httpApi } from "@/api/client";
import type { Api } from "@/api/types";
import { bearerFor, signIn, signOut } from "@/auth/msal";
import { Dashboard } from "@/components/Dashboard";
import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Card, CardTitle, Quiet } from "@/components/ui/card";
import { useWords, type MessageKey } from "@/i18n";

type Stage =
  | { view: "loading" }
  | { view: "signedout" }
  | { view: "connecting" }
  | { view: "pending" }
  | { view: "dashboard"; api: Api }
  | { view: "error"; message: MessageKey };

// One line under the name, saying where the parent is. The dashboard says nothing: the
// section headings are already there, and a running commentary on what the program is
// doing is a thing for us, not for whoever is holding the phone.
const LEDE: Record<Stage["view"], MessageKey | null> = {
  loading: "lede.checking",
  signedout: "lede.signedout",
  connecting: "lede.checking",
  pending: "lede.pending",
  dashboard: null,
  error: "lede.failed",
};

export function App() {
  const { t } = useWords();
  const { accounts, inProgress } = useMsal();
  const [stage, setStage] = useState<Stage>({ view: "loading" });

  useEffect(() => {
    if (inProgress !== InteractionStatus.None) return;
    const account = accounts[0];
    if (account === undefined) {
      setStage({ view: "signedout" });
      return;
    }

    let live = true;
    setStage({ view: "connecting" });

    (async () => {
      const token = await bearerFor(account);
      // null means a redirect is under way and this page is about to be replaced.
      if (token === null || !live) return;
      const api = httpApi(token);
      const admission = await api.admission();
      if (!live) return;
      if (admission.kind === "in") {
        setStage({ view: "dashboard", api });
      } else if (admission.kind === "pending") {
        setStage({ view: "pending" });
      } else {
        setStage({
          view: "error",
          message: admission.kind === "noAuth" ? "error.noAuth" : "error.refused",
        });
      }
    })().catch(() => {
      // A rejected redirect leaves MSAL's interaction flag set, so every later click is
      // refused and the button simply stops responding. Say so instead.
      if (live) setStage({ view: "error", message: "error.signin" });
    });

    return () => {
      live = false;
    };
  }, [accounts, inProgress]);

  const signedIn = accounts[0];

  return (
    <Shell
      lede={LEDE[stage.view]}
      account={
        signedIn === undefined
          ? null
          : { username: signedIn.username, onSignOut: () => void signOut() }
      }
    >
      {stage.view === "signedout" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("signin.title")}</CardTitle>
          <p>{t("signin.body")}</p>
          <div className="mt-6 flex flex-wrap gap-2.5">
            <Button variant="primary" onClick={() => void signIn()}>
              {t("signin.button")}
            </Button>
          </div>
        </Card>
      ) : null}

      {stage.view === "connecting" ? (
        <Card className="max-w-[34rem]" aria-live="polite">
          <Quiet>{t("connecting.note")}</Quiet>
        </Card>
      ) : null}

      {stage.view === "pending" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("pending.title")}</CardTitle>
          <p className="mb-3">{t("pending.body")}</p>
          <Quiet>{t("pending.note")}</Quiet>
        </Card>
      ) : null}

      {stage.view === "dashboard" ? <Dashboard api={stage.api} /> : null}

      {stage.view === "error" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("error.title")}</CardTitle>
          <p>{t(stage.message)}</p>
          <div className="mt-6 flex flex-wrap gap-2.5">
            <Button onClick={() => window.location.reload()}>{t("error.retry")}</Button>
          </div>
        </Card>
      ) : null}
    </Shell>
  );
}
