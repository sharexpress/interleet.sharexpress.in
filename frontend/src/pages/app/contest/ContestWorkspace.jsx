import React, { useEffect, useRef, useState, useCallback } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Play, Send, FileCode2, Terminal as TerminalIcon, Check, X, ArrowLeft, Clock, ShieldAlert, Award, Loader2, RefreshCw, BookOpen, Sparkles, Users } from "lucide-react";
import { toast } from "sonner";

import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { API } from "@/api/api";
import { runCode, submitCode, resetExecution, selectChallengeExecution } from "@/redux/slices/challengeExecutionSlice";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// Monaco Loader
function loadMonaco() {
  return new Promise((resolve) => {
    if (window.__monacoReady) {
      resolve(window.monaco);
      return;
    }
    const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/monaco-editor@0.50.0/min/vs/loader.js";
    s.onload = () => {
      window.require.config({
        paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.50.0/min/vs" },
      });
      window.require(["vs/editor/editor.main"], (monaco) => {
        window.monaco = monaco;
        window.__monacoReady = true;
        resolve(monaco);
      });
    };
    document.head.appendChild(s);
  });
}

function MonacoEditor({ value, language, onChange }) {
  const containerRef = useRef(null);
  const editorRef = useRef(null);
  const subRef = useRef(null);
  const prevLang = useRef(language);

  useEffect(() => {
    let alive = true;
    loadMonaco().then((monaco) => {
      if (!alive || !containerRef.current || editorRef.current) return;

      const editor = monaco.editor.create(containerRef.current, {
        value,
        language: language === "py" ? "python" : language === "ts" ? "typescript" : "javascript",
        theme: "vs-dark",
        fontSize: 13,
        fontFamily: '"JetBrains Mono", "Fira Code", ui-monospace, monospace',
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        lineNumbers: "on",
        renderLineHighlight: "gutter",
        padding: { top: 12, bottom: 12 },
        tabSize: 2,
        wordWrap: "on",
        automaticLayout: true,
        contextmenu: false, // DISABLE CONTEXT MENU IN MONACO
        scrollbar: { verticalScrollbarSize: 5, horizontalScrollbarSize: 5 },
      });

      // BLOCK CONTEXT MENU COPY/PASTE KEYBINDINGS
      editor.onKeyDown((e) => {
        const isCopy = (e.ctrlKey || e.metaKey) && e.keyCode === monaco.KeyCode.KeyC;
        const isPaste = (e.ctrlKey || e.metaKey) && e.keyCode === monaco.KeyCode.KeyV;
        const isCut = (e.ctrlKey || e.metaKey) && e.keyCode === monaco.KeyCode.KeyX;

        if (isCopy || isPaste || isCut) {
          e.preventDefault();
          e.stopPropagation();
          toast.warning("Clipboard operations are blocked in contest mode!");
        }
      });

      editorRef.current = editor;
      subRef.current = editor.onDidChangeModelContent(() => onChange?.(editor.getValue()));
    });

    return () => {
      alive = false;
      subRef.current?.dispose();
      editorRef.current?.dispose();
      editorRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!editorRef.current || !window.monaco) return;
    const model = editorRef.current.getModel();
    if (!model) return;
    window.monaco.editor.setModelLanguage(model, language === "py" ? "python" : language === "ts" ? "typescript" : "javascript");
    if (prevLang.current !== language) {
      model.setValue(value);
      prevLang.current = language;
    }
  }, [language, value]);

  return <div ref={containerRef} style={{ height: "100%", width: "100%" }} />;
}

