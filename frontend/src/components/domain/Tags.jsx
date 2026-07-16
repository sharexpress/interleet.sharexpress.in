/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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