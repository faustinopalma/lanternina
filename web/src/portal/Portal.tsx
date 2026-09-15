import { InteractionStatus, type AccountInfo } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { Camera, ImagePlus, RefreshCw, Send, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import type { Photograph } from "@/api/types";
import { bearerFor, signIn, signOut } from "@/auth/msal";
import { Shell } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";
import { portalApi, PortalError, preparePhoto, type PortalApi } from "./api";
import { clearInvitation, invitationToken } from "./session";

function problem(error: unknown): MessageKey {
  if (!(error instanceof PortalError)) return "portal.failed";
  if (error.detail === "invitation_email_mismatch") return "portal.mismatch";
  if (error.detail === "parent_account") return "portal.parentAccount";
  if (error.status === 429) return "portal.redemptionLimit";
  if (error.status === 410) return "portal.unavailable";
  if (error.status === 403) return "portal.denied";
  return "portal.failed";
}

export function Portal() {
  const { accounts, inProgress } = useMsal();
  const { t } = useWords();
  const [failure, setFailure] = useState(false);
  const account = accounts[0];
  const starting = inProgress === InteractionStatus.Startup
    || inProgress === InteractionStatus.HandleRedirect;
  return <Shell lede={null} account={account ? {
    username: account.username, onSignOut: () => void signOut().catch(() => setFailure(true)),
  } : null}>
    {failure && <p role="alert">{t("portal.failed")}</p>}
    {starting ? <p role="status">{t("portal.loading")}</p> : account ?
      <PortalAccount key={account.homeAccountId} account={account} /> :
      <section className="space-y-5 py-8">
        <h1 className="text-2xl font-semibold">{t(invitationToken() ? "portal.invited" : "portal.show")}</h1>
        {invitationToken() && <p>{t("portal.emailNote")}</p>}
        <Button variant="primary" onClick={() => void signIn().catch(() => setFailure(true))}>
          {t("portal.register")}
        </Button>
      </section>}
  </Shell>;
}

function PortalAccount({ account }: { account: AccountInfo }) {
  const [api] = useState(() => portalApi(() => bearerFor(account)));
  return <PortalSession api={api} />;
}

export function PortalSession({ api }: { api: PortalApi }) {
  const { t } = useWords();
  const [token, setToken] = useState(invitationToken);
  const [enteredCode, setEnteredCode] = useState(() => token ?? "");
  const [accepted, setAccepted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<MessageKey | null>(null);
  const [member, reload] = useLoad(async () => {
    if (token) return { allowed: false, error: null };
    try { await api.me(); return { allowed: true, error: null }; }
    catch (caught) {
      if (caught instanceof PortalError && [401, 403].includes(caught.status)) {
        return { allowed: false, error: problem(caught) };
      }
      throw caught;
    }
  }, [api, token, accepted], { live: !token });

  async function accept() {
    const code = enteredCode.trim();
    if (!/^[A-Za-z0-9_-]{40,100}$/.test(code)) {
      setError("portal.invalidCode");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await api.accept(code);
      clearInvitation();
      setToken(null);
      setEnteredCode("");
      setAccepted(true);
    } catch (caught) { setError(problem(caught)); }
    finally { setBusy(false); }
  }

  const redemption = <section className="space-y-4 py-8">
    <h1 className="text-2xl font-semibold">{t("portal.invited")}</h1>
    <p>{t("portal.emailNote")}</p>
    {error && <p role="alert">{t(error)}</p>}
    <form className="space-y-3" onSubmit={(event) => { event.preventDefault(); void accept(); }}>
      <label htmlFor="redemption-code">{t("portal.code")}</label>
      <Input id="redemption-code" className="block w-full max-w-[40rem] font-mono" required
        autoComplete="off" autoCapitalize="none" spellCheck={false} maxLength={100}
        value={enteredCode} disabled={busy} onChange={(event) => setEnteredCode(event.target.value)} />
      <Button type="submit" variant="primary" disabled={busy || !enteredCode.trim()}>{t("portal.accept")}</Button>
    </form>
  </section>;
  if (token) return redemption;
  if (member.status === "loading") return <p role="status">{t("portal.loading")}</p>;
  if (member.status === "failed") return <section className="space-y-4">
    <p role="alert">{t("portal.failed")}</p><Button onClick={reload}>{t("portal.retry")}</Button>
  </section>;
  if (!member.data.allowed) return <section className="space-y-4">
    <p role="alert">{t(member.data.error ?? "portal.loading")}</p>
    {redemption}
    <Button onClick={reload}>{t("portal.retry")}</Button>
  </section>;
  return <PhotoPortal api={api} />;
}

function PhotoItem({ photo, api, changed }: { photo: Photograph; api: PortalApi; changed: () => void }) {
  const { t, dateTime } = useWords();
  const [url, setUrl] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  const [confirm, setConfirm] = useState(false);
  const [busy, setBusy] = useState(false);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let current = true;
    let objectUrl: string | null = null;
    setFailed(false);
    void api.content(photo.id).then((blob) => {
      if (!current) return;
      objectUrl = URL.createObjectURL(blob);
      setUrl(objectUrl);
    }).catch(() => { if (current) setFailed(true); });
    return () => { current = false; if (objectUrl) URL.revokeObjectURL(objectUrl); };
  }, [api, photo.id, attempt]);

  async function remove() {
    setBusy(true);
    setFailed(false);
    try { await api.delete(photo.id); changed(); }
    catch { setFailed(true); }
    finally { setBusy(false); }
  }
  return <article className="min-w-0 space-y-3 border-b border-edge pb-5">
    <div className="aspect-[4/3] overflow-hidden rounded-[8px] bg-card">
      {url ? <img src={url} alt={dateTime(photo.receivedAt)} className="h-full w-full object-contain" />
        : <Button onClick={() => setAttempt(attempt + 1)}>{t(failed ? "portal.retry" : "portal.loading")}</Button>}
    </div>
    <p className="text-sm">{dateTime(photo.receivedAt)}</p>
    <p>{t(`portal.state.${photo.state}`)}</p>
    {failed && confirm && <p role="alert">{t("portal.deleteFailed")}</p>}
    {confirm ? <div className="space-y-3">
      <p>{t("portal.deleteConfirm")}</p>
      <div className="flex flex-wrap gap-2">
        <Button disabled={busy} onClick={() => void remove()}>{t("portal.delete")}</Button>
        <Button disabled={busy} onClick={() => setConfirm(false)}>{t("portal.cancel")}</Button>
      </div>
    </div> : <Button title={t("portal.delete")} aria-label={t("portal.delete")}
      onClick={() => setConfirm(true)}><Trash2 aria-hidden className="size-5" /></Button>}
  </article>;
}

