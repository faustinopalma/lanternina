import { InteractionStatus } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { useCallback, useEffect, useState } from "react";

import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Card, CardTitle, Quiet } from "@/components/ui/card";
import { adminConfig } from "@/config";
import { useWords } from "@/i18n";

import { httpAdminApi, type AdminApi, type Admission, type Waiting } from "./api";
import { adminBearerFor, adminSignIn, adminSignOut } from "./msal";

type Stage =
  | { view: "loading" }
  | { view: "signedout" }
  | { view: "notAdmin" }
  | { view: "notConfigured" }
  | { view: "failed" }
  | { view: "list"; api: AdminApi };

/** The waiting sign-ups, and the two decisions. Nothing else is on this page: an
 *  administrator judges an address, and everything about a family stays where it is. */
function WaitingList({ api }: { api: AdminApi }) {
  const { t, ago, dateTime } = useWords();
  const [rows, setRows] = useState<Waiting[] | null>(null);
  const [broken, setBroken] = useState(false);
  const [busy, setBusy] = useState("");

  const load = useCallback(() => {
    api
      .waiting()
      .then(setRows)
      .catch(() => setBroken(true));
  }, [api]);

  useEffect(load, [load]);

  const decide = (id: string, state: Admission) => {
    setBusy(id);
    api
      .decide(id, state)
      .then(() => {
        // Re-read rather than remove the row locally: another administrator may have
        // decided in the meantime, and the list is the truth.
        load();
      })
      .catch(() => setBroken(true))
      .finally(() => setBusy(""));
  };

  if (broken) return <Quiet>{t("admin.waiting.unreadable")}</Quiet>;
  if (rows === null) return <Quiet aria-live="polite">{t("admin.waiting.loading")}</Quiet>;
  if (rows.length === 0) return <Quiet>{t("admin.waiting.empty")}</Quiet>;

  const now = Date.now() / 1000;

  return (
    <ul className="flex flex-col gap-3">
      {rows.map((row) => (
        <li
          key={row.id}
          className="flex flex-wrap items-center justify-between gap-x-5 gap-y-3 rounded-control border border-edge p-4"
        >
          <span className="flex flex-col gap-0.5">
            <span className="font-medium break-all">{row.contact}</span>
            <span className="text-[0.85rem] text-quiet" title={dateTime(row.createdAt)}>
              {ago(now - row.createdAt)}
            </span>
          </span>
          <span className="flex gap-2.5">
            <Button
              variant="primary"
              size="small"
              disabled={busy === row.id}
              onClick={() => decide(row.id, "active")}
            >
              {t("admin.admit")}
            </Button>
            <Button
              size="small"
              disabled={busy === row.id}
              onClick={() => decide(row.id, "rejected")}
            >
              {t("admin.refuse")}
            </Button>
          </span>
        </li>
      ))}
    </ul>
  );
}

export function AdminApp() {
  const { t } = useWords();
  const { accounts, inProgress } = useMsal();
  const [stage, setStage] = useState<Stage>(
    adminConfig.configured ? { view: "loading" } : { view: "notConfigured" },
  );

  useEffect(() => {
    if (!adminConfig.configured) return;
    if (inProgress !== InteractionStatus.None) return;
    const account = accounts[0];
    if (account === undefined) {
      setStage({ view: "signedout" });
      return;
    }

    let live = true;
    (async () => {
      const token = await adminBearerFor(account);
      // null means a redirect is under way and this page is about to be replaced.
      if (token === null || !live) return;
      const api = httpAdminApi(token);
      const standing = await api.standing();
      if (!live) return;
      setStage(standing === "in" ? { view: "list", api } : { view: standing });
    })().catch(() => {
      if (live) setStage({ view: "failed" });
    });

    return () => {
      live = false;
    };
  }, [accounts, inProgress]);

  const signedIn = accounts[0];

  return (
    <Shell
      lede="admin.lede"
      account={
        signedIn === undefined
          ? null
          : { username: signedIn.username, onSignOut: () => void adminSignOut() }
      }
    >
      {stage.view === "signedout" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("admin.signin.title")}</CardTitle>
          <p>{t("admin.signin.body")}</p>
          <div className="mt-6 flex flex-wrap gap-2.5">
            <Button variant="primary" onClick={() => void adminSignIn()}>
              {t("admin.signin.button")}
            </Button>
          </div>
        </Card>
      ) : null}

      {stage.view === "notAdmin" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("admin.notAdmin.title")}</CardTitle>
          <p>{t("admin.notAdmin.body")}</p>
        </Card>
      ) : null}

      {stage.view === "notConfigured" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("admin.notConfigured.title")}</CardTitle>
          <p>{t("admin.notConfigured.body")}</p>
        </Card>
      ) : null}

      {stage.view === "failed" ? (
        <Card className="max-w-[34rem]">
          <CardTitle>{t("error.title")}</CardTitle>
          <p>{t("error.signin")}</p>
          <div className="mt-6 flex flex-wrap gap-2.5">
            <Button onClick={() => window.location.reload()}>{t("error.retry")}</Button>
          </div>
        </Card>
      ) : null}

      {stage.view === "list" ? (
        <Card>
          <CardTitle>{t("admin.waiting.title")}</CardTitle>
          <Quiet className="mb-5">{t("admin.waiting.note")}</Quiet>
          <WaitingList api={stage.api} />
        </Card>
      ) : null}
    </Shell>
  );
}
