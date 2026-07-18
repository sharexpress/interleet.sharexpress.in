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

import { memo } from "react";
import { Loader2, X, Check, AlertTriangle, Info, Bug } from "lucide-react";

import { useState } from "react";
import { ChevronRight, ChevronDown } from "lucide-react";

// ─── Log Type Styles ─────────────────────────────────────────────────────────
const TYPE_STYLES = {
  log:   { bg: "",                  text: "text-foreground/90",   border: "",                    icon: null,          label: null },
  info:  { bg: "bg-blue-950/30",    text: "text-blue-300",        border: "border-l-2 border-blue-500/50",  icon: Info,          label: "info"  },
  warn:  { bg: "bg-yellow-950/30",  text: "text-yellow-300",      border: "border-l-2 border-yellow-500/50", icon: AlertTriangle, label: "warn"  },
  error: { bg: "bg-red-950/30",     text: "text-red-300",         border: "border-l-2 border-red-500/50",   icon: X,             label: "error" },
  debug: { bg: "bg-zinc-900/40",    text: "text-zinc-400",        border: "border-l-2 border-zinc-600/40",  icon: Bug,           label: "debug" },
};

// ─── Interactive DevTools Value Renderer ────────────────────────────────────
function DOMElementToken({ data }) {
  const [expanded, setExpanded] = useState(false);
  const tag = data.tagName || "element";
  const idStr = data.id ? `#${data.id}` : "";
  const clsStr = data.className && typeof data.className === "string" ? `.${data.className.trim().replace(/\s+/g, ".")}` : "";

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
          <span className="ml-1 text-[9px] text-cyan-400/60">
            {expanded ? "▲" : "▼"}
          </span>
        )}
      </span>

      {expanded && data.outerHTML && (
        <div className="mt-1 rounded border border-cyan-800/40 bg-zinc-950 p-2 font-mono text-[10px] text-zinc-300 shadow-lg max-w-full overflow-x-auto whitespace-pre-wrap">
          <div className="text-[9px] font-semibold text-cyan-400/80 mb-1 border-b border-zinc-800 pb-0.5">DOM Inspector</div>
          <code>{data.outerHTML}</code>
        </div>
      )}
    </span>
  );
}

function DeepValueRenderer({ val, name, isLast = true }) {
  const [expanded, setExpanded] = useState(false);

  // Null & Undefined
  if (val === null || val === undefined) {
    return (
      <span className="font-mono">
        {name && <span className="text-zinc-400">{name}: </span>}
        <span className="text-zinc-500 italic">{String(val)}</span>
        {!isLast && <span className="text-zinc-600">, </span>}
      </span>
    );
  }

  // Primitive strings, numbers, booleans, bigint
  if (typeof val === "number") {
    return (
      <span className="font-mono">
        {name && <span className="text-zinc-300">{name}: </span>}
        <span className="text-emerald-400">{val}</span>
        {!isLast && <span className="text-zinc-600">, </span>}
      </span>
    );
  }

  if (typeof val === "boolean") {
    return (
      <span className="font-mono">
        {name && <span className="text-zinc-300">{name}: </span>}
        <span className="text-sky-400 font-semibold">{String(val)}</span>
        {!isLast && <span className="text-zinc-600">, </span>}
      </span>
    );
  }

  if (typeof val === "string") {
    return (
      <span className="font-mono">
        {name && <span className="text-zinc-300">{name}: </span>}
        <span className="text-amber-300">"{val}"</span>
        {!isLast && <span className="text-zinc-600">, </span>}
      </span>
    );
  }

  // Special Serialized Objects (__type)
  if (typeof val === "object" && val.__type) {
    if (val.__type === "DOMElement") {
      return (
        <span className="font-mono">
          {name && <span className="text-zinc-300">{name}: </span>}
          <DOMElementToken data={val} />
          {!isLast && <span className="text-zinc-600">, </span>}
        </span>
      );
    }
    if (val.__type === "Error") {
      return (
        <span className="font-mono text-red-400 bg-red-950/40 border border-red-900/50 px-1.5 py-0.5 rounded">
          {name && <span className="text-zinc-300">{name}: </span>}
          <span className="font-bold">{val.name || "Error"}: </span>
          <span>{val.message}</span>
        </span>
      );
    }
    if (val.__type === "Date") {
      return (
        <span className="font-mono">
          {name && <span className="text-zinc-300">{name}: </span>}
          <span className="text-purple-300 italic">{val.value}</span>
          {!isLast && <span className="text-zinc-600">, </span>}
        </span>
      );
    }
  }

  // Functions
  if (typeof val === "string" && val.startsWith("[Function")) {
    return (
      <span className="font-mono">
        {name && <span className="text-zinc-300">{name}: </span>}
        <span className="text-yellow-300/80 italic">{val}</span>
        {!isLast && <span className="text-zinc-600">, </span>}
      </span>
    );
  }

  // Arrays
  if (Array.isArray(val)) {
    if (val.length === 0) {
      return (
        <span className="font-mono text-zinc-400">
          {name && <span className="text-zinc-300">{name}: </span>}
          <span>[]</span>
          {!isLast && <span className="text-zinc-600">, </span>}
        </span>
      );
    }

    return (
      <div className="inline-flex flex-col font-mono align-baseline">
        <span
          onClick={() => setExpanded(!expanded)}
          className="cursor-pointer select-none text-zinc-300 hover:text-white inline-flex items-center gap-0.5"
        >
          {expanded ? <ChevronDown className="h-3 w-3 text-zinc-400" /> : <ChevronRight className="h-3 w-3 text-zinc-400" />}
          {name && <span>{name}: </span>}
          <span className="text-zinc-400">Array({val.length})</span>
          {!expanded && (
            <span className="text-zinc-500 text-[10px] ml-1">
              [{val.slice(0, 3).map(v => (typeof v === "object" ? "{...}" : String(v))).join(", ")}{val.length > 3 ? ", ..." : ""}]
            </span>
          )}
        </span>

        {expanded && (
          <div className="ml-4 pl-2 border-l border-zinc-800 my-1 space-y-0.5">
            {val.map((item, idx) => (
              <div key={idx}>
                <DeepValueRenderer val={item} name={String(idx)} isLast={idx === val.length - 1} />
              </div>
            ))}
          </div>
        )}
        {!isLast && !expanded && <span className="text-zinc-600">, </span>}
      </div>
    );
  }

  // General Objects
  if (typeof val === "object") {
    const keys = Object.keys(val);
    if (keys.length === 0) {
      return (
        <span className="font-mono text-zinc-400">
          {name && <span className="text-zinc-300">{name}: </span>}
          <span>{"{}"}</span>
          {!isLast && <span className="text-zinc-600">, </span>}
        </span>
      );
    }

    return (
      <div className="inline-flex flex-col font-mono align-baseline">
        <span
          onClick={() => setExpanded(!expanded)}
          className="cursor-pointer select-none text-zinc-300 hover:text-white inline-flex items-center gap-0.5"
        >
          {expanded ? <ChevronDown className="h-3 w-3 text-zinc-400" /> : <ChevronRight className="h-3 w-3 text-zinc-400" />}
          {name && <span>{name}: </span>}
          <span className="text-zinc-400">Object</span>
          {!expanded && (
            <span className="text-zinc-500 text-[10px] ml-1">
              {"{"} {keys.slice(0, 3).join(", ")}{keys.length > 3 ? ", ..." : ""} {"}"}
            </span>
          )}
        </span>

        {expanded && (
          <div className="ml-4 pl-2 border-l border-zinc-800 my-1 space-y-0.5">
            {keys.map((k, idx) => (
              <div key={k}>
                <DeepValueRenderer val={val[k]} name={k} isLast={idx === keys.length - 1} />
              </div>
            ))}
          </div>
        )}
        {!isLast && !expanded && <span className="text-zinc-600">, </span>}
      </div>
    );
  }

  return (
    <span className="font-mono text-zinc-200">
      {name && <span className="text-zinc-300">{name}: </span>}
      <span>{String(val)}</span>
      {!isLast && <span className="text-zinc-600">, </span>}
    </span>
  );
}