export function PhotoPortal({ api }: { api: PortalApi }) {
  const { t } = useWords();
  const [page, setPage] = useState(1);
  const [history, refresh] = useLoad(() => api.photos(page), [api, page], { live: true });
  const [photo, setPhoto] = useState<{ id: string; blob: Blob; url: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<MessageKey | null>(null);
  const [online, setOnline] = useState(navigator.onLine);
  const camera = useRef<HTMLInputElement>(null);
  const library = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const update = () => setOnline(navigator.onLine);
    window.addEventListener("online", update);
    window.addEventListener("offline", update);
    return () => { window.removeEventListener("online", update); window.removeEventListener("offline", update); };
  }, []);
  useEffect(() => () => { if (photo) URL.revokeObjectURL(photo.url); }, [photo]);
  useEffect(() => {
    if (!photo) return;
    const warn = (event: BeforeUnloadEvent) => { event.preventDefault(); event.returnValue = ""; };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [photo]);

  async function choose(file?: File) {
    if (!file) return;
    setBusy(true);
    setMessage(null);
    try {
      const blob = await preparePhoto(file);
      setPhoto({ id: crypto.randomUUID().replaceAll("-", ""), blob, url: URL.createObjectURL(blob) });
    } catch { setMessage("portal.badPhoto"); }
    finally { setBusy(false); }
  }
  async function send() {
    if (!photo) return;
    setBusy(true);
    setMessage(null);
    try {
      await api.send(photo.id, photo.blob);
      setPhoto(null);
      setMessage("portal.saved");
      setPage(1);
      refresh();
    } catch (error) {
      setMessage(error instanceof PortalError && error.detail === "photo_daily_limit" ? "portal.dailyLimit" :
        error instanceof PortalError && error.status === 429 ? "portal.full" :
        error instanceof PortalError && error.status === 403 ? "portal.denied" : "portal.photoFailed");
    } finally { setBusy(false); }
  }

  return <div className="mx-auto max-w-[60rem] space-y-8 pb-12">
    <section className="space-y-5 border-b border-edge py-6">
      <h1 className="text-2xl font-semibold">{t("portal.show")}</h1>
      <input ref={camera} type="file" accept="image/jpeg,image/png,image/webp" capture="environment" hidden
        onChange={(event) => { void choose(event.target.files?.[0]); event.target.value = ""; }} />
      <input ref={library} type="file" accept="image/jpeg,image/png,image/webp" hidden
        onChange={(event) => { void choose(event.target.files?.[0]); event.target.value = ""; }} />
      {!photo ? <div className="flex flex-wrap gap-3">
        <Button variant="primary" disabled={busy} onClick={() => camera.current?.click()}>
          <Camera aria-hidden className="size-6" />{t("portal.camera")}
        </Button>
        <Button disabled={busy} onClick={() => library.current?.click()}>
          <ImagePlus aria-hidden className="size-5" />{t("portal.choose")}
        </Button>
      </div> : <div className="max-w-[40rem] space-y-4">
        <img src={photo.url} alt={t("portal.preview")}
          className="aspect-[4/3] w-full rounded-[8px] object-contain bg-card" />
        <p>{t("portal.visibility")}</p>
        <div className="flex flex-wrap gap-3">
          <Button variant="primary" disabled={busy || !online} onClick={() => void send()}>
            <Send aria-hidden className="size-5" />{t(busy ? "portal.sending" : "portal.send")}
          </Button>
          <Button disabled={busy} title={t("portal.cancel")} aria-label={t("portal.cancel")}
            onClick={() => setPhoto(null)}><X aria-hidden className="size-5" /></Button>
        </div>
      </div>}
      {!online && <p role="alert">{t("portal.offline")}</p>}
      <p role="status">{message ? t(message) : busy && !photo ? t("portal.loading") : ""}</p>
    </section>
    <section className="space-y-5">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-xl font-semibold">{t("portal.history")}</h2>
        <Button onClick={refresh} aria-label={t("portal.refresh")} title={t("portal.refresh")}>
          <RefreshCw aria-hidden className="size-5" />
        </Button>
      </div>
      {history.status === "loading" && <p role="status">{t("portal.loading")}</p>}
      {history.status === "failed" && <p role="alert">{t("portal.failed")}</p>}
      {history.status === "ready" && <>
        {history.data.photos.length === 0 && <p>{t("portal.empty")}</p>}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {history.data.photos.map((entry) => <PhotoItem key={entry.id} photo={entry} api={api} changed={refresh} />)}
        </div>
        {history.data.pages > 1 && <nav className="flex flex-wrap items-center gap-3">
          <Button disabled={history.data.page <= 1} onClick={() => setPage(history.data.page - 1)}>{t("portal.previous")}</Button>
          <span>{history.data.page} / {history.data.pages}</span>
          <Button disabled={history.data.page >= history.data.pages} onClick={() => setPage(history.data.page + 1)}>{t("portal.next")}</Button>
        </nav>}
      </>}
    </section>
  </div>;
}