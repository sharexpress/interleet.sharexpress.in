import { useEffect, useRef, useState, useCallback, memo } from "react";
import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";
import "@xterm/xterm/css/xterm.css";
import { Link, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import EnvironmentCard from "@/components/runtime/EnvironmentCard";
import RuntimeBadge from "@/components/runtime/RuntimeBadge";
import { AppShell } from "@/components/layout/AppShell";
import UpgradeModal from "@/components/UpgradeModal";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Drawer, DrawerContent, DrawerTrigger } from "@/components/ui/drawer";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { runCode, submitCode, resetExecution, selectChallengeExecution } from "@/redux/slices/challengeExecutionSlice";
import ExecutionResult from "@/components/ExecutionResult";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import {
  FetchChallengeBySlug,
  selectChallengeDetail,
  selectDetailLoading,
  selectDetailError,
} from "@/redux/slices/challengesSlice";
import { API } from "@/api/api";
import {
  Play,
  Send,
  FileCode2,
  Terminal as TerminalIcon,
  Check,
  CheckCircle2,
  AlertCircle,
  X,
  ArrowLeft,
  Clock,
  Sparkles,
  Users,
  BookOpen,
  Globe,
  RotateCw,
  RotateCcw,
  Lock,
  Loader2,
  Trash2,
  Plus,
} from "lucide-react";

// ─── Modular Child Components & Configs ───────────────────────────────────────
import MonacoEditor from "./editor/MonacoEditor";
import EnvironmentInfo from "./editor/EnvironmentInfo";
import ConsoleOutput from "./editor/ConsoleOutput";
import { DragHandle, VerticalDragHandle } from "./editor/DragHandles";
import { BrowserPreview } from "./editor/BrowserPreview";
import {
  LANG_LABEL,
  LANG_BADGE,
  LANG_FILE,
  BACKEND_LANG_TO_SHORT,
  getStarter
} from "./editor/editor.config";

// ─── Markdown Parser Helpers ──────────────────────────────────────────────────

function parseItalic(text) {
  const italicRegex = /\*([^*]+)\*/g;
  let match;
  let lastIndex = 0;
  const parts = [];
  while ((match = italicRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }
    parts.push(<em key={`i-${match.index}`} className="italic">{match[1]}</em>);
    lastIndex = italicRegex.lastIndex;
  }
  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }
  return parts.length > 0 ? parts : text;
}

