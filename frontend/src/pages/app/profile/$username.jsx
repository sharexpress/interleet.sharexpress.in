import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { 
  Award, MapPin, Github, Link as LinkIcon, ShieldCheck, 
  Sparkles, Brain, RefreshCw, CheckCircle2, AlertCircle, PlayCircle, Loader2
} from "lucide-react";
import { API } from "@/api/api";

function ProfilePage() {
  const { username } = useParams();
  const { user: actual_user } = useSelector((state) => state.user);

  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [aiEvaluation, setAiEvaluation] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const fetchProfile = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await API.get(`/api/profile/${username}`);
        if (isMounted) {
          setProfileData(response.data);
          setLoading(false);
        }
      } catch (err) {
        if (isMounted) {
          setError("Failed to load user profile.");
          setLoading(false);
        }
      }
    };
    fetchProfile();
    return () => {
      isMounted = false;
    };
  }, [username]);

  const fetchAiEvaluation = async (force = false) => {
    setAiLoading(true);
    setAiError(null);
    try {
      const response = await API.get(`/api/profile/${username}/ai-evaluation`, {
        params: { force }
      });
      setAiEvaluation(response.data.evaluation);
    } catch (err) {
      setAiError("Failed to generate AI evaluation report.");
    } finally {
      setAiLoading(false);
    }
  };

  if (loading) {
    return (
      <AppShell>
        <div className="flex h-[80vh] flex-col items-center justify-center gap-3 text-muted-foreground">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm font-medium">Analyzing developer DNA...</p>
        </div>
      </AppShell>
    );
  }

  if (error || !profileData) {
    return (
      <AppShell>
        <div className="flex h-[80vh] flex-col items-center justify-center gap-3 text-muted-foreground px-4">
          <AlertCircle className="h-10 w-10 text-destructive" />
          <p className="text-sm font-semibold">{error || "User not found"}</p>
          <Button variant="outline" asChild className="mt-2">
            <Link to="/app/dashboard">Back to Dashboard</Link>
          </Button>
        </div>
      </AppShell>
    );
  }

  const { user, challenges, interviews_history } = profileData;

  // Generate heatmap dates
  const heatmapDays = [];
  const today = new Date();
  for (let i = 181; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    const dateStr = d.toISOString().split("T")[0];
    heatmapDays.push(dateStr);
  }
  const totalContributions = Object.values(user.heatmap || {}).reduce((a, b) => a + b, 0);

  return (
    <AppShell>
      {/* Banner */}
      <div className="relative border-b border-border">
        <div className="grid-bg absolute inset-0 opacity-30" />
        <div className="pointer-events-none absolute -top-20 left-1/3 h-[300px] w-[500px] rounded-full bg-primary/10 blur-3xl" />
        <div className="relative mx-auto flex max-w-6xl flex-col gap-5 px-4 py-8 md:flex-row md:items-end md:px-8">
          <Avatar className="h-20 w-20 border-2 border-border bg-card">
            {user.avatar && (
              <AvatarImage
                src={user.avatar}
                alt={user.name}
                className="object-cover"
              />
            )}
            <AvatarFallback className="text-xl font-bold bg-zinc-800 text-white">
              {user.name
                ?.split(" ")
                ?.map((n) => n[0])
                ?.join("")
                ?.slice(0, 2)
                ?.toUpperCase() || "?"}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-2xl font-semibold tracking-tight text-white">
                {user.name}
              </h1>
              <Badge className="gap-1 bg-success/15 text-success border border-success/30">
                <ShieldCheck className="h-3 w-3" />
                Verified
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">@{user.username}</p>
            <div className="mt-2 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
              <span className="inline-flex items-center gap-1">
                <MapPin className="h-3.5 w-3.5" />
                {user.location}
              </span>
              <span className="inline-flex items-center gap-1">
                <Github className="h-3.5 w-3.5" />
                {user.username}
              </span>
              <span className="inline-flex items-center gap-1">
                <LinkIcon className="h-3.5 w-3.5" />
                {user.username}.dev
              </span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">Share</Button>
            {actual_user?.username === user.username ? (
              <Button size="sm" asChild>
                <Link to="/app/settings">Edit Profile</Link>
              </Button>
            ) : (
              <Button size="sm">Follow</Button>
            )}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-4 py-6 md:px-8">
        <div className="grid gap-4 md:grid-cols-4">
          {[
            ["Overall Rating", user.rating.toString()],
            ["Global Rank", `#${user.rank}`],
            ["Challenges Solved", user.solved.toString()],
            ["Interviews Completed", user.interviews.toString()],
          ].map(([k, v]) => (
            <Card key={k} className="border-border bg-card p-4 shadow-sm hover:border-zinc-700 transition-colors">
              <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                {k}
              </p>
              <p className="mt-1 text-2xl font-semibold text-white">{v}</p>
            </Card>
          ))}
        </div>

        <Tabs defaultValue="overview" className="mt-6" onValueChange={(val) => {
          if (val === "ai-evaluation" && !aiEvaluation && !aiLoading) {
            fetchAiEvaluation();
          }
        }}>
          <TabsList className="bg-zinc-900 border border-zinc-800">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="challenges">Challenges</TabsTrigger>
            <TabsTrigger value="interviews">Interviews</TabsTrigger>
            <TabsTrigger value="badges">Badges</TabsTrigger>
            <TabsTrigger value="ai-evaluation" className="gap-1.5 text-primary hover:text-white">
              <Brain className="h-3.5 w-3.5 text-primary" />
              AI Career Coach
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="mt-4 grid gap-4 lg:grid-cols-3">
            <Card className="border-border bg-card p-5 lg:col-span-2">
              <h3 className="text-sm font-semibold text-white">Domain proficiency</h3>
              <div className="mt-4 space-y-4">
                {(user.domains || []).map((d) => (
                  <div key={d.domain}>
                    <div className="mb-1.5 flex justify-between text-xs">
                      <span className="text-muted-foreground">{d.domain}</span>
                      <span className="font-mono text-white">{d.score}/100</span>
                    </div>
                    <Progress value={d.score} className="h-2 bg-zinc-850" />
                  </div>
                ))}
              </div>
            </Card>
            <Card className="border-border bg-card p-5">
              <h3 className="text-sm font-semibold text-white">Contribution heatmap</h3>
              <div
                className="mt-4 grid grid-cols-26 gap-1"
                style={{ gridTemplateColumns: "repeat(26, minmax(0, 1fr))" }}
              >
                {heatmapDays.map((dateStr, i) => {
                  const count = user.heatmap?.[dateStr] || 0;
                  const bucket = count >= 4 ? 4 : count;
                  const cls = [
                    "bg-zinc-800/40",
                    "bg-primary/20",
                    "bg-primary/45",
                    "bg-primary/70",
                    "bg-primary",
                  ][bucket];
                  return (
                    <span 
                      key={dateStr} 
                      className={`h-2.5 w-2.5 rounded-sm ${cls} transition-all duration-300 hover:scale-125`} 
                      title={`${dateStr}: ${count} activities`}
                    />
                  );
                })}
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                Last 6 months · {totalContributions} contributions
              </p>
            </Card>
          </TabsContent>

          <TabsContent value="challenges" className="mt-4">
            <Card className="overflow-hidden border-border bg-card p-0">
              {challenges && challenges.length > 0 ? (
                <ul className="divide-y divide-border">
                  {challenges.map((c) => (
                    <li key={c.id} className="flex items-center justify-between px-4 py-3.5 hover:bg-zinc-850/30 transition-colors">
                      <div>
                        <p className="text-sm font-medium text-white">{c.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {c.domain} · {c.difficulty}
                        </p>
                      </div>
                      <Badge variant="outline" className="font-mono bg-zinc-900 border-zinc-700 text-white">
                        {c.xp} XP
                      </Badge>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground gap-3">
                  <PlayCircle className="h-10 w-10 text-zinc-600" />
                  <div>
                    <p className="text-sm font-medium text-white">No solved challenges yet</p>
                    <p className="text-xs max-w-sm mt-1">
                      Start solving coding and architectural challenges to build up your proficiency score.
                    </p>
                  </div>
                  <Button size="sm" asChild className="mt-2">
                    <Link to="/app/challenges">Solve Challenges</Link>
                  </Button>
                </div>
              )}
            </Card>
          </TabsContent>

          <TabsContent value="interviews" className="mt-4">
            <Card className="overflow-hidden border-border bg-card p-0">
              {interviews_history && interviews_history.length > 0 ? (
                <ul className="divide-y divide-border">
                  {interviews_history.map((iv) => (
                    <li key={iv.id} className="flex items-center justify-between px-4 py-3.5 hover:bg-zinc-850/30 transition-colors">
                      <div>
                        <p className="text-sm font-medium text-white">{iv.role}</p>
                        <p className="text-xs text-muted-foreground">
                          {iv.when} · {iv.duration}m
                        </p>
                      </div>
                      <div className="flex items-center gap-3">
                        <Badge variant="outline" className="font-mono bg-zinc-900 border-zinc-700 text-white">
                          Score: {iv.score}/100
                        </Badge>
                        <Button variant="ghost" size="sm" asChild className="h-7 text-xs px-2 text-primary hover:text-white">
                          <Link to={`/app/interviews/${iv.id}/report`}>View Report</Link>
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground gap-3">
                  <Award className="h-10 w-10 text-zinc-600" />
                  <div>
                    <p className="text-sm font-medium text-white">No completed interviews yet</p>
                    <p className="text-xs max-w-sm mt-1">
                      Complete AI mock interviews to get targeted feedback, score trends, and system design evaluations.
                    </p>
                  </div>
                  <Button size="sm" asChild className="mt-2">
                    <Link to="/app/interviews/setup">Start Mock Interview</Link>
                  </Button>
                </div>
              )}
            </Card>
          </TabsContent>

          <TabsContent value="badges" className="mt-4 grid gap-3 sm:grid-cols-2 md:grid-cols-4">
            {(user.badges || []).map((b) => (
              <Card key={b} className="flex items-center gap-3 border-zinc-800 bg-card p-4 hover:border-zinc-700 transition-colors">
                <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary/10 text-primary border border-primary/20">
                  <Award className="h-4 w-4" />
                </span>
                <span className="text-sm text-white font-medium">{b}</span>
              </Card>
            ))}
          </TabsContent>

          <TabsContent value="ai-evaluation" className="mt-4">
            {aiLoading ? (
              <Card className="flex flex-col items-center justify-center p-16 text-center text-muted-foreground border-zinc-800 bg-card">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <h4 className="mt-4 text-sm font-semibold text-white">Generating AI Skill Assessment</h4>
                <p className="mt-1 text-xs max-w-md">
                  Analyzing code execution metrics, language syntaxes, complexity analyses, and mock interview transcripts to evaluate your expertise...
                </p>
              </Card>
            ) : aiError ? (
              <Card className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground border-zinc-800 bg-card gap-3">
                <AlertCircle className="h-8 w-8 text-destructive" />
                <p className="text-sm font-medium text-white">{aiError}</p>
                <Button size="sm" onClick={() => fetchAiEvaluation(true)}>
                  Try Again
                </Button>
              </Card>
            ) : aiEvaluation ? (
              <div className="grid gap-4 md:grid-cols-3">
                {/* Profile Summary & Path Recommendation */}
                <div className="md:col-span-2 space-y-4">
                  <Card className="border-border bg-card p-5 relative overflow-hidden">
                    <div className="absolute right-0 top-0 h-32 w-32 rounded-full bg-primary/5 blur-2xl pointer-events-none" />
                    <div className="flex items-center gap-2 mb-3">
                      <Sparkles className="h-5 w-5 text-primary" />
                      <h3 className="text-base font-semibold text-white">AI Skill Profile</h3>
                    </div>
                    <p className="text-sm text-zinc-300 leading-relaxed">
                      {aiEvaluation.profile_summary}
                    </p>
                  </Card>

                  <div className="grid gap-4 sm:grid-cols-2">
                    <Card className="border-zinc-850 bg-card p-5">
                      <h4 className="text-xs font-semibold uppercase tracking-widest text-primary mb-3">Key Strengths</h4>
                      <ul className="space-y-2.5">
                        {aiEvaluation.strengths?.map((str, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-sm text-zinc-300">
                            <CheckCircle2 className="h-4 w-4 text-success shrink-0 mt-0.5" />
                            <span>{str}</span>
                          </li>
                        ))}
                      </ul>
                    </Card>

                    <Card className="border-zinc-850 bg-card p-5">
                      <h4 className="text-xs font-semibold uppercase tracking-widest text-orange-500 mb-3">Suggested Growth Areas</h4>
                      <ul className="space-y-2.5">
                        {aiEvaluation.improvements?.map((imp, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-sm text-zinc-300">
                            <span className="h-1.5 w-1.5 rounded-full bg-orange-500 shrink-0 mt-2" />
                            <span>{imp}</span>
                          </li>
                        ))}
                      </ul>
                    </Card>
                  </div>
                </div>

                {/* Career Fit & Challenges */}
                <div className="space-y-4">
                  <Card className="border-zinc-850 bg-card p-5">
                    <h3 className="text-sm font-semibold text-white mb-4">Recommended Career Paths</h3>
                    <div className="flex flex-wrap gap-2">
                      {aiEvaluation.suggested_paths?.map((path, idx) => (
                        <Badge key={idx} className="bg-primary/10 text-primary border border-primary/20 font-medium px-2.5 py-1">
                          {path}
                        </Badge>
                      ))}
                    </div>
                  </Card>

                  <Card className="border-zinc-850 bg-card p-5">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-semibold text-white">Next Practice Targets</h3>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => fetchAiEvaluation(true)} 
                        className="h-6 text-[10px] px-1.5 gap-1 hover:text-white"
                      >
                        <RefreshCw className="h-3 w-3" />
                        Re-evaluate
                      </Button>
                    </div>
                    <div className="space-y-2.5">
                      {aiEvaluation.next_challenges?.map((chTitle, idx) => (
                        <div 
                          key={idx} 
                          className="flex items-center justify-between p-2 rounded-md bg-zinc-900 border border-zinc-850 hover:border-zinc-700 transition-colors"
                        >
                          <span className="text-xs font-medium text-zinc-300 truncate max-w-[170px]">{chTitle}</span>
                          <Button size="sm" variant="ghost" asChild className="h-6 text-[10px] px-2 text-primary hover:text-white">
                            <Link to="/app/challenges">Solve</Link>
                          </Button>
                        </div>
                      ))}
                    </div>
                  </Card>
                </div>
              </div>
            ) : null}
          </TabsContent>
        </Tabs>
      </div>
    </AppShell>
  );
}

export default ProfilePage;
