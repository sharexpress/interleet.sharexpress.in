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

import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { Card } from "@/components/ui/card";
import { DifficultyPill } from "@/components/domain/Tags";
import { Clock, Sparkles, Users, Lock, Monitor, Server, Terminal, Network, Database, Layers, ArrowRight } from "lucide-react";
import UpgradeModal from "@/components/UpgradeModal";

const DOMAIN_THEMES = {
  Frontend: {
    icon: Monitor,
    color: "from-pink-500/20 to-rose-500/20",
    border: "hover:border-pink-500/30",
    text: "text-pink-400 bg-pink-500/10",
    glow: "shadow-pink-500/10"
  },
  Backend: {
    icon: Server,
    color: "from-blue-500/20 to-indigo-500/20",
    border: "hover:border-blue-500/30",
    text: "text-blue-400 bg-blue-500/10",
    glow: "shadow-blue-500/10"
  },
  DevOps: {
    icon: Terminal,
    color: "from-amber-500/20 to-orange-500/20",
    border: "hover:border-amber-500/30",
    text: "text-amber-400 bg-amber-500/10",
    glow: "shadow-amber-500/10"
  },
  APIs: {
    icon: Network,
    color: "from-purple-500/20 to-fuchsia-500/20",
    border: "hover:border-purple-500/30",
    text: "text-purple-400 bg-purple-500/10",
    glow: "shadow-purple-500/10"
  },
  Databases: {
    icon: Database,
    color: "from-emerald-500/20 to-teal-500/20",
    border: "hover:border-emerald-500/30",
    text: "text-emerald-400 bg-emerald-500/10",
    glow: "shadow-emerald-500/10"
  },
  Fullstack: {
    icon: Layers,
    color: "from-cyan-500/20 to-blue-500/20",
    border: "hover:border-cyan-500/30",
    text: "text-cyan-400 bg-cyan-500/10",
    glow: "shadow-cyan-500/10"
  }
};

export function ChallengeCard({ c }) {
  const user = useSelector((state) => state.user?.user);
  const isLocked = false;

  const domain = c.domain || "Backend";
  const theme = DOMAIN_THEMES[domain] || DOMAIN_THEMES.Backend;
  const DomainIcon = theme.icon;

  const isSolved = (user?.solved_problems || user?.solved_challenges || []).includes(c.slug) || c.user_status === "solved";
  const isAttempted = !isSolved && ((user?.attempted_problems || []).includes(c.slug) || c.user_status === "attempted");

  const cardContent = (
    <Card className="relative overflow-hidden h-full flex flex-col justify-between border border-border bg-card rounded-lg p-5 transition-colors duration-150 hover:border-primary/60 group cursor-pointer">
      <div>
        {/* Top Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded bg-muted/60 text-primary border border-border/60">
              <DomainIcon className="h-3.5 w-3.5" />
            </span>
            <span className="font-mono text-xs text-muted-foreground">
              {domain}
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            {isSolved && (
              <span className="inline-flex items-center gap-1 rounded bg-emerald-500/10 border border-emerald-500/30 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-400">
                <Sparkles className="h-2.5 w-2.5" /> Solved
              </span>
            )}
            {isAttempted && (
              <span className="inline-flex items-center gap-1 rounded bg-amber-500/10 border border-amber-500/30 px-1.5 py-0.5 text-[10px] font-semibold text-amber-400">
                <Clock className="h-2.5 w-2.5" /> Attempted
              </span>
            )}
            {c.is_premium && (
              <span className="inline-flex items-center gap-1 rounded bg-amber-500/10 border border-amber-500/30 px-1.5 py-0.5 text-[10px] font-bold text-amber-400">
                <Lock className="h-2.5 w-2.5" /> Pro
              </span>
            )}
            <DifficultyPill d={c.difficulty} />
          </div>
        </div>

        {/* Title & Summary */}
        <h3 className="text-sm font-semibold tracking-tight text-foreground group-hover:text-primary transition-colors line-clamp-1 mb-1.5">
          {c.title || "Untitled Challenge"}
        </h3>
        <p className="line-clamp-2 text-xs text-muted-foreground leading-relaxed mb-3">
          {c.summary || "No description provided."}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-1 mb-4">
          {(c.tags || []).slice(0, 3).map((t) => (
            <span
              key={t}
              className="rounded border border-border/50 bg-muted/40 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground"
            >
              #{t}
            </span>
          ))}
        </div>
      </div>

      {/* Footer Info */}
      <div className="flex items-center justify-between border-t border-border/50 pt-3 mt-auto">
        <div className="flex gap-3 text-xs font-medium text-muted-foreground">
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            {c.minutes || c.estimated_time_minutes || 0}m
          </span>
          <span className="flex items-center gap-1">
            <Sparkles className="h-3 w-3 text-primary" />
            {c.xp || c.xp_reward || 0} XP
          </span>
          <span className="flex items-center gap-1">
            <Users className="h-3 w-3" />
            {c.completion || 0}%
          </span>
        </div>

        {/* Open Indicator */}
        <span className="text-muted-foreground group-hover:text-primary transition-colors">
          <ArrowRight className="h-3.5 w-3.5" />
        </span>
      </div>
    </Card>
  );

  if (isLocked) {
    return (
      <UpgradeModal
        trigger={
          <div className="group block h-full">
            {cardContent}
          </div>
        }
      />
    );
  }

  return (
    <Link to={`/app/challenges/${c.slug}`} className="group block h-full">
      {cardContent}
    </Link>
  );
}
