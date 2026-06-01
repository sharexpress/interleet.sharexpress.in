
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Search, ShieldCheck, Filter, ArrowUpRight } from "lucide-react";
import { candidates } from "@/lib/mock";



function Recruiter() {
  return (
    <AppShell>
      <PageHeader
        title="Recruiter dashboard"
        description="Search verified engineers. Compare candidates with rubric-backed scores."
        badge="Enterprise"
        actions={<Button>Save search</Button>} />
      
      <div className="grid gap-6 px-4 py-6 md:grid-cols-4 md:px-8">
        {/* Filters */}
        <Card className="border-border bg-card p-5 md:col-span-1">
          <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">Filters</p>
          <div className="mt-4 space-y-4">
            {["Domain", "Min rating", "Location", "Verified only"].map((l) =>
            <div key={l}>
                <p className="mb-1.5 text-xs font-medium text-muted-foreground">{l}</p>
                <Input placeholder={`Any ${l.toLowerCase()}…`} className="h-8" />
              </div>
            )}
            <Button className="w-full"><Filter className="mr-1.5 h-4 w-4" /> Apply</Button>
          </div>
        </Card>

        {/* Candidates */}
        <div className="space-y-4 md:col-span-3">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input placeholder="Search candidates by skill, role, or username…" className="h-10 bg-card pl-9" />
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
                {candidates.map((c) =>
                <tr key={c.username} className="border-t border-border hover:bg-accent/40">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <Avatar className="h-7 w-7 border border-border">
                          <AvatarFallback className="text-[10px]">{c.name.split(" ").map((p) => p[0]).join("")}</AvatarFallback>
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
                      {c.verified ?
                    <Badge className="gap-1 bg-success/15 text-success"><ShieldCheck className="h-3 w-3" />Verified</Badge> :

                    <Badge variant="outline">Unverified</Badge>
                    }
                    </td>
                    <td className="px-4 py-3 text-right">
                      <Button variant="ghost" size="sm">View <ArrowUpRight className="ml-1 h-3.5 w-3.5" /></Button>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </Card>

          {/* Compare */}
          <Card className="border-border bg-card p-5">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold">Side-by-side comparison</h3>
              <Badge variant="outline" className="font-mono text-[10px]">2 selected</Badge>
            </div>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              {candidates.slice(0, 2).map((c) =>
              <div key={c.username} className="rounded-lg border border-border bg-background/40 p-4">
                  <p className="text-sm font-medium">{c.name}</p>
                  <p className="text-xs text-muted-foreground">@{c.username} · {c.top}</p>
                  <div className="mt-3 space-y-2">
                    {[["Technical", 86], ["Communication", 78], ["System design", 81]].map(([k, v]) =>
                  <div key={k}>
                        <div className="mb-0.5 flex justify-between text-[11px]"><span className="text-muted-foreground">{k}</span><span className="font-mono">{v}</span></div>
                        <div className="h-1 rounded-full bg-muted"><div className="h-full rounded-full bg-primary" style={{ width: `${v}%` }} /></div>
                      </div>
                  )}
                  </div>
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </AppShell>);

}
export default Recruiter;
