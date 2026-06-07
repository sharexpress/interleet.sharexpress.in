import React from "react";
import { Loader2, Check, AlertTriangle, X, Clock, Database } from "lucide-react";
import TestCaseResultCard from "./TestCaseResultCard";

/**
 * ExecutionResult — full LeetCode-style execution result panel.
 *
 * For "Run" (runStatus / runResult):
 *   Shows per-test-case pass/fail cards with actual vs expected.
 *
 * For "Submit" (submitStatus / submitResult):
 *   Shows aggregate verdict, score, runtime, memory, per-testcase breakdown.
 *
 * Props:
 *   mode:         'run' | 'submit'
 *   status:       'idle' | 'loading' | 'succeeded' | 'failed'
 *   result:       ExecutionResult object from backend
 *   error:        string error message
 */
export default function ExecutionResult({ mode = 'run', status, result, error }) {
  if (!status || status === 'idle') return null;

  // ── Loading ────────────────────────────────────────────────────────────────
  if (status === 'loading') {
    const label = mode === 'submit'
      ? 'Submitting & judging all test cases… (may take up to 60s)'
      : 'Running sample test cases…';
    return (
      <div className="flex items-center gap-3 text-slate-400 text-sm py-2">
        <Loader2 className="h-4 w-4 animate-spin shrink-0" />
        <span>{label}</span>
      </div>
    );
  }

  // ── Failed (network/server/security error) ─────────────────────────────────
  if (status === 'failed') {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-400 font-mono">
        <div className="flex items-start gap-2">
          <X className="h-4 w-4 mt-0.5 shrink-0" />
          <pre className="whitespace-pre-wrap break-words">{error || 'Execution failed'}</pre>
        </div>
      </div>
    );
  }

  // ── Succeeded ──────────────────────────────────────────────────────────────
  if (status === 'succeeded' && result) {
    const {
      verdict,
      success,
      stdout,
      stderr,
      compile_output,
      time,
      memory,
      testcase_results = [],
      passed_testcases,
      total_testcases,
      score,
    } = result;

    const accepted = verdict === 'ACCEPTED';
    const verdictLabel = verdict?.replace(/_/g, ' ') || (success ? 'OK' : 'Error');
    const VerdictIcon = accepted ? Check : AlertTriangle;
    const verdictColor = accepted
      ? 'text-emerald-400'
      : verdict === 'WRONG_ANSWER' ? 'text-red-400'
      : verdict === 'TIME_LIMIT_EXCEEDED' ? 'text-yellow-400'
      : verdict === 'COMPILATION_ERROR' ? 'text-orange-400'
      : 'text-red-400';

    // Score fraction text
    const scoreText = (total_testcases > 0)
      ? `${passed_testcases}/${total_testcases} tests passed`
      : null;

    return (
      <div className="space-y-3">
        {/* Verdict header */}
        <div className="flex items-center gap-3">
          <div className={`flex items-center gap-1.5 font-bold text-base ${verdictColor}`}>
            <VerdictIcon className="h-5 w-5 shrink-0" />
            {verdictLabel}
          </div>
          {scoreText && (
            <span className="text-xs text-slate-500">{scoreText}</span>
          )}
          {mode === 'submit' && score !== undefined && (
            <span className="ml-auto text-xs font-mono text-slate-400">
              Score: {score.toFixed(0)}%
            </span>
          )}
        </div>

        {/* Runtime + Memory */}
        {(time !== undefined || memory !== undefined) && (
          <div className="flex items-center gap-4 text-xs text-slate-400">
            {time !== undefined && (
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {(time * 1000).toFixed(0)} ms
              </span>
            )}
            {memory !== undefined && (
              <span className="flex items-center gap-1">
                <Database className="h-3 w-3" />
                {memory.toFixed(1)} MB
              </span>
            )}
          </div>
        )}

        {/* Compile error (no testcase breakdown) */}
        {compile_output && (
          <div className="rounded-lg border border-orange-500/30 bg-orange-500/10 p-3">
            <p className="text-[10px] uppercase tracking-wider text-orange-400 mb-1">Compile Error</p>
            <pre className="text-orange-300 text-xs whitespace-pre-wrap break-words">{compile_output}</pre>
          </div>
        )}

        {/* Per-testcase breakdown */}
        {testcase_results.length > 0 ? (
          <div className="space-y-2">
            {testcase_results.map((tc, i) => (
              <TestCaseResultCard
                key={tc.testcase_id || i}
                result={tc}
                index={i}
              />
            ))}
          </div>
        ) : (
          /* Fallback: raw stdout/stderr when no testcase breakdown */
          <div className="space-y-2">
            {stdout && (
              <div className="rounded-lg border border-white/10 bg-white/5 p-3">
                <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Output</p>
                <pre className="text-slate-200 text-xs whitespace-pre-wrap break-words">{stdout}</pre>
              </div>
            )}
            {stderr && (
              <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-3">
                <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Stderr</p>
                <pre className="text-red-300 text-xs whitespace-pre-wrap break-words">{stderr}</pre>
              </div>
            )}
            {!stdout && !stderr && !compile_output && (
              <p className="text-xs text-slate-500 italic">(no output)</p>
            )}
          </div>
        )}
      </div>
    );
  }

  return null;
}
