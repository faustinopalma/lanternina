import { useEffect, useRef, useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import type { Draft, DraftCard } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label, Textarea } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* An idea the parent is working on, in a conversation, with the text open beside it.
 *
 * **The parent judges an afternoon by four things** — title, overview, themes, script — and
 * those four are what this edits. Never the plan: the moments have a format with a dozen
 * checks behind them, and free text cannot become one. Approving hands the script to the
 * deviser as a brief, and what comes back is checked and screened like an afternoon nobody
 * steered. So a refusal is a normal outcome here, and it arrives with its reason, because
 * the parent has the text and can change it.
 *
 * **The text is theirs to type in.** Asking a model to change one word is slower than
 * changing it, and costs money to do worse. What is typed is saved by an inert write.
 *
 * This is the one page in the panel where a parent's own action calls a model. What that
 * does not do is reach the house — see `docs/NON-GOALS.md`, which was amended rather than
 * quietly bent.
 */

/* The two panes stop being two on a narrow screen: a chat beside a document in 24rem is
   two unusable columns. Stacked, the conversation comes first, because that is what the
   parent came to do. */
function Conversation({
  draft,
  onSaid,
  busy,
  problem,
}: {
  draft: Draft;
  onSaid: (words: string) => void;
  busy: boolean;
  problem: MessageKey | null;
}) {
  const { t } = useWords();
  const [words, setWords] = useState("");
  const end = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Guarded because scrolling is a nicety and losing it must not take the pane with it:
    // jsdom has no `scrollIntoView` at all, and the whole component threw on mount.
    end.current?.scrollIntoView?.({ block: "end" });
  }, [draft.said.length, busy]);

  function send(event: FormEvent) {
    event.preventDefault();
    const said = words.trim();
    if (!said || busy) return;
    onSaid(said);
    setWords("");
  }

  return (
    <div className="flex min-h-[24rem] flex-col rounded-control border border-edge bg-paper p-4">
      <div className="mb-3 flex-1 overflow-y-auto" aria-live="polite">
        {draft.said.length === 0 ? (
          <Quiet>{t(draft.script ? "drafts.openingNote" : "drafts.blankNote")}</Quiet>
        ) : null}
        {draft.said.map((turn, index) => (
          <p
            key={`${turn.at}-${index}`}
            className={
              turn.who === "parent"
                ? "mt-2.5 rounded-control bg-card px-3 py-2"
                : "mt-2.5 px-3 py-2 text-quiet"
            }
          >
            {turn.words}
          </p>
        ))}
        {/* Said out loud because the first one is slow: the container that answers has
            scaled to zero and is starting. A spinner would not explain that. */}
        {busy ? <Quiet className="mt-2.5">{t("drafts.thinking")}</Quiet> : null}
        <div ref={end} />
      </div>
      <form className="flex flex-col gap-2" onSubmit={send}>
        <Label htmlFor="draft-say">{t("drafts.say")}</Label>
        <Textarea
          id="draft-say"
          rows={3}
          value={words}
          disabled={busy}
          placeholder={t("drafts.sayPlaceholder")}
          onChange={(event) => setWords(event.target.value)}
        />
        <Button type="submit" variant="primary" disabled={busy || words.trim() === ""}>
          {t("drafts.send")}
        </Button>
        {problem === null ? null : <Quiet aria-live="polite">{t(problem)}</Quiet>}
      </form>
    </div>
  );
}

function TheText({
  draft,
  onTyped,
  busy,
}: {
  draft: Draft;
  onTyped: (text: { title: string; overview: string; script: string }) => void;
  busy: boolean;
}) {
  const { t } = useWords();
  const [title, setTitle] = useState(draft.title);
  const [overview, setOverview] = useState(draft.overview);
  const [script, setScript] = useState(draft.script);
  const [known, setKnown] = useState(draft.updatedAt);

  /* The model rewrites the same text the parent is typing in, so the boxes follow the
     draft when a turn comes back — and only then. Following it on every render would
     overwrite a half-typed word with what the server last saw. */
  useEffect(() => {
    if (draft.updatedAt === known) return;
    setKnown(draft.updatedAt);
    setTitle(draft.title);
    setOverview(draft.overview);
    setScript(draft.script);
  }, [draft.updatedAt, draft.title, draft.overview, draft.script, known]);

  const changed =
    title !== draft.title || overview !== draft.overview || script !== draft.script;

  return (
    <div className="flex flex-col gap-3 rounded-control border border-edge bg-paper p-4">
      <div className="flex flex-col gap-1.5">
        <Label htmlFor="draft-title">{t("drafts.titleField")}</Label>
        <Input
          id="draft-title"
          value={title}
          disabled={busy}
          onChange={(event) => setTitle(event.target.value)}
        />
      </div>
      <div className="flex flex-col gap-1.5">
        <Label htmlFor="draft-overview">{t("drafts.overviewField")}</Label>
        <Textarea
          id="draft-overview"
          rows={3}
          value={overview}
          disabled={busy}
          onChange={(event) => setOverview(event.target.value)}
        />
      </div>
      {draft.themes.length > 0 ? (
        <p className="flex flex-wrap gap-1.5">
          {draft.themes.map((theme) => (
            <span
              key={theme}
              className="rounded-full border border-edge px-2.5 py-0.5 text-[0.8rem]"
            >
              {theme}
            </span>
          ))}
        </p>
      ) : null}
      <div className="flex flex-col gap-1.5">
        <Label htmlFor="draft-script">{t("drafts.scriptField")}</Label>
        <Textarea
          id="draft-script"
          rows={20}
          value={script}
          disabled={busy}
          className="font-mono text-[0.88rem]"
          onChange={(event) => setScript(event.target.value)}
        />
      </div>
      {/* Grey until the text and the draft differ, like every other save here. */}
      <Button
        size="small"
        disabled={busy || !changed}
        className="self-start"
        onClick={() => onTyped({ title, overview, script })}
      >
        {t("drafts.keepTyping")}
      </Button>
    </div>
  );
}

