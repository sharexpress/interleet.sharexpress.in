import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { MessageSquare, Users, UserPlus, Play, ArrowLeft, Send, ShieldAlert, Award } from "lucide-react";
import { toast } from "sonner";

import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { API } from "@/api/api";

function ContestLobby() {
  const { code } = useParams();
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.user);

  const [contest, setContest] = useState(null);
  const [participants, setParticipants] = useState([]);
  const [chatMessages, setChatMessages] = useState([]);
  const [typedMessage, setTypedMessage] = useState("");
  const [inviteUsername, setInviteUsername] = useState("");
  const [inviting, setInviting] = useState(false);
  const [starting, setStarting] = useState(false);

  const wsRef = useRef(null);
  const chatEndRef = useRef(null);

  // Helper to extract cookie
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  };

  const fetchContestDetails = async () => {
    try {
      const res = await API.get(`/api/contest/${code}`);
      if (res.data && res.data.success) {
        setContest(res.data.data);
        setParticipants(res.data.data.participants || []);
      }
    } catch (err) {
      toast.error("Failed to load lobby details.");
      navigate("/app/contest");
    }
  };

  const handleInviteUser = async (e) => {
    e.preventDefault();
    if (!inviteUsername.trim()) return;
    setInviting(true);
    try {
      const res = await API.post("/api/notifications/invite", {
        username: inviteUsername.trim(),
        room_code: code.toUpperCase(),
        contest_title: contest?.title || "Coding Duel",
      });
      if (res.data && res.data.success) {
        toast.success(`Invitation pushed to @${inviteUsername}!`);
        setInviteUsername("");
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Could not invite user.");
    } finally {
      setInviting(false);
    }
  };

  const handleStartContest = async () => {
    setStarting(true);
    try {
      await API.post(`/api/contest/${code}/start`);
      toast.success("Starting match...");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to start match.");
    } finally {
      setStarting(false);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!typedMessage.trim() || !wsRef.current) return;

    wsRef.current.send(
      JSON.stringify({
        type: "chat",
        message: typedMessage.trim(),
      })
    );
    setTypedMessage("");
  };

  useEffect(() => {
    fetchContestDetails();
  }, [code]);

  useEffect(() => {
    if (!contest || !user) return;

    // Join room database entry first
    const initJoinAndConnect = async () => {
      try {
        await API.post(`/api/contest/${code}/join`);
      } catch (err) {
        console.error("Auto join lobby failed:", err);
      }

      // Establish WebSocket
      const token = getCookie("user");
      const wsUrl = `ws://localhost:8000/api/contest/ws/${code}${token ? `?token=${token}` : ""}`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "chat") {
          setChatMessages((prev) => [...prev, data]);
        } else if (data.type === "user_joined") {
          fetchContestDetails();
        } else if (data.type === "contest_started") {
          toast.success("Match starting! Loading workspace...");
          setTimeout(() => {
            navigate(`/app/contest/editor/${code}`);
          }, 1000);
        }
      };

      ws.onerror = (err) => {
        console.error("WS Lobby error:", err);
      };

      ws.onclose = () => {
        console.log("WS Lobby disconnected.");
      };
    };

    initJoinAndConnect();

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, [contest, user]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  if (!contest) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-muted-foreground">
            <div className="h-8 w-8 animate-spin rounded-full border border-zinc-700 border-t-primary" />
            <p className="text-sm">Loading lobby details...</p>
          </div>
        </div>
      </AppShell>
    );
  }

  const isHost = String(contest.creator_id) === String(user?.user_id);

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">

        {/* Back Link */}
        <div className="mb-6 flex items-center justify-between">
          <button
            onClick={() => navigate("/app/contest")}
            className="flex items-center gap-2 text-xs font-semibold text-zinc-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="h-4 w-4" /> Back to Arena
          </button>

          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping" />
            <span className="text-[11px] font-mono text-zinc-400">Match Code: {contest.room_code}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_360px_320px]">

          {/* Column 1: Match Info + Lobby Chat */}
          <div className="flex flex-col gap-6 h-[calc(100vh-200px)]">

            {/* Header detail */}
            <div className="p-6 rounded-2xl border border-zinc-850 bg-zinc-900/30">
              <div className="space-y-1">
                <h2 className="text-xl font-bold text-white tracking-tight">{contest.title}</h2>
                <p className="text-xs text-zinc-400">{contest.description}</p>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-6 border-t border-zinc-850 pt-4 text-xs">
                <div>
                  <span className="text-zinc-500 block text-[10px] font-mono uppercase">Duration</span>
                  <span className="text-zinc-200 font-semibold">{contest.duration_minutes} minutes</span>
                </div>
                <div>
                  <span className="text-zinc-500 block text-[10px] font-mono uppercase">Match Type</span>
                  <span className="text-zinc-200 font-semibold uppercase">{contest.contest_type}</span>
                </div>
                <div>
                  <span className="text-zinc-500 block text-[10px] font-mono uppercase">Challenges</span>
                  <span className="text-zinc-200 font-semibold">{contest.challenges?.length || 1} problem(s)</span>
                </div>
              </div>
            </div>

            {/* Chat Box */}
            <div className="flex-1 flex flex-col rounded-2xl border border-zinc-850 bg-zinc-900/20 overflow-hidden">
              <div className="p-4 border-b border-zinc-850 flex items-center gap-2 bg-zinc-900/40">
                <MessageSquare className="h-4 w-4 text-primary" />
                <h3 className="text-xs font-bold text-white">Lobby Chat</h3>
              </div>

              {/* Message Feed */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {chatMessages.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-xs text-zinc-500">
                    Type a message below to start chatting
                  </div>
                ) : (
                  chatMessages.map((msg, i) => {
                    const isSelf = msg.username === user?.username;
                    const isSystem = msg.username === "System";

                    if (isSystem) {
                      return (
                        <div key={i} className="text-center text-[10px] text-zinc-500 italic">
                          {msg.message}
                        </div>
                      );
                    }

                    return (
                      <div key={i} className={`flex flex-col ${isSelf ? "items-end" : "items-start"}`}>
                        <span className="text-[10px] text-zinc-500 mb-0.5 px-1 font-mono">
                          @{msg.username}
                        </span>
                        <div className={`text-xs rounded-xl px-3.5 py-2 max-w-[80%] ${isSelf
                            ? "bg-primary text-primary-foreground font-medium rounded-tr-none"
                            : "bg-zinc-850 text-zinc-200 rounded-tl-none border border-zinc-800"
                          }`}>
                          {msg.message}
                        </div>
                      </div>
                    );
                  })
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Chat Input */}
              <form onSubmit={handleSendMessage} className="p-3 border-t border-zinc-850 bg-zinc-900/40 flex gap-2">
                <Input
                  value={typedMessage}
                  onChange={(e) => setTypedMessage(e.target.value)}
                  placeholder="Type message..."
                  className="h-9 text-xs"
                />
                <Button type="submit" size="icon" className="h-9 w-9 shrink-0">
                  <Send className="h-3.5 w-3.5" />
                </Button>
              </form>

            </div>

          </div>

          {/* Column 2: Players List */}
          <div className="p-6 rounded-2xl border border-zinc-850 bg-zinc-900/20 h-fit space-y-4">
            <h3 className="text-xs font-bold text-white flex items-center gap-2">
              <Users className="h-4 w-4 text-primary" />
              Participants ({participants.length})
            </h3>

            <div className="space-y-2.5 max-h-[400px] overflow-y-auto">
              {participants.map((p) => {
                const isUserHost = String(contest.creator_id) === String(p.user_id);
                return (
                  <div
                    key={p.user_id}
                    className="flex items-center justify-between p-3 rounded-lg border border-zinc-850 bg-zinc-900/40"
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <div className="h-7 w-7 rounded-full bg-zinc-850 border border-zinc-800 flex items-center justify-center text-xs font-bold text-zinc-300 uppercase shrink-0">
                        {p.username?.[0]}
                      </div>
                      <div className="min-w-0">
                        <span className="block text-xs font-semibold text-zinc-200 truncate">
                          {p.full_name || p.username}
                        </span>
                        <span className="block text-[9px] text-zinc-500 font-mono">
                          @{p.username}
                        </span>
                      </div>
                    </div>

                    {isUserHost && (
                      <span className="flex items-center gap-1 text-[9px] font-mono text-amber-500 bg-amber-500/10 border border-amber-500/20 px-1.5 py-0.5 rounded">
                        <Award className="h-2.5 w-2.5" /> Host
                      </span>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Launch Game Section */}
            <div className="border-t border-zinc-850/60 pt-4">
              {isHost ? (
                <div className="space-y-3">
                  <p className="text-[11px] text-zinc-500 text-center">
                    You are the host. Once all players join, press the start button.
                  </p>
                  <Button
                    onClick={handleStartContest}
                    className="w-full text-xs h-10 gap-1.5 bg-emerald-600 hover:bg-emerald-500"
                    disabled={starting}
                  >
                    <Play className="h-4 w-4 fill-white" />
                    {starting ? "Launching..." : "Start Contest"}
                  </Button>
                </div>
              ) : (
                <div className="text-center py-2 bg-zinc-900/30 rounded border border-zinc-850/80">
                  <p className="text-[11px] text-zinc-400 font-medium">Waiting for host to start...</p>
                </div>
              )}
            </div>
          </div>

          {/* Column 3: Invite Panel & Rules summary */}
          <div className="space-y-6 h-fit">

            {/* Invite Peer */}
            <div className="p-6 rounded-2xl border border-zinc-850 bg-zinc-900/20 space-y-4">
              <h3 className="text-xs font-bold text-white flex items-center gap-2">
                <UserPlus className="h-4 w-4 text-primary" />
                Invite Competitor
              </h3>
              <p className="text-[11px] text-zinc-400">
                Send a real-time in-app notification to another member.
              </p>
              <form onSubmit={handleInviteUser} className="space-y-3">
                <Input
                  value={inviteUsername}
                  onChange={(e) => setInviteUsername(e.target.value)}
                  placeholder="Username (e.g. kenji_w)"
                  className="h-9 text-xs font-mono"
                  required
                />
                <Button type="submit" size="sm" className="w-full h-9 text-xs" disabled={inviting}>
                  {inviting ? "Inviting..." : "Send Invite"}
                </Button>
              </form>
            </div>

            {/* Rules reminder */}
            <div className="p-5 rounded-xl border border-zinc-800 bg-zinc-950/40 text-[11px] leading-relaxed text-zinc-500 space-y-2">
              <span className="flex items-center gap-1.5 font-semibold text-zinc-400">
                <ShieldAlert className="h-3.5 w-3.5 text-zinc-400 shrink-0" />
                Audited Sandbox Sandbox
              </span>
              <p>
                Tab visibility loss, minimization, clipboard actions (copying or pasting code), and window resizing are logged immediately. Ensure your workspace is clean before the match starts!
              </p>
            </div>

          </div>

        </div>
      </div>
    </AppShell>
  );
}

export default ContestLobby;
