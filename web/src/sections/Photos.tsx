import { ArrowLeft, ArrowRight, Download, Link2, RefreshCw, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { useApi } from "@/api/client";
import type { CurrentRun, Photograph, PhotoSelection } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

export function dateSelection(start: string, end: string): PhotoSelection | null {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2}$/.test(end) || end < start) return null;
  const first = new Date(`${start}T00:00:00`);
  const after = new Date(`${end}T00:00:00`);
  if (!Number.isFinite(first.getTime()) || !Number.isFinite(after.getTime())) return null;
  after.setDate(after.getDate() + 1);
  return { mode: "range", start: first.getTime() / 1000, end: after.getTime() / 1000 };
}

function PhotoTile({ photo, remove, disabled, runs, assignmentPending }: {
  photo: Photograph; remove: () => void; disabled: boolean; runs: CurrentRun[]; assignmentPending: boolean;
}) {
  const api = useApi();
  const { t, dateTime } = useWords();
  const [url, setUrl] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  const [chosen, setChosen] = useState("");
  const [assignment, setAssignment] = useState<"idle" | "busy" | "sent" | "failed">("idle");
  const candidates = photo.target && "candidates" in photo.target ? photo.target.candidates : [];
  const selected = photo.target && "run" in photo.target ? photo.target : null;
  const eligible = runs.filter(run => candidates.some(target => target.run === run.runId
    && target.moment === run.momentId && target.since === run.waitingSince));
  async function assign() {
    setAssignment("busy");
    try {
      await api.assignPhoto(photo.id, chosen);
      setAssignment("sent");
    } catch { setAssignment("failed"); }
  }
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    let current = true;
    let objectUrl: string | null = null;
    api.photoContent(photo.id).then(blob => {
      if (current) { objectUrl = URL.createObjectURL(blob); setUrl(objectUrl); }
    }).catch(() => { if (current) setFailed(true); });
    return () => { current = false; if (objectUrl) URL.revokeObjectURL(objectUrl); };
  }, [api, photo.id]);
  const states: Record<Photograph["state"], MessageKey> = {
    pending: "photos.pending", processing: "photos.processing", done: "photos.done", failed: "photos.error",
    awaiting_assignment: "photos.awaitingAssignment",
  };
  return <figure className="m-0 min-w-0 overflow-hidden rounded-control border border-edge bg-paper">
    <button className="block aspect-[4/3] w-full cursor-zoom-in bg-white" disabled={!url}
      aria-label={t("pictures.enlarge")} onClick={() => dialog.current?.showModal()}>
      {url ? <img src={url} alt={t("photos.title")} className="h-full w-full object-contain" /> : null}
    </button>
    <figcaption className="space-y-1 border-t border-edge p-3 text-sm">
      <time>{dateTime(photo.date)}</time>
      {photo.capturedAt === null ? <Quiet>{t("photos.dateUnknown")}</Quiet> : null}
      <Quiet>{photo.width} × {photo.height} px · {photo.camera}</Quiet>
      <Quiet>{t(states[photo.state])}</Quiet>
      {selected ? <p>{t("photos.assignedActivity", {
        title: runs.find(run => run.runId === selected.run)?.title ?? selected.run,
      })}</p> : null}
      {photo.detail ? <details className="pt-1">
        <summary className="cursor-pointer text-quiet">{t("photos.processingDetail")}</summary>
        <p className="mt-1 whitespace-pre-wrap [overflow-wrap:anywhere]">{photo.detail}</p>
      </details> : null}
      {photo.state === "awaiting_assignment" ? <div className="space-y-2 pt-2">
        {assignment === "sent" || assignmentPending ? <p role="status">{t("photos.assignmentSent")}</p> : eligible.length ? <>
          <Label htmlFor={`activity-${photo.id}`}>{t("photos.activity")}</Label>
          <select id={`activity-${photo.id}`} className="block w-full min-w-0 border border-edge bg-paper p-2"
            value={chosen} disabled={disabled || assignment === "busy"}
            onChange={event => setChosen(event.target.value)}>
            <option value="">{t("photos.chooseActivity")}</option>
            {eligible.map(run => <option key={run.runId} value={run.runId}>{run.title} · {run.heading}</option>)}
          </select>
          <Button size="small" disabled={disabled || assignment === "busy" || !eligible.some(run => run.runId === chosen)}
            onClick={() => void assign()}><Link2 size={16} />{t("photos.assign")}</Button>
          {assignment === "failed" ? <p role="alert">{t("photos.assignmentFailed")}</p> : null}
        </> : <Quiet>{t("photos.noActivity")}</Quiet>}
      </div> : null}
      {failed ? <Quiet>{t("photos.failed")}</Quiet> : null}
      <div className="flex justify-end gap-2 pt-2">
        {url ? <a href={url} download={`${photo.id}.jpg`} aria-label={t("photos.download")}
          title={t("photos.download")} className="p-2"><Download className="size-5" /></a> : null}
        <Button size="small" disabled={disabled} aria-label={t("photos.delete")} title={t("photos.delete")} onClick={remove}>
          <Trash2 className="size-5" />
        </Button>
      </div>
    </figcaption>
    <dialog ref={dialog} className="m-auto max-h-[95vh] max-w-[95vw] rounded-control bg-paper p-3 backdrop:bg-black/60"
      onClick={event => { if (event.target === dialog.current) dialog.current.close(); }}>
      <Button className="ml-auto mb-2" aria-label={t("photos.close")} title={t("photos.close")}
        onClick={() => dialog.current?.close()}><X className="size-5" /></Button>
      {url ? <img src={url} alt={t("photos.title")} className="max-h-[80vh] max-w-full object-contain" /> : null}
    </dialog>
  </figure>;
}