function renderArg(a, j) {
  return <DeepValueRenderer key={j} val={a} isLast={true} />;
}

// ─── Live Browser Console Entry (from iframe postMessage) ─────────────────────
const LiveEntry = memo(function LiveEntry({ entry, index }) {
  const type = entry.type || "log";
  const s = TYPE_STYLES[type] || TYPE_STYLES.log;
  const Icon = s.icon;
  const time = entry.ts ? new Date(entry.ts).toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" }) : null;

  return (
    <div className={`mb-1 flex items-start gap-2 rounded px-2 py-1 ${s.bg} ${s.border}`}>
      <span className="select-none text-[10px] text-muted-foreground/40 mt-0.5 w-5 shrink-0 text-right">
        {String(index + 1).padStart(2, "0")}
      </span>
      {Icon && <Icon className={`mt-0.5 h-3 w-3 shrink-0 ${s.text}`} />}
      <div className={`flex flex-wrap gap-1.5 flex-1 ${s.text}`}>
        {(entry.args || []).map((a, j) => renderArg(a, j))}
      </div>
      {time && (
        <span className="ml-auto text-[9px] text-muted-foreground/30 shrink-0 font-mono mt-0.5">
          {time}
        </span>
      )}
    </div>
  );
});

// ─── Legacy console output (JS/TS eval) ──────────────────────────────────────
const LegacyConsoleOutput = memo(function LegacyConsoleOutput({ result, isRunning }) {
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

// ─── Main ConsoleOutput: shows live browser logs for Frontend, legacy for others ─
const ConsoleOutput = memo(function ConsoleOutput({ result, isRunning, liveLogs, isFrontend }) {
  // Frontend domain: show real browser console logs via postMessage
  if (isFrontend) {
    const logs = liveLogs || [];
    const errorCount = logs.filter(e => e.type === "error").length;
    const warnCount = logs.filter(e => e.type === "warn").length;

    return (
      <div className="h-full overflow-auto font-mono text-[11px] leading-relaxed">
        {/* DevTools-style header bar */}
        <div className="sticky top-0 z-10 flex items-center gap-3 border-b border-border bg-background/90 px-3 py-1.5 text-[10px] text-muted-foreground backdrop-blur">
          <span className="font-semibold text-foreground/70">Console</span>
          <span className="ml-1">{logs.length} message{logs.length !== 1 ? "s" : ""}</span>
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
          <span className="ml-auto text-[9px] text-muted-foreground/40 italic">
            Live · iframe console
          </span>
        </div>

        <div className="p-2 space-y-0.5">
          {logs.length === 0 ? (
            <p className="p-2 text-muted-foreground/60 italic text-[11px]">
              No console output yet. Use <code className="text-amber-400">console.log()</code> in your JavaScript to see output here.
            </p>
          ) : (
            logs.map((entry, i) => <LiveEntry key={`${entry.ts}-${i}`} entry={entry} index={i} />)
          )}
        </div>
      </div>
    );
  }

  // Non-frontend: show legacy eval output
  return <LegacyConsoleOutput result={result} isRunning={isRunning} />;
});

const ObjToken = DeepValueRenderer;

export default ConsoleOutput;
export { ObjToken, DeepValueRenderer };
