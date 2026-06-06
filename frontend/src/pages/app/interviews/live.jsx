import { Link, useSearchParams } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Mic, MicOff, PhoneOff, ArrowLeft, MessageSquare } from "lucide-react";
import { useState, useEffect, useRef } from "react";



const TRANSCRIPT = [
{ from: "ai", text: "Hi, I'm Sara. Let's start — can you walk me through your experience with distributed systems?", t: "00:12" },
{ from: "you", text: "Sure. I've spent the last three years building event-driven microservices at scale.", t: "00:34" },
{ from: "ai", text: "Great. How would you design a rate limiter that works across multiple nodes without a single point of failure?", t: "01:02" },
{ from: "you", text: "I'd start with a token bucket backed by Redis using Lua scripts for atomicity…", t: "01:25" },
{ from: "ai", text: "Interesting. What trade-offs would you accept between strict consistency and throughput?", t: "01:58" }];


function LiveInterview() {
  const [searchParams] = useSearchParams();
  const role = searchParams.get("role") || "Senior Backend Engineer";
  const difficulty = searchParams.get("difficulty") || "Intermediate";

  const [muted, setMuted] = useState(false);
  const [speaking, setSpeaking] = useState(true);
  const transcriptRef = useRef(null);

  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, []);

  // Simulate AI speaking pulse
  useEffect(() => {
    const t = setInterval(() => setSpeaking((s) => !s), 2400);
    return () => clearInterval(t);
  }, []);

  return (
    <AppShell>
      {/* Top bar */}
      <div className="flex items-center justify-between border-b border-border px-4 py-3 md:px-8">
        <div className="flex items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="h-8 w-8">
            <Link to="/app/interviews"><ArrowLeft className="h-4 w-4" /></Link>
          </Button>
          <div>
            <p className="text-sm font-semibold">{role} ({difficulty}) · Live</p>
            <p className="text-xs text-muted-foreground">Voice call · Session #iv-22</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="gap-1.5 text-success">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" /> Recording
          </Badge>
          <Badge variant="outline" className="font-mono">02:14 / 45:00</Badge>
        </div>
      </div>

      {/* Video-call stage */}
      <div className="relative flex min-h-[calc(100vh-56px-57px)] flex-col bg-black lg:flex-row">
        {/* Video stage */}
        <div className="relative flex flex-1 flex-col">
          <div className="flex flex-1 items-center justify-center px-4 py-10">
            <div className="relative flex w-full max-w-2xl flex-col items-center">
              {/* AI tile */}
              <div className="relative flex aspect-video w-full items-center justify-center overflow-hidden rounded-2xl border border-border bg-[#0A0A0A]">
                <span
                  className={`absolute h-56 w-56 rounded-full bg-primary/10 transition-transform duration-1000 ${
                  speaking ? "scale-110" : "scale-100"}`
                  } />
                
                <span
                  className={`absolute h-44 w-44 rounded-full bg-primary/15 transition-transform duration-1000 ${
                  speaking ? "scale-110" : "scale-95"}`
                  } />
                

                <div className="relative flex h-32 w-32 items-center justify-center rounded-full bg-gradient-to-br from-primary to-orange-700 text-4xl font-bold text-white shadow-2xl">
                  S
                </div>

                <div className="absolute bottom-4 left-4 flex items-center gap-2 rounded-md bg-black/70 px-3 py-1.5 backdrop-blur">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" />
                  <span className="text-sm font-medium text-white">Sara · AI Interviewer</span>
                </div>
                <div className="absolute bottom-4 right-4 rounded-md bg-black/70 px-2.5 py-1 font-mono text-[11px] text-white/80 backdrop-blur">
                  {speaking ? "Speaking…" : "Listening"}
                </div>
              </div>

              {/* Live caption of what AI just asked */}
              <div className="mt-4 w-full rounded-xl border border-border bg-card/80 px-4 py-3 backdrop-blur">
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
                  Sara is asking
                </p>
                <p className="mt-1 text-sm text-foreground">
                  {TRANSCRIPT.filter((m) => m.from === "ai").slice(-1)[0]?.text}
                </p>
              </div>

              {/* Self tile */}
              <div className="mt-4 flex w-full max-w-xs items-center gap-3 self-end rounded-xl border border-border bg-card/80 px-4 py-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                  You
                </div>
                <div className="flex-1">
                  <p className="text-xs font-semibold">You</p>
                  <p className="text-[10px] text-muted-foreground">
                    {muted ? "Microphone muted" : "Microphone on"}
                  </p>
                </div>
                {muted ?
                <MicOff className="h-4 w-4 text-destructive" /> :

                <Mic className="h-4 w-4 text-success" />
                }
              </div>
            </div>
          </div>

          {/* Call controls */}
          <div className="flex items-center justify-center gap-4 border-t border-border bg-card/40 py-5">
            <button
              onClick={() => setMuted((m) => !m)}
              className={`flex h-14 w-14 items-center justify-center rounded-full border transition-colors ${
              muted ?
              "border-destructive bg-destructive/15 text-destructive" :
              "border-border bg-secondary text-foreground hover:bg-secondary/70"}`
              }
              aria-label={muted ? "Unmute" : "Mute"}>
              
              {muted ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
            </button>

            <Link
              to={`/app/interviews/${"iv-22"}/report`}
              className="flex h-14 w-20 items-center justify-center rounded-full bg-destructive text-destructive-foreground transition-colors hover:bg-destructive/90"
              aria-label="End call">
              
              <PhoneOff className="h-5 w-5" />
            </Link>
          </div>
        </div>

        {/* Transcript sidebar */}
        <aside className="flex w-full flex-col border-t border-border bg-card lg:w-[380px] lg:border-l lg:border-t-0">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <MessageSquare className="h-4 w-4 text-primary" />
            <p className="text-sm font-semibold">Live Transcript</p>
            <Badge variant="outline" className="ml-auto text-[10px]">Auto</Badge>
          </div>
          <div ref={transcriptRef} className="flex-1 space-y-3 overflow-auto px-4 py-4">
            {TRANSCRIPT.map((m, i) =>
            <div key={i} className={`flex flex-col ${m.from === "you" ? "items-end" : "items-start"}`}>
                <div className="mb-1 flex items-center gap-2 text-[10px] text-muted-foreground">
                  <span className="font-semibold">{m.from === "ai" ? "Sara" : "You"}</span>
                  <span className="font-mono">{m.t}</span>
                </div>
                <div
                className={`max-w-[90%] rounded-2xl px-3 py-2 text-sm leading-relaxed ${
                m.from === "ai" ?
                "rounded-tl-sm bg-secondary text-foreground" :
                "rounded-tr-sm bg-primary text-primary-foreground"}`
                }>
                
                  {m.text}
                </div>
              </div>
            )}
          </div>
        </aside>
      </div>
    </AppShell>);

}
export default LiveInterview;
