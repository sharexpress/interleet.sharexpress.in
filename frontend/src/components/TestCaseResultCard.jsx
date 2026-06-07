import React, { useState } from "react";
import { Check, X, Clock, MemoryStick, ChevronDown, ChevronRight } from "lucide-react";

/**
 * Single test case result card — LeetCode style.
 * Props: { result: TestCaseResult, index: number }
 */
export default function TestCaseResultCard({ result, index }) {
  const [open, setOpen] = useState(!result.passed); // auto-expand failures

  const passed = result.passed;
  const verdict = result.verdict?.replace(/_/g, " ") || (passed ? "PASSED" : "FAILED");

  const border = passed
    ? "border-emerald-500/30 bg-emerald-500/5"
    : "border-red-500/30 bg-red-500/5";
  const iconColor = passed ? "text-emerald-400" : "text-red-400";

  return (
    <div className={`rounded-lg border ${border} overflow-hidden text-sm font-mono`}>
      {/* Header */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center gap-2 px-3 py-2 text-left hover:bg-white/5 transition-colors"
      >
        {passed
          ? <Check className={`h-3.5 w-3.5 shrink-0 ${iconColor}`} />
          : <X     className={`h-3.5 w-3.5 shrink-0 ${iconColor}`} />
        }
        <span className="text-xs text-slate-300 font-semibold">
          {result.name || `Test ${index + 1}`}
        </span>
        <span className={`ml-1 text-[10px] uppercase tracking-wide ${iconColor}`}>
          {verdict}
        </span>
        {result.wall_time_ms > 0 && (
          <span className="ml-auto text-[10px] text-slate-500">
            {result.wall_time_ms.toFixed(0)} ms
          </span>
        )}
        <span className="text-slate-600 ml-1">
          {open ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        </span>
      </button>

      {/* Detail rows */}
      {open && (
        <div className="border-t border-white/5 px-3 py-2 space-y-2">
          {/* Input */}
          {result.stdin !== undefined && result.stdin !== null && (
            <div>
              <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Input</p>
              <pre className="text-slate-300 whitespace-pre-wrap break-words text-xs">
                {result.stdin || "(empty)"}
              </pre>
            </div>
          )}

          {/* Expected */}
          {!result.hidden && result.expected_output !== undefined && (
            <div>
              <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Expected Output</p>
              <pre className="text-emerald-300 whitespace-pre-wrap break-words text-xs">
                {result.expected_output || "(empty)"}
              </pre>
            </div>
          )}

          {/* Actual */}
          {!result.hidden && result.stdout !== undefined && (
            <div>
              <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Your Output</p>
              <pre className={`whitespace-pre-wrap break-words text-xs ${passed ? "text-emerald-300" : "text-red-300"}`}>
                {result.stdout || "(empty)"}
              </pre>
            </div>
          )}

          {/* Stderr */}
          {result.stderr && (
            <div>
              <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Stderr</p>
              <pre className="text-yellow-300 whitespace-pre-wrap break-words text-xs">{result.stderr}</pre>
            </div>
          )}

          {/* Compile output */}
          {result.compile_output && (
            <div>
              <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Compile Error</p>
              <pre className="text-red-300 whitespace-pre-wrap break-words text-xs">{result.compile_output}</pre>
            </div>
          )}

          {/* Hidden notice */}
          {result.hidden && (
            <p className="text-[10px] text-slate-500 italic">
              This is a hidden test case. Output is not shown.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
