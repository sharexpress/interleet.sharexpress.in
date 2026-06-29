import { useState, useEffect, useLayoutEffect, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { toast } from "sonner";
import { API } from "@/api/api";

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

import { ArrowUpRight, Sparkles, Trophy, Flame, Target, Award, ChevronRight, CheckCircle2, Circle, Bell, Mail } from "lucide-react";

import { activityWeekly, challenges, recentActivity } from "@/lib/mock";

import { ChallengeCard } from "@/components/domain/ChallengeCard";
import UpgradeModal from "@/components/UpgradeModal";

function Dashboard() {
  const navigate = useNavigate();
  // state.user.user is the flat user object — no double-nesting needed
  const { user } = useSelector((state) => state.user);

  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isReady, setIsReady] = useState(false);

  useLayoutEffect(() => {
    if (!loading) {
      setIsReady(true);
    }
  }, [loading]);

  const [quests, setQuests] = useState([
    { id: "1", text: "Maintain active streak", reward: "50 XP", done: true, type: "streak" },
    { id: "2", text: "Solve a medium challenge", reward: "150 XP", done: false, type: "challenge" },
    { id: "3", text: "Complete mock interview prep", reward: "300 XP", done: false, type: "interview" },
  ]);

  useEffect(() => {
    let isMounted = true;
    const fetchDashboard = async () => {
      try {
        const response = await API.get("/api/dashboard");
        if (isMounted) {
          setDashboardData(response.data);
          setLoading(false);
        }
      } catch (err) {
        console.error("Failed to load live dashboard, falling back to mock.", err);
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    fetchDashboard();
    return () => {
      isMounted = false;
    };
  }, []);

  if (!user) return null;

  // Real-time resolved data
  const activeUser = dashboardData?.user || user;

  // Map domainData dynamically from user.domains or backend ratings
  const domainData = useMemo(() => {
    return (activeUser.domains || [
      { domain: "Frontend", score: activeUser.frontend_rating || 0 },
      { domain: "Backend", score: activeUser.backend_rating || 0 },
      { domain: "Fullstack", score: activeUser.fullstack_rating || 0 },
      { domain: "DevOps", score: activeUser.devops_rating || 0 },
    ]).map(d => ({
      domain: d.domain,
      score: d.score || d.rating || 0
    }));
  }, [activeUser]);

  if (loading) {
    return (
      <AppShell>
        <PageHeader
          title={`Welcome back, ${user.username}`}
          description="Track your ratings, achievements, and mock interview readiness."
        />
        <div className="px-4 py-6 md:px-8 max-w-7xl mx-auto space-y-6 animate-pulse">
          {/* Quick stats skeleton cards */}
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-24 rounded-xl border border-border bg-card/30 p-4 space-y-3">
                <div className="h-3.5 w-16 rounded bg-zinc-800/40" />
                <div className="h-6 w-24 rounded bg-zinc-800/20" />
              </div>
            ))}
          </div>
          {/* Main content grid skeleton */}
          <div className="grid gap-6 md:grid-cols-3">
            {/* Left side skeletons */}
            <div className="md:col-span-2 space-y-6">
              <div className="h-[280px] rounded-xl border border-border bg-card/30 p-6 space-y-4" />
              <div className="h-[220px] rounded-xl border border-border bg-card/30 p-6 space-y-4" />
            </div>
            {/* Right side skeletons */}
            <div className="space-y-6">
              <div className="h-[180px] rounded-xl border border-border bg-card/30 p-6 space-y-4" />
              <div className="h-[320px] rounded-xl border border-border bg-card/30 p-6 space-y-4" />
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  const activeWeekly = dashboardData?.activityWeekly || activityWeekly;
  const activeRecentActivity = dashboardData?.recentActivity || recentActivity;
  const activeChallenges = dashboardData?.recommendedChallenges || challenges;
  const activeInterviewTrend = dashboardData?.interviewTrend || [
    { d: "W1", s: 62 },
    { d: "W2", s: 65 },
    { d: "W3", s: 71 },
    { d: "W4", s: 70 },
    { d: "W5", s: 76 },
    { d: "W6", s: 78 },
    { d: "W7", s: 81 },
    { d: "W8", s: 84 },
  ];

  const handleQuestToggle = (id) => {
    setQuests(prev => prev.map(q => {
      if (q.id === id) {
        const nextDone = !q.done;
        if (nextDone) {
          toast.success(`Quest completed! Claimed ${q.reward}!`);
        }
        return { ...q, done: nextDone };
      }
      return q;
    }));
  };

  const xp = activeUser.xp ?? activeUser.total_xp ?? 0;
  const level = Math.floor(xp / 1000) + 1;
  const xpInLevel = xp % 1000;
  const progress = (xpInLevel / 1000) * 100;

  return (
    <AppShell>
      <PageHeader
        title={`Welcome back, ${activeUser.name?.split(" ")[0] || "Engineer"}`}
        description="Your engineering arena at a glance."
        actions={
          <>
            {!activeUser.is_premium ? (
              <UpgradeModal
                trigger={
                  <Button className="bg-gradient-to-r from-[#FF6500] to-orange-600 hover:from-[#E05900] hover:to-orange-700 text-white font-bold border-none shadow-lg shadow-orange-500/25 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] cursor-pointer">
                    <Sparkles className="mr-1.5 h-4 w-4 fill-white text-white" />
                    Go Premium
                  </Button>
                }
              />
            ) : (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#FF6500]/10 border border-[#FF6500]/30 px-3.5 py-1.5 text-xs font-bold text-[#FF6500] shadow-[0_0_15px_rgba(255,101,0,0.1)]">
                <Sparkles className="h-3.5 w-3.5 fill-[#FF6500] text-[#FF6500] animate-pulse" /> Pro Elite
              </span>
            )}

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
            label={`Level ${level}`}
            value={`${xp.toLocaleString()} XP`}
            icon={Sparkles}
            accent="text-primary"
          >
            <div className="mt-2">
              <Progress value={progress} className="h-1.5 bg-zinc-850 animate-pulse" />
              <p className="text-[10px] text-muted-foreground mt-1 font-mono">
                {1000 - xpInLevel} XP to Level {level + 1}
              </p>
            </div>
          </StatCard>
          <StatCard
            label="Frontend"
            value={activeUser.frontend_rating || 0}
            delta="Frontend score"
            icon={Trophy}
            accent="text-chart-2"
          />
          <StatCard
            label="Streak"
            value={`${activeUser.streak_count || activeUser.streak || 0} days`}
            delta="Keep consistency"
            icon={Flame}
            accent="text-chart-3"
          />
          <StatCard
            label="Backend"
            value={activeUser.backend_rating || 0}
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
              {isReady ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={activeWeekly}>
                    <CartesianGrid
                      stroke="var(--color-border)"
                      strokeDasharray="3 3"
                      vertical={false}
                    />
                    <XAxis
                      dataKey="day"
                      stroke="var(--color-muted-foreground)"
                      fontSize={11}
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      stroke="var(--color-muted-foreground)"
                      fontSize={11}
                      tickLine={false}
                      axisLine={false}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "var(--color-card)",
                        border: "1px solid var(--color-border)",
                        borderRadius: 8,
                        fontSize: 12,
                      }}
                    />
                    <Bar dataKey="solved" fill="var(--color-primary)" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full w-full bg-zinc-900/10 dark:bg-zinc-900/40 rounded-xl p-4 flex flex-col justify-end gap-3 animate-pulse">
                  <div className="flex items-end justify-between gap-3 h-full px-2">
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[40%]" />
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[70%]" />
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[50%]" />
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[90%]" />
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[30%]" />
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[60%]" />
                    <div className="w-full bg-zinc-850 dark:bg-zinc-800 rounded-t h-[80%]" />
                  </div>
                </div>
              )}
            </div>
          </Card>

          <Card className="border-border bg-card p-5">
            <div className="mb-4">
              <h3 className="text-sm font-semibold">Domain strengths</h3>
              <p className="text-xs text-muted-foreground">Skill across the engineering stack.</p>
            </div>

            <div className="h-64">
              {isReady ? (
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={domainData}>
                    <PolarGrid stroke="var(--color-border)" />
                    <PolarAngleAxis
                      dataKey="domain"
                      tick={{ fontSize: 10, fill: "var(--color-muted-foreground)" }}
                    />
                    <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 100]} />
                    <Radar
                      dataKey="score"
                      stroke="var(--color-primary)"
                      fill="var(--color-primary)"
                      fillOpacity={0.25}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full w-full bg-zinc-900/10 dark:bg-zinc-900/40 rounded-xl flex items-center justify-center animate-pulse">
                  <div className="relative w-36 h-36 rounded-full border border-dashed border-zinc-800/80 flex items-center justify-center">
                    <div className="w-24 h-24 rounded-full border border-dashed border-zinc-800/60 flex items-center justify-center">
                      <div className="w-12 h-12 rounded-full bg-zinc-850 dark:bg-zinc-800/80" />
                    </div>
                  </div>
                </div>
              )}
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
              {activeChallenges.slice(0, 4).map((challenge) => (
                <ChallengeCard key={challenge.id} c={challenge} />
              ))}
            </div>
          </div>

          <div className="space-y-4">
            {/* Daily Quests Card */}
            <Card className="border-border bg-card p-5">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-white">Daily Quests</h3>
                <Badge variant="outline" className="font-mono text-[9px] border-primary/30 text-primary bg-primary/5">
                  Bonus XP
                </Badge>
              </div>
              <ul className="space-y-2.5">
                {quests.map((q) => (
                  <li 
                    key={q.id} 
                    onClick={() => handleQuestToggle(q.id)}
                    className="flex items-center justify-between p-2 rounded bg-zinc-900/60 border border-zinc-850 hover:border-zinc-700 transition-all cursor-pointer group animate-fade-in"
                  >
                    <div className="flex items-center gap-2 min-w-0">
                      {q.done ? (
                        <CheckCircle2 className="h-4 w-4 text-primary shrink-0" />
                      ) : (
                        <Circle className="h-4 w-4 text-zinc-650 group-hover:text-primary shrink-0 transition-colors" />
                      )}
                      <span className={`text-xs truncate ${q.done ? "text-zinc-500 line-through" : "text-zinc-300 font-medium"}`}>
                        {q.text}
                      </span>
                    </div>
                    <span className={`text-[10px] font-mono shrink-0 px-1.5 py-0.5 rounded ${q.done ? "bg-zinc-800 text-zinc-500" : "bg-primary/10 text-primary font-bold"}`}>
                      {q.reward}
                    </span>
                  </li>
                ))}
              </ul>
            </Card>

            {/* Recent Activity Card */}
            <Card className="border-border bg-card p-5 shadow-sm">
              <h3 className="mb-4 text-sm font-semibold">Recent activity</h3>
              <ul className="space-y-2">
                {activeRecentActivity.length === 0 ? (
                  <p className="text-xs text-muted-foreground py-4 text-center font-mono">No recent activity. Start solving challenges!</p>
                ) : (
                  activeRecentActivity.map((activity, index) => {
                    const isNotification = activity.type === "notification";
                    const isUnreadNotif = isNotification && activity.read === false;

                    const getActivityIcon = () => {
                      if (activity.type === "solved") {
                        return <CheckCircle2 className="h-4 w-4 text-emerald-500" />;
                      }
                      if (activity.type === "interview") {
                        return <Sparkles className="h-4 w-4 text-amber-500" />;
                      }
                      if (isNotification) {
                        if (activity.notification_type === "invite") {
                          return <Mail className="h-4 w-4 text-blue-500" />;
                        }
                        return <Bell className="h-4 w-4 text-purple-500" />;
                      }
                      return <span className="h-2 w-2 rounded-full bg-primary mt-1.5" />;
                    };

                    const handleActivityClick = async () => {
                      if (isNotification && isUnreadNotif) {
                        try {
                          await API.post(`/api/notifications/${activity.id}/read`);
                          if (dashboardData) {
                            const updatedRecent = dashboardData.recentActivity.map((act) =>
                              act.id === activity.id ? { ...act, read: true } : act
                            );
                            setDashboardData({
                              ...dashboardData,
                              recentActivity: updatedRecent,
                            });
                          }
                        } catch (err) {
                          console.error("Failed to mark notification as read:", err);
                        }
                      }
                      if (activity.link) {
                        navigate(activity.link);
                      }
                    };

                    const isClickable = !!activity.link;

                    return (
                      <li
                        key={index}
                        onClick={isClickable ? handleActivityClick : undefined}
                        className={`group flex items-start gap-3 p-2 rounded-lg transition-all ${
                          isClickable
                            ? "hover:bg-zinc-800/40 cursor-pointer active:scale-[0.98]"
                            : ""
                        } ${isUnreadNotif ? "bg-primary/5 border border-primary/20" : ""}`}
                      >
                        <div className="mt-0.5 shrink-0">
                          {getActivityIcon()}
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-1.5">
                            <p className={`truncate text-sm ${isUnreadNotif ? "font-semibold text-white" : "text-zinc-300"}`}>
                              {activity.text}
                            </p>
                            {isUnreadNotif && (
                              <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse shrink-0" />
                            )}
                          </div>
                          <p className="text-xs text-muted-foreground mt-0.5">
                            {activity.domain} · {activity.when}
                          </p>
                        </div>
                        {isClickable && (
                          <ChevronRight className="h-3.5 w-3.5 text-zinc-650 shrink-0 self-center opacity-0 group-hover:opacity-100 transition-opacity" />
                        )}
                      </li>
                    );
                  })
                )}
              </ul>
              <Button
                variant="ghost"
                className="mt-3 w-full"
                onClick={() => navigate("/app/settings?tab=notifications")}
              >
                View all activity
                <ArrowUpRight className="ml-1 h-3.5 w-3.5" />
              </Button>
            </Card>
          </div>
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
              {!isReady ? (
                <div className="h-full w-full bg-zinc-900/10 dark:bg-zinc-900/40 rounded-xl p-4 flex flex-col justify-between animate-pulse">
                  <div className="w-full h-px bg-zinc-850 dark:bg-zinc-850/50" />
                  <div className="w-full h-px bg-zinc-850 dark:bg-zinc-850/50" />
                  <div className="w-full h-px bg-zinc-850 dark:bg-zinc-850/50" />
                  <div className="w-full h-px bg-zinc-850 dark:bg-zinc-850/50" />
                </div>
              ) : activeInterviewTrend.length === 0 ? (
                <div className="flex h-full flex-col items-center justify-center border border-dashed border-border rounded bg-zinc-950/20 p-4 text-center">
                  <p className="text-xs text-muted-foreground font-mono">No mock interviews completed yet.</p>
                  <p className="text-[10px] text-zinc-500 font-mono mt-1">Practice mock interviews to plot your score trends!</p>
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={activeInterviewTrend}
                  >
                    <CartesianGrid
                      stroke="var(--color-border)"
                      strokeDasharray="3 3"
                      vertical={false}
                    />
                    <XAxis
                      dataKey="d"
                      stroke="var(--color-muted-foreground)"
                      fontSize={11}
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      stroke="var(--color-muted-foreground)"
                      fontSize={11}
                      tickLine={false}
                      axisLine={false}
                      domain={[40, 100]}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "var(--color-card)",
                        border: "1px solid var(--color-border)",
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
              )}
            </div>
          </Card>

          <Card className="border-border bg-card p-5">
            <h3 className="mb-3 text-sm font-semibold">Badges & achievements</h3>
            <div className="space-y-2">
              {(activeUser.badges || []).map((badge) => (
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

function StatCard({ label, value, delta, icon: Icon, accent, children }) {
  return (
    <Card className="gap-2 border-border bg-card p-4 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between">
          <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
            {label}
          </p>
          <Icon className={`h-4 w-4 ${accent}`} />
        </div>
        <p className="text-2xl font-semibold tracking-tight mt-1">{value}</p>
      </div>
      {children ? children : <p className="text-xs text-muted-foreground">{delta}</p>}
    </Card>
  );
}

export default Dashboard;
