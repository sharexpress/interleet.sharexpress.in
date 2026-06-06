import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

import interleetLogo from "@/assets/logo.png";

export function Logo({ className, compact = false }) {
  return (
    <Link to="/" className={cn("flex items-center gap-3", className)}>
      <img
        src={interleetLogo}
        alt="Interleet"
        className={cn(
          "object-contain transition-all duration-200",
          compact ? "h-10 w-10" : "h-25 w-auto",
        )}
      />

      {!compact && <span className="sr-only">Interleet</span>}
    </Link>
  );
}
