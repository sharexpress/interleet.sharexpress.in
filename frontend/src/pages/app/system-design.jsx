
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Network, Database, Cpu, Cloud, Layers, Globe2 } from "lucide-react";
import { systemDesignTopics } from "@/lib/mock";



const icons = {
  Scalability: Layers,
  Caching: Cpu,
  Databases: Database,
  "Distributed Systems": Network,
  Infrastructure: Cloud,
  "Load Balancing": Globe2
};

function SystemDesign() {
  return (
    <AppShell>
      <PageHeader
        title="System Design"
        description="Architect, defend, and iterate on production-grade systems." />
      
      <div className="px-4 py-6 md:px-8">
        <Card className="mb-6 border-border bg-card p-5">
          <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">Reference architecture</p>
          <div className="mt-3 grid grid-cols-3 gap-3 md:grid-cols-6">
            {[
            { i: Globe2, l: "Client" },
            { i: Layers, l: "API Gateway" },
            { i: Network, l: "Service Mesh" },
            { i: Cpu, l: "Workers" },
            { i: Database, l: "Postgres" },
            { i: Cloud, l: "Object Store" }].
            map(({ i: Icon, l }) =>
            <div key={l} className="rounded-lg border border-border bg-background/40 p-3 text-center">
                <Icon className="mx-auto h-4 w-4 text-primary" />
                <p className="mt-2 font-mono text-[11px] text-muted-foreground">{l}</p>
              </div>
            )}
          </div>
        </Card>

        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {systemDesignTopics.map((t) => {
            const Icon = icons[t.title] ?? Network;
            return (
              <Card key={t.title} className="border-border bg-card p-5 transition-colors hover:border-primary/40">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-background">
                      <Icon className="h-4 w-4 text-primary" />
                    </span>
                    <h3 className="text-sm font-semibold">{t.title}</h3>
                  </div>
                  <Badge variant="outline" className="font-mono text-[10px]">{t.items.length} topics</Badge>
                </div>
                <ul className="mt-4 space-y-1.5 text-sm">
                  {t.items.map((i) =>
                  <li key={i} className="flex items-center gap-2 text-foreground/85">
                      <span className="h-1 w-1 rounded-full bg-primary" />{i}
                    </li>
                  )}
                </ul>
              </Card>);

          })}
        </div>
      </div>
    </AppShell>);

}
export default SystemDesign;
