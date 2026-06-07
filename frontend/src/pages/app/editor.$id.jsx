import { useEffect, useRef, useState, useCallback } from "react";
import { Link, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
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
import {
  Play,
  Send,
  FileCode2,
  Terminal as TerminalIcon,
  Check,
  X,
  ArrowLeft,
  Clock,
  Sparkles,
  Users,
  BookOpen,
  Globe,
  RotateCw,
  Lock,
  Loader2,
  Trash2,
} from "lucide-react";

// ─── Monaco CDN loader ────────────────────────────────────────────────────────

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

// ─── Language config ──────────────────────────────────────────────────────────

const LANG_TO_MONACO = { ts: "typescript", js: "javascript", py: "python", go: "go" };
const LANG_LABEL = { ts: "TypeScript", js: "JavaScript", py: "Python", go: "Go" };
const LANG_BADGE = { ts: "node v20.10", js: "node v20.10", py: "python 3.12", go: "go 1.22" };
const LANG_FILE = { ts: "solution.ts", js: "solution.js", py: "solution.py", go: "main.go" };

// ─── Starter code ─────────────────────────────────────────────────────────────

const STARTERS = {
  "build-a-rate-limiter": {
    ts: `// rate-limiter.ts
export class TokenBucket {
  private tokens: number;
  private last = Date.now();

  constructor(
    private readonly capacity: number,
    private readonly refillPerSec: number,
  ) {
    this.tokens = capacity;
  }

  allow(): boolean {
    const now = Date.now();
    const elapsed = (now - this.last) / 1000;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsed * this.refillPerSec,
    );
    this.last = now;
    if (this.tokens >= 1) {
      this.tokens -= 1;
      return true;
    }
    return false;
  }
}

const bucket = new TokenBucket(3, 1);
console.log({ call: 1, allowed: bucket.allow() });
console.log({ call: 2, allowed: bucket.allow() });
console.log({ call: 3, allowed: bucket.allow() });
console.log({ call: 4, allowed: bucket.allow() });
`,
    js: `// rate-limiter.js
class TokenBucket {
  #tokens;
  #last = Date.now();

  constructor(capacity, refillPerSec) {
    this.capacity = capacity;
    this.refillPerSec = refillPerSec;
    this.#tokens = capacity;
  }

  allow() {
    const now = Date.now();
    const elapsed = (now - this.#last) / 1000;
    this.#tokens = Math.min(this.capacity, this.#tokens + elapsed * this.refillPerSec);
    this.#last = now;
    if (this.#tokens >= 1) { this.#tokens -= 1; return true; }
    return false;
  }
}

const bucket = new TokenBucket(3, 1);
console.log({ call: 1, allowed: bucket.allow() });
console.log({ call: 2, allowed: bucket.allow() });
console.log({ call: 3, allowed: bucket.allow() });
console.log({ call: 4, allowed: bucket.allow() });
`,
    py: `# rate_limiter.py
import time

class TokenBucket:
    def __init__(self, capacity: int, refill_per_sec: float):
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self._tokens = float(capacity)
        self._last = time.time()

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self._last
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_per_sec)
        self._last = now
        if self._tokens >= 1:
            self._tokens -= 1
            return True
        return False

bucket = TokenBucket(3, 1)
print({"call": 1, "allowed": bucket.allow()})
print({"call": 2, "allowed": bucket.allow()})
print({"call": 3, "allowed": bucket.allow()})
print({"call": 4, "allowed": bucket.allow()})
`,
    go: `package main

import (
  "fmt"
  "time"
)

type TokenBucket struct {
  capacity, refillPerSec, tokens float64
  last                           time.Time
}

func New(cap, rate float64) *TokenBucket {
  return &TokenBucket{capacity: cap, refillPerSec: rate, tokens: cap, last: time.Now()}
}

func (b *TokenBucket) Allow() bool {
  elapsed := time.Since(b.last).Seconds()
  b.last = time.Now()
  b.tokens = min(b.capacity, b.tokens+elapsed*b.refillPerSec)
  if b.tokens >= 1 { b.tokens--; return true }
  return false
}

func main() {
  b := New(3, 1)
  fmt.Printf("%+v\n", map[string]any{"call": 1, "allowed": b.Allow()})
  fmt.Printf("%+v\n", map[string]any{"call": 2, "allowed": b.Allow()})
  fmt.Printf("%+v\n", map[string]any{"call": 3, "allowed": b.Allow()})
  fmt.Printf("%+v\n", map[string]any{"call": 4, "allowed": b.Allow()})
}
`,
  },
  "feature-flag-service": {
    ts: `// feature-flags.ts
type Ctx = { userId?: string; [k: string]: unknown };

interface Flag {
  key: string;
  enabled: boolean;
  rollout?: number;
  allowlist?: string[];
}

class FeatureFlagService {
  private flags = new Map<string, Flag>();
  register(f: Flag) { this.flags.set(f.key, f); }

  isOn(key: string, ctx: Ctx = {}): boolean {
    const f = this.flags.get(key);
    if (!f || !f.enabled) return false;
    if (f.allowlist?.includes(ctx.userId ?? "")) return true;
    if (f.rollout !== undefined) {
      const h = [...(ctx.userId ?? "x")].reduce((a, c) => a + c.charCodeAt(0), 0);
      return (h % 100) < f.rollout;
    }
    return true;
  }
}

const svc = new FeatureFlagService();
svc.register({ key: "new-checkout", enabled: true, allowlist: ["u_42"] });
svc.register({ key: "dark-mode",    enabled: true, rollout: 50 });

console.log({ flag: "new-checkout", userId: "u_42", result: svc.isOn("new-checkout", { userId: "u_42" }) });
console.log({ flag: "dark-mode",    userId: "u_7",  result: svc.isOn("dark-mode",    { userId: "u_7"  }) });
`,
    js: `// feature-flags.js
class FeatureFlagService {
  #flags = new Map();
  register(f) { this.#flags.set(f.key, f); }
  isOn(key, ctx = {}) {
    const f = this.#flags.get(key);
    if (!f || !f.enabled) return false;
    if (f.allowlist?.includes(ctx.userId ?? "")) return true;
    if (f.rollout !== undefined) {
      const h = [...(ctx.userId ?? "x")].reduce((a, c) => a + c.charCodeAt(0), 0);
      return (h % 100) < f.rollout;
    }
    return true;
  }
}

const svc = new FeatureFlagService();
svc.register({ key: "new-checkout", enabled: true, allowlist: ["u_42"] });
svc.register({ key: "dark-mode",    enabled: true, rollout: 50 });

console.log({ flag: "new-checkout", userId: "u_42", result: svc.isOn("new-checkout", { userId: "u_42" }) });
console.log({ flag: "dark-mode",    userId: "u_7",  result: svc.isOn("dark-mode",    { userId: "u_7"  }) });
`,
    py: `# feature_flags.py
class FeatureFlagService:
    def __init__(self): self._flags = {}
    def register(self, flag): self._flags[flag["key"]] = flag
    def is_on(self, key, ctx={}):
        f = self._flags.get(key)
        if not f or not f.get("enabled"): return False
        if ctx.get("userId") in f.get("allowlist", []): return True
        if "rollout" in f:
            h = sum(ord(c) for c in ctx.get("userId", "x"))
            return (h % 100) < f["rollout"]
        return True

svc = FeatureFlagService()
svc.register({"key": "new-checkout", "enabled": True,  "allowlist": ["u_42"]})
svc.register({"key": "dark-mode",    "enabled": True,  "rollout": 50})
print({"flag": "new-checkout", "userId": "u_42", "result": svc.is_on("new-checkout", {"userId": "u_42"})})
print({"flag": "dark-mode",    "userId": "u_7",  "result": svc.is_on("dark-mode",    {"userId": "u_7"})})
`,
    go: `package main

import "fmt"

type Flag struct{ Key string; Enabled bool; Rollout int; Allowlist []string }
type FlagSvc struct{ flags map[string]Flag }

func NewSvc() *FlagSvc { return &FlagSvc{flags: map[string]Flag{}} }
func (s *FlagSvc) Register(f Flag) { s.flags[f.Key] = f }
func (s *FlagSvc) IsOn(key, uid string) bool {
  f, ok := s.flags[key]
  if !ok || !f.Enabled { return false }
  for _, u := range f.Allowlist { if u == uid { return true } }
  if f.Rollout > 0 { var h int; for _, c := range uid { h += int(c) }; return h%100 < f.Rollout }
  return true
}

func main() {
  s := NewSvc()
  s.Register(Flag{Key: "new-checkout", Enabled: true, Allowlist: []string{"u_42"}})
  s.Register(Flag{Key: "dark-mode",    Enabled: true, Rollout: 50})
  fmt.Printf("%+v\n", map[string]any{"flag": "new-checkout", "userId": "u_42", "result": s.IsOn("new-checkout", "u_42")})
  fmt.Printf("%+v\n", map[string]any{"flag": "dark-mode",    "userId": "u_7",  "result": s.IsOn("dark-mode",    "u_7")})
}
`,
  },
};

const DEFAULT_STARTER = {
  ts: `// Write your TypeScript solution here

function solution(): void {
  console.log({ status: "ready", message: "Start coding!" });
}

solution();
`,
  js: `// Write your JavaScript solution here
function solution() {
  console.log({ status: "ready", message: "Start coding!" });
}
solution();
`,
  py: `# Write your Python solution here
def solution():
    print({"status": "ready", "message": "Start coding!"})
solution()
`,
  go: `package main
import "fmt"
func main() {
  fmt.Printf("%+v\n", map[string]any{"status": "ready", "message": "Start coding!"})
}
`,
};

function getStarter(slug, lang) {
  return STARTERS[slug]?.[lang] ?? DEFAULT_STARTER[lang] ?? DEFAULT_STARTER.ts;
}

// ─── Sandboxed JS/TS runner ───────────────────────────────────────────────────

function runCodeLocally(code, lang) {
  const logs = [],
    errors = [];
  const t0 = performance.now();
  const proxyConsole = {
    log: (...args) =>
      logs.push(
        args.map((a) => {
          try {
            return typeof a === "object" && a !== null ? JSON.parse(JSON.stringify(a)) : a;
          } catch {
            return String(a);
          }
        }),
      ),
    error: (...args) => errors.push(args.map(String).join(" ")),
    warn: (...args) => errors.push("[warn] " + args.map(String).join(" ")),
  };

  let src = code;
  if (lang === "ts") {
    src = src
      .replace(/interface\s+\w+\s*\{[^}]*\}/gs, "")
      .replace(/type\s+\w+\s*=\s*[^;]+;/g, "")
      .replace(/:\s*(number|string|boolean|void|any|never|unknown|object|Ctx|Flag)\b(\[\])?/g, "")
      .replace(/<[A-Za-z,\s[\]|]+>/g, "")
      .replace(/\b(private|public|protected|readonly|export)\s+/g, "")
      .replace(/\bimport\s+.*?;/g, "");
  }

  try {
    // eslint-disable-next-line no-new-func
    new Function("console", src)(proxyConsole);
  } catch (e) {
    errors.push(e.message);
  }

  return { logs, errors, ms: (performance.now() - t0).toFixed(2) };
}

