
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Users, Code2, Trophy, AlertTriangle, Plus, MoreHorizontal } from "lucide-react";
import { challenges, leaderboard } from "@/lib/mock";



function Admin() {
  return (
    <AppShell>
      <PageHeader title="Admin" description="Platform operations and moderation." badge="Restricted" />
      <div className="space-y-6 px-4 py-6 md:px-8">
        <div className="grid gap-4 md:grid-cols-4">
          {[
          { l: "Users", v: "184,210", i: Users },
          { l: "Challenges", v: "12,420", i: Code2 },
          { l: "Contests", v: "62", i: Trophy },
          { l: "Open reports", v: "14", i: AlertTriangle }].
          map(({ l, v, i: Icon }) =>
          <Card key={l} className="border-border bg-card p-4">
              <div className="flex items-center justify-between">
                <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">{l}</p>
                <Icon className="h-4 w-4 text-primary" />
              </div>
              <p className="mt-2 text-2xl font-semibold">{v}</p>
            </Card>
          )}
        </div>

        <Tabs defaultValue="challenges">
          <TabsList>
            <TabsTrigger value="challenges">Challenges</TabsTrigger>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="contests">Contests</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          <TabsContent value="challenges" className="mt-4">
            <Card className="overflow-hidden border-border bg-card p-0">
              <div className="flex items-center justify-between border-b border-border px-4 py-3">
                <p className="text-sm font-medium">Challenge catalog</p>
                <Button size="sm"><Plus className="mr-1 h-3.5 w-3.5" /> New challenge</Button>
              </div>
              <table className="w-full text-sm">
                <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                  <tr>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Title</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Domain</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Status</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Submissions</th>
                    <th className="px-4 py-2" />
                  </tr>
                </thead>
                <tbody>
                  {challenges.map((c, i) =>
                  <tr key={c.id} className="border-t border-border">
                      <td className="px-4 py-3 font-medium">{c.title}</td>
                      <td className="px-4 py-3">{c.domain}</td>
                      <td className="px-4 py-3">
                        <Badge variant="outline" className={i % 4 === 0 ? "text-warning" : "text-success"}>
                          {i % 4 === 0 ? "Draft" : "Published"}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 font-mono">{(c.completion * 120).toLocaleString()}</td>
                      <td className="px-4 py-3 text-right">
                        <Button variant="ghost" size="icon" className="h-7 w-7"><MoreHorizontal className="h-4 w-4" /></Button>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </Card>
          </TabsContent>

          <TabsContent value="users" className="mt-4">
            <Card className="overflow-hidden border-border bg-card p-0">
              <table className="w-full text-sm">
                <thead className="bg-background/60 text-left text-xs text-muted-foreground">
                  <tr>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">User</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Rating</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">XP</th>
                    <th className="px-4 py-2 font-mono uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.slice(0, 8).map((r, i) =>
                  <tr key={r.username} className="border-t border-border">
                      <td className="px-4 py-3 font-medium">@{r.username}</td>
                      <td className="px-4 py-3 font-mono">{r.rating}</td>
                      <td className="px-4 py-3 font-mono">{r.xp.toLocaleString()}</td>
                      <td className="px-4 py-3">
                        <Badge variant="outline" className={i === 4 ? "text-destructive" : "text-success"}>
                          {i === 4 ? "Suspended" : "Active"}
                        </Badge>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </Card>
          </TabsContent>

          <TabsContent value="contests" className="mt-4">
            <Card className="border-border bg-card p-6">
              <p className="text-sm text-muted-foreground">Weekly Engineering Cup · 14,200 registrations · Live in 2d 4h</p>
            </Card>
          </TabsContent>

          <TabsContent value="reports" className="mt-4">
            <Card className="border-border bg-card p-6">
              <p className="text-sm text-muted-foreground">14 open moderation reports. No critical items.</p>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </AppShell>);

}
export default Admin;
