import { useParams } from "react-router-dom";

import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Award, MapPin, Github, Link as LinkIcon, ShieldCheck } from "lucide-react";
import { user, interviewHistory, challenges } from "@/lib/mock";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { GetCurrentUser } from "@/redux/slices/userSlice";

function ProfilePage() {
  const { username } = useParams();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(GetCurrentUser());
  }, [dispatch]);

  const {
    user: actual_user,
    loading,
    error,
    onboardingCompleted,
    isAuthenticated,
  } = useSelector((state) => state.user);

  console.log(actual_user.user.full_name);

  return (
    <AppShell>
      {/* Banner */}
      <div className="relative border-b border-border">
        <div className="grid-bg absolute inset-0 opacity-30" />
        <div className="pointer-events-none absolute -top-20 left-1/3 h-[300px] w-[500px] rounded-full bg-primary/10 blur-3xl" />
        <div className="relative mx-auto flex max-w-6xl flex-col gap-5 px-4 py-8 md:flex-row md:items-end md:px-8">
          <Avatar className="h-20 w-20 border-2 border-border bg-card">
            <AvatarFallback className="text-xl">AM</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-2xl font-semibold tracking-tight">
                {actual_user.user?.full_name || "null"}
              </h1>
              <Badge className="gap-1 bg-success/15 text-success">
                <ShieldCheck className="h-3 w-3" />
                Verified
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">
              @{actual_user.user?.username} · {user.title}
            </p>
            <div className="mt-2 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
              <span className="inline-flex items-center gap-1">
                <MapPin className="h-3.5 w-3.5" />
                {user.location}
              </span>
              <span className="inline-flex items-center gap-1">
                <Github className="h-3.5 w-3.5" />
                alex-morgan
              </span>
              <span className="inline-flex items-center gap-1">
                <LinkIcon className="h-3.5 w-3.5" />
                alexmorgan.dev
              </span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">Share</Button>
            <Button>Follow</Button>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-4 py-6 md:px-8">
        <div className="grid gap-4 md:grid-cols-4">
          {[
            ["Rating", user.rating.toString()],
            ["Rank", `#${user.rank}`],
            ["Solved", user.solved.toString()],
            ["Interviews", user.interviews.toString()],
          ].map(([k, v]) => (
            <Card key={k} className="border-border bg-card p-4">
              <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                {k}
              </p>
              <p className="mt-1 text-2xl font-semibold">{v}</p>
            </Card>
          ))}
        </div>

        <Tabs defaultValue="overview" className="mt-6">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="challenges">Challenges</TabsTrigger>
            <TabsTrigger value="interviews">Interviews</TabsTrigger>
            <TabsTrigger value="badges">Badges</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="mt-4 grid gap-4 lg:grid-cols-3">
            <Card className="border-border bg-card p-5 lg:col-span-2">
              <h3 className="text-sm font-semibold">Domain proficiency</h3>
              <div className="mt-4 space-y-3">
                {user.domains.map((d) => (
                  <div key={d.domain}>
                    <div className="mb-1 flex justify-between text-xs">
                      <span className="text-muted-foreground">{d.domain}</span>
                      <span className="font-mono">{d.score}/100</span>
                    </div>
                    <div className="h-1.5 rounded-full bg-muted">
                      <div
                        className="h-full rounded-full bg-primary"
                        style={{ width: `${d.score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </Card>
            <Card className="border-border bg-card p-5">
              <h3 className="text-sm font-semibold">Contribution heatmap</h3>
              <div
                className="mt-4 grid grid-cols-26 gap-1"
                style={{ gridTemplateColumns: "repeat(26, minmax(0, 1fr))" }}
              >
                {Array.from({ length: 26 * 7 }).map((_, i) => {
                  const v = (Math.sin(i * 1.3) + 1) / 2;
                  const bucket = Math.floor(v * 4);
                  const cls = [
                    "bg-muted",
                    "bg-primary/25",
                    "bg-primary/55",
                    "bg-primary/80",
                    "bg-primary",
                  ][bucket];
                  return <span key={i} className={`h-2.5 w-2.5 rounded-sm ${cls}`} />;
                })}
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                Last 6 months · 412 contributions
              </p>
            </Card>
          </TabsContent>

          <TabsContent value="challenges" className="mt-4">
            <Card className="overflow-hidden border-border bg-card p-0">
              <ul className="divide-y divide-border">
                {challenges.slice(0, 6).map((c) => (
                  <li key={c.id} className="flex items-center justify-between px-4 py-3">
                    <div>
                      <p className="text-sm font-medium">{c.title}</p>
                      <p className="text-xs text-muted-foreground">
                        {c.domain} · {c.difficulty}
                      </p>
                    </div>
                    <Badge variant="outline" className="font-mono">
                      {c.xp} XP
                    </Badge>
                  </li>
                ))}
              </ul>
            </Card>
          </TabsContent>

          <TabsContent value="interviews" className="mt-4">
            <Card className="overflow-hidden border-border bg-card p-0">
              <ul className="divide-y divide-border">
                {interviewHistory.map((iv) => (
                  <li key={iv.id} className="flex items-center justify-between px-4 py-3">
                    <div>
                      <p className="text-sm font-medium">{iv.role}</p>
                      <p className="text-xs text-muted-foreground">
                        {iv.when} · {iv.duration}m
                      </p>
                    </div>
                    <Badge variant="outline" className="font-mono">
                      {iv.score}/100
                    </Badge>
                  </li>
                ))}
              </ul>
            </Card>
          </TabsContent>

          <TabsContent value="badges" className="mt-4 grid gap-3 sm:grid-cols-2 md:grid-cols-4">
            {user.badges
              .concat(["Frontend I", "Database Pro", "Distributed II", "Contest Finalist"])
              .map((b) => (
                <Card key={b} className="flex items-center gap-3 border-border bg-card p-4">
                  <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary/15 text-primary">
                    <Award className="h-4 w-4" />
                  </span>
                  <span className="text-sm">{b}</span>
                </Card>
              ))}
          </TabsContent>
        </Tabs>
      </div>
    </AppShell>
  );
}
export default ProfilePage;