// ─── Monaco Editor component ──────────────────────────────────────────────────

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
        language: LANG_TO_MONACO[language] ?? "typescript",
        theme: "vs-dark",
        fontSize: 13,
        fontFamily: '"JetBrains Mono", "Fira Code", ui-monospace, monospace',
        fontLigatures: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        lineNumbers: "on",
        renderLineHighlight: "gutter",
        padding: { top: 12, bottom: 12 },
        tabSize: 2,
        wordWrap: "on",
        automaticLayout: true,
        scrollbar: { verticalScrollbarSize: 5, horizontalScrollbarSize: 5 },
        overviewRulerLanes: 0,
        renderWhitespace: "none",
        contextmenu: true,
        glyphMargin: false,
        folding: true,
        suggest: { showKeywords: true },
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!editorRef.current || !window.monaco) return;
    const model = editorRef.current.getModel();
    if (!model) return;
    window.monaco.editor.setModelLanguage(model, LANG_TO_MONACO[language] ?? "typescript");
    if (prevLang.current !== language) {
      model.setValue(value);
      prevLang.current = language;
    }
  }, [language, value]);

  return <div ref={containerRef} style={{ height: "100%", width: "100%" }} />;
}

// ─── Console output ───────────────────────────────────────────────────────────

function fmt(v) {
  if (v === null || v === undefined) return String(v);
  if (typeof v === "string") return `"${v}"`;
  if (typeof v === "boolean" || typeof v === "number") return String(v);
  if (Array.isArray(v)) return `[${v.map(fmt).join(", ")}]`;
  if (typeof v === "object") return JSON.stringify(v);
  return String(v);
}