export function Photos() {
  const api = useApi();
  const { t, dateTime } = useWords();
  const [page, setPage] = useState(1);
  const [state, reload] = useLoad(() => api.photos(page), [api, page], { live: true });
  const [current] = useLoad(() => api.currentTrail(), [], { live: true });
  const [messages] = useLoad(() => api.messages(), [], { live: true });
  const runs = current.status === "ready" && Date.now() / 1000 - current.data.updatedAt <= 180
    ? current.data.runs.filter(run => run.phase === "waiting" || run.phase === "received") : [];
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<{ text: string; temporary?: boolean } | null>(null);
  useEffect(() => {
    if (!message?.temporary) return;
    const timer = setTimeout(() => setMessage(null), 5000);
    return () => clearTimeout(timer);
  }, [message]);
  const [pending, setPending] = useState<{ selection: PhotoSelection; ids: string[] } | null>(null);
  const confirmation = useRef<HTMLDialogElement>(null);
  useEffect(() => { if (pending) confirmation.current?.showModal(); }, [pending]);
  const range = dateSelection(start, end);
  const cancel = () => { if (!busy) { confirmation.current?.close(); setPending(null); } };
  async function preview(selection: PhotoSelection) {
    setBusy(true); setMessage(null);
    try {
      const { ids } = await api.previewPhotoDeletion(selection);
      if (ids.length) setPending({ selection, ids });
      else setMessage({ text: t("photos.noMatch") });
    } catch { setMessage({ text: t("photos.deleteFailed") }); }
    finally { setBusy(false); }
  }
  async function erase() {
    if (!pending) return;
    setBusy(true);
    try {
      const result = await api.deletePhotos(pending.selection, pending.ids);
      setMessage(result.failed.length
        ? { text: t("photos.deleteFailed") }
        : { text: t("photos.deleted", { count: result.deleted.length }), temporary: true });
      confirmation.current?.close(); setPending(null); reload();
    } catch { setMessage({ text: t("photos.deleteFailed") }); }
    finally { setBusy(false); }
  }
  const disabled = busy || pending !== null;
  return <div className="mt-5 space-y-5">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <div aria-live="polite">
        {state.status === "ready" ? <>
          <p>{t("photos.total", { count: state.data.total })}</p>
          {state.data.lastReceivedAt !== null ? <Quiet>{t("photos.received", { date: dateTime(state.data.lastReceivedAt) })}</Quiet> : null}
          {state.data.hub ? <>
            <Quiet>{t("photos.hubContact", { date: dateTime(state.data.hub.contactAt) })}</Quiet>
            <Quiet>{t("photos.syncPending", { count: state.data.hub.pending })}</Quiet>
          </> : <Quiet>{t("photos.noHub")}</Quiet>}
        </> : <Quiet>{t(state.status === "loading" ? "photos.loading" : "photos.failed")}</Quiet>}
      </div>
      <Button disabled={disabled} aria-label={t("photos.refresh")} title={t("photos.refresh")} onClick={reload}><RefreshCw className="size-5" /></Button>
    </div>
    <div className="flex flex-wrap items-end gap-3 border-y border-edge py-4">
      <div><Label htmlFor="photos-start">{t("photos.start")}</Label><Input id="photos-start" type="date" value={start} disabled={disabled} onChange={event => setStart(event.target.value)} /></div>
      <div><Label htmlFor="photos-end">{t("photos.end")}</Label><Input id="photos-end" type="date" value={end} disabled={disabled} onChange={event => setEnd(event.target.value)} /></div>
      <Button disabled={disabled || range === null} onClick={() => { if (range) void preview(range); }}><Trash2 className="mr-2 size-4" />{t("photos.range")}</Button>
      <Button disabled={disabled || state.status !== "ready" || !state.data.total} onClick={() => void preview({ mode: "all" })}><Trash2 className="mr-2 size-4" />{t("photos.all")}</Button>
      {(start || end) && range === null ? <p className="w-full text-sm text-quiet">{t("photos.invalidDates")}</p> : null}
    </div>
    {state.status === "ready" && state.data.hub?.cameras?.length ? <details>
      <summary className="cursor-pointer">{t("photos.diagnostics")}</summary>
      {state.data.hub.cameras.map(camera => <section key={camera.id} className="my-3 min-w-0">
        <h4 className="text-sm">{camera.id}</h4>
        {[...camera.history].reverse().map((event, index) => <details key={index} className="border-b border-edge py-2 text-sm">
          <summary className="cursor-pointer break-words">
            {typeof event.receivedAt === "number" ? dateTime(event.receivedAt) : ""} · {String(event.phase ?? "")}
            {event.previousSleepConfirmed === true ? ` · ${t("photos.sleepConfirmed")}` : ""}
            {event.phase === "sleep_planned" ? ` · ${t("photos.sleepPlanned")}` : ""}
          </summary>
          <dl className="mt-2 grid grid-cols-[minmax(0,1fr)_minmax(0,2fr)] gap-x-3 gap-y-1 font-mono text-xs">
            {Object.entries(event).map(([key, value]) => <div key={key} className="contents">
              <dt className="break-words">{key}</dt><dd className="break-all">{String(value)}</dd>
            </div>)}
          </dl>
        </details>)}
      </section>)}
    </details> : null}
    {message ? <p role="status">{message.text}</p> : null}
    {state.status === "ready" ? <>
      {!state.data.total ? <Quiet>{t("photos.empty")}</Quiet> : null}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {state.data.photos.map(photo => <PhotoTile key={photo.id} photo={photo} disabled={disabled}
          runs={runs} assignmentPending={messages.status === "ready" && messages.data.some(message =>
            message.says === "assign_photo" && message.photoId === photo.id)}
          remove={() => void preview({ mode: "single", id: photo.id })} />)}
      </div>
      <div className="flex items-center justify-end gap-3">
        <Button disabled={disabled || state.data.page <= 1} aria-label={t("photos.previous")} title={t("photos.previous")}
          onClick={() => setPage(state.data.page - 1)}><ArrowLeft className="size-4" /></Button>
        <span>{t("photos.page", { page: state.data.page, pages: state.data.pages })}</span>
        <Button disabled={disabled || state.data.page >= state.data.pages} aria-label={t("photos.next")} title={t("photos.next")}
          onClick={() => setPage(state.data.page + 1)}><ArrowRight className="size-4" /></Button>
      </div>
    </> : null}
    <dialog ref={confirmation} aria-labelledby="delete-photos-title" onCancel={event => { event.preventDefault(); cancel(); }}
      className="m-auto w-[min(30rem,calc(100vw-32px))] rounded-control border border-edge bg-paper p-5 backdrop:bg-black/50">
      <h4 id="delete-photos-title" className="text-lg">{t("photos.confirm", { count: pending?.ids.length ?? 0 })}</h4>
      <p className="my-4 text-sm text-quiet">{t("photos.copies")}</p>
      <div className="flex flex-wrap justify-end gap-2">
        <Button disabled={busy} onClick={cancel}>{t("photos.cancel")}</Button>
        <Button disabled={busy} onClick={() => void erase()}><Trash2 className="mr-2 size-4" />{t("photos.confirmDelete")}</Button>
      </div>
    </dialog>
  </div>;
}