import { useEffect, useRef, useState, useCallback } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Mic, MicOff, PhoneOff, ArrowLeft, MessageSquare,
  Send, Loader2, Volume2, VolumeX, AlertTriangle, CheckCircle2,
} from "lucide-react";
import { toast } from "sonner";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import {
  startInterview,
  submitAnswer,
  appendTranscript,
  clearSession,
} from "@/redux/slices/interviewsSlice";

// ─── Browser STT API ──────────────────────────────────────────────────────────
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition || null;

// ─── Module-level audio handles (prevent GC and allow global stop) ────────────
let _activeAudio = null;
let _activeUtterance = null;

// ─── Voice state machine phases ───────────────────────────────────────────────
// The single source of truth for what the interview audio pipeline is doing.
//
//   idle ──► speaking ──► listening ──► reviewing ──► submitting
//    ▲          │              │              │            │
//    └──────────┴──────────────┴──────────────┴────────────┘ (loop until completed)
//
const PHASE = {
  IDLE:       "idle",       // No audio activity
  SPEAKING:   "speaking",   // Sara TTS is playing
  LISTENING:  "listening",  // STT active, waiting for user to speak
  REVIEWING:  "reviewing",  // Speech detected, silence countdown running
  SUBMITTING: "submitting", // Answer sent, waiting for AI response
  COMPLETED:  "completed",  // Interview finished
};

// ─── TTS helpers ──────────────────────────────────────────────────────────────

function speakText(text, { baseUrl, onStart, onEnd } = {}) {
  // Kill any active audio first
  _stopAllAudio();

  const url = `${baseUrl}/interview/tts?text=${encodeURIComponent(text)}&voice=nova`;
  const audio = new Audio(url);
  _activeAudio = audio;

  const cleanup = () => {
    if (_activeAudio === audio) _activeAudio = null;
  };

  audio.onplay    = () => onStart?.();
  audio.onended   = () => { cleanup(); onEnd?.(); };
  audio.onerror   = () => { cleanup(); _browserSpeak(text, { onStart, onEnd }); };
  audio.play().catch(() => { cleanup(); _browserSpeak(text, { onStart, onEnd }); });
}

function _browserSpeak(text, { onStart, onEnd } = {}) {
  if (!window.speechSynthesis) { onEnd?.(); return; }
  window.speechSynthesis.cancel();

  const utter = new SpeechSynthesisUtterance(text);
  _activeUtterance = utter; // Pin to module scope to prevent GC mid-speech

  utter.rate   = 0.95;
  utter.pitch  = 1.05;
  utter.volume = 1;

  // Best available English voice
  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(v =>
    v.name.toLowerCase().includes("samantha") ||
    v.name.toLowerCase().includes("google us english") ||
    (v.lang === "en-US" && !v.name.toLowerCase().includes("microsoft"))
  );
  if (preferred) utter.voice = preferred;

  utter.onstart = () => onStart?.();
  utter.onend   = () => { _activeUtterance = null; onEnd?.(); };
  utter.onerror = () => { _activeUtterance = null; onEnd?.(); };

  window.speechSynthesis.speak(utter);
}

function _stopAllAudio() {
  if (_activeAudio) {
    try { _activeAudio.pause(); } catch (_) {}
    _activeAudio = null;
  }
  if (_activeUtterance) {
    window.speechSynthesis?.cancel();
    _activeUtterance = null;
  }
}