function valColor(v) {
  if (typeof v === "boolean") return v ? "#4FC1FF" : "#F44747";
  if (typeof v === "number") return "#B5CEA8";
  if (typeof v === "string") return "#CE9178";
  return "#858585";
}

function ObjToken({ data }) {
  const entries = Object.entries(data);
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 2,
        border: "1px solid #333",
        borderRadius: 4,
        padding: "1px 6px",
        background: "#1a1a1a",
        fontFamily: "inherit",
      }}
    >
      <span style={{ color: "#858585" }}>{"{"}</span>
      {entries.map(([k, v], i) => (
        <span key={k}>
          <span style={{ color: "#9CDCFE" }}>{k}</span>
          <span style={{ color: "#858585" }}>: </span>
          <span style={{ color: valColor(v) }}>{fmt(v)}</span>
          {i < entries.length - 1 && <span style={{ color: "#858585" }}>, </span>}
        </span>
      ))}
      <span style={{ color: "#858585" }}>{"}"}</span>
    </span>
  );
}

function ConsoleOutput({ result, isRunning }) {
  if (isRunning)
    return (
      <div className="flex items-center gap-2 p-3 font-mono text-xs text-muted-foreground">
        <Loader2 className="h-3.5 w-3.5 animate-spin" /> Running...
      </div>
    );
  if (!result)
    return (
      <p className="p-3 font-mono text-[11px] text-muted-foreground">
        Press <span className="text-foreground">Run</span> to execute. Output appears here as
        structured objects.
      </p>
    );

  const { logs, errors, ms } = result;
  return (
    <div className="max-h-64 overflow-auto p-3 font-mono text-[11px] leading-relaxed">
      <div className="mb-2 flex items-center gap-3 border-b border-border pb-1.5 text-[10px] text-muted-foreground">
        <span>
          {logs.length} log{logs.length !== 1 ? "s" : ""}
        </span>
        {errors.length > 0 && (
          <span className="text-destructive">
            {errors.length} error{errors.length !== 1 ? "s" : ""}
          </span>
        )}
        <span className="ml-auto">{ms} ms</span>
      </div>
      {logs.map((args, i) => (
        <div key={i} className="mb-1.5 flex items-start gap-2">
          <span className="select-none text-[10px] text-muted-foreground/40">
            {String(i + 1).padStart(2, "0")}
          </span>
          <div className="flex flex-wrap gap-1.5">
            {args.map((a, j) =>
              typeof a === "object" && a !== null ? (
                <ObjToken key={j} data={a} />
              ) : (
                <span key={j} className="text-foreground/90">
                  {String(a)}
                </span>
              ),
            )}
          </div>
        </div>
      ))}
      {errors.map((e, i) => (
        <div key={i} className="mb-1 flex items-start gap-1.5">
          <X className="mt-0.5 h-3 w-3 shrink-0 text-destructive" />
          <span className="text-destructive">{e}</span>
        </div>
      ))}
      {errors.length === 0 && logs.length > 0 && (
        <div className="mt-2 flex items-center gap-1.5 border-t border-border pt-2 text-[10px] text-success">
          <Check className="h-3 w-3" /> Run finished in {ms} ms
        </div>
      )}
    </div>
  );
}

