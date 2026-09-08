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
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Play,
  Clock,
  Cpu,
  Layers,
  Sparkles,
  Loader2,
  RefreshCw
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SqlTableViewer } from "./SqlTableViewer";

export function SqlQueryOutputViewer({ execState, onRun, isRunning, isSubmitting }) {
  // Determine which mode/result is most recent
  const isSubmitMode = execState?.submitStatus !== "idle" && !!execState?.submitResult;
  const status = isSubmitMode ? execState.submitStatus : execState.runStatus;
  const result = isSubmitMode ? execState.submitResult : execState.runResult;
  const error = isSubmitMode ? execState.submitError : execState.runError;

  const [selectedCaseIdx, setSelectedCaseIdx] = useState(0);

  // 1. Loading State
  if (status === "loading" || isRunning || isSubmitting) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[220px] p-6 text-center space-y-3">
        <div className="relative">
          <Database className="h-10 w-10 text-orange-400 animate-pulse" />
          <Loader2 className="h-5 w-5 text-emerald-400 animate-spin absolute -bottom-1 -right-1" />
        </div>
        <div className="space-y-1">
          <p className="text-sm font-semibold text-zinc-200">Executing SQL in Isolated Sandbox...</p>
          <p className="text-xs text-zinc-500 font-mono">
            Parsing dialect, running against SQLite engine, comparing result set...
          </p>
        </div>
      </div>
    );
  }

  // 2. Failed / Network / Server Error
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
            <RefreshCw className="h-3.5 w-3.5" /> Retry Query Execution
          </Button>
        )}
      </div>
    );
  }

  // 3. Idle State (No execution yet)
  if (!result || status === "idle") {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[220px] p-6 text-center space-y-3">
        <div className="p-3 rounded-full bg-zinc-900/80 border border-zinc-800 text-orange-400">
          <Database className="h-8 w-8 opacity-80" />
        </div>
        <div className="space-y-1 max-w-sm">
          <p className="text-sm font-semibold text-zinc-200">No Query Executed Yet</p>
          <p className="text-xs text-zinc-500 leading-relaxed">
            Write your SQL statement in the editor and click <strong className="text-zinc-300">Run</strong> to execute it against the database and inspect your query output table.
          </p>
        </div>
        {onRun && (
          <Button size="sm" onClick={onRun} className="h-8 gap-1.5 text-xs bg-emerald-600 hover:bg-emerald-500 text-white">
            <Play className="h-3.5 w-3.5 fill-current" /> Run Query
          </Button>
        )}
      </div>
    );
  }

  // 4. Succeeded Result
  const {
    verdict,
    stdout,
    stderr,
    compile_output,
    time = 0,
    testcase_results = [],
    passed_testcases = 0,
    total_testcases = 1,
    score = 0
  } = result;

  const isAccepted = verdict === "ACCEPTED";
  const isWrongAnswer = verdict === "WRONG_ANSWER";
  const isSyntaxError = verdict === "COMPILATION_ERROR" || verdict === "RUNTIME_ERROR";

  const activeTc = testcase_results[selectedCaseIdx] || testcase_results[0] || {
    stdout: stdout,
    expected_output: "",
    passed: isAccepted,
    verdict: verdict
  };

  const actualOutput = activeTc.stdout || stdout || "";
  const expectedOutput = activeTc.expected_output || "";

  return (
    <div className="space-y-4 font-sans text-xs pb-4">
      {/* ── Verdict Status Header ────────────────────────────────────────────── */}
      <div
        className={`rounded-lg border p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
          isAccepted
            ? "border-emerald-500/40 bg-emerald-950/20 text-emerald-200"
            : isWrongAnswer
            ? "border-red-500/40 bg-red-950/20 text-red-200"
            : "border-amber-500/40 bg-amber-950/20 text-amber-200"
        }`}
      >
        <div className="flex items-center gap-2.5">
          {isAccepted ? (
            <CheckCircle2 className="h-6 w-6 text-emerald-400 shrink-0" />
          ) : isWrongAnswer ? (
            <XCircle className="h-6 w-6 text-red-400 shrink-0" />
          ) : (
            <AlertTriangle className="h-6 w-6 text-amber-400 shrink-0" />
          )}

          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm">
                {isAccepted
                  ? "CORRECT — Query Accepted!"
                  : isWrongAnswer
                  ? "WRONG ANSWER — Output Mismatch"
                  : "SQL QUERY ERROR"}
              </span>
              <Badge
                variant="outline"
                className={`text-[10px] font-mono font-bold ${
                  isAccepted
                    ? "border-emerald-500/50 bg-emerald-500/20 text-emerald-300"
                    : "border-red-500/50 bg-red-500/20 text-red-300"
                }`}
              >
                {verdict}
              </Badge>
            </div>
            <p className="text-[11px] opacity-80 mt-0.5">
              {isAccepted
                ? "Your query output matches the target table schema and all expected rows."
                : isWrongAnswer
                ? "Your query ran successfully, but the returned rows or columns differ from the target answer."
                : "SQLite syntax error or database execution exception. Check stderr below."}
            </p>
          </div>
        </div>

        {/* Quick Metrics */}
        <div className="flex items-center gap-3 text-xs font-mono shrink-0 sm:border-l sm:border-zinc-800 sm:pl-3">
          <div className="flex items-center gap-1" title="Execution Time">
            <Clock className="h-3.5 w-3.5 text-zinc-400" />
            <span>{(time * 1000).toFixed(0)} ms</span>
          </div>
          {total_testcases > 0 && (
            <div className="flex items-center gap-1" title="Passed Test Cases">
              <Layers className="h-3.5 w-3.5 text-zinc-400" />
              <span>
                {passed_testcases}/{total_testcases} passed
              </span>
            </div>
          )}
        </div>
      </div>

      {/* ── Testcase Selectors (if multiple) ─────────────────────────────────── */}
      {testcase_results.length > 1 && (
        <div className="flex items-center gap-1.5 border-b border-zinc-800/80 pb-2 overflow-x-auto">
          {testcase_results.map((tc, idx) => (
            <button
              key={tc.testcase_id || idx}
              onClick={() => setSelectedCaseIdx(idx)}
              className={`rounded px-2.5 py-1 text-xs font-mono font-semibold border transition-all flex items-center gap-1.5 ${
                selectedCaseIdx === idx
                  ? "bg-zinc-800 border-zinc-700 text-white"
                  : "border-transparent text-zinc-400 hover:text-white"
              }`}
            >
              {tc.passed ? (
                <CheckCircle2 className="h-3 w-3 text-emerald-400" />
              ) : (
                <XCircle className="h-3 w-3 text-red-400" />
              )}
              <span>{tc.name || `Case ${idx + 1}`}</span>
            </button>
          ))}
        </div>
      )}

      {/* ── Compile Error / Stderr (if any) ─────────────────────────────────── */}
      {(compile_output || stderr || activeTc.stderr) && (
        <div className="rounded-lg border border-red-500/40 bg-red-950/30 p-3 space-y-1">
          <p className="text-[10px] font-bold uppercase tracking-wider text-red-400">Database Engine Stderr</p>
          <pre className="font-mono text-xs text-red-200 whitespace-pre-wrap break-words">
            {compile_output || stderr || activeTc.stderr}
          </pre>
        </div>
      )}

      {/* ── Side-by-Side / Stacked Result Tables ────────────────────────────── */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        {/* Your Output */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-zinc-300 flex items-center gap-1.5">
              <span className={`h-2 w-2 rounded-full ${isAccepted ? "bg-emerald-400" : "bg-red-400"}`} />
              Your Query Output
            </span>
          </div>
          <SqlTableViewer
            data={actualOutput}
            title="Actual Result"
            badgeColor={isAccepted ? "emerald" : "orange"}
            emptyMessage="(Query returned zero rows)"
          />
        </div>

        {/* Expected Output */}
        {expectedOutput && !activeTc.hidden ? (
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-zinc-300 flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                Expected Target Output
              </span>
            </div>
            <SqlTableViewer
              data={expectedOutput}
              title="Target Output"
              badgeColor="emerald"
              emptyMessage="(Expected zero rows)"
            />
          </div>
        ) : activeTc.hidden ? (
          <div className="rounded-lg border border-zinc-800 bg-zinc-950/50 p-6 flex flex-col items-center justify-center text-center text-zinc-500 space-y-2">
            <Sparkles className="h-6 w-6 text-zinc-600" />
            <p className="text-xs font-semibold">Hidden Test Case</p>
            <p className="text-[11px] text-zinc-600 max-w-xs">
              Expected output for hidden benchmark cases is not revealed to prevent hardcoding.
            </p>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default SqlQueryOutputViewer;
