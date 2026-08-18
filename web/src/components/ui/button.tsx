import { cva, type VariantProps } from "class-variance-authority";
import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

/* One filled button per view, so the next step is never ambiguous; everything else is
   outlined. Minimum height 44px: this panel is used on a phone, one-handed. */
const button = cva(
  "inline-flex items-center justify-center gap-2 rounded-[--radius-control] font-sans " +
    "text-base whitespace-nowrap cursor-pointer transition-[color,background-color,border-color] " +
    "disabled:cursor-default disabled:opacity-50",
  {
    variants: {
      variant: {
        primary:
          "bg-accent border border-accent text-accent-ink font-semibold hover:brightness-105",
        outline:
          "bg-card border border-edge text-ink hover:border-accent hover:text-accent " +
          "disabled:hover:border-edge disabled:hover:text-ink",
        ghost: "border-0 bg-transparent text-quiet hover:bg-paper hover:text-ink",
      },
      size: {
        default: "min-h-11 px-[18px] py-2.5",
        small: "min-h-9.5 px-3.5 py-1.5 text-[0.95rem]",
      },
    },
    defaultVariants: { variant: "outline", size: "default" },
  },
);

export type ButtonProps = ComponentProps<"button"> & VariantProps<typeof button>;

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      data-slot="button"
      className={cn(button({ variant, size }), className)}
      {...props}
    />
  );
}
