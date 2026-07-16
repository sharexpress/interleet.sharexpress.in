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
import { Loader2, X, Check } from "lucide-react";

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

export default ConsoleOutput;
export { ObjToken };