// ─── AI Avatar ────────────────────────────────────────────────────────────────
function AIAvatar({ phase }) {
  const isSpeaking  = phase === PHASE.SPEAKING;
  const isActive    = phase === PHASE.LISTENING || phase === PHASE.REVIEWING;
  const isThinking  = phase === PHASE.IDLE || phase === PHASE.SUBMITTING;

  return (
    <div className="relative flex items-center justify-center select-none">
      {/* Outer ring */}
      <span className="absolute rounded-full border border-primary/10 transition-all duration-700"
        style={{ width: isSpeaking ? 260 : 220, height: isSpeaking ? 260 : 220, opacity: isSpeaking ? 0.45 : 0.15 }} />
      {/* Middle ring */}
      <span className="absolute rounded-full border border-primary/20 transition-all duration-500"
        style={{ width: isSpeaking ? 210 : 180, height: isSpeaking ? 210 : 180, opacity: isSpeaking ? 0.6 : 0.2 }} />
      {/* Inner glow */}
      <span className="absolute rounded-full bg-primary/10 transition-all duration-300"
        style={{ width: isSpeaking ? 165 : 145, height: isSpeaking ? 165 : 145 }} />
      {/* Avatar */}
      <div className="relative z-10 flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br from-primary via-orange-600 to-amber-600 text-4xl font-bold text-white shadow-[0_0_40px_rgba(255,101,0,0.35)]">
        S
      </div>
      {/* Status label */}
      <div className="absolute -bottom-8 flex items-center gap-1.5 text-xs font-medium">
        {isThinking ? (
          <><Loader2 className="h-3 w-3 animate-spin text-amber-400" /><span className="text-amber-400">Processing…</span></>
        ) : isSpeaking ? (
          <><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-primary" /><span className="text-primary">Sara is speaking</span></>
        ) : phase === PHASE.LISTENING ? (
          <><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" /><span className="text-emerald-400">Listening…</span></>
        ) : phase === PHASE.REVIEWING ? (
          <><span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-pulse" /><span className="text-amber-400">Got it…</span></>
        ) : (
          <span className="text-zinc-500">Ready</span>
        )}
      </div>
    </div>
  );
}

// ─── Transcript Message ───────────────────────────────────────────────────────
function TranscriptMessage({ msg }) {
  const isAI = msg.from === "ai";
  return (
    <div className={`flex flex-col ${isAI ? "items-start" : "items-end"}`}>
      <div className="mb-1 flex items-center gap-2 text-[10px] text-muted-foreground">
        <span className="font-semibold">{isAI ? "Sara" : "You"}</span>
        <span className="font-mono">{msg.timestamp}</span>
        {msg.topic && !isAI && (
          <Badge variant="outline" className="h-4 px-1 text-[9px] font-mono border-zinc-700 text-zinc-500">
            {msg.topic}
          </Badge>
        )}
      </div>
      <div className={`max-w-[92%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
        isAI
          ? "rounded-tl-sm bg-zinc-900/80 border border-zinc-800 text-zinc-100"
          : "rounded-tr-sm bg-primary/90 text-white"
      }`}>
        {msg.text}
      </div>
      {msg.evaluation && (
        <div className="mt-1.5 flex flex-wrap items-center gap-1.5 text-[10px] font-medium">
          <span className="flex items-center gap-1 text-emerald-400">
            <CheckCircle2 className="h-3 w-3" />
            Score: {msg.evaluation.score ?? "—"}/10
          </span>
          {msg.evaluation.summary && (
            <span className="text-zinc-500">· {msg.evaluation.summary}</span>
          )}
        </div>
      )}
    </div>
  );
}

