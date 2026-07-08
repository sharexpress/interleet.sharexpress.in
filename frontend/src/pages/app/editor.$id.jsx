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

const LANG_TO_MONACO = {
  ts: "typescript", js: "javascript", py: "python", go: "go",
  html: "html", css: "css",
  java: "java", cpp: "cpp", rust: "rust",
  // Monaco-native language IDs (passed through from multi-file extension detection)
  shell: "shell", yaml: "yaml", dockerfile: "dockerfile", plaintext: "plaintext",
  javascript: "javascript", typescript: "typescript", python: "python",
  multi: "shell",  // default for multi-file DevOps mode
};
const LANG_LABEL = { ts: "TypeScript", js: "JavaScript", py: "Python", go: "Go", java: "Java", cpp: "C++", rust: "Rust" };
const LANG_BADGE = { ts: "node v20.10", js: "node v20.10", py: "python 3.12", go: "go 1.22", java: "openjdk 21", cpp: "gcc 13.2", rust: "rustc 1.75" };
const LANG_FILE = { ts: "solution.ts", js: "solution.js", py: "solution.py", go: "main.go", java: "Solution.java", cpp: "solution.cpp", rust: "solution.rs" };

// Reverse-map backend language strings to editor short codes
const BACKEND_LANG_TO_SHORT = {
  typescript: "ts",
  javascript: "js",
  python: "py",
  go: "go",
  cpp: "cpp",
  rust: "rust",
  java: "java",
};

const EnvironmentInfo = memo(function EnvironmentInfo({ domain, lang }) {
  const isFrontend = domain === "Frontend";
  return (
    <div className="mt-4 rounded-lg border border-border bg-background/35 p-3 space-y-2 font-sans text-xs">
      <div className="flex items-center gap-1.5 border-b border-border/60 pb-1.5 text-[9px] uppercase font-mono tracking-wider text-muted-foreground">
        <span>⚙️ Execution Environment</span>
      </div>
      <div className="grid grid-cols-2 gap-2 text-[10px]">
        <div>
          <span className="text-zinc-500 block">Preview / Runtime</span>
          <span className="text-zinc-300 font-medium truncate block">
            {isFrontend ? "Live Browser Preview" : lang === "py" ? "Python 3.12 (Docker)" : lang === "js" ? "Node.js 20 (Docker)" : lang === "ts" ? "Node.js 20 (TS-Node)" : lang === "go" ? "Go 1.22 (Docker)" : "Docker Sandbox"}
          </span>
        </div>
        <div>
          <span className="text-zinc-500 block">Network Access</span>
          <span className="text-red-400 font-medium">Disabled (Isolated)</span>
        </div>
        <div>
          <span className="text-zinc-500 block">Memory Limit</span>
          <span className="text-zinc-300 font-medium">256 MB Hard Cap</span>
        </div>
        <div>
          <span className="text-zinc-500 block">Time Limit</span>
          <span className="text-zinc-300 font-medium">10.0 seconds</span>
        </div>
      </div>
      <div className="text-[9px] text-zinc-500 border-t border-border/60 pt-1.5 flex flex-wrap gap-1.5 items-center">
        <span>Preinstalled:</span>
        <span className="bg-secondary/40 px-1 py-0.5 rounded text-zinc-400 font-mono">lodash</span>
        <span className="bg-secondary/40 px-1 py-0.5 rounded text-zinc-400 font-mono">axios</span>
        {isFrontend && <span className="bg-secondary/40 px-1 py-0.5 rounded text-zinc-400 font-mono">jsdom</span>}
      </div>
    </div>
  );
});

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
  java: `import java.util.Map;

public class Solution {
    public static void main(String[] args) {
        System.out.println("{\\"status\\": \\"ready\\", \\"message\\": \\"Start coding!\\"}");
    }
}
`,
  cpp: `#include <iostream>

int main() {
    std::cout << "{\\"status\\": \\"ready\\", \\"message\\": \\"Start coding!\\"}" << std::endl;
    return 0;
}
`,
  rust: `fn main() {
    println!("{{\\"status\\": \\"ready\\", \\"message\\": \\"Start coding!\\"}}");
}
`,
};

