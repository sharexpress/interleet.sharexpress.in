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

import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

import {
  FetchChallengeBySlug,
  selectChallengeDetail,
  selectDetailLoading,
  selectDetailError,
} from "@/redux/slices/challengesSlice";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { toast } from "sonner";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import {
  ArrowLeft,
  ArrowRight,
  Clock,
  Sparkles,
  Users,
  RefreshCw,
  Share2,
} from "lucide-react";

// ── Markdown renderer ────────────────────────────────────────────────────────

function parseInline(text) {
  const richRegex = /\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`|\*([^*]+)\*/g;
  const parts = [];
  let last = 0;
  let m;
  while ((m = richRegex.exec(text)) !== null) {
    if (m.index > last) parts.push(text.slice(last, m.index));
    if (m[1] !== undefined) {
      parts.push(
        <a key={m.index} href={m[2]} target="_blank" rel="noopener noreferrer"
          className="text-primary underline underline-offset-2 hover:opacity-80">
          {m[1]}
        </a>
      );
    } else if (m[3] !== undefined) {
      parts.push(<strong key={m.index} className="font-semibold text-foreground">{m[3]}</strong>);
    } else if (m[4] !== undefined) {
      parts.push(
        <code key={m.index} className="rounded bg-zinc-800/80 px-1.5 py-0.5 font-mono text-[11px] text-amber-500 font-semibold border border-zinc-700/50">
          {m[4]}
        </code>
      );
    } else if (m[5] !== undefined) {
      parts.push(<em key={m.index} className="italic">{m[5]}</em>);
    }
    last = richRegex.lastIndex;
  }
  if (last < text.length) parts.push(text.slice(last));
  return parts.length > 0 ? parts : text;
}

function renderMarkdown(text) {
  if (!text) return null;
  const lines = text.split('\n');

  // Pre-pass: group consecutive | lines into table blocks
  const blocks = [];
  let tableRows = [];
  const flushTable = () => {
    if (tableRows.length === 0) return;
    const [header, , ...body] = tableRows;
    blocks.push({ type: 'table', header, body });
    tableRows = [];
  };
  lines.forEach((line, idx) => {
    if (line.startsWith('|')) {
      tableRows.push(line);
    } else {
      flushTable();
      blocks.push({ type: 'line', content: line, idx });
    }
  });
  flushTable();

  return blocks.map((block, bIdx) => {
    if (block.type === 'table') {
      const parseRow = (row) => row.split('|').slice(1, -1).map(c => c.trim());
      const headerCells = parseRow(block.header);
      const bodyRows = (block.body || []).filter(r => !r.includes('---'));
      return (
        <div key={`tbl-${bIdx}`} className="my-3 overflow-x-auto rounded-md border border-border/40">
          <table className="w-full text-xs">
            <thead>
              <tr className="bg-card/30">
                {headerCells.map((cell, cIdx) => (
                  <th key={cIdx} className="px-3 py-2 text-left font-semibold text-foreground whitespace-nowrap">
                    {parseInline(cell)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {bodyRows.map((row, rIdx) => (
                <tr key={rIdx} className="border-t border-border/30 hover:bg-muted/10">
                  {parseRow(row).map((cell, cIdx) => (
                    <td key={cIdx} className="px-3 py-2 text-muted-foreground">
                      {parseInline(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    const { content: line, idx } = block;

    if (line.startsWith('#### ')) {
      return <h4 key={idx} className="mt-4 mb-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">{parseInline(line.slice(5))}</h4>;
    }
    if (line.startsWith('### ')) {
      return <h3 key={idx} className="mt-5 mb-2 text-sm font-semibold text-foreground">{parseInline(line.slice(4))}</h3>;
    }
    if (line.startsWith('## ')) {
      return <h2 key={idx} className="mt-6 mb-3 text-base font-bold text-foreground">{parseInline(line.slice(3))}</h2>;
    }
    if (line.startsWith('# ')) {
      return <h1 key={idx} className="mt-7 mb-4 text-lg font-extrabold text-foreground">{parseInline(line.slice(2))}</h1>;
    }
    if (line.trim().startsWith('- ')) {
      return (
        <ul key={idx} className="list-disc pl-5 my-1 text-muted-foreground">
          <li>{parseInline(line.trim().slice(2))}</li>
        </ul>
      );
    }
    if (line.trim() === '') {
      return <div key={idx} className="h-2" />;
    }
    return (
      <p key={idx} className="my-1.5 leading-relaxed text-muted-foreground">
        {parseInline(line)}
      </p>
    );
  });
}

// ── ChallengeDetail ──────────────────────────────────────────────────────────

function ChallengeDetail() {
  const { id: slug } = useParams();
  const dispatch = useDispatch();

  const c = useSelector(selectChallengeDetail(slug));
  const loading = useSelector(selectDetailLoading);
  const error = useSelector(selectDetailError);

  useEffect(() => {
    dispatch(FetchChallengeBySlug(slug));
  }, [dispatch, slug]);

  const handleShare = async () => {
    const challengeUrl = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${c?.title || 'Challenge'} - Interleet`,
          text: `Check out this coding challenge: "${c?.title || 'Challenge'}" on Interleet!`,
          url: challengeUrl,
        });
      } catch (err) {
        if (err.name !== "AbortError") {
          toast.error("Failed to share challenge.");
        }
      }
    } else {
      try {
        await navigator.clipboard.writeText(challengeUrl);
        toast.success("Challenge link copied to clipboard!");
      } catch (err) {
        toast.error("Failed to copy link.");
      }
    }
  };

  // ── Loading ──────────────────────────────────────────────────────────────
  if (loading && !c) {
    return (
      <AppShell>
        <div className="border-b border-border bg-card/10 px-4 py-6 md:px-8 space-y-4 animate-pulse">
          <div className="h-7 w-56 rounded bg-zinc-800/40" />
          <div className="h-4.5 w-96 rounded bg-zinc-800/20" />
        </div>
        <div className="max-w-4xl mx-auto px-4 py-8 md:px-8 animate-pulse space-y-4">
          <div className="h-[380px] rounded-xl border border-border bg-card/30 p-6 space-y-4">
            <div className="flex gap-2">
              <div className="h-5 w-16 rounded bg-zinc-800/40" />
              <div className="h-5 w-20 rounded bg-zinc-800/40" />
              <div className="h-5 w-16 rounded bg-zinc-800/20" />
            </div>
            <div className="h-6 w-32 rounded bg-zinc-800/40 mt-6" />
            <div className="space-y-2 pt-2">
              <div className="h-3.5 w-full rounded bg-zinc-800/20" />
              <div className="h-3.5 w-full rounded bg-zinc-800/20" />
              <div className="h-3.5 w-5/6 rounded bg-zinc-800/20" />
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  // ── Error ────────────────────────────────────────────────────────────────
  if (error && !c) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-center">
            <p className="text-sm text-destructive">{error}</p>
            <Button
              variant="outline"
              size="sm"
              onClick={() => dispatch(FetchChallengeBySlug(slug))}
            >
              <RefreshCw className="mr-2 h-4 w-4" /> Retry
            </Button>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/app/challenges">
                <ArrowLeft className="mr-1.5 h-4 w-4" /> Back to challenges
              </Link>
            </Button>
          </div>
        </div>
      </AppShell>
    );
  }

  if (!c) return null;

  return (
    <AppShell>
      <PageHeader
        title={c.title}
        description={c.summary}
        badge={c.domain}
        actions={
          <div className="flex flex-wrap items-center gap-2">
            <Button variant="outline" onClick={handleShare}>
              <Share2 className="mr-1.5 h-4 w-4" />
              Share
            </Button>
            <Button variant="outline" asChild>
              <Link to="/app/challenges">
                <ArrowLeft className="mr-1.5 h-4 w-4" />
                Back to challenges
              </Link>
            </Button>
            <Button asChild>
              <Link to={`/app/editor/${c.slug}`}>
                Open editor <ArrowRight className="ml-1.5 h-4 w-4" />
              </Link>
            </Button>
          </div>
        }
      />

      <div className="mx-auto max-w-4xl px-4 py-8 md:px-8 space-y-6">
        <Card className="border-border bg-card p-6 md:p-8">
          <div className="flex flex-wrap items-center gap-3">
            <DifficultyPill d={c.difficulty} />
            <DomainTag d={c.domain} />
            <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
              <Clock className="h-3.5 w-3.5" /> {c.minutes}m
            </span>
            <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
              <Sparkles className="h-3.5 w-3.5" /> {c.xp} XP
            </span>
            <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
              <Users className="h-3.5 w-3.5" /> {c.completion}% completion
            </span>
          </div>

          <h2 className="mt-6 text-xl font-semibold">Problem</h2>
          <div className="mt-3 max-w-none text-sm">
            <p className="text-base leading-relaxed text-foreground/90">{c.summary}</p>
            {c.description ? (
              <div className="mt-4">
                {renderMarkdown(c.description)}
              </div>
            ) : (
              <>
                <p className="text-muted-foreground mt-3">
                  You're given a service that needs to behave correctly under realistic production
                  constraints. Read the requirements carefully, propose an approach, and implement
                  it with the provided scaffolding. Your solution will be graded against a hidden
                  test suite plus a rubric for clarity, correctness, and tradeoffs.
                </p>
                <h3 className="text-base mt-4">Requirements</h3>
                <ul className="text-muted-foreground list-disc pl-5 my-1">
                  <li>Handle the documented happy path with correct behavior under load.</li>
                  <li>Degrade gracefully under partial failure (timeouts, retries).</li>
                  <li>Ship clear, justified code — comments only where intent isn't obvious.</li>
                </ul>
                <h3 className="text-base mt-4">Constraints</h3>
                <ul className="text-muted-foreground list-disc pl-5 my-1">
                  <li>p95 latency under 200ms at 1k rps</li>
                  <li>Memory budget: 256MB</li>
                  <li>No external network calls beyond the provided clients</li>
                </ul>
              </>
            )}
          </div>

          <div className="mt-8 pt-6 border-t border-border flex items-center justify-between">
            <Button variant="outline" asChild>
              <Link to="/app/challenges">
                <ArrowLeft className="mr-1.5 h-4 w-4" />
                Back to challenges
              </Link>
            </Button>
            <Button asChild size="lg">
              <Link to={`/app/editor/${c.slug}`}>
                Solve Challenge <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </Card>

        {c.hints && c.hints.length > 0 && (
          <Card className="border-border bg-card p-6">
            <h3 className="text-sm font-semibold">Hints</h3>
            <ol className="mt-3 list-inside list-decimal space-y-1 text-sm text-muted-foreground">
              {c.hints.map((hint, i) => (
                <li key={i}>{hint}</li>
              ))}
            </ol>
          </Card>
        )}
      </div>
    </AppShell>
  );
}

export default ChallengeDetail;
