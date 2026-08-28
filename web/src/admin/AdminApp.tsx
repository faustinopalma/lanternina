import { InteractionStatus } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { useCallback, useEffect, useState } from "react";

import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Card, CardTitle, Quiet } from "@/components/ui/card";
import { adminConfig } from "@/config";
import { useWords } from "@/i18n";

import { httpAdminApi, type AdminApi, type Admission, type Keeping, type Waiting } from "./api";
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

/** The one permission that is not a parent's to give: whether a household is one somebody
 *  is building against, and so keeps what came back off its glass as well as what the
 *  system wrote. It is off everywhere unless it is turned on here, and it lapses on its own
 *  rather than waiting to be turned off. `panel/keeping.py` has the whole of it.
 *
 *  A field for the household rather than a list of them: a page that enumerated households
 *  would be a way to find out who is registered, which is the thing the sign-up list is
 *  deliberately not. */
function WorkingOn({ api }: { api: AdminApi }) {
  const { t, dateTime } = useWords();
  const [household, setHousehold] = useState("");
  const [found, setFound] = useState<Keeping | null>(null);
  const [broken, setBroken] = useState(false);
  const [busy, setBusy] = useState(false);

  const answered = (work: Promise<Keeping>) => {
    setBusy(true);
    setBroken(false);
    work
      .then(setFound)
      .catch(() => setBroken(true))
      .finally(() => setBusy(false));
  };

  return (
    <div>
      <div className="flex flex-wrap items-end gap-2.5">
        <label className="flex flex-col gap-1">
          <span className="text-[0.85rem] text-quiet">{t("admin.keeping.household")}</span>
          <input
            className="rounded-control border border-edge bg-paper px-3 py-2"
            value={household}
            onChange={(event) => {
              setHousehold(event.target.value);
              setFound(null);
            }}
          />
        </label>
        <Button
          size="small"
          disabled={busy || !household.trim()}
          onClick={() => answered(api.keeping(household.trim()))}
        >
          {t("admin.keeping.look")}
        </Button>
      </div>

      {broken ? <Quiet className="mt-3">{t("admin.keeping.unreadable")}</Quiet> : null}

      {found !== null ? (
        <div className="mt-4">
          <p>
            {found.keeping
              ? t("admin.keeping.standing", { until: dateTime(found.until) })
              : t("admin.keeping.notStanding")}
          </p>
          <div className="mt-3 flex flex-wrap gap-2.5">
            <Button
              size="small"
              disabled={busy}
              onClick={() => answered(api.keep(found.householdId, true))}
            >
              {t(found.keeping ? "admin.keeping.renew" : "admin.keeping.on", {
                days: String(found.daysAtATime),
              })}
            </Button>
            {found.keeping ? (
              <Button
                size="small"
                disabled={busy}
                onClick={() => answered(api.keep(found.householdId, false))}
              >
                {t("admin.keeping.off")}
              </Button>
            ) : null}
          </div>
        </div>
      ) : null}
    </div>
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

      {stage.view === "list" ? (
        <Card>
          <CardTitle>{t("admin.keeping.title")}</CardTitle>
          <Quiet className="mb-5">{t("admin.keeping.note")}</Quiet>
          <WorkingOn api={stage.api} />
        </Card>
      ) : null}
    </Shell>
  );
}
