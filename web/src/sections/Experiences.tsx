import { useState } from "react";

import { useApi } from "@/api/client";
import type { Backlog, Decision, Moment, OfferedExperience } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* An afternoon a model devised, shown to the one person who decides whether it may happen
 * in this house.
 *
 * **The parent judges an idea, not a script.** Approval is given to the overview — that is
 * what `ideas/08 §2` settled — and nothing here may assume they read the steps. The steps
 * are behind a button because an overview nobody *can* check is a claim about itself; being
 * able to look and choosing not to are different things, and only the first is designed for.
 *
 * So the summary has to be enough on its own. Title, length and overview were not: none of
 * them says what will actually happen in the room. `shapeOf` counts that off the document —
 * how many sheets it prints, whether the scanner is wanted — because a parent decides on
 * "two sheets and the scanner" without wanting the sheets themselves.
 *
 * There is no button that asks for one. The house asks on its own rhythm and the parent
 * decides about what came back; a "devise me one" control is the exact thing an inert
 * panel forbids, and its absence is the feature.
 */

/** What the afternoon does to the room, counted off the moments rather than described. */
function shapeOf(moments: Moment[]): { sheets: number; scanner: boolean } {
  return {
    sheets: moments.filter((moment) => moment.act === "hand_over").length,
    scanner: moments.some((moment) => moment.act === "collect"),
  };
}

/** Everything a model wrote reaches this page as text. Nothing here is markup. */
function Plan({ moments }: { moments: Moment[] }) {
  return (
    <ol className="mt-2.5 flex list-none flex-col gap-2.5 p-0">
      {moments.map((moment) => (
        <li key={moment.id} className="border-l-2 border-edge pl-3">
          <Step moment={moment} />
        </li>
      ))}
    </ol>
  );
}

function Step({ moment }: { moment: Moment }) {
  const { t } = useWords();
  const kind =
    moment.act === "close"
      ? "experiences.close"
      : moment.act === "hand_over"
        ? "experiences.handOver"
        : moment.act === "collect"
          ? "experiences.collect"
          : "experiences.say";
  /* The standard version is what is shown, and the other two are named by how long they
   * take. A parent reading the plan is reading what usually happens; that it can be run
   * shorter or longer is a property of the document, not three paragraphs to read. */
  const standard = moment.weights?.standard;

  return (
    <>
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">{t(kind)}</p>
      <p>{moment.heading}</p>
      {(standard?.lines ?? []).map((line, index) => (
        <Quiet key={index}>{line}</Quiet>
      ))}
      {moment.act === "hand_over" ? <Page moment={moment} /> : null}
      {moment.act === "collect" ? <Branches moment={moment} /> : null}
      <Ladder moment={moment} />
      <WayOutOf moment={moment} />
    </>
  );
}

function Page({ moment }: { moment: Moment }) {
  const { t } = useWords();
  const page = moment.page;
  /* Every word that will be lettered on the paper, because the parent approves the
   * afternoon once and this is where the page's words are read. What is left out is the
   * illustration: it describes a drawing and is never printed as text. */
  const asked = (page?.spaces ?? []).map((space) => space.label).filter(Boolean);
  return (
    <>
      <p className="mt-1">{page?.title}</p>
      {(page?.note ?? []).map((line) => (
        <Quiet key={line}>{line}</Quiet>
      ))}
      {asked.length === 0 ? null : <Quiet>{asked.map((words) => `«${words}»`).join(" ")}</Quiet>}
      {(moment.instead ?? []).length === 0 ? null : (
        <Quiet>
          {t("experiences.instead")} {(moment.instead ?? []).join(" ")}
        </Quiet>
      )}
    </>
  );
}

function Branches({ moment }: { moment: Moment }) {
  const { t } = useWords();
  const named = (then: string) => (then === "ask" ? t("experiences.asks") : then);
  return (
    <>
      {(moment.outcomes ?? []).map((outcome) => (
        <Quiet key={outcome.when}>
          {t(outcome.when === "blank" ? "experiences.blank" : "experiences.marks")}{" "}
          {named(outcome.then)}
        </Quiet>
      ))}
      {moment.if_no_page ? (
        <Quiet>
          {t("experiences.ifNoPage")} {named(moment.if_no_page)}
        </Quiet>
      ) : null}
    </>
  );
}

/* Four rungs, written in the plan. What is shown is what is written, never what was given:
 * `ideas/09 §8` is why there is no route in that direction at all. */
function Ladder({ moment }: { moment: Moment }) {
  const { t } = useWords();
  if (!(moment.help ?? []).length) return null;
  return (
    <Quiet>
      {t("experiences.help")}{" "}
      {(moment.help ?? []).map((rung) => rung.lines.join(" ")).join(" · ")}
    </Quiet>
  );
}

function WayOutOf({ moment }: { moment: Moment }) {
  const { t } = useWords();
  const out = moment.way_out;
  if (!out) return null;
  return (
    <Quiet>
      {t("experiences.wayOut", { minutes: out.minutes })} {out.heading}. {out.lines.join(" ")}
    </Quiet>
  );
}

