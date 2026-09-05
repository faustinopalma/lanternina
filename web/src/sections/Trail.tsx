import { useEffect, useState } from "react";

import { useApi } from "@/api/client";
import type { Made, Trail } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";
import { Verdicts } from "@/sections/Verdicts";

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
      .pictureContent(pictureId)
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
      className="mt-2 max-w-[22rem] rounded-control border border-edge bg-white"
    />
  );
}

/* What the system wrote, afternoon by afternoon.
 *
 * The parent approved an idea. Everything after that was written as the afternoon went, by
 * an agent working from the script, and none of it was approved by anybody — there is no
 * moment where a parent could stand between a generated page and the room without stopping
 * the afternoon to do it. This page is the other half of that trade: no veto on each piece,
 * and every piece readable afterwards, in full, beside the script it came from.
 *
 * **Only one half is here, and that is the design.** Nothing on this page says what the
 * adolescent did — not the pages that came back, not what was on them, not how long anything
 * took, not whether it was finished. None of it is stored, so none of it can be shown. What
 * is watched here is the machine.
 *
 * The exception is written where it is made: a household an administrator has turned on
 * while this is being built keeps the other half too, and those entries say on the page how
 * long they last. Nothing here can turn that on.
 *
 * A card carries a title and a date and nothing else, because that is what recognising an
 * afternoon needs. The script arrives when one is opened.
 */

