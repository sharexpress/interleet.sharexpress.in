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
import { Badge } from "@/components/ui/badge";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import {
  ArrowLeft,
  ArrowRight,
  Clock,
  Sparkles,
  Users,
  FileCode,
  Beaker,
  RefreshCw,
} from "lucide-react";

function ChallengeDetail() {
  const { id: slug } = useParams();
  const dispatch = useDispatch();

  const c = useSelector(selectChallengeDetail(slug));
  const loading = useSelector(selectDetailLoading);
  const error = useSelector(selectDetailError);

  useEffect(() => {
    dispatch(FetchChallengeBySlug(slug));
  }, [dispatch, slug]);

  // ── Loading ──────────────────────────────────────────────────────────────
  if (loading && !c) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-muted-foreground">
            <div className="h-8 w-8 animate-spin rounded-full border border-zinc-700 border-t-primary" />
            <p className="text-sm">Loading challenge…</p>
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

      <div className="grid gap-6 px-4 py-6 md:grid-cols-3 md:px-8">
        <div className="space-y-4 md:col-span-2">
          <Card className="border-border bg-card p-6">
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
            <h2 className="mt-5 text-lg font-semibold">Problem</h2>
            <div className="prose prose-invert mt-3 max-w-none text-sm text-foreground/85">
              <p>{c.summary}</p>
              {c.description ? (
                <p className="text-muted-foreground">{c.description}</p>
              ) : (
                <p className="text-muted-foreground">
                  You're given a service that needs to behave correctly under realistic production
                  constraints. Read the requirements carefully, propose an approach, and implement
                  it with the provided scaffolding. Your solution will be graded against a hidden
                  test suite plus a rubric for clarity, correctness, and tradeoffs.
                </p>
              )}
              <h3 className="text-base">Requirements</h3>
              <ul className="text-muted-foreground">
                <li>Handle the documented happy path with correct behavior under load.</li>
                <li>Degrade gracefully under partial failure (timeouts, retries).</li>
                <li>Ship clear, justified code — comments only where intent isn't obvious.</li>
              </ul>
              <h3 className="text-base">Constraints</h3>
              <ul className="text-muted-foreground">
                <li>p95 latency under 200ms at 1k rps</li>
                <li>Memory budget: 256MB</li>
                <li>No external network calls beyond the provided clients</li>
              </ul>
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

          {c.test_cases && c.test_cases.filter((t) => !t.hidden).length > 0 && (
            <Card className="border-border bg-card p-6">
              <h3 className="text-sm font-semibold">Example tests</h3>
              <div className="mt-3 space-y-3">
                {c.test_cases
                  .filter((t) => !t.hidden)
                  .map((t) => (
                    <div
                      key={t.id}
                      className="rounded-md border border-border bg-background/60 p-3"
                    >
                      <p className="mb-2 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                        {t.name}
                      </p>
                      <div className="grid gap-2 sm:grid-cols-2">
                        {t.stdin && (
                          <div>
                            <p className="mb-1 text-[10px] text-muted-foreground">Input</p>
                            <pre className="overflow-x-auto font-mono text-xs text-foreground/85">
                              {t.stdin}
                            </pre>
                          </div>
                        )}
                        {t.expected_output && (
                          <div>
                            <p className="mb-1 text-[10px] text-muted-foreground">
                              Expected output
                            </p>
                            <pre className="overflow-x-auto font-mono text-xs text-foreground/85">
                              {t.expected_output}
                            </pre>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
              </div>
            </Card>
          )}
        </div>

        <div className="space-y-4">
          {c.tags && c.tags.length > 0 && (
            <Card className="border-border bg-card p-5">
              <h3 className="text-sm font-semibold">Tags</h3>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {c.tags.map((t) => (
                  <Badge key={t} variant="outline" className="font-mono text-[10px]">
                    {t}
                  </Badge>
                ))}
              </div>
            </Card>
          )}
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold">Resources</h3>
            <ul className="mt-3 space-y-2 text-sm">
              <li className="flex items-center gap-2 text-foreground/85">
                <FileCode className="h-4 w-4 text-primary" />
                Starter scaffold (Node / TS)
              </li>
              <li className="flex items-center gap-2 text-foreground/85">
                <Beaker className="h-4 w-4 text-primary" />
                Local test runner
              </li>
            </ul>
          </Card>
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold">Discussion</h3>
            <p className="mt-2 text-xs text-muted-foreground">
              328 engineers discussing tradeoffs. Open after you submit.
            </p>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}

export default ChallengeDetail;
