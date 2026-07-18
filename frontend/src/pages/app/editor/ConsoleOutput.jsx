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

import { memo, useState, useCallback } from "react";
import { Loader2, X, Check, AlertTriangle, Info, Bug, ChevronRight, ChevronDown } from "lucide-react";

// ─── Log Type Styles ──────────────────────────────────────────────────────────
const TYPE_STYLES = {
  log:   { bg: "",                 text: "text-zinc-200",    border: "",                               icon: null,          label: null  },
  info:  { bg: "bg-blue-950/30",   text: "text-blue-300",   border: "border-l-2 border-blue-500/50",  icon: Info,          label: "info"  },
  warn:  { bg: "bg-yellow-950/30", text: "text-yellow-300", border: "border-l-2 border-yellow-500/50",icon: AlertTriangle, label: "warn"  },
  error: { bg: "bg-red-950/30",    text: "text-red-300",    border: "border-l-2 border-red-500/50",   icon: X,             label: "error" },
  debug: { bg: "bg-zinc-900/40",   text: "text-zinc-400",   border: "border-l-2 border-zinc-600/40",  icon: Bug,           label: "debug" },
};

// ─── DOM Element Inspector Token ──────────────────────────────────────────────
function DOMElementToken({ data }) {
  const [expanded, setExpanded] = useState(false);
  const tag = data.tagName || "element";
  const idStr = data.id ? `#${data.id}` : "";
  const clsStr =
    data.className && typeof data.className === "string"
      ? `.${data.className.trim().replace(/\s+/g, ".")}`
      : "";

  return (
    <span className="inline-flex flex-col font-mono text-[11px] align-baseline">
      <span
        onClick={() => setExpanded(!expanded)}
        className="cursor-pointer select-none rounded bg-cyan-950/60 hover:bg-cyan-900/60 px-1.5 py-0.5 text-cyan-300 border border-cyan-800/40 inline-flex items-center gap-1 transition-colors"
        title="Click to inspect HTML"
      >
        <span className="text-purple-400 font-semibold">&lt;{tag}</span>
        {idStr && <span className="text-amber-300 font-semibold">{idStr}</span>}
        {clsStr && <span className="text-teal-300">{clsStr}</span>}
        <span className="text-purple-400 font-semibold">&gt;</span>
        {data.outerHTML && (
          <span className="ml-1 text-[9px] text-cyan-400/60">{expanded ? "▲" : "▼"}</span>
        )}
      </span>
      {expanded && data.outerHTML && (
        <div className="mt-1 rounded border border-cyan-800/40 bg-zinc-950 p-2 font-mono text-[10px] text-zinc-300 shadow-lg max-w-full overflow-x-auto whitespace-pre-wrap">
          <div className="text-[9px] font-semibold text-cyan-400/80 mb-1 border-b border-zinc-800 pb-0.5">
            DOM Inspector
          </div>
          <code>{data.outerHTML}</code>
        </div>
      )}
    </span>
  );
}

// ─── Collapsed one-line preview (like Chrome DevTools) ────────────────────────
function collapsedPreview(val, depth) {
  if (depth === undefined) depth = 0;
  if (val === null || val === undefined) return String(val);
  if (typeof val === "boolean" || typeof val === "number") return String(val);
  if (typeof val === "bigint") return String(val) + "n";
  if (typeof val === "string") {
    const s = val.slice(0, 40);
    return "'" + s + (val.length > 40 ? "…" : "") + "'";
  }
  if (typeof val !== "object") return String(val);
  if (val.__type === "DOMElement") return "<" + (val.tagName || "el") + (val.id ? "#" + val.id : "") + ">";
  if (val.__type === "Error") return (val.name || "Error") + ": " + val.message;
  if (val.__type === "Date") return val.value;
  if (Array.isArray(val)) {
    if (depth > 0) return "[…]";
    const inner = val.slice(0, 4).map(function (v) { return collapsedPreview(v, depth + 1); }).join(", ");
    return "(" + val.length + ") [" + inner + (val.length > 4 ? ", …" : "") + "]";
  }
  if (depth > 0) return "{…}";
  const keys = Object.keys(val);
  const inner = keys.slice(0, 3).map(function (k) { return k + ": " + collapsedPreview(val[k], depth + 1); }).join(", ");
  return "{" + inner + (keys.length > 3 ? ", …" : "") + "}";
}