// ─── Audio Visualizer ─────────────────────────────────────────────────────────
function AudioVisualizer({ levels, active }) {
  return (
    <div className="flex items-end gap-[2px] h-4 px-1">
      {levels.map((level, i) =>
        active ? (
          <div key={i}
            className="w-1 rounded-full bg-gradient-to-t from-primary via-orange-500 to-amber-400 transition-all duration-75"
            style={{ height: `${Math.max(20, level)}%` }} />
        ) : (
          <div key={i} className="w-1 h-1.5 rounded-full bg-zinc-700/60" />
        )
      )}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────
function LiveInterview() {
  const dispatch    = useAppDispatch();
  const navigate    = useNavigate();
  const [searchParams] = useSearchParams();

  const role       = searchParams.get("role") || "Senior Backend Engineer";
  const difficulty = searchParams.get("difficulty") || "Intermediate";
  const baseUrl    = import.meta.env?.VITE_BACKEND_URL || "http://localhost:8000";

  // ── Redux state ──────────────────────────────────────────────────────────────
  const {
    setupPayload, sessionId, currentQuestion, currentPreamble,
    currentTopic, answerGuidance, interviewPhase, transcript,
    isCompleted, closingMessage, isStarting, isSubmitting,
    sessionError, coveredTopics, remainingTopics,
  } = useAppSelector(s => s.interviews);

  // ── Voice state machine ──────────────────────────────────────────────────────
  // voicePhaseRef is the authoritative gate used INSIDE all async callbacks.
  // voicePhase (state) drives the UI re-renders.
  const [voicePhase, _setVoicePhase] = useState(PHASE.IDLE);
  const voicePhaseRef = useRef(PHASE.IDLE);

  const setPhase = useCallback((p) => {
    voicePhaseRef.current = p;
    _setVoicePhase(p);
  }, []);

  // ── UI state ─────────────────────────────────────────────────────────────────
  const [isMuted,          setIsMuted]          = useState(false);
  const [ttsEnabled,       setTtsEnabled]       = useState(true);
  const [interimText,      setInterimText]      = useState("");
  const [textInput,        setTextInput]        = useState("");
  const [elapsedSeconds,   setElapsedSeconds]   = useState(0);
  const [countdownPercent, setCountdownPercent] = useState(100);
  const [audioLevels,      setAudioLevels]      = useState([0, 0, 0, 0, 0]);
  const [interactionMode,  setInteractionMode]  = useState("auto"); // "auto" | "ptt" | "keyboard"
  const [hasSttSupport]   = useState(() => !!SpeechRecognition);

  // ── Stable refs mirroring state (safe inside event handler closures) ─────────
  const isMutedRef         = useRef(false);
  const ttsEnabledRef      = useRef(true);
  const interactionModeRef = useRef("auto");
  const sessionIdRef       = useRef(sessionId);
  const currentTopicRef    = useRef(currentTopic);
  const textInputRef       = useRef("");

  useEffect(() => { isMutedRef.current         = isMuted;          }, [isMuted]);
  useEffect(() => { ttsEnabledRef.current      = ttsEnabled;       }, [ttsEnabled]);
  useEffect(() => { interactionModeRef.current = interactionMode;  }, [interactionMode]);
  useEffect(() => { sessionIdRef.current       = sessionId;        }, [sessionId]);
  useEffect(() => { currentTopicRef.current    = currentTopic;     }, [currentTopic]);
  useEffect(() => { textInputRef.current       = textInput;        }, [textInput]);

  // ── Component refs ───────────────────────────────────────────────────────────
  const transcriptRef   = useRef(null);
  const recognitionRef  = useRef(null);
  const timerRef        = useRef(null);
  const lastMsgRef      = useRef("");   // Deduplicate TTS triggers
  const sessionInitRef  = useRef(false);

  // Silence timer
  const silenceTimerRef    = useRef(null);
  const countdownIntervalRef = useRef(null);

  // Audio analyser
  const audioCtxRef     = useRef(null);
  const audioStreamRef  = useRef(null);
  const audioAnalyserRef = useRef(null);
  const audioAnimRef    = useRef(null);

  // Stable submit ref so silence timer always calls the latest version
  const submitRef = useRef(null);

  // Stable startSTT ref for internal async callbacks
  const startSTTRef = useRef(null);

  // ── Elapsed clock ────────────────────────────────────────────────────────────
  useEffect(() => {
    timerRef.current = setInterval(() => setElapsedSeconds(s => s + 1), 1000);
    return () => clearInterval(timerRef.current);
  }, []);

  const formatTime = s =>
    `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;

  // ── Auto-scroll transcript ───────────────────────────────────────────────────
  useEffect(() => {
    if (transcriptRef.current)
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
  }, [transcript, interimText]);

  // ── Audio level analyser ─────────────────────────────────────────────────────
  const startAnalyser = useCallback(async () => {
    if (audioCtxRef.current) return; // Already running
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioStreamRef.current = stream;

      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      audioCtxRef.current = ctx;

      const analyser = ctx.createAnalyser();
      analyser.fftSize = 32;
      audioAnalyserRef.current = analyser;
      ctx.createMediaStreamSource(stream).connect(analyser);

      const data = new Uint8Array(analyser.frequencyBinCount);
      const tick = () => {
        if (!audioAnalyserRef.current) return;
        analyser.getByteFrequencyData(data);
        const step = Math.floor(data.length / 5) || 1;
        setAudioLevels(
          Array.from({ length: 5 }, (_, j) =>
            Math.min(100, Math.floor(((data[j * step] || 0) / 200) * 100))
          )
        );
        audioAnimRef.current = requestAnimationFrame(tick);
      };
      audioAnimRef.current = requestAnimationFrame(tick);
    } catch (_) {
      // Mic permission already handled by setup page — silently skip
    }
  }, []);

  const stopAnalyser = useCallback(() => {
    if (audioAnimRef.current) { cancelAnimationFrame(audioAnimRef.current); audioAnimRef.current = null; }
    audioStreamRef.current?.getTracks().forEach(t => t.stop());
    audioStreamRef.current = null;
    audioCtxRef.current?.close().catch(() => {});
    audioCtxRef.current = null;
    audioAnalyserRef.current = null;
    setAudioLevels([0, 0, 0, 0, 0]);
  }, []);

  // ── Silence timer ─────────────────────────────────────────────────────────────
  const clearSilence = useCallback(() => {
    if (silenceTimerRef.current)    { clearTimeout(silenceTimerRef.current);   silenceTimerRef.current = null; }
    if (countdownIntervalRef.current) { clearInterval(countdownIntervalRef.current); countdownIntervalRef.current = null; }
    setCountdownPercent(100);
  }, []);

  const startSilenceTimer = useCallback(() => {
    clearSilence();
    if (interactionModeRef.current !== "auto") return;

    const DURATION = 2500;
    const t0 = Date.now();

    countdownIntervalRef.current = setInterval(() => {
      const pct = Math.max(0, ((DURATION - (Date.now() - t0)) / DURATION) * 100);
      setCountdownPercent(pct);
    }, 80);

    silenceTimerRef.current = setTimeout(() => {
      clearSilence();
      const text = textInputRef.current.trim();
      if (text && submitRef.current) submitRef.current(text);
    }, DURATION);
  }, [clearSilence]);

  // ── STT lifecycle ─────────────────────────────────────────────────────────────
  const stopSTT = useCallback(() => {
    try { recognitionRef.current?.abort(); } catch (_) {}
    recognitionRef.current = null;
    setInterimText("");
    stopAnalyser();
  }, [stopAnalyser]);

  // startSTT is defined as a callback that reads voicePhaseRef — the gate ensures
  // it never starts unless the machine says LISTENING or REVIEWING.
  const startSTT = useCallback(() => {
    const phase = voicePhaseRef.current;
    if (!hasSttSupport)                              return;
    if (isMutedRef.current)                          return;
    if (interactionModeRef.current === "keyboard")   return;
    if (phase !== PHASE.LISTENING && phase !== PHASE.REVIEWING) return;

    // Cleanly kill any previous instance — its onend won't restart because
    // we're about to create a fresh one immediately after.
    try { recognitionRef.current?.abort(); } catch (_) {}

    const rec = new SpeechRecognition();
    rec.continuous     = true;
    rec.interimResults = true;
    rec.lang           = "en-US";
    rec.maxAlternatives = 1;
    recognitionRef.current = rec;

    rec.onstart = () => {
      startAnalyser();
    };

    rec.onend = () => {
      setInterimText("");
      stopAnalyser();
      // Only restart if we're genuinely still listening and nothing stopped us
      if (voicePhaseRef.current === PHASE.LISTENING) {
        setTimeout(() => {
          if (voicePhaseRef.current === PHASE.LISTENING) startSTTRef.current?.();
        }, 300);
      }
    };

    rec.onerror = (e) => {
      if (e.error === "not-allowed")
        toast.error("Microphone blocked. Please allow microphone access in your browser settings.");
      if (e.error !== "aborted" && e.error !== "no-speech")
        console.warn("STT error:", e.error);
      setInterimText("");
      stopAnalyser();
    };

    rec.onresult = (e) => {
      let interim = "";
      let final   = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) final   += e.results[i][0].transcript;
        else                       interim += e.results[i][0].transcript;
      }

      if (final.trim()) {
        // Append final speech to text box and start the silence countdown
        setTextInput(prev => {
          const next = prev.trim() ? `${prev.trim()} ${final.trim()}` : final.trim();
          textInputRef.current = next;
          return next;
        });
        setPhase(PHASE.REVIEWING);
        startSilenceTimer();
      } else if (interim.trim() && voicePhaseRef.current === PHASE.LISTENING) {
        // Show interim text without changing phase yet
        setPhase(PHASE.REVIEWING);
      }
      setInterimText(interim);
    };

    try { rec.start(); } catch (e) { console.warn("STT start failed:", e); }
  }, [hasSttSupport, startAnalyser, stopAnalyser, startSilenceTimer, setPhase]);

  // Keep stable ref so callbacks (rec.onend, silence timer) always call the latest
  useEffect(() => { startSTTRef.current = startSTT; }, [startSTT]);

  // ── Mic mute toggle ───────────────────────────────────────────────────────────
  const toggleMic = useCallback(() => {
    setIsMuted(prev => {
      const next = !prev;
      isMutedRef.current = next;
      if (next) {
        // Muting: stop STT & silence timer
        stopSTT();
        clearSilence();
        if (voicePhaseRef.current === PHASE.LISTENING ||
            voicePhaseRef.current === PHASE.REVIEWING) {
          setPhase(PHASE.IDLE);
        }
      } else if (voicePhaseRef.current === PHASE.LISTENING) {
        // Unmuting while we should be listening: restart STT
        setTimeout(() => startSTTRef.current?.(), 150);
      }
      return next;
    });
  }, [stopSTT, clearSilence, setPhase]);

  // ── Submit answer ─────────────────────────────────────────────────────────────
  const handleSubmit = useCallback((text) => {
    const sid = sessionIdRef.current;
    if (!text?.trim() || !sid) return;

    stopSTT();
    _stopAllAudio();
    clearSilence();
    setPhase(PHASE.SUBMITTING);

    // Clear input immediately (no stale text while AI thinks)
    setTextInput("");
    textInputRef.current = "";
    setInterimText("");

    dispatch(appendTranscript({
      from:  "you",
      text:  text.trim(),
      topic: currentTopicRef.current,
    }));
    dispatch(submitAnswer({
      sessionId: sid,
      answer:    text.trim(),
      topic:     currentTopicRef.current,
    }));
  }, [dispatch, stopSTT, clearSilence, setPhase]);

  // Keep submit ref stable for the silence timer closure
  useEffect(() => { submitRef.current = handleSubmit; }, [handleSubmit]);

  // ── Bootstrap session on first render ─────────────────────────────────────────
  useEffect(() => {
    if (sessionInitRef.current) return;
    sessionInitRef.current = true;

    const payload = setupPayload || buildFallbackPayload(role, difficulty);
    dispatch(startInterview(payload));

    return () => {
      // Full cleanup on unmount
      clearSilence();
      stopSTT();
      _stopAllAudio();
      stopAnalyser();
      clearInterval(timerRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── React to new question: TTS → STT chain ────────────────────────────────────
  useEffect(() => {
    if (isCompleted) return;

    const msg = currentPreamble
      ? `${currentPreamble}. ${currentQuestion}`
      : currentQuestion;

    // Deduplicate: don't re-trigger for the same message
    if (!msg || msg === lastMsgRef.current) return;
    lastMsgRef.current = msg;

    // Reset input/timers for fresh answer
    clearSilence();
    setTextInput("");
    textInputRef.current = "";
    setInterimText("");
    stopSTT();

    if (!ttsEnabledRef.current) {
      // TTS off → go straight to listening
      setPhase(PHASE.LISTENING);
      if (!isMutedRef.current && interactionModeRef.current !== "keyboard") {
        setTimeout(() => startSTTRef.current?.(), 100);
      }
      return;
    }

    // TTS on → speak, then start STT in the onEnd callback
    setPhase(PHASE.SPEAKING);
    speakText(msg, {
      baseUrl,
      onStart: () => setPhase(PHASE.SPEAKING),
      onEnd:   () => {
        setPhase(PHASE.LISTENING);
        if (!isMutedRef.current && interactionModeRef.current !== "keyboard") {
          setTimeout(() => startSTTRef.current?.(), 300);
        }
      },
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentQuestion]);

  // ── Handle interview completion ────────────────────────────────────────────────
  useEffect(() => {
    if (!isCompleted || !sessionId) return;
    setPhase(PHASE.COMPLETED);
    stopSTT();
    clearSilence();
    clearInterval(timerRef.current);

    if (ttsEnabled && closingMessage) {
      speakText(closingMessage, {
        baseUrl,
        onEnd: () => setTimeout(() => navigate(`/app/interviews/${sessionId}/report`), 1200),
      });
    } else {
      setTimeout(() => navigate(`/app/interviews/${sessionId}/report`), 2500);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isCompleted, sessionId]);

  // ── Show API errors ──────────────────────────────────────────────────────────
  useEffect(() => {
    if (sessionError) toast.error(sessionError);
  }, [sessionError]);

  // ── Interaction mode switch ──────────────────────────────────────────────────
  useEffect(() => {
    if (interactionMode === "keyboard") {
      isMutedRef.current = true;
      setIsMuted(true);
      stopSTT();
    } else if (voicePhaseRef.current === PHASE.LISTENING) {
      isMutedRef.current = false;
      setIsMuted(false);
      setTimeout(() => startSTTRef.current?.(), 100);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [interactionMode]);

  // ── Manual end call ──────────────────────────────────────────────────────────
  const handleEndCall = async () => {
    _stopAllAudio();
    stopSTT();
    clearSilence();
    clearInterval(timerRef.current);
    if (sessionId) {
      try {
        await fetch(`${baseUrl}/interview/end`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId }),
        });
      } catch (_) { /* non-fatal */ }
      navigate(`/app/interviews/${sessionId}/report`);
    } else {
      dispatch(clearSession());
      navigate("/app/interviews");
    }
  };

  // ── Derived booleans for render ──────────────────────────────────────────────
  const isListening = voicePhase === PHASE.LISTENING || voicePhase === PHASE.REVIEWING;
  const isThinking  = isStarting || isSubmitting;
  const displayPhase = isThinking ? PHASE.IDLE : voicePhase;

  const phaseLabel = {
    intro:              "Introduction",
    adaptive_questions: "Technical Q&A",
    closing:            "Closing",
  }[interviewPhase] || interviewPhase;

  // ─── Render ──────────────────────────────────────────────────────────────────
  return (
    <AppShell>
      {/* ── Top bar ── */}
      <div className="flex items-center justify-between border-b border-border px-4 py-3 md:px-6">
        <div className="flex items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-foreground">
            <Link to="/app/interviews"><ArrowLeft className="h-4 w-4" /></Link>
          </Button>
          <div>
            <p className="text-sm font-semibold text-foreground">
              {role} · <span className="text-zinc-400 font-normal">{difficulty}</span>
            </p>
            <p className="text-[11px] text-muted-foreground capitalize">{phaseLabel}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {coveredTopics.length > 0 && (
            <Badge variant="outline" className="hidden sm:flex text-[10px] border-zinc-800 text-zinc-400 font-mono">
              {coveredTopics.length}/{coveredTopics.length + remainingTopics.length} topics
            </Badge>
          )}
          <Badge variant="outline" className="gap-1.5 text-emerald-400 border-emerald-800/40 bg-emerald-950/20">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" /> Live
          </Badge>
          <Badge variant="outline" className="font-mono text-zinc-300 border-zinc-700">
            {formatTime(elapsedSeconds)}
          </Badge>
        </div>
      </div>

      {/* ── Main layout ── */}
      <div className="relative flex min-h-[calc(100vh-57px)] flex-col bg-[#050505] lg:flex-row">

        {/* ── Left: Stage ── */}
        <div className="relative flex flex-1 flex-col">
          <div className="flex flex-1 flex-col items-center justify-center gap-10 px-4 py-12">

            <AIAvatar phase={displayPhase} />

            {/* Question / status card */}
            <div className="w-full max-w-2xl space-y-2 mt-8">
              {isStarting ? (
                <div className="flex flex-col items-center gap-3 rounded-2xl border border-zinc-800/60 bg-zinc-900/40 px-6 py-8 text-center">
                  <Loader2 className="h-6 w-6 animate-spin text-primary" />
                  <p className="text-sm text-zinc-400">Connecting to Sara, your AI interviewer…</p>
                </div>
              ) : isCompleted ? (
                <div className="flex flex-col items-center gap-3 rounded-2xl border border-emerald-800/40 bg-emerald-950/20 px-6 py-8 text-center">
                  <CheckCircle2 className="h-8 w-8 text-emerald-400" />
                  <p className="text-base font-semibold text-emerald-300">Interview Complete!</p>
                  <p className="text-sm text-zinc-400">{closingMessage || "Generating your report…"}</p>
                  <Loader2 className="h-4 w-4 animate-spin text-zinc-500 mt-1" />
                </div>
              ) : (
                <>
                  {currentPreamble && (
                    <p className="text-center text-[11px] uppercase tracking-widest text-zinc-500 font-medium">
                      {currentPreamble}
                    </p>
                  )}
                  <div className="rounded-2xl border border-zinc-800/60 bg-zinc-900/50 px-6 py-5 backdrop-blur">
                    <p className="text-[10px] uppercase tracking-wider text-primary font-semibold mb-2">Sara is asking</p>
                    <p className="text-base text-zinc-100 leading-relaxed font-medium">
                      {currentQuestion || "Waiting for the next question…"}
                    </p>
                    {answerGuidance && (
                      <p className="mt-3 text-[11px] text-zinc-500 italic leading-relaxed border-t border-zinc-800 pt-3">
                        💡 {answerGuidance}
                      </p>
                    )}
                  </div>
                </>
              )}
            </div>

            {/* Speech preview / silence countdown */}
            {(interimText || (voicePhase === PHASE.REVIEWING && textInput.trim())) && (
              <div className="w-full max-w-2xl rounded-xl border border-zinc-800/40 bg-zinc-900/40 px-4 py-3 space-y-2">
                <div className="flex justify-between items-center">
                  <p className="text-[10px] uppercase tracking-wider text-zinc-500 font-semibold">
                    {interimText ? "You're saying…" : "Voice Answer Ready"}
                  </p>
                  {interactionMode === "auto" && textInput.trim() && !isSubmitting && (
                    <span className="text-[10px] text-amber-500 font-medium">
                      Auto-sending in {((countdownPercent * 2.5) / 100).toFixed(1)}s
                    </span>
                  )}
                </div>
                <p className="text-sm text-zinc-300 italic">{interimText || textInput}</p>
                {interactionMode === "auto" && textInput.trim() && !isSubmitting && (
                  <div className="h-1 w-full bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-amber-600 to-primary transition-all duration-75"
                      style={{ width: `${countdownPercent}%` }} />
                  </div>
                )}
              </div>
            )}

            {/* User presence tile */}
            <div className="flex w-full max-w-xs items-center gap-3 rounded-xl border border-zinc-800/50 bg-zinc-900/40 px-4 py-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-sm font-bold text-zinc-300">
                You
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-zinc-200">You</p>
                <p className="text-[10px] text-muted-foreground truncate">
                  {voicePhase === PHASE.LISTENING  ? "Listening… speak your answer"
                  : voicePhase === PHASE.REVIEWING ? "Got it — counting down"
                  : isMuted                        ? "Microphone muted"
                  :                                  "Microphone ready"}
                </p>
              </div>
              <AudioVisualizer levels={audioLevels} active={isListening} />
              <div className="shrink-0 ml-1">
                {isMuted
                  ? <MicOff className="h-4 w-4 text-destructive" />
                  : isListening
                  ? <Mic className="h-4 w-4 text-emerald-400 animate-pulse" />
                  : <Mic className="h-4 w-4 text-zinc-500" />}
              </div>
            </div>
          </div>

          {/* ── Input area ── */}
          {!isCompleted && !isStarting && (
            <div className="border-t border-zinc-900 bg-zinc-950/80 px-4 py-4 space-y-3">
              {/* Mode toggles */}
              <div className="flex flex-wrap items-center justify-center gap-2 max-w-2xl mx-auto border-b border-zinc-900/60 pb-3">
                <span className="text-[10px] uppercase tracking-wider text-zinc-500 font-semibold mr-2">Mode:</span>
                {[
                  { id: "auto",     label: "🎙️ Voice Auto-Submit" },
                  { id: "ptt",      label: "🎯 Push to Talk"       },
                  { id: "keyboard", label: "⌨️ Keyboard Only"      },
                ].map(({ id, label }) => (
                  <button key={id} type="button" onClick={() => setInteractionMode(id)}
                    className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${
                      interactionMode === id
                        ? "bg-primary/10 border-primary text-primary"
                        : "bg-zinc-900/40 border-zinc-800 text-zinc-400 hover:text-zinc-300"
                    }`}>
                    {label}
                  </button>
                ))}
              </div>

              <form
                onSubmit={e => { e.preventDefault(); if (textInput.trim()) handleSubmit(textInput.trim()); }}
                className="flex items-center gap-2 max-w-2xl mx-auto">
                <input
                  type="text"
                  value={textInput}
                  onChange={e => setTextInput(e.target.value)}
                  placeholder={
                    interactionMode === "keyboard" ? "Type your answer here…"
                    : isListening                  ? "Listening via mic… or type / edit here"
                    :                                "Mic paused — type here or unmute"
                  }
                  disabled={isSubmitting}
                  className="flex-1 rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:ring-1 focus:ring-primary/50 disabled:opacity-50"
                />
                <Button
                  type="submit"
                  disabled={!textInput.trim() || isSubmitting || !sessionId}
                  size="icon"
                  className="h-10 w-10 shrink-0 bg-primary hover:bg-orange-600 text-white">
                  {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </form>
            </div>
          )}

          {/* ── Call controls ── */}
          <div className="flex items-center justify-center gap-5 border-t border-zinc-900 bg-zinc-950/90 py-5">
            {/* TTS toggle */}
            <button
              onClick={() => {
                const next = !ttsEnabled;
                setTtsEnabled(next);
                ttsEnabledRef.current = next;
                if (!next) _stopAllAudio();
                toast(next ? "Sara's voice enabled" : "Sara's voice muted");
              }}
              title={ttsEnabled ? "Mute Sara's voice" : "Enable Sara's voice"}
              className="flex h-12 w-12 items-center justify-center rounded-full border border-zinc-800 bg-zinc-900 text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white">
              {ttsEnabled ? <Volume2 className="h-5 w-5" /> : <VolumeX className="h-5 w-5" />}
            </button>

            {/* Mic toggle */}
            <button
              onClick={toggleMic}
              title={isMuted ? "Unmute mic" : "Mute mic"}
              className={`flex h-14 w-14 items-center justify-center rounded-full border transition-colors ${
                isMuted
                  ? "border-destructive/60 bg-destructive/15 text-destructive"
                  : isListening
                  ? "border-emerald-600/60 bg-emerald-950/40 text-emerald-400"
                  : "border-zinc-700 bg-zinc-900 text-zinc-300 hover:bg-zinc-800"
              }`}>
              {isMuted ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
            </button>

            {/* End call */}
            <button
              onClick={handleEndCall}
              title="End interview"
              className="flex h-14 w-20 items-center justify-center rounded-full bg-destructive text-white transition-colors hover:bg-red-700">
              <PhoneOff className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* ── Right: Transcript sidebar ── */}
        <aside className="flex w-full flex-col border-t border-zinc-900 bg-zinc-950/80 lg:w-[360px] lg:border-l lg:border-t-0">
          <div className="flex items-center gap-2 border-b border-zinc-900 px-4 py-3">
            <MessageSquare className="h-4 w-4 text-primary" />
            <p className="text-sm font-semibold text-zinc-100">Live Transcript</p>
            <Badge variant="outline" className="ml-auto text-[10px] border-zinc-800 text-zinc-500">Auto</Badge>
          </div>

          <div
            ref={transcriptRef}
            className="flex-1 space-y-4 overflow-auto px-4 py-4 scroll-smooth"
            style={{ maxHeight: "calc(100vh - 57px - 49px)" }}>

            {transcript.length === 0 && !isStarting && (
              <p className="text-center text-xs text-zinc-600 pt-8">Transcript will appear here…</p>
            )}
            {isStarting && (
              <div className="flex flex-col items-center gap-2 pt-8">
                <Loader2 className="h-5 w-5 animate-spin text-zinc-600" />
                <p className="text-xs text-zinc-600">Connecting…</p>
              </div>
            )}

            {transcript.map(msg => <TranscriptMessage key={msg.id} msg={msg} />)}

            {/* Live interim preview */}
            {interimText && (
              <div className="flex flex-col items-end">
                <div className="mb-1 text-[10px] text-muted-foreground font-semibold">You (live)</div>
                <div className="max-w-[92%] rounded-2xl rounded-tr-sm bg-primary/30 border border-primary/20 px-3.5 py-2.5 text-sm text-zinc-200 italic">
                  {interimText}…
                </div>
              </div>
            )}

            {/* AI thinking indicator */}
            {isSubmitting && (
              <div className="flex items-center gap-2 text-xs text-zinc-500 pl-1">
                <Loader2 className="h-3 w-3 animate-spin" /> Sara is thinking…
              </div>
            )}
          </div>

          {!hasSttSupport && (
            <div className="flex items-start gap-2 border-t border-zinc-900 px-4 py-3 text-[11px] text-amber-500/80">
              <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
              <span>Speech recognition not supported in this browser. Use the text input below.</span>
            </div>
          )}
        </aside>
      </div>
    </AppShell>
  );
}

// ─── Fallback payload when setup page didn't set Redux state ──────────────────
function buildFallbackPayload(role, difficulty) {
  const diffMap = { Easy: "easy", Intermediate: "medium", Hard: "hard" };
  return {
    mock_test: {
      role,
      interview_type: "technical",
      difficulty: diffMap[difficulty] || "medium",
      job_description: `We are looking for a ${role}. Please assess the candidate on their technical knowledge and problem-solving skills.`,
      topics: [],
      max_questions: 8,
      min_questions: 5,
    },
    parsed_resume: { summary: "", skills: [], technologies: [], experience: [], projects: [] },
  };
}

export default LiveInterview;
