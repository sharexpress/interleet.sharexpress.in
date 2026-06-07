import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Swords, Trophy, Users, ShieldAlert, Plus, Zap, ArrowRight, Play } from "lucide-react";
import { toast } from "sonner";

import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { API } from "@/api/api";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

function ContestList() {
  const navigate = useNavigate();
  const [activeContests, setActiveContests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roomCodeInput, setRoomCodeInput] = useState("");
  const [challenges, setChallenges] = useState([]);

  // Create Room State
  const [title, setTitle] = useState("Daily Coding Battle");
  const [contestType, setContestType] = useState("1v1");
  const [selectedChallenge, setSelectedChallenge] = useState("");
  const [duration, setDuration] = useState("30");
  const [creating, setCreating] = useState(false);

  const fetchActiveContests = async () => {
    try {
      const res = await API.get("/api/contest/active");
      if (res.data && res.data.success) {
        setActiveContests(res.data.data);
      }
    } catch (err) {
      console.error(err);
      toast.error("Failed to load active contests.");
    } finally {
      setLoading(false);
    }
  };

  const fetchChallengesList = async () => {
    try {
      const res = await API.get("/challenges");
      if (res.data && res.data.success) {
        setChallenges(res.data.data);
        if (res.data.data.length > 0) {
          setSelectedChallenge(res.data.data[0].slug);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchActiveContests();
    fetchChallengesList();
  }, []);

  const handleJoinByCode = async (e) => {
    e.preventDefault();
    if (!roomCodeInput.trim()) {
      toast.error("Please enter a valid room code.");
      return;
    }
    const code = roomCodeInput.trim().toUpperCase();
    try {
      const res = await API.post(`/api/contest/${code}/join`);
      if (res.data && res.data.success) {
        toast.success("Joined room successfully!");
        navigate(`/app/contest/room/${code}`);
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Could not join room. Check the code.");
    }
  };

  const handleCreateRoom = async (e) => {
    e.preventDefault();
    if (!selectedChallenge) {
      toast.error("Please select at least one challenge.");
      return;
    }
    setCreating(true);
    try {
      const res = await API.post("/api/contest/create", {
        title,
        contest_type: contestType,
        challenges: [selectedChallenge],
        duration_minutes: parseInt(duration),
      });

      if (res.data && res.data.success) {
        const room = res.data.data;
        toast.success("Room created successfully!");
        navigate(`/app/contest/room/${room.room_code}`);
      }
    } catch (err) {
      console.error(err);
      toast.error("Failed to create room.");
    } finally {
      setCreating(false);
    }
  };

  return (
    <AppShell>
      <PageHeader
        title="Contest Arena"
        description="Challenge peers, enter 1v1 rooms, and climb the live leaderboards."
        badge="Live"
      />

      <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1fr_400px]">
          
          {/* Main Area: Contests List */}
          <div className="space-y-8">
            {/* Top banner visual */}
            <div className="relative overflow-hidden rounded-2xl border border-zinc-800/80 bg-zinc-900/30 p-8 shadow-xl">
              <div className="absolute -top-12 -left-12 w-48 h-48 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
              <div className="absolute -bottom-12 -right-12 w-48 h-48 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
              
              <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="space-y-2">
                  <div className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 border border-primary/20 px-2.5 py-0.5 text-xs font-medium text-primary">
                    <Zap className="h-3 w-3 animate-pulse" /> Multi-Player coding matches
                  </div>
                  <h2 className="text-2xl font-bold text-white tracking-tight">Prove your skills in real-time</h2>
                  <p className="text-sm text-zinc-400 max-w-xl">
                    Compete in strict sandbox environments with anti-cheat checks. Solve challenges from the platform database and climb the ranks.
                  </p>
                </div>
                <div className="shrink-0 flex items-center justify-center w-20 h-20 rounded-full bg-zinc-850/50 border border-zinc-800 text-primary">
                  <Swords className="h-10 w-10 animate-bounce" />
                </div>
              </div>
            </div>

            {/* Active Contests List */}
            <section className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Play className="h-4 w-4 text-emerald-400 fill-emerald-400/20" />
                  Active Rooms & Contests
                </h3>
                <Button variant="ghost" size="sm" onClick={fetchActiveContests} className="text-xs">
                  Refresh
                </Button>
              </div>

              {loading ? (
                <div className="flex flex-col items-center justify-center py-20 border border-zinc-800/60 rounded-xl bg-zinc-900/10 gap-3">
                  <div className="h-6 w-6 animate-spin rounded-full border border-zinc-700 border-t-primary" />
                  <p className="text-sm text-zinc-500">Loading contests...</p>
                </div>
              ) : activeContests.length === 0 ? (
                <div className="text-center py-16 border border-zinc-800 border-dashed rounded-xl bg-zinc-900/10">
                  <Trophy className="h-10 w-10 text-zinc-600 mx-auto mb-3" />
                  <p className="text-sm text-zinc-400 font-medium">No open contests at the moment</p>
                  <p className="text-xs text-zinc-500 mt-1 max-w-sm mx-auto">
                    Create a custom 1v1 room on the right side panel and invite your friend to start!
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {activeContests.map((c) => (
                    <div
                      key={c.contest_id}
                      className="group flex flex-col justify-between p-5 rounded-xl border border-zinc-850 bg-zinc-900/30 hover:border-zinc-800 transition-all shadow-md relative overflow-hidden"
                    >
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className={`text-[10px] uppercase font-mono tracking-widest font-bold px-2 py-0.5 rounded ${
                            c.contest_type === "1v1"
                              ? "bg-red-500/10 text-red-400 border border-red-500/20"
                              : c.contest_type === "open_world"
                              ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
                              : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                          }`}>
                            {c.contest_type} Room
                          </span>
                          {c.room_code && (
                            <span className="text-xs font-mono font-bold text-zinc-500">
                              CODE: {c.room_code}
                            </span>
                          )}
                        </div>
                        <h4 className="font-bold text-zinc-100 group-hover:text-primary transition-colors">
                          {c.title}
                        </h4>
                        <p className="text-xs text-zinc-400 line-clamp-2">
                          {c.description}
                        </p>
                      </div>

                      <div className="flex items-center justify-between mt-5 border-t border-zinc-850/60 pt-3 text-[11px] text-zinc-500">
                        <span className="flex items-center gap-1">
                          <Users className="h-3.5 w-3.5" />
                          {c.participants?.length || 1} joined
                        </span>
                        <Button
                          size="sm"
                          variant="secondary"
                          className="h-7 text-xs bg-zinc-850 hover:bg-zinc-800 text-zinc-200"
                          asChild
                        >
                          <Link to={c.room_code ? `/app/contest/room/${c.room_code}` : `/app/contest/room/${c.contest_id}`}>
                            Enter Lobby <ArrowRight className="h-3 w-3 ml-1" />
                          </Link>
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>

          {/* Right Sidebar: Matchmaking, Create, Join Room */}
          <div className="space-y-6">
            
            {/* Join Room */}
            <div className="p-6 rounded-2xl border border-zinc-850 bg-zinc-900/20 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                Join Private Room
              </h3>
              <p className="text-xs text-zinc-400">
                Enter a 6-character room code to join an invite-only multiplayer arena.
              </p>
              <form onSubmit={handleJoinByCode} className="flex gap-2">
                <Input
                  value={roomCodeInput}
                  onChange={(e) => setRoomCodeInput(e.target.value)}
                  placeholder="e.g. AB12CD"
                  className="h-9 font-mono tracking-widest text-center text-sm"
                  maxLength={6}
                />
                <Button type="submit" size="sm" className="h-9 shrink-0">
                  Join
                </Button>
              </form>
            </div>

            {/* Create Contest Room */}
            <div className="p-6 rounded-2xl border border-zinc-850 bg-zinc-900/20 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Plus className="h-4 w-4 text-primary" />
                Create Custom Room
              </h3>
              <p className="text-xs text-zinc-400">
                Configure your own coding lobby and invite friends or colleagues.
              </p>

              <form onSubmit={handleCreateRoom} className="space-y-3.5">
                <div className="space-y-1">
                  <label className="text-[10px] font-mono uppercase text-zinc-500">Room Title</label>
                  <Input
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Enter battle title..."
                    className="h-9 text-xs"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <label className="text-[10px] font-mono uppercase text-zinc-500">Match Type</label>
                    <Select value={contestType} onValueChange={setContestType}>
                      <SelectTrigger className="h-9 text-xs">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1v1">1v1 Duel</SelectItem>
                        <SelectItem value="open_world">Open World</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] font-mono uppercase text-zinc-500">Duration</label>
                    <Select value={duration} onValueChange={setDuration}>
                      <SelectTrigger className="h-9 text-xs">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="15">15 mins</SelectItem>
                        <SelectItem value="30">30 mins</SelectItem>
                        <SelectItem value="45">45 mins</SelectItem>
                        <SelectItem value="60">60 mins</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-mono uppercase text-zinc-500">Select Coding Challenge</label>
                  <Select value={selectedChallenge} onValueChange={setSelectedChallenge}>
                    <SelectTrigger className="h-9 text-xs">
                      <SelectValue placeholder="Pick a challenge" />
                    </SelectTrigger>
                    <SelectContent className="max-h-56">
                      {challenges.map((c) => (
                        <SelectItem key={c.slug} value={c.slug}>
                          {c.title} ({c.difficulty})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <Button type="submit" className="w-full h-9 text-xs mt-2" disabled={creating}>
                  {creating ? "Creating room..." : "Create Lobby & Generate Code"}
                </Button>
              </form>
            </div>

            {/* Strict Rules Warning */}
            <div className="p-4 rounded-xl border border-zinc-800 bg-zinc-950/40 text-[11px] leading-relaxed text-zinc-500 space-y-2">
              <span className="flex items-center gap-1.5 font-semibold text-zinc-400">
                <ShieldAlert className="h-3.5 w-3.5 text-zinc-400 shrink-0" />
                LeetCode Rules Apply
              </span>
              <p>
                Once a match starts, copy-paste is fully blocked in the code editor. Any browser tab switching or window defocus triggers a warning. Exceeding 3 warnings results in automatic disqualification.
              </p>
            </div>

          </div>

        </div>
      </div>
    </AppShell>
  );
}

export default ContestList;
