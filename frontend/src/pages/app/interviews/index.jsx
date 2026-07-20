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

import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Bot, Clock, ArrowRight, Mic, LayoutGrid, List as ListIcon, Lock,
  Server, Database, Cpu, Layout, Code2, Layers, Network, Terminal,
  Globe, Zap, Sparkles, Boxes, ShieldCheck, CheckCircle2, TrendingUp,
  Award, Search, Filter, Compass, Workflow, Play
} from "lucide-react";
import { cn } from "@/lib/utils";
import { API } from "@/api/api";
import UpgradeModal from "@/components/UpgradeModal";

/* ─── Global In-Memory Cache for AI Interviews ─── */
let cachedInterviewPresets = null;
let cachedInterviewHistory = null;

const ROLE_ICONS = {
  "Senior Backend Engineer": { icon: Server, color: "text-amber-400 bg-amber-950/40 border-amber-800/40", category: "Backend" },
  "Frontend Architect": { icon: Layout, color: "text-sky-400 bg-sky-950/40 border-sky-800/40", category: "Frontend" },
  "System Design (L5)": { icon: Network, color: "text-purple-400 bg-purple-950/40 border-purple-800/40", category: "System Design" },
  "DevOps Lead": { icon: Terminal, color: "text-emerald-400 bg-emerald-950/40 border-emerald-800/40", category: "DevOps" },
  "API Design": { icon: Globe, color: "text-blue-400 bg-blue-950/40 border-blue-800/40", category: "Backend" },
  "Full-Stack Generalist": { icon: Sparkles, color: "text-primary bg-primary/10 border-primary/30", category: "Fullstack" },
  "MERN Stack Developer": { icon: Boxes, color: "text-emerald-400 bg-emerald-950/40 border-emerald-800/40", category: "Fullstack" },
};

function getRoleMeta(title) {
  return ROLE_ICONS[title] || { icon: Bot, color: "text-primary bg-primary/10 border-primary/30", category: "All" };
}