function parseInlineMarkdown(text) {
  const codeRegex = /`([^`]+)`/g;
  let match;
  let lastIndex = 0;
  const tokens = [];
  while ((match = codeRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      tokens.push({ type: 'text', content: text.slice(lastIndex, match.index) });
    }
    tokens.push({ type: 'code', content: match[1] });
    lastIndex = codeRegex.lastIndex;
  }
  if (lastIndex < text.length) {
    tokens.push({ type: 'text', content: text.slice(lastIndex) });
  }
  if (tokens.length === 0) {
    tokens.push({ type: 'text', content: text });
  }
  return tokens.map((token, tIdx) => {
    if (token.type === 'code') {
      return (
        <code key={tIdx} className="rounded bg-zinc-800/80 px-1.5 py-0.5 font-mono text-[11px] text-amber-500 font-semibold border border-zinc-700/50">
          {token.content}
        </code>
      );
    }
    let txt = token.content;
    const subParts = [];
    const boldRegex = /\*\*([^*]+)\*\*/g;
    let bMatch;
    let bLastIndex = 0;
    while ((bMatch = boldRegex.exec(txt)) !== null) {
      if (bMatch.index > bLastIndex) {
        subParts.push(parseItalic(txt.slice(bLastIndex, bMatch.index)));
      }
      subParts.push(<strong key={`b-${bMatch.index}`} className="font-semibold text-foreground">{bMatch[1]}</strong>);
      bLastIndex = boldRegex.lastIndex;
    }
    if (bLastIndex < txt.length) {
      subParts.push(parseItalic(txt.slice(bLastIndex)));
    }
    return subParts.length > 0 ? subParts : txt;
  });
}

function renderMarkdown(text) {
  if (!text) return null;
  const lines = text.split('\n');
  return lines.map((line, idx) => {
    if (line.startsWith('### ')) {
      return (
        <h3 key={idx} className="mt-5 mb-2 text-sm font-semibold text-foreground flex items-center gap-1.5">
          {parseInlineMarkdown(line.slice(4))}
        </h3>
      );
    }
    if (line.startsWith('## ')) {
      return (
        <h2 key={idx} className="mt-6 mb-3 text-base font-bold text-foreground">
          {parseInlineMarkdown(line.slice(3))}
        </h2>
      );
    }
    if (line.startsWith('# ')) {
      return (
        <h1 key={idx} className="mt-7 mb-4 text-lg font-extrabold text-foreground">
          {parseInlineMarkdown(line.slice(2))}
        </h1>
      );
    }
    if (line.trim().startsWith('- ')) {
      return (
        <ul key={idx} className="list-disc pl-5 my-1 text-muted-foreground">
          <li>{parseInlineMarkdown(line.trim().slice(2))}</li>
        </ul>
      );
    }
    if (line.startsWith('|')) {
      if (line.includes('---')) {
        return null;
      }
      const cells = line.split('|').slice(1, -1).map(c => c.trim());
      const isHeader = idx === 0 || (lines[idx - 1] && lines[idx - 1].trim() === '') || idx === 2; // naive check
      return (
        <div key={idx} className={`flex border-b border-border/40 py-2 text-xs ${isHeader ? 'font-semibold text-foreground bg-card/25' : 'text-muted-foreground'}`}>
          {cells.map((cell, cIdx) => (
            <div key={cIdx} className="flex-1 px-3">
              {parseInlineMarkdown(cell)}
            </div>
          ))}
        </div>
      );
    }
    if (line.trim() === '') {
      return <div key={idx} className="h-2" />;
    }
    return (
      <p key={idx} className="my-2 text-muted-foreground leading-relaxed">
        {parseInlineMarkdown(line)}
      </p>
    );
  });
}

// ─── Main EditorPage ──────────────────────────────────────────────────────────

function EditorPage() {
  const { id: slug } = useParams();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.user);
  const execState = useSelector(selectChallengeExecution);
  const c = useSelector(selectChallengeDetail(slug));
  const loading = useSelector(selectDetailLoading);
  const detailError = useSelector(selectDetailError);
  const runtimeEditor = c?.runtime_config?.editor;

  const availableLangs = (() => {
    if (runtimeEditor?.mode === "files") {
      return [runtimeEditor.executionLanguage || "multi"];
    }
    if (c?.domain === "APIs") {
      return ["js", "py", "go"];
    }
    if (c?.domain === "Backend") {
      return ["ts", "js", "py", "go", "java", "cpp", "rust"];
    }
    return ["ts", "js", "py", "go"];
  })();

  const getInitialState = () => {
    let initialLang = "ts";
    // If the runtime config specifies an execution language (e.g. "multi" for DevOps, "html" for Frontend),
    // use that first — it takes priority over starter_code key inference.
    if (runtimeEditor?.executionLanguage) {
      initialLang = runtimeEditor.executionLanguage;
    } else if (c?.starter_code) {
      const keys = Object.keys(c.starter_code);
      if (keys.includes("multi")) {
        initialLang = "multi";
      } else if (keys.includes("html")) {
        initialLang = "html";
      } else if (keys.includes("javascript") && !keys.includes("typescript")) {
        initialLang = "js";
      } else if (keys.length > 0) {
        const matched = keys.map(k => k === "typescript" ? "ts" : k === "javascript" ? "js" : k === "python" ? "py" : k === "go" ? "go" : k === "cpp" ? "cpp" : k === "rust" ? "rust" : k === "java" ? "java" : k).find(k => ["ts", "js", "py", "go", "java", "cpp", "rust"].includes(k));
        if (matched) initialLang = matched;
      }
    }
    return {
      lang: initialLang,
      code: getStarter(slug, initialLang, c)
    };
  };

  const [lang, setLang] = useState(() => getInitialState().lang);
  const [code, setCode] = useState(() => getInitialState().code);
  const [consoleResult, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState(() => typeof window !== "undefined" && window.innerWidth < 768 ? "description" : "testcase");
  const [customTestCases, setCustomTestCases] = useState([]);
  const [selectedTestCaseIdx, setSelectedTestCaseIdx] = useState(0);

  const isMultiFileDomain = c?.runtime_config?.editor?.mode === "files";

  // Multi-file states
  const [activeFile, setActiveFile] = useState("index.html");
  const [multiFiles, setMultiFiles] = useState({ "index.html": "" });
  const isLocalChange = useRef(false);

  // Resizing drag tracking
  const [isDraggingAny, setIsDraggingAny] = useState(false);
  const handleDragStart = useCallback(() => setIsDraggingAny(true), []);
  const handleDragEnd = useCallback(() => setIsDraggingAny(false), []);

  // DevOps terminal mount state
  const [terminalMounted, setTerminalMounted] = useState(false);

  // Vertical dragging state
  const [bottomHeight, setBottomHeight] = useState(280);
  const fitAddonInstance = useRef(null);

  const onDragVertical = useCallback((deltaY) => {
    setBottomHeight((prev) => {
      const next = prev - deltaY;
      return Math.max(150, Math.min(600, next));
    });
  }, []);

  useEffect(() => {
    if (fitAddonInstance.current) {
      try {
        fitAddonInstance.current.fit();
      } catch (e) {}
    }
  }, [bottomHeight]);

  // DevOps Terminal states & refs
  const [devopsSessionId, setDevopsSessionId] = useState(null);
  const terminalRef = useRef(null);
  const xtermInstance = useRef(null);
  const wsInstance = useRef(null);

  useEffect(() => {
    let activeSessionId = null;
    let isAborted = false;

    async function initSession() {
      if (c && c.domain === "DevOps") {
        try {
          const res = await API.post("/api/v1/devops/session/start", { slug });
          if (!isAborted) {
            const sid = res.data.session_id;
            setDevopsSessionId(sid);
            activeSessionId = sid;
          }
        } catch (err) {
          console.error("Failed to start DevOps session container:", err);
        }
      }
    }

    initSession();

    return () => {
      isAborted = true;
      if (activeSessionId) {
        API.post(`/api/v1/devops/session/${activeSessionId}/stop`).catch((e) =>
          console.error("Failed to stop DevOps session container on cleanup:", e)
        );
      }
      setDevopsSessionId(null);
    };
  }, [c?.id, slug]);

  // Background auto-sync of workspace files to the container sandbox
  useEffect(() => {
    if (!devopsSessionId || !isMultiFileDomain) return;

    const syncFiles = async () => {
      try {
        await API.post(`/api/v1/devops/session/${devopsSessionId}/sync`, { files: multiFiles });
      } catch (e) {
        console.error("Failed to sync files to container sandbox:", e);
      }
    };

    const timer = setTimeout(syncFiles, 500);
    return () => clearTimeout(timer);
  }, [devopsSessionId, multiFiles, isMultiFileDomain]);

  // Dynamic WebSocket interactive terminal connector
  useEffect(() => {
    if (activeTab !== "terminal" || !devopsSessionId || !terminalRef.current || !terminalMounted) {
      return;
    }

    // Initialize Xterm.js terminal instance
    const term = new Terminal({
      cursorBlink: true,
      fontSize: 12,
      fontFamily: 'Menlo, Monaco, "Courier New", monospace',
      theme: {
        background: "#0c0c0c",
        foreground: "#d4d4d8",
        cursor: "#3b82f6",
        selectionBackground: "rgba(59, 130, 246, 0.3)"
      }
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    fitAddonInstance.current = fitAddon;

    term.open(terminalRef.current);
    
    // Slight timeout to ensure layout sizing completes before fitting
    setTimeout(() => {
      try {
        fitAddon.fit();
      } catch (e) {}
    }, 50);

    xtermInstance.current = term;

    // Connect WebSocket
    let wsHost;
    let wsProtocol;

    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      wsHost = "localhost:8000";
      wsProtocol = "ws:";
    } else {
      wsHost = "interleet-backend.sharexpress.in";
      wsProtocol = "wss:";
    }

    const wsUrl = `${wsProtocol}//${wsHost}/api/v1/devops/session/${devopsSessionId}/ws`;
    const ws = new WebSocket(wsUrl);
    wsInstance.current = ws;

    ws.onopen = () => {
      const osName = c?.runtime_config?.os || "Linux";
      term.write(`\r\n*** Terminal connection established. Welcome to Interleet Sandbox (${osName})! ***\r\n\r\n`);
    };

    ws.onmessage = (event) => {
      term.write(event.data);
    };

    ws.onclose = () => {
      term.write("\r\n*** Terminal connection closed. ***\r\n");
    };

    ws.onerror = (err) => {
      term.write(`\r\n*** Connection error: ${err.message || "Unknown error"} ***\r\n`);
    };

    // Forward terminal input keystrokes directly to Docker stdin socket
    term.onData((data) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });

    const handleResize = () => {
      try {
        fitAddon.fit();
      } catch (e) {}
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      term.dispose();
      ws.close();
      xtermInstance.current = null;
      wsInstance.current = null;
    };
  }, [activeTab, devopsSessionId, terminalMounted]);

  useEffect(() => {
    if (isLocalChange.current) {
      isLocalChange.current = false;
      return;
    }
    
    if (isMultiFileDomain) {
      try {
        const parsed = JSON.parse(code);
        if (parsed && typeof parsed === "object") {
          setMultiFiles(parsed);
          const keys = Object.keys(parsed);
          if (!keys.includes(activeFile) && keys.length > 0) {
            setActiveFile(keys[0]);
          }
          return;
        }
      } catch (e) {}

      if (runtimeEditor?.executionLanguage === "html") {
        // Fallback for legacy plain text starter code
        const fallback = {
          "index.html": `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <title>Interleet Preview</title>\n  <link rel="stylesheet" href="index.css">\n</head>\n<body>\n  <div id="app">\n    <!-- Write your HTML structure here -->\n  </div>\n  <script src="index.js"></script>\n</body>\n</html>`,
          "index.css": `body {\n  font-family: system-ui, -apple-system, sans-serif;\n  color: #fafafa;\n  background: #09090b;\n  margin: 0;\n  padding: 24px;\n}\n#app {\n  max-width: 600px;\n  margin: 0 auto;\n  padding: 20px;\n  border: 1px solid #27272a;\n  border-radius: 8px;\n  background: #18181b;\n}`,
          "index.js": code || `console.log("DOM loaded successfully!");\n`
        };
        setMultiFiles(fallback);
        isLocalChange.current = true;
        setCode(JSON.stringify(fallback));
      } else {
        const entryFile = runtimeEditor?.entryFile || "main.txt";
        const fallback = { [entryFile]: code || "" };
        setMultiFiles(fallback);
        isLocalChange.current = true;
        setCode(JSON.stringify(fallback));
      }
    }
  }, [code, isMultiFileDomain, runtimeEditor?.entryFile, runtimeEditor?.executionLanguage]);

  useEffect(() => {
    if (c && c.test_cases) {
      setCustomTestCases(
        c.test_cases.filter(t => !t.hidden).map((t, idx) => ({
          id: t.id || `tc-${idx}`,
          stdin: t.stdin || "",
          expected_output: t.expected_output || "",
          name: t.name || `Case ${idx + 1}`,
          isCustom: false,
          ...(t.verification_script ? { verification_script: t.verification_script } : {}),
          ...(t.files ? { files: t.files } : {}),
        }))
      );
      setSelectedTestCaseIdx(0);
    }
  }, [c]);

  // Previous submission state
  const [prevSubmission, setPrevSubmission] = useState(null); // { found, is_accepted, code, language, score, verdict, created_at, total_attempts }
  const [prevSubLoading, setPrevSubLoading] = useState(true);
  const [usingPrevCode, setUsingPrevCode] = useState(false);

  // Derived busy flags
  const isRunning = execState.runStatus === 'loading';
  const isSubmitting = execState.submitStatus === 'loading';

  const containerRef = useRef(null);
  const [leftW, setLeftW] = useState(340);
  const [rightW, setRightW] = useState(420);
  const MIN_COL = 220;

  const getW = () => containerRef.current?.offsetWidth ?? window.innerWidth;

  const onDragLeft = useCallback((delta) => {
    setLeftW((w) => Math.max(MIN_COL, Math.min(w + delta, getW() - MIN_COL * 2)));
  }, []);

  const onDragRight = useCallback((delta) => {
    setRightW((w) => Math.max(MIN_COL, Math.min(w - delta, getW() - MIN_COL * 2)));
  }, []);

  useEffect(() => {
    const initialState = getInitialState();
    setLang(initialState.lang);
    setCode(initialState.code);
    setResult(null);
    setPrevSubmission(null);
    setUsingPrevCode(false);
    setMultiFiles({});
    setActiveFile("");
    dispatch(resetExecution());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  useEffect(() => {
    if (c && !usingPrevCode) {
      const keys = Object.keys(c.starter_code || {});

      // For multi-file domains (DevOps, Frontend filesystem), skip the lang selection logic
      if (isMultiFileDomain || keys.includes("multi") || keys.includes("html")) {
        const multiLang = runtimeEditor?.executionLanguage || (keys.includes("multi") ? "multi" : keys.includes("html") ? "html" : lang);
        setLang(multiLang);
        setCode(getStarter(slug, multiLang, c));
        return;
      }

      const shortKeys = keys.map(k => k === "typescript" ? "ts" : k === "javascript" ? "js" : k === "python" ? "py" : k === "go" ? "go" : k === "cpp" ? "cpp" : k === "rust" ? "rust" : k === "java" ? "java" : k).filter(k => ["ts", "js", "py", "go", "java", "cpp", "rust"].includes(k));
      
      const allowedLangs = c.domain === "Frontend"
        ? ["ts", "js"].filter(k => shortKeys.includes(k))
        : (c.domain === "Backend" ? ["ts", "js", "py", "go", "java", "cpp", "rust"] : ["ts", "js", "py", "go"]);

      let nextLang = lang;
      
      // If current lang is not allowed, or current lang has no starter code but others in the DB do:
      const currentHasStarter = keys.includes(lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang === "cpp" ? "cpp" : lang === "rust" ? "rust" : lang === "java" ? "java" : lang);
      
      if (!allowedLangs.includes(lang) || (!currentHasStarter && shortKeys.length > 0)) {
        const dbLang = shortKeys.find(k => allowedLangs.includes(k));
        nextLang = dbLang || allowedLangs[0];
        setLang(nextLang);
      }
      setCode(getStarter(slug, nextLang, c));
    }
  }, [c, slug, usingPrevCode]);

  useEffect(() => {
    dispatch(FetchChallengeBySlug(slug));
  }, [dispatch, slug]);

  // Fetch the user's previous submission for this challenge
  useEffect(() => {
    let cancelled = false;
    const fetchPrev = async () => {
      setPrevSubLoading(true);
      try {
        const res = await API.get(`/api/v1/my-submissions/${slug}`);
        if (!cancelled && res.data?.found) {
          setPrevSubmission(res.data);
          // Auto-load previous code
          const shortLang = BACKEND_LANG_TO_SHORT[res.data.language] ?? "ts";
          setLang(shortLang);
          setCode(res.data.code);
          setUsingPrevCode(true);
        }
      } catch (_) {
        // Not authenticated or no submission — silently ignore
      } finally {
        if (!cancelled) setPrevSubLoading(false);
      }
    };
    if (user) fetchPrev();
    else setPrevSubLoading(false);
    return () => { cancelled = true; };
  }, [slug, user]);

  const handleLangChange = useCallback(
    (l) => {
      setLang(l);
      setCode(getStarter(slug, l, c));
      setResult(null);
    },
    [slug, c],
  );

  const handleCodeChange = useCallback((newValue) => {
    if (isMultiFileDomain) {
      setMultiFiles((prev) => {
        const next = { ...prev, [activeFile]: newValue };
        isLocalChange.current = true;
        setCode(JSON.stringify(next));
        return next;
      });
    } else {
      setCode(newValue);
    }
  }, [isMultiFileDomain, activeFile]);

  // Run — executes custom test cases or visible sample test cases
  const handleRun = useCallback(() => {
    dispatch(resetExecution());
    setActiveTab("result");
    const executionLang = runtimeEditor?.executionLanguage || lang;
    dispatch(runCode({ code, language: executionLang, testCases: customTestCases, executionMode: c?.execution_mode || "cli", runtime: c?.runtime }));
  }, [code, lang, customTestCases, dispatch, runtimeEditor?.executionLanguage, c?.execution_mode, c?.runtime]);

  // Submit — runs against all test cases (including hidden) via backend DB
  const handleSubmit = useCallback(() => {
    dispatch(resetExecution());
    setActiveTab("result");
    const executionLang = runtimeEditor?.executionLanguage || lang;
    dispatch(submitCode({ code, language: executionLang, slug, userId: user?.user_id, executionMode: c?.execution_mode || "cli", runtime: c?.runtime }));
  }, [code, lang, slug, dispatch, user, runtimeEditor?.executionLanguage, c?.execution_mode, c?.runtime]);

  // Reset editor to default starter code, dismissing previous submission
  const handleResetToStarter = useCallback(() => {
    const starterCode = getStarter(slug, lang, c);
    setCode(starterCode);
    setUsingPrevCode(false);
    setResult(null);
  }, [slug, lang, c]);

  if (loading && !c)
    return (
      <AppShell>
        {/* Mock workspace toolbar */}
        <div className="flex h-12 items-center justify-between border-b border-border bg-card/40 px-4 py-2 animate-pulse">
          <div className="flex items-center gap-3 w-1/3">
            <div className="h-6 w-8 rounded bg-zinc-800/40" />
            <div className="space-y-1.5 w-full">
              <div className="h-3.5 w-24 rounded bg-zinc-800/40" />
              <div className="h-2 w-32 rounded bg-zinc-800/20" />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-7 w-24 rounded bg-zinc-800/40" />
            <div className="h-7 w-16 rounded bg-zinc-800/40" />
            <div className="h-7 w-16 rounded bg-zinc-800/40" />
          </div>
        </div>
        {/* Mock panel layout */}
        <div className="flex h-[calc(100vh-56px-49px)] overflow-hidden animate-pulse">
          {/* Left panel skeleton */}
          <div className="w-80 border-r border-border p-4 space-y-4 shrink-0 bg-card/10">
            <div className="h-4 w-1/3 rounded bg-zinc-800/40" />
            <div className="h-3 w-2/3 rounded bg-zinc-800/30" />
            <div className="space-y-2 pt-4">
              <div className="h-3 w-full rounded bg-zinc-800/20" />
              <div className="h-3 w-full rounded bg-zinc-800/20" />
              <div className="h-3 w-5/6 rounded bg-zinc-800/20" />
            </div>
          </div>
          {/* Center sizer mock */}
          <div className="w-1 border-r border-border shrink-0" />
          {/* Monaco mock code workspace */}
          <div className="flex-1 bg-zinc-950 p-6 space-y-3">
            <div className="h-3.5 w-48 rounded bg-zinc-800/30" />
            <div className="h-3 w-64 rounded bg-zinc-800/20 ml-4" />
            <div className="h-3 w-32 rounded bg-zinc-800/20 ml-4" />
            <div className="h-3 w-80 rounded bg-zinc-800/20 ml-8" />
            <div className="h-3 w-56 rounded bg-zinc-800/20 ml-12" />
            <div className="h-3 w-40 rounded bg-zinc-800/20 ml-8" />
          </div>
        </div>
      </AppShell>
    );

  if ((detailError || !c) && !loading)
    return (
      <AppShell>
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-center">
            <p className="text-sm text-destructive">{detailError ?? "Challenge not found"}</p>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/app/challenges">
                <ArrowLeft className="mr-1.5 h-4 w-4" /> Back to challenges
              </Link>
            </Button>
          </div>
        </div>
      </AppShell>
    );

  const fileName = LANG_FILE[lang] ?? "solution.ts";

  return (
    <AppShell>
      {/* Toolbar */}
      <div className="flex flex-col gap-3 border-b border-border bg-card/40 px-4 py-2.5 sm:flex-row sm:items-center sm:justify-between md:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="h-8 w-8">
            <Link to={`/app/challenges/${c.slug}`}>
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
          <div className="min-w-0">
            <div className="flex items-center">
              <p className="truncate text-sm font-semibold">{c.title}</p>
              <RuntimeBadge runtime={c?.runtime_config} />
            </div>
            <p className="truncate text-xs text-muted-foreground mt-0.5">
              {c.domain} · {c.difficulty} · {c.minutes}m
            </p>
          </div>
        </div>
        <div className="flex items-center justify-between sm:justify-end gap-2 w-full sm:w-auto">
          {(!isMultiFileDomain || c?.domain === "APIs") && (
            <Select value={lang} onValueChange={handleLangChange}>
            <SelectTrigger className="h-8 w-[130px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {availableLangs.map((v) => {
                let label = LANG_LABEL[v];
                if (c?.domain === "APIs") {
                  if (v === "js") label = "Express.js (Node.js)";
                  if (v === "py") label = "FastAPI (Python)";
                  if (v === "go") label = "Gin (Go)";
                }
                return (
                  <SelectItem key={v} value={v}>
                    {label}
                  </SelectItem>
                );
              })}
            </SelectContent>
          </Select>
          )}
          <Button variant="outline" size="sm" onClick={handleRun} disabled={c?.locked || isRunning || isSubmitting} className="flex-1 sm:flex-none">
            {isRunning ? (
              <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
            ) : (
              <Play className="mr-1.5 h-3.5 w-3.5" />
            )}
            Run
          </Button>
          <Button size="sm" onClick={handleSubmit} disabled={c?.locked || isRunning || isSubmitting} className="flex-1 sm:flex-none">
            {isSubmitting ? (
              <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
            ) : (
              <Send className="mr-1.5 h-3.5 w-3.5" />
            )}
            Submit
          </Button>
          <Drawer>
            <DrawerTrigger asChild>
              <Button
                variant="outline"
                size="icon"
                className="xl:hidden h-8 w-8"
                aria-label="Open browser preview"
              >
                <Globe className="h-4 w-4" />
              </Button>
            </DrawerTrigger>
            <DrawerContent className="p-0">
              <div className="flex h-[85vh] flex-col overflow-hidden">
                <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} code={code} execState={execState} isMultiFileDomain={isMultiFileDomain} />
              </div>
            </DrawerContent>
          </Drawer>
        </div>
      </div>

      {/* ── Previous Submission Acknowledgement Banner ───────────────────── */}
      {usingPrevCode && prevSubmission && !c?.locked && (
        <div
          className={`flex items-center gap-3 px-4 py-2.5 text-sm border-b ${
            prevSubmission.is_accepted
              ? "bg-emerald-950/40 border-emerald-800/40 text-emerald-300"
              : "bg-amber-950/40 border-amber-800/40 text-amber-300"
          }`}
        >
          {prevSubmission.is_accepted ? (
            <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
          ) : (
            <AlertCircle className="h-4 w-4 shrink-0 text-amber-400" />
          )}
          <div className="flex-1 min-w-0">
            <span className="font-semibold">
              {prevSubmission.is_accepted
                ? "You've already solved this challenge!"
                : "Previously attempted"}
            </span>
            <span className="ml-2 text-xs opacity-70">
              {prevSubmission.is_accepted
                ? "Your accepted solution is loaded below. You can re-submit to improve."
                : `Your last submission is loaded (${prevSubmission.total_attempts} attempt${prevSubmission.total_attempts !== 1 ? "s" : ""} · not yet accepted). Keep improving!`}
            </span>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            {prevSubmission.score > 0 && (
              <Badge
                variant="outline"
                className={`font-mono text-[10px] ${
                  prevSubmission.is_accepted
                    ? "border-emerald-700 text-emerald-300"
                    : "border-amber-700 text-amber-300"
                }`}
              >
                {prevSubmission.score}/100
              </Badge>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleResetToStarter}
              className="h-7 px-2 text-xs text-muted-foreground hover:text-foreground gap-1.5"
            >
              <RotateCcw className="h-3 w-3" />
              Reset to starter
            </Button>
          </div>
        </div>
      )}

      {/* Workspace Area: Locked check */}

      {c?.locked ? (
        <div className="flex flex-col items-center justify-center h-[calc(100vh-56px-49px)] bg-zinc-950 px-4 text-center">
          <div className="max-w-md w-full bg-zinc-900/40 border border-zinc-800/80 rounded-2xl p-8 space-y-6 shadow-xl relative overflow-hidden">
            {/* Ambient orange glow */}
            <div className="absolute -top-12 -left-12 w-24 h-24 bg-[#FF6500]/5 rounded-full blur-2xl pointer-events-none" />
            <div className="absolute -bottom-12 -right-12 w-24 h-24 bg-[#FF6500]/5 rounded-full blur-2xl pointer-events-none" />

            <div className="flex flex-col items-center space-y-3">
              <div className="flex items-center justify-center w-14 h-14 rounded-full bg-[#FF6500]/10 border border-[#FF6500]/30 text-[#FF6500]">
                <Lock className="w-6 h-6 animate-pulse" />
              </div>
              <h2 className="text-xl font-bold tracking-tight text-white">
                Premium Challenge Locked
              </h2>
              <p className="text-sm text-zinc-400 leading-relaxed">
                This challenge requires an active Pro Elite subscription. Unlock the complete catalog, interactive test suites, and unlimited AI mock interviews today.
              </p>
            </div>

            <div className="border-t border-b border-zinc-800/60 py-4 my-2 text-left space-y-2.5">
              <div className="flex items-center gap-2 text-xs text-zinc-300">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span>Full access to all premium/expert challenges</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-zinc-300">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span>Interactive editor, test cases, and solutions</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-zinc-300">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span>Unlimited tailored AI interview feedback reports</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <Button
                variant="outline"
                className="flex-1 border-zinc-800 hover:bg-zinc-850 hover:text-white text-zinc-400"
                asChild
              >
                <Link to="/app/challenges">
                  <ArrowLeft className="w-4 h-4 mr-1.5" /> Challenges
                </Link>
              </Button>
              <UpgradeModal
                trigger={
                  <Button className="flex-1 bg-gradient-to-r from-[#FF6500] to-orange-600 hover:from-[#E05900] hover:to-orange-700 text-white font-bold border-none shadow-lg shadow-orange-500/25 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] cursor-pointer">
                    <Sparkles className="w-4 h-4 mr-1.5 fill-white text-white animate-pulse" />
                    Unlock Pro
                  </Button>
                }
              />
            </div>
          </div>
        </div>
      ) : (
        <div ref={containerRef} className="flex h-[calc(100vh-56px-49px)] overflow-hidden">
          {/* LEFT: problem panel */}
          <aside
            className="hidden h-full flex-col overflow-hidden border-r border-border bg-card md:flex"
            style={{ width: leftW, minWidth: MIN_COL, flexShrink: 0 }}
          >
            <div className="border-b border-border px-4 py-3">
              <div className="flex items-center gap-2">
                <BookOpen className="h-4 w-4 text-primary" />
                <p className="text-sm font-semibold">Problem</p>
              </div>
              <p className="mt-1 truncate text-base font-semibold">{c.title}</p>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <DifficultyPill d={c.difficulty} />
                <DomainTag d={c.domain} />
                <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                  <Clock className="h-3 w-3" /> {c.minutes}m
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                  <Sparkles className="h-3 w-3" /> {c.xp} XP
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                  <Users className="h-3 w-3" /> {c.completion}%
                </span>
              </div>
            </div>
            <div className="flex-1 min-h-0 overflow-y-auto px-4 py-4 text-sm leading-relaxed text-foreground/90">
              <p>{c.summary}</p>
              
              {c.function_signature && (
                <div className="mt-4 space-y-1.5">
                  <p className="text-[10px] uppercase font-mono tracking-wider text-muted-foreground">Function Signature</p>
                  <pre className="bg-zinc-950 p-2.5 rounded border border-border font-mono text-[11px] text-emerald-400 overflow-x-auto select-all">
                    {c.function_signature}
                  </pre>
                </div>
              )}

              {c.description && (
                <div className="mt-4 space-y-1 text-muted-foreground">
                  {renderMarkdown(c.description)}
                </div>
              )}

              {!isMultiFileDomain && <EnvironmentInfo domain={c.domain} lang={lang} />}
              {c.test_cases?.filter((t) => !t.hidden).length > 0 && (
                <>
                  <h3 className="mt-5 text-sm font-semibold">Examples</h3>
                  <div className="mt-2 space-y-2">
                    {c.test_cases
                      .filter((t) => !t.hidden)
                      .map((t) => (
                        <div
                          key={t.id}
                          className="rounded-md border border-border bg-background/60 p-3"
                        >
                          <p className="mb-1.5 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                            {t.name}
                          </p>
                          {t.stdin && (
                            <div className="mb-1">
                              <span className="text-[10px] text-muted-foreground">Input: </span>
                              <code className="font-mono text-[11px] text-foreground/85">
                                {t.stdin.trim()}
                              </code>
                            </div>
                          )}
                          {t.expected_output && (
                            <div>
                              <span className="text-[10px] text-muted-foreground">Output: </span>
                              <code className="font-mono text-[11px] text-foreground/85">
                                {t.expected_output.trim()}
                              </code>
                            </div>
                          )}
                        </div>
                      ))}
                  </div>
                </>
              )}
              {c.hints?.length > 0 && (
                <>
                  <h3 className="mt-5 text-sm font-semibold">Hints</h3>
                  <ol className="mt-2 list-inside list-decimal space-y-1 text-muted-foreground">
                    {c.hints.map((h, i) => (
                      <li key={i}>{h}</li>
                    ))}
                  </ol>
                </>
              )}
              {c.tags?.length > 0 && (
                <>
                  <h3 className="mt-5 text-sm font-semibold">Tags</h3>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {c.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded border border-border bg-background/60 px-2 py-0.5 font-mono text-[10px] text-muted-foreground"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </>
              )}
              {c?.runtime_config && (
                <EnvironmentCard runtime={c.runtime_config} />
              )}
            </div>
          </aside>

          {/* DRAG: left | center */}
          <div className="hidden md:block h-full flex-shrink-0">
            <DragHandle onDelta={onDragLeft} onDragStart={handleDragStart} onDragEnd={handleDragEnd} />
          </div>

          {/* CENTER: editor + bottom tabs */}
          <div className="flex min-w-0 flex-1 flex-col">
            {/* File tab bar */}
            <div className="flex items-center gap-1 border-b border-border bg-muted/30 px-2 pt-2 overflow-x-auto">
              {isMultiFileDomain ? (
                <>
                  {Object.keys(multiFiles).map((f) => (
                    <button
                      key={f}
                      onClick={() => setActiveFile(f)}
                      className={`flex items-center gap-2 rounded px-3 py-1 font-mono text-xs transition-colors ${
                        activeFile === f
                          ? "bg-primary/10 text-primary border border-primary/20"
                          : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                      }`}
                    >
                      <FileCode2 className="h-3 w-3" /> {f}
                    </button>
                  ))}
                </>
              ) : (
                <div className="flex items-center gap-2 rounded-t border-b-2 border-primary bg-card px-3 py-1 font-mono text-xs text-foreground">
                  <FileCode2 className="h-3 w-3" /> {fileName}
                </div>
              )}
            </div>

            {/* Monaco editor */}
            <div className="min-h-0 flex-1 overflow-hidden bg-[#1E1E1E]">
              <MonacoEditor
                value={(isMultiFileDomain ? multiFiles[activeFile] : code) || ""}
                language={
                  isMultiFileDomain
                    ? (activeFile || "").endsWith(".html") ? "html"
                      : (activeFile || "").endsWith(".css") ? "css"
                      : (activeFile || "").endsWith(".js") ? "javascript"
                      : (activeFile || "").endsWith(".ts") ? "typescript"
                      : (activeFile || "").endsWith(".yml") || (activeFile || "").endsWith(".yaml") ? "yaml"
                      : (activeFile || "").endsWith(".sh") || (activeFile || "").endsWith(".conf") ? "shell"
                      : activeFile === "Dockerfile" ? "dockerfile"
                      : "plaintext"
                    : lang
                }
                onChange={handleCodeChange}
              />
            </div>

            {/* Vertical drag handle */}
            <VerticalDragHandle onDelta={onDragVertical} onDragStart={handleDragStart} onDragEnd={handleDragEnd} />

            {/* Bottom panel */}
            <div className="border-t border-border bg-background/60 flex-shrink-0" style={{ height: `${bottomHeight}px` }}>
              <Tabs value={activeTab} onValueChange={setActiveTab} className="flex flex-col h-full">
                <div className="flex items-center justify-between border-b border-border px-3 py-1.5">
                  <TabsList className="h-8 bg-transparent p-0 flex flex-wrap gap-1">
                    <TabsTrigger value="description" className="h-7 px-3 text-xs md:hidden">
                      Description
                    </TabsTrigger>
                    <TabsTrigger value="testcase" className="h-7 px-3 text-xs">
                      Testcase
                    </TabsTrigger>
                    <TabsTrigger value="result" className="h-7 px-3 text-xs">
                      Result
                    </TabsTrigger>
                    <TabsTrigger value="console" className="h-7 px-3 text-xs">
                      <TerminalIcon className="mr-1 h-3 w-3" /> Console
                      {consoleResult && (
                        <span
                          className={`ml-1.5 inline-flex h-4 min-w-4 items-center justify-center rounded-full px-1 text-[9px] font-semibold ${consoleResult.errors.length > 0
                              ? "bg-destructive/20 text-destructive"
                              : "bg-success/20 text-success"
                            }`}
                        >
                          {consoleResult.errors.length > 0
                            ? consoleResult.errors.length
                            : consoleResult.logs.length}
                        </span>
                      )}
                    </TabsTrigger>
                    {c?.domain === "DevOps" && (
                      <TabsTrigger value="terminal" className="h-7 px-3 text-xs">
                        <TerminalIcon className="mr-1 h-3 w-3" /> Terminal
                      </TabsTrigger>
                    )}
                  </TabsList>
                  <div className="flex items-center gap-2">
                    {activeTab === "console" && consoleResult && (
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-muted-foreground hover:text-foreground"
                        onClick={() => setResult(null)}
                        title="Clear console"
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    )}
                    <Badge variant="outline" className="font-mono text-[10px]">
                      {isMultiFileDomain ? c?.runtime_config?.name : LANG_BADGE[lang]}
                    </Badge>
                  </div>
                </div>

                {/* Description tab for mobile */}
                <TabsContent value="description" className="m-0 overflow-auto p-4 space-y-3 md:hidden" style={{ height: "calc(100% - 36px)" }}>
                  <div className="space-y-3 font-sans text-xs">
                    <h3 className="text-sm font-semibold text-white">{c.title}</h3>
                    <div className="flex flex-wrap items-center gap-2">
                      <DifficultyPill d={c.difficulty} />
                      <DomainTag d={c.domain} />
                      <span className="inline-flex items-center gap-1 text-[10px] text-muted-foreground">
                        <Clock className="h-3.5 w-3.5" /> {c.minutes}m
                      </span>
                      <span className="inline-flex items-center gap-1 text-[10px] text-muted-foreground">
                        <Sparkles className="h-3.5 w-3.5" /> {c.xp} XP
                      </span>
                    </div>
                    <div className="mt-2 text-zinc-300 leading-relaxed space-y-3">
                      <p>{c.summary}</p>

                      {c.function_signature && (
                        <div className="mt-4 space-y-1.5">
                          <p className="text-[9px] uppercase font-mono tracking-wider text-muted-foreground">Function Signature</p>
                          <pre className="bg-zinc-950 p-2 rounded border border-border font-mono text-[10px] text-emerald-400 overflow-x-auto select-all">
                            {c.function_signature}
                          </pre>
                        </div>
                      )}

                      {c.description && (
                        <div className="mt-4 space-y-1 text-muted-foreground prose prose-invert max-w-none text-xs">
                          {renderMarkdown(c.description)}
                        </div>
                      )}

                      {!isMultiFileDomain && <EnvironmentInfo domain={c.domain} lang={lang} />}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="testcase" className="m-0 overflow-auto p-4 space-y-4" style={{ height: "calc(100% - 36px)" }}>
                  {/* Case buttons */}
                  <div className="flex flex-wrap items-center gap-1.5 border-b border-zinc-800 pb-2">
                    {customTestCases.map((tc, idx) => (
                      <button
                        key={tc.id}
                        type="button"
                        onClick={() => setSelectedTestCaseIdx(idx)}
                        className={`rounded px-2.5 py-1 text-xs font-semibold border transition-all flex items-center gap-1.5 ${
                          selectedTestCaseIdx === idx
                            ? "bg-zinc-800 border-zinc-700 text-white"
                            : "border-transparent text-muted-foreground hover:text-white"
                        }`}
                      >
                        <span>{tc.name}</span>
                        {tc.isCustom && (
                          <X
                            className="h-3 w-3 text-muted-foreground hover:text-destructive shrink-0 cursor-pointer"
                            onClick={(e) => {
                              e.stopPropagation();
                              const newCases = customTestCases.filter((_, i) => i !== idx);
                              setCustomTestCases(newCases);
                              setSelectedTestCaseIdx(Math.max(0, idx - 1));
                            }}
                          />
                        )}
                      </button>
                    ))}
                    {customTestCases.length < 8 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 px-2 text-muted-foreground hover:text-white text-xs gap-1 border border-dashed border-zinc-800"
                        onClick={() => {
                          const nextIdx = customTestCases.length + 1;
                          const newCase = {
                            id: `custom-tc-${Date.now()}`,
                            stdin: "",
                            expected_output: "",
                            name: `Case ${nextIdx} (Custom)`,
                            isCustom: true
                          };
                          setCustomTestCases([...customTestCases, newCase]);
                          setSelectedTestCaseIdx(customTestCases.length);
                        }}
                      >
                        <Plus className="h-3 w-3 animate-none shrink-0" />
                        <span>Add Case</span>
                      </Button>
                    )}
                  </div>

                  {/* Input editing area */}
                  {customTestCases[selectedTestCaseIdx] ? (
                    <div className="space-y-3 font-sans text-xs">
                      <div className="space-y-1">
                        <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider block">Input (stdin)</label>
                        <textarea
                          value={customTestCases[selectedTestCaseIdx].stdin}
                          onChange={(e) => {
                            const newCases = [...customTestCases];
                            newCases[selectedTestCaseIdx].stdin = e.target.value;
                            setCustomTestCases(newCases);
                          }}
                          placeholder="Provide lines of inputs..."
                          rows={4}
                          className="w-full rounded-md border border-zinc-850 bg-zinc-950/40 p-2.5 font-mono text-[11px] text-white focus:outline-none focus:border-primary resize-y"
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider block">Expected Output (Optional)</label>
                        <textarea
                          value={customTestCases[selectedTestCaseIdx].expected_output}
                          onChange={(e) => {
                            const newCases = [...customTestCases];
                            newCases[selectedTestCaseIdx].expected_output = e.target.value;
                            setCustomTestCases(newCases);
                          }}
                          placeholder="Provide target output comparison..."
                          rows={2}
                          className="w-full rounded-md border border-zinc-850 bg-zinc-950/40 p-2.5 font-mono text-[11px] text-white focus:outline-none focus:border-primary resize-y"
                        />
                      </div>
                      <div className="flex gap-2 border-t border-border/60 pt-3 mt-3">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={handleRun}
                          disabled={isRunning || isSubmitting}
                          className="h-7 px-3 text-[10px] bg-background/50 border-border text-zinc-300 hover:text-white"
                        >
                          <Play className="mr-1 h-3 w-3" /> Run Custom Cases
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs text-muted-foreground">Add a test case to edit inputs.</p>
                  )}
                </TabsContent>

                {/* Test Result tab: shows Run OR Submit results */}
                <TabsContent value="result" className="m-0 overflow-auto p-3 space-y-3" style={{ height: "calc(100% - 36px)" }}>
                  {/* Run result */}
                  {(execState.runStatus !== 'idle' || execState.runResult) && (
                    <ExecutionResult
                      mode="run"
                      status={execState.runStatus}
                      result={execState.runResult}
                      error={execState.runError}
                    />
                  )}
                  {/* Submit result */}
                  {(execState.submitStatus !== 'idle' || execState.submitResult) && (
                    <ExecutionResult
                      mode="submit"
                      status={execState.submitStatus}
                      result={execState.submitResult}
                      error={execState.submitError}
                    />
                  )}
                  {/* Idle placeholder */}
                  {execState.runStatus === 'idle' && execState.submitStatus === 'idle' && (
                    <p className="text-xs text-muted-foreground italic">
                      Click <strong>Run</strong> to test against sample cases, or <strong>Submit</strong> to judge all test cases.
                    </p>
                  )}
                </TabsContent>

                {/* Console tab: legacy local output (JS/TS eval) */}
                <TabsContent value="console" className="m-0 overflow-auto p-3" style={{ height: "calc(100% - 36px)" }}>
                  <ConsoleOutput result={consoleResult} isRunning={false} />
                </TabsContent>

                {/* DevOps Terminal tab */}
                {c?.domain === "DevOps" && (
                  <TabsContent value="terminal" className="m-0 bg-[#0c0c0c] border-t border-zinc-800 overflow-hidden" style={{ height: "calc(100% - 36px)" }}>
                    <div
                      ref={(el) => {
                        terminalRef.current = el;
                        if (el) {
                          setTerminalMounted(true);
                        } else {
                          setTerminalMounted(false);
                        }
                      }}
                      className="w-full h-full p-2 select-text"
                    />
                  </TabsContent>
                )}

              </Tabs>
            </div>
          </div>

          {/* DRAG: center | right */}
          <div className="hidden xl:block h-full flex-shrink-0">
            <DragHandle onDelta={onDragRight} onDragStart={handleDragStart} onDragEnd={handleDragEnd} />
          </div>

          {/* RIGHT: browser preview */}
          <aside
            className={`hidden h-full flex-col overflow-hidden bg-card xl:flex ${isDraggingAny ? "pointer-events-none" : ""}`}
            style={{ width: rightW, minWidth: MIN_COL, flexShrink: 0 }}
          >
            <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} code={code} execState={execState} isMultiFileDomain={isMultiFileDomain} />
          </aside>
        </div>
      )}
    </AppShell>
  );
}

export default EditorPage;