// ─── Drag handle ──────────────────────────────────────────────────────────────

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

// ─── Main EditorPage ──────────────────────────────────────────────────────────

function EditorPage() {
  const { id: slug } = useParams();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.user);
  const execState = useSelector(selectChallengeExecution);
  const c = useSelector(selectChallengeDetail(slug));
  const loading = useSelector(selectDetailLoading);
  const detailError = useSelector(selectDetailError);

  const [lang, setLang] = useState("ts");
  const [code, setCode] = useState(() => getStarter(slug, "ts"));
  const [consoleResult, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("testcase");

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
    setCode(getStarter(slug, lang));
    setResult(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  useEffect(() => {
    dispatch(FetchChallengeBySlug(slug));
  }, [dispatch, slug]);

  const handleLangChange = useCallback(
    (l) => {
      setLang(l);
      setCode(getStarter(slug, l));
      setResult(null);
    },
    [slug],
  );

  // Run — executes visible sample test cases only
  const handleRun = useCallback(() => {
    dispatch(resetExecution());
    setActiveTab("result");
    const sampleTests = (c?.test_cases ?? []).filter((t) => !t.hidden);
    dispatch(runCode({ code, language: lang, testCases: sampleTests }));
  }, [code, lang, c, dispatch]);

  // Submit — runs against all test cases (including hidden) via backend DB
  const handleSubmit = useCallback(() => {
    dispatch(resetExecution());
    setActiveTab("result");
    dispatch(submitCode({ code, language: lang, slug, userId: user?.user_id }));
  }, [code, lang, slug, dispatch, user]);

  if (loading && !c)
    return (
      <AppShell>
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-muted-foreground">
            <div className="h-8 w-8 animate-spin rounded-full border border-zinc-700 border-t-primary" />
            <p className="text-sm">Loading editor...</p>
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
      <div className="flex items-center justify-between border-b border-border bg-card/40 px-4 py-2 md:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="h-8 w-8">
            <Link to={`/app/challenges/${c.slug}`}>
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold">{c.title}</p>
            <p className="truncate text-xs text-muted-foreground">
              {c.domain} · {c.difficulty} · {c.minutes}m
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Select value={lang} onValueChange={handleLangChange}>
            <SelectTrigger className="h-8 w-[130px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(LANG_LABEL).map(([v, l]) => (
                <SelectItem key={v} value={v}>
                  {l}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" onClick={handleRun} disabled={c?.locked || isRunning || isSubmitting}>
            {isRunning ? (
              <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
            ) : (
              <Play className="mr-1.5 h-3.5 w-3.5" />
            )}
            Run
          </Button>
          <Button size="sm" onClick={handleSubmit} disabled={c?.locked || isRunning || isSubmitting}>
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
                className="xl:hidden"
                aria-label="Open browser preview"
              >
                <Globe className="h-4 w-4" />
              </Button>
            </DrawerTrigger>
            <DrawerContent className="p-0">
              <div className="flex h-[85vh] flex-col overflow-hidden">
                <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} code={code} execState={execState} />
              </div>
            </DrawerContent>
          </Drawer>
        </div>
      </div>

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
            className="hidden flex-col overflow-hidden border-r border-border bg-card md:flex"
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
            <div className="flex-1 overflow-auto px-4 py-4 text-sm leading-relaxed text-foreground/90">
              <p>{c.summary}</p>
              {c.description && <p className="mt-3 text-muted-foreground">{c.description}</p>}
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
            </div>
          </aside>

          {/* DRAG: left | center */}
          <DragHandle onDelta={onDragLeft} />

          {/* CENTER: editor + bottom tabs */}
          <div className="flex min-w-0 flex-1 flex-col">
            {/* File tab bar */}
            <div className="flex items-center gap-1 border-b border-border bg-background/60 px-2 py-1.5">
              <div className="flex items-center gap-2 rounded-t border-b-2 border-primary bg-card px-3 py-1 font-mono text-xs text-foreground">
                <FileCode2 className="h-3 w-3" /> {fileName}
              </div>
            </div>

            {/* Monaco editor */}
            <div className="min-h-0 flex-1 overflow-hidden bg-[#1E1E1E]">
              <MonacoEditor value={code} language={lang} onChange={setCode} />
            </div>

            {/* Bottom panel */}
            <div className="border-t border-border bg-background/60">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="flex flex-col">
                <div className="flex items-center justify-between border-b border-border px-3 py-1.5">
                  <TabsList className="h-8 bg-transparent p-0">
                    <TabsTrigger value="testcase" className="h-7 px-3 text-xs">
                      Testcase
                    </TabsTrigger>
                    <TabsTrigger value="result" className="h-7 px-3 text-xs">
                      Test Result
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
                      {LANG_BADGE[lang]}
                    </Badge>
                  </div>
                </div>

                <TabsContent value="testcase" className="m-0 max-h-64 overflow-auto p-3">
                  {c.test_cases?.filter((t) => !t.hidden).length > 0 ? (
                    <div className="grid gap-2 md:grid-cols-3">
                      {c.test_cases
                        .filter((t) => !t.hidden)
                        .map((t) => (
                          <div
                            key={t.id}
                            className="rounded-md border border-border bg-card/60 p-3 text-xs"
                          >
                            <p className="font-mono text-[11px] text-muted-foreground">{t.name}</p>
                            {t.stdin && (
                              <p className="mt-1.5 font-mono text-foreground">{t.stdin.trim()}</p>
                            )}
                            {t.expected_output && (
                              <p className="mt-1 font-mono text-muted-foreground">
                                → {t.expected_output.trim()}
                              </p>
                            )}
                          </div>
                        ))}
                    </div>
                  ) : (
                    <p className="text-xs text-muted-foreground">
                      No visible test cases for this challenge.
                    </p>
                  )}
                </TabsContent>

                {/* Test Result tab: shows Run OR Submit results */}
                <TabsContent value="result" className="m-0 max-h-72 overflow-auto p-3 space-y-3">
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
                <TabsContent value="console" className="m-0 max-h-64 overflow-auto p-3">
                  <ConsoleOutput result={consoleResult} isRunning={false} />
                </TabsContent>

              </Tabs>
            </div>
          </div>

          {/* DRAG: center | right */}
          <DragHandle onDelta={onDragRight} />

          {/* RIGHT: browser preview */}
          <aside
            className="hidden flex-col overflow-hidden bg-card xl:flex"
            style={{ width: rightW, minWidth: MIN_COL, flexShrink: 0 }}
          >
            <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} code={code} execState={execState} />
          </aside>
        </div>
      )}
    </AppShell>
  );
}

