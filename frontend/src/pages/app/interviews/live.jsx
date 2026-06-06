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

// ─── Helpers ────────────────────────────────────────────────────────────────

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition || null;

function speak(text, onStart, onEnd) {
  if (!window.speechSynthesis) {
    onEnd?.();
    return;
  }
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 0.95;
  utter.pitch = 1.05;
  utter.volume = 1;

  // Prefer a good voice
  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(
    (v) =>
      v.name.toLowerCase().includes("samantha") ||
      v.name.toLowerCase().includes("google us english") ||
      v.name.toLowerCase().includes("zira") ||
      (v.lang === "en-US" && !v.name.toLowerCase().includes("microsoft"))
  );
  if (preferred) utter.voice = preferred;

  utter.onstart = onStart;
  utter.onend = onEnd;
  utter.onerror = onEnd;
  window.speechSynthesis.speak(utter);
}

// ─── Pulsing AI Avatar ───────────────────────────────────────────────────────

function AIAvatar({ isSpeaking, isListening, isThinking }) {
  return (
    <div className="relative flex items-center justify-center select-none">
      {/* Outermost ring */}
      <span
        className="absolute rounded-full border border-primary/10 transition-all duration-700"
        style={{
          width: isSpeaking ? 260 : 220,
          height: isSpeaking ? 260 : 220,
          opacity: isSpeaking ? 0.4 : 0.15,
        }}
      />
      {/* Middle ring */}
      <span
        className="absolute rounded-full border border-primary/20 transition-all duration-500"
        style={{
          width: isSpeaking ? 210 : 180,
          height: isSpeaking ? 210 : 180,
          opacity: isSpeaking ? 0.55 : 0.2,
        }}
      />
      {/* Inner glow */}
      <span
        className="absolute rounded-full bg-primary/10 transition-all duration-400"
        style={{
          width: isSpeaking ? 165 : 145,
          height: isSpeaking ? 165 : 145,
        }}
      />
      {/* Avatar circle */}
      <div className="relative z-10 flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br from-primary via-orange-600 to-amber-600 text-4xl font-bold text-white shadow-[0_0_40px_rgba(255,101,0,0.35)]">
        S
      </div>
      {/* Status label */}
      <div className="absolute -bottom-8 flex items-center gap-1.5 text-xs font-medium">
        {isThinking ? (
          <>
            <Loader2 className="h-3 w-3 animate-spin text-amber-400" />
            <span className="text-amber-400">Processing…</span>
          </>
        ) : isSpeaking ? (
          <>
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-primary" />
            <span className="text-primary">Sara is speaking</span>
          </>
        ) : isListening ? (
          <>
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
            <span className="text-emerald-400">Listening…</span>
          </>
        ) : (
          <span className="text-zinc-500">Ready</span>
        )}
      </div>
    </div>
  );
}

// ─── Transcript Message ──────────────────────────────────────────────────────

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
      <div
        className={`max-w-[92%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${isAI
            ? "rounded-tl-sm bg-zinc-900/80 border border-zinc-800 text-zinc-100"
            : "rounded-tr-sm bg-primary/90 text-white"
          }`}
      >
        {msg.text}
      </div>
      {msg.evaluation && (
        <div className="mt-1.5 flex items-center gap-1 text-[10px] text-emerald-400 font-medium">
          <CheckCircle2 className="h-3 w-3" />
          Score: {msg.evaluation.score ?? "—"}/10 · {msg.evaluation.summary ?? ""}
        </div>
      )}
    </div>
  );
}

// ─── Audio Visualizer ───────────────────────────────────────────────────────

function AudioVisualizer({ levels, isListening }) {
  if (!isListening) {
    return (
      <div className="flex items-center gap-1 h-4 px-1">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="w-1 h-1.5 rounded-full bg-zinc-700/60"
          />
        ))}
      </div>
    );
  }

  return (
    <div className="flex items-end gap-1 h-4 px-1">
      {levels.map((level, i) => (
        <div
          key={i}
          className="w-1 rounded-full bg-gradient-to-t from-primary via-orange-500 to-amber-400 transition-all duration-75"
          style={{
            height: `${Math.max(20, level)}%`,
          }}
        />
      ))}
    </div>
  );
}

