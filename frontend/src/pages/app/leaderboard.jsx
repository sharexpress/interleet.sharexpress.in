import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Trophy, TrendingUp, TrendingDown, Minus, Crown, Medal, Flame, Sparkles } from "lucide-react";
import { API } from "@/api/api";
import { leaderboard as mockLeaderboard } from "@/lib/mock";

const getDivisionTier = (rating, rank) => {
  if (rank === 1) return { name: "Grandmaster Elite", color: "bg-purple-500/15 text-purple-400 border-purple-500/30 glow-sm" };
  if (rank <= 3) return { name: "Grandmaster", color: "bg-pink-500/15 text-pink-400 border-pink-500/30" };
  if (rank <= 5) return { name: "Master Architect", color: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30" };
  if (rating >= 2500) return { name: "Diamond Stack", color: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30" };
  if (rating >= 2000) return { name: "Gold Tech", color: "bg-amber-500/15 text-amber-400 border-amber-500/30" };
  if (rating >= 1500) return { name: "Silver Developer", color: "bg-slate-400/15 text-slate-300 border-slate-400/30" };
  return { name: "Bronze Apprentice", color: "bg-orange-950/20 text-orange-400 border-orange-900/30" };
};

function Leaderboard() {
  const { user } = useSelector((state) => state.user);
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(true);

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
    return () => {
      isMounted = false;
    };
  }, []);

  // Podium sorting: 2nd Place, 1st Place, 3rd Place
  const getPodiumList = () => {
    if (leaderboardData.length === 0) return [];
    const podium = [];
    if (leaderboardData[1]) podium.push({ ...leaderboardData[1], spot: 2 });
    if (leaderboardData[0]) podium.push({ ...leaderboardData[0], spot: 1 });
    if (leaderboardData[2]) podium.push({ ...leaderboardData[2], spot: 3 });
    return podium;
  };

  const podiumUsers = getPodiumList();
  const spotlightUser = user ? leaderboardData.find(u => u.username === user.username) : null;

  return (
    <AppShell>
      <PageHeader
        title="Leaderboard"
        description="Rated by domain. Ranked weekly. Climb the arena."
      />
      <div className="px-4 py-6 md:px-8 space-y-8">

        {/* Visual Podium Section */}
        {!loading && podiumUsers.length > 0 && (
          <div className="flex flex-col items-center justify-center pt-8 pb-4 relative">
            <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent blur-3xl pointer-events-none" />

            <div className="flex items-end justify-center gap-3 md:gap-8 w-full max-w-4xl px-2">

              {/* 2nd Place - Silver */}
              {podiumUsers.find(u => u.spot === 2) && (
                <div className="flex flex-col items-center flex-1 max-w-[240px] group">
                  <div className="mb-3 text-center">
                    <Medal className="h-6 w-6 text-zinc-400 mx-auto animate-bounce duration-1000" />
                    <span className="text-xs font-mono font-semibold text-zinc-400">2nd Place</span>
                  </div>
                  <Card className="w-full border-zinc-700 bg-zinc-950/40 p-4 text-center transition-all duration-300 group-hover:-translate-y-1 group-hover:border-zinc-500 shadow-md">
                    <Avatar className="h-12 w-12 mx-auto border-2 border-zinc-400 shadow-lg">
                      <AvatarImage src={podiumUsers.find(u => u.spot === 2).avatar} />
                      <AvatarFallback className="bg-zinc-800 text-zinc-300 font-bold text-sm">
                        {podiumUsers.find(u => u.spot === 2).username.slice(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <p className="mt-3 truncate text-sm font-bold text-white">
                      @{podiumUsers.find(u => u.spot === 2).username}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      Rating {podiumUsers.find(u => u.spot === 2).rating}
                    </p>
                    <div className="mt-3 inline-flex items-center gap-1 bg-zinc-900 border border-zinc-800 px-2 py-0.5 rounded text-[10px] font-mono text-zinc-300">
                      {podiumUsers.find(u => u.spot === 2).xp.toLocaleString()} XP
                    </div>
                  </Card>
                  {/* Podium Base */}
                  <div className="w-full h-16 bg-gradient-to-b from-zinc-800/80 to-zinc-900/90 border-t border-zinc-700 rounded-t-md flex items-center justify-center mt-2 shadow-inner">
                    <span className="font-mono text-3xl font-extrabold text-zinc-500">II</span>
                  </div>
                </div>
              )}

              {/* 1st Place - Gold */}
              {podiumUsers.find(u => u.spot === 1) && (
                <div className="flex flex-col items-center flex-1 max-w-[260px] group relative z-10 -translate-y-4">
                  <div className="absolute -top-16 inset-x-0 h-40 bg-yellow-500/10 rounded-full blur-3xl pointer-events-none" />
                  <div className="mb-3 text-center">
                    <Crown className="h-8 w-8 text-yellow-500 mx-auto animate-pulse" />
                    <span className="text-xs font-mono font-bold text-yellow-500 tracking-wider">Champion</span>
                  </div>
                  <Card className="w-full border-yellow-500/50 bg-zinc-950/60 p-5 text-center transition-all duration-300 group-hover:-translate-y-1 group-hover:border-yellow-400 shadow-xl ring-1 ring-yellow-500/30">
                    <Avatar className="h-16 w-16 mx-auto border-2 border-yellow-500 shadow-2xl">
                      <AvatarImage src={podiumUsers.find(u => u.spot === 1).avatar} />
                      <AvatarFallback className="bg-yellow-950 text-yellow-400 font-bold text-base">
                        {podiumUsers.find(u => u.spot === 1).username.slice(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <p className="mt-3 truncate text-base font-extrabold text-white">
                      @{podiumUsers.find(u => u.spot === 1).username}
                    </p>
                    <p className="text-xs text-yellow-500 font-semibold mt-0.5">
                      Rating {podiumUsers.find(u => u.spot === 1).rating}
                    </p>
                    <div className="mt-3 inline-flex items-center gap-1 bg-yellow-950/20 border border-yellow-500/25 px-2.5 py-0.5 rounded text-[10px] font-mono text-yellow-400">
                      <Sparkles className="h-3 w-3 text-yellow-500 animate-spin duration-3000" />
                      {podiumUsers.find(u => u.spot === 1).xp.toLocaleString()} XP
                    </div>
                  </Card>
                  {/* Podium Base */}
                  <div className="w-full h-24 bg-gradient-to-b from-yellow-600/40 to-yellow-900/50 border-t border-yellow-500/40 rounded-t-md flex items-center justify-center mt-2 shadow-2xl">
                    <span className="font-mono text-4xl font-black text-yellow-500">I</span>
                  </div>
                </div>
              )}

              {/* 3rd Place - Bronze */}
              {podiumUsers.find(u => u.spot === 3) && (
                <div className="flex flex-col items-center flex-1 max-w-[240px] group">
                  <div className="mb-3 text-center">
                    <Medal className="h-6 w-6 text-amber-700 mx-auto animate-bounce duration-1000 delay-300" />
                    <span className="text-xs font-mono font-semibold text-amber-600">3rd Place</span>
                  </div>
                  <Card className="w-full border-zinc-700 bg-zinc-950/40 p-4 text-center transition-all duration-300 group-hover:-translate-y-1 group-hover:border-zinc-500 shadow-md">
                    <Avatar className="h-12 w-12 mx-auto border-2 border-amber-700 shadow-lg">
                      <AvatarImage src={podiumUsers.find(u => u.spot === 3).avatar} />
                      <AvatarFallback className="bg-zinc-800 text-amber-600 font-bold text-sm">
                        {podiumUsers.find(u => u.spot === 3).username.slice(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <p className="mt-3 truncate text-sm font-bold text-white">
                      @{podiumUsers.find(u => u.spot === 3).username}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      Rating {podiumUsers.find(u => u.spot === 3).rating}
                    </p>
                    <div className="mt-3 inline-flex items-center gap-1 bg-zinc-900 border border-zinc-800 px-2 py-0.5 rounded text-[10px] font-mono text-zinc-300">
                      {podiumUsers.find(u => u.spot === 3).xp.toLocaleString()} XP
                    </div>
                  </Card>
                  {/* Podium Base */}
                  <div className="w-full h-12 bg-gradient-to-b from-zinc-800/80 to-zinc-900/90 border-t border-zinc-700 rounded-t-md flex items-center justify-center mt-2 shadow-inner">
                    <span className="font-mono text-2xl font-extrabold text-amber-700">III</span>
                  </div>
                </div>
              )}

            </div>
          </div>
        )}

        {/* User Spotlight Banner */}
        {user && !loading && (
          <Card className="border-primary/25 bg-gradient-to-r from-primary/5 via-zinc-950 to-primary/5 p-4 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-lg glow-soft">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/15 border border-primary/30 text-primary">
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
                <span className="text-lg font-bold text-primary">
                  {Math.floor((user.xp || 0) / 1000) + 1}
                </span>
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

        {/* Leaderboard Lists */}
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
                      {loading ? (
                        <tr>
                          <td colSpan="7" className="py-20 text-center text-muted-foreground">
                            <Sparkles className="h-6 w-6 animate-spin mx-auto text-primary mb-2" />
                            Loading arena records...
                          </td>
                        </tr>
                      ) : leaderboardData.length === 0 ? (
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
                              className={`border-t border-border hover:bg-zinc-900/40 transition-colors ${isSelf ? "bg-primary/5 border-l-2 border-l-primary" : ""}`}
                            >
                              <td className="px-5 py-4 text-center">
                                <span className={`inline-flex items-center justify-center font-mono font-bold text-sm w-7 h-7 rounded-full ${row.rank === 1 ? "bg-yellow-500/15 text-yellow-400" :
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
                  {loading ? (
                    <li className="py-12 text-center text-muted-foreground">
                      <Sparkles className="h-5 w-5 animate-spin mx-auto text-primary mb-2" />
                      Loading arena records...
                    </li>
                  ) : leaderboardData.length === 0 ? (
                    <li className="py-8 text-center text-muted-foreground">
                      No active participants.
                    </li>
                  ) : (
                    leaderboardData.map((row) => {
                      const isSelf = user && row.username === user.username;
                      const tier = getDivisionTier(row.rating, row.rank);
                      return (
                        <li
                          key={row.username}
                          className={`flex items-center gap-3 p-4 hover:bg-zinc-900/20 ${isSelf ? "bg-primary/5 border-l-2 border-l-primary" : ""}`}
                        >
                          <span className={`w-8 font-mono text-center font-bold text-xs ${row.rank === 1 ? "text-yellow-500" :
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
                              <Badge variant="outline" className={`font-mono text-[8px] px-1 py-0.01 border shrink-0 ${tier.color}`}>
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
      </div>
    </AppShell>
  );
}

export default Leaderboard;