// Drag Handle for resizable split pane layout
function DragHandle({ onDelta }) {
  const dragging = useRef(false);
  const startX = useRef(0);

  const onMouseDown = useCallback(
    (e) => {
      e.preventDefault();
      dragging.current = true;
      startX.current = e.clientX;
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";

      const onMove = (ev) => {
        if (!dragging.current) return;
        const delta = ev.clientX - startX.current;
        startX.current = ev.clientX;
        onDelta(delta);
      };
      const onUp = () => {
        dragging.current = false;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [onDelta],
  );

  return (
    <div
      onMouseDown={onMouseDown}
      className="group relative z-10 flex-shrink-0"
      style={{ width: 4, cursor: "col-resize" }}
    >
      <div
        className="absolute inset-y-0 left-0 right-0 bg-border opacity-0 transition-opacity group-hover:opacity-100"
        style={{ margin: "0 1px" }}
      />
    </div>
  );
}

function ContestWorkspace() {
  const { code: roomCode } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.user);
  const execState = useSelector(selectChallengeExecution);

  const [contest, setContest] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [currentChallengeIdx, setCurrentChallengeIdx] = useState(0);

  const [editorCode, setEditorCode] = useState("");
  const [language, setLanguage] = useState("py");
  const [leaderboard, setLeaderboard] = useState([]);

  const [warnings, setWarnings] = useState(0);
  const [disqualified, setDisqualified] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);

  const [outputTab, setOutputTab] = useState("testcase"); // "testcase" | "result"
  const [wsUpdateTrigger, setWsUpdateTrigger] = useState(0);

  const containerRef = useRef(null);
  const [leftW, setLeftW] = useState(380);
  const MIN_COL = 220;

  const getW = () => containerRef.current?.offsetWidth ?? window.innerWidth;

  const onDragLeft = useCallback((delta) => {
    setLeftW((w) => Math.max(MIN_COL, Math.min(w + delta, getW() - MIN_COL * 2)));
  }, []);

  const isRunning = execState.runStatus === "loading";
  const isSubmitting = execState.submitStatus === "loading";
  const currentChallenge = challenges[currentChallengeIdx];

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  };

  const fetchContest = async () => {
    try {
      const res = await API.get(`/api/contest/${roomCode}`);
      if (res.data && res.data.success) {
        const data = res.data.data;
        setContest(data);

        // Calculate remaining seconds
        let endTimeStr = data.end_time;
        if (endTimeStr && !endTimeStr.endsWith("Z")) {
          endTimeStr += "Z";
        }
        const end = new Date(endTimeStr);
        const diff = Math.max(0, Math.floor((end - new Date()) / 1000));
        setTimeLeft(diff);

        // Match user's disqualification state
        const selfParticipant = data.participants.find(p => String(p.user_id) === String(user?.user_id));
        if (selfParticipant) {
          setWarnings(selfParticipant.warnings?.length || 0);
          if (selfParticipant.disqualified) {
            setDisqualified(true);
          }
        }

        // Fetch challenge models for slugs
        const chList = [];
        for (const slug of data.challenges) {
          const chRes = await API.get(`/challenges/${slug}?contest_id=${roomCode}`);
          if (chRes.data && chRes.data.success) {
            chList.push(chRes.data.data);
          }
        }
        setChallenges(chList);
        if (chList.length > 0 && !editorCode) {
          const key = language === "py" ? "python" : language === "ts" ? "typescript" : language === "js" ? "javascript" : language;
          const starter = chList[0].starter_code?.[key] || "def solution():\n    pass";
          setEditorCode(starter);
        }
      }
    } catch (err) {
      console.error(err);
      toast.error("Failed to load contest workspace.");
    }
  };

  const logCheatingEvent = async (type) => {
    if (disqualified) return;
    try {
      const res = await API.post(`/api/contest/${roomCode}/cheating`, { event_type: type });
      if (res.data && res.data.success) {
        setWarnings(res.data.warnings_count);
        if (res.data.disqualified) {
          setDisqualified(true);
          toast.error("You have been disqualified for violating contest integrity rules.");
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Setup WebSocket connection to stay in sync with leaderboard and disqualifications
  useEffect(() => {
    if (!contest || !user) return;
    const token = getCookie("user");
    const wsUrl = `ws://localhost:8000/api/contest/ws/${roomCode}${token ? `?token=${token}` : ""}`;
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "leaderboard_update") {
        setWsUpdateTrigger(t => t + 1); // trigger local fetch/reload of standings
      } else if (data.type === "cheating_warning") {
        if (data.username === user.username) {
          setWarnings(data.warnings_count);
          if (data.disqualified) {
            setDisqualified(true);
          }
        }
      }
    };

    return () => {
      ws.close();
    };
  }, [contest, user]);

  // Fetch leaderboard standings
  const fetchLeaderboard = async () => {
    try {
      const res = await API.get(`/api/contest/${roomCode}/leaderboard`);
      if (res.data && res.data.success) {
        setLeaderboard(res.data.data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (roomCode) {
      fetchLeaderboard();
    }
  }, [roomCode, wsUpdateTrigger]);

  useEffect(() => {
    fetchContest();
  }, [roomCode]);

  // Time Countdown
  useEffect(() => {
    if (timeLeft <= 0) return;
    const timer = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timer);
          toast.error("Contest time is up!");
          navigate(`/app/contest/results/${roomCode}`);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft > 0]);

  // Strict anti-cheating window listeners
  useEffect(() => {
    if (disqualified) return;

    const preventDefault = (e) => {
      e.preventDefault();
      toast.warning("Clipboard operations are blocked in contest mode!");
      logCheatingEvent("copy_paste_attempt");
    };

    // Global copy, paste, cut block
    document.addEventListener("copy", preventDefault);
    document.addEventListener("paste", preventDefault);
    document.addEventListener("cut", preventDefault);

    // Tab-switching detection
    const handleVisibilityChange = () => {
      if (document.hidden) {
        toast.error("Warning: Tab switch detected! Keeping focus on this page is required.");
        logCheatingEvent("tab_switch");
      }
    };

    // Focus lost detection
    const handleBlur = () => {
      toast.error("Warning: Focus lost! You clicked outside the contest window.");
      logCheatingEvent("focus_loss");
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("blur", handleBlur);

    return () => {
      document.removeEventListener("copy", preventDefault);
      document.removeEventListener("paste", preventDefault);
      document.removeEventListener("cut", preventDefault);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("blur", handleBlur);
    };
  }, [disqualified]);

  const handleChallengeChange = (idx) => {
    setCurrentChallengeIdx(idx);
    const key = language === "py" ? "python" : language === "ts" ? "typescript" : language === "js" ? "javascript" : language;
    const starter = challenges[idx].starter_code?.[key] || "def solution():\n    pass";
    setEditorCode(starter);
    dispatch(resetExecution());
    setOutputTab("testcase");
  };

  const handleLangChange = (lang) => {
    setLanguage(lang);
    const key = lang === "py" ? "python" : lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang;
    const starter = currentChallenge?.starter_code?.[key] || "def solution():\n    pass";
    setEditorCode(starter);
  };

  const handleRunCode = () => {
    dispatch(resetExecution());
    setOutputTab("result");
    const samples = (currentChallenge?.test_cases || []).filter(tc => !tc.hidden);
    dispatch(runCode({ code: editorCode, language, testCases: samples }));
  };

  const handleSubmitCode = () => {
    dispatch(resetExecution());
    setOutputTab("result");
    dispatch(submitCode({
      code: editorCode,
      language,
      slug: currentChallenge.slug,
      userId: user?.user_id,
      contestId: contest?.contest_id
    }));
  };

  const formatTime = (sec) => {
    const mins = Math.floor(sec / 60);
    const secs = sec % 60;
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  };

  const getSolvedRuntime = (item) => {
    const solved = Object.values(item.scores || {}).filter((s) => s.solved);
    const sum = solved.reduce((acc, curr) => acc + (curr.runtime_ms || 0), 0);
    return sum > 0 ? `${sum.toFixed(0)}ms` : null;
  };

  // Disqualification Lock Screen
  if (disqualified) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-zinc-950 px-4 text-center">
        <div className="max-w-md w-full bg-zinc-900 border border-red-500/30 rounded-2xl p-8 space-y-6 shadow-2xl relative">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 rounded-full bg-red-600/10 border border-red-500 text-red-500 flex items-center justify-center">
            <ShieldAlert className="w-8 h-8 animate-pulse" />
          </div>
          <div className="space-y-2 pt-4">
            <h2 className="text-xl font-bold text-white uppercase tracking-wider">Disqualified</h2>
            <p className="text-sm text-zinc-400">
              Your session has been terminated due to multiple focus losses or tab switching actions, violating the contest integrity rules.
            </p>
          </div>
          <div className="border-t border-zinc-800 pt-4 text-xs text-zinc-500">
            Cheating Violations Limit: 3/3 Exceeded.
          </div>
          <Button className="w-full bg-red-600 hover:bg-red-500 text-white" asChild>
            <Link to="/app/contest">Exit Arena</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <AppShell>
      {/* Workspace Header */}
      <div className="flex items-center justify-between border-b border-border bg-card/40 px-4 py-2.5 md:px-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
            <Link to="/app/contest">
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
          <div>
            <span className="text-xs uppercase font-mono tracking-widest text-zinc-500 font-bold block">
              Contest Match
            </span>
            <span className="text-sm font-bold text-white">
              {contest?.title}
            </span>
          </div>
        </div>

        {/* Timer, Warnings, Submissions */}
        <div className="flex items-center gap-6">

          {/* Warning count badge */}
          <div className="flex items-center gap-1.5 px-3 py-1 bg-red-500/10 border border-red-500/20 text-red-400 rounded-full text-xs font-semibold">
            <ShieldAlert className="h-3.5 w-3.5" />
            <span>Violations: {warnings}/3</span>
          </div>

          {/* Time Countdown clock */}
          <div className="flex items-center gap-2 font-mono text-sm font-bold text-zinc-300 bg-zinc-900 border border-zinc-800 px-3.5 py-1 rounded-lg">
            <Clock className="h-4 w-4 text-primary animate-pulse" />
            <span>{formatTime(timeLeft)}</span>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <Select value={language} onValueChange={handleLangChange}>
              <SelectTrigger className="h-8 w-[120px] bg-zinc-900 border-zinc-850 text-zinc-200 text-xs">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="py">Python</SelectItem>
                <SelectItem value="js">JavaScript</SelectItem>
                <SelectItem value="ts">TypeScript</SelectItem>
              </SelectContent>
            </Select>
            <Button
              variant="outline"
              size="sm"
              className="h-8 text-xs gap-1.5"
              onClick={handleRunCode}
              disabled={isRunning || isSubmitting}
            >
              {isRunning ? <Loader2 className="h-3 animate-spin" /> : <Play className="h-3.5 w-3.5" />}
              Run
            </Button>
            <Button
              size="sm"
              className="h-8 text-xs gap-1.5"
              onClick={handleSubmitCode}
              disabled={isRunning || isSubmitting}
            >
              {isSubmitting ? <Loader2 className="h-3 animate-spin" /> : <Send className="h-3.5 w-3.5" />}
              Submit
            </Button>
          </div>

        </div>
      </div>

      {/* Main split view */}
      <div ref={containerRef} className="flex h-[calc(100vh-109px)] overflow-hidden bg-zinc-950">

        {/* Left: Challenge Details */}
        <div
          className="flex flex-col border-r border-border bg-zinc-900/10 shrink-0 min-h-0"
          style={{ width: leftW, minWidth: MIN_COL }}
        >
          {/* Tabs for switching challenges */}
          <div className="flex border-b border-border bg-card/20 overflow-x-auto shrink-0">
            {challenges.map((ch, idx) => (
              <button
                key={ch.slug}
                onClick={() => handleChallengeChange(idx)}
                className={`flex items-center gap-1.5 px-3.5 py-2.5 text-xs font-semibold border-r border-border transition-colors shrink-0 ${idx === currentChallengeIdx
                    ? "bg-zinc-900 text-primary border-b-2 border-b-primary"
                    : "text-zinc-400 hover:text-white"
                  }`}
              >
                <FileCode2 className="h-3.5 w-3.5" />
                {ch.title}
              </button>
            ))}
          </div>

          {/* Description Content */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {currentChallenge && (
              <>
                <div className="border-b border-zinc-850 pb-3.5 space-y-2">
                  <div className="flex items-center gap-2">
                    <BookOpen className="h-4 w-4 text-primary" />
                    <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wider font-mono">Problem Description</p>
                  </div>
                  <h2 className="text-lg font-bold text-white tracking-tight leading-snug">{currentChallenge.title}</h2>
                  <div className="flex flex-wrap items-center gap-2 pt-1">
                    <DifficultyPill d={currentChallenge.difficulty} />
                    <DomainTag d={currentChallenge.domain} />
                    <span className="inline-flex items-center gap-1 text-[11px] text-zinc-400">
                      <Clock className="h-3.5 w-3.5" /> {currentChallenge.estimated_time_minutes || currentChallenge.minutes || 15}m
                    </span>
                    <span className="inline-flex items-center gap-1 text-[11px] text-zinc-400">
                      <Sparkles className="h-3.5 w-3.5" /> {currentChallenge.xp_reward || currentChallenge.xp || 100} XP
                    </span>
                    <span className="inline-flex items-center gap-1 text-[11px] text-zinc-400">
                      <Users className="h-3.5 w-3.5" /> {currentChallenge.completion_rate || currentChallenge.completion || 85}% Completion
                    </span>
                  </div>
                </div>

                <p className="text-sm text-zinc-300 leading-relaxed whitespace-pre-wrap">
                  {currentChallenge.description || currentChallenge.summary}
                </p>

                {currentChallenge.test_cases?.filter(t => !t.hidden).length > 0 && (
                  <div className="space-y-2.5 pt-2">
                    <h4 className="font-semibold text-zinc-350 text-[10px] uppercase font-mono tracking-wider">
                      Sample Test Cases
                    </h4>
                    {currentChallenge.test_cases.filter(t => !t.hidden).slice(0, 2).map((tc, i) => (
                      <div key={i} className="p-3 bg-zinc-900 border border-zinc-850 rounded-xl space-y-1 font-mono text-[10px]">
                        <div className="text-zinc-500">Input:</div>
                        <pre className="text-zinc-300 bg-zinc-950 p-1.5 rounded border border-zinc-900 overflow-x-auto whitespace-pre-wrap">
                          {tc.stdin || "None"}
                        </pre>
                        <div className="text-zinc-500">Expected Output:</div>
                        <pre className="text-zinc-300 bg-zinc-950 p-1.5 rounded border border-zinc-900 overflow-x-auto whitespace-pre-wrap">
                          {tc.expected_output}
                        </pre>
                      </div>
                    ))}
                  </div>
                )}

                {currentChallenge.hints?.length > 0 && (
                  <div className="pt-2 space-y-2">
                    <h4 className="font-semibold text-zinc-350 text-[10px] uppercase font-mono tracking-wider">Hints</h4>
                    <ol className="list-inside list-decimal space-y-1.5 text-zinc-400 text-xs">
                      {currentChallenge.hints.map((h, i) => (
                        <li key={i} className="leading-relaxed">{h}</li>
                      ))}
                    </ol>
                  </div>
                )}

                {currentChallenge.tags?.length > 0 && (
                  <div className="pt-2 space-y-2">
                    <h4 className="font-semibold text-zinc-350 text-[10px] uppercase font-mono tracking-wider">Tags</h4>
                    <div className="flex flex-wrap gap-1.5">
                      {currentChallenge.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded border border-zinc-800 bg-zinc-900/60 px-2.5 py-0.5 font-mono text-[10px] text-zinc-450"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {/* DRAG: left | center */}
        <DragHandle onDelta={onDragLeft} />

        {/* Center: Editor + Console */}
        <div className="flex flex-col flex-1 min-w-0 min-h-0 border-r border-border">

          {/* File tab bar */}
          <div className="flex items-center gap-1 border-b border-border bg-background/60 px-2 py-1.5 shrink-0">
            <div className="flex items-center gap-2 rounded-t border-b-2 border-primary bg-card px-3 py-1 font-mono text-xs text-foreground">
              <FileCode2 className="h-3 w-3 text-primary" />
              <span>
                {language === "py" ? "solution.py" : language === "ts" ? "solution.ts" : "solution.js"}
              </span>
            </div>
          </div>

          {/* Monaco Editor Container */}
          <div className="flex-1 min-h-0 relative bg-[#1E1E1E]">
            {currentChallenge && (
              <MonacoEditor
                value={editorCode}
                language={language}
                onChange={setEditorCode}
              />
            )}
          </div>

          {/* Console / Output drawer */}
          <div className="h-[240px] flex-shrink-0 border-t border-border bg-zinc-950 flex flex-col min-h-0">
            <div className="flex items-center border-b border-border px-4 py-1.5 bg-zinc-900/40 justify-between shrink-0">
              <span className="text-[10px] font-bold font-mono uppercase text-zinc-400">
                Console Output
              </span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 text-xs font-sans">
              <div className="font-mono text-[10px] space-y-2">
                {isRunning && (
                  <div className="flex items-center gap-2 text-zinc-500 italic py-2">
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                    Running code against sample test cases...
                  </div>
                )}
                {isSubmitting && (
                  <div className="flex items-center gap-2 text-zinc-500 italic py-2">
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                    Submitting code against all system test cases...
                  </div>
                )}

                {!isRunning && !isSubmitting && !execState.runResult && !execState.submitResult && (
                  <div className="text-zinc-500 italic">No output yet. Run or Submit code to see results.</div>
                )}

                {/* Run Result Output */}
                {execState.runResult && (
                  <div className="space-y-2.5">
                    <div className="flex items-center gap-2 text-white font-semibold">
                      <TerminalIcon className="h-4 w-4 text-zinc-400" />
                      <span>Run Results ({execState.runResult.passed_testcases}/{execState.runResult.total_testcases} passed)</span>
                    </div>

                    {execState.runResult.compile_output && (
                      <div className="p-3 bg-red-950/20 border border-red-500/20 rounded-lg text-red-400 overflow-x-auto">
                        <div className="font-bold text-[9px] uppercase tracking-wider mb-1">Compilation Errors:</div>
                        <pre>{execState.runResult.compile_output}</pre>
                      </div>
                    )}

                    {execState.runResult.testcase_results?.map((tc, idx) => (
                      <div key={idx} className="p-3 bg-zinc-900 border border-zinc-850 rounded-xl space-y-1.5">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold text-zinc-300">Test Case #{idx + 1}: {tc.name}</span>
                          <span className={`font-mono text-[9px] px-2 py-0.5 rounded ${tc.passed ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400"
                            }`}>
                            {tc.passed ? "PASSED" : "FAILED"}
                          </span>
                        </div>
                        {tc.stderr && (
                          <pre className="text-red-400 bg-zinc-950 p-2 rounded text-[9px] whitespace-pre-wrap">{tc.stderr}</pre>
                        )}
                        {!tc.passed && (
                          <div className="grid grid-cols-2 gap-2 mt-1">
                            <div>
                              <span className="text-zinc-500 block">Stdout:</span>
                              <pre className="bg-zinc-950 p-2 rounded text-zinc-400 text-[9px] overflow-x-auto">{tc.stdout || "Empty"}</pre>
                            </div>
                            <div>
                              <span className="text-zinc-500 block">Expected:</span>
                              <pre className="bg-zinc-950 p-2 rounded text-zinc-400 text-[9px] overflow-x-auto">{tc.expected_output || "Empty"}</pre>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* Submission Result Output */}
                {execState.submitResult && (
                  <div className="space-y-3">
                    <div className={`p-4 rounded-xl border flex items-start gap-3.5 ${execState.submitResult.success
                        ? "bg-emerald-950/20 border-emerald-500/20 text-emerald-400"
                        : "bg-red-950/20 border-red-500/20 text-red-400"
                      }`}>
                      <div className="shrink-0 mt-0.5">
                        {execState.submitResult.success ? (
                          <Check className="h-6 w-6 text-emerald-400 border border-emerald-500/30 rounded-full p-0.5" />
                        ) : (
                          <X className="h-6 w-6 text-red-400 border border-red-500/30 rounded-full p-0.5" />
                        )}
                      </div>
                      <div className="space-y-1">
                        <h4 className="font-bold text-sm tracking-tight text-white uppercase">
                          {execState.submitResult.verdict}
                        </h4>
                        <p className="text-[11px] text-zinc-400">
                          Passed {execState.submitResult.passed_testcases} / {execState.submitResult.total_testcases} testcases.
                        </p>
                        {execState.submitResult.success && (
                          <p className="text-[10px] text-emerald-400">
                            Challenge solved! Standings updated automatically.
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}

              </div>
            </div>
          </div>

        </div>

        {/* Right Sidebar: Live Standings Leaderboard */}
        <div className="flex flex-col bg-zinc-900/10 min-h-0 border-l border-zinc-850">

          <div className="p-4 border-b border-border flex items-center justify-between bg-zinc-900/40">
            <h3 className="text-xs font-bold text-white flex items-center gap-1.5">
              <Award className="h-4 w-4 text-primary" /> Live Standings
            </h3>
            <button onClick={fetchLeaderboard} className="text-zinc-500 hover:text-white transition-colors">
              <RefreshCw className="h-3 w-3" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {leaderboard.map((item, idx) => {
              const isSelf = String(item.user_id) === String(user?.user_id);
              return (
                <div
                  key={item.user_id}
                  className={`p-3 rounded-xl border flex items-center justify-between gap-3 ${isSelf
                      ? "bg-primary/10 border-primary/40 ring-1 ring-primary/20"
                      : item.disqualified
                        ? "bg-red-950/10 border-red-950/40 opacity-60"
                        : "bg-zinc-900/40 border-zinc-850"
                    }`}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <span className="font-mono text-xs font-semibold text-zinc-500 w-4">
                      #{idx + 1}
                    </span>
                    <div className="min-w-0">
                      <span className={`block text-xs font-semibold truncate ${isSelf ? "text-primary font-bold" : "text-zinc-200"}`}>
                        {item.username}
                      </span>
                      {item.disqualified ? (
                        <span className="text-[9px] text-red-400 font-mono">Disqualified</span>
                      ) : (
                        <div className="flex flex-col gap-0.5">
                          <span className="text-[9px] text-zinc-500 font-mono">
                            {item.warnings_count} warning(s)
                          </span>
                          {getSolvedRuntime(item) && (
                            <span className="text-[9px] text-emerald-500 font-mono font-medium">
                              Runtime: {getSolvedRuntime(item)}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <span className="block text-xs font-bold text-zinc-100">
                      {item.total_score} pts
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Finish contest button */}
          <div className="p-4 border-t border-zinc-850">
            <Button
              className="w-full text-xs"
              variant="outline"
              onClick={() => {
                if (window.confirm("Are you sure you want to exit the contest? You cannot re-enter once the timer ends.")) {
                  navigate(`/app/contest/results/${roomCode}`);
                }
              }}
            >
              Exit Arena & Submit All
            </Button>
          </div>

        </div>

      </div>

    </AppShell>
  );
}

export default ContestWorkspace;