function Working({ id, onDone }: { id: string; onDone: () => void }) {
  const api = useApi();
  const { t } = useWords();
  const [state, again] = useLoad(() => api.draft(id), [id]);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState<MessageKey | null>(null);
  const [refused, setRefused] = useState("");

  const shown = draft ?? (state.status === "ready" ? state.data : null);

  if (state.status === "loading" && draft === null) return <Quiet>{t("drafts.loading")}</Quiet>;
  if (state.status === "failed" && draft === null) return <Quiet>{t("drafts.unreadable")}</Quiet>;
  if (shown === null) return null;

  async function said(words: string) {
    setBusy(true);
    setProblem(null);
    try {
      setDraft(await api.sayToDraft(id, words));
    } catch {
      setProblem("drafts.sayFailed");
    }
    setBusy(false);
  }

  async function typed(text: { title: string; overview: string; script: string }) {
    setProblem(null);
    try {
      setDraft(await api.typeIntoDraft(id, text));
    } catch {
      setProblem("drafts.keepFailed");
    }
  }

  async function approve() {
    setBusy(true);
    setProblem(null);
    setRefused("");
    try {
      await api.approveDraft(id);
      onDone();
    } catch (error) {
      /* The reason, not a shrug. A script asking for a scoreboard is refused by the same
         check whoever wrote it, and the parent can change the text and try again — which
         is the whole point of them having the text. */
      setRefused(error instanceof Error ? error.message : "");
      setProblem("drafts.approveFailed");
    }
    setBusy(false);
  }

  async function close() {
    try {
      await api.closeDraft(id);
    } finally {
      onDone();
    }
  }

  return (
    <div>
      <div className="mt-3.5 grid gap-4 wide:grid-cols-2 wide:items-start">
        <Conversation draft={shown} onSaid={said} busy={busy} problem={problem} />
        <TheText draft={shown} onTyped={typed} busy={busy} />
      </div>
      <div className="mt-3.5 flex flex-wrap items-center gap-2.5">
        <Button
          variant="primary"
          disabled={busy || shown.script.trim() === ""}
          onClick={approve}
        >
          {t("drafts.approve")}
        </Button>
        <Button disabled={busy} onClick={close}>
          {t("drafts.close")}
        </Button>
        <Button size="small" variant="ghost" disabled={busy} onClick={again}>
          {t("drafts.reread")}
        </Button>
      </div>
      <Quiet className="mt-2">{t("drafts.approveNote")}</Quiet>
      {refused === "" ? null : (
        <Quiet className="mt-2" aria-live="polite">
          {refused}
        </Quiet>
      )}
    </div>
  );
}

function Cards({
  drafts,
  onOpen,
}: {
  drafts: DraftCard[];
  onOpen: (id: string) => void;
}) {
  const { t, dateTime } = useWords();
  const open = drafts.filter((one) => one.state === "open");
  if (open.length === 0) return null;

  return (
    <div className="mt-3.5">
      <h3 className="mb-1 text-[1.05rem] font-semibold">{t("drafts.open")}</h3>
      {open.map((one) => (
        <article
          key={one.id}
          className="mt-2.5 max-w-[42rem] rounded-control border border-edge bg-paper p-4"
        >
          <p className="font-semibold">{one.title || t("drafts.untitled")}</p>
          <Quiet>{dateTime(one.updatedAt || one.createdAt)}</Quiet>
          {one.overview ? <p className="mt-1">{one.overview}</p> : null}
          <Button size="small" className="mt-2.5" onClick={() => onOpen(one.id)}>
            {t("drafts.reopen")}
          </Button>
        </article>
      ))}
    </div>
  );
}

/* The same two panes, opened from wherever a parent decided to take an afternoon apart
 * rather than approve or refuse it. Exported so the afternoons page can show it in place:
 * sending the parent to another section and asking them to find their draft there is two
 * steps for something they just asked for. */
export function WorkOn({ id, onDone }: { id: string; onDone: () => void }) {
  return <Working id={id} onDone={onDone} />;
}

export function Drafts() {
  const api = useApi();
  const { t } = useWords();
  const [round, setRound] = useState(0);
  const [state] = useLoad(() => api.drafts(), [round]);
  const [working, setWorking] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);

  async function blank() {
    setStarting(true);
    try {
      setWorking((await api.startDraft("")).id);
    } finally {
      setStarting(false);
    }
  }

  if (working !== null) {
    return (
      <Working
        id={working}
        onDone={() => {
          setWorking(null);
          setRound((n) => n + 1);
        }}
      />
    );
  }

  return (
    <div>
      <Button variant="primary" disabled={starting} onClick={blank}>
        {t("drafts.blank")}
      </Button>
      <Quiet className="mt-2">{t("drafts.blankHint")}</Quiet>
      {state.status === "ready" ? (
        <Cards drafts={state.data} onOpen={setWorking} />
      ) : null}
    </div>
  );
}
