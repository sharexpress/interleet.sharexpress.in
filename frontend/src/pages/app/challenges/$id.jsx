import { Link, useParams, useLoaderData } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import { challenges } from "@/lib/mock";
import { ArrowLeft, ArrowRight, Clock, Sparkles, Users, FileCode, Beaker } from "lucide-react";



function ChallengeDetail() {
  const c = useLoaderData();
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
        } />
      
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
              <p className="text-muted-foreground">
                You're given a service that needs to behave correctly under realistic production
                constraints. Read the requirements carefully, propose an approach, and implement it
                with the provided scaffolding. Your solution will be graded against a hidden test
                suite plus a rubric for clarity, correctness, and tradeoffs.
              </p>
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

          <Card className="border-border bg-card p-6">
            <h3 className="text-sm font-semibold">Example test</h3>
            <pre className="mt-3 overflow-x-auto rounded-md border border-border bg-background/60 p-4 font-mono text-xs leading-relaxed">
{`> POST /allow { userId: "u_123", action: "search" }
< 200 { allowed: true, remaining: 14 }

> POST /allow x16 (burst)
< first 15 → allowed: true
< next   1 → 429 Too Many Requests`}
            </pre>
          </Card>
        </div>

        <div className="space-y-4">
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold">Tags</h3>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {c.tags.map((t) =>
              <Badge key={t} variant="outline" className="font-mono text-[10px]">
                  {t}
                </Badge>
              )}
            </div>
          </Card>
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
    </AppShell>);

}
export const loader = ({ params }) => {
    const c = challenges.find((x) => x.slug === params.id);
    if (!c) throw new Error("Not found");
    return c;
  };
export default ChallengeDetail;
