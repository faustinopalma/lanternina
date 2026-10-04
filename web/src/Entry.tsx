import { InteractionStatus, type AccountInfo } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { useEffect } from "react";

import { App } from "@/App";
import { bearerFor } from "@/auth/msal";
import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";
import { Portal } from "@/portal/Portal";
import { clearInvitation, clearPortalReturn, sessionDestination } from "@/portal/session";

export function Entry({ portalRequested }: { portalRequested: boolean }) {
  const { accounts, inProgress } = useMsal();
  const { t } = useWords();
  if (inProgress === InteractionStatus.Startup || inProgress === InteractionStatus.HandleRedirect) {
    return <Shell lede={null} account={null}><p role="status">{t("portal.loading")}</p></Shell>;
  }
  const account = accounts[0];
  if (!account) return portalRequested ? <Portal /> : <App />;
  return <AccountEntry key={`${account.homeAccountId}:${account.localAccountId}`}
    account={account} portalRequested={portalRequested} />;
}

function AccountEntry({ account, portalRequested }: {
  account: AccountInfo; portalRequested: boolean;
}) {
  const { t } = useWords();
  const [session, retry] = useLoad(() => sessionDestination(() => bearerFor(account)), [account]);
  const destination = session.status === "ready" ? session.data : null;
  useEffect(() => {
    if (!destination) return;
    clearPortalReturn();
    if (destination === "new") return;
    if (destination === "parent") clearInvitation();
    const path = destination === "parent" ? "/" : "/portal";
    if (location.pathname !== path) history.replaceState(null, "", path + location.search);
  }, [destination]);
  if (session.status === "failed") return <Shell lede={null} account={null}>
    <p role="alert">{t("portal.failed")}</p>
    <Button onClick={retry}>{t("portal.retry")}</Button>
  </Shell>;
  if (!destination) return <Shell lede={null} account={null}><p role="status">{t("portal.loading")}</p></Shell>;
  return destination === "adolescent" || (destination === "new" && portalRequested)
    ? <Portal /> : <App />;
}