import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

export function Logo({ className, compact = false }) {
  return (
    <Link to="/" className={cn("flex items-center gap-2", className)}>
      <span className="relative inline-flex h-7 w-7 items-center justify-center rounded-md border border-border bg-gradient-to-br from-primary/30 to-primary/10">
        <span className="font-mono text-[11px] font-bold text-primary">{"</>"}</span>
      </span>
      {!compact &&
      <span className="font-semibold tracking-tight">
          Interleet
          <span className="ml-1 align-top font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
            beta
          </span>
        </span>
      }
    </Link>);

}