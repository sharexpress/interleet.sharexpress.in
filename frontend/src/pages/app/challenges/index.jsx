import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

import {
  FetchChallenges,
  selectChallengesList,
  selectChallengesDomains,
  selectChallengesTotal,
  selectChallengesLoading,
  selectChallengesError,
} from "@/redux/slices/challengesSlice";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { ChallengeCard } from "@/components/domain/ChallengeCard";
import UpgradeModal from "@/components/UpgradeModal";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Search, SlidersHorizontal, LayoutGrid, List as ListIcon, RefreshCw, Lock } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import { cn } from "@/lib/utils";

const DIFFICULTIES = ["Easy", "Medium", "Hard", "Expert"];

function ChallengesPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { user } = useSelector((state) => state.user);
  const [upgradeOpen, setUpgradeOpen] = useState(false);

  const items = useSelector(selectChallengesList);
  const domains = useSelector(selectChallengesDomains);
  const total = useSelector(selectChallengesTotal);
  const loading = useSelector(selectChallengesLoading);
  const error = useSelector(selectChallengesError);

  const [q, setQ] = useState("");
  const [domain, setDomain] = useState("all");
  const [diff, setDiff] = useState("all");
  const [sort, setSort] = useState("popular");
  const [view, setView] = useState("grid");

  // Advanced filters state
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [premiumFilter, setPremiumFilter] = useState("all"); // "all", "free", "premium"
  const [timeFilter, setTimeFilter] = useState("all"); // "all", "quick", "medium", "extended"
  const [beginnerFilter, setBeginnerFilter] = useState("all"); // "all", "beginner"

  // Displayed items state to support local filtering or backend results
  const [displayedItems, setDisplayedItems] = useState([]);

  const [debouncedQ, setDebouncedQ] = useState("");

  // Debounce the query input state
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQ(q);
    }, 300);
    return () => clearTimeout(handler);
  }, [q]);

  // Sync displayed items locally based on query, domain, difficulty, and advanced filters
  useEffect(() => {
    let filtered = [...items];

    // 1. Search Query
    const term = q.trim().toLowerCase();
    if (term) {
      filtered = filtered.filter((c) => {
        const haystack = `${c.title} ${(c.tags || []).join(" ")} ${c.summary || ""}`.toLowerCase();
        return haystack.includes(term);
      });
    }

    // 2. Domain matching
    if (domain !== "all") {
      filtered = filtered.filter((c) => c.domain === domain);
    }

    // 3. Difficulty matching
    if (diff !== "all") {
      filtered = filtered.filter((c) => c.difficulty === diff);
    }

    // 4. Premium/Free filter
    if (premiumFilter === "free") {
      filtered = filtered.filter((c) => !c.is_premium);
    } else if (premiumFilter === "premium") {
      filtered = filtered.filter((c) => c.is_premium);
    }

    // 5. Estimated Time duration filter (resilient for minutes / estimated_time_minutes keys)
    if (timeFilter === "quick") {
      filtered = filtered.filter((c) => (c.minutes || c.estimated_time_minutes || 0) < 45);
    } else if (timeFilter === "medium") {
      filtered = filtered.filter((c) => {
        const m = c.minutes || c.estimated_time_minutes || 0;
        return m >= 45 && m <= 90;
      });
    } else if (timeFilter === "extended") {
      filtered = filtered.filter((c) => (c.minutes || c.estimated_time_minutes || 0) > 90);
    }

    // 6. Target Audience filter
    if (beginnerFilter === "beginner") {
      filtered = filtered.filter((c) => c.recommended_for_beginner || c.difficulty === "Easy");
    }

    setDisplayedItems(filtered);
  }, [items, q, domain, diff, premiumFilter, timeFilter, beginnerFilter]);

  // Fetch challenges from backend only when parameters or debounced query changes
  useEffect(() => {
    const term = debouncedQ.trim().toLowerCase();

    // Prevent API request if matching items are already loaded locally
    if (term) {
      const localMatches = items.filter((c) => {
        const haystack = `${c.title} ${(c.tags || []).join(" ")} ${c.summary || ""}`.toLowerCase();
        return haystack.includes(term);
      });
      if (localMatches.length > 0) {
        return;
      }
    }

    dispatch(
      FetchChallenges({
        ...(term && { q: term }),
        ...(domain !== "all" && { domain }),
        ...(diff !== "all" && { difficulty: diff }),
        sort,
      })
    );
  }, [dispatch, debouncedQ, domain, diff, sort]);

  const openChallenge = (c) => {
    if (c.is_premium && !user?.is_premium) {
      setUpgradeOpen(true);
    } else {
      navigate(`/app/challenges/${c.slug}`);
    }
  };

  // ── Loading state ──────────────────────────────────────────────────────────
  if (loading && displayedItems.length === 0) {
    return (
      <AppShell>
        <PageHeader
          title="Challenges"
          description="Real-world engineering problems across the full stack."
        />
        <div className="px-4 py-6 md:px-8 space-y-6">
          {/* Filters bar skeleton */}
          <div className="h-16 w-full rounded-xl border border-border bg-card/40 animate-pulse" />
          
          {/* Domain pills skeleton */}
          <div className="flex flex-wrap gap-2 animate-pulse">
            <div className="h-7 w-20 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-24 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-16 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-28 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-20 rounded-full bg-zinc-800/40" />
          </div>

          {/* Cards grid skeleton */}
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-[140px] rounded-xl border border-border bg-card/30 p-5 flex flex-col justify-between animate-pulse">
                <div className="space-y-2">
                  <div className="h-4 w-3/4 rounded bg-zinc-800/40" />
                  <div className="h-3 w-1/2 rounded bg-zinc-800/20" />
                </div>
                <div className="flex justify-between items-center mt-4">
                  <div className="h-5 w-16 rounded bg-zinc-800/25" />
                  <div className="h-5 w-12 rounded bg-zinc-800/25" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </AppShell>
    );
  }

  // ── Error state ────────────────────────────────────────────────────────────
  if (error && displayedItems.length === 0) {
    return (
      <AppShell>
        <PageHeader
          title="Challenges"
          description="Real-world engineering problems across the full stack."
        />
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3 text-center">
            <p className="text-sm text-destructive">{error}</p>
            <Button variant="outline" size="sm" onClick={() => dispatch(FetchChallenges({ sort }))}>
              <RefreshCw className="mr-2 h-4 w-4" /> Retry
            </Button>
          </div>
        </div>
      </AppShell>
    );
  }

  const activeFiltersCount = 
    (premiumFilter !== "all" ? 1 : 0) + 
    (timeFilter !== "all" ? 1 : 0) + 
    (beginnerFilter !== "all" ? 1 : 0);

  return (
    <AppShell>
      <PageHeader
        title="Challenges"
        description="Real-world engineering problems across the full stack."
        actions={
          <>
            <Button 
              variant={showAdvanced ? "secondary" : "outline"}
              onClick={() => setShowAdvanced(!showAdvanced)}
              className={cn(showAdvanced && "bg-accent text-foreground")}
            >
              <SlidersHorizontal className="mr-1.5 h-4 w-4" /> 
              Advanced filters
              {activeFiltersCount > 0 && (
                <span className="ml-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] text-primary-foreground font-semibold">
                  {activeFiltersCount}
                </span>
              )}
            </Button>
            <Button>Submit a challenge</Button>
          </>
        }
      />

      <div className="px-4 py-6 md:px-8">
        {/* Filters bar */}
        <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-3 md:flex-row md:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search challenges, tags, technologies…"
              className="h-9 border-transparent bg-background pl-9"
            />
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Select value={domain} onValueChange={setDomain}>
              <SelectTrigger className="h-9 w-[150px]">
                <SelectValue placeholder="Domain" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All domains</SelectItem>
                {domains.map((d) => (
                  <SelectItem key={d} value={d}>
                    {d}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={diff} onValueChange={setDiff}>
              <SelectTrigger className="h-9 w-[140px]">
                <SelectValue placeholder="Difficulty" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Any difficulty</SelectItem>
                {DIFFICULTIES.map((d) => (
                  <SelectItem key={d} value={d}>
                    {d}
                  </SelectItem>
                ))}
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
                  view === "grid" ? "bg-accent text-foreground" : "text-muted-foreground",
                )}
                aria-label="Grid view"
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setView("list")}
                className={cn(
                  "rounded p-1.5",
                  view === "list" ? "bg-accent text-foreground" : "text-muted-foreground",
                )}
                aria-label="List view"
              >
                <ListIcon className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Collapsible Advanced Filters Panel */}
        {showAdvanced && (
          <div className="mt-3 grid gap-4 rounded-xl border border-border bg-card/60 p-4 sm:grid-cols-3 relative animate-in slide-in-from-top-4 duration-200">
            <div className="space-y-1.5">
              <label className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">Access level</label>
              <Select value={premiumFilter} onValueChange={setPremiumFilter}>
                <SelectTrigger className="h-9 w-full bg-background/50 border-border hover:bg-background/80">
                  <SelectValue placeholder="All Access" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Access</SelectItem>
                  <SelectItem value="free">Free Only</SelectItem>
                  <SelectItem value="premium">Premium Only</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-1.5">
              <label className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">Estimated Time</label>
              <Select value={timeFilter} onValueChange={setTimeFilter}>
                <SelectTrigger className="h-9 w-full bg-background/50 border-border hover:bg-background/80">
                  <SelectValue placeholder="Any duration" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Any duration</SelectItem>
                  <SelectItem value="quick">Quick (&lt; 45 mins)</SelectItem>
                  <SelectItem value="medium">Medium (45 - 90 mins)</SelectItem>
                  <SelectItem value="extended">Extended (&gt; 90 mins)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-1.5 flex flex-col justify-between">
              <div className="space-y-1.5">
                <label className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">Target Audience</label>
                <Select value={beginnerFilter} onValueChange={setBeginnerFilter}>
                  <SelectTrigger className="h-9 w-full bg-background/50 border-border hover:bg-background/80">
                    <SelectValue placeholder="All Skill Levels" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Skill Levels</SelectItem>
                    <SelectItem value="beginner">Beginner Friendly</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              {activeFiltersCount > 0 && (
                <button 
                  onClick={() => {
                    setPremiumFilter("all");
                    setTimeFilter("all");
                    setBeginnerFilter("all");
                  }}
                  className="mt-2 text-right text-xs text-primary hover:underline self-end"
                >
                  Reset Advanced Filters
                </button>
              )}
            </div>
          </div>
        )}

        {/* Domain pills */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          {domains.map((d) => (
            <button
              key={d}
              onClick={() => setDomain(domain === d ? "all" : d)}
              className={cn(
                "rounded-full border px-3 py-1 text-xs transition-colors",
                domain === d
                  ? "border-primary/50 bg-primary/10 text-foreground"
                  : "border-border text-muted-foreground hover:text-foreground",
              )}
            >
              {d}
            </button>
          ))}
          <span className="ml-auto text-xs text-muted-foreground">
            {loading ? "Loading…" : `${displayedItems.length} of ${total}`}
          </span>
        </div>

        {/* Grid view */}
        {view === "grid" && (
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {displayedItems.map((c) => (
              <ChallengeCard key={c.id || c.slug} c={c} />
            ))}
          </div>
        )}

        {/* List view */}
        {view === "list" && (
          <div className="mt-5 overflow-hidden rounded-xl border border-border bg-card">
            <table className="w-full text-xs md:text-sm">
              <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                <tr>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider md:px-4">Title</th>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider md:px-4">Domain</th>
                  <th className="px-3 py-2 font-mono uppercase tracking-wider md:px-4">
                    Difficulty
                  </th>
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
                {displayedItems.map((c) => (
                  <tr
                    key={c.id || c.slug}
                    role="link"
                    tabIndex={0}
                    aria-label={`Open challenge ${c.title}`}
                    onClick={() => openChallenge(c)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        openChallenge(c);
                      }
                    }}
                    className="cursor-pointer border-t border-border hover:bg-accent/40 focus-visible:bg-accent/40"
                  >
                    <td className="px-3 py-3 font-medium md:px-4">
                      <div className="flex items-center gap-1.5">
                        {c.is_premium && <Lock className="h-3.5 w-3.5 text-[#FF6500] flex-shrink-0" />}
                        <span>{c.title}</span>
                      </div>
                    </td>
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
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Empty state */}
        {!loading && displayedItems.length === 0 && (
          <div className="mt-10 rounded-xl border border-dashed border-border p-10 text-center">
            <Badge variant="outline" className="mx-auto">
              No matches
            </Badge>
            <p className="mt-3 text-sm text-muted-foreground">Try clearing some filters.</p>
          </div>
        )}
      </div>
      <UpgradeModal open={upgradeOpen} onOpenChange={setUpgradeOpen} />
    </AppShell>
  );
}

export default ChallengesPage;