/** The bodies are what a model wrote. They are text, and they are shown as text. */
function Written({ made }: { made: Made }) {
  const { t, dateTime } = useWords();
  /* Written out rather than built from `made.kind`: a key that only exists at runtime is a
     key no test can find missing. A kind we have no word for is shown as it arrived. */
  const kind =
    made.kind === "plan"
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

  return (
    <li className="border-l-2 border-edge pl-3">
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">{kind}</p>
      {made.heading ? <p className="font-semibold">{made.heading}</p> : null}
      {made.body ? (
        <p className="mt-1 text-[0.9rem] whitespace-pre-wrap">{made.body}</p>
      ) : null}
      {made.paper ? (
        <div className="mt-2 rounded-control border border-edge px-3 py-2">
          <p className="text-[0.82rem] tracking-wider text-quiet uppercase">
            {t("trail.paper")}
          </p>
          <p className="mt-1 text-[0.9rem] whitespace-pre-wrap">{made.paper}</p>
        </div>
      ) : null}
      {made.pictureId ? <Drawn pictureId={made.pictureId} /> : null}
      {made.asked ? (
        <details className="mt-2">
          <summary className="cursor-pointer text-[0.82rem] tracking-wider text-quiet uppercase">
            {t("trail.asked")}
          </summary>
          <p className="mt-1 text-[0.9rem] whitespace-pre-wrap">{made.asked}</p>
        </details>
      ) : null}
      {made.why ? <Quiet className="mt-1">{t("trail.why", { why: made.why })}</Quiet> : null}
      {made.until ? <Quiet className="mt-1">{t("trail.until")}</Quiet> : null}
      <Quiet className="mt-1">{dateTime(made.at)}</Quiet>
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
function OnPaper({ made }: { made: Made[] }) {
  const { t } = useWords();
  const drawn = made.filter((one) => one.kind === "drawn");
  const pages = made.filter((one) => one.kind === "hand_over");
  const faults = made.filter((one) => one.kind === "fault");
  if (drawn.length === 0 && pages.length === 0 && faults.length === 0) return null;

  return (
    <div className="mt-3 rounded-control border border-edge px-3 py-2">
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">
        {t("trail.onPaper")}
      </p>
      {pages.length === 0 ? <Quiet className="mt-1">{t("trail.onPaperNone")}</Quiet> : null}
      <ul className="mt-1 flex list-none flex-col gap-1 p-0">
        {drawn.map((one) => (
          <li key={one.id} className="text-[0.9rem]">
            {t("trail.onPaperDrawn")} — {one.heading}
          </li>
        ))}
        {pages.map((one) => (
          <li key={one.id} className="text-[0.9rem]">
            {one.heading}
          </li>
        ))}
        {faults.map((one) => (
          <li key={one.id} className="text-[0.9rem]">
            {t("trail.onPaperMissing")} — {one.heading}
          </li>
        ))}
      </ul>
    </div>
  );
}

function Whole({ runId }: { runId: string }) {
  const api = useApi();
  const { t } = useWords();
  const [state] = useLoad(() => api.trail(runId), [runId]);

  if (state.status === "loading") return <Quiet className="mt-2.5">{t("trail.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet className="mt-2.5">{t("trail.unreadable")}</Quiet>;
  const trail = state.data;
  const made = trail.made ?? [];

  return (
    <div className="mt-3">
      <OnPaper made={made} />
      {trail.script ? (
        <>
          <p className="mt-3 text-[0.82rem] tracking-wider text-quiet uppercase">
            {t("trail.script")}
          </p>
          <p className="mt-1 mb-3 text-[0.9rem] whitespace-pre-wrap">{trail.script}</p>
        </>
      ) : null}
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">{t("trail.made")}</p>
      {made.length === 0 ? (
        <Quiet className="mt-1">{t("trail.madeNothing")}</Quiet>
      ) : (
        <ol className="mt-2 flex list-none flex-col gap-2.5 p-0">
          {made.map((one) => (
            <Written key={one.id} made={one} />
          ))}
        </ol>
      )}
    </div>
  );
}

function Card({ trail }: { trail: Trail }) {
  const { t, dateTime } = useWords();
  const [open, setOpen] = useState(false);

  return (
    <article className="mt-3.5 max-w-[42rem] rounded-control border border-edge bg-paper p-[18px] pb-4">
      <h3 className="text-[1.05rem] font-semibold">{trail.title}</h3>
      <Quiet className="mb-2">{dateTime(trail.beganAt)}</Quiet>
      <p className="mb-2">{trail.overview}</p>
      <Button size="small" variant="ghost" aria-expanded={open} onClick={() => setOpen(!open)}>
        {t(open ? "trail.hide" : "trail.read")}
      </Button>
      {open ? <Whole runId={trail.runId} /> : null}
    </article>
  );
}

export function TheTrail() {
  const api = useApi();
  const { t } = useWords();
  const [state, again] = useLoad(() => api.trails());
  /* Two presses, not a dialog. The first turns the button into what it will actually do,
     which is the sentence a parent needs before the second — and it is the parent's own
     record, so nothing here asks anybody's permission, only their attention. */
  const [sure, setSure] = useState(false);
  const [gone, setGone] = useState<number | null>(null);

  async function throwItAway() {
    if (!sure) {
      setSure(true);
      return;
    }
    setSure(false);
    try {
      const { forgotten } = await api.forgetTrail();
      setGone(forgotten);
      again();
    } catch {
      setGone(-1);
    }
  }

  return (
    <div>
      {state.status === "loading" ? <Quiet>{t("trail.loading")}</Quiet> : null}
      {state.status === "failed" ? <Quiet>{t("trail.unreadable")}</Quiet> : null}
      {state.status === "ready" && state.data.length === 0 ? (
        <Quiet>{t("trail.empty")}</Quiet>
      ) : null}
      {state.status === "ready"
        ? state.data.map((trail) => <Card key={trail.runId} trail={trail} />)
        : null}

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Button type="button" size="small" variant="ghost" onClick={throwItAway}>
          {t(sure ? "trail.forgetSure" : "trail.forget")}
        </Button>
        <Quiet aria-live="polite">
          {gone === null
            ? t("trail.forgetNote")
            : gone < 0
              ? t("trail.forgetFailed")
              : t("trail.forgotten", { n: String(gone) })}
        </Quiet>
      </div>

      {/* One section, not two. The readings were their own page while the prompts were
          being changed, and a parent had to know that an afternoon they had not decided on
          yet was filed somewhere else from one that had run. Both are the same question —
          what did the system write, and what did a reader make of it — so they are read in
          one place, with the afternoons that happened first. */}
      <h3 className="mt-7 mb-1 text-[1.05rem] font-semibold">{t("trail.readings")}</h3>
      <Quiet>{t("trail.readingsNote")}</Quiet>
      <Verdicts
        alreadyOnTheTrail={
          state.status === "ready" ? state.data.map((one) => one.experienceId) : []
        }
      />
    </div>
  );
}
