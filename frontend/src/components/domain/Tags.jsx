import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";


const difficultyStyles = {
  Easy: "border-success/30 bg-success/10 text-success",
  Medium: "border-warning/30 bg-warning/10 text-warning",
  Hard: "border-destructive/30 bg-destructive/10 text-destructive",
  Expert: "border-chart-4/40 bg-chart-4/10 text-chart-4"
};

const domainColors = {
  Frontend: "text-chart-1",
  Backend: "text-chart-2",
  DevOps: "text-chart-3",
  APIs: "text-chart-4",
  Databases: "text-chart-5",
  "System Design": "text-primary"
};

export function DifficultyPill({ d, className }) {
  return (
    <Badge
      variant="outline"
      className={cn(
        "rounded-full font-mono text-[10px] uppercase tracking-wider",
        difficultyStyles[d],
        className
      )}>
      
      {d}
    </Badge>);

}

export function DomainTag({ d }) {
  return (
    <span className={cn("font-mono text-[11px] uppercase tracking-widest", domainColors[d])}>
      {d}
    </span>);

}