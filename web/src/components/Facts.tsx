import { Fragment, type ReactNode } from "react";

import { cn } from "@/lib/utils";

export interface Fact {
  label: string;
  value: ReactNode;
}

/** Label and value on one line, as a pair is read. */
export function Facts({ rows, className }: { rows: Fact[]; className?: string }) {
  return (
    <dl
      className={cn(
        "mt-4 grid grid-cols-[max-content_minmax(0,1fr)] gap-x-5 gap-y-2",
        className,
      )}
    >
      {rows.map((row) => (
        <Fragment key={row.label}>
          <dt className="self-baseline text-[0.92rem] text-quiet">{row.label}</dt>
          <dd className="m-0 [overflow-wrap:anywhere]">{row.value}</dd>
        </Fragment>
      ))}
    </dl>
  );
}