/* An afternoon the house has begun, and the only thing that reaches one from here.
 *
 * Two things, chosen from a list of two, with an hour where an hour is what moved. There
 * is no box to type a sentence in and there will not be one: `shared/message.py` says why
 * at length, and the short version is that a sentence about a person reaches a model and
 * colours everything written after it.
 *
 * Pressing writes a row. Nothing is sent, nothing is woken, and the house applies it on
 * the look it already makes every ten minutes. Nothing appears on any display when it
 * does — an afternoon whose hour moved looks like an afternoon that is ending. */
function Saying({ when }: { when: number }) {
  const { t, dateTime } = useWords();
  const api = useApi();
  const [at, setAt] = useState("");
  const [saying, setSaying] = useState(false);
  const [failed, setFailed] = useState(false);
  const [again, setAgain] = useState(0);
  const [waiting] = useLoad(() => api.messages(), [again]);

  async function say(said: { says: string; at?: string }) {
    setSaying(true);
    setFailed(false);
    try {
      await api.say(said);
      setAgain((n) => n + 1);
    } catch {
      setFailed(true);
    }
    setSaying(false);
  }

  const pending = waiting.status === "ready" && waiting.data.length > 0;

  return (
    <div className="w-full">
      <Quiet>{t("experiences.begun", { when: dateTime(when) })}</Quiet>
      <form
        className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-2"
        onSubmit={(event) => {
          event.preventDefault();
          void say({ says: "end_by", at });
        }}
      >
        <Label htmlFor="end-by">{t("experiences.endBy")}</Label>
        <Input
          id="end-by"
          type="time"
          required
          className="w-34"
          value={at}
          onChange={(event) => setAt(event.target.value)}
        />
        <Button type="submit" size="small" disabled={saying}>
          {t("action.moveTheHour")}
        </Button>
        <Button
          type="button"
          size="small"
          disabled={saying}
          onClick={() => void say({ says: "close_now" })}
        >
          {t("action.closeNow")}
        </Button>
      </form>
      <Quiet className="mt-2">{t("experiences.sayingNote")}</Quiet>
      <Quiet aria-live="polite">
        {failed ? t("experiences.sayFailed") : pending ? t("experiences.saidWaiting") : ""}
      </Quiet>
    </div>
  );
}

function Card({
  offered,
  picked,
  onPick,
  onDecided,
}: {
  offered: OfferedExperience;
  picked?: boolean;
  onPick?: (on: boolean) => void;
  onDecided: (state: Decision) => void;
}) {
  const { t } = useWords();
  const api = useApi();
  const [open, setOpen] = useState(false);
  const [deciding, setDeciding] = useState(false);
  const [failed, setFailed] = useState(false);
  async function decide(state: Decision) {
    setDeciding(true);
    setFailed(false);
    try {
      await api.decideExperience(offered.id, state);
      onDecided(state);
    } catch {
      setFailed(true);
      setDeciding(false);
    }
  }

  const approved = offered.state === "approved";

  // One line the parent can decide on without opening anything: how long, how much paper,
  // and whether the scanner is wanted.
  const shape = shapeOf(offered.experience.moments);
  const summary = [
    t("experiences.minutes", { minutes: offered.minutes }),
    shape.sheets > 0 ? t("experiences.sheets", { sheets: shape.sheets }) : null,
    shape.scanner ? t("experiences.usesScanner") : null,
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <article className="mt-3.5 max-w-[42rem] rounded-control border border-edge bg-paper p-[18px] pb-4">
      <h3 className="text-[1.05rem] font-semibold">
        {onPick ? (
          <label className="flex items-start gap-2.5">
            {/* Ticking is how a sitting is built. It decides nothing on its own: the
                buttons at the bottom send whatever is ticked, in one request. */}
            <input
              type="checkbox"
              className="mt-1.5"
              checked={picked ?? false}
              onChange={(event) => onPick(event.target.checked)}
              aria-label={t("experiences.pick", { title: offered.title })}
            />
            <span>{offered.title}</span>
          </label>
        ) : (
          offered.title
        )}
      </h3>
      <Quiet className="mb-2">{summary}</Quiet>
      {offered.themes?.length ? (
        <p className="mb-2 flex flex-wrap gap-1.5">
          {offered.themes.map((theme) => (
            <span
              key={theme}
              className="rounded-full border border-edge px-2.5 py-0.5 text-[0.8rem]"
            >
              {theme}
            </span>
          ))}
        </p>
      ) : null}
      <p className="mb-2">{offered.overview}</p>
      {offered.strategy ? (
        <details className="mb-2">
          <summary className="cursor-pointer text-[0.88rem] text-quiet">
            {t("experiences.strategy")}
          </summary>
          <p className="mt-1.5 text-[0.9rem]">{offered.strategy}</p>
        </details>
      ) : null}
      <Button size="small" variant="ghost" aria-expanded={open} onClick={() => setOpen(!open)}>
        {t(open ? "experiences.hide" : "experiences.read")}
      </Button>
      {open ? <Plan moments={offered.experience.moments} /> : null}
      <div className="mt-3.5 flex flex-wrap gap-2.5">
        {approved ? (
          offered.begunAt > 0 ? (
            /* An afternoon the house has begun cannot be withdrawn, stopped or watched
               from here. What it can be given is an hour. */
            <Saying when={offered.begunAt} />
          ) : (
            <Button size="small" disabled={deciding} onClick={() => decide("withdrawn")}>
              {t("action.withdraw")}
            </Button>
          )
        ) : (
          <>
            <Button
              variant="primary"
              size="small"
              disabled={deciding}
              onClick={() => decide("approved")}
            >
              {t("action.approve")}
            </Button>
            <Button size="small" disabled={deciding} onClick={() => decide("rejected")}>
              {t("action.refuse")}
            </Button>
          </>
        )}
      </div>
      {failed ? <Quiet className="mt-2.5">{t("experiences.decideFailed")}</Quiet> : null}
    </article>
  );
}