// ─── Chrome-style vertical tree renderer ─────────────────────────────────────
function DeepValueRenderer({ val, name, depth }) {
  if (depth === undefined) depth = 0;
  const [expanded, setExpanded] = useState(false);

  // null / undefined
  if (val === null || val === undefined) {
    return (
      <span className="font-mono text-[11px]">
        {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
        <span className="text-zinc-500 italic">{String(val)}</span>
      </span>
    );
  }

  // number
  if (typeof val === "number" || typeof val === "bigint") {
    return (
      <span className="font-mono text-[11px]">
        {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
        <span className="text-cyan-300">{String(val)}</span>
      </span>
    );
  }

  // boolean
  if (typeof val === "boolean") {
    return (
      <span className="font-mono text-[11px]">
        {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
        <span className="text-cyan-300">{String(val)}</span>
      </span>
    );
  }

  // string — also catches "[Function: foo]" labels from serializer
  if (typeof val === "string") {
    if (val.startsWith("[Function")) {
      return (
        <span className="font-mono text-[11px]">
          {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
          <span className="text-zinc-400 italic">{val}</span>
        </span>
      );
    }
    return (
      <span className="font-mono text-[11px]">
        {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
        <span className="text-amber-300">'{val}'</span>
      </span>
    );
  }

  // Special serialized __type objects
  if (typeof val === "object" && val.__type) {
    if (val.__type === "DOMElement") {
      return (
        <span className="font-mono text-[11px]">
          {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
          <DOMElementToken data={val} />
        </span>
      );
    }
    if (val.__type === "Error") {
      return (
        <span className="font-mono text-[11px] text-red-400">
          {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
          <span className="font-bold">{val.name || "Error"}:&nbsp;</span>
          <span>{val.message}</span>
        </span>
      );
    }
    if (val.__type === "Date") {
      return (
        <span className="font-mono text-[11px]">
          {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
          <span className="text-purple-300 italic">{val.value}</span>
        </span>
      );
    }
  }

  // Array — vertical expand
  if (Array.isArray(val)) {
    if (val.length === 0) {
      return (
        <span className="font-mono text-[11px]">
          {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
          <span className="text-zinc-400">[]</span>
        </span>
      );
    }
    const preview = collapsedPreview(val);
    return (
      <div className="font-mono text-[11px] w-full">
        <div
          className="flex items-start gap-0.5 cursor-pointer select-none group"
          onClick={function () { setExpanded(function (e) { return !e; }); }}
        >
          <span className="mt-px text-zinc-600 group-hover:text-zinc-300 transition-colors w-3 shrink-0 text-center leading-none">
            {expanded ? "▼" : "▶"}
          </span>
          <span className="flex-1 break-all">
            {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
            {expanded
              ? <span className="text-zinc-400">[</span>
              : <span className="text-zinc-400 hover:text-zinc-200 transition-colors">{preview}</span>
            }
          </span>
        </div>
        {expanded && (
          <>
            <div className="flex">
              <div className="ml-[5px] mr-2 border-l border-zinc-700/50 self-stretch shrink-0" />
              <div className="flex-1 space-y-[1px] py-[1px]">
                {val.map(function (item, idx) {
                  return (
                    <div key={idx}>
                      <DeepValueRenderer val={item} name={idx} depth={depth + 1} />
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="pl-3 text-zinc-400">]</div>
          </>
        )}
      </div>
    );
  }

  // Object — vertical expand
  if (typeof val === "object") {
    const keys = Object.keys(val);
    if (keys.length === 0) {
      return (
        <span className="font-mono text-[11px]">
          {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
          <span className="text-zinc-400">{"{}"}</span>
        </span>
      );
    }
    const preview = collapsedPreview(val);
    return (
      <div className="font-mono text-[11px] w-full">
        <div
          className="flex items-start gap-0.5 cursor-pointer select-none group"
          onClick={function () { setExpanded(function (e) { return !e; }); }}
        >
          <span className="mt-px text-zinc-600 group-hover:text-zinc-300 transition-colors w-3 shrink-0 text-center leading-none">
            {expanded ? "▼" : "▶"}
          </span>
          <span className="flex-1 break-all">
            {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
            {expanded
              ? <span className="text-zinc-400">{"{"}</span>
              : <span className="text-zinc-400 hover:text-zinc-200 transition-colors">{preview}</span>
            }
          </span>
        </div>
        {expanded && (
          <>
            <div className="flex">
              <div className="ml-[5px] mr-2 border-l border-zinc-700/50 self-stretch shrink-0" />
              <div className="flex-1 space-y-[1px] py-[1px]">
                {keys.map(function (k) {
                  return (
                    <div key={k}>
                      <DeepValueRenderer val={val[k]} name={k} depth={depth + 1} />
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="pl-3 text-zinc-400">{"}"}</div>
          </>
        )}
      </div>
    );
  }

  // Fallback
  return (
    <span className="font-mono text-[11px] text-zinc-200">
      {name !== undefined && <span className="text-zinc-500">{name}:&nbsp;</span>}
      <span>{String(val)}</span>
    </span>
  );
}

// ─── Live Browser Console Entry (from iframe postMessage) ────────────────────
const LiveEntry = memo(function LiveEntry({ entry, index }) {
  const type = entry.type || "log";
  const s = TYPE_STYLES[type] || TYPE_STYLES.log;
  const Icon = s.icon;
  const time = entry.ts
    ? new Date(entry.ts).toLocaleTimeString("en-US", {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })
    : null;
  const args = entry.args || [];

  return (
    <div className={`border-b border-zinc-800/40 px-2 py-1 ${s.bg} ${s.border} hover:bg-zinc-800/20 transition-colors`}>
      {/* Row header */}
      <div className="flex items-center gap-2 mb-0.5">
        <span className="select-none text-[10px] text-muted-foreground/30 w-5 shrink-0 text-right font-mono">
          {String(index + 1).padStart(2, "0")}
        </span>
        {Icon && <Icon className={`h-3 w-3 shrink-0 ${s.text}`} />}
        {time && (
          <span className="ml-auto text-[9px] text-muted-foreground/25 shrink-0 font-mono">{time}</span>
        )}
      </div>
      {/* Each arg on its own line — objects expand vertically */}
      <div className={`ml-7 space-y-0.5 ${s.text}`}>
        {args.map(function (a, j) {
          return (
            <div key={j} className="w-full min-w-0">
              <DeepValueRenderer val={a} />
            </div>
          );
        })}
      </div>
    </div>
  );
});

// ─── Legacy console output (JS/TS eval mode) ─────────────────────────────────
const LegacyConsoleOutput = memo(function LegacyConsoleOutput({ result, isRunning }) {
  if (isRunning) {
    return (
      <div className="flex items-center gap-2 p-3 font-mono text-xs text-muted-foreground">
        <Loader2 className="h-3.5 w-3.5 animate-spin" /> Running...
      </div>
    );
  }
  if (!result) {
    return (
      <p className="p-3 font-mono text-[11px] text-muted-foreground">
        Press <span className="text-foreground">Run</span> to execute. Output appears here as structured objects.
      </p>
    );
  }

  const { logs, errors, ms } = result;
  return (
    <div className="max-h-64 overflow-auto p-3 font-mono text-[11px] leading-relaxed">
      <div className="mb-2 flex items-center gap-3 border-b border-border pb-1.5 text-[10px] text-muted-foreground">
        <span>{logs.length} log{logs.length !== 1 ? "s" : ""}</span>
        {errors.length > 0 && (
          <span className="text-destructive">{errors.length} error{errors.length !== 1 ? "s" : ""}</span>
        )}
        <span className="ml-auto">{ms} ms</span>
      </div>
      {logs.map((args, i) => (
        <div key={i} className="mb-1.5 flex items-start gap-2">
          <span className="select-none text-[10px] text-muted-foreground/40">
            {String(i + 1).padStart(2, "0")}
          </span>
          <div className="flex flex-col gap-0.5 flex-1">
            {args.map((a, j) =>
              typeof a === "object" && a !== null ? (
                <DeepValueRenderer key={j} val={a} />
              ) : (
                <span key={j} className="text-foreground/90">{String(a)}</span>
              )
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

// ─── Main export: live browser console for Frontend, legacy for others ────────
const ConsoleOutput = memo(function ConsoleOutput({ result, isRunning, liveLogs, isFrontend, onClear }) {
  if (isFrontend) {
    const logs = liveLogs || [];
    const errorCount = logs.filter((e) => e.type === "error").length;
    const warnCount  = logs.filter((e) => e.type === "warn").length;

    return (
      <div className="h-full flex flex-col overflow-hidden font-mono text-[11px] leading-relaxed">
        {/* DevTools-style header */}
        <div className="sticky top-0 z-10 flex items-center gap-2 border-b border-border bg-background/90 px-2 py-1.5 text-[10px] text-muted-foreground backdrop-blur shrink-0">
          {/* Clear console button — exactly like Chrome */}
          <button
            onClick={onClear}
            title="Clear console (Ctrl+L)"
            className="flex items-center justify-center rounded p-0.5 hover:bg-zinc-700/60 text-zinc-500 hover:text-zinc-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
            </svg>
          </button>
          <div className="w-px h-3 bg-zinc-700/60 shrink-0" />
          <span className="font-semibold text-foreground/60">Console</span>
          <span>{logs.length} message{logs.length !== 1 ? "s" : ""}</span>
          {errorCount > 0 && (
            <span className="flex items-center gap-1 text-red-400">
              <X className="h-3 w-3" /> {errorCount}
            </span>
          )}
          {warnCount > 0 && (
            <span className="flex items-center gap-1 text-yellow-400">
              <AlertTriangle className="h-3 w-3" /> {warnCount}
            </span>
          )}
          <span className="ml-auto text-[9px] text-muted-foreground/40 italic">Live · iframe</span>
        </div>

        <div className="py-1 overflow-auto flex-1">
          {logs.length === 0 ? (
            <p className="p-3 text-muted-foreground/60 italic text-[11px]">
              No console output yet. Use <code className="text-amber-400">console.log()</code> in your JavaScript to see output here.
            </p>
          ) : (
            logs.map((entry, i) => (
              <LiveEntry key={`${entry.ts}-${i}`} entry={entry} index={i} />
            ))
          )}
        </div>
      </div>
    );
  }

  return <LegacyConsoleOutput result={result} isRunning={isRunning} />;
});

const ObjToken = DeepValueRenderer;

export default ConsoleOutput;
export { ObjToken, DeepValueRenderer };
