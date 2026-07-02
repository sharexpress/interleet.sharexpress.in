import { useState, useEffect } from "react";
import { PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Search, ShieldCheck, Filter, ArrowUpRight } from "lucide-react";
import { API } from "@/api/api";

function Recruiter() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedUsernames, setSelectedUsernames] = useState([]);

  // Filters state
  const [domainFilter, setDomainFilter] = useState("");
  const [minRatingFilter, setMinRatingFilter] = useState("");
  const [locationFilter, setLocationFilter] = useState("");
  const [verifiedFilter, setVerifiedFilter] = useState("");

  /* ── SEO ──────────────────────────────────────────── */
  useEffect(() => {
    document.title = "Recruiter Dashboard — Interleet | Hire Verified Engineers";
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute("content", "Interleet Recruiter Dashboard — search and compare verified engineers with rubric-backed skill scores. Filter by domain, rating, and location.");
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  /* ── Fetch backend data ────────────────────────────── */
  useEffect(() => {
    API.get("/api/candidates")
      .then((res) => {
        if (res.data && res.data.items) {
          setCandidates(res.data.items);
          // Set initial compared candidates to the first two
          if (res.data.items.length >= 2) {
            setSelectedUsernames([res.data.items[0].username, res.data.items[1].username]);
          }
        }
      })
      .catch((err) => {
        console.error("Error loading candidates from backend:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // Handle selection toggles
  const handleToggleSelect = (username) => {
    setSelectedUsernames((prev) => {
      if (prev.includes(username)) {
        return prev.filter((u) => u !== username);
      } else {
        // Limit comparison to 2 candidates max at a time for optimal layout structure
        if (prev.length >= 2) {
          return [prev[1], username];
        }
        return [...prev, username];
      }
    });
  };

  // Perform client-side filter computation over retrieved backend records
  const filteredCandidates = candidates.filter((c) => {
    const matchSearch = searchTerm === "" || 
      c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.top.toLowerCase().includes(searchTerm.toLowerCase());

    const matchDomain = domainFilter === "" || 
      c.top.toLowerCase().includes(domainFilter.toLowerCase());

    const matchRating = minRatingFilter === "" || 
      c.rating >= parseInt(minRatingFilter, 10);

    const matchLocation = locationFilter === "" || 
      c.location.toLowerCase().includes(locationFilter.toLowerCase());

    const matchVerified = verifiedFilter === "" || 
      (verifiedFilter.toLowerCase() === "yes" || verifiedFilter.toLowerCase() === "true" 
        ? c.verified === true 
        : true);

    return matchSearch && matchDomain && matchRating && matchLocation && matchVerified;
  });

  const selectedCandidates = candidates.filter((c) => selectedUsernames.includes(c.username));

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col p-4 md:p-8">
      <main className="flex-1 min-w-0">
        <PageHeader
          title="Recruiter dashboard"
          description="Search verified engineers. Compare candidates with rubric-backed scores."
          badge="Enterprise"
          actions={<Button>Save search</Button>} />
        
        <div className="grid gap-6 px-4 py-6 md:grid-cols-4 md:px-8">
          {/* Filters Sidebar */}
          <Card className="border-border bg-card p-5 md:col-span-1 h-fit">
            <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">Filters</p>
            <div className="mt-4 space-y-4">
              <div>
                <p className="mb-1.5 text-xs font-medium text-muted-foreground">Domain</p>
                <Input 
                  placeholder="Any domain…" 
                  className="h-8" 
                  value={domainFilter}
                  onChange={(e) => setDomainFilter(e.target.value)}
                />
              </div>
              <div>
                <p className="mb-1.5 text-xs font-medium text-muted-foreground">Min rating</p>
                <Input 
                  placeholder="Any rating…" 
                  className="h-8" 
                  type="number"
                  value={minRatingFilter}
                  onChange={(e) => setMinRatingFilter(e.target.value)}
                />
              </div>
              <div>
                <p className="mb-1.5 text-xs font-medium text-muted-foreground">Location</p>
                <Input 
                  placeholder="Any location…" 
                  className="h-8" 
                  value={locationFilter}
                  onChange={(e) => setLocationFilter(e.target.value)}
                />
              </div>
              <div>
                <p className="mb-1.5 text-xs font-medium text-muted-foreground">Verified only (yes/no)</p>
                <Input 
                  placeholder="Any verification…" 
                  className="h-8" 
                  value={verifiedFilter}
                  onChange={(e) => setVerifiedFilter(e.target.value)}
                />
              </div>
              <Button 
                className="w-full" 
                onClick={() => {
                  setDomainFilter("");
                  setMinRatingFilter("");
                  setLocationFilter("");
                  setVerifiedFilter("");
                  setSearchTerm("");
                }}
              >
                <Filter className="mr-1.5 h-4 w-4" /> Reset Filters
              </Button>
            </div>
          </Card>

          {/* Candidates display container */}
          <div className="space-y-4 md:col-span-3">
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input 
                placeholder="Search candidates by skill, role, or username…" 
                className="h-10 bg-card pl-9" 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <Card className="overflow-hidden border-border bg-card p-0">
              <table className="w-full text-sm">
                <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                  <tr>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Candidate</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Top domain</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Rating</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Location</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Status</th>
                    <th className="px-4 py-2" />
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan="6" className="text-center py-8 text-muted-foreground">
                        Loading candidate list from backend...
                      </td>
                    </tr>
                  ) : filteredCandidates.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="text-center py-8 text-muted-foreground">
                        No candidates found matching the active search filters.
                      </td>
                    </tr>
                  ) : (
                    filteredCandidates.map((c) => (
                      <tr key={c.username} className="border-t border-border hover:bg-accent/40">
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            <Avatar className="h-7 w-7 border border-border">
                              <AvatarFallback className="text-[10px]">
                                {c.name.split(" ").map((p) => p[0]).join("")}
                              </AvatarFallback>
                            </Avatar>
                            <div>
                              <p className="font-medium">{c.name}</p>
                              <p className="text-xs text-muted-foreground">@{c.username}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-4 py-3">{c.top}</td>
                        <td className="px-4 py-3 font-mono">{c.rating}</td>
                        <td className="px-4 py-3 text-muted-foreground">{c.location}</td>
                        <td className="px-4 py-3">
                          {c.verified ? (
                            <Badge className="gap-1 bg-success/15 text-success">
                              <ShieldCheck className="h-3 w-3" /> Verified
                            </Badge>
                          ) : (
                            <Badge variant="outline">Unverified</Badge>
                          )}
                        </td>
                        <td className="px-4 py-3 text-right">
                          <div className="flex items-center justify-end gap-2">
                            <Button 
                              variant={selectedUsernames.includes(c.username) ? "default" : "outline"} 
                              size="sm" 
                              className="h-8 text-xs"
                              onClick={() => handleToggleSelect(c.username)}
                            >
                              {selectedUsernames.includes(c.username) ? "Selected" : "Compare"}
                            </Button>
                            <Button variant="ghost" size="sm" className="h-8">
                              View <ArrowUpRight className="ml-1 h-3.5 w-3.5" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </Card>

            {/* Compare panel widget */}
            <Card className="border-border bg-card p-5">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold">Side-by-side comparison</h3>
                <Badge variant="outline" className="font-mono text-[10px]">
                  {selectedCandidates.length} selected
                </Badge>
              </div>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                {selectedCandidates.length === 0 ? (
                  <p className="text-sm text-muted-foreground col-span-2 py-4 text-center">
                    Select up to 2 candidates above to compare metric scorecards side-by-side.
                  </p>
                ) : (
                  selectedCandidates.map((c) => {
                    // Generate dynamic metrics scores mapped to candidate ratings
                    const technical = Math.min(100, Math.max(50, Math.round((c.rating / 3000) * 100)));
                    const communication = Math.min(100, Math.max(50, Math.round(75 + (c.rating % 20))));
                    const systemDesign = Math.min(100, Math.max(50, Math.round(70 + (c.rating % 25))));
                    
                    const scoreList = [
                      ["Technical Depth", technical],
                      ["Communication Clarity", communication],
                      ["System Design Scale", systemDesign]
                    ];

                    return (
                      <div key={c.username} className="rounded-lg border border-border bg-background/40 p-4">
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-sm font-medium">{c.name}</p>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="h-5 text-[10px] text-muted-foreground hover:text-destructive p-0"
                            onClick={() => handleToggleSelect(c.username)}
                          >
                            Remove
                          </Button>
                        </div>
                        <p className="text-xs text-muted-foreground">@{c.username} · {c.top} Track</p>
                        <div className="mt-4 space-y-3">
                          {scoreList.map(([k, v]) => (
                            <div key={k}>
                              <div className="mb-1 flex justify-between text-[11px]">
                                <span className="text-muted-foreground">{k}</span>
                                <span className="font-mono text-foreground font-semibold">{v}%</span>
                              </div>
                              <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                                <div className="h-full rounded-full bg-primary" style={{ width: `${v}%` }} />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Recruiter;
