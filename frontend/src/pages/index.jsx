import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MarketingNav, MarketingFooter } from "@/components/marketing/Marketing";
import { API } from "@/api/api";
import {
  ArrowRight,
  Bot,
  Code2,
  Network,
  Trophy,
  ShieldCheck,
  Sparkles,
  Terminal,
  Database,
  Layers,
  Cloud,
  Globe2,
  Check,
  Star,
  Cpu,
  Activity } from
"lucide-react";

/* ─── Domain icon map ─────────────────────────────────────────── */
const domainIcons = {
  Frontend: Code2,
  Backend: Terminal,
  DevOps: Cloud,
  APIs: Layers,
  Databases: Database,
  Fullstack: Cpu,
  "System Design": Network,
};

const domainDescriptions = {
  Frontend: "Performance, accessibility, state, design systems.",
  Backend: "Concurrency, queues, services, business logic.",
  DevOps: "CI/CD, containers, observability, infra-as-code.",
  APIs: "REST, gRPC, GraphQL, contracts, versioning.",
  Databases: "Modeling, indexing, replication, query tuning.",
  Fullstack: "End-to-end applications, full-stack architecture.",
  "System Design": "Distributed systems, caching, scale, tradeoffs.",
};

/* ─── Root component ──────────────────────────────────────────── */
function Landing() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    document.title = "Interleet — Practice Real Engineering Challenges | Frontend, Backend, DevOps, System Design";
    API.get("/api/public/stats")
      .then((res) => setStats(res.data))
      .catch(() => {});
  }, []);

  /* Signal to vite-plugin-prerender that the page is ready to snapshot */
  useEffect(() => {
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <MarketingNav />
      <Hero />
      <StatsStrip stats={stats} />
      <ProblemStatement />
      <Features />
      <InterviewShowcase />
      <SystemDesignShowcase />
      <Domains stats={stats} />
      <CompetitiveEcosystem stats={stats} />
      <RecruiterSection />
      <Testimonials />
      <CTA />
      <MarketingFooter />
    </div>);

}

function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-border">
      <div className="dot-bg pointer-events-none absolute inset-0 opacity-40" />
      <div
        className="pointer-events-none absolute inset-x-0 -top-32 h-[500px] bg-[radial-gradient(ellipse_at_top,theme(colors.primary/15),transparent_60%)]"
        aria-hidden />
      
      <div className="relative mx-auto max-w-7xl px-4 pb-20 pt-16 md:px-8 md:pt-24">
        <div className="mx-auto max-w-3xl text-center">
          <Badge variant="outline" className="mb-5 gap-1.5 border-border/80 bg-card/50 px-3 py-1 font-mono text-[11px] uppercase tracking-wider text-muted-foreground">
            <Sparkles className="h-3 w-3 text-primary" />
            Real engineering, not just puzzles
          </Badge>
          <h1 className="text-balance text-4xl font-semibold tracking-tight md:text-6xl">
            Bridging the Gap Between{" "}
            <span className="bg-gradient-to-b from-foreground to-foreground/60 bg-clip-text text-transparent">
              DSA
            </span>{" "}
            and{" "}
            <span className="bg-gradient-to-br from-primary via-primary to-chart-4 bg-clip-text text-transparent">
              Real-World Engineering
            </span>
            .
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base text-muted-foreground md:text-lg">
            Practice frontend, backend, DevOps, APIs, databases, and system design on real
            production-style problems. Run AI mock interviews. Compete on engineering leaderboards.
            Build a recruiter-verified profile.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <Button asChild size="lg">
              <Link to="/app/challenges">
                Start Practicing <ArrowRight className="ml-1.5 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link to="/app/interviews/live">
                <Bot className="mr-1.5 h-4 w-4" />
                Try AI Interview
              </Link>
            </Button>
          </div>
          <p className="mt-4 font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            Free to start · No credit card required
          </p>
        </div>

        {/* Dashboard preview */}
        <div className="relative mx-auto mt-14 max-w-5xl">
          <div className="absolute -inset-x-10 -top-10 -z-10 h-[520px] bg-[radial-gradient(ellipse_at_center,theme(colors.primary/12),transparent_70%)]" />
          <DashboardPreview />
        </div>
      </div>
    </section>);

}

