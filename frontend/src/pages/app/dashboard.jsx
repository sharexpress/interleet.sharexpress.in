import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  BarChart,
  Bar,
} from "recharts";

import { AppShell, PageHeader } from "@/components/layout/AppShell";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

import { ArrowUpRight, Sparkles, Trophy, Flame, Target, Award, ChevronRight } from "lucide-react";

import { activityWeekly, challenges, recentActivity } from "@/lib/mock";

import { ChallengeCard } from "@/components/domain/ChallengeCard";

function Dashboard() {
  // state.user.user is the flat user object — no double-nesting needed
  const { user } = useSelector((state) => state.user);

  if (!user) return null;

  const domainData = [
    { domain: "Frontend", score: user.frontend_rating || 0 },
    { domain: "Backend", score: user.backend_rating || 0 },
    { domain: "Fullstack", score: user.fullstack_rating || 0 },
    { domain: "DevOps", score: user.devops_rating || 0 },
  ];

  return (
    <AppShell>
      <PageHeader
        title={`Welcome back, ${user.full_name?.split(" ")[0] || "Engineer"}`}
        description="Your engineering arena at a glance."
        actions={
          <>
            <Button variant="outline" asChild>
              <Link to="/app/interviews/live">Start an interview</Link>
            </Button>

            <Button asChild>
              <Link to="/app/challenges">Practice now</Link>
            </Button>
          </>
        }
      />

      <div className="space-y-6 px-4 py-6 md:px-8">
        {/* STATS */}
        <div className="grid gap-4 md:grid-cols-4">
          <StatCard
            label="XP"
            value={user.overall_rating || 0}
            delta="+120 this week"
            icon={Sparkles}
            accent="text-primary"
          />
          <StatCard
            label="Frontend"
            value={user.frontend_rating || 0}
            delta="Frontend score"
            icon={Trophy}
            accent="text-chart-2"
          />
          <StatCard
            label="Streak"
            value={`${user.streak_count || 0} days`}
            delta="Keep consistency"
            icon={Flame}
            accent="text-chart-3"
          />
          <StatCard
            label="Backend"
            value={user.backend_rating || 0}
            delta="Backend score"
            icon={Target}
            accent="text-chart-4"
          />
        </div>

        {/* CHARTS */}
        <div className="grid gap-4 lg:grid-cols-3">
          <Card className="border-border bg-card p-5 lg:col-span-2">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold">Weekly activity</h3>
                <p className="text-xs text-muted-foreground">
                  Challenges solved and minutes practiced.
                </p>
              </div>
              <Badge variant="outline" className="font-mono text-[10px]">
                7d
              </Badge>
            </div>

            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={activityWeekly}>
                  <CartesianGrid
                    stroke="hsl(var(--border))"
                    strokeDasharray="3 3"
                    vertical={false}
                  />
                  <XAxis
                    dataKey="day"
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                  />
                  <YAxis
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: 8,
                      fontSize: 12,
                    }}
                  />
                  <Bar dataKey="solved" fill="var(--color-primary)" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card className="border-border bg-card p-5">
            <div className="mb-4">
              <h3 className="text-sm font-semibold">Domain strengths</h3>
              <p className="text-xs text-muted-foreground">Skill across the engineering stack.</p>
            </div>

            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={domainData}>
                  <PolarGrid stroke="hsl(var(--border))" />
                  <PolarAngleAxis
                    dataKey="domain"
                    tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
                  />
                  <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 3000]} />
                  <Radar
                    dataKey="score"
                    stroke="var(--color-primary)"
                    fill="var(--color-primary)"
                    fillOpacity={0.25}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        {/* RECOMMENDED */}
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="text-sm font-semibold">Recommended for you</h3>
              <Link
                to="/app/challenges"
                className="text-xs text-muted-foreground hover:text-foreground"
              >
                See all
                <ChevronRight className="ml-0.5 inline h-3 w-3" />
              </Link>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              {challenges.slice(0, 4).map((challenge) => (
                <ChallengeCard key={challenge.id} c={challenge} />
              ))}
            </div>
          </div>

          <Card className="border-border bg-card p-5">
            <h3 className="mb-4 text-sm font-semibold">Recent activity</h3>
            <ul className="space-y-3">
              {recentActivity.map((activity, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-primary" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm">{activity.text}</p>
                    <p className="text-xs text-muted-foreground">
                      {activity.domain} · {activity.when}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
            <Button variant="ghost" className="mt-3 w-full">
              View all activity
              <ArrowUpRight className="ml-1 h-3.5 w-3.5" />
            </Button>
          </Card>
        </div>

        {/* INTERVIEW + BADGES */}
        <div className="grid gap-4 lg:grid-cols-3">
          <Card className="border-border bg-card p-5 lg:col-span-2">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold">Interview score trend</h3>
                <p className="text-xs text-muted-foreground">
                  Rolling average across all sessions.
                </p>
              </div>
              <Badge variant="outline" className="font-mono text-[10px]">
                90d
              </Badge>
            </div>

            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={[
                    { d: "W1", s: 62 },
                    { d: "W2", s: 65 },
                    { d: "W3", s: 71 },
                    { d: "W4", s: 70 },
                    { d: "W5", s: 76 },
                    { d: "W6", s: 78 },
                    { d: "W7", s: 81 },
                    { d: "W8", s: 84 },
                  ]}
                >
                  <CartesianGrid
                    stroke="hsl(var(--border))"
                    strokeDasharray="3 3"
                    vertical={false}
                  />
                  <XAxis
                    dataKey="d"
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                  />
                  <YAxis
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                    domain={[40, 100]}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: 8,
                      fontSize: 12,
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="s"
                    stroke="var(--color-primary)"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card className="border-border bg-card p-5">
            <h3 className="mb-3 text-sm font-semibold">Badges & achievements</h3>
            <div className="space-y-2">
              {(user.badges || []).map((badge) => (
                <div
                  key={badge}
                  className="flex items-center gap-3 rounded-md border border-border bg-background/40 p-2.5"
                >
                  <span className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/15 text-primary">
                    <Award className="h-4 w-4" />
                  </span>
                  <span className="text-sm">{badge}</span>
                </div>
              ))}
            </div>

            <div className="mt-4">
              <div className="mb-1 flex items-center justify-between text-xs">
                <span className="text-muted-foreground">Next badge: Top 5% APIs</span>
                <span className="font-mono">82/100</span>
              </div>
              <Progress value={82} />
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}

function StatCard({ label, value, delta, icon: Icon, accent }) {
  return (
    <Card className="gap-2 border-border bg-card p-4">
      <div className="flex items-center justify-between">
        <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
          {label}
        </p>
        <Icon className={`h-4 w-4 ${accent}`} />
      </div>
      <p className="text-2xl font-semibold tracking-tight">{value}</p>
      <p className="text-xs text-muted-foreground">{delta}</p>
    </Card>
  );
}

export default Dashboard;
