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

export function Proposals() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.proposals());
  const [decided, setDecided] = useState<string[]>([]);

  if (state.status === "loading") return <Quiet>{t("proposals.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("proposals.unreadable")}</Quiet>;

  const waiting = state.data.filter((proposal) => !decided.includes(proposal.id));
  if (waiting.length === 0) return <Quiet>{t("proposals.empty")}</Quiet>;

  return (
    <div aria-live="polite">
      {waiting.map((proposal) => (
        <Card
          key={proposal.id}
          proposal={proposal}
          onDecided={() => setDecided((seen) => [...seen, proposal.id])}
        />
      ))}
    </div>
  );
}
