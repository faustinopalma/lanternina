import { InteractionStatus, type AccountInfo } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { useState } from "react";

import { httpApi } from "@/api/client";
import type { Api } from "@/api/types";
import { bearerFor, signIn, signOut } from "@/auth/msal";
import { Dashboard } from "@/components/Dashboard";
import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Card, CardTitle, Quiet } from "@/components/ui/card";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

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
  const { accounts, inProgress } = useMsal();
  const signedIn = accounts[0];
  if (inProgress === InteractionStatus.Startup || inProgress === InteractionStatus.HandleRedirect) {
    return <SessionView stage={{ view: "loading" }} />;
  }
  return signedIn === undefined ? (
    <SessionView stage={{ view: "signedout" }} />
  ) : (
    <AccountPanel key={`${signedIn.homeAccountId}:${signedIn.localAccountId}`} account={signedIn} />
  );
}

function AccountPanel({ account }: { account: AccountInfo }) {
  const [api] = useState(() => httpApi(() => bearerFor(account)));
  const [admission, retry] = useLoad(() => api.admission(), [api]);
  let stage: Stage = { view: "connecting" };
  if (admission.status === "failed") {
    stage = { view: "error", message: "error.signin" };
  } else if (admission.status === "ready") {
    const { kind } = admission.data;
    stage = kind === "in" ? { view: "dashboard", api }
      : kind === "pending" ? { view: "pending" }
      : { view: "error", message: kind === "noAuth" ? "error.noAuth" : "error.refused" };
  }
  return <SessionView stage={stage} signedIn={account} retry={retry} />;
}

function SessionView({ stage, signedIn, retry }: {
  stage: Stage;
  signedIn?: AccountInfo;
  retry?: () => void;
}) {
  const { t } = useWords();
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
            <Button onClick={retry}>{t("error.retry")}</Button>
          </div>
        </Card>
      ) : null}
    </Shell>
  );
}
