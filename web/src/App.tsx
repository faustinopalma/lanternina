import { InteractionStatus } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { useEffect, useState } from "react";

import { httpApi } from "@/api/client";
import type { Api, Me } from "@/api/types";
import { bearerFor, signIn, signOut } from "@/auth/msal";
import { Dashboard } from "@/components/Dashboard";
import { Facts } from "@/components/Facts";
import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Card, CardTitle, Quiet } from "@/components/ui/card";
import { useWords, type MessageKey } from "@/i18n";

type Stage =
  | { view: "loading" }
  | { view: "signedout" }
  | { view: "connecting"; username: string }
  | { view: "pending" }
  | { view: "dashboard"; me: Me; api: Api; username: string }
  | { view: "error"; message: MessageKey };

const LEDE: Record<Stage["view"], MessageKey> = {
  loading: "lede.checking",
  signedout: "lede.signedout",
  connecting: "lede.ready",
  pending: "lede.pending",
  dashboard: "lede.in",
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
    setStage({ view: "connecting", username: account.username });

    (async () => {
      const token = await bearerFor(account);
      // null means a redirect is under way and this page is about to be replaced.
      if (token === null || !live) return;
      const api = httpApi(token);
      const admission = await api.admission();
      if (!live) return;
      if (admission.kind === "in") {
        setStage({ view: "dashboard", me: admission.me, api, username: account.username });
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

  return (
    <Shell lede={LEDE[stage.view]}>
      {stage.view === "loading" ? (
        <Card className="max-w-[34rem]">
          <Quiet>{t("loading.moment")}</Quiet>
        </Card>
      ) : null}

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
          <CardTitle>{t("panel.title")}</CardTitle>
          <Quiet>
            {stage.username ? t("signin.as", { user: stage.username }) : t("signin.anon")}
          </Quiet>
          <Facts rows={[{ label: t("facts.status"), value: t("connecting.loading") }]} />
          <Quiet className="mt-4">{t("connecting.note")}</Quiet>
        </Card>
      ) : null}

      {stage.view === "pending" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("pending.title")}</CardTitle>
          <p className="mb-3">{t("pending.body")}</p>
          <Quiet>{t("pending.note")}</Quiet>
          <div className="mt-6 flex flex-wrap gap-2.5">
            <Button onClick={() => void signOut()}>{t("signout")}</Button>
          </div>
        </Card>
      ) : null}

      {stage.view === "dashboard" ? (
        <Dashboard
          me={stage.me}
          api={stage.api}
          username={stage.username}
          onSignOut={() => void signOut()}
        />
      ) : null}

      {stage.view === "error" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("error.title")}</CardTitle>
          <p>{t(stage.message)}</p>
          <div className="mt-6 flex flex-wrap gap-2.5">
            <Button onClick={() => window.location.reload()}>{t("error.retry")}</Button>
            <Button onClick={() => void signOut()}>{t("signout")}</Button>
          </div>
        </Card>
      ) : null}
    </Shell>
  );
}
