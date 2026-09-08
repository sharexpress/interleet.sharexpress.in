import React, { useState } from "react";
import { Copy, Check } from "lucide-react";

// ─── Inline Markdown Parser ──────────────────────────────────────────────────
export function parseInlineMarkdown(text) {
  if (!text || typeof text !== "string") return text;

  // Regex matches:
  // 1: `inline code`
  // 2: [label](url), 3: label, 4: url
  // 5: ***bold italic***, 6: content
  // 7: **bold**, 8: content
  // 9: *italic*, 10: content
  // 11: ~~strikethrough~~, 12: content
  const inlineRegex =
    /(`[^`]+`)|(\[([^\]]+)\]\(([^)]+)\))|(\*\*\*([^*]+)\*\*\*)|(\*\*([^*]+)\*\*)|(\*([^*]+)\*)|(~~([^~]+)~~)/g;

  let match;
  let lastIndex = 0;
  const elements = [];
  let keyCounter = 0;

  while ((match = inlineRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      elements.push(text.slice(lastIndex, match.index));
    }

    if (match[1]) {
      // Inline code
      const codeVal = match[1].slice(1, -1);
      elements.push(
        <code
          key={`code-${keyCounter++}`}
          className="rounded bg-zinc-800/90 px-1.5 py-0.5 font-mono text-[11px] text-amber-400 font-semibold border border-zinc-700/50 select-text"
        >
          {codeVal}
        </code>
      );
    } else if (match[2]) {
      // Hyperlink [text](url)
      const label = match[3];
      const url = match[4];
      elements.push(
        <a
          key={`lnk-${keyCounter++}`}
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary underline underline-offset-2 hover:opacity-80 font-medium transition-opacity"
        >
          {label}
        </a>
      );
    } else if (match[5]) {
      // Bold + Italic
      elements.push(
        <strong key={`bi-${keyCounter++}`} className="font-semibold text-foreground">
          <em className="italic">{match[6]}</em>
        </strong>
      );
    } else if (match[7]) {
      // Bold
      elements.push(
        <strong key={`b-${keyCounter++}`} className="font-semibold text-foreground">
          {match[8]}
        </strong>
      );
    } else if (match[9]) {
      // Italic
      elements.push(
        <em key={`i-${keyCounter++}`} className="italic text-zinc-300">
          {match[10]}
        </em>
      );
    } else if (match[11]) {
      // Strikethrough
      elements.push(
        <del key={`s-${keyCounter++}`} className="line-through text-muted-foreground/70">
          {match[12]}
        </del>
      );
    }

    lastIndex = inlineRegex.lastIndex;
  }

  if (lastIndex < text.length) {
    elements.push(text.slice(lastIndex));
  }

  return elements.length > 0 ? elements : text;
}

// ─── Code Snippet Block with Copy Action ─────────────────────────────────────
export function CodeSnippet({ code, lang }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (typeof navigator !== "undefined" && navigator.clipboard?.writeText) {
      navigator.clipboard
        .writeText(code)
        .then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 2000);
        })
        .catch(() => {});
    }
  };

  return (
    <div className="my-3.5 overflow-hidden rounded-lg border border-zinc-800/80 bg-zinc-950 shadow-sm">
      <div className="flex items-center justify-between border-b border-zinc-800/60 bg-zinc-900/60 px-3.5 py-1.5 text-[11px] font-mono text-zinc-400">
        <span className="uppercase tracking-wider font-semibold text-zinc-300 text-[10px]">
          {lang || "CODE"}
        </span>
        <button
          type="button"
          onClick={handleCopy}
          aria-label="Copy code block"
          className="flex items-center gap-1 rounded px-2 py-0.5 text-[10px] text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-zinc-200 cursor-pointer"
        >
          {copied ? (
            <>
              <Check className="h-3 w-3 text-emerald-400" />
              <span className="text-emerald-400 font-medium">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="h-3 w-3" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className="p-3.5 text-xs font-mono text-zinc-200 overflow-x-auto leading-relaxed whitespace-pre select-text">
        <code>{code}</code>
      </pre>
    </div>
  );
}

// ─── Block Parser ─────────────────────────────────────────────────────────────
export function parseMarkdownBlocks(text) {
  if (!text || typeof text !== "string") return [];
  const normalized = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  const lines = normalized.split("\n");
  const blocks = [];

  let inCodeBlock = false;
  let codeLang = "";
  let codeLines = [];

  let tableRows = [];
  let listItems = [];
  let listType = null; // 'ul' | 'ol'
  let quoteLines = [];

  const flushTable = () => {
    if (tableRows.length === 0) return;
    const headerLine = tableRows[0];
    const dividerLine = tableRows.length > 1 && tableRows[1].includes("---") ? tableRows[1] : null;
    const bodyLines = tableRows.slice(dividerLine ? 2 : 1);
    blocks.push({
      type: "table",
      header: headerLine,
      divider: dividerLine,
      body: bodyLines,
    });
    tableRows = [];
  };

  const flushList = () => {
    if (listItems.length === 0) return;
    blocks.push({
      type: listType,
      items: [...listItems],
    });
    listItems = [];
    listType = null;
  };

  const flushQuote = () => {
    if (quoteLines.length === 0) return;
    blocks.push({
      type: "quote",
      lines: [...quoteLines],
    });
    quoteLines = [];
  };

  const flushAll = () => {
    flushTable();
    flushList();
    flushQuote();
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // ── Code Block boundary (```lang ... ```) ──
    if (trimmed.startsWith("```")) {
      if (inCodeBlock) {
        blocks.push({
          type: "code",
          lang: codeLang,
          code: codeLines.join("\n"),
        });
        inCodeBlock = false;
        codeLang = "";
        codeLines = [];
      } else {
        flushAll();
        inCodeBlock = true;
        codeLang = trimmed.slice(3).trim();
        codeLines = [];
      }
      continue;
    }

    if (inCodeBlock) {
      codeLines.push(line);
      continue;
    }

    // ── Horizontal Rule (---, ***, ___) ──────────
    if (/^(\-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
      flushAll();
      blocks.push({ type: "hr" });
      continue;
    }

    // ── Table Row (| ... |) ───────────────────────
    if (trimmed.startsWith("|")) {
      flushList();
      flushQuote();
      tableRows.push(trimmed);
      continue;
    } else {
      flushTable();
    }

    // ── Blockquote (> ...) ────────────────────────
    if (trimmed.startsWith(">")) {
      flushList();
      quoteLines.push(trimmed.replace(/^>\s?/, ""));
      continue;
    } else {
      flushQuote();
    }

    // ── Headings (# to ######) ────────────────────
    if (trimmed.startsWith("#")) {
      flushAll();
      const hMatch = trimmed.match(/^(#{1,6})\s+(.*)$/);
      if (hMatch) {
        const level = hMatch[1].length;
        const content = hMatch[2];
        blocks.push({ type: "heading", level, content });
        continue;
      }
    }

    // ── Unordered List (- item, * item, + item) ───
    const ulMatch = line.match(/^(\s*)([-*+])\s+(.*)$/);
    if (ulMatch) {
      flushTable();
      flushQuote();
      if (listType && listType !== "ul") flushList();
      listType = "ul";
      listItems.push(ulMatch[3]);
      continue;
    }

    // ── Ordered List (1. item, 2. item) ───────────
    const olMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/);
    if (olMatch) {
      flushTable();
      flushQuote();
      if (listType && listType !== "ol") flushList();
      listType = "ol";
      listItems.push(olMatch[3]);
      continue;
    }

    flushList();

    // ── Empty Line ────────────────────────────────
    if (trimmed === "") {
      blocks.push({ type: "empty" });
      continue;
    }

    // ── Normal Paragraph ──────────────────────────
    blocks.push({ type: "p", content: line });
  }

  // Trailing flushes
  if (inCodeBlock) {
    blocks.push({
      type: "code",
      lang: codeLang,
      code: codeLines.join("\n"),
    });
  }
  flushAll();

  return blocks;
}

