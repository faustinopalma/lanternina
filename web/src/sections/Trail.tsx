import { useEffect, useState } from "react";
import { Square, Trash2 } from "lucide-react";

import { useApi } from "@/api/client";
import type { CurrentRun, Made, Trail } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* The sheet as it was drawn, fetched as bytes.
 *
 * The route wants a bearer token and an <img> sends no headers, so the element is handed a
 * blob URL — the same shape as the pictures section, and the reason the CSP allows `blob:`
 * for images. */
function Drawn({ pictureId }: { pictureId: string }) {
  const api = useApi();
  const { t } = useWords();
  const [url, setUrl] = useState("");
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let alive = true;
    let made = "";
    api
      .pageContent(pictureId)
      .then((bytes) => {
        if (!alive) return;
        made = URL.createObjectURL(bytes);
        setUrl(made);
      })
      .catch(() => alive && setFailed(true));
    return () => {
      alive = false;
      if (made) URL.revokeObjectURL(made);
    };
  }, [api, pictureId]);

  if (failed) return <Quiet className="mt-1">{t("trail.sheetGone")}</Quiet>;
  if (!url) return <Quiet className="mt-1">{t("trail.sheetLoading")}</Quiet>;
  return (
    <img
      src={url}
      alt={t("trail.sheetAlt")}
      className="mt-2 w-full max-w-[22rem] rounded-control border border-edge bg-white"
    />
  );
}

function Step({ made, technical = false }: { made: Made; technical?: boolean }) {
  const { t, dateTime } = useWords();
  /* Written out rather than built from `made.kind`: a key that only exists at runtime is a
     key no test can find missing. A kind we have no word for is shown as it arrived. */
  const kind =
    made.kind === "terminated" ? t("trail.terminated") : made.kind === "plan"
      ? t("trail.kind.plan")
      : made.kind === "say"
        ? t("trail.kind.say")
        : made.kind === "hand_over"
          ? t("trail.kind.hand_over")
          : made.kind === "collect"
            ? t("trail.kind.collect")
            : made.kind === "close"
              ? t("trail.kind.close")
              : made.kind === "continuation"
                ? t("trail.kind.continuation")
                : made.kind === "fault"
                  ? t("trail.kind.fault")
                  : made.kind === "came"
                    ? t("trail.kind.came")
                    : made.kind === "judged"
                      ? t("trail.kind.judged")
                      : made.kind === "drawn"
                        ? t("trail.kind.drawn")
                        : made.kind;
  const outcome = made.paper || made.body;

  return (
    <li className="min-w-0 border-l-2 border-edge pl-3 [overflow-wrap:anywhere]">
      <p className="text-[0.82rem] text-quiet">
        {technical ? t("trail.filedAt", { at: dateTime(made.at) }) : dateTime(made.at)}
      </p>
      <p className="font-medium">{kind}</p>
      {made.heading ? <p className="mt-1 text-[0.9rem] text-quiet">{made.heading}</p> : null}

      {technical && (outcome || made.pictureId) ? (
        <div className="mt-2">
          <p className="text-[0.82rem] tracking-wider text-quiet uppercase">
            {t("trail.modelDocument")}
          </p>
          {outcome ? <pre className="mt-1 max-w-full font-mono text-[0.82rem] whitespace-pre-wrap [overflow-wrap:anywhere]">{outcome}</pre> : null}
          {made.pictureId ? <Drawn pictureId={made.pictureId} /> : null}
        </div>
      ) : null}

      {!technical && made.body ? (
        made.kind === "came" || made.kind === "fault" ? <details className="mt-2">
          <summary className="cursor-pointer text-quiet">{t(made.kind === "came" ? "trail.reading" : "trail.failureDetail")}</summary>
          <pre className="mt-1 font-mono text-[0.82rem] whitespace-pre-wrap [overflow-wrap:anywhere]">{made.body}</pre>
        </details> : <blockquote className="mt-2 whitespace-pre-wrap">{made.body}</blockquote>
      ) : null}
      {!technical && made.paper ? <div className="mt-3">
        <p className="text-[0.82rem] text-quiet">{t("trail.onPaper")}</p>
        <p className="mt-1 whitespace-pre-wrap">{made.paper}</p>
      </div> : null}
      {made.asked || made.why || made.until ? <details className="mt-2">
        <summary className="cursor-pointer text-quiet">{t("trail.stepDetails")}</summary>
        {made.asked ? <div className="mt-2">
          <p className="text-[0.82rem] text-quiet">{t("trail.went_in")}</p>
          <pre className="mt-1 font-mono text-[0.82rem] whitespace-pre-wrap [overflow-wrap:anywhere]">{made.asked}</pre>
        </div> : null}
        {made.why ? <Quiet className="mt-2">{t("trail.why", { why: made.why })}</Quiet> : null}
        {made.until ? <Quiet className="mt-1">{t("trail.until")}</Quiet> : null}
      </details> : null}
    </li>
  );
}

