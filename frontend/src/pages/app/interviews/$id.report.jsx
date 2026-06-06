import { Link, useParams } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Check, X, ArrowRight } from "lucide-react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid } from
"recharts";



function ReportPage() {
  const { id } = useParams();
  const scores = [
  { k: "Communication", v: 82 },
  { k: "Technical", v: 78 },
  { k: "Problem solving", v: 84 },
  { k: "Confidence", v: 76 }];

  const radar = [
  { axis: "Concurrency", s: 85 },
  { axis: "Scaling", s: 78 },
  { axis: "Data modeling", s: 72 },
  { axis: "Tradeoffs", s: 88 },
  { axis: "Communication", s: 82 },
  { axis: "Edge cases", s: 65 }];

  return (
    <AppShell>
      <PageHeader
        title="Interview report"
        badge={id}
        description="Rubric-graded breakdown of your session with personalized recommendations."
        actions={<Button asChild><Link to="/app/interviews">Run another <ArrowRight className="ml-1.5 h-4 w-4" /></Link></Button>} />
      
      <div className="space-y-6 px-4 py-6 md:px-8">
        <div className="grid gap-4 md:grid-cols-4">
          {scores.map((s) =>
          <Card key={s.k} className="border-border bg-card p-5">
              <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">{s.k}</p>
              <p className="mt-2 text-3xl font-semibold tracking-tight">{s.v}<span className="text-base text-muted-foreground">/100</span></p>
              <div className="mt-3 h-1 rounded-full bg-muted">
                <div className="h-full rounded-full bg-primary" style={{ width: `${s.v}%` }} />
              </div>
            </Card>
          )}
        </div>

        <div className="grid gap-4 lg:grid-cols-2">
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold">Skill breakdown</h3>
            <div className="mt-3 h-72">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radar}>
                  <PolarGrid stroke="hsl(var(--border))" />
                  <PolarAngleAxis dataKey="axis" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} />
                  <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 100]} />
                  <Radar dataKey="s" stroke="var(--color-primary)" fill="var(--color-primary)" fillOpacity={0.25} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </Card>
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold">Progress over time</h3>
            <div className="mt-3 h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={[55, 60, 62, 68, 71, 74, 78, 80, 84].map((s, i) => ({ d: `S${i + 1}`, s }))}>
                  <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="d" stroke="hsl(var(--muted-foreground))" fontSize={11} tickLine={false} axisLine={false} />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={11} tickLine={false} axisLine={false} domain={[40, 100]} />
                  <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8, fontSize: 12 }} />
                  <Line type="monotone" dataKey="s" stroke="var(--color-primary)" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        <div className="grid gap-4 lg:grid-cols-2">
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold text-success">Strengths</h3>
            <ul className="mt-3 space-y-2 text-sm">
              {["Clear articulation of tradeoffs", "Strong concurrency intuition", "Justified component choices"].map((x) =>
              <li key={x} className="flex items-start gap-2"><Check className="mt-0.5 h-4 w-4 text-success" /><span>{x}</span></li>
              )}
            </ul>
          </Card>
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold text-destructive">To improve</h3>
            <ul className="mt-3 space-y-2 text-sm">
              {["Drive more edge-case discussion proactively", "Quantify scale assumptions earlier", "Tighten estimation language"].map((x) =>
              <li key={x} className="flex items-start gap-2"><X className="mt-0.5 h-4 w-4 text-destructive" /><span>{x}</span></li>
              )}
            </ul>
          </Card>
        </div>

        <Card className="border-border bg-card p-5">
          <h3 className="text-sm font-semibold">Recommended next steps</h3>
          <ul className="mt-3 grid gap-2 md:grid-cols-3">
            {["Design Twitter's Home Feed", "Postgres Indexing Strategy", "Feature Flag Service"].map((x) =>
            <li key={x} className="rounded-md border border-border bg-background/40 p-3 text-sm">{x}</li>
            )}
          </ul>
        </Card>
      </div>
    </AppShell>);

}
export default ReportPage;