// ─── Table Block Component ───────────────────────────────────────────────────
function TableBlock({ block, blockKey }) {
  const parseRow = (row) =>
    row
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((c) => c.trim());

  const headerCells = parseRow(block.header);
  const dividerCells = block.divider ? parseRow(block.divider) : [];
  const alignments = dividerCells.map((cell) => {
    const c = cell.trim();
    if (c.startsWith(":") && c.endsWith(":")) return "text-center";
    if (c.endsWith(":")) return "text-right";
    return "text-left";
  });

  return (
    <div key={blockKey} className="my-3.5 overflow-x-auto rounded-lg border border-border/60 bg-card/30 shadow-xs">
      <table className="w-full border-collapse text-xs">
        <thead>
          <tr className="border-b border-border/50 bg-muted/40 font-semibold text-foreground">
            {headerCells.map((cell, cIdx) => {
              const align = alignments[cIdx] || "text-left";
              return (
                <th
                  key={cIdx}
                  className={`px-3.5 py-2.5 ${align} font-semibold text-foreground whitespace-nowrap tracking-wide`}
                >
                  {parseInlineMarkdown(cell)}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          {block.body.map((row, rIdx) => {
            const cells = parseRow(row);
            return (
              <tr
                key={rIdx}
                className="border-b border-border/30 last:border-b-0 hover:bg-muted/20 transition-colors"
              >
                {cells.map((cell, cIdx) => {
                  const align = alignments[cIdx] || "text-left";
                  return (
                    <td key={cIdx} className={`px-3.5 py-2 text-muted-foreground ${align}`}>
                      {parseInlineMarkdown(cell)}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ─── Main Component: MarkdownRenderer ─────────────────────────────────────────
export default function MarkdownRenderer({ content, className = "" }) {
  if (!content || typeof content !== "string") return null;

  try {
    const blocks = parseMarkdownBlocks(content);

    return (
      <div className={`markdown-body space-y-1 text-xs text-muted-foreground ${className}`}>
        {blocks.map((block, idx) => {
          const key = `blk-${idx}`;

          if (block.type === "code") {
            return <CodeSnippet key={key} code={block.code} lang={block.lang} />;
          }

          if (block.type === "table") {
            return <TableBlock key={key} block={block} blockKey={key} />;
          }

          if (block.type === "hr") {
            return <hr key={key} className="my-4 border-border/60" />;
          }

          if (block.type === "heading") {
            const { level, content: hContent } = block;
            if (level === 1) {
              return (
                <h1 key={key} className="mt-6 mb-3 text-lg font-bold text-foreground tracking-tight">
                  {parseInlineMarkdown(hContent)}
                </h1>
              );
            }
            if (level === 2) {
              return (
                <h2 key={key} className="mt-5 mb-2.5 text-base font-bold text-foreground tracking-tight">
                  {parseInlineMarkdown(hContent)}
                </h2>
              );
            }
            if (level === 3) {
              return (
                <h3 key={key} className="mt-4 mb-2 text-sm font-semibold text-foreground">
                  {parseInlineMarkdown(hContent)}
                </h3>
              );
            }
            if (level === 4) {
              return (
                <h4 key={key} className="mt-3.5 mb-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {parseInlineMarkdown(hContent)}
                </h4>
              );
            }
            return (
              <h5 key={key} className="mt-3 mb-1 text-xs font-semibold text-muted-foreground">
                {parseInlineMarkdown(hContent)}
              </h5>
            );
          }

          if (block.type === "ul") {
            return (
              <ul key={key} className="my-2 list-disc list-outside pl-5 space-y-1 text-xs text-muted-foreground">
                {block.items.map((it, iIdx) => (
                  <li key={iIdx} className="leading-relaxed">
                    {parseInlineMarkdown(it)}
                  </li>
                ))}
              </ul>
            );
          }

          if (block.type === "ol") {
            return (
              <ol key={key} className="my-2 list-decimal list-outside pl-5 space-y-1 text-xs text-muted-foreground">
                {block.items.map((it, iIdx) => (
                  <li key={iIdx} className="leading-relaxed">
                    {parseInlineMarkdown(it)}
                  </li>
                ))}
              </ol>
            );
          }

          if (block.type === "quote") {
            return (
              <blockquote
                key={key}
                className="my-3 border-l-2 border-primary/60 bg-primary/5 px-3.5 py-2 rounded-r text-xs text-muted-foreground italic space-y-1"
              >
                {block.lines.map((ln, qIdx) => (
                  <p key={qIdx} className="leading-relaxed">
                    {parseInlineMarkdown(ln)}
                  </p>
                ))}
              </blockquote>
            );
          }

          if (block.type === "empty") {
            return <div key={key} className="h-2" />;
          }

          // Paragraph
          return (
            <p key={key} className="my-1.5 text-xs text-muted-foreground leading-relaxed">
              {parseInlineMarkdown(block.content)}
            </p>
          );
        })}
      </div>
    );
  } catch (err) {
    console.error("Failed to render markdown:", err);
    return <div className="whitespace-pre-wrap text-xs text-muted-foreground">{content}</div>;
  }
}

// ─── Backward-compatible Helper ───────────────────────────────────────────────
export function renderMarkdown(content) {
  if (!content) return null;
  return <MarkdownRenderer content={content} />;
}
