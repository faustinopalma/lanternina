import { Copy, KeyRound, Link, RefreshCw, UserX } from "lucide-react";
import { useState } from "react";

import { useApi } from "@/api/client";
import type { InvitationCode } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/field";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

export function Adolescents() {
  const api = useApi();
  const { t, dateTime } = useWords();
  const [state, refresh] = useLoad(() => api.familyAccess(), [api]);
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [confirm, setConfirm] = useState<string | null>(null);
  const [issued, setIssued] = useState<(InvitationCode & { email: string }) | null>(null);

  async function invite(address: string) {
    setBusy(true);
    setMessage("");
    try {
      const result = await api.inviteAdolescent(address);
      setIssued({ ...result, email: address });
      setEmail("");
      setMessage("");
      refresh();
    } catch { setMessage(t("access.failed")); }
    finally { setBusy(false); }
  }

  async function revoke(id: string) {
    setBusy(true);
    try {
      await api.revokeAdolescent(id);
      setIssued(null);
      setConfirm(null);
      refresh();
    } catch { setMessage(t("access.failed")); }
    finally { setBusy(false); }
  }

  async function copy(value: string) {
    try {
      await navigator.clipboard.writeText(value);
      setMessage(t("access.copied"));
    } catch { setMessage(t("access.copyFailed")); }
  }

  if (state.status === "loading") return <p role="status">{t("portal.loading")}</p>;
  if (state.status === "failed") return <Button onClick={refresh}>{t("portal.retry")}</Button>;
  const active = state.data.members.filter((member) => member.active);
  const invitations = state.data.invitations.filter((entry) => entry.status !== "accepted");
  return <div className="max-w-[42rem] space-y-6">
    <form onSubmit={(event) => { event.preventDefault(); void invite(email); }} className="space-y-3">
      <label className="block" htmlFor="adolescent-email">{t("access.email")}</label>
      <div className="flex flex-wrap gap-3">
        <Input id="adolescent-email" type="email" autoComplete="email" required maxLength={254}
          className="min-w-0 flex-1" value={email} disabled={busy}
          onChange={(event) => setEmail(event.target.value)} />
        <Button type="submit" variant="primary" disabled={busy}>
          <KeyRound aria-hidden className="size-5" />{t("access.invite")}
        </Button>
      </div>
    </form>
    {issued && <section className="space-y-3 border-y border-edge py-4">
      <p className="break-all">{issued.email}</p>
      <p>{t("access.share", { date: dateTime(issued.expiresAt) })}</p>
      <label htmlFor="invitation-code">{t("portal.code")}</label>
      <Input id="invitation-code" value={issued.code} readOnly className="w-full font-mono"
        onFocus={(event) => event.target.select()} />
      <label htmlFor="invitation-link">{t("access.link")}</label>
      <Input id="invitation-link" value={`${window.location.origin}/portal#invite=${issued.code}`}
        readOnly className="w-full" onFocus={(event) => event.target.select()} />
      <div className="flex flex-wrap gap-3">
        <Button onClick={() => void copy(issued.code)}><Copy aria-hidden className="size-4" />{t("access.copy")}</Button>
        <Button onClick={() => void copy(`${window.location.origin}/portal#invite=${issued.code}`)}>
          <Link aria-hidden className="size-4" />{t("access.copyLink")}
        </Button>
      </div>
    </section>}
    <p role="status">{message}</p>
    {active.length === 0 && invitations.length === 0 && <p>{t("access.empty")}</p>}
    {[...active.map((member) => ({ ...member, status: "active", expiresAt: 0 })), ...invitations]
      .map((entry) => <div key={entry.id} className="border-t border-edge py-4 space-y-3">
        <p className="break-all font-semibold">{entry.email}</p>
        <p>{t(`access.state.${entry.status}` as Parameters<typeof t>[0])}
          {["sent", "ready"].includes(entry.status) ? ` · ${dateTime(entry.expiresAt)}` : ""}</p>
        {confirm === entry.id ? <div className="flex flex-wrap items-center gap-3">
          <p>{t("access.confirm")}</p>
          <Button disabled={busy} onClick={() => void revoke(entry.id)}>{t("access.revoke")}</Button>
          <Button disabled={busy} onClick={() => setConfirm(null)}>{t("portal.cancel")}</Button>
        </div> : <div className="flex flex-wrap gap-3">
          {entry.status !== "active" && <Button disabled={busy}
            onClick={() => void invite(entry.email)}>
            <RefreshCw aria-hidden className="size-4" />{t("access.resend")}
          </Button>}
          {["active", "ready", "sent", "sending"].includes(entry.status) && <Button disabled={busy}
            onClick={() => setConfirm(entry.id)}>
            <UserX aria-hidden className="size-4" />{t("access.revoke")}
          </Button>}
        </div>}
      </div>)}
  </div>;
}