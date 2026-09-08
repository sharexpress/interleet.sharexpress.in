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

import React, { useState } from "react";
import {
  Database,
  Play,
  Clock,
  Rows,
  AlertTriangle,
  XCircle,
  Loader2,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { SqlTableViewer } from "./SqlTableViewer";

/**
 * SqlQueryOutputViewer — shows only the raw output of the user's SQL query.
 *
 * Architecture:
 *   - Output tab  → shows this component (raw query result, no comparison)
 *   - Result tab  → shows ExecutionResult (comparison + verdict)
 */
export function SqlQueryOutputViewer({ execState, onRun, isRunning, isSubmitting }) {
  const [selectedCaseIdx, setSelectedCaseIdx] = useState(0);

  // Pick the most recent execution (run > submit, whichever ran last)
  const hasRun    = execState?.runStatus    !== "idle";
  const hasSubmit = execState?.submitStatus !== "idle";
  const useSubmit = hasSubmit && !hasRun;

  const status = useSubmit ? execState?.submitStatus : execState?.runStatus;
  const result = useSubmit ? execState?.submitResult : execState?.runResult;
  const error  = useSubmit ? execState?.submitError  : execState?.runError;

  // ── 1. Loading ──────────────────────────────────────────────────────────────
  if (status === "loading" || isRunning || isSubmitting) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[220px] p-6 text-center space-y-3">
        <div className="relative">
          <Database className="h-10 w-10 text-orange-400 animate-pulse" />
          <Loader2 className="h-5 w-5 text-emerald-400 animate-spin absolute -bottom-1 -right-1" />
        </div>
        <div className="space-y-1">
          <p className="text-sm font-semibold text-zinc-200">Running SQL Query…</p>
          <p className="text-xs text-zinc-500 font-mono">
            Parsing dialect · executing in SQLite sandbox · fetching rows…
          </p>
        </div>
      </div>
    );
  }

  // ── 2. Network / Server error (no result at all) ────────────────────────────
  if (status === "failed" && !result) {
    return (
      <div className="p-4 space-y-3 font-sans text-xs">
        <div className="rounded-lg border border-red-500/40 bg-red-950/20 p-4 text-red-300">
          <div className="flex items-start gap-2.5">
            <XCircle className="h-5 w-5 text-red-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="font-bold text-sm text-red-300">Query Execution Failed</p>
              <pre className="font-mono text-xs text-red-200/90 whitespace-pre-wrap">
                {error || "An unexpected error occurred while executing the SQL query."}
              </pre>
            </div>
          </div>
        </div>
        {onRun && (
          <Button size="sm" onClick={onRun} className="gap-1.5 text-xs bg-orange-600 hover:bg-orange-500">
            <RefreshCw className="h-3.5 w-3.5" /> Retry
          </Button>
        )}
      </div>
    );
  }

  // ── 3. Idle — nothing has been executed yet ─────────────────────────────────
  if (!result || status === "idle") {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[220px] p-6 text-center space-y-3">
        <div className="p-3 rounded-full bg-zinc-900/80 border border-zinc-800 text-orange-400">
          <Database className="h-8 w-8 opacity-80" />
        </div>
        <div className="space-y-1 max-w-sm">
          <p className="text-sm font-semibold text-zinc-200">Ready to Execute SQL</p>
          <p className="text-xs text-zinc-500 leading-relaxed">
            Write your query in the editor and click{" "}
            <strong className="text-zinc-300">Run</strong> — the result table will appear here.
          </p>
        </div>
        {onRun && (
          <Button
            size="sm"
            onClick={onRun}
            className="h-8 gap-1.5 text-xs bg-emerald-600 hover:bg-emerald-500 text-white"
          >
            <Play className="h-3.5 w-3.5 fill-current" /> Run Query
          </Button>
        )}
      </div>
    );
  }

  // ── 4. Result — show raw query output only, no comparison ──────────────────
  const {
    stdout,
    stderr,
    compile_output,
    time = 0,
    testcase_results = [],
  } = result;

  // If multiple test cases, pick the active one's stdout
  const activeTc = testcase_results[selectedCaseIdx] || testcase_results[0] || null;
  const queryOutput = activeTc?.stdout ?? stdout ?? "";
  const queryStderr = activeTc?.stderr ?? stderr ?? compile_output ?? "";

  // Count rows from the JSON output (best-effort)
  let rowCount = null;
  try {
    const parsed = JSON.parse(queryOutput);
    if (Array.isArray(parsed)) rowCount = parsed.length;
  } catch (_) { /* ignore */ }

  const hasError = !!queryStderr;

  return (
    <div className="space-y-3 font-sans text-xs pb-4">
      {/* ── Toolbar: execution metrics ─────────────────────────────────────── */}
      <div className="flex items-center gap-3 px-0.5 py-1 border-b border-zinc-800/80 text-zinc-400 font-mono">
        <div className="flex items-center gap-1.5" title="Execution Time">
          <Clock className="h-3.5 w-3.5" />
          <span>{(time * 1000).toFixed(0)} ms</span>
        </div>
        {rowCount !== null && (
          <div className="flex items-center gap-1.5" title="Rows Returned">
            <Rows className="h-3.5 w-3.5" />
            <span>{rowCount} {rowCount === 1 ? "row" : "rows"}</span>
          </div>
        )}
        {hasError && (
          <div className="flex items-center gap-1.5 text-amber-400 ml-auto">
            <AlertTriangle className="h-3.5 w-3.5" />
            <span className="font-sans font-semibold">SQL Error</span>
          </div>
        )}
      </div>

      {/* ── Test-case tabs (only when multiple test cases ran) ──────────────── */}
      {testcase_results.length > 1 && (
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
          {testcase_results.map((tc, idx) => (
            <button
              key={tc.testcase_id || idx}
              onClick={() => setSelectedCaseIdx(idx)}
              className={`rounded px-2.5 py-1 text-xs font-mono border transition-all ${
                selectedCaseIdx === idx
                  ? "bg-zinc-800 border-zinc-700 text-white"
                  : "border-transparent text-zinc-500 hover:text-zinc-200"
              }`}
            >
              {tc.name || `Case ${idx + 1}`}
            </button>
          ))}
        </div>
      )}

      {/* ── SQL Engine Stderr / Syntax Error ──────────────────────────────── */}
      {hasError && (
        <div className="rounded-lg border border-amber-500/40 bg-amber-950/20 p-3 space-y-1">
          <p className="text-[10px] font-bold uppercase tracking-wider text-amber-400">
            Database Engine Error
          </p>
          <pre className="font-mono text-xs text-amber-200/90 whitespace-pre-wrap break-words">
            {queryStderr}
          </pre>
        </div>
      )}

      {/* ── Query Result Table ─────────────────────────────────────────────── */}
      {!hasError && (
        <SqlTableViewer
          data={queryOutput}
          title="Query Output"
          badgeColor="orange"
          emptyMessage="(Query returned zero rows)"
        />
      )}
    </div>
  );
}

export default SqlQueryOutputViewer;
