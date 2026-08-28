import { useState } from "react";

import { useApi } from "@/api/client";
import type { Made, Trail } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

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
      {made.why ? <Quiet className="mt-1">{t("trail.why", { why: made.why })}</Quiet> : null}
      {made.until ? <Quiet className="mt-1">{t("trail.until")}</Quiet> : null}
      <Quiet className="mt-1">{dateTime(made.at)}</Quiet>
    </li>
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
      {trail.script ? (
        <>
          <p className="text-[0.82rem] tracking-wider text-quiet uppercase">
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
  const [state] = useLoad(() => api.trails());

  if (state.status === "loading") return <Quiet>{t("trail.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("trail.unreadable")}</Quiet>;
  if (state.data.length === 0) return <Quiet>{t("trail.empty")}</Quiet>;

  return (
    <div>
      {state.data.map((trail) => (
        <Card key={trail.runId} trail={trail} />
      ))}
    </div>
  );
}