/* An index of what reached paper, above the moves.
 *
 * Headings only, deliberately: the words that were on each sheet are in the move itself,
 * with the rest of its context, and printing them twice on one page makes the long one
 * harder to read rather than the short one easier. What this adds is the count and the
 * absences — until 5 September 2026 a page the printer never took looked exactly like a
 * page that came out, because the house counted the queue accepting the file as the sheet
 * being on the table. Two pages sat in a queue for eighty-two minutes and the trail showed
 * an afternoon that had gone as written. */

function Whole({ runId }: { runId: string }) {
  const api = useApi();
  const { t, dateTime } = useWords();
  const [state] = useLoad(() => api.trail(runId), [runId], { live: true });

  if (state.status === "loading") return <Quiet className="mt-2.5">{t("trail.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet className="mt-2.5">{t("trail.unreadable")}</Quiet>;
  const trail = state.data;
  const made = trail.made ?? [];
  const interactionKinds = new Set(["say", "hand_over", "collect", "close", "fault", "came", "terminated"]);
  const events = made.filter((one) => interactionKinds.has(one.kind));
  const documents = made.filter((one) => !interactionKinds.has(one.kind));
  const printed = events.filter((one) => one.kind === "hand_over").at(-1);

  return (
    <div className="mt-3">
      {printed ? <p className="mb-3">{t("trail.printedAt", { at: dateTime(printed.at) })}</p> : null}
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">{t("trail.made")}</p>
      {events.length === 0 ? (
        <Quiet className="mt-1">{t("trail.madeNothing")}</Quiet>
      ) : (
        <ol aria-label={t("trail.made")} className="mt-2 flex list-none flex-col gap-3.5 p-0">
          {events.map((one) => <Step key={one.id} made={one} />)}
        </ol>
      )}
      {trail.script || documents.length > 0 ? (
        <details className="mt-5 border-t border-edge pt-3">
          <summary className="cursor-pointer text-quiet">{t("trail.technical")}</summary>
          <Quiet className="mt-2">{t("trail.technicalNote")}</Quiet>
          {trail.script ? (
            <details className="mt-3">
              <summary className="cursor-pointer text-quiet">{t("trail.script")}</summary>
              <p className="mt-1 text-[0.9rem] whitespace-pre-wrap">{trail.script}</p>
            </details>
          ) : null}
          <ol className="mt-3 flex list-none flex-col gap-3.5 p-0">
            {documents.map((one) => <Step key={one.id} made={one} technical />)}
          </ol>
        </details>
      ) : null}
    </div>
  );
}

function Card({ trail, onDeleted }: { trail: Trail; onDeleted: () => void }) {
  const { t, dateTime } = useWords();
  const api = useApi();
  const [open, setOpen] = useState(false);
  const [sure, setSure] = useState(false);
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState(false);

  async function remove() {
    setBusy(true);
    setFailed(false);
    try {
      await api.forgetRun(trail.runId);
      onDeleted();
    } catch {
      setFailed(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <article className="mt-3.5 max-w-[42rem] rounded-control border border-edge bg-paper p-[18px] pb-4">
      <h3 className="text-[1.05rem] font-semibold">{trail.title}</h3>
      <Quiet className="mb-2">{dateTime(trail.beganAt)}</Quiet>
      <p className="mb-2">{trail.overview}</p>
      <div className="flex flex-wrap items-center gap-2">
        <Button size="small" variant="ghost" aria-expanded={open} onClick={() => setOpen(!open)}>
          {t(open ? "trail.hide" : "trail.read")}
        </Button>
        <Button size="small" variant="ghost" disabled={busy}
          title={t("trail.deleteOne", { title: trail.title })}
          aria-label={t("trail.deleteOne", { title: trail.title })}
          onClick={() => setSure(true)}>
          <Trash2 size={18} aria-hidden="true" />
        </Button>
      </div>
      {sure ? (
        <div className="mt-3" role="group" aria-label={t("trail.deleteConfirm", { title: trail.title })}>
          <p>{t("trail.deleteConfirm", { title: trail.title })}</p>
          <div className="mt-2 flex flex-wrap gap-2">
            <Button size="small" disabled={busy} onClick={remove}>{t("trail.deleteYes")}</Button>
            <Button size="small" variant="ghost" disabled={busy} onClick={() => setSure(false)}>{t("trail.cancel")}</Button>
          </div>
        </div>
      ) : null}
      {failed ? <Quiet role="alert">{t("trail.deleteFailed")}</Quiet> : null}
      {open ? <Whole runId={trail.runId} /> : null}
    </article>
  );
}

function Running({ run, fresh, terminationPending }: { run: CurrentRun; fresh: boolean; terminationPending: boolean }) {
  const { t, dateTime } = useWords();
  const api = useApi();
  const [termination, setTermination] = useState<"idle" | "confirm" | "busy" | "sent" | "failed">("idle");
  async function terminate() {
    setTermination("busy");
    try {
      await api.say({ says: "terminate", runId: run.runId });
      setTermination("sent");
    } catch {
      setTermination("failed");
    }
  }
  return (
    <article className="mt-3 border-b border-edge pb-5">
      <h3 className="text-[1.05rem] font-semibold">{run.title}</h3>
      <p className="mt-2 font-semibold">
        {run.phase === "waiting" ? t("trail.waiting") : run.phase === "received" ? t("trail.received") : run.phase === "ending" ? t("trail.ending") : t("trail.runUnreadable")}
      </p>
      {run.heading ? <p>{run.heading}</p> : null}
      {run.waitingSince > 0 ? <Quiet>{t("trail.waitingSince", { at: dateTime(run.waitingSince) })}</Quiet> : null}
      {run.receivedAt ? <Quiet>{t("trail.receivedAt", { at: dateTime(run.receivedAt) })}</Quiet> : null}
      {run.endsAt > 0 ? <Quiet>{t("trail.endsAt", { at: dateTime(run.endsAt) })}</Quiet> : null}
      <div className="mt-3 flex flex-wrap items-center gap-2">
        {termination === "confirm" ? <>
          <p>{t("trail.terminateQuestion")}</p>
          <Button onClick={() => void terminate()}>{t("trail.terminateConfirm")}</Button>
          <Button variant="ghost" onClick={() => setTermination("idle")}>{t("trail.cancel")}</Button>
        </> : termination === "sent" || terminationPending ? <Quiet role="status">{t("trail.terminateSent")}</Quiet> : <>
          <Button variant="ghost" disabled={termination === "busy"}
            onClick={() => setTermination("confirm")}><Square size={14} />{t("trail.terminate")}</Button>
          {termination === "failed" ? <p role="alert">{t("trail.terminateFailed")}</p> : null}
        </>}
      </div>
      {fresh ? <Whole runId={run.runId} /> : null}
    </article>
  );
}

export function TheTrail() {
  const api = useApi();
  const { t, dateTime } = useWords();
  const [state, again] = useLoad(() => api.trails(), [], { live: true });
  const [current] = useLoad(() => api.currentTrail(), [], { live: true });
  const [messages] = useLoad(() => api.messages(), [], { live: true });
  const [now, setNow] = useState(() => Date.now() / 1000);
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now() / 1000), 15_000);
    return () => window.clearInterval(timer);
  }, []);
  const snapshot = current.status === "ready" ? current.data : undefined;
  const fresh = !!snapshot?.updatedAt && now - snapshot.updatedAt <= 180;
  const currentIds = new Set(fresh ? snapshot?.runs.map((run) => run.runId) : []);
  /* Two presses, not a dialog. The first turns the button into what it will actually do,
     which is the sentence a parent needs before the second — and it is the parent's own
     record, so nothing here asks anybody's permission, only their attention. */
  const [sure, setSure] = useState(false);
  const [gone, setGone] = useState<number | null>(null);
  const [busy, setBusy] = useState(false);
  const [deletionVersion, setDeletionVersion] = useState(0);

  async function throwItAway() {
    if (!sure) {
      setSure(true);
      return;
    }
    setSure(false);
    setBusy(true);
    try {
      const { forgotten } = await api.forgetTrail();
      setGone(forgotten);
      setDeletionVersion((version) => version + 1);
      again();
    } catch {
      setGone(-1);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-[42rem] min-w-0 [overflow-wrap:anywhere]">
      <section aria-label={t("trail.current")} className="mb-6">
        <h2 className="text-[1.1rem] font-semibold">{t(fresh ? "trail.current" : "trail.lastKnown")}</h2>
        {current.status === "loading" ? <Quiet>{t("trail.loading")}</Quiet> : null}
        {current.status === "failed" || snapshot?.updatedAt === 0 ? <Quiet>{t("trail.statusUnavailable")}</Quiet> : null}
        {snapshot && snapshot.updatedAt > 0 ? (
          <>
            <Quiet>{t("trail.updatedAt", { at: dateTime(snapshot.updatedAt) })}</Quiet>
            {!fresh ? <p role="status">{t("trail.statusStale")}</p> : null}
            {fresh && snapshot.runs.length === 0 ? <p>{t("trail.idle")}</p> : null}
            {snapshot.runs.map((run) => <Running key={`${run.runId}:${deletionVersion}`} run={run} fresh={fresh}
              terminationPending={messages.status === "ready" && messages.data.some(message =>
                message.says === "terminate" && message.runId === run.runId)} />)}
          </>
        ) : null}
      </section>
      <h2 className="text-[1.1rem] font-semibold">{t("trail.history")}</h2>
      {state.status === "loading" ? <Quiet>{t("trail.loading")}</Quiet> : null}
      {state.status === "failed" ? <Quiet>{t("trail.unreadable")}</Quiet> : null}
      {state.status === "ready" && state.data.length === 0 ? (
        <Quiet>{t("trail.empty")}</Quiet>
      ) : null}
      {state.status === "ready"
        ? state.data.filter((trail) => !currentIds.has(trail.runId)).map((trail) => <Card key={trail.runId} trail={trail} onDeleted={again} />)
        : null}

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Button type="button" size="small" variant="ghost" disabled={busy} onClick={throwItAway}>
          {t(sure ? "trail.forgetSure" : "trail.forget")}
        </Button>
        {sure ? <Button size="small" variant="ghost" onClick={() => setSure(false)}>{t("trail.cancel")}</Button> : null}
        <Quiet aria-live="polite">
          {gone === null
            ? t("trail.forgetNote")
            : gone < 0
              ? t("trail.forgetFailed")
              : t("trail.forgotten", { n: String(gone) })}
        </Quiet>
      </div>
    </div>
  );
}
