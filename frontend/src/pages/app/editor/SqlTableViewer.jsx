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

import React, { useState, useMemo } from "react";
import { Table, Copy, Check, Code, Layers } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

/**
 * SqlTableViewer
 * Renders SQL query output sets (array of row objects or serialized JSON)
 * into a rich, interactive, data-grid view with NULL pills, row numbers,
 * and JSON toggle.
 */
export function SqlTableViewer({
  data,
  title = "Query Result",
  badgeColor = "emerald",
  emptyMessage = "0 rows returned",
  maxRows = 50,
}) {
  const [viewMode, setViewMode] = useState("table"); // 'table' | 'json'
  const [copied, setCopied] = useState(false);

  // Parse data into rows array
  const { rows, columns, parseError, rawText } = useMemo(() => {
    if (!data) {
      return { rows: [], columns: [], parseError: null, rawText: "" };
    }

    let parsed = data;
    let rawStr = typeof data === "string" ? data : JSON.stringify(data, null, 2);

    if (typeof data === "string") {
      try {
        parsed = JSON.parse(data.trim());
      } catch (err) {
        return { rows: [], columns: [], parseError: data, rawText: data };
      }
    }

    if (!Array.isArray(parsed)) {
      if (typeof parsed === "object" && parsed !== null) {
        // If it's a single object or { columns, rows } format
        if (Array.isArray(parsed.rows) && Array.isArray(parsed.columns)) {
          const mappedRows = parsed.rows.map((r) => {
            const obj = {};
            parsed.columns.forEach((col, idx) => {
              obj[col] = r[idx];
            });
            return obj;
          });
          return { rows: mappedRows, columns: parsed.columns, parseError: null, rawText: rawStr };
        }
        parsed = [parsed];
      } else {
        return { rows: [], columns: [], parseError: String(parsed), rawText: rawStr };
      }
    }

    // Extract unique column names preserving first row's order
    const cols = [];
    const seen = new Set();
    parsed.forEach((row) => {
      if (row && typeof row === "object") {
        Object.keys(row).forEach((k) => {
          if (!seen.has(k)) {
            seen.add(k);
            cols.push(k);
          }
        });
      }
    });

    return { rows: parsed, columns: cols, parseError: null, rawText: rawStr };
  }, [data]);

  const handleCopy = () => {
    navigator.clipboard.writeText(rawText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (parseError) {
    return (
      <div className="rounded-md border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs">
        <div className="flex items-center justify-between mb-2">
          <span className="text-zinc-400 font-semibold">{title}</span>
          <Button variant="ghost" size="sm" onClick={handleCopy} className="h-6 px-2 text-[10px]">
            {copied ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
          </Button>
        </div>
        <pre className="text-zinc-300 whitespace-pre-wrap">{parseError}</pre>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-zinc-800/80 bg-zinc-950/70 overflow-hidden text-xs font-mono shadow-sm">
      {/* Header Toolbar */}
      <div className="flex items-center justify-between px-3 py-1.5 border-b border-zinc-800/60 bg-zinc-900/40">
        <div className="flex items-center gap-2">
          <Table className="h-3.5 w-3.5 text-zinc-400" />
          <span className="font-semibold text-zinc-200">{title}</span>
          <Badge
            variant="outline"
            className={`text-[9px] px-1.5 py-0 h-4 border-zinc-700 font-mono ${
              badgeColor === "emerald"
                ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/30"
                : "text-orange-400 bg-orange-500/10 border-orange-500/30"
            }`}
          >
            {rows.length} {rows.length === 1 ? "row" : "rows"}
          </Badge>
        </div>

        <div className="flex items-center gap-1.5">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setViewMode(viewMode === "table" ? "json" : "table")}
            className="h-6 px-2 text-[10px] text-zinc-400 hover:text-white"
            title={viewMode === "table" ? "View Raw JSON" : "View Table"}
          >
            {viewMode === "table" ? (
              <span className="flex items-center gap-1">
                <Code className="h-3 w-3" /> JSON
              </span>
            ) : (
              <span className="flex items-center gap-1">
                <Table className="h-3 w-3" /> Table
              </span>
            )}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="h-6 px-1.5 text-zinc-400 hover:text-white"
            title="Copy Result"
          >
            {copied ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
          </Button>
        </div>
      </div>

      {/* Body Content */}
      {viewMode === "json" ? (
        <pre className="p-3 text-[11px] text-zinc-300 overflow-x-auto max-h-[300px] whitespace-pre-wrap select-text">
          {rawText || "[]"}
        </pre>
      ) : rows.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-6 text-center text-zinc-500 text-xs">
          <Layers className="h-6 w-6 mb-1 opacity-40" />
          <p>{emptyMessage}</p>
        </div>
      ) : (
        <div className="overflow-x-auto max-h-[340px] select-text">
          <table className="w-full text-left text-[11px] font-mono border-collapse">
            <thead className="sticky top-0 bg-zinc-900 text-zinc-400 uppercase text-[10px] tracking-wider z-10 border-b border-zinc-800">
              <tr>
                <th className="px-2.5 py-1.5 w-10 text-zinc-600 font-normal select-none border-r border-zinc-800/40">
                  #
                </th>
                {columns.map((col) => (
                  <th key={col} className="px-3 py-1.5 font-semibold text-zinc-300 border-r border-zinc-800/40">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-900">
              {rows.slice(0, maxRows).map((row, idx) => (
                <tr key={idx} className="hover:bg-zinc-800/30 transition-colors">
                  <td className="px-2.5 py-1 text-zinc-600 font-mono text-[10px] select-none border-r border-zinc-800/40 bg-zinc-950/40">
                    {idx + 1}
                  </td>
                  {columns.map((col) => {
                    const val = row[col];
                    const isNull = val === null || val === undefined;
                    const isNum = typeof val === "number";

                    return (
                      <td
                        key={col}
                        className={`px-3 py-1.5 border-r border-zinc-800/20 max-w-[240px] truncate ${
                          isNum ? "text-right text-emerald-300/90" : "text-zinc-200"
                        }`}
                      >
                        {isNull ? (
                          <span className="italic text-zinc-500 bg-zinc-900 px-1 py-0.5 rounded text-[10px]">
                            NULL
                          </span>
                        ) : typeof val === "object" ? (
                          JSON.stringify(val)
                        ) : (
                          String(val)
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
          {rows.length > maxRows && (
            <div className="py-2 text-center text-zinc-500 text-[10px] border-t border-zinc-800 bg-zinc-900/20">
              + {rows.length - maxRows} more rows truncated for preview
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SqlTableViewer;