/* What the house may still be handed. Kept visible so that withdrawing is possible after
 * the fact — and so that a parent can see there is one waiting rather than none. */
function Approved({ again }: { again: number }) {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.experiences("approved"), [again]);
  const [withdrawn, setWithdrawn] = useState<string[]>([]);

  if (state.status !== "ready") return null;
  const left = state.data.experiences.filter((offered) => !withdrawn.includes(offered.id));

  return (
    <section className="mt-7 border-t border-edge pt-5">
      <h2 className="mb-2 text-[1.05rem] font-semibold">{t("experiences.approved")}</h2>
      {left.length === 0 ? <Quiet>{t("experiences.noneApproved")}</Quiet> : null}
      {left.map((offered) => (
        <Card
          key={offered.id}
          offered={offered}
          onDecided={() => setWithdrawn((gone) => [...gone, offered.id])}
        />
      ))}
      {withdrawn.length > 0 ? <Quiet className="mt-2.5">{t("experiences.withdrawn")}</Quiet> : null}
    </section>
  );
}

export function Experiences() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.experiences("pending"));
  const [decided, setDecided] = useState<string[]>([]);
  const [approvals, setApprovals] = useState(0);
  // What the parent has ticked in this sitting but not yet sent. Held here rather than on
  // each card, because the whole point is that they go up together.
  const [picked, setPicked] = useState<string[]>([]);
  const [sending, setSending] = useState(false);
  const [stock, setStock] = useState<Backlog | null>(null);

  if (state.status === "loading") return <Quiet>{t("experiences.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("experiences.unreadable")}</Quiet>;

  const waiting = state.data.experiences.filter((offered) => !decided.includes(offered.id));
  const backlog = stock ?? state.data.backlog;

  async function sit(decision: "approved" | "rejected") {
    const ids = picked;
    setSending(true);
    try {
      setStock(await api.decideSeveral(ids, decision));
      setDecided((seen) => [...seen, ...ids]);
      setPicked([]);
      if (decision === "approved") setApprovals((n) => n + 1);
    } catch {
      // Nothing is removed from the list, so what failed is still there to try again.
    }
    setSending(false);
  }

  return (
    <div aria-live="polite">
      <Stock backlog={backlog} />
      <Quiet>{t("experiences.laterNote")}</Quiet>
      {waiting.length === 0 ? (
        <Quiet className="mt-3.5">{t("experiences.empty")}</Quiet>
      ) : (
        <>
          {waiting.map((offered) => (
            <Card
              key={offered.id}
              offered={offered}
              picked={picked.includes(offered.id)}
              onPick={(on) =>
                setPicked((chosen) =>
                  on ? [...chosen, offered.id] : chosen.filter((id) => id !== offered.id),
                )
              }
              onDecided={(state) => {
                setDecided((seen) => [...seen, offered.id]);
                if (state === "approved") setApprovals((n) => n + 1);
              }}
            />
          ))}
          {picked.length > 0 ? (
            <div className="sticky bottom-3 mt-3.5 flex max-w-[42rem] flex-wrap items-center gap-2.5 rounded-control border border-edge bg-paper p-3">
              <Quiet>{t("experiences.picked", { count: picked.length })}</Quiet>
              <span className="ml-auto flex gap-2">
                <Button
                  variant="primary"
                  size="small"
                  disabled={sending}
                  onClick={() => void sit("approved")}
                >
                  {t("action.approveThese")}
                </Button>
                <Button size="small" disabled={sending} onClick={() => void sit("rejected")}>
                  {t("action.refuseThese")}
                </Button>
              </span>
            </div>
          ) : null}
        </>
      )}
      <Approved again={approvals} />
    </div>
  );
}

/* What the house has in hand, read before closing the panel for a week. `days` is a floor:
 * the stock spread over the days the rhythm allows, rounded down. Nothing here says how
 * many afternoons happened — that number does not exist anywhere, on purpose. */
function Stock({ backlog }: { backlog: Backlog }) {
  const { t } = useWords();
  if (backlog.approved === 0) return <Quiet className="mb-2">{t("experiences.stockNone")}</Quiet>;
  return (
    <p className="mb-2 font-medium">
      {t("experiences.stock", { approved: backlog.approved })}
      {backlog.days > 0 ? ` · ${t("experiences.stockDays", { days: backlog.days })}` : ""}
    </p>
  );
}