function getStarter(slug, lang, dbChallenge) {
  if (dbChallenge?.starter_code) {
    // For multi-file domains (DevOps, Frontend filesystem), use the "multi" or "html" key directly
    if (lang === "multi" && dbChallenge.starter_code.multi) {
      return dbChallenge.starter_code.multi;
    }
    if (lang === "html" && dbChallenge.starter_code.html) {
      return dbChallenge.starter_code.html;
    }
    const backendKey = lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang;
    if (dbChallenge.starter_code[backendKey]) {
      return dbChallenge.starter_code[backendKey];
    }
  }
  return STARTERS[slug]?.[lang] ?? DEFAULT_STARTER[lang] ?? DEFAULT_STARTER.ts;
}

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

const MonacoEditor = memo(function MonacoEditor({ value, language, onChange }) {
  const containerRef = useRef(null);
  const editorRef = useRef(null);
  const subRef = useRef(null);
  const prevLang = useRef(language);

  // Store latest onChange callback in a ref to avoid stale closures in Monaco listeners
  const onChangeRef = useRef(onChange);
  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

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
      subRef.current = editor.onDidChangeModelContent(() => onChangeRef.current?.(editor.getValue()));
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
});

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

const ObjToken = memo(function ObjToken({ data }) {
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
});

const ConsoleOutput = memo(function ConsoleOutput({ result, isRunning }) {
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
});

// ─── Drag handle ──────────────────────────────────────────────────────────────

const DragHandle = memo(function DragHandle({ onDelta, onDragStart, onDragEnd }) {
  const dragging = useRef(false);
  const startX = useRef(0);

  const onMouseDown = useCallback(
    (e) => {
      e.preventDefault();
      dragging.current = true;
      startX.current = e.clientX;
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      if (onDragStart) onDragStart();

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
        if (onDragEnd) onDragEnd();
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [onDelta, onDragStart, onDragEnd],
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
});

const VerticalDragHandle = memo(function VerticalDragHandle({ onDelta, onDragStart, onDragEnd }) {
  const dragging = useRef(false);
  const startY = useRef(0);

  const onMouseDown = useCallback(
    (e) => {
      e.preventDefault();
      dragging.current = true;
      startY.current = e.clientY;
      document.body.style.cursor = "row-resize";
      document.body.style.userSelect = "none";
      if (onDragStart) onDragStart();

      const onMove = (ev) => {
        if (!dragging.current) return;
        const delta = ev.clientY - startY.current;
        startY.current = ev.clientY;
        onDelta(delta);
      };
      const onUp = () => {
        dragging.current = false;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
        if (onDragEnd) onDragEnd();
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [onDelta, onDragStart, onDragEnd],
  );

  return (
    <div
      onMouseDown={onMouseDown}
      className="group relative z-10 flex-shrink-0"
      style={{ height: 4, cursor: "row-resize" }}
    >
      <div
        className="absolute inset-x-0 top-0 bottom-0 bg-border opacity-0 transition-opacity group-hover:opacity-100"
        style={{ margin: "1px 0" }}
      />
    </div>
  );
});

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

  const isMultiFileDomain = c?.runtime_config?.capabilities?.filesystem || false;

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

  // Sync workspace helper
  const syncWorkspaceFiles = useCallback(async () => {
    if (!devopsSessionId) return;
    try {
      await API.post(`/api/v1/devops/session/${devopsSessionId}/sync`, { files: multiFiles });
    } catch (e) {
      console.error("Failed to sync files to container sandbox:", e);
    }
  }, [devopsSessionId, multiFiles]);

  // Dynamic WebSocket interactive terminal connector
  useEffect(() => {
    if (activeTab !== "terminal" || !devopsSessionId || !terminalRef.current || !terminalMounted) {
      return;
    }

    // 1. Sync workspace files first so Nginx/scripts reflect latest editor state
    syncWorkspaceFiles();

    // 2. Initialize Xterm.js terminal instance
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

    // 3. Connect WebSocket
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
      term.write("\r\n*** Terminal connection established. Welcome to Interleet Sandbox! ***\r\n\r\n");
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
  }, [activeTab, devopsSessionId, terminalMounted, syncWorkspaceFiles]);

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
          isCustom: false
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
          {!isMultiFileDomain && (
            <Select value={lang} onValueChange={handleLangChange}>
            <SelectTrigger className="h-8 w-[130px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {availableLangs.map((v) => (
                <SelectItem key={v} value={v}>
                  {LANG_LABEL[v]}
                </SelectItem>
              ))}
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
          <div className="hidden md:block flex-shrink-0">
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
          <div className="hidden xl:block flex-shrink-0">
            <DragHandle onDelta={onDragRight} onDragStart={handleDragStart} onDragEnd={handleDragEnd} />
          </div>

          {/* RIGHT: browser preview */}
          <aside
            className={`hidden flex-col overflow-hidden bg-card xl:flex ${isDraggingAny ? "pointer-events-none" : ""}`}
            style={{ width: rightW, minWidth: MIN_COL, flexShrink: 0 }}
          >
            <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} code={code} execState={execState} isMultiFileDomain={isMultiFileDomain} />
          </aside>
        </div>
      )}
    </AppShell>
  );
}