function InterviewsPage() {
  const navigate = useNavigate();
  const [view, setView] = useState("grid");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const user = useSelector((state) => state.user?.user);
  const [upgradeOpen, setUpgradeOpen] = useState(false);
  const [interviewHistory, setInterviewHistory] = useState(cachedInterviewHistory || []);
  const [loadingHistory, setLoadingHistory] = useState(!cachedInterviewHistory);
  const [roles, setRoles] = useState(cachedInterviewPresets || []);
  const [loadingRoles, setLoadingRoles] = useState(!cachedInterviewPresets);

  useEffect(() => {
    let isMounted = true;
    const fetchPresets = async () => {
      if (cachedInterviewPresets) {
        setRoles(cachedInterviewPresets);
        setLoadingRoles(false);
      }
      try {
        const response = await API.get("/api/v1/interviews/presets");
        if (isMounted && response.data?.presets) {
          const mapped = response.data.presets.map((p) => ({
            t: p.title || p.role_title,
            d: p.description,
            m: p.duration_minutes || 45,
          }));
          cachedInterviewPresets = mapped;
          setRoles(mapped);
          setLoadingRoles(false);
        }
      } catch (err) {
        console.error("Failed to load interview presets, falling back to defaults.", err);
        if (isMounted) {
          const fallback = cachedInterviewPresets || [
            { t: "Senior Backend Engineer", d: "Concurrency, services, databases, scaling.", m: 45 },
            { t: "Frontend Architect", d: "Performance, state, design systems, accessibility.", m: 45 },
            { t: "System Design (L5)", d: "End-to-end architecture for production systems.", m: 60 },
            { t: "DevOps Lead", d: "CI/CD, infrastructure, reliability, on-call.", m: 45 },
            { t: "API Design", d: "REST, contracts, versioning, evolvability.", m: 30 },
            { t: "Full-Stack Generalist", d: "Mixed scenarios across the stack.", m: 50 },
            { t: "MERN Stack Developer", d: "MongoDB, Express, React, Node.js integration.", m: 45 }
          ];
          cachedInterviewPresets = fallback;
          setRoles(fallback);
          setLoadingRoles(false);
        }
      }
    };
    const fetchHistory = async () => {
      if (cachedInterviewHistory) {
        setInterviewHistory(cachedInterviewHistory);
        setLoadingHistory(false);
      }
      try {
        const response = await API.get("/interview/reports/recent");
        if (isMounted) {
          cachedInterviewHistory = response.data;
          setInterviewHistory(response.data);
          setLoadingHistory(false);
        }
      } catch (err) {
        console.error("Failed to load interview history, falling back to empty.", err);
        if (isMounted) {
          const fallback = cachedInterviewHistory || [];
          cachedInterviewHistory = fallback;
          setInterviewHistory(fallback);
          setLoadingHistory(false);
        }
      }
    };
    fetchPresets();
    fetchHistory();
    return () => { isMounted = false; };
  }, []);

  const handleRandomInterview = (e) => {
    if (e) e.preventDefault();
    if (roles.length === 0) return;
    const randomRole = roles[Math.floor(Math.random() * roles.length)];
    const difficulties = ["Easy", "Intermediate", "Hard"];
    const randomDiff = difficulties[Math.floor(Math.random() * difficulties.length)];
    navigate(`/app/interviews/setup?role=${encodeURIComponent(randomRole.t)}&difficulty=${encodeURIComponent(randomDiff)}`);
  };

  const categories = ["All", "Backend", "Frontend", "System Design", "DevOps", "Fullstack"];

  const filteredRoles = roles.filter((r) => {
    const meta = getRoleMeta(r.t);
    const matchesCategory = selectedCategory === "All" || meta.category === selectedCategory;
    const matchesSearch = r.t.toLowerCase().includes(searchQuery.toLowerCase()) || r.d.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <AppShell>
      <PageHeader
        title="AI Mock Interviews"
        description="Practice technical conversations with Sara AI. Dynamic decision trees & rubric-graded feedback."
        actions={
          <Button onClick={handleRandomInterview} className="cursor-pointer bg-primary hover:bg-orange-600 shadow-[0_0_20px_rgba(255,101,0,0.3)]">
            <Mic className="mr-2 h-4 w-4" /> Start a live session
          </Button>
        } 
      />
      
      <div className="space-y-8 px-4 py-6 md:px-8">

        {/* Hero Card Banner */}
        <div className="relative overflow-hidden rounded-2xl border border-primary/20 bg-gradient-to-r from-zinc-950 via-zinc-900 to-zinc-950 p-6 md:p-8 shadow-[0_0_50px_rgba(255,101,0,0.1)]">
          <div className="absolute right-0 top-0 -mr-16 -mt-16 h-64 w-64 rounded-full bg-primary/10 blur-3xl pointer-events-none" />
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-xl">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="border-primary/40 bg-primary/10 text-primary font-mono text-xs">
                  ✨ Dynamic Decision Tree Engine v2.0
                </Badge>
              </div>
              <h1 className="text-xl md:text-2xl font-bold tracking-tight text-zinc-100">
                Master Technical Interviews with Sara AI
              </h1>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Start with a self-introduction to build your personalized decision tree. Questions adapt dynamically from 2 to 20 bounds based on your response accuracy.
              </p>
            </div>
            <div className="flex items-center gap-3 shrink-0">
              <div className="flex flex-col items-center justify-center px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-900/60 text-center min-w-[100px]">
                <span className="text-lg font-bold text-primary">2-20</span>
                <span className="text-[10px] text-zinc-500 font-mono uppercase">Dynamic Qs</span>
              </div>
              <div className="flex flex-col items-center justify-center px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-900/60 text-center min-w-[100px]">
                <span className="text-lg font-bold text-emerald-400">100%</span>
                <span className="text-[10px] text-zinc-500 font-mono uppercase">Adaptive</span>
              </div>
            </div>
          </div>
        </div>

        <section className="space-y-4">
          {/* Controls Bar: Category Filters, Search, Grid/List toggle */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-900 pb-4">
            {/* Category Pills */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 no-scrollbar">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                    selectedCategory === cat
                      ? "bg-primary/15 border border-primary/50 text-primary"
                      : "bg-zinc-900/40 border border-zinc-800 text-zinc-400 hover:text-zinc-200 hover:border-zinc-700"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-3">
              {/* Search input */}
              <div className="relative flex-1 md:w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-zinc-500" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter interview roles..."
                  className="w-full rounded-lg border border-zinc-800 bg-zinc-900/60 pl-9 pr-3 py-1.5 text-xs text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:ring-1 focus:ring-primary/50"
                />
              </div>

              {/* Grid / List switcher */}
              <div className="flex rounded-lg border border-zinc-800 p-0.5 bg-zinc-950">
                <button
                  onClick={() => setView("grid")}
                  className={cn(
                    "rounded-md p-1.5 cursor-pointer transition-colors",
                    view === "grid" ? "bg-primary/20 text-primary" : "text-zinc-500 hover:text-zinc-300"
                  )}
                  aria-label="Grid view"
                >
                  <LayoutGrid className="h-3.5 w-3.5" />
                </button>
                <button
                  onClick={() => setView("list")}
                  className={cn(
                    "rounded-md p-1.5 cursor-pointer transition-colors",
                    view === "list" ? "bg-primary/20 text-primary" : "text-zinc-500 hover:text-zinc-300"
                  )}
                  aria-label="List view"
                >
                  <ListIcon className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          </div>

          {/* Conditional Role Grid / List */}
          {loadingRoles ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 animate-pulse">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="h-[200px] rounded-xl border border-border bg-card/30 p-5 space-y-4" />
              ))}
            </div>
          ) : view === "grid" ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {filteredRoles.map((r) => {
                const meta = getRoleMeta(r.t);
                const IconComponent = meta.icon;

                return (
                  <Card key={r.t} className="group relative border-border bg-card/80 p-5 transition-all duration-300 hover:border-primary/50 hover:shadow-[0_0_25px_rgba(255,101,0,0.12)] hover:-translate-y-0.5">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <span className={`flex h-10 w-10 items-center justify-center rounded-xl border ${meta.color} transition-transform group-hover:scale-105`}>
                          <IconComponent className="h-5 w-5" />
                        </span>
                        <div>
                          <h3 className="text-sm font-bold text-zinc-100 flex items-center gap-1.5">
                            <span>{r.t}</span>
                          </h3>
                          <span className="text-[10px] font-mono text-zinc-500 uppercase">{meta.category}</span>
                        </div>
                      </div>
                    </div>

                    <p className="mt-3 text-xs text-muted-foreground leading-relaxed min-h-[36px] line-clamp-2">{r.d}</p>

                    <div className="mt-4">
                      <p className="mb-2 font-mono text-[10px] uppercase tracking-widest text-zinc-500 font-semibold">Select Difficulty Tier</p>
                      <div className="grid grid-cols-3 gap-1.5">
                        {[
                          { l: "Easy", c: "text-emerald-400 border-emerald-800/40 hover:bg-emerald-950/40 bg-emerald-950/20" },
                          { l: "Intermediate", c: "text-amber-400 border-amber-800/40 hover:bg-amber-950/40 bg-amber-950/20" },
                          { l: "Hard", c: "text-rose-400 border-rose-800/40 hover:bg-rose-950/40 bg-rose-950/20" }
                        ].map((d) => (
                          <button
                            key={d.l}
                            type="button"
                            onClick={() => {
                              navigate(`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=${encodeURIComponent(d.l)}`);
                            }}
                            className={`rounded-lg border px-2 py-1.5 text-center text-[11px] font-medium transition-all cursor-pointer ${d.c}`}
                          >
                            {d.l}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="mt-4 flex items-center justify-between border-t border-zinc-900 pt-3 text-xs text-muted-foreground">
                      <span className="inline-flex items-center gap-1 text-zinc-400 font-mono text-[11px]">
                        <Clock className="h-3.5 w-3.5 text-zinc-500" /> ~{r.m}m session
                      </span>
                      <button
                        type="button"
                        onClick={() => {
                          navigate(`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=Intermediate`);
                        }}
                        className="inline-flex items-center text-primary hover:text-orange-400 font-semibold cursor-pointer text-xs group-hover:translate-x-0.5 transition-transform"
                      >
                        Start Session <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                      </button>
                    </div>
                  </Card>
                );
              })}
            </div>
          ) : (
            <Card className="overflow-hidden border-border bg-card p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-sm min-w-[600px]">
                  <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                    <tr>
                      <th className="px-4 py-3.5 font-mono uppercase tracking-wider">Role</th>
                      <th className="px-4 py-3.5 font-mono uppercase tracking-wider">Description</th>
                      <th className="px-4 py-3.5 font-mono uppercase tracking-wider">Duration</th>
                      <th className="px-4 py-3.5 font-mono uppercase tracking-wider">Difficulty Tiers</th>
                      <th className="px-4 py-3.5 text-right font-mono uppercase tracking-wider">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredRoles.map((r) => {
                      const meta = getRoleMeta(r.t);
                      const IconComponent = meta.icon;
                      return (
                        <tr key={r.t} className="border-t border-border hover:bg-accent/10 transition-colors">
                          <td className="px-4 py-4 font-medium flex items-center gap-3">
                            <span className={`flex h-8 w-8 items-center justify-center rounded-lg border ${meta.color}`}>
                              <IconComponent className="h-4 w-4" />
                            </span>
                            <div>
                              <p className="text-sm font-bold text-zinc-100">{r.t}</p>
                              <span className="text-[10px] font-mono text-zinc-500">{meta.category}</span>
                            </div>
                          </td>
                          <td className="px-4 py-4 text-muted-foreground text-xs">{r.d}</td>
                          <td className="px-4 py-4 font-mono text-xs text-zinc-400">
                            <span className="inline-flex items-center gap-1">
                              <Clock className="h-3.5 w-3.5 text-zinc-500" /> {r.m}m
                            </span>
                          </td>
                          <td className="px-4 py-4">
                            <div className="flex gap-2">
                              {[
                                { l: "Easy", c: "text-emerald-400 border-emerald-800/40 hover:bg-emerald-950/40 bg-emerald-950/20" },
                                { l: "Intermediate", c: "text-amber-400 border-amber-800/40 hover:bg-amber-950/40 bg-amber-950/20" },
                                { l: "Hard", c: "text-rose-400 border-rose-800/40 hover:bg-rose-950/40 bg-rose-950/20" }
                              ].map((d) => (
                                <button
                                  key={d.l}
                                  type="button"
                                  onClick={() => {
                                    navigate(`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=${encodeURIComponent(d.l)}`);
                                  }}
                                  className={`rounded-md border px-2 py-1 text-[10px] font-medium transition-colors cursor-pointer ${d.c}`}
                                >
                                  {d.l}
                                </button>
                              ))}
                            </div>
                          </td>
                          <td className="px-4 py-4 text-right">
                            <button
                              type="button"
                              onClick={() => {
                                navigate(`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=Intermediate`);
                              }}
                              className="inline-flex items-center text-xs text-primary hover:underline font-semibold cursor-pointer"
                            >
                              Start <ArrowRight className="ml-1 h-3.5 w-3.5" />
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </Card>
          )}
        </section>

        {/* Recent Sessions */}
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-zinc-100 flex items-center gap-2">
              <Clock className="h-4 w-4 text-primary" /> Recent Practice Sessions
            </h2>
          </div>

          <Card className="overflow-hidden border-border bg-card p-0">
            {loadingHistory ? (
              <div className="p-6 space-y-3 animate-pulse">
                <div className="h-5 w-full rounded bg-zinc-800/40" />
                <div className="h-5 w-5/6 rounded bg-zinc-800/20" />
                <div className="h-5 w-4/5 rounded bg-zinc-800/20" />
              </div>
            ) : interviewHistory.length === 0 ? (
              <div className="flex flex-col items-center justify-center p-8 text-center text-zinc-500 space-y-2">
                <Award className="h-8 w-8 text-zinc-600" />
                <p className="text-xs">No practice sessions completed yet.</p>
                <p className="text-[11px] text-zinc-600">Select any role above to begin your first AI mock interview.</p>
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead className="bg-background/60 text-left text-xs text-muted-foreground border-b border-border">
                  <tr>
                    <th className="px-4 py-3 font-mono uppercase tracking-wider">Role</th>
                    <th className="px-4 py-3 font-mono uppercase tracking-wider">Score</th>
                    <th className="px-4 py-3 font-mono uppercase tracking-wider">Duration</th>
                    <th className="px-4 py-3 font-mono uppercase tracking-wider">When</th>
                    <th className="px-4 py-3 text-right font-mono uppercase tracking-wider">Report</th>
                  </tr>
                </thead>
                <tbody>
                  {interviewHistory.map((iv) => {
                    const scoreVal = parseInt(iv.score || "0", 10);
                    const scoreBadgeClass = scoreVal >= 80 ? "border-emerald-800/40 bg-emerald-950/30 text-emerald-300"
                      : scoreVal >= 60 ? "border-amber-800/40 bg-amber-950/30 text-amber-300"
                      : "border-rose-800/40 bg-rose-950/30 text-rose-300";

                    return (
                      <tr key={iv.id} className="border-t border-border/60 hover:bg-accent/10 transition-colors">
                        <td className="px-4 py-3 font-medium text-zinc-200">{iv.role}</td>
                        <td className="px-4 py-3">
                          <Badge variant="outline" className={`font-mono text-xs ${scoreBadgeClass}`}>
                            {iv.score}/100
                          </Badge>
                        </td>
                        <td className="px-4 py-3 font-mono text-xs text-zinc-400">{iv.duration}m</td>
                        <td className="px-4 py-3 text-xs text-muted-foreground">{iv.when}</td>
                        <td className="px-4 py-3 text-right">
                          <Link
                            to={`/app/interviews/${iv.id}/report`}
                            className="inline-flex items-center text-xs text-primary hover:underline font-medium"
                          >
                            View report <ArrowRight className="ml-1 h-3 w-3" />
                          </Link>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </Card>
        </section>
      </div>
      <UpgradeModal open={upgradeOpen} onOpenChange={setUpgradeOpen} />
    </AppShell>
  );
}

export default InterviewsPage;