// ─── BrowserPreview ───────────────────────────────────────────────────────────

function BrowserPreview({ domain, slug, title, code, execState }) {
  return (
    <div className="flex min-h-0 flex-1 flex-col overflow-hidden bg-card">
      <div className="border-b border-border bg-background/60 px-3 py-2">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-destructive/70" />
            <span className="h-2.5 w-2.5 rounded-full bg-warning/70" />
            <span className="h-2.5 w-2.5 rounded-full bg-success/70" />
          </div>
          <button className="ml-1 rounded p-1 text-muted-foreground hover:bg-secondary hover:text-foreground">
            <RotateCw className="h-3.5 w-3.5" />
          </button>
          <div className="flex flex-1 items-center gap-1.5 rounded-md border border-border bg-background/80 px-2.5 py-1 font-mono text-[11px] text-muted-foreground">
            <Lock className="h-3 w-3 text-success" />
            <span className="truncate">localhost:3000/preview</span>
          </div>
          <button className="rounded p-1 text-muted-foreground hover:bg-secondary hover:text-foreground">
            <Globe className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
      <PreviewArea domain={domain} slug={slug} title={title} code={code} execState={execState} />
    </div>
  );
}

const FRONTEND_DOMAINS = new Set(["Frontend"]);

function PreviewArea({ domain, slug, title, code, execState }) {
  if (FRONTEND_DOMAINS.has(domain)) {
    return (
      <div className="flex flex-1 flex-col overflow-hidden bg-white">
        <iframe
          title={`${title} preview`}
          srcDoc={code || getFrontendSrcDoc(slug, title)}
          sandbox="allow-scripts"
          className="h-full w-full flex-1 border-0 bg-white"
        />
      </div>
    );
  }

  // Determine if we have real execution results
  const runResult = execState?.runResult;
  const submitResult = execState?.submitResult;
  const isRunning = execState?.runStatus === "loading";
  const isSubmitting = execState?.submitStatus === "loading";

  if (isRunning || isSubmitting) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center bg-[#0A0A0A] p-6 text-zinc-500 italic text-xs">
        <Loader2 className="h-5 w-5 animate-spin text-primary mb-2" />
        {isRunning ? "Running test cases on backend sandbox..." : "Submitting solution to judge..."}
      </div>
    );
  }

  if (!runResult && !submitResult) {
    // Show empty state or static seed as fallback
    const out = getProgramOutput(slug);
    return (
      <div className="flex flex-1 flex-col overflow-auto bg-[#0A0A0A] p-4 text-xs font-sans">
        <div className="rounded-lg border border-border bg-card/60 p-4">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">Backend Preview Console</p>
          <p className="mt-2 text-zinc-400 leading-relaxed">
            No active execution session. Write code and click <strong>Run</strong> or <strong>Submit</strong> to verify results here.
          </p>
        </div>

        {/* Render a fallback expected output */}
        <div className="mt-3 rounded-lg border border-border bg-card/60 p-4">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">Expected Output Format</p>
          <pre className="mt-3 whitespace-pre-wrap font-mono text-[11px] leading-relaxed text-zinc-500">
            {out.log}
          </pre>
        </div>
      </div>
    );
  }

  // Actual results!
  if (runResult) {
    const sumRuntime = (results) => results.reduce((acc, curr) => acc + (curr.runtime_ms || 0), 0);
    const hasCompileError = !!runResult.compile_output;
    return (
      <div className="flex flex-1 flex-col overflow-auto bg-[#0A0A0A] p-4 font-mono text-[11px] leading-relaxed text-zinc-300 space-y-4">
        <div className="rounded-lg border border-border bg-card/65 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-sans">Sandbox Statistics</p>
          <div className="grid grid-cols-2 gap-2 mt-1 font-sans text-xs">
            <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
              <p className="text-muted-foreground text-[10px] uppercase">Passed</p>
              <p className="font-mono font-bold text-white text-sm">
                {runResult.passed_testcases} / {runResult.total_testcases}
              </p>
            </div>
            <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
              <p className="text-muted-foreground text-[10px] uppercase">Runtime</p>
              <p className="font-mono font-bold text-emerald-400 text-sm">
                {runResult.testcase_results?.[0]?.runtime_ms ? `${sumRuntime(runResult.testcase_results).toFixed(0)} ms` : "N/A"}
              </p>
            </div>
          </div>
        </div>

        {hasCompileError && (
          <div className="rounded-lg border border-red-500/20 bg-red-950/15 p-4 space-y-2">
            <p className="text-[10px] uppercase tracking-wider text-red-400 font-bold">Compilation Errors</p>
            <pre className="whitespace-pre-wrap text-red-300 bg-black/40 p-2.5 rounded border border-red-500/10 text-[10px]">{runResult.compile_output}</pre>
          </div>
        )}

        {runResult.testcase_results?.map((tc, idx) => (
          <div key={idx} className="rounded-lg border border-border bg-card/45 p-4 space-y-2">
            <div className="flex justify-between items-center border-b border-border pb-1.5">
              <span className="font-bold text-white">Test Case #{idx + 1}: {tc.name}</span>
              <span className={`text-[9px] font-bold px-2 py-0.5 rounded ${tc.passed ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400"}`}>
                {tc.passed ? "PASSED" : "FAILED"}
              </span>
            </div>
            {tc.stdout && (
              <div className="space-y-1">
                <span className="text-zinc-500 text-[10px] block font-sans">Standard Output:</span>
                <pre className="bg-black/50 p-2 rounded text-zinc-350 text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.stdout}</pre>
              </div>
            )}
            {tc.stderr && (
              <div className="space-y-1">
                <span className="text-red-400 text-[10px] block font-sans">Error Output (stderr):</span>
                <pre className="bg-red-950/10 p-2 rounded text-red-350 text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.stderr}</pre>
              </div>
            )}
            {!tc.passed && (
              <div className="grid grid-cols-2 gap-2 mt-1 font-sans text-xs">
                <div>
                  <span className="text-zinc-500 text-[10px]">Actual</span>
                  <pre className="bg-zinc-950 p-2 rounded text-zinc-400 font-mono text-[10px] overflow-x-auto">{tc.actual_output || tc.stdout || "Empty"}</pre>
                </div>
                <div>
                  <span className="text-zinc-500 text-[10px]">Expected</span>
                  <pre className="bg-zinc-950 p-2 rounded text-zinc-400 font-mono text-[10px] overflow-x-auto">{tc.expected_output || "Empty"}</pre>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    );
  }

  if (submitResult) {
    return (
      <div className="flex flex-1 flex-col overflow-auto bg-[#0A0A0A] p-4 font-mono text-[11px] leading-relaxed text-zinc-300 space-y-4">
        <div className={`p-4 rounded-xl border flex items-start gap-3.5 ${submitResult.success ? "bg-emerald-950/20 border-emerald-500/20 text-emerald-400" : "bg-red-950/20 border-red-500/20 text-red-400"
          }`}>
          <div className="space-y-1 font-sans">
            <h4 className="font-bold text-sm tracking-tight text-white uppercase">{submitResult.verdict}</h4>
            <p className="text-[11px] text-zinc-400">
              Passed {submitResult.passed_testcases} / {submitResult.total_testcases} testcases.
            </p>
          </div>
        </div>

        {submitResult.compile_output && (
          <div className="rounded-lg border border-red-500/20 bg-red-950/15 p-4 space-y-2">
            <p className="text-[10px] uppercase tracking-wider text-red-400 font-bold font-sans">Compilation Failure Details</p>
            <pre className="whitespace-pre-wrap text-red-300 bg-black/40 p-2.5 rounded border border-red-500/10 text-[10px]">{submitResult.compile_output}</pre>
          </div>
        )}
      </div>
    );
  }
}

function getProgramOutput(slug) {
  switch (slug) {
    case "build-a-rate-limiter":
      return {
        log: "> TokenBucket(3, 1)\n> b.allow() → true\n> b.allow() → true\n> b.allow() → true\n> b.allow() → false\n[waiting 1000ms...]\n> b.allow() → true\n\n✓ Run finished in 1.04s",
        stats: [
          { label: "Calls", value: "5" },
          { label: "Allowed", value: "4", tone: "text-success" },
          { label: "Denied", value: "1", tone: "text-destructive" },
          { label: "Avg ms", value: "0.21" },
        ],
      };
    case "feature-flag-service":
      return {
        log: '> flags.isOn("new-checkout", { userId: "u_42" }) → true\n> flags.isOn("dark-mode", { userId: "u_7" })       → false\n> flags.rollout("beta-search", 25%)                → ok\n> 1,204 evaluations in 980ms\n\n✓ Run finished in 0.98s',
        stats: [
          { label: "Evals", value: "1204" },
          { label: "Cache hit", value: "94%", tone: "text-success" },
          { label: "p95 ms", value: "1.8" },
          { label: "Errors", value: "0", tone: "text-success" },
        ],
      };
    default:
      return {
        log: `> running ${slug}...\n✓ build ok\n✓ tests passed\n✓ Run finished in 1.21s`,
        stats: [
          { label: "Status", value: "OK", tone: "text-success" },
          { label: "Duration", value: "1.21s" },
          { label: "Warnings", value: "0" },
          { label: "Errors", value: "0", tone: "text-success" },
        ],
      };
  }
}

function getFrontendSrcDoc(slug, title) {
  const base = `<style>:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Inter",sans-serif;color:#0a0a0a;background:#fff;padding:16px}h1,h2,h3{margin:0 0 12px}button{font:inherit;cursor:pointer}</style>`;
  switch (slug) {
    case "responsive-data-table":
      return `<!doctype html><html><head>${base}<style>.wrap{max-width:720px;margin:0 auto}.toolbar{display:flex;gap:8px;margin-bottom:12px}input{flex:1;padding:8px 10px;border:1px solid #e5e5e5;border-radius:8px;font:inherit}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #eee}th{background:#fafafa}tr:hover td{background:#fafafa}.pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px}.ok{background:#dcfce7;color:#166534}.warn{background:#fef9c3;color:#854d0e}.err{background:#fee2e2;color:#991b1b}</style></head><body><div class="wrap"><h2>Users</h2><div class="toolbar"><input id="q" placeholder="Search..."/></div><table><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th></tr></thead><tbody id="b"></tbody></table></div><script>const rows=[{name:"Ada Lovelace",email:"ada@interleet.dev",role:"Admin",status:"ok"},{name:"Linus Torvalds",email:"linus@interleet.dev",role:"Maintainer",status:"ok"},{name:"Grace Hopper",email:"grace@interleet.dev",role:"Member",status:"warn"},{name:"Alan Turing",email:"alan@interleet.dev",role:"Member",status:"err"},{name:"Margaret Hamilton",email:"margaret@interleet.dev",role:"Admin",status:"ok"}];const b=document.getElementById("b"),q=document.getElementById("q");function render(f){f=(f||"").toLowerCase();b.innerHTML=rows.filter(r=>r.name.toLowerCase().includes(f)||r.email.toLowerCase().includes(f)).map(r=>'<tr><td>'+r.name+'</td><td>'+r.email+'</td><td>'+r.role+'</td><td><span class="pill '+r.status+'">'+r.status+'</span></td></tr>').join("");}q.addEventListener("input",e=>render(e.target.value));render("");</script></body></html>`;
    case "ssr-cache-strategy":
      return `<!doctype html><html><head>${base}<style>.card{border:1px solid #e5e5e5;border-radius:10px;padding:14px;margin-bottom:10px}.row{display:flex;justify-content:space-between;font-family:monospace;font-size:12px;padding:4px 0}.ok{color:#16a34a}.miss{color:#dc2626}button{padding:8px 12px;border:1px solid #0a0a0a;background:#0a0a0a;color:#fff;border-radius:8px}</style></head><body><h2>SSR Cache Preview</h2><div class="card"><div class="row"><span>GET /products</span><span id="s1" class="ok">HIT · 4ms</span></div><div class="row"><span>GET /products/42</span><span id="s2" class="miss">MISS · 218ms</span></div><div class="row"><span>GET /search?q=shoe</span><span id="s3" class="ok">HIT · 6ms</span></div></div><button onclick="bust()">Bust cache</button><script>function bust(){["s1","s2","s3"].forEach(id=>{const el=document.getElementById(id);el.textContent="MISS · "+(180+Math.floor(Math.random()*120))+"ms";el.className="miss";});}</script></body></html>`;
    default:
      return `<!doctype html><html><head>${base}</head><body><h2>${title}</h2><p style="color:#525252">Interactive preview for this challenge will render here.</p></body></html>`;
  }
}

export default EditorPage;
