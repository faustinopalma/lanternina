import { useState } from "react";

import { useApi } from "@/api/client";
import type { Decision, Proposal } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { useWords, type MessageKey } from "@/i18n";
import {
  exerciseChoices,
  exerciseQuestion,
  sheetExercises,
  sheetInstructions,
  sheetTitle,
  type Sheet,
} from "@/lib/sheet";
import { useLoad } from "@/lib/useLoad";

// Unknown kinds show their raw name rather than a missing-key placeholder: the panel is
// allowed to meet a kind this build has never heard of.
const KNOWN_KINDS = ["exercise", "routine_prompt", "feedback", "schedule", "print_layout"];

/* Everything here is rendered as text. This body was written by a model and reaches the
 * page as words, never as markup. */
function Body({ proposal }: { proposal: Proposal }) {
  if (!proposal.contentKind.endsWith("json")) return <p className="mb-2">{proposal.body}</p>;

  let sheet: Sheet;
  try {
    sheet = JSON.parse(proposal.body);
  } catch {
    return <p className="mb-2">{proposal.body}</p>;
  }

  return (
    <>
      <h3 className="mb-1 text-[1.05rem] font-semibold">{sheetTitle(sheet)}</h3>
      <p className="mb-2">{sheetInstructions(sheet)}</p>
      <ul className="mb-2.5 list-disc pl-5">
        {sheetExercises(sheet).map((entry, index) => (
          <li key={index} className="mb-1.5">
            {exerciseQuestion(entry)}
            <span className="block text-[0.92rem] text-quiet">
              {exerciseChoices(entry).join(" · ")}
            </span>
          </li>
        ))}
      </ul>
    </>
  );
}

function Card({ proposal, onDecided }: { proposal: Proposal; onDecided: () => void }) {
  const { t } = useWords();
  const api = useApi();
  const [deciding, setDeciding] = useState(false);
  const [failed, setFailed] = useState(false);

  async function decide(state: Decision) {
    setDeciding(true);
    setFailed(false);
    try {
      await api.decide(proposal.id, state);
      onDecided();
    } catch {
      setFailed(true);
      setDeciding(false);
    }
  }

  const kind = KNOWN_KINDS.includes(proposal.kind)
    ? t(`kind.${proposal.kind}` as MessageKey)
    : proposal.kind;

  return (
    <article className="mt-3.5 max-w-[42rem] rounded-control border border-edge bg-paper p-[18px] pb-4">
      <p className="text-[0.82rem] tracking-wider text-quiet uppercase">{kind}</p>
      <Body proposal={proposal} />
      <p className="text-[0.92rem] text-quiet">{proposal.rationale}</p>
      <div className="mt-3.5 flex flex-wrap gap-2.5">
        <Button variant="primary" size="small" disabled={deciding} onClick={() => decide("approved")}>
          {t("action.approve")}
        </Button>
        <Button size="small" disabled={deciding} onClick={() => decide("rejected")}>
          {t("action.refuse")}
        </Button>
      </div>
      {failed ? <Quiet className="mt-2.5">{t("proposals.decideFailed")}</Quiet> : null}
    </article>
  );
}

function Approved() {
  const { t } = useWords();
  const api = useApi();
  const [approved] = useLoad(() => api.approved(), []);
  const [themes] = useLoad(() => api.themes(), []);
  const [withdrawn, setWithdrawn] = useState<string[]>([]);
  const [failed, setFailed] = useState(false);

  if (approved.status !== "ready" || themes.status !== "ready") return null;

  const left = approved.data.filter((proposal) => !withdrawn.includes(proposal.id));

  return (
    <section className="mt-7 border-t border-edge pt-5">
      <h2 className="mb-2 text-[1.05rem] font-semibold">{t("proposals.approved")}</h2>
      {/* A fact, not a task. The reserve is what the house serves from when the cloud
          does not answer, so an empty one is worth being able to see — but nothing here
          asks the parent to fill it. */}
      <p className="text-quiet" aria-live="polite">
        {t("proposals.reserve", {
          activities: left.length,
          themes: themes.data.length,
        })}
      </p>
      <ul className="mt-3 flex max-w-[42rem] list-none flex-col gap-2 p-0">
        {left.map((proposal) => (
          <li
            key={proposal.id}
            className="flex flex-wrap items-center gap-x-3 gap-y-1.5 rounded-control border border-edge bg-paper px-3.5 py-2.5"
          >
            <span className="grow">{summary(proposal)}</span>
            <Button
              size="small"
              onClick={async () => {
                setFailed(false);
                try {
                  await api.decide(proposal.id, "withdrawn");
                  setWithdrawn((gone) => [...gone, proposal.id]);
                } catch {
                  setFailed(true);
                }
              }}
            >
              {t("action.withdraw")}
            </Button>
          </li>
        ))}
      </ul>
      {withdrawn.length > 0 ? (
        <p className="mt-2.5 text-quiet">{t("proposals.withdrawn")}</p>
      ) : null}
      {failed ? <Quiet className="mt-2.5">{t("proposals.withdrawFailed")}</Quiet> : null}
    </section>
  );
}

/** One line naming an approved item, so a parent can tell which one they are taking back
 *  without having the whole sheet unrolled in front of them again. */
function summary(proposal: Proposal): string {
  if (!proposal.contentKind.endsWith("json")) return proposal.body;
  try {
    return sheetTitle(JSON.parse(proposal.body));
  } catch {
    return proposal.body;
  }
}

/* The older half of approving, kept because the store and the route are still here and a
 * proposal that arrived would have to be decidable. Nothing on the hub submits one — no
 * timer, no service, only `tools/home_server.py propose` run by hand — so in a working
 * house this is empty, and empty it says nothing at all rather than occupying a page of
 * its own next to the one that is live. */
export function Proposals() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.proposals());
  const [decided, setDecided] = useState<string[]>([]);

  if (state.status !== "ready") return null;

  const waiting = state.data.filter((proposal) => !decided.includes(proposal.id));
  if (waiting.length === 0) return null;

  return (
    <div aria-live="polite" className="mt-6">
      <h3 className="mb-1.5 text-[1rem] font-semibold tracking-tight">
        {t("proposals.title")}
      </h3>
      <Quiet className="mb-2">{t("proposals.note")}</Quiet>
      {waiting.map((proposal) => (
        <Card
          key={proposal.id}
          proposal={proposal}
          onDecided={() => setDecided((seen) => [...seen, proposal.id])}
        />
      ))}
      <Approved />
    </div>
  );
}