// ─── Main Component ──────────────────────────────────────────────────────────

function LiveInterview() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const role = searchParams.get("role") || "Senior Backend Engineer";
  const difficulty = searchParams.get("difficulty") || "Intermediate";

  // ── Redux state ────────────────────────────────────────────────────────────
  const {
    setupPayload,
    sessionId,
    currentQuestion,
    currentPreamble,
    currentTopic,
    answerGuidance,
    interviewPhase,
    transcript,
    isCompleted,
    closingMessage,
    isStarting,
    isSubmitting,
    sessionError,
    coveredTopics,
    remainingTopics,
  } = useAppSelector((s) => s.interviews);

  // ── Local UI state ─────────────────────────────────────────────────────────
  const [isMuted, setIsMuted] = useState(false);
  const [ttsEnabled, setTtsEnabled] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);   // AI TTS
  const [isListening, setIsListening] = useState(false);  // STT active
  const [interimText, setInterimText] = useState("");     // STT live preview
  const [textInput, setTextInput] = useState("");
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [hasSttSupport] = useState(() => !!SpeechRecognition);
  const [sessionStarted, setSessionStarted] = useState(false);

  // New state for interaction mode and silence auto-submit
  const [interactionMode, setInteractionMode] = useState("auto"); // "auto", "ptt", "keyboard"
  const [countdownPercent, setCountdownPercent] = useState(100);
  const [audioLevels, setAudioLevels] = useState([0, 0, 0, 0, 0]);

  const transcriptRef = useRef(null);
  const recognitionRef = useRef(null);
  const timerRef = useRef(null);
  const lastQuestionRef = useRef("");

  // Refs for tracking values inside event handlers (preventing stale closures)
  const sessionIdRef = useRef(sessionId);
  const isSubmittingRef = useRef(isSubmitting);
  const currentTopicRef = useRef(currentTopic);
  const isMutedRef = useRef(isMuted);
  const interactionModeRef = useRef(interactionMode);
  const isSpeakingRef = useRef(isSpeaking);
  const isCompletedRef = useRef(isCompleted);
  const textInputRef = useRef(textInput);

  // Sync refs with state
  useEffect(() => {
    sessionIdRef.current = sessionId;
    isSubmittingRef.current = isSubmitting;
    currentTopicRef.current = currentTopic;
    isMutedRef.current = isMuted;
    interactionModeRef.current = interactionMode;
    isSpeakingRef.current = isSpeaking;
    isCompletedRef.current = isCompleted;
    textInputRef.current = textInput;
  }, [sessionId, isSubmitting, currentTopic, isMuted, interactionMode, isSpeaking, isCompleted, textInput]);

  // Audio Analyser refs
  const audioContextRef = useRef(null);
  const audioStreamRef = useRef(null);
  const audioAnalyserRef = useRef(null);
  const audioAnimationRef = useRef(null);

  // Silence Timer refs
  const silenceTimerIdRef = useRef(null);
  const countdownIntervalIdRef = useRef(null);

  // ── Timer ──────────────────────────────────────────────────────────────────
  useEffect(() => {
    timerRef.current = setInterval(() => setElapsedSeconds((s) => s + 1), 1000);
    return () => clearInterval(timerRef.current);
  }, []);

  const formatTime = (s) => {
    const m = Math.floor(s / 60).toString().padStart(2, "0");
    const sec = (s % 60).toString().padStart(2, "0");
    return `${m}:${sec}`;
  };

  // ── Scroll transcript ──────────────────────────────────────────────────────
  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [transcript, interimText]);

  // ── Bootstrap session on mount ─────────────────────────────────────────────
  useEffect(() => {
    if (sessionStarted) return;
    setSessionStarted(true);

    const payload = setupPayload || buildFallbackPayload(role, difficulty);
    dispatch(startInterview(payload));

    return () => {
      window.speechSynthesis?.cancel();
      recognitionRef.current?.abort();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Handle completion ──────────────────────────────────────────────────────
  useEffect(() => {
    if (!isCompleted || !sessionId) return;

    if (ttsEnabled && closingMessage) {
      speak(closingMessage, null, () => {
        setTimeout(() => {
          navigate(`/app/interviews/${sessionId}/report`);
        }, 1200);
      });
    } else {
      setTimeout(() => {
        navigate(`/app/interviews/${sessionId}/report`);
      }, 2500);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isCompleted, sessionId]);

  // ── Show session errors ────────────────────────────────────────────────────
  useEffect(() => {
    if (sessionError) toast.error(sessionError);
  }, [sessionError]);

  // Silence timers
  const clearSilenceTimer = useCallback(() => {
    if (silenceTimerIdRef.current) {
      clearTimeout(silenceTimerIdRef.current);
      silenceTimerIdRef.current = null;
    }
    if (countdownIntervalIdRef.current) {
      clearInterval(countdownIntervalIdRef.current);
      countdownIntervalIdRef.current = null;
    }
    setCountdownPercent(100);
  }, []);

  const handleSubmitAnswerRef = useRef(null);

  const resetSilenceTimer = useCallback(() => {
    clearSilenceTimer();

    if (interactionModeRef.current !== "auto") return;
    if (!textInputRef.current.trim()) return; // Don't trigger if nothing is transcribed

    const start = Date.now();
    const duration = 2500; // 2.5s silence duration

    countdownIntervalIdRef.current = setInterval(() => {
      const elapsed = Date.now() - start;
      const remaining = Math.max(0, duration - elapsed);
      setCountdownPercent((remaining / duration) * 100);
    }, 100);

    silenceTimerIdRef.current = setTimeout(() => {
      clearSilenceTimer();
      const finalVal = textInputRef.current.trim();
      if (finalVal && handleSubmitAnswerRef.current) {
        handleSubmitAnswerRef.current(finalVal);
      }
    }, duration);
  }, [clearSilenceTimer]);

  // Audio Analyser
  const startAudioAnalyser = useCallback(async () => {
    if (audioContextRef.current) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioStreamRef.current = stream;

      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      const context = new AudioContextClass();
      audioContextRef.current = context;

      const analyser = context.createAnalyser();
      analyser.fftSize = 32;
      audioAnalyserRef.current = analyser;

      const source = context.createMediaStreamSource(stream);
      source.connect(analyser);

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateVolume = () => {
        if (!audioAnalyserRef.current) return;
        analyser.getByteFrequencyData(dataArray);

        const newLevels = [];
        const step = Math.floor(bufferLength / 5) || 1;
        for (let j = 0; j < 5; j++) {
          const val = dataArray[j * step] || 0;
          newLevels.push(Math.min(100, Math.floor((val / 200) * 100)));
        }
        setAudioLevels(newLevels);
        audioAnimationRef.current = requestAnimationFrame(updateVolume);
      };

      audioAnimationRef.current = requestAnimationFrame(updateVolume);
    } catch (err) {
      console.warn("Failed to start audio analyser:", err);
    }
  }, []);

  const stopAudioAnalyser = useCallback(() => {
    if (audioAnimationRef.current) {
      cancelAnimationFrame(audioAnimationRef.current);
      audioAnimationRef.current = null;
    }
    if (audioStreamRef.current) {
      audioStreamRef.current.getTracks().forEach((track) => track.stop());
      audioStreamRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => { });
      audioContextRef.current = null;
    }
    audioAnalyserRef.current = null;
    setAudioLevels([0, 0, 0, 0, 0]);
  }, []);

  useEffect(() => {
    if (isListening) {
      startAudioAnalyser();
    } else {
      stopAudioAnalyser();
    }
  }, [isListening, startAudioAnalyser, stopAudioAnalyser]);

  // ── STT Setup ─────────────────────────────────────────────────────────────
  const startListening = useCallback(() => {
    if (!hasSttSupport || isMutedRef.current || interactionModeRef.current === "keyboard") return;

    try {
      recognitionRef.current?.abort();
    } catch (e) { }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);
      setInterimText("");

      const shouldRestart =
        !isMutedRef.current &&
        !isSubmittingRef.current &&
        !isSpeakingRef.current &&
        !isCompletedRef.current &&
        interactionModeRef.current !== "keyboard";

      if (shouldRestart) {
        setTimeout(() => {
          if (
            !isMutedRef.current &&
            !isSubmittingRef.current &&
            !isSpeakingRef.current &&
            !isCompletedRef.current &&
            interactionModeRef.current !== "keyboard"
          ) {
            try {
              recognitionRef.current?.start();
            } catch (err) { }
          }
        }, 400);
      }
    };

    recognition.onerror = (e) => {
      if (e.error !== "aborted" && e.error !== "no-speech") {
        console.warn(`Speech recognition error: ${e.error}`);
        if (e.error === "not-allowed") {
          toast.error("Microphone access blocked. Please allow mic permissions in your browser.");
        }
      }
      setIsListening(false);
      setInterimText("");
    };

    recognition.onresult = (e) => {
      let interim = "";
      let finalSpeech = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) {
          finalSpeech += e.results[i][0].transcript;
        } else {
          interim += e.results[i][0].transcript;
        }
      }

      if (interim.trim() || finalSpeech.trim()) {
        resetSilenceTimer();
      }

      if (finalSpeech.trim()) {
        setTextInput((prev) => {
          const base = prev.trim();
          return base ? `${base} ${finalSpeech.trim()}` : finalSpeech.trim();
        });
      }

      setInterimText(interim);
    };

    recognitionRef.current = recognition;
    try {
      recognition.start();
    } catch (e) {
      console.warn("Recognition start error:", e);
    }
  }, [hasSttSupport, resetSilenceTimer]);

  const stopListening = useCallback(() => {
    clearSilenceTimer();
    try {
      recognitionRef.current?.stop();
    } catch (e) { }
    setIsListening(false);
    setInterimText("");
  }, [clearSilenceTimer]);

  const toggleMic = useCallback(() => {
    setIsMuted((prevMuted) => {
      const nextMuted = !prevMuted;
      if (nextMuted) {
        stopListening();
      } else {
        if (!isSpeakingRef.current && !isSubmittingRef.current) {
          setTimeout(() => startListening(), 50);
        }
      }
      return nextMuted;
    });
  }, [startListening, stopListening]);

  // ── Submit answer ──────────────────────────────────────────────────────────
  const handleSubmitAnswer = useCallback(
    (text) => {
      const activeSessionId = sessionIdRef.current;
      const submitting = isSubmittingRef.current;
      const topic = currentTopicRef.current;

      if (!text.trim() || !activeSessionId || submitting) return;

      stopListening();
      window.speechSynthesis?.cancel();
      setIsSpeaking(false);
      clearSilenceTimer();

      dispatch(
        appendTranscript({
          from: "you",
          text: text.trim(),
          topic: topic,
        })
      );

      dispatch(
        submitAnswer({
          sessionId: activeSessionId,
          answer: text.trim(),
          topic: topic,
        })
      );
    },
    [dispatch, stopListening, clearSilenceTimer]
  );

  useEffect(() => {
    handleSubmitAnswerRef.current = handleSubmitAnswer;
  }, [handleSubmitAnswer]);

  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (!textInput.trim()) return;
    handleSubmitAnswer(textInput.trim());
    setTextInput("");
  };

  // ── TTS: speak whenever question changes ───────────────────────────────────
  useEffect(() => {
    const msg = currentPreamble
      ? `${currentPreamble}. ${currentQuestion}`
      : currentQuestion;

    if (!msg || msg === lastQuestionRef.current) return;
    lastQuestionRef.current = msg;

    setTextInput("");
    setInterimText("");
    clearSilenceTimer();

    if (!ttsEnabled || !msg) {
      if (!isMutedRef.current && hasSttSupport && interactionModeRef.current !== "keyboard") {
        setTimeout(() => startListening(), 100);
      }
      return;
    }

    setIsSpeaking(true);
    setIsListening(false);
    try {
      recognitionRef.current?.abort();
    } catch (e) { }

    speak(
      msg,
      () => {
        setIsSpeaking(true);
      },
      () => {
        setIsSpeaking(false);
        if (!isMutedRef.current && hasSttSupport && interactionModeRef.current !== "keyboard") {
          setTimeout(() => startListening(), 400);
        }
      }
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentQuestion]);

  // Unmount cleanups
  useEffect(() => {
    return () => {
      clearSilenceTimer();
      stopAudioAnalyser();
      window.speechSynthesis?.cancel();
      try {
        recognitionRef.current?.abort();
      } catch (e) { }
    };
  }, [clearSilenceTimer, stopAudioAnalyser]);

  // Handle interaction mode changes
  useEffect(() => {
    if (interactionMode === "keyboard") {
      setIsMuted(true);
      stopListening();
    } else {
      setIsMuted(false);
      if (!isSpeaking && !isSubmitting) {
        startListening();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [interactionMode]);

  // ── End call manually ──────────────────────────────────────────────────────
  const handleEndCall = () => {
    window.speechSynthesis?.cancel();
    recognitionRef.current?.abort();
    clearInterval(timerRef.current);
    if (sessionId) {
      navigate(`/app/interviews/${sessionId}/report`);
    } else {
      dispatch(clearSession());
      navigate("/app/interviews");
    }
  };

  // ── Phase label ────────────────────────────────────────────────────────────
  const phaseLabel = {
    intro: "Introduction",
    adaptive_questions: "Technical Q&A",
    closing: "Closing",
  }[interviewPhase] || interviewPhase;

  const isThinking = isSubmitting || isStarting;

  // ─── Render ────────────────────────────────────────────────────────────────
  return (
    <AppShell>
      {/* ── Top Bar ── */}
      <div className="flex items-center justify-between border-b border-border px-4 py-3 md:px-6">
        <div className="flex items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-foreground">
            <Link to="/app/interviews">
              <ArrowLeft className="h-4 w-4" />
            </Link>
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
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
            Live
          </Badge>
          <Badge variant="outline" className="font-mono text-zinc-300 border-zinc-700">
            {formatTime(elapsedSeconds)}
          </Badge>
        </div>
      </div>

      {/* ── Main Layout ── */}
      <div className="relative flex min-h-[calc(100vh-57px)] flex-col bg-[#050505] lg:flex-row">

        {/* ── Left: Stage ── */}
        <div className="relative flex flex-1 flex-col">

          {/* Stage area */}
          <div className="flex flex-1 flex-col items-center justify-center gap-10 px-4 py-12">

            {/* AI Avatar */}
            <AIAvatar
              isSpeaking={isSpeaking}
              isListening={isListening}
              isThinking={isThinking}
            />

            {/* Question card */}
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
                    <p className="text-[10px] uppercase tracking-wider text-primary font-semibold mb-2">
                      Sara is asking
                    </p>
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

            {/* STT interim preview or silence countdown */}
            {(interimText || (interactionMode === "auto" && textInput.trim())) && (
              <div className="w-full max-w-2xl rounded-xl border border-zinc-800/40 bg-zinc-900/40 px-4 py-3 space-y-2">
                <div className="flex justify-between items-center">
                  <p className="text-[10px] uppercase tracking-wider text-zinc-500 font-semibold">
                    {interimText ? "You're saying…" : "Voice Answer Transcribed"}
                  </p>
                  {interactionMode === "auto" && textInput.trim() && !isSubmitting && (
                    <span className="text-[10px] text-amber-500 font-medium">
                      Auto-submitting in {((countdownPercent * 2.5) / 100).toFixed(1)}s (pause mic to edit)
                    </span>
                  )}
                </div>
                {interimText ? (
                  <p className="text-sm text-zinc-300 italic">{interimText}</p>
                ) : (
                  <p className="text-sm text-zinc-300">{textInput}</p>
                )}
                {/* Silence countdown progress bar */}
                {interactionMode === "auto" && textInput.trim() && !isSubmitting && (
                  <div className="h-1 w-full bg-zinc-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-amber-600 to-primary transition-all duration-75"
                      style={{ width: `${countdownPercent}%` }}
                    />
                  </div>
                )}
              </div>
            )}

            {/* User tile */}
            <div className="flex w-full max-w-xs items-center gap-3 rounded-xl border border-zinc-800/50 bg-zinc-900/40 px-4 py-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-sm font-bold text-zinc-300">
                You
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-zinc-200">You</p>
                <p className="text-[10px] text-muted-foreground truncate">
                  {isListening
                    ? "Listening… speak your answer"
                    : isMuted
                      ? "Microphone muted"
                      : "Microphone on"}
                </p>
              </div>

              {/* Audio Visualizer */}
              <AudioVisualizer levels={audioLevels} isListening={isListening} />

              <div className="shrink-0 ml-1">
                {isMuted ? (
                  <MicOff className="h-4 w-4 text-destructive shrink-0" />
                ) : isListening ? (
                  <Mic className="h-4 w-4 text-emerald-400 shrink-0 animate-pulse" />
                ) : (
                  <Mic className="h-4 w-4 text-zinc-500 shrink-0" />
                )}
              </div>
            </div>
          </div>

          {/* ── Interaction Settings & Text input fallback (always shown) ── */}
          {!isCompleted && !isStarting && (
            <div className="border-t border-zinc-900 bg-zinc-950/80 px-4 py-4 space-y-3">
              {/* Interaction Mode Toggles */}
              <div className="flex flex-wrap items-center justify-center gap-2 max-w-2xl mx-auto border-b border-zinc-900/60 pb-3">
                <span className="text-[10px] uppercase tracking-wider text-zinc-500 font-semibold mr-2">
                  Mode:
                </span>
                <button
                  type="button"
                  onClick={() => setInteractionMode("auto")}
                  className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${interactionMode === "auto"
                      ? "bg-primary/10 border-primary text-primary"
                      : "bg-zinc-900/40 border-zinc-800 text-zinc-400 hover:text-zinc-300"
                    }`}
                >
                  🎙️ Voice Auto-Submit
                </button>
                <button
                  type="button"
                  onClick={() => setInteractionMode("ptt")}
                  className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${interactionMode === "ptt"
                      ? "bg-primary/10 border-primary text-primary"
                      : "bg-zinc-900/40 border-zinc-800 text-zinc-400 hover:text-zinc-300"
                    }`}
                >
                  🎯 Push to Talk (Manual Send)
                </button>
                <button
                  type="button"
                  onClick={() => setInteractionMode("keyboard")}
                  className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${interactionMode === "keyboard"
                      ? "bg-primary/10 border-primary text-primary"
                      : "bg-zinc-900/40 border-zinc-800 text-zinc-400 hover:text-zinc-300"
                    }`}
                >
                  ⌨️ Keyboard Only
                </button>
              </div>

              <form onSubmit={handleTextSubmit} className="flex items-center gap-2 max-w-2xl mx-auto">
                <input
                  type="text"
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder={
                    interactionMode === "keyboard"
                      ? "Type your answer here…"
                      : isListening
                        ? "Listening via mic… or type/edit here"
                        : "Microphone muted… type here or unmute"
                  }
                  disabled={isSubmitting}
                  className="flex-1 rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:ring-1 focus:ring-primary/50 disabled:opacity-50"
                />
                <Button
                  type="submit"
                  disabled={!textInput.trim() || isSubmitting || !sessionId}
                  size="icon"
                  className="h-10 w-10 shrink-0 bg-primary hover:bg-orange-600 text-white"
                >
                  {isSubmitting ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </form>
            </div>
          )}

          {/* ── Call Controls ── */}
          <div className="flex items-center justify-center gap-5 border-t border-zinc-900 bg-zinc-950/90 py-5">
            {/* TTS toggle */}
            <button
              onClick={() => {
                const next = !ttsEnabled;
                setTtsEnabled(next);
                window.speechSynthesis?.cancel();
                toast(next ? "Voice enabled" : "Voice muted");
              }}
              title={ttsEnabled ? "Mute Sara's voice" : "Enable Sara's voice"}
              className="flex h-12 w-12 items-center justify-center rounded-full border border-zinc-800 bg-zinc-900 text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white"
            >
              {ttsEnabled ? <Volume2 className="h-5 w-5" /> : <VolumeX className="h-5 w-5" />}
            </button>

            {/* Mic toggle */}
            <button
              onClick={toggleMic}
              title={isMuted ? "Unmute mic" : "Mute mic"}
              className={`flex h-14 w-14 items-center justify-center rounded-full border transition-colors ${isMuted
                  ? "border-destructive/60 bg-destructive/15 text-destructive"
                  : isListening
                    ? "border-emerald-600/60 bg-emerald-950/40 text-emerald-400"
                    : "border-zinc-700 bg-zinc-900 text-zinc-300 hover:bg-zinc-800"
                }`}
            >
              {isMuted ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
            </button>

            {/* End call */}
            <button
              onClick={handleEndCall}
              title="End interview"
              className="flex h-14 w-20 items-center justify-center rounded-full bg-destructive text-white transition-colors hover:bg-red-700"
            >
              <PhoneOff className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* ── Right: Transcript Sidebar ── */}
        <aside className="flex w-full flex-col border-t border-zinc-900 bg-zinc-950/80 lg:w-[360px] lg:border-l lg:border-t-0">
          <div className="flex items-center gap-2 border-b border-zinc-900 px-4 py-3">
            <MessageSquare className="h-4 w-4 text-primary" />
            <p className="text-sm font-semibold text-zinc-100">Live Transcript</p>
            <Badge variant="outline" className="ml-auto text-[10px] border-zinc-800 text-zinc-500">
              Auto
            </Badge>
          </div>

          <div
            ref={transcriptRef}
            className="flex-1 space-y-4 overflow-auto px-4 py-4 scroll-smooth"
            style={{ maxHeight: "calc(100vh - 57px - 49px)" }}
          >
            {transcript.length === 0 && !isStarting && (
              <p className="text-center text-xs text-zinc-600 pt-8">
                Transcript will appear here…
              </p>
            )}
            {isStarting && (
              <div className="flex flex-col items-center gap-2 pt-8">
                <Loader2 className="h-5 w-5 animate-spin text-zinc-600" />
                <p className="text-xs text-zinc-600">Connecting…</p>
              </div>
            )}
            {transcript.map((msg) => (
              <TranscriptMessage key={msg.id} msg={msg} />
            ))}

            {/* Live interim preview in transcript */}
            {interimText && (
              <div className="flex flex-col items-end">
                <div className="mb-1 text-[10px] text-muted-foreground font-semibold">You (live)</div>
                <div className="max-w-[92%] rounded-2xl rounded-tr-sm bg-primary/30 border border-primary/20 px-3.5 py-2.5 text-sm text-zinc-200 italic">
                  {interimText}…
                </div>
              </div>
            )}

            {/* Submitting indicator */}
            {isSubmitting && (
              <div className="flex items-center gap-2 text-xs text-zinc-500 pl-1">
                <Loader2 className="h-3 w-3 animate-spin" />
                Sara is thinking…
              </div>
            )}
          </div>

          {/* STT unavailable warning */}
          {!hasSttSupport && (
            <div className="flex items-start gap-2 border-t border-zinc-900 px-4 py-3 text-[11px] text-amber-500/80">
              <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
              <span>Speech recognition not supported in this browser. Use the text input above.</span>
            </div>
          )}
        </aside>
      </div>
    </AppShell>
  );
}

// ─── Fallback payload if setupPayload was not set in Redux ───────────────────

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
    parsed_resume: {
      summary: "",
      skills: [],
      technologies: [],
      experience: [],
      projects: [],
    },
  };
}

export default LiveInterview;
