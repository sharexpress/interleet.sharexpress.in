import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { Trophy, ShieldAlert, Award, ArrowLeft, Users, RefreshCw } from "lucide-react";

import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { API } from "@/api/api";

function ContestResults() {
  const { code } = useParams();
  const navigate = useNavigate();
  const [leaderboard, setLeaderboard] = useState([]);
  const [contest, setContest] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchResults = async () => {
    try {
      // Fetch details
      const contestRes = await API.get(`/api/contest/${code}`);
      if (contestRes.data && contestRes.data.success) {
        setContest(contestRes.data.data);
      }

      // Fetch leaderboard
      const leaderboardRes = await API.get(`/api/contest/${code}/leaderboard`);
      if (leaderboardRes.data && leaderboardRes.data.success) {
        setLeaderboard(leaderboardRes.data.data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, [code]);

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-muted-foreground">
            <div className="h-8 w-8 animate-spin rounded-full border border-zinc-700 border-t-primary" />
            <p className="text-sm">Loading final results...</p>
          </div>
        </div>
      </AppShell>
    );
  }

  // Get podium ranks (1, 2, 3)
  const podium = leaderboard.slice(0, 3);
  const rest = leaderboard.slice(3);

  return (
    <AppShell>
      <PageHeader
        title="Contest Results"
        description="Review final match standings, solve metrics, and compliance checks."
        badge="Completed"
      />

      <div className="mx-auto max-w-5xl px-4 py-8 md:px-8 space-y-8">
        
        {/* Back Link */}
        <div className="flex justify-between items-center">
          <Button variant="ghost" size="sm" asChild>
            <Link to="/app/contest" className="gap-1.5 text-xs">
              <ArrowLeft className="h-4 w-4" /> Back to Arena
            </Link>
          </Button>

          <Button variant="outline" size="sm" onClick={fetchResults} className="gap-1.5 h-8 text-xs">
            <RefreshCw className="h-3.5 w-3.5" /> Refresh
          </Button>
        </div>

        {/* Podium Highlight */}
        {podium.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end justify-center py-6">
            
            {/* 2nd Place */}
            {podium[1] && (
              <div className="flex flex-col items-center p-5 rounded-2xl border border-zinc-850 bg-zinc-900/10 order-2 md:order-1 relative overflow-hidden">
                <div className="absolute top-0 left-0 right-0 h-1 bg-zinc-400" />
                <div className="h-10 w-10 rounded-full bg-zinc-850 border border-zinc-700 flex items-center justify-center font-bold text-zinc-300 text-sm mb-3">
                  2
                </div>
                <h4 className="font-bold text-zinc-200 text-sm truncate max-w-[150px]">
                  @{podium[1].username}
                </h4>
                <p className="text-xs text-zinc-400 font-semibold mt-1">
                  {podium[1].total_score} pts
                </p>
                <span className="text-[10px] text-zinc-500 font-mono mt-1">
                  {podium[1].disqualified ? "Disqualified" : `${podium[1].warnings_count} violation(s)`}
                </span>
              </div>
            )}

            {/* 1st Place Winner */}
            {podium[0] && (
              <div className="flex flex-col items-center p-7 rounded-2xl border border-primary/30 bg-primary/5 order-1 md:order-2 relative overflow-hidden ring-1 ring-primary/20 shadow-[0_4px_30px_rgba(255,101,0,0.08)]">
                <div className="absolute top-0 left-0 right-0 h-1.5 bg-primary" />
                <div className="absolute -top-6 -right-6 w-16 h-16 bg-primary/10 rounded-full blur-xl pointer-events-none" />
                
                <Trophy className="h-10 w-10 text-amber-500 mb-3 animate-bounce" />
                <h3 className="font-extrabold text-white text-base truncate max-w-[180px]">
                  @{podium[0].username}
                </h3>
                <p className="text-sm font-extrabold text-primary mt-1">
                  {podium[0].total_score} pts
                </p>
                <span className="text-[10px] text-zinc-400 font-mono mt-1">
                  {podium[0].disqualified ? "Disqualified" : `${podium[0].warnings_count} violation(s)`}
                </span>
                
                <div className="mt-4 inline-flex items-center gap-1 text-[9px] uppercase font-mono bg-primary/20 border border-primary/30 px-2 py-0.5 rounded text-primary font-bold">
                  Winner
                </div>
              </div>
            )}

            {/* 3rd Place */}
            {podium[2] && (
              <div className="flex flex-col items-center p-5 rounded-2xl border border-zinc-850 bg-zinc-900/10 order-3 relative overflow-hidden">
                <div className="absolute top-0 left-0 right-0 h-1 bg-amber-800" />
                <div className="h-10 w-10 rounded-full bg-zinc-850 border border-zinc-700 flex items-center justify-center font-bold text-amber-800 text-sm mb-3">
                  3
                </div>
                <h4 className="font-bold text-zinc-200 text-sm truncate max-w-[150px]">
                  @{podium[2].username}
                </h4>
                <p className="text-xs text-zinc-400 font-semibold mt-1">
                  {podium[2].total_score} pts
                </p>
                <span className="text-[10px] text-zinc-500 font-mono mt-1">
                  {podium[2].disqualified ? "Disqualified" : `${podium[2].warnings_count} violation(s)`}
                </span>
              </div>
            )}

          </div>
        )}

        {/* Complete Standings Table */}
        <section className="p-6 rounded-2xl border border-zinc-850 bg-zinc-900/20 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Users className="h-4 w-4 text-primary" />
            Complete Standings
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-zinc-800 text-zinc-400 text-[10px] font-mono uppercase">
                  <th className="py-3 px-4 w-16">Rank</th>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Compliance Status</th>
                  <th className="py-3 px-4 text-right">Score</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((item, idx) => (
                  <tr
                    key={item.user_id}
                    className={`border-b border-zinc-850/60 last:border-b-0 hover:bg-zinc-900/20 ${
                      item.disqualified ? "bg-red-950/5 opacity-70" : ""
                    }`}
                  >
                    <td className="py-4 px-4 font-mono font-bold text-zinc-400">
                      #{idx + 1}
                    </td>
                    <td className="py-4 px-4">
                      <div>
                        <span className="font-semibold text-zinc-200 block">
                          {item.full_name || item.username}
                        </span>
                        <span className="text-[10px] text-zinc-500 font-mono">
                          @{item.username}
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      {item.disqualified ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-red-400 bg-red-500/10 border border-red-500/20 px-2 py-0.5 rounded">
                          <ShieldAlert className="h-3 w-3" /> Disqualified
                        </span>
                      ) : item.warnings_count > 0 ? (
                        <span className="text-[10px] text-amber-500 font-medium font-mono">
                          {item.warnings_count} focus warning(s)
                        </span>
                      ) : (
                        <span className="text-[10px] text-emerald-400 font-medium">
                          Passed verification checks
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-4 text-right font-bold text-white text-sm">
                      {item.total_score} pts
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </AppShell>
  );
}

export default ContestResults;
