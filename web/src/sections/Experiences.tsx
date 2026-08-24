import { useState } from "react";

import { useApi } from "@/api/client";
import type { Decision, Moment, OfferedExperience } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/* An afternoon a model devised, shown to the one person who decides whether it may happen
 * in this house. Approval is given to the overview — that is what `ideas/08 §2` settled —
 * and the whole plan is here underneath it, because an overview nobody can check against
 * the document is a claim about itself.
 *
 * There is no button that asks for one. The house asks on its own rhythm and the parent
 * decides about what came back; a "devise me one" control is the exact thing an inert
 * panel forbids, and its absence is the feature.
 */

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
  const design = moment.design;
  /* The labels beside the boxes, the lines and the drawing areas: the words an
   * adolescent is asked something by. Where the marks sit on the page is left out — a
   * position means nothing to somebody not holding the sheet. */
  const asked = (design?.marks ?? [])
    .map((mark) => (mark.mark === "words" ? mark.text : mark.label))
    .filter((words) => Boolean(words));
  return (
    <>
      <p className="mt-1">{design?.title}</p>
      <Quiet>{design?.instructions}</Quiet>
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

function Card({
  offered,
  onDecided,
}: {
  offered: OfferedExperience;
  onDecided: (state: Decision) => void;
}) {
  const { t, dateTime } = useWords();
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

  return (
    <article className="mt-3.5 max-w-[42rem] rounded-control border border-edge bg-paper p-[18px] pb-4">
      <h3 className="text-[1.05rem] font-semibold">{offered.title}</h3>
      <Quiet className="mb-2">{t("experiences.minutes", { minutes: offered.minutes })}</Quiet>
      <p className="mb-2">{offered.overview}</p>
      <Button size="small" variant="ghost" aria-expanded={open} onClick={() => setOpen(!open)}>
        {t(open ? "experiences.hide" : "experiences.read")}
      </Button>
      {open ? <Plan moments={offered.experience.moments} /> : null}
      <div className="mt-3.5 flex flex-wrap gap-2.5">
        {approved ? (
          offered.begunAt > 0 ? (
            /* Nothing to press. An afternoon the house has begun is out of reach from
               here, which is true of every afternoon once it has started. */
            <Quiet>{t("experiences.begun", { when: dateTime(offered.begunAt) })}</Quiet>
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
  const left = state.data.filter((offered) => !withdrawn.includes(offered.id));

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
  // An approval moves an afternoon from one list to the other, so the second is asked
  // again rather than left showing what was true before the button was pressed.
  const [approvals, setApprovals] = useState(0);

  if (state.status === "loading") return <Quiet>{t("experiences.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("experiences.unreadable")}</Quiet>;

  const waiting = state.data.filter((offered) => !decided.includes(offered.id));

  return (
    <div aria-live="polite">
      <Quiet>{t("experiences.laterNote")}</Quiet>
      {waiting.length === 0 ? (
        <Quiet className="mt-3.5">{t("experiences.empty")}</Quiet>
      ) : (
        waiting.map((offered) => (
          <Card
            key={offered.id}
            offered={offered}
            onDecided={(state) => {
              setDecided((seen) => [...seen, offered.id]);
              if (state === "approved") setApprovals((n) => n + 1);
            }}
          />
        ))
      )}
      <Approved again={approvals} />
    </div>
  );
}