function DashboardPreview() {
  const { isAuthenticated, user } = useSelector((state) => state.user || {});
  const [stats, setStats] = useState(null);

  useEffect(() => {
    API.get("/api/public/stats")
      .then((res) => setStats(res.data))
      .catch(() => {});
  }, []);

  // Use authenticated user's data if logged in, otherwise showcase user from API
  const showcase = stats?.showcase_user;
  const displayName = isAuthenticated
    ? (user?.full_name?.split(" ")[0] || "Engineer")
    : (showcase?.name?.split(" ")[0] || "Alex");
  const rating = isAuthenticated
    ? (user?.overall_rating || 0)
    : (showcase?.rating || 0);
  const xp = showcase?.xp || 0;
  const rank = showcase?.rank || 1;
  const streak = isAuthenticated
    ? (user?.streak_count || 0)
    : (showcase?.streak || 0);
  const domainStrengths = showcase?.domain_strengths || [
    { name: "Backend", score: 10 },
    { name: "APIs", score: 10 },
    { name: "System Design", score: 10 },
  ];

  // Generate activity bars from showcase data or defaults
  const activityBars = [40, 65, 35, 80, 55, 90, 70];

  return (
    <div className="overflow-hidden rounded-xl border border-border bg-card shadow-2xl shadow-black/40">
      {/* Window chrome */}
      <div className="flex items-center gap-2 border-b border-border bg-background/60 px-3 py-2.5">
        <div className="flex gap-1.5">
          <span className="h-2.5 w-2.5 rounded-full bg-destructive/60" />
          <span className="h-2.5 w-2.5 rounded-full bg-warning/60" />
          <span className="h-2.5 w-2.5 rounded-full bg-success/60" />
        </div>
        <div className="mx-auto flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1 font-mono text-[11px] text-muted-foreground">
          <Globe2 className="h-3 w-3" />
          interleet.sharexpress.in/dashboard
        </div>
      </div>
      <div className="grid gap-0 md:grid-cols-[180px_1fr]">
        {/* mini sidebar */}
        <div className="hidden border-r border-border bg-sidebar p-3 md:block">
          <p className="mb-2 px-2 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">Menu</p>
          {[
          { i: Activity, l: "Dashboard", active: true },
          { i: Code2, l: "Challenges" },
          { i: Bot, l: "AI Interviews" },
          { i: Network, l: "System Design" },
          { i: Trophy, l: "Leaderboard" }].
          map(({ i: Icon, l, active }) =>
          <div
            key={l}
            className={`mb-0.5 flex items-center gap-2 rounded-md px-2 py-1.5 text-xs ${
            active ? "bg-accent text-foreground" : "text-muted-foreground"}`
            }>
            
              <Icon className="h-3.5 w-3.5" />
              {l}
            </div>
          )}
        </div>

        <div className="p-4 md:p-6">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs text-muted-foreground">Welcome back, {displayName}</p>
              <p className="text-base font-semibold">Your engineering arena</p>
            </div>
            <Badge variant="outline" className="font-mono text-[10px]">RATING {rating.toLocaleString()}</Badge>
          </div>

          <div className="mt-4 grid gap-3 md:grid-cols-4">
            {[
            { k: "XP", v: xp > 1000 ? `${(xp / 1000).toFixed(1)}k` : String(xp), c: "text-primary" },
            { k: "Rank", v: `#${rank}`, c: "text-chart-2" },
            { k: "Streak", v: `${streak}d`, c: "text-chart-3" },
            { k: "Solved", v: String(showcase?.solved || 0), c: "text-chart-4" }].
            map((m) =>
            <div key={m.k} className="rounded-lg border border-border bg-background/40 p-3">
                <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  {m.k}
                </p>
                <p className={`mt-1 text-lg font-semibold ${m.c}`}>{m.v}</p>
              </div>
            )}
          </div>

          <div className="mt-3 grid gap-3 md:grid-cols-3">
            <div className="rounded-lg border border-border bg-background/40 p-3 md:col-span-2">
              <div className="mb-2 flex items-center justify-between">
                <p className="text-xs font-medium">Weekly activity</p>
                <p className="font-mono text-[10px] text-muted-foreground">7d</p>
              </div>
              <div className="flex h-20 items-end gap-1.5">
                {activityBars.map((h, i) =>
                <div key={i} className="flex-1 rounded-sm bg-gradient-to-t from-primary/60 to-primary/20" style={{ height: `${h}%` }} />
                )}
              </div>
            </div>
            <div className="rounded-lg border border-border bg-background/40 p-3">
              <p className="mb-2 text-xs font-medium">Domain strength</p>
              <div className="space-y-1.5">
                {domainStrengths.slice(0, 3).map(({ name, score }) =>
                <div key={name}>
                    <div className="mb-0.5 flex justify-between text-[11px]">
                      <span className="text-muted-foreground">{name}</span>
                      <span className="font-mono">{score}%</span>
                    </div>
                    <div className="h-1 rounded-full bg-muted">
                      <div className="h-full rounded-full bg-primary" style={{ width: `${score}%` }} />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>);

}

function StatsStrip({ stats }) {
  const data = stats
    ? [
        { n: String(stats.total_challenges), l: "engineering challenges" },
        { n: String(stats.total_users), l: "developers practicing" },
        { n: String(stats.total_interviews), l: "AI interviews completed" },
        { n: String(stats.total_submissions), l: "code submissions" },
      ]
    : [
        { n: "—", l: "engineering challenges" },
        { n: "—", l: "developers practicing" },
        { n: "—", l: "AI interviews completed" },
        { n: "—", l: "code submissions" },
      ];

  return (
    <section className="border-b border-border bg-card/30">
      <div className="mx-auto grid max-w-7xl grid-cols-2 gap-6 px-4 py-10 md:grid-cols-4 md:px-8">
        {data.map((s) =>
        <div key={s.l}>
            <p className="text-2xl font-semibold tracking-tight md:text-3xl">{s.n}</p>
            <p className="mt-1 text-xs text-muted-foreground md:text-sm">{s.l}</p>
          </div>
        )}
      </div>
    </section>);

}

function ProblemStatement() {
  return (
    <section className="border-b border-border">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 md:grid-cols-2 md:px-8">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            The problem
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            DSA isn't the job.
          </h2>
          <p className="mt-4 text-muted-foreground md:text-lg">
            Most platforms drill algorithm puzzles. Real engineering means shipping software
            against real constraints — latency budgets, broken deploys, ambiguous specs, and
            code that has to outlive the sprint.
          </p>
          <p className="mt-3 text-muted-foreground md:text-lg">
            Interleet is built around the work engineers actually do.
          </p>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {[
          { i: Terminal, t: "Ship-shaped problems", d: "Modeled after real on-call tickets and design docs." },
          { i: Cpu, t: "Production constraints", d: "SLOs, p95 latency, cost, and consistency tradeoffs." },
          { i: Layers, t: "Full stack scope", d: "Frontend through infra — not a single language drill." },
          { i: Bot, t: "Communication too", d: "AI mock interviews score how you think and explain." }].
          map(({ i: Icon, t, d }) =>
          <Card key={t} className="border-border bg-card p-4">
              <Icon className="h-5 w-5 text-primary" />
              <p className="mt-3 text-sm font-medium">{t}</p>
              <p className="mt-1 text-xs text-muted-foreground">{d}</p>
            </Card>
          )}
        </div>
      </div>
    </section>);

}

function Features() {
  const features = [
  { i: Code2, t: "Full-stack challenges", d: "Frontend, backend, infra, APIs, databases — all in one place." },
  { i: Bot, t: "AI mock interviews", d: "Voice + chat sessions with rubric-graded feedback." },
  { i: Network, t: "System design studio", d: "Diagram, justify, and benchmark architectures." },
  { i: Trophy, t: "Engineering leaderboards", d: "Elo-style ratings by domain. Compete weekly." },
  { i: ShieldCheck, t: "Recruiter verification", d: "Verified skill badges hiring teams actually trust." },
  { i: Activity, t: "Deep analytics", d: "Track strengths, weaknesses, and progress over time." }];

  return (
    <section id="features" className="border-b border-border bg-card/30">
      <div className="mx-auto max-w-7xl px-4 py-20 md:px-8">
        <div className="max-w-2xl">
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            Platform
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Everything an engineer practices, in one workspace.
          </h2>
        </div>
        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {features.map(({ i: Icon, t, d }) =>
          <Card key={t} className="group border-border bg-card p-6 transition-colors hover:border-primary/40">
              <div className="flex h-9 w-9 items-center justify-center rounded-md border border-border bg-background">
                <Icon className="h-4 w-4 text-primary" />
              </div>
              <h3 className="mt-4 text-base font-semibold">{t}</h3>
              <p className="mt-1.5 text-sm text-muted-foreground">{d}</p>
            </Card>
          )}
        </div>
      </div>
    </section>);

}

function InterviewShowcase() {
  return (
    <section id="interviews" className="border-b border-border">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 md:grid-cols-2 md:px-8">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            AI Mock Interviews
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Practice the conversation, not just the code.
          </h2>
          <p className="mt-4 text-muted-foreground">
            Live, voice-enabled sessions that probe like a real senior interviewer would. Get a
            rubric-graded report on technical depth, communication, and problem-solving.
          </p>
          <ul className="mt-6 space-y-2 text-sm">
            {[
            "Role-specific prompts (Backend, Frontend, System Design, DevOps)",
            "Live transcript with confidence and clarity scoring",
            "Targeted recommendations after every session"].
            map((x) =>
            <li key={x} className="flex items-start gap-2">
                <Check className="mt-0.5 h-4 w-4 text-success" />
                <span className="text-foreground/85">{x}</span>
              </li>
            )}
          </ul>
        </div>
        <Card className="border-border bg-card p-5">
          <div className="flex items-center justify-between border-b border-border pb-3">
            <div className="flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-primary/15">
                <Bot className="h-3.5 w-3.5 text-primary" />
              </span>
              <div>
                <p className="text-sm font-medium">Senior Backend Interview</p>
                <p className="text-xs text-muted-foreground">42 min · Live</p>
              </div>
            </div>
            <Badge variant="outline" className="font-mono text-[10px]">REC</Badge>
          </div>
          <div className="mt-4 space-y-3">
            <Bubble who="ai">
              Let's design a URL shortener. Walk me through how you'd handle 50k writes/sec at the
              hot path.
            </Bubble>
            <Bubble who="me">
              I'd front it with a write-ahead queue, batch into the ID generator, and store the
              mapping in a sharded KV…
            </Bubble>
            <Bubble who="ai">
              How are you generating IDs without a single point of contention?
            </Bubble>
          </div>
          <div className="mt-4 flex items-center justify-between rounded-lg border border-border bg-background/40 p-3">
            <div className="flex items-center gap-3 text-xs">
              <span className="font-mono">02:14 / 45:00</span>
              <span className="h-1 w-24 rounded-full bg-muted">
                <span className="block h-full w-1/3 rounded-full bg-primary" />
              </span>
            </div>
            <Badge variant="outline" className="gap-1 text-success">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" />
              Mic on
            </Badge>
          </div>
        </Card>
      </div>
    </section>);

}

function Bubble({ who, children }) {
  return (
    <div className={`flex ${who === "me" ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-3.5 py-2 text-sm ${
        who === "me" ?
        "bg-primary/15 text-foreground" :
        "border border-border bg-background/60 text-foreground/90"}`
        }>
        
        {children}
      </div>
    </div>);

}

function SystemDesignShowcase() {
  return (
    <section id="system-design" className="border-b border-border bg-card/30">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 md:grid-cols-2 md:px-8">
        <Card className="order-2 border-border bg-card p-5 md:order-1">
          <div className="grid grid-cols-3 gap-3">
            {[
            { i: Globe2, l: "Client" },
            { i: Layers, l: "API Gateway" },
            { i: Network, l: "Service Mesh" },
            { i: Cpu, l: "Workers" },
            { i: Database, l: "Postgres" },
            { i: Cloud, l: "Object Store" }].
            map(({ i: Icon, l }) =>
            <div key={l} className="rounded-lg border border-border bg-background/40 p-3 text-center">
                <Icon className="mx-auto h-4 w-4 text-primary" />
                <p className="mt-2 font-mono text-[11px] text-muted-foreground">{l}</p>
              </div>
            )}
          </div>
          <div className="mt-4 rounded-lg border border-dashed border-border p-3">
            <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
              Notes · p95 = 240ms
            </p>
            <p className="mt-1 text-xs text-foreground/80">
              Read-through cache in front of Postgres; consistent hashing for shard pinning.
            </p>
          </div>
        </Card>
        <div className="order-1 md:order-2">
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            System Design Studio
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Architect, defend, iterate.
          </h2>
          <p className="mt-4 text-muted-foreground">
            Build architectures with real components. Justify tradeoffs. Simulate failure modes and
            scale curves. Compare your design against reference solutions.
          </p>
        </div>
      </div>
    </section>);

}

function Domains({ stats }) {
  // Build domain items from real data if available
  const items = stats?.domains?.length
    ? stats.domains.map((d) => {
        const Icon = domainIcons[d.name] || Code2;
        return {
          i: Icon,
          t: d.name,
          d: domainDescriptions[d.name] || "",
          count: d.challenge_count,
        };
      })
    : [
        { i: Code2, t: "Frontend", d: domainDescriptions.Frontend, count: null },
        { i: Terminal, t: "Backend", d: domainDescriptions.Backend, count: null },
        { i: Cloud, t: "DevOps", d: domainDescriptions.DevOps, count: null },
        { i: Layers, t: "APIs", d: domainDescriptions.APIs, count: null },
        { i: Database, t: "Databases", d: domainDescriptions.Databases, count: null },
        { i: Network, t: "System Design", d: domainDescriptions["System Design"], count: null },
      ];

  return (
    <section className="border-b border-border">
      <div className="mx-auto max-w-7xl px-4 py-20 md:px-8">
        <div className="max-w-2xl">
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            Practice domains
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            {stats?.domains?.length
              ? `${stats.domains.length} tracks. One stack of skills.`
              : "Six tracks. One stack of skills."}
          </h2>
        </div>
        <div className="mt-10 grid gap-3 md:grid-cols-3">
          {items.map(({ i: Icon, t, d, count }) =>
          <Card key={t} className="border-border bg-card p-5 transition-colors hover:border-primary/40">
              <div className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-background">
                  <Icon className="h-4 w-4 text-primary" />
                </span>
                <div>
                  <h3 className="text-base font-semibold">{t}</h3>
                  {count !== null && (
                    <p className="font-mono text-[10px] text-muted-foreground">
                      {count} challenge{count !== 1 ? "s" : ""}
                    </p>
                  )}
                </div>
              </div>
              <p className="mt-3 text-sm text-muted-foreground">{d}</p>
            </Card>
          )}
        </div>
      </div>
    </section>);

}

function CompetitiveEcosystem({ stats }) {
  const topUsers = stats?.top_users || [];

  return (
    <section className="border-b border-border bg-card/30">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 md:grid-cols-2 md:px-8">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            Competitive ecosystem
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Rated by domain. Ranked weekly.
          </h2>
          <p className="mt-4 text-muted-foreground">
            Engineering Elo across six tracks. Compete in weekly contests. Climb regional and
            global boards. Show the work, not the buzzwords.
          </p>
        </div>
        <Card className="border-border bg-card p-3">
          <div className="overflow-hidden rounded-md border border-border">
            <table className="w-full text-sm">
              <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                <tr>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider">#</th>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider">User</th>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider">Rating</th>
                  <th className="px-3 py-2 text-right font-mono uppercase tracking-wider">Δ</th>
                </tr>
              </thead>
              <tbody>
                {topUsers.length > 0
                  ? topUsers.map((u) => (
                      <tr key={u.rank} className="border-t border-border">
                        <td className="px-3 py-2 font-mono text-muted-foreground">{u.rank}</td>
                        <td className="px-3 py-2 font-medium">
                          <Link to={`/app/profile/${u.username}`} className="hover:text-primary transition-colors">
                            @{u.username}
                          </Link>
                        </td>
                        <td className="px-3 py-2 font-mono">{u.rating}</td>
                        <td
                          className={`px-3 py-2 text-right font-mono ${
                            u.delta < 0 ? "text-destructive" : "text-success"
                          }`}>
                          {u.delta >= 0 ? `+${u.delta}` : String(u.delta)}
                        </td>
                      </tr>
                    ))
                  : [1, 2, 3, 4, 5].map((r) => (
                      <tr key={r} className="border-t border-border">
                        <td className="px-3 py-2 font-mono text-muted-foreground">{r}</td>
                        <td className="px-3 py-2">
                          <div className="h-3 w-20 animate-pulse rounded bg-muted" />
                        </td>
                        <td className="px-3 py-2">
                          <div className="h-3 w-10 animate-pulse rounded bg-muted" />
                        </td>
                        <td className="px-3 py-2 text-right">
                          <div className="ml-auto h-3 w-6 animate-pulse rounded bg-muted" />
                        </td>
                      </tr>
                    ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </section>);

}

function RecruiterSection() {
  return (
    <section id="recruiters" className="border-b border-border">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 md:grid-cols-2 md:px-8">
        <Card className="border-border bg-card p-5">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm font-medium">Jordan Lee</p>
              <p className="text-xs text-muted-foreground">Senior Backend · NYC</p>
            </div>
            <Badge className="gap-1 bg-success/15 text-success">
              <ShieldCheck className="h-3 w-3" />
              Verified
            </Badge>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-3 text-center">
            {[
            ["Rating", "2,410"],
            ["Solved", "412"],
            ["Top", "Backend"]].
            map(([k, v]) =>
            <div key={k} className="rounded-md border border-border bg-background/40 p-2">
                <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  {k}
                </p>
                <p className="text-sm font-semibold">{v}</p>
              </div>
            )}
          </div>
          <div className="mt-4 space-y-2">
            {[
            ["Concurrency", 92],
            ["Distributed systems", 84],
            ["API design", 88]].
            map(([n, v]) =>
            <div key={n}>
                <div className="mb-0.5 flex justify-between text-[11px]">
                  <span className="text-muted-foreground">{n}</span>
                  <span className="font-mono">{v}/100</span>
                </div>
                <div className="h-1 rounded-full bg-muted">
                  <div className="h-full rounded-full bg-primary" style={{ width: `${v}%` }} />
                </div>
              </div>
            )}
          </div>
        </Card>
        <div>
          <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            For recruiters
          </p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Verified engineering, not vibes.
          </h2>
          <p className="mt-4 text-muted-foreground">
            Profile badges that map to actual measured skill. Side-by-side candidate comparison.
            Full interview transcripts and rubric scores. The signal you actually need to hire.
          </p>
          <Button asChild className="mt-6" variant="outline">
            <Link to="/recruiter">
              Open recruiter dashboard <ArrowRight className="ml-1.5 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>
    </section>);

}

function Testimonials() {
  const t = [
  {
    q: "Finally a platform that tests how I actually work, not just whether I remember graph traversals.",
    n: "Maya Chen",
    r: "Staff Engineer, fintech"
  },
  {
    q: "The AI interview feedback was uncomfortably accurate. My on-sites felt easy after a month.",
    n: "Ravi Shankar",
    r: "DevOps Lead"
  },
  {
    q: "We screen with verified Interleet profiles now. Cut bad-fit loops in half.",
    n: "Priya Nair",
    r: "Head of Engineering Hiring"
  }];

  return (
    <section className="border-b border-border bg-card/30">
      <div className="mx-auto max-w-7xl px-4 py-20 md:px-8">
        <h2 className="max-w-2xl text-3xl font-semibold tracking-tight md:text-4xl">
          Built by engineers, trusted by teams.
        </h2>
        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {t.map((x) =>
          <Card key={x.n} className="border-border bg-card p-5">
              <div className="flex gap-0.5 text-warning">
                {Array.from({ length: 5 }).map((_, i) =>
              <Star key={i} className="h-3.5 w-3.5 fill-current" />
              )}
              </div>
              <p className="mt-3 text-sm text-foreground/90">"{x.q}"</p>
              <div className="mt-4 border-t border-border pt-3">
                <p className="text-sm font-medium">{x.n}</p>
                <p className="text-xs text-muted-foreground">{x.r}</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </section>);

}

function CTA() {
  const isAuthenticated = useSelector((state) => state.user?.isAuthenticated);

  return (
    <section className="border-b border-border">
      <div className="mx-auto max-w-5xl px-4 py-20 text-center md:px-8">
        <h2 className="text-3xl font-semibold tracking-tight md:text-5xl">
          Ready to engineer like it's production?
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-muted-foreground md:text-lg">
          Jump into a challenge or run a mock interview right now. No setup, no install.
        </p>
        <div className="mt-7 flex flex-wrap justify-center gap-3">
          {isAuthenticated ? (
            <Button asChild size="lg">
              <Link to="/app/dashboard">Go to Dashboard</Link>
            </Button>
          ) : (
            <>
              <Button asChild size="lg">
                <Link to="/signup">Create your account</Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link to="/app/dashboard">Explore the platform</Link>
              </Button>
            </>
          )}
        </div>
      </div>
    </section>);

}
export default Landing;
