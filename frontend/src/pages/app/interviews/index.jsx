import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bot, Clock, ArrowRight, Mic, LayoutGrid, List as ListIcon } from "lucide-react";
import { interviewHistory } from "@/lib/mock";
import { cn } from "@/lib/utils";

const roles = [
  { t: "Senior Backend Engineer", d: "Concurrency, services, databases, scaling.", m: 45 },
  { t: "Frontend Architect", d: "Performance, state, design systems, accessibility.", m: 45 },
  { t: "System Design (L5)", d: "End-to-end architecture for production systems.", m: 60 },
  { t: "DevOps Lead", d: "CI/CD, infrastructure, reliability, on-call.", m: 45 },
  { t: "API Design", d: "REST, contracts, versioning, evolvability.", m: 30 },
  { t: "Full-Stack Generalist", d: "Mixed scenarios across the stack.", m: 50 }
];

function InterviewsPage() {
  const navigate = useNavigate();
  const [view, setView] = useState("grid");

  const handleRandomInterview = (e) => {
    e.preventDefault();
    const randomRole = roles[Math.floor(Math.random() * roles.length)];
    const difficulties = ["Easy", "Intermediate", "Hard"];
    const randomDiff = difficulties[Math.floor(Math.random() * difficulties.length)];
    navigate(`/app/interviews/setup?role=${encodeURIComponent(randomRole.t)}&difficulty=${encodeURIComponent(randomDiff)}`);
  };

  return (
    <AppShell>
      <PageHeader
        title="AI Mock Interviews"
        description="Practice the conversation. Get rubric-graded feedback after every session."
        actions={
          <Button onClick={handleRandomInterview} className="cursor-pointer">
            <Mic className="mr-1.5 h-4 w-4" /> Start a live session
          </Button>
        } 
      />
      
      <div className="space-y-8 px-4 py-6 md:px-8">
        <section>
          {/* Section Header with grid/list toggler */}
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-sm font-semibold">Choose a role</h2>
            <div className="flex rounded-md border border-border p-0.5 bg-zinc-950/60">
              <button
                onClick={() => setView("grid")}
                className={cn(
                  "rounded p-1 cursor-pointer transition-colors",
                  view === "grid" ? "bg-accent text-white" : "text-muted-foreground hover:text-zinc-300"
                )}
                aria-label="Grid view"
              >
                <LayoutGrid className="h-3.5 w-3.5" />
              </button>
              <button
                onClick={() => setView("list")}
                className={cn(
                  "rounded p-1 cursor-pointer transition-colors",
                  view === "list" ? "bg-accent text-white" : "text-muted-foreground hover:text-zinc-300"
                )}
                aria-label="List view"
              >
                <ListIcon className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          {/* Conditional View Rendering */}
          {view === "grid" ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {roles.map((r) => (
                <Card key={r.t} className="group border-border bg-card p-5 transition-colors hover:border-primary/40">
                  <div className="flex items-center gap-3">
                    <span className="flex h-9 w-9 items-center justify-center rounded-md border border-border bg-background">
                      <Bot className="h-4 w-4 text-primary" />
                    </span>
                    <h3 className="text-sm font-semibold">{r.t}</h3>
                  </div>
                  <p className="mt-3 text-sm text-muted-foreground">{r.d}</p>

                  <div className="mt-4">
                    <p className="mb-2 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">Difficulty</p>
                    <div className="grid grid-cols-3 gap-1.5">
                      {[
                        { l: "Easy", c: "text-success border-success/30 hover:bg-success/10 bg-success/5" },
                        { l: "Intermediate", c: "text-warning border-warning/30 hover:bg-warning/10 bg-warning/5" },
                        { l: "Hard", c: "text-destructive border-destructive/30 hover:bg-destructive/10 bg-destructive/5" }
                      ].map((d) => (
                        <Link
                          key={d.l}
                          to={`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=${encodeURIComponent(d.l)}`}
                          className={`rounded-md border px-2 py-1.5 text-center text-[11px] font-medium transition-colors ${d.c}`}
                        >
                          {d.l}
                        </Link>
                      ))}
                    </div>
                  </div>

                  <div className="mt-4 flex items-center justify-between border-t border-border pt-3 text-xs text-muted-foreground">
                    <span className="inline-flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5" />{r.m}m
                    </span>
                    <Link 
                      to={`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=Intermediate`} 
                      className="inline-flex items-center text-primary hover:underline"
                    >
                      Start <ArrowRight className="ml-1 h-3 w-3" />
                    </Link>
                  </div>
                </Card>
              ))}
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
                    {roles.map((r) => (
                      <tr key={r.t} className="border-t border-border hover:bg-accent/10 transition-colors">
                        <td className="px-4 py-4 font-medium flex items-center gap-3">
                          <span className="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-background">
                            <Bot className="h-4 w-4 text-primary" />
                          </span>
                          {r.t}
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
                              { l: "Easy", c: "text-success border-success/30 hover:bg-success/10 bg-success/5" },
                              { l: "Intermediate", c: "text-warning border-warning/30 hover:bg-warning/10 bg-warning/5" },
                              { l: "Hard", c: "text-destructive border-destructive/30 hover:bg-destructive/10 bg-destructive/5" }
                            ].map((d) => (
                              <Link
                                key={d.l}
                                to={`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=${encodeURIComponent(d.l)}`}
                                className={`rounded border px-2 py-1 text-[10px] font-medium transition-colors ${d.c}`}
                              >
                                {d.l}
                              </Link>
                            ))}
                          </div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <Link 
                            to={`/app/interviews/setup?role=${encodeURIComponent(r.t)}&difficulty=Intermediate`}
                            className="inline-flex items-center text-xs text-primary hover:underline font-semibold"
                          >
                            Start <ArrowRight className="ml-1 h-3.5 w-3.5" />
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}
        </section>

        <section>
          <h2 className="mb-3 text-sm font-semibold">Recent sessions</h2>
          <Card className="overflow-hidden border-border bg-card p-0">
            <table className="w-full text-sm">
              <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                <tr>
                  <th className="px-4 py-2 font-mono uppercase tracking-wider">Role</th>
                  <th className="px-4 py-2 font-mono uppercase tracking-wider">Score</th>
                  <th className="px-4 py-2 font-mono uppercase tracking-wider">Duration</th>
                  <th className="px-4 py-2 font-mono uppercase tracking-wider">When</th>
                  <th className="px-4 py-2 text-right" />
                </tr>
              </thead>
              <tbody>
                {interviewHistory.map((iv) => (
                  <tr key={iv.id} className="border-t border-border">
                    <td className="px-4 py-3 font-medium">{iv.role}</td>
                    <td className="px-4 py-3">
                      <Badge variant="outline" className="font-mono">{iv.score}/100</Badge>
                    </td>
                    <td className="px-4 py-3 font-mono">{iv.duration}m</td>
                    <td className="px-4 py-3 text-muted-foreground">{iv.when}</td>
                    <td className="px-4 py-3 text-right">
                      <Link
                        to={`/app/interviews/${iv.id}/report`}
                        className="text-xs text-primary hover:underline"
                      >
                        View report
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </section>
      </div>
    </AppShell>
  );
}

export default InterviewsPage;
