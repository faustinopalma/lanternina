import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

/* One appearance for every control the parent types into or picks from. The classic panel
   had four near-copies of these rules, which is how they drift apart. */
const control =
  "min-h-11 rounded-control border border-edge bg-card px-3 py-2 " +
  "font-sans text-base text-ink";

export function Input({ className, ...props }: ComponentProps<"input">) {
  return <input data-slot="input" className={cn(control, className)} {...props} />;
}

export function Textarea({ className, ...props }: ComponentProps<"textarea">) {
  return (
    <textarea
      data-slot="textarea"
      className={cn(control, "min-h-0 resize-y leading-relaxed", className)}
      {...props}
    />
  );
}

/* A native select, not a listbox built out of divs: on a phone it opens the system picker,
   and it is the one control that already works with assistive technology everywhere. The
   cost is that the open list cannot be styled. */
export function Select({ className, ...props }: ComponentProps<"select">) {
  return <select data-slot="select" className={cn(control, className)} {...props} />;
}

export function Label({ className, ...props }: ComponentProps<"label">) {
  return <label data-slot="label" className={cn("text-quiet", className)} {...props} />;
}
