import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

export function Card({ className, ...props }: ComponentProps<"section">) {
  return (
    <section
      data-slot="card"
      className={cn(
        "rounded-panel border border-edge bg-card p-[26px] pb-7 shadow-card",
        className,
      )}
      {...props}
    />
  );
}

export function CardTitle({ className, ...props }: ComponentProps<"h2">) {
  return (
    <h2
      data-slot="card-title"
      className={cn("mb-2.5 text-[1.3rem] font-semibold tracking-tight", className)}
      {...props}
    />
  );
}

/** The muted voice the panel uses for everything that is context rather than content. */
export function Quiet({ className, ...props }: ComponentProps<"p">) {
  return <p data-slot="quiet" className={cn("max-w-[34rem] text-quiet", className)} {...props} />;
}
