/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { MessageSquare, Users, UserPlus, Play, ArrowLeft, Send, ShieldAlert, Award, Copy } from "lucide-react";
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
    if (!user || !code) return;

    let active = true;
    let ws = null;

    // Join room database entry first
    const initJoinAndConnect = async () => {
      try {
        await API.post(`/api/contest/${code}/join`);
      } catch (err) {
        console.error("Auto join lobby failed:", err);
      }

      if (!active) return;

      const token = getCookie("user");
      const backendUrl = import.meta.env?.VITE_BACKEND_URL || import.meta.env?.BACKEND_URL || "https://interleet-backend.sharexpress.in";
      const wsBase = backendUrl.replace(/^http/, "ws");
      const wsUrl = `${wsBase}/api/contest/ws/${code}${token ? `?token=${token}` : ""}`;
      
      const wsInstance = new WebSocket(wsUrl);
      ws = wsInstance;
      wsRef.current = wsInstance;

      ws.onmessage = (event) => {
        if (!active) return;
        const data = JSON.parse(event.data);
        if (data.type === "chat") {
          setChatMessages((prev) => {
            if (prev.length > 0) {
              const lastMsg = prev[prev.length - 1];
              if (data.username === "System" && lastMsg.username === "System" && lastMsg.message === data.message) {
                return prev;
              }
            }
            return [...prev, data];
          });
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
        if (!active) return;
        console.error("WS Lobby error:", err);
      };

      ws.onclose = () => {
        console.log("WS Lobby disconnected.");
      };
    };

    initJoinAndConnect();

    return () => {
      active = false;
      if (ws) {
        ws.close();
      }
    };
  }, [code, user?.user_id]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  if (!contest) {
    return (
      <AppShell>
        <div className="mx-auto max-w-7xl px-4 py-8 md:px-8 space-y-6 animate-pulse">
          {/* Header row skeleton */}
          <div className="flex items-center justify-between">
            <div className="h-4 w-28 rounded bg-zinc-800/40" />
            <div className="h-6 w-32 rounded bg-zinc-800/40" />
          </div>
          {/* Lobby layout skeleton */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left side (participants / settings) */}
            <div className="lg:col-span-2 space-y-6">
              <div className="h-[180px] rounded-xl border border-border bg-card/30 p-6 space-y-4">
                <div className="h-5 w-48 rounded bg-zinc-800/40" />
                <div className="h-4 w-96 rounded bg-zinc-800/20" />
              </div>
              <div className="h-[140px] rounded-xl border border-border bg-card/30 p-6 space-y-3">
                <div className="h-4 w-32 rounded bg-zinc-800/40" />
                <div className="h-3.5 w-64 rounded bg-zinc-800/20" />
              </div>
            </div>
            {/* Right side (chat window) */}
            <div className="h-[360px] rounded-xl border border-border bg-card/30 p-6 flex flex-col justify-between" />
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

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping" />
              <span className="text-[11px] font-mono text-zinc-400">Match Code: {contest.room_code}</span>
            </div>
            <button
              onClick={() => {
                const inviteUrl = `${window.location.origin}/app/contest/room/${contest.room_code}`;
                navigator.clipboard.writeText(inviteUrl);
                toast.success("Contest invite link copied!");
              }}
              className="text-zinc-400 hover:text-white transition-colors p-1 rounded hover:bg-zinc-800"
              title="Copy Invite Link"
            >
              <Copy className="h-3.5 w-3.5" />
            </button>
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
                        <div key={i} className="text-center text-[10px] text-zinc-550 italic my-1 font-mono">
                          {msg.message}
                        </div>
                      );
                    }

                    const prevMsg = i > 0 ? chatMessages[i - 1] : null;
                    const showHeader = !prevMsg || prevMsg.username !== msg.username || prevMsg.username === "System";

                    return (
                      <div key={i} className={`flex flex-col ${isSelf ? "items-end" : "items-start"} ${showHeader ? "mt-3" : "mt-0.5"}`}>
                        {showHeader && (
                          <span className="text-[10px] text-zinc-500 mb-0.5 px-1 font-mono">
                            @{msg.username}
                          </span>
                        )}
                        <div className={`text-xs rounded-xl px-3.5 py-1.5 max-w-[80%] ${isSelf
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
                    onClick={() => navigate(`/app/profile/${p.username}`)}
                    className="flex items-center justify-between p-3 rounded-lg border border-zinc-850 bg-zinc-900/40 cursor-pointer hover:bg-zinc-850/50 transition-colors"
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
