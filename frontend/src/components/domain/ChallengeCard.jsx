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

  const cardContent = (
    <Card className={`relative overflow-hidden h-full flex flex-col justify-between border border-zinc-800 bg-zinc-950/60 backdrop-blur-md p-6 transition-all duration-300 hover:-translate-y-1 ${theme.border} hover:shadow-lg ${theme.glow} group cursor-pointer`}>
      {/* Background Radial Glow on Hover */}
      <div className={`absolute -right-16 -top-16 w-32 h-32 rounded-full bg-gradient-to-br ${theme.color} blur-3xl opacity-50 transition-opacity duration-300 group-hover:opacity-100`} />
      
      <div>
        {/* Top Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className={`p-1.5 rounded-lg ${theme.text}`}>
              <DomainIcon className="h-4 w-4" />
            </span>
            <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
              {domain}
            </span>
          </div>
          <div className="flex items-center gap-2">
            {c.is_premium && (
              <span className="inline-flex items-center gap-1 rounded-full bg-gradient-to-r from-amber-500/20 to-orange-500/20 px-2.5 py-0.5 text-[10px] font-bold text-amber-400 border border-amber-500/30 shadow-sm shadow-orange-500/5">
                <Lock className="h-2.5 w-2.5" /> PRO
              </span>
            )}
            <DifficultyPill d={c.difficulty} />
          </div>
        </div>

        {/* Title & Summary */}
        <h3 className="text-lg font-semibold tracking-tight text-zinc-100 group-hover:text-white transition-colors duration-200 line-clamp-1 mb-2">
          {c.title || "Untitled Challenge"}
        </h3>
        <p className="line-clamp-2 text-sm text-zinc-400 leading-relaxed mb-4">
          {c.summary || "No description provided."}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 mb-6">
          {(c.tags || []).slice(0, 3).map((t) => (
            <span
              key={t}
              className="rounded-md border border-zinc-800 bg-zinc-900/50 px-2 py-0.5 font-mono text-[10px] text-zinc-400 group-hover:border-zinc-700 transition-colors"
            >
              #{t}
            </span>
          ))}
        </div>
      </div>

      {/* Footer Info */}
      <div className="flex items-center justify-between border-t border-zinc-900 pt-4 mt-auto">
        <div className="flex gap-4 text-xs font-medium text-zinc-500">
          <span className="flex items-center gap-1 hover:text-zinc-300 transition-colors">
            <Clock className="h-3.5 w-3.5 text-zinc-600" />
            {c.minutes || c.estimated_time_minutes || 0}m
          </span>
          <span className="flex items-center gap-1 hover:text-zinc-300 transition-colors">
            <Sparkles className="h-3.5 w-3.5 text-amber-500/70" />
            {c.xp || c.xp_reward || 0} XP
          </span>
          <span className="flex items-center gap-1 hover:text-zinc-300 transition-colors">
            <Users className="h-3.5 w-3.5 text-zinc-600" />
            {c.completion || 0}%
          </span>
        </div>
        
        {/* Play Action Indicator */}
        <span className={`p-1.5 rounded-full ${theme.text} opacity-0 group-hover:opacity-100 transition-opacity duration-300 transform translate-x-2 group-hover:translate-x-0`}>
          <ArrowRight className="h-4 w-4" />
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