// ─── BrowserPreview ───────────────────────────────────────────────────────────

const BrowserPreview = memo(function BrowserPreview({ domain, slug, title, code, execState, isMultiFileDomain }) {
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
      <PreviewArea domain={domain} slug={slug} title={title} code={code} execState={execState} isMultiFileDomain={isMultiFileDomain} />
    </div>
  );
});

const FRONTEND_DOMAINS = new Set(["Frontend"]);

const PreviewArea = memo(function PreviewArea({ domain, slug, title, code, execState, isMultiFileDomain }) {
  if (FRONTEND_DOMAINS.has(domain)) {
    return (
      <div className="flex flex-1 flex-col overflow-hidden bg-white">
        <iframe
          title={`${title} preview`}
          srcDoc={compileFrontendCode(code, slug, title)}
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
    const activeStatus = execState?.activeStatus;
    const stages = [
      { key: "QUEUED", label: "Queued", desc: "Waiting for container sandbox..." },
      { key: "COMPILING", label: "Compiling", desc: "Analyzing syntax and structure..." },
      { key: "RUNNING", label: "Running", desc: "Executing sandbox test suite..." },
      { key: "JUDGING", label: "Judging", desc: "Validating output against expectations..." },
    ];

    const activeIdx = stages.findIndex((s) => s.key === activeStatus);
    const currentIdx = activeIdx !== -1 ? activeIdx : isRunning ? 2 : 0;

    return (
      <div className="flex flex-1 flex-col items-center justify-center bg-[#0A0A0A] p-6 font-sans">
        <div className="max-w-xs w-full space-y-6">
          <div className="flex flex-col items-center text-center space-y-1.5">
            <Loader2 className="h-5 w-5 animate-spin text-primary" />
            <h4 className="text-zinc-200 text-xs font-semibold uppercase tracking-wider">
              {isSubmitting ? "Async Submitting" : "Executing Code"}
            </h4>
            <p className="text-zinc-500 text-[11px] italic min-h-[16px]">
              {stages[currentIdx]?.desc || "Running test cases on backend sandbox..."}
            </p>
          </div>

          <div className="relative px-2">
            <div className="absolute top-2.5 left-0 w-full h-[2px] bg-zinc-800 rounded-full" />
            <div
              className="absolute top-2.5 left-0 h-[2px] bg-primary rounded-full transition-all duration-500"
              style={{ width: `${(currentIdx / (stages.length - 1)) * 100}%` }}
            />
            <div className="relative flex justify-between">
              {stages.map((stage, idx) => {
                const isPassed = idx < currentIdx;
                const isActive = idx === currentIdx;
                
                return (
                  <div key={stage.key} className="flex flex-col items-center">
                    <div
                      className={`h-5 w-5 rounded-full flex items-center justify-center text-[9px] font-bold border transition-all duration-300 ${
                        isPassed
                          ? "bg-emerald-950 border-emerald-500 text-emerald-400"
                          : isActive
                          ? "bg-primary/20 border-primary text-primary animate-pulse font-extrabold"
                          : "bg-zinc-900 border-zinc-800 text-zinc-600"
                      }`}
                    >
                      {isPassed ? "✓" : idx + 1}
                    </div>
                    <span
                      className={`text-[9px] mt-1.5 font-mono ${
                        isActive
                          ? "text-primary font-bold animate-pulse"
                          : isPassed
                          ? "text-emerald-400"
                          : "text-zinc-600"
                      }`}
                    >
                      {stage.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!runResult && !submitResult) {
    // Show empty state or static seed as fallback
    const out = getProgramOutput(slug);
    return (
      <div className="flex flex-1 flex-col overflow-auto bg-[#0A0A0A] p-4 text-xs font-sans">
        <div className="rounded-lg border border-border bg-card/60 p-4">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
            {isMultiFileDomain ? "Infrastructure Logs" : "Backend Preview Console"}
          </p>
          <p className="mt-2 text-zinc-400 leading-relaxed">
            {isMultiFileDomain
              ? "No active execution session. Write configuration and click Run or Submit to verify results here."
              : "No active execution session. Write code and click Run or Submit to verify results here."}
          </p>
        </div>

        {/* Render a fallback expected output */}
        <div className="mt-3 rounded-lg border border-border bg-card/60 p-4">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
            {isMultiFileDomain ? "Validation Pipeline Spec" : "Expected Output Format"}
          </p>
          <pre className="mt-3 whitespace-pre-wrap font-mono text-[11px] leading-relaxed text-zinc-500">
            {out.log}
          </pre>
        </div>
      </div>
    );
  }

  // ── Shared result renderer for both Run and Submit ──
  const activeResult = runResult || submitResult;
  const isSubmitResult = !!submitResult && !runResult;
  const verdictStr = activeResult.verdict || "UNKNOWN";
  const tcResults = activeResult.testcase_results || [];
  const hasCompileError = !!activeResult.compile_output;

  const sumRuntime = (results) => results.reduce((acc, curr) => acc + (curr.runtime_ms || curr.wall_time_ms || 0), 0);
  const maxMemory = (results) => results.reduce((max, curr) => Math.max(max, curr.peak_memory_mb || 0), 0);

  // Verdict → styling map
  const VERDICT_STYLES = {
    ACCEPTED:              { bg: "bg-emerald-500/10", border: "border-emerald-500/20", text: "text-emerald-400", label: "Accepted", icon: "✓" },
    WRONG_ANSWER:          { bg: "bg-red-500/10",     border: "border-red-500/20",     text: "text-red-400",     label: "Wrong Answer", icon: "✗" },
    RUNTIME_ERROR:         { bg: "bg-orange-500/10",   border: "border-orange-500/20",  text: "text-orange-400",  label: "Runtime Error", icon: "!" },
    TIME_LIMIT_EXCEEDED:   { bg: "bg-yellow-500/10",   border: "border-yellow-500/20",  text: "text-yellow-400",  label: "Time Limit Exceeded", icon: "⏱" },
    MEMORY_LIMIT_EXCEEDED: { bg: "bg-purple-500/10",   border: "border-purple-500/20",  text: "text-purple-400",  label: "Memory Limit Exceeded", icon: "💾" },
    COMPILATION_ERROR:     { bg: "bg-red-500/10",      border: "border-red-500/20",     text: "text-red-400",     label: "Compilation Error", icon: "⚠" },
    INTERNAL_ERROR:        { bg: "bg-zinc-500/10",     border: "border-zinc-500/20",    text: "text-zinc-400",    label: "Internal Error", icon: "⚙" },
  };

  const vs = VERDICT_STYLES[verdictStr] || VERDICT_STYLES.INTERNAL_ERROR;

  return (
    <div className="flex flex-1 flex-col overflow-auto bg-[#0A0A0A] p-4 font-sans text-xs space-y-3">

      {/* ── Verdict Banner ── */}
      <div className={`p-4 rounded-xl border flex items-center gap-3 ${vs.bg} ${vs.border}`}>
        <span className={`text-2xl ${vs.text}`}>{vs.icon}</span>
        <div className="flex-1 min-w-0">
          <h4 className={`font-bold text-sm tracking-tight uppercase ${vs.text}`}>{vs.label}</h4>
          <p className="text-[11px] text-zinc-400 mt-0.5">
            Passed {activeResult.passed_testcases ?? 0} / {activeResult.total_testcases ?? 0} test cases
            {activeResult.score != null && activeResult.score < 100 && ` · Score: ${activeResult.score}%`}
          </p>
        </div>
        {isSubmitResult && <span className="text-[9px] text-zinc-500 uppercase font-mono">Submission</span>}
      </div>

      {/* ── Execution Summary Card ── */}
      <div className="rounded-lg border border-border bg-card/60 p-3.5 space-y-2">
        <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">Execution Diagnostics</p>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-1">
          <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
            <p className="text-muted-foreground text-[10px] uppercase">Compilation</p>
            <p className={`font-mono font-bold text-sm ${hasCompileError ? "text-red-400" : "text-emerald-400"}`}>
              {hasCompileError ? "Failed" : "Success"}
            </p>
          </div>
          <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
            <p className="text-muted-foreground text-[10px] uppercase">Exit Code</p>
            <p className={`font-mono font-bold text-sm ${(activeResult.exit_code || 0) !== 0 ? "text-orange-400" : "text-emerald-400"}`}>
              {activeResult.exit_code ?? 0}
            </p>
          </div>
          <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
            <p className="text-muted-foreground text-[10px] uppercase">Total Runtime</p>
            <p className="font-mono font-bold text-emerald-400 text-sm">
              {tcResults.length > 0 ? `${sumRuntime(tcResults).toFixed(0)} ms` : `${((activeResult.time || 0) * 1000).toFixed(0)} ms`}
            </p>
          </div>
          <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
            <p className="text-muted-foreground text-[10px] uppercase">Peak Memory</p>
            <p className="font-mono font-bold text-sky-400 text-sm">
              {tcResults.length > 0 ? `${maxMemory(tcResults).toFixed(1)} MB` : `${(activeResult.memory || 0).toFixed(1)} MB`}
            </p>
          </div>
          <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
            <p className="text-muted-foreground text-[10px] uppercase">Passed</p>
            <p className="font-mono font-bold text-white text-sm">
              {activeResult.passed_testcases ?? 0} / {activeResult.total_testcases ?? 0}
            </p>
          </div>
          <div className="rounded border border-border bg-background/40 px-2.5 py-1.5">
            <p className="text-muted-foreground text-[10px] uppercase">Verdict</p>
            <p className={`font-mono font-bold text-sm ${vs.text}`}>{vs.label}</p>
          </div>
        </div>
      </div>

      {/* ── Compilation Error Details ── */}
      {hasCompileError && (
        <div className="rounded-lg border border-red-500/20 bg-red-950/15 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-red-400 font-bold font-mono">Compilation Error</p>
          <pre className="whitespace-pre-wrap text-red-300 bg-black/40 p-2.5 rounded border border-red-500/10 text-[10px]">{activeResult.compile_output}</pre>
        </div>
      )}

      {/* ── Global stderr (if present at top level) ── */}
      {activeResult.stderr && !hasCompileError && (
        <div className="rounded-lg border border-orange-500/20 bg-orange-950/10 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-orange-400 font-bold font-mono">Standard Error (stderr)</p>
          <pre className="whitespace-pre-wrap text-orange-300 bg-black/40 p-2.5 rounded border border-orange-500/10 text-[10px]">{activeResult.stderr}</pre>
        </div>
      )}

      {/* ── Internal Error Message ── */}
      {activeResult.error && (
        <div className="rounded-lg border border-zinc-500/20 bg-zinc-900/40 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-zinc-400 font-bold font-mono">Internal Error</p>
          <pre className="whitespace-pre-wrap text-zinc-300 bg-black/40 p-2.5 rounded border border-zinc-500/10 text-[10px]">{activeResult.error}</pre>
        </div>
      )}

      {/* ── Per-Testcase Breakdown ── */}
      {tcResults.map((tc, idx) => {
        const tcVerdict = tc.verdict || (tc.passed ? "ACCEPTED" : "WRONG_ANSWER");
        const tcVs = VERDICT_STYLES[tcVerdict] || VERDICT_STYLES.INTERNAL_ERROR;
        const tcRuntime = tc.runtime_ms || tc.wall_time_ms || 0;
        const tcMemory = tc.peak_memory_mb || 0;

        return (
          <div key={idx} className="rounded-lg border border-border bg-card/45 p-4 space-y-2.5">
            {/* Header */}
            <div className="flex justify-between items-center border-b border-border pb-1.5">
              <span className="font-bold text-white text-xs">
                Test Case #{idx + 1}{tc.name ? `: ${tc.name}` : ""}
                {tc.hidden && <span className="ml-1.5 text-[9px] text-zinc-500 font-normal">(hidden)</span>}
              </span>
              <span className={`text-[9px] font-bold px-2 py-0.5 rounded ${tcVs.bg} ${tcVs.text}`}>
                {tcVs.icon} {tcVs.label}
              </span>
            </div>

            {/* Testcase diagnostics row */}
            <div className="flex flex-wrap gap-3 text-[10px] text-zinc-500 font-mono">
              {tc.exit_code !== 0 && <span>Exit: <span className="text-orange-400">{tc.exit_code}</span></span>}
              {tcRuntime > 0 && <span>Runtime: <span className="text-zinc-300">{tcRuntime.toFixed(0)} ms</span></span>}
              {tcMemory > 0 && <span>Memory: <span className="text-zinc-300">{tcMemory.toFixed(1)} MB</span></span>}
            </div>

            {/* stderr (always show if present) */}
            {tc.stderr && (
              <div className="space-y-1">
                <span className="text-orange-400 text-[10px] block font-sans font-semibold">stderr:</span>
                <pre className="bg-orange-950/20 border border-orange-500/10 p-2 rounded text-orange-300 text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.stderr}</pre>
              </div>
            )}

            {/* stdout (always show, even when empty) */}
            {!tc.hidden && (
              <div className="space-y-1">
                <span className="text-zinc-500 text-[10px] block font-sans">Your Output:</span>
                <pre className={`bg-black/50 p-2 rounded text-[10px] overflow-x-auto whitespace-pre-wrap ${
                  tc.stdout && !tc.stdout.startsWith("(no output") ? "text-zinc-300" : "text-zinc-600 italic"
                }`}>{tc.stdout || "(empty)"}</pre>
              </div>
            )}

            {/* Revealed diagnostic for hidden testcase */}
            {tc.hidden && tc.revealed_input && (
              <div className="space-y-2 border border-yellow-500/10 bg-yellow-500/5 p-3 rounded mt-2">
                <p className="text-[10px] font-bold text-yellow-400 uppercase tracking-wider block font-sans">Failing Hidden Case Diagnostics:</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1">
                  <div>
                    <span className="text-zinc-500 text-[9px] font-sans">Input:</span>
                    <pre className="bg-zinc-950 p-2 rounded border border-border text-zinc-300 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap select-all">{tc.revealed_input}</pre>
                  </div>
                  {tc.revealed_expected && (
                    <div>
                      <span className="text-zinc-500 text-[9px] font-sans">Expected Output:</span>
                      <pre className="bg-zinc-950 p-2 rounded border border-border text-emerald-400 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap select-all">{tc.revealed_expected}</pre>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Expected vs Actual on failure (non-hidden only) */}
            {!tc.passed && !tc.hidden && (
              <div className="grid grid-cols-2 gap-2 mt-1">
                <div>
                  <span className="text-zinc-500 text-[10px] font-sans">Expected:</span>
                  <pre className="bg-zinc-950 p-2 rounded text-emerald-400/70 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.expected_output || "(empty)"}</pre>
                </div>
                <div>
                  <span className="text-zinc-500 text-[10px] font-sans">Actual:</span>
                  <pre className="bg-zinc-950 p-2 rounded text-red-400/70 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.stdout || "(empty)"}</pre>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
});

function getProgramOutput(slug) {
  switch (slug) {
    case "configure-nginx-proxy":
      return {
        log: "Workspace Ready\n✓\nConfiguration Loaded\n✓\nStarting Backend\n✓\nReloading Nginx\n✓\nRunning Health Checks\n✓\nValidation Passed\n\nAll HTTP checks passed successfully.",
        stats: [
          { label: "Nginx", value: "Running", tone: "text-success" },
          { label: "Backend", value: "Running", tone: "text-success" },
          { label: "Reverse Proxy", value: "Configured", tone: "text-success" },
        ],
      };
    case "orchestrate-redis-node":
      return {
        log: "Workspace Ready\n✓\nDocker Compose File Loaded\n✓\nStarting Containers\n✓\nWaiting for redis-db\n✓\nWaiting for node-api\n✓\nHTTP Check (Port 8080)\n✓\nValidation Passed",
        stats: [
          { label: "Redis DB", value: "Running", tone: "text-success" },
          { label: "Node API", value: "Running", tone: "text-success" },
          { label: "Orchestration", value: "OK", tone: "text-success" },
        ],
      };
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

function compileFrontendCode(code, slug, title) {
  if (!code) return getFrontendSrcDoc(slug, title);
  try {
    const files = JSON.parse(code);
    if (files && typeof files === "object" && "index.html" in files) {
      let html = files["index.html"] || "";
      const css = files["index.css"] || "";
      const js = files["index.js"] || "";

      // Inject css
      const styleTag = `<style>\n${css}\n</style>`;
      if (html.includes("</head>")) {
        html = html.replace("</head>", `${styleTag}\n</head>`);
      } else {
        html = `${styleTag}\n${html}`;
      }

      // Inject js
      const scriptTag = `<script>\n${js}\n</script>`;
      if (html.includes("</body>")) {
        html = html.replace("</body>", `${scriptTag}\n</body>`);
      } else {
        html = `${html}\n${scriptTag}`;
      }

      return html;
    }
  } catch (e) {}

  return code;
}

export default EditorPage;
