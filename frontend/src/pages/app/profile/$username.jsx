import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { toast } from "sonner";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { 
  Award, MapPin, Github, Link as LinkIcon, ShieldCheck, 
  Sparkles, Brain, RefreshCw, CheckCircle2, AlertCircle, PlayCircle, Loader2, Lock
} from "lucide-react";
import { API } from "@/api/api";
import ContributionHeatmap from "@/components/domain/ContributionHeatmap";

const getDivisionTier = (rating, rank) => {
  if (rank === 1) return { name: "Grandmaster Elite", color: "bg-purple-500/15 text-purple-400 border-purple-500/30" };
  if (rank <= 3) return { name: "Grandmaster", color: "bg-pink-500/15 text-pink-400 border-pink-500/30" };
  if (rank <= 5) return { name: "Master Architect", color: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30" };
  if (rating >= 2500) return { name: "Diamond Stack", color: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30" };
  if (rating >= 2000) return { name: "Gold Tech", color: "bg-amber-500/15 text-amber-400 border-amber-500/30" };
  if (rating >= 1500) return { name: "Silver Developer", color: "bg-slate-400/15 text-slate-300 border-slate-400/30" };
  return { name: "Bronze Apprentice", color: "bg-orange-950/20 text-orange-400 border-orange-900/30" };
};

function ProfilePage() {
  const { username } = useParams();
  const { user: actual_user } = useSelector((state) => state.user);

  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [aiEvaluation, setAiEvaluation] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState(null);

  const [followLoading, setFollowLoading] = useState(false);

  const handleFollowToggle = async () => {
    if (!profileData || !profileData.user) return;
    const { user } = profileData;
    setFollowLoading(true);
    const action = user.is_following ? "unfollow" : "follow";
    try {
      const response = await API.post(`/api/profile/${user.username}/${action}`);
      if (response.data.success) {
        setProfileData((prev) => ({
          ...prev,
          user: {
            ...prev.user,
            is_following: !user.is_following,
            followers_count: user.is_following
              ? Math.max(0, (user.followers_count || 0) - 1)
              : (user.followers_count || 0) + 1,
          },
        }));
        toast.success(response.data.message || `Successfully ${action}ed user.`);
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || `Failed to ${action} user.`);
    } finally {
      setFollowLoading(false);
    }
  };

  const handleShare = async () => {
    const profileUrl = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${profileData?.user?.username || 'Developer'}'s Profile - Interleet`,
          text: `Check out ${profileData?.user?.username || 'this developer'}'s profile on Interleet!`,
          url: profileUrl,
        });
      } catch (err) {
        if (err.name !== "AbortError") {
          toast.error("Failed to share profile.");
        }
      }
    } else {
      try {
        await navigator.clipboard.writeText(profileUrl);
        toast.success("Profile link copied to clipboard!");
      } catch (err) {
        toast.error("Failed to copy link.");
      }
    }
  };



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
        {/* Mock Banner skeleton */}
        <div className="relative border-b border-border bg-card/10 animate-pulse">
          <div className="relative mx-auto flex max-w-6xl flex-col gap-5 px-4 py-8 md:flex-row md:items-end md:px-8">
            <div className="h-20 w-20 rounded-full bg-zinc-800/40 shrink-0" />
            <div className="flex-1 space-y-2">
              <div className="h-6 w-48 rounded bg-zinc-800/40" />
              <div className="h-4 w-32 rounded bg-zinc-800/20" />
              <div className="h-3 w-64 rounded bg-zinc-800/20 mt-2" />
            </div>
            <div className="flex gap-2 shrink-0">
              <div className="h-8 w-16 rounded bg-zinc-800/40" />
              <div className="h-8 w-24 rounded bg-zinc-800/40" />
            </div>
          </div>
        </div>

        {/* Mock stats grid skeleton */}
        <div className="mx-auto max-w-6xl px-4 py-6 md:px-8 space-y-6 animate-pulse">
          <div className="grid gap-4 md:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="border border-border bg-card/30 p-4 rounded-lg space-y-2">
                <div className="h-2.5 w-24 rounded bg-zinc-800/40" />
                <div className="h-6 w-16 rounded bg-zinc-800/30" />
              </div>
            ))}
          </div>

          {/* Main content grid placeholder */}
          <div className="grid gap-4 lg:grid-cols-3">
            <div className="border border-border bg-card/30 p-5 rounded-lg lg:col-span-2 h-64 space-y-4">
              <div className="h-4 w-36 rounded bg-zinc-800/40" />
              <div className="space-y-3 pt-2">
                <div className="h-2.5 w-full rounded bg-zinc-800/20" />
                <div className="h-2.5 w-5/6 rounded bg-zinc-800/20" />
                <div className="h-2.5 w-4/5 rounded bg-zinc-800/20" />
              </div>
            </div>
            <div className="border border-border bg-card/30 p-5 rounded-lg h-64 space-y-4">
              <div className="h-4 w-28 rounded bg-zinc-800/40" />
              <div className="h-32 rounded bg-zinc-800/10 border border-dashed border-zinc-800" />
            </div>
          </div>
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

  const { user, challenges, interviews_history, badge_progress: badgeProgress } = profileData;
  const level = Math.floor((user.xp || 0) / 1000) + 1;
  const xpInLevel = (user.xp || 0) % 1000;
  const progress = (xpInLevel / 1000) * 100;
  const division = getDivisionTier(user.rating, user.rank);

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
      {/* Banner */}
      <div className="relative border-b border-border">
        <div className="grid-bg absolute inset-0 opacity-30" />
        <div className="pointer-events-none absolute -top-20 left-1/3 h-[300px] w-[500px] rounded-full bg-primary/10 blur-3xl" />
        <div className="relative mx-auto flex max-w-6xl flex-col gap-5 px-4 py-8 md:flex-row md:items-end md:px-8">
          <div className="relative flex-shrink-0">
            <Avatar className={`h-20 w-20 border-2 bg-card ${user.is_premium ? "border-[#FF6500]" : "border-border"}`}>
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
            {user.is_premium && (
              <span className="absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-[#FF6500] text-[10px] font-black text-white border-2 border-background shadow-md">
                ★
              </span>
            )}
          </div>
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-2xl font-semibold tracking-tight text-white">
                {user.name}
              </h1>
              {user.is_premium && (
                <Badge variant="outline" className="bg-[#FF6500]/10 border-[#FF6500]/30 text-[#FF6500] text-xs font-black uppercase tracking-wider px-2 py-0.5">
                  Pro
                </Badge>
              )}
              <Badge className="gap-1 bg-success/15 text-success border border-success/30">
                <ShieldCheck className="h-3 w-3" />
                Verified
              </Badge>
            </div>
            <div className="flex flex-wrap items-center gap-2 mt-1">
              <p className="text-sm text-muted-foreground">@{user.username}</p>
              <Badge className="font-mono text-[10px] bg-primary/10 text-primary border border-primary/20">
                Level {level}
              </Badge>
              <Badge className={`font-mono text-[10px] border ${division.color}`}>
                {division.name}
              </Badge>
              <div className="flex items-center gap-3 ml-2 text-xs text-muted-foreground">
                <span>
                  <strong className="text-white font-semibold">{user.following_count || 0}</strong> following
                </span>
                <span>
                  <strong className="text-white font-semibold">{user.followers_count || 0}</strong> followers
                </span>
              </div>
            </div>
            <div className="mt-2 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
              {user.location && (
                <span className="inline-flex items-center gap-1">
                  <MapPin className="h-3.5 w-3.5" />
                  {user.location}
                </span>
              )}
              {user.github_username && (
                <span className="inline-flex items-center gap-1">
                  <Github className="h-3.5 w-3.5" />
                  <a
                    href={`https://github.com/${user.github_username}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-primary transition-colors"
                  >
                    {user.github_username}
                  </a>
                </span>
              )}
              {user.website && (
                <span className="inline-flex items-center gap-1">
                  <LinkIcon className="h-3.5 w-3.5" />
                  <a
                    href={user.website.startsWith("http") ? user.website : `https://${user.website}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-primary transition-colors"
                  >
                    {user.website.replace(/^https?:\/\/(www\.)?/, "")}
                  </a>
                </span>
              )}
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={handleShare}>Share</Button>
            {actual_user?.username === user.username ? (
              <Button size="sm" asChild>
                <Link to="/app/settings?tab=profile">Edit Profile</Link>
              </Button>
            ) : (
              <Button
                size="sm"
                onClick={handleFollowToggle}
                disabled={followLoading}
                className={user.is_following ? "bg-zinc-800 hover:bg-zinc-700 text-white" : "bg-[#FF6500] hover:bg-[#E05900] text-white"}
              >
                {followLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin mr-1" />
                ) : user.is_following ? (
                  "Unfollow"
                ) : (
                  "Follow"
                )}
              </Button>
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

          <TabsContent value="overview" className="mt-4 space-y-4">
            <div className="grid gap-4 lg:grid-cols-3">
              {/* Domain proficiency */}
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

              {/* Level Progress Card */}
              <Card className="border-border bg-card p-5 lg:col-span-1 relative overflow-hidden group">
                {/* Radial Glow */}
                <div className="absolute -right-12 -top-12 h-36 w-36 rounded-full bg-primary/10 blur-3xl opacity-60 group-hover:opacity-100 transition-opacity" />

                <div className="relative flex items-center justify-between border-b border-zinc-850 pb-3">
                  <div>
                    <h3 className="text-sm font-bold text-white tracking-wide">Arena Level</h3>
                    <p className="text-[10px] text-muted-foreground mt-0.5 font-mono">XP PROGRESSION</p>
                  </div>
                  <Badge className="bg-primary/10 text-primary border border-primary/20 font-mono text-[10px] uppercase">
                    Tier {level}
                  </Badge>
                </div>

                <div className="relative mt-6 flex flex-col items-center justify-center">
                  {/* Circle SVG */}
                  <div className="relative h-28 w-28 flex items-center justify-center">
                    <svg className="absolute inset-0 h-full w-full -rotate-90">
                      {/* Gray track */}
                      <circle
                        cx="56"
                        cy="56"
                        r="44"
                        className="stroke-zinc-850"
                        strokeWidth="6"
                        fill="transparent"
                      />
                      {/* Orange progress */}
                      <circle
                        cx="56"
                        cy="56"
                        r="44"
                        className="stroke-primary transition-all duration-1000 ease-out"
                        strokeWidth="6"
                        fill="transparent"
                        strokeDasharray={2 * Math.PI * 44}
                        strokeDashoffset={2 * Math.PI * 44 * (1 - progress / 100)}
                        strokeLinecap="round"
                      />
                    </svg>
                    {/* Inner Content */}
                    <div className="text-center z-10">
                      <span className="text-2xl font-black text-white">{progress.toFixed(0)}%</span>
                      <p className="text-[8px] text-muted-foreground font-mono uppercase tracking-wider mt-0.5">Progress</p>
                    </div>
                  </div>

                  <p className="mt-5 text-center text-xs font-medium text-white font-mono">
                    {xpInLevel} <span className="text-zinc-500">/ 1000 XP</span>
                  </p>
                </div>

                {/* Sub Stats Grid */}
                <div className="mt-6 grid grid-cols-2 gap-3 border-t border-zinc-850 pt-4 text-xs font-mono">
                  <div className="bg-zinc-950/30 rounded p-2.5 border border-zinc-850/40">
                    <span className="text-zinc-500 text-[9px] uppercase block">Total XP</span>
                    <span className="font-bold text-white text-sm mt-0.5 block">{user.xp || 0}</span>
                  </div>
                  <div className="bg-zinc-950/30 rounded p-2.5 border border-zinc-850/40">
                    <span className="text-zinc-500 text-[9px] uppercase block">Next Tier</span>
                    <span className="font-bold text-primary text-sm mt-0.5 block">+{1000 - xpInLevel} XP</span>
                  </div>
                </div>
              </Card>
            </div>

            {/* Contribution Heatmap Card (Full width) */}
            <Card className="border-border bg-card p-5 relative overflow-hidden group">
              <div className="absolute -left-12 -bottom-12 h-36 w-36 rounded-full bg-primary/5 blur-3xl opacity-40 group-hover:opacity-100 transition-opacity" />
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-zinc-850 pb-3 mb-5">
                <div>
                  <h3 className="text-sm font-bold text-white tracking-wide">Contribution heatmap</h3>
                  <p className="text-[10px] text-muted-foreground mt-0.5 font-mono uppercase tracking-wider">365-DAY ACTIVITY LEDGER</p>
                </div>
              </div>
              <div className="overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-zinc-800">
                <div className="min-w-[720px] pr-4 relative">
                  <ContributionHeatmap heatmap={user.heatmap || {}} />
                </div>
              </div>
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

          <TabsContent value="badges" className="mt-4">
            <div className="space-y-6">
              {/* Earned Badges Grid */}
              <div>
                <h4 className="text-sm font-semibold text-white mb-3">Earned Achievements</h4>
                {badgeProgress?.earned && badgeProgress.earned.length > 0 ? (
                  <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-4">
                    {badgeProgress.earned.map((b) => {
                      const glowColor = 
                        b.rarity === "Legendary" ? "shadow-[0_0_15px_rgba(250,204,21,0.2)] border-yellow-500/40" :
                        b.rarity === "Epic" ? "shadow-[0_0_15px_rgba(168,85,247,0.2)] border-purple-500/40" :
                        b.rarity === "Rare" ? "shadow-[0_0_15px_rgba(59,130,246,0.2)] border-blue-500/40" :
                        "border-zinc-800";
                      
                      const rarityBadge = 
                        b.rarity === "Legendary" ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20" :
                        b.rarity === "Epic" ? "bg-purple-500/10 text-purple-400 border-purple-500/20" :
                        b.rarity === "Rare" ? "bg-blue-500/10 text-blue-400 border-blue-500/20" :
                        "bg-zinc-800/50 text-zinc-400 border-zinc-700/30";

                      return (
                        <Card key={b.id} className={`relative overflow-hidden flex flex-col justify-between border bg-card p-4 hover:border-zinc-700 transition-all duration-300 ${glowColor}`}>
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              {b.image_url ? (
                                <img src={b.image_url} alt={b.name} className="w-10 h-10 object-contain hover:scale-110 transition-transform duration-200" />
                              ) : (
                                <span className="text-2xl">{b.icon || "🏆"}</span>
                              )}
                              <Badge className={`text-[9px] font-mono border ${rarityBadge}`}>
                                {b.rarity}
                              </Badge>
                            </div>
                            <h5 className="text-sm text-white font-semibold mb-1">{b.name}</h5>
                            <p className="text-xs text-muted-foreground mb-3">{b.description}</p>
                          </div>
                          <div className="text-[10px] text-primary font-mono mt-auto flex justify-between items-center border-t border-white/[0.04] pt-2">
                            <span>+{b.xp_reward} XP</span>
                            <span className="text-muted-foreground">Earned</span>
                          </div>
                        </Card>
                      );
                    })}
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center p-8 border border-dashed border-zinc-800 rounded bg-zinc-950/20 text-center">
                    <p className="text-xs text-muted-foreground">No badges earned yet. Solve challenges to earn your first milestone!</p>
                  </div>
                )}
              </div>

              {/* Locked/Progress Badges Grid */}
              {badgeProgress?.locked && badgeProgress.locked.length > 0 && (
                <div>
                  <h4 className="text-sm font-semibold text-white mb-3">Locked Achievements</h4>
                  <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-4">
                    {badgeProgress.locked.map((b) => (
                      <Card key={b.id} className="relative overflow-hidden flex flex-col justify-between border border-zinc-900 bg-card/45 p-4 opacity-75 hover:opacity-100 transition-opacity">
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            {b.image_url ? (
                              <img src={b.image_url} alt={b.name} className="w-10 h-10 object-contain filter grayscale opacity-45 hover:opacity-85 transition-all duration-200" />
                            ) : (
                              <span className="text-2xl filter grayscale opacity-60">{b.icon || "🏆"}</span>
                            )}
                            <div className="flex items-center gap-1 text-[10px] text-muted-foreground font-mono">
                              <Lock className="w-3 h-3" />
                              <span>{b.progress}%</span>
                            </div>
                          </div>
                          <h5 className="text-sm text-zinc-400 font-semibold mb-1">{b.name}</h5>
                          <p className="text-xs text-zinc-500 mb-3">{b.description}</p>
                        </div>
                        <div className="space-y-1.5 mt-auto pt-2 border-t border-white/[0.04]">
                          <Progress value={b.progress} className="h-1 bg-zinc-850" />
                          <div className="flex justify-between text-[9px] font-mono text-zinc-500">
                            <span>+{b.xp_reward} XP</span>
                            <span>Locked</span>
                          </div>
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
            </div>
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
