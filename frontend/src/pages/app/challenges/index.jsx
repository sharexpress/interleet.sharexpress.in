import { useNavigate } from "react-router-dom";
import { useMemo, useState } from "react";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { ChallengeCard } from "@/components/domain/ChallengeCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Search, SlidersHorizontal, LayoutGrid, List as ListIcon } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue } from
"@/components/ui/select";
import { DOMAINS, challenges } from "@/lib/mock";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import { cn } from "@/lib/utils";



const difficulties = ["Easy", "Medium", "Hard", "Expert"];

function ChallengesPage() {
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [domain, setDomain] = useState("all");
  const [diff, setDiff] = useState("all");
  const [sort, setSort] = useState("popular");
  const [view, setView] = useState("grid");

  const openChallenge = (slug) => {
    navigate(`/app/challenges/${slug}`);
  };

  const filtered = useMemo(() => {
    let list = challenges.filter((c) => {
      if (domain !== "all" && c.domain !== domain) return false;
      if (diff !== "all" && c.difficulty !== diff) return false;
      if (q && !`${c.title} ${c.tags.join(" ")}`.toLowerCase().includes(q.toLowerCase()))
      return false;
      return true;
    });
    if (sort === "xp") list = [...list].sort((a, b) => b.xp - a.xp);
    if (sort === "time") list = [...list].sort((a, b) => a.minutes - b.minutes);
    if (sort === "completion") list = [...list].sort((a, b) => b.completion - a.completion);
    return list;
  }, [q, domain, diff, sort]);

  return (
    <AppShell>
      <PageHeader
        title="Challenges"
        description="Real-world engineering problems across the full stack."
        actions={
        <>
            <Button variant="outline">
              <SlidersHorizontal className="mr-1.5 h-4 w-4" /> Advanced filters
            </Button>
            <Button>Submit a challenge</Button>
          </>
        } />
      

      <div className="px-4 py-6 md:px-8">
        {/* Filters */}
        <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-3 md:flex-row md:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search challenges, tags, technologies…"
              className="h-9 border-transparent bg-background pl-9" />
            
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Select value={domain} onValueChange={(v) => setDomain(v)}>
              <SelectTrigger className="h-9 w-[150px]">
                <SelectValue placeholder="Domain" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All domains</SelectItem>
                {DOMAINS.map((d) =>
                <SelectItem key={d} value={d}>
                    {d}
                  </SelectItem>
                )}
              </SelectContent>
            </Select>
            <Select value={diff} onValueChange={(v) => setDiff(v)}>
              <SelectTrigger className="h-9 w-[140px]">
                <SelectValue placeholder="Difficulty" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Any difficulty</SelectItem>
                {difficulties.map((d) =>
                <SelectItem key={d} value={d}>
                    {d}
                  </SelectItem>
                )}
              </SelectContent>
            </Select>
            <Select value={sort} onValueChange={setSort}>
              <SelectTrigger className="h-9 w-[140px]">
                <SelectValue placeholder="Sort" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="popular">Most popular</SelectItem>
                <SelectItem value="xp">Most XP</SelectItem>
                <SelectItem value="time">Quickest</SelectItem>
                <SelectItem value="completion">Highest completion</SelectItem>
              </SelectContent>
            </Select>
            <div className="flex rounded-md border border-border p-0.5">
              <button
                onClick={() => setView("grid")}
                className={cn(
                  "rounded p-1.5",
                  view === "grid" ? "bg-accent text-foreground" : "text-muted-foreground"
                )}
                aria-label="Grid view">
                
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setView("list")}
                className={cn(
                  "rounded p-1.5",
                  view === "list" ? "bg-accent text-foreground" : "text-muted-foreground"
                )}
                aria-label="List view">
                
                <ListIcon className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          {DOMAINS.map((d) =>
          <button
            key={d}
            onClick={() => setDomain(domain === d ? "all" : d)}
            className={cn(
              "rounded-full border px-3 py-1 text-xs transition-colors",
              domain === d ?
              "border-primary/50 bg-primary/10 text-foreground" :
              "border-border text-muted-foreground hover:text-foreground"
            )}>
            
              {d}
            </button>
          )}
          <span className="ml-auto text-xs text-muted-foreground">
            {filtered.length} of {challenges.length}
          </span>
        </div>

        {view === "grid" ?
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((c) =>
          <ChallengeCard key={c.id} c={c} />
          )}
          </div> :

        <div className="mt-5 overflow-hidden rounded-xl border border-border bg-card">
            <table className="w-full text-xs md:text-sm">
              <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                <tr>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider md:px-4">Title</th>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider md:px-4">Domain</th>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider md:px-4">Difficulty</th>
                  <th className="hidden px-4 py-2 font-mono uppercase tracking-wider md:table-cell">
                    XP
                  </th>
                  <th className="hidden px-4 py-2 font-mono uppercase tracking-wider md:table-cell">
                    Time
                  </th>
                  <th className="hidden px-4 py-2 font-mono uppercase tracking-wider md:table-cell">
                    Done
                  </th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((c) =>
              <tr
                key={c.id}
                role="link"
                tabIndex={0}
                aria-label={`Open challenge ${c.title}`}
                onClick={() => openChallenge(c.slug)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    openChallenge(c.slug);
                  }
                }}
                className="cursor-pointer border-t border-border hover:bg-accent/40 focus-visible:bg-accent/40">
                
                    <td className="px-3 py-3 font-medium md:px-4">{c.title}</td>
                    <td className="px-3 py-3 md:px-4">
                      <DomainTag d={c.domain} />
                    </td>
                    <td className="px-3 py-3 md:px-4">
                      <DifficultyPill d={c.difficulty} />
                    </td>
                    <td className="hidden px-4 py-3 font-mono md:table-cell">{c.xp}</td>
                    <td className="hidden px-4 py-3 font-mono md:table-cell">{c.minutes}m</td>
                    <td className="hidden px-4 py-3 font-mono md:table-cell">{c.completion}%</td>
                  </tr>
              )}
              </tbody>
            </table>
          </div>
        }

        {filtered.length === 0 &&
        <div className="mt-10 rounded-xl border border-dashed border-border p-10 text-center">
            <Badge variant="outline" className="mx-auto">No matches</Badge>
            <p className="mt-3 text-sm text-muted-foreground">Try clearing some filters.</p>
          </div>
        }
      </div>
    </AppShell>);

}
export default ChallengesPage;
