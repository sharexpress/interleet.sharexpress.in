
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Trophy, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { leaderboard } from "@/lib/mock";



function Leaderboard() {
  return (
    <AppShell>
      <PageHeader title="Leaderboard" description="Rated by domain. Ranked weekly. Climb the arena." />
      <div className="px-4 py-6 md:px-8">
        {/* Podium */}
        <div className="mb-6 grid gap-3 md:grid-cols-3">
          {leaderboard.slice(0, 3).map((r, i) =>
          <Card
            key={r.username}
            className={`flex items-center gap-4 border-border bg-card p-5 ${i === 0 ? "ring-1 ring-primary/40" : ""}`}>
            
              <span className={`flex h-12 w-12 items-center justify-center rounded-full ${i === 0 ? "bg-warning/20 text-warning" : i === 1 ? "bg-muted text-foreground" : "bg-chart-3/20 text-chart-3"}`}>
                <Trophy className="h-5 w-5" />
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-semibold">@{r.username}</p>
                <p className="text-xs text-muted-foreground">Rating {r.rating} · {r.country}</p>
              </div>
              <p className="font-mono text-2xl font-semibold text-foreground">#{r.rank}</p>
            </Card>
          )}
        </div>

        <Tabs defaultValue="global">
          <TabsList>
            <TabsTrigger value="global">Global</TabsTrigger>
            <TabsTrigger value="weekly">Weekly</TabsTrigger>
            <TabsTrigger value="friends">Friends</TabsTrigger>
          </TabsList>
          {["global", "weekly", "friends"].map((v) =>
          <TabsContent key={v} value={v} className="mt-4">
              <Card className="overflow-hidden border-border bg-card p-0">
                <div className="hidden md:block">
                  <table className="w-full text-sm">
                    <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                      <tr>
                        <th className="px-4 py-2 font-mono uppercase tracking-wider">#</th>
                        <th className="px-4 py-2 font-mono uppercase tracking-wider">Engineer</th>
                        <th className="px-4 py-2 font-mono uppercase tracking-wider">Rating</th>
                        <th className="px-4 py-2 font-mono uppercase tracking-wider">XP</th>
                        <th className="px-4 py-2 font-mono uppercase tracking-wider">Badges</th>
                        <th className="px-4 py-2 text-right font-mono uppercase tracking-wider">Δ 7d</th>
                      </tr>
                    </thead>
                    <tbody>
                      {leaderboard.map((r) =>
                    <tr key={r.username} className="border-t border-border hover:bg-accent/40">
                          <td className="px-4 py-3 font-mono text-muted-foreground">#{r.rank}</td>
                          <td className="px-4 py-3">
                            <div className="flex items-center gap-2">
                              <Avatar className="h-7 w-7 border border-border">
                                <AvatarFallback className="text-[10px]">{r.username.slice(0, 2).toUpperCase()}</AvatarFallback>
                              </Avatar>
                              <div>
                                <p className="font-medium">@{r.username}</p>
                                <p className="text-xs text-muted-foreground">{r.country}</p>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 font-mono">{r.rating}</td>
                          <td className="px-4 py-3 font-mono">{r.xp.toLocaleString()}</td>
                          <td className="px-4 py-3">
                            <div className="flex flex-wrap gap-1">
                              {r.badges.map((b) =>
                          <Badge key={b} variant="outline" className="font-mono text-[10px]">{b}</Badge>
                          )}
                            </div>
                          </td>
                          <td className={`px-4 py-3 text-right font-mono ${r.delta > 0 ? "text-success" : r.delta < 0 ? "text-destructive" : "text-muted-foreground"}`}>
                            <span className="inline-flex items-center gap-1">
                              {r.delta > 0 ? <TrendingUp className="h-3.5 w-3.5" /> : r.delta < 0 ? <TrendingDown className="h-3.5 w-3.5" /> : <Minus className="h-3.5 w-3.5" />}
                              {r.delta > 0 ? `+${r.delta}` : r.delta}
                            </span>
                          </td>
                        </tr>
                    )}
                    </tbody>
                  </table>
                </div>
                <ul className="divide-y divide-border md:hidden">
                  {leaderboard.map((r) =>
                <li key={r.username} className="flex items-center gap-3 p-4">
                      <span className="w-6 font-mono text-xs text-muted-foreground">#{r.rank}</span>
                      <Avatar className="h-8 w-8 border border-border">
                        <AvatarFallback className="text-[10px]">{r.username.slice(0, 2).toUpperCase()}</AvatarFallback>
                      </Avatar>
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">@{r.username}</p>
                        <p className="text-xs text-muted-foreground">Rating {r.rating}</p>
                      </div>
                      <span className={`font-mono text-xs ${r.delta >= 0 ? "text-success" : "text-destructive"}`}>
                        {r.delta >= 0 ? `+${r.delta}` : r.delta}
                      </span>
                    </li>
                )}
                </ul>
              </Card>
            </TabsContent>
          )}
        </Tabs>
      </div>
    </AppShell>);

}
export default Leaderboard;
