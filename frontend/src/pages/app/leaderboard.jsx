import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { TrendingUp, TrendingDown, Minus, Flame, Sparkles } from "lucide-react";
import { API } from "@/api/api";
import { leaderboard as mockLeaderboard } from "@/lib/mock";

/* ─── Helpers ─────────────────────────────────────────────── */
const getDivisionTier = (rating, rank) => {
  if (rank === 1) return { name: "Grandmaster Elite", color: "bg-purple-500/15 text-purple-400 border-purple-500/30" };
  if (rank <= 3) return { name: "Grandmaster", color: "bg-pink-500/15 text-pink-400 border-pink-500/30" };
  if (rank <= 5) return { name: "Master Architect", color: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30" };
  if (rating >= 2500) return { name: "Diamond Stack", color: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30" };
  if (rating >= 2000) return { name: "Gold Tech", color: "bg-amber-500/15 text-amber-400 border-amber-500/30" };
  if (rating >= 1500) return { name: "Silver Developer", color: "bg-slate-400/15 text-slate-300 border-slate-400/30" };
  return { name: "Bronze Apprentice", color: "bg-orange-950/20 text-orange-400 border-orange-900/30" };
};


/* ─── Trophy SVG Components ───────────────────────────────── */
const TrophyGold = () => (
  <svg viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-16 h-16 drop-shadow-2xl">
    <defs>
      <radialGradient id="tg1" cx="50%" cy="30%" r="60%">
        <stop offset="0%" stopColor="#FFE066" />
        <stop offset="60%" stopColor="#FFB800" />
        <stop offset="100%" stopColor="#B8860B" />
      </radialGradient>
      <radialGradient id="tg2" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#FFF3A0" />
        <stop offset="100%" stopColor="#FFB800" />
      </radialGradient>
    </defs>
    {/* cup body */}
    <path d="M20 8 H60 L55 45 Q40 55 25 45 Z" fill="url(#tg1)" />
    {/* handles */}
    <path d="M20 15 Q8 20 10 32 Q12 42 22 40" stroke="#B8860B" strokeWidth="4" fill="none" strokeLinecap="round" />
    <path d="M60 15 Q72 20 70 32 Q68 42 58 40" stroke="#B8860B" strokeWidth="4" fill="none" strokeLinecap="round" />
    {/* shine */}
    <ellipse cx="32" cy="22" rx="5" ry="8" fill="url(#tg2)" opacity="0.55" transform="rotate(-15 32 22)" />
    {/* stem */}
    <rect x="34" y="55" width="12" height="14" rx="2" fill="#B8860B" />
    {/* base */}
    <rect x="24" y="69" width="32" height="6" rx="3" fill="#FFB800" />
    {/* medal circle */}
    <circle cx="40" cy="30" r="9" fill="#FFF3A0" opacity="0.9" />
    <text x="40" y="34" textAnchor="middle" fontSize="11" fontWeight="bold" fill="#B8860B">1</text>
    {/* sparkle dots */}
    <circle cx="14" cy="10" r="2" fill="#FFE066" opacity="0.8" />
    <circle cx="66" cy="8" r="1.5" fill="#FFE066" opacity="0.7" />
    <circle cx="68" cy="50" r="1.5" fill="#FFE066" opacity="0.6" />
  </svg>
);

const TrophySilver = () => (
  <svg viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-12 h-12 drop-shadow-lg">
    <defs>
      <radialGradient id="ts1" cx="50%" cy="30%" r="60%">
        <stop offset="0%" stopColor="#E8E8E8" />
        <stop offset="60%" stopColor="#A8A8A8" />
        <stop offset="100%" stopColor="#606060" />
      </radialGradient>
    </defs>
    <path d="M20 8 H60 L55 45 Q40 55 25 45 Z" fill="url(#ts1)" />
    <path d="M20 15 Q8 20 10 32 Q12 42 22 40" stroke="#606060" strokeWidth="4" fill="none" strokeLinecap="round" />
    <path d="M60 15 Q72 20 70 32 Q68 42 58 40" stroke="#606060" strokeWidth="4" fill="none" strokeLinecap="round" />
    <ellipse cx="32" cy="22" rx="5" ry="8" fill="white" opacity="0.4" transform="rotate(-15 32 22)" />
    <rect x="34" y="55" width="12" height="14" rx="2" fill="#808080" />
    <rect x="24" y="69" width="32" height="6" rx="3" fill="#A8A8A8" />
    <circle cx="40" cy="30" r="9" fill="white" opacity="0.75" />
    <text x="40" y="34" textAnchor="middle" fontSize="11" fontWeight="bold" fill="#606060">2</text>
  </svg>
);

const TrophyBronze = () => (
  <svg viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-11 h-11 drop-shadow-lg">
    <defs>
      <radialGradient id="tb1" cx="50%" cy="30%" r="60%">
        <stop offset="0%" stopColor="#E8A87C" />
        <stop offset="60%" stopColor="#CD7F32" />
        <stop offset="100%" stopColor="#7B4A1E" />
      </radialGradient>
    </defs>
    <path d="M20 8 H60 L55 45 Q40 55 25 45 Z" fill="url(#tb1)" />
    <path d="M20 15 Q8 20 10 32 Q12 42 22 40" stroke="#7B4A1E" strokeWidth="4" fill="none" strokeLinecap="round" />
    <path d="M60 15 Q72 20 70 32 Q68 42 58 40" stroke="#7B4A1E" strokeWidth="4" fill="none" strokeLinecap="round" />
    <ellipse cx="32" cy="22" rx="5" ry="8" fill="#E8A87C" opacity="0.5" transform="rotate(-15 32 22)" />
    <rect x="34" y="55" width="12" height="14" rx="2" fill="#7B4A1E" />
    <rect x="24" y="69" width="32" height="6" rx="3" fill="#CD7F32" />
    <circle cx="40" cy="30" r="9" fill="#E8A87C" opacity="0.8" />
    <text x="40" y="34" textAnchor="middle" fontSize="11" fontWeight="bold" fill="#7B4A1E">3</text>
  </svg>
);

/* ─── Podium Card Component ───────────────────────────────── */
const PodiumCard = ({ userData, spot, visible }) => {
  const isFirst = spot === 1;
  const isSecond = spot === 2;

  const delay = spot === 1 ? "0ms" : spot === 2 ? "150ms" : "300ms";
  const translateY = spot === 1 ? "-translate-y-6" : "";
  const podiumHeight = isFirst ? "h-28" : isSecond ? "h-20" : "h-14";
  const podiumGradient = isFirst
    ? "from-yellow-600/50 to-yellow-900/60 border-yellow-500/40"
    : isSecond
      ? "from-zinc-600/50 to-zinc-800/60 border-zinc-600/40"
      : "from-amber-900/50 to-amber-950/60 border-amber-700/40";
  const ringColor = isFirst
    ? "ring-yellow-500/40 border-yellow-500/60 shadow-[0_0_30px_rgba(255,184,0,0.25)]"
    : isSecond
      ? "ring-zinc-500/30 border-zinc-500/40"
      : "ring-amber-700/30 border-amber-700/40";
  const avatarBorder = isFirst ? "border-yellow-500" : isSecond ? "border-zinc-400" : "border-amber-700";
  const avatarSize = isFirst ? "h-20 w-20 md:h-16 md:w-16" : "h-16 w-16 md:h-12 md:w-12";
  const labelColor = isFirst ? "text-yellow-400" : isSecond ? "text-zinc-300" : "text-amber-600";
  const podiumNumeral = isFirst ? "I" : isSecond ? "II" : "III";
  const podiumNumeralColor = isFirst ? "text-yellow-400" : isSecond ? "text-zinc-400" : "text-amber-700";
  const podiumNumeralSize = isFirst ? "text-4xl" : isSecond ? "text-3xl" : "text-2xl";

  return (
    <div
      className={`flex flex-col items-center flex-1 max-w-[260px] md:max-w-[260px] min-w-0 w-full group transition-all duration-700 ease-out ${translateY} ${
        visible
          ? "opacity-100 translate-y-0 scale-100"
          : "opacity-0 translate-y-10 scale-95"
      }`}
      style={{
        transitionDelay: delay,
        transform: visible
          ? spot === 1
            ? "translateY(-1.5rem)"
            : "translateY(0)"
          : "translateY(2.5rem) scale(0.95)",
      }}
    >
      {/* Trophy */}
      <div
        className={`mb-2 flex flex-col items-center transition-all duration-700 ease-out ${
          visible ? "opacity-100 scale-100" : "opacity-0 scale-50"
        }`}
        style={{ transitionDelay: `${parseInt(delay) + 200}ms` }}
      >
        <div className={isFirst ? "scale-125 md:scale-100" : "scale-110 md:scale-100"}>
          {isFirst ? <TrophyGold /> : isSecond ? <TrophySilver /> : <TrophyBronze />}
        </div>
        <span className={`text-xs md:text-[11px] font-mono font-bold tracking-widest mt-1 ${labelColor}`}>
          {isFirst ? "Champion" : isSecond ? "2nd Place" : "3rd Place"}
        </span>
      </div>

      {/* Card */}
      <Card
        className={`w-full ${isFirst ? "p-5 md:p-5" : "p-4 md:p-4"} text-center transition-all duration-300 group-hover:-translate-y-1 shadow-xl ring-1 border bg-zinc-950/70 ${ringColor}`}
      >
        <Avatar className={`${avatarSize} mx-auto border-2 ${avatarBorder} shadow-lg`}>
          <AvatarImage src={userData.avatar} />
          <AvatarFallback className={`${isFirst ? "bg-yellow-950 text-yellow-300" : "bg-zinc-800 text-zinc-200"} font-bold ${isFirst ? "text-base" : "text-sm"}`}>
            {userData.username.slice(0, 2).toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <p className={`mt-3 truncate font-extrabold text-white ${isFirst ? "text-base" : "text-sm md:text-sm"}`}>
          @{userData.username}
        </p>
        <p className={`text-xs mt-0.5 font-semibold ${isFirst ? "text-yellow-400" : "text-muted-foreground"}`}>
          Rating {userData.rating}
        </p>
        <div
          className={`mt-3 inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-mono border
            ${isFirst
              ? "bg-yellow-950/20 border-yellow-500/25 text-yellow-400"
              : isSecond
                ? "bg-zinc-900 border-zinc-700 text-zinc-300"
                : "bg-zinc-900 border-zinc-700 text-zinc-400"
            }`}
        >
          {isFirst && <Sparkles className="h-3 w-3 text-yellow-500" />}
          {userData.xp.toLocaleString()} XP
        </div>
      </Card>

      {/* Podium Base */}
      <div
        className={`w-full ${podiumHeight} bg-gradient-to-b ${podiumGradient} border-t rounded-t-md flex items-center justify-center mt-2`}
      >
        <span className={`font-mono font-black ${podiumNumeralSize} ${podiumNumeralColor}`}>
          {podiumNumeral}
        </span>
      </div>
    </div>
  );
};

/* ─── Main Component ──────────────────────────────────────── */
function Leaderboard() {
  const { user } = useSelector((state) => state.user);
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [podiumVisible, setPodiumVisible] = useState(false);

  useEffect(() => {
    let isMounted = true;
    const fetchLeaderboard = async () => {
      try {
        const response = await API.get("/api/leaderboard");
        if (isMounted) {
          setLeaderboardData(response.data?.items || mockLeaderboard);
          setLoading(false);
        }
      } catch (err) {
        console.error("Failed to load live leaderboard, falling back to mock.", err);
        if (isMounted) {
          setLeaderboardData(mockLeaderboard);
          setLoading(false);
        }
      }
    };
    fetchLeaderboard();
    return () => { isMounted = false; };
  }, []);

  // Trigger pop-in once data loads
  useEffect(() => {
    if (!loading) {
      const t = setTimeout(() => setPodiumVisible(true), 120);
      return () => clearTimeout(t);
    }
  }, [loading]);

  const getPodiumList = () => {
    if (leaderboardData.length === 0) return [];
    const podium = [];
    if (leaderboardData[1]) podium.push({ ...leaderboardData[1], spot: 2 });
    if (leaderboardData[0]) podium.push({ ...leaderboardData[0], spot: 1 });
    if (leaderboardData[2]) podium.push({ ...leaderboardData[2], spot: 3 });
    return podium;
  };

  if (loading) {
    return (
      <AppShell>
        <PageHeader
          title="Leaderboard"
          description="Rated by domain. Ranked weekly. Climb the arena."
        />
        <div className="px-0 pb-6 md:px-0 space-y-6">
          {/* Podium Skeleton */}
          <div className="relative flex flex-col items-center justify-center pt-8 pb-4 overflow-hidden border-b border-zinc-800/50">
            {/* Dot bg */}
            <div className="dot-bg pointer-events-none absolute inset-0 opacity-40" />
            <div className="flex items-center gap-2 mb-6 animate-pulse">
              <div className="h-4 w-40 rounded bg-zinc-800/40" />
            </div>

            {/* Podium Row Skeleton */}
            <div className="flex items-end justify-center gap-2 md:gap-6 w-full max-w-3xl px-6 md:px-20 relative z-10 animate-pulse">
              {/* 2nd spot */}
              <div className="flex flex-col items-center flex-1 max-w-[260px] w-full">
                <div className="h-16 w-16 rounded-full bg-zinc-800/40 mb-3" />
                <div className="h-28 w-full rounded-t-md bg-zinc-800/20 border-t border-zinc-700/30 flex items-center justify-center">
                  <span className="text-xl font-mono font-black text-zinc-700">II</span>
                </div>
              </div>
              
              {/* 1st spot */}
              <div className="flex flex-col items-center flex-1 max-w-[260px] w-full -translate-y-6">
                <div className="h-20 w-20 rounded-full bg-zinc-800/40 mb-3" />
                <div className="h-36 w-full rounded-t-md bg-zinc-800/30 border-t border-zinc-700/40 flex items-center justify-center">
                  <span className="text-2xl font-mono font-black text-zinc-600">I</span>
                </div>
              </div>

              {/* 3rd spot */}
              <div className="flex flex-col items-center flex-1 max-w-[260px] w-full">
                <div className="h-16 w-16 rounded-full bg-zinc-800/40 mb-3" />
                <div className="h-20 w-full rounded-t-md bg-zinc-800/20 border-t border-zinc-700/30 flex items-center justify-center">
                  <span className="text-lg font-mono font-black text-zinc-700">III</span>
                </div>
              </div>
            </div>
          </div>

          <div className="px-4 md:px-8 space-y-6">
            {/* Spotlight Banner Skeleton */}
            <div className="h-16 w-full rounded-xl border border-zinc-800/50 bg-card/30 p-4 animate-pulse flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="h-10 w-10 rounded-full bg-zinc-800/40 shrink-0" />
                <div className="space-y-2">
                  <div className="h-4 w-32 rounded bg-zinc-800/40" />
                  <div className="h-3 w-48 rounded bg-zinc-800/20" />
                </div>
              </div>
              <div className="flex gap-4">
                <div className="h-8 w-16 rounded bg-zinc-800/25" />
                <div className="h-8 w-16 rounded bg-zinc-800/25" />
              </div>
            </div>

            {/* List/Table Skeleton */}
            <div className="rounded-xl border border-border bg-card p-0 shadow-xl animate-pulse">
              {/* Table header skeleton */}
              <div className="h-10 bg-zinc-900/80 border-b border-border w-full flex items-center px-5 gap-4">
                <div className="h-3 w-10 bg-zinc-800/30 rounded" />
                <div className="h-3 w-32 bg-zinc-800/30 rounded" />
                <div className="h-3 w-24 bg-zinc-800/30 rounded mx-auto" />
                <div className="h-3 w-16 bg-zinc-800/30 rounded mx-auto" />
                <div className="h-3 w-20 bg-zinc-800/30 rounded mx-auto" />
              </div>

              {/* Table rows skeleton */}
              <div className="divide-y divide-border">
                {Array.from({ length: 6 }).map((_, idx) => (
                  <div key={idx} className="h-14 flex items-center px-5 gap-4">
                    <div className="h-4 w-6 bg-zinc-800/40 rounded shrink-0" />
                    <div className="flex items-center gap-3 flex-1">
                      <div className="h-8 w-8 rounded-full bg-zinc-800/40 shrink-0" />
                      <div className="space-y-1.5 flex-1 max-w-[120px]">
                        <div className="h-3.5 w-full bg-zinc-800/40 rounded" />
                        <div className="h-2.5 w-2/3 bg-zinc-800/20 rounded" />
                      </div>
                    </div>
                    <div className="h-5 w-20 bg-zinc-800/30 rounded shrink-0 mx-auto" />
                    <div className="h-4 w-12 bg-zinc-800/40 rounded shrink-0 mx-auto" />
                    <div className="h-4 w-16 bg-zinc-800/30 rounded shrink-0 mx-auto" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  const podiumUsers = getPodiumList();
  const spotlightUser = user ? leaderboardData.find(u => u.username === user.username) : null;

  return (
    <AppShell>
      <PageHeader
        title="Leaderboard"
        description="Rated by domain. Ranked weekly. Climb the arena."
      />
      <div className="px-0 pb-6 md:px-0 space-y-6">

        {/* ── Podium Section ── */}
        {podiumUsers.length > 0 && (
          <div className="relative flex flex-col items-center justify-center pt-8 pb-4 overflow-hidden border-b border-zinc-800/50">

            {/* Dot bg — exact homepage hero pattern */}
            <div className="dot-bg pointer-events-none absolute inset-0 opacity-40" />
            {/* Orange radial glow — exact homepage hero gradient */}
            <div
              className="pointer-events-none absolute inset-x-0 -top-32 h-[500px] bg-[radial-gradient(ellipse_at_top,theme(colors.primary/15),transparent_60%)]"
              aria-hidden
            />


            {/* Title with sparkle */}
            <div
              className={`flex items-center gap-2 mb-6 transition-all duration-700 ${podiumVisible ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-4"}`}
            >
              <Sparkles className="h-4 w-4 text-yellow-500 animate-pulse" />
              <span className="text-xs font-mono font-bold tracking-[0.25em] uppercase text-yellow-500/80">
                Hall of Champions
              </span>
              <Sparkles className="h-4 w-4 text-yellow-500 animate-pulse" />
            </div>

            {/* Podium Row */}
            <div className="flex items-end justify-center gap-2 md:gap-6 w-full max-w-3xl px-6 md:px-20 relative z-10">
              {podiumUsers.map((u) => (
                <PodiumCard
                  key={u.username}
                  userData={u}
                  spot={u.spot}
                  visible={podiumVisible}
                />
              ))}
            </div>
          </div>
        )}

        {/* ── Below-podium content wrapper ── */}
        <div className="px-4 md:px-8 space-y-6">

        {/* ── User Spotlight Banner ── */}
        {user && (
          <Card className="border-[#FF6500]/25 bg-gradient-to-r from-[#FF6500]/5 via-zinc-950 to-[#FF6500]/5 p-4 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-lg glow-soft">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#FF6500]/15 border border-[#FF6500]/30 text-[#FF6500]">
                <Flame className="h-6 w-6 animate-pulse" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-white">Your Standing in the Arena</h4>
                <p className="text-xs text-muted-foreground mt-0.5">
                  {spotlightUser
                    ? `You are ranked #${spotlightUser.rank} with ${spotlightUser.rating} rating. Keep solving challenges to climb higher!`
                    : `You are ranked #${user.rank || "Unranked"} with ${user.rating || 0} rating. Climb the Leaderboard!`
                  }
                </p>
              </div>
            </div>

            <div className="flex items-center gap-6">
              <div className="text-center sm:text-right">
                <span className="block text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Rating</span>
                <span className="text-lg font-bold text-white">{user.rating || 0}</span>
              </div>
              <div className="text-center sm:text-right">
                <span className="block text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Level</span>
                <span className="text-lg font-bold text-[#FF6500]">{Math.floor((user.xp || 0) / 1000) + 1}</span>
              </div>
              <div className="text-center sm:text-right">
                <span className="block text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Streak</span>
                <span className="text-lg font-bold text-chart-3 inline-flex items-center gap-1">
                  <Flame className="h-4 w-4 fill-chart-3" />
                  {user.streak_count || user.streak || 0}d
                </span>
              </div>
            </div>
          </Card>
        )}

        {/* ── Leaderboard Lists ── */}
        <Tabs defaultValue="global" className="w-full">
          <div className="flex justify-between items-center border-b border-zinc-800 pb-2">
            <TabsList className="bg-zinc-900 border border-zinc-800">
              <TabsTrigger value="global" className="font-semibold">Global Arena</TabsTrigger>
              <TabsTrigger value="weekly" className="font-semibold">Weekly Sprint</TabsTrigger>
              <TabsTrigger value="friends" className="font-semibold">Clan / Friends</TabsTrigger>
            </TabsList>
            <Badge variant="outline" className="font-mono text-xs text-muted-foreground py-1 bg-zinc-900 border-zinc-800">
              Updated hourly
            </Badge>
          </div>

          {["global", "weekly", "friends"].map((tab) => (
            <TabsContent key={tab} value={tab} className="mt-4">
              <Card className="overflow-hidden border-border bg-card p-0 shadow-xl">

                {/* Desktop view */}
                <div className="hidden md:block">
                  <table className="w-full text-sm">
                    <thead className="bg-zinc-900/80 text-left text-xs text-muted-foreground">
                      <tr>
                        <th className="px-5 py-3.5 font-mono uppercase tracking-wider w-[80px] text-center">Rank</th>
                        <th className="px-5 py-3.5 font-mono uppercase tracking-wider">Developer</th>
                        <th className="px-5 py-3.5 font-mono uppercase tracking-wider text-center">Division Tier</th>
                        <th className="px-5 py-3.5 font-mono uppercase tracking-wider text-center">Rating</th>
                        <th className="px-5 py-3.5 font-mono uppercase tracking-wider text-center">Total XP</th>
                        <th className="px-5 py-3.5 font-mono uppercase tracking-wider">Achievements</th>
                        <th className="px-5 py-3.5 text-right font-mono uppercase tracking-wider">7d Change</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                      {leaderboardData.length === 0 ? (
                        <tr>
                          <td colSpan="7" className="py-12 text-center text-muted-foreground">
                            No active participants in this arena yet.
                          </td>
                        </tr>
                      ) : (
                        leaderboardData.map((row) => {
                          const isSelf = user && row.username === user.username;
                          const tier = getDivisionTier(row.rating, row.rank);
                          return (
                            <tr
                              key={row.username}
                              className={`border-t border-border hover:bg-zinc-900/40 transition-colors ${isSelf ? "bg-[#FF6500]/5 border-l-2 border-l-[#FF6500]" : ""}`}
                            >
                              <td className="px-5 py-4 text-center">
                                <span className={`inline-flex items-center justify-center font-mono font-bold text-sm w-7 h-7 rounded-full ${
                                  row.rank === 1 ? "bg-yellow-500/15 text-yellow-400" :
                                  row.rank === 2 ? "bg-zinc-300/15 text-zinc-300" :
                                  row.rank === 3 ? "bg-amber-700/20 text-amber-500" :
                                  "text-muted-foreground"
                                }`}>
                                  #{row.rank}
                                </span>
                              </td>
                              <td className="px-5 py-4">
                                <div className="flex items-center gap-3">
                                  <Avatar className="h-8 w-8 border border-border">
                                    <AvatarImage src={row.avatar} />
                                    <AvatarFallback className="text-xs bg-zinc-800 text-zinc-300 font-bold">
                                      {row.username.slice(0, 2).toUpperCase()}
                                    </AvatarFallback>
                                  </Avatar>
                                  <div>
                                    <p className="font-semibold text-white text-sm">@{row.username}</p>
                                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider">{row.country || "GLOBAL"}</p>
                                  </div>
                                </div>
                              </td>
                              <td className="px-5 py-4 text-center">
                                <Badge variant="outline" className={`font-mono text-[10px] px-2 py-0.5 border ${tier.color}`}>
                                  {tier.name}
                                </Badge>
                              </td>
                              <td className="px-5 py-4 text-center font-mono font-bold text-white">{row.rating}</td>
                              <td className="px-5 py-4 text-center font-mono text-zinc-300">{row.xp.toLocaleString()}</td>
                              <td className="px-5 py-4">
                                <div className="flex flex-wrap gap-1">
                                  {(row.badges || []).map((b) => (
                                    <Badge key={b} variant="outline" className="font-mono text-[9px] bg-zinc-900 border-zinc-800 text-zinc-400">
                                      {b}
                                    </Badge>
                                  ))}
                                </div>
                              </td>
                              <td className={`px-5 py-4 text-right font-mono font-semibold ${row.delta > 0 ? "text-success" : row.delta < 0 ? "text-destructive" : "text-muted-foreground"}`}>
                                <span className="inline-flex items-center gap-1 justify-end">
                                  {row.delta > 0 ? <TrendingUp className="h-3.5 w-3.5" /> : row.delta < 0 ? <TrendingDown className="h-3.5 w-3.5" /> : <Minus className="h-3.5 w-3.5" />}
                                  {row.delta > 0 ? `+${row.delta}` : row.delta}
                                </span>
                              </td>
                            </tr>
                          );
                        })
                      )}
                    </tbody>
                  </table>
                </div>

                {/* Mobile view */}
                <ul className="divide-y divide-border md:hidden">
                  {leaderboardData.length === 0 ? (
                    <li className="py-8 text-center text-muted-foreground">No active participants.</li>
                  ) : (
                    leaderboardData.map((row) => {
                      const isSelf = user && row.username === user.username;
                      const tier = getDivisionTier(row.rating, row.rank);
                      return (
                        <li
                          key={row.username}
                          className={`flex items-center gap-3 p-4 hover:bg-zinc-900/20 ${isSelf ? "bg-[#FF6500]/5 border-l-2 border-l-[#FF6500]" : ""}`}
                        >
                          <span className={`w-8 font-mono text-center font-bold text-xs ${
                            row.rank === 1 ? "text-yellow-500" :
                            row.rank === 2 ? "text-zinc-300" :
                            row.rank === 3 ? "text-amber-600" :
                            "text-muted-foreground"
                          }`}>
                            #{row.rank}
                          </span>
                          <Avatar className="h-9 w-9 border border-border shrink-0">
                            <AvatarImage src={row.avatar} />
                            <AvatarFallback className="text-[10px] bg-zinc-800 text-zinc-300 font-bold">
                              {row.username.slice(0, 2).toUpperCase()}
                            </AvatarFallback>
                          </Avatar>
                          <div className="min-w-0 flex-1">
                            <div className="flex items-center gap-2">
                              <p className="truncate text-sm font-semibold text-white">@{row.username}</p>
                              <Badge variant="outline" className={`font-mono text-[8px] px-1 border shrink-0 ${tier.color}`}>
                                {tier.name.split(" ")[0]}
                              </Badge>
                            </div>
                            <p className="text-xs text-muted-foreground">Rating {row.rating} · {row.xp.toLocaleString()} XP</p>
                          </div>
                          <span className={`font-mono text-xs font-bold ${row.delta >= 0 ? "text-success" : "text-destructive"}`}>
                            {row.delta >= 0 ? `+${row.delta}` : row.delta}
                          </span>
                        </li>
                      );
                    })
                  )}
                </ul>
              </Card>
            </TabsContent>
          ))}
        </Tabs>
        </div>{/* end px-4 md:px-8 wrapper */}
      </div>{/* end outer spacer */}
    </AppShell>
  );
}

export default Leaderboard;
