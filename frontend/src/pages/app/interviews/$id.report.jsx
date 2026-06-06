import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Check, X, ArrowRight, Loader2, AlertTriangle, Trophy, Target, TrendingUp, BookOpen } from "lucide-react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip,
} from "recharts";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import { fetchReport } from "@/redux/slices/interviewsSlice";

// ─── Score Badge ─────────────────────────────────────────────────────────────

function ScoreRing({ value, label }) {
  const color =
    value >= 80 ? "#22c55e" : value >= 60 ? "#f97316" : "#ef4444";
  return (
    <Card className="border-border bg-card p-5 flex flex-col items-center gap-3">
      <div className="relative flex items-center justify-center">
        <svg width={80} height={80} viewBox="0 0 80 80">
          <circle cx={40} cy={40} r={34} fill="none" stroke="#1f1f1f" strokeWidth={8} />
          <circle
            cx={40}
            cy={40}
            r={34}
            fill="none"
            stroke={color}
            strokeWidth={8}
            strokeDasharray={`${(value / 100) * 2 * Math.PI * 34} ${2 * Math.PI * 34}`}
            strokeLinecap="round"
            transform="rotate(-90 40 40)"
            style={{ transition: "stroke-dasharray 0.8s ease" }}
          />
        </svg>
        <span className="absolute text-xl font-bold text-white">{value}</span>
      </div>
      <p className="text-[11px] font-mono uppercase tracking-widest text-muted-foreground text-center">
        {label}
      </p>
    </Card>
  );
}

// ─── Topic Evaluation Row ─────────────────────────────────────────────────────

function TopicRow({ item }) {
  const score = item.score ?? item.s ?? 0;
  const color =
    score >= 8 ? "text-emerald-400 border-emerald-800/40 bg-emerald-950/20"
    : score >= 6 ? "text-amber-400 border-amber-800/40 bg-amber-950/20"
    : "text-red-400 border-red-800/40 bg-red-950/20";
  return (
    <div className="flex items-start gap-3 rounded-lg border border-zinc-800/50 bg-zinc-900/30 p-3">
      <Badge className={`shrink-0 font-mono text-xs ${color} border`}>
        {score}/10
      </Badge>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-zinc-100">{item.topic || item.axis}</p>
        {item.summary && (
          <p className="text-[11px] text-zinc-500 leading-relaxed mt-0.5 line-clamp-2">
            {item.summary}
          </p>
        )}
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

function ReportPage() {
  const { id } = useParams();
  const dispatch = useAppDispatch();
  const { report, reportLoading, reportError } = useAppSelector(
    (s) => s.interviews
  );

  useEffect(() => {
    // If we don't have a report yet (or it's for a different session), fetch it
    if (!report || report.session_id !== id) {
      dispatch(fetchReport(id));
    }
    return () => {
      // Keep report in state so user can navigate back without refetch
    };
  }, [id]); // eslint-disable-line

  // ── Loading state ───────────────────────────────────────────────────────────
  if (reportLoading) {
    return (
      <AppShell>
        <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
          <Loader2 className="h-10 w-10 animate-spin text-primary" />
          <p className="text-sm text-zinc-400">Generating your interview report…</p>
        </div>
      </AppShell>
    );
  }

  // ── Error state ─────────────────────────────────────────────────────────────
  if (reportError || (!reportLoading && !report)) {
    return (
      <AppShell>
        <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
          <AlertTriangle className="h-10 w-10 text-amber-500" />
          <p className="text-sm font-semibold text-zinc-200">Report not found</p>
          <p className="text-xs text-zinc-500">{reportError || "This session may have already expired."}</p>
          <Button asChild className="mt-2 bg-primary hover:bg-orange-600">
            <Link to="/app/interviews">Run another interview</Link>
          </Button>
        </div>
      </AppShell>
    );
  }

  // ── Map report fields ───────────────────────────────────────────────────────
  const role = report.role || "Interview";
  const difficulty = report.difficulty || "medium";
  const overallScore = report.overall_score ?? report.score ?? 0;

  // Score cards: try common backend field names
  const rawScores = report.scores || {};
  const scoreCards = [
    { k: "Technical", v: rawScores.technical ?? rawScores.technical_knowledge ?? 0 },
    { k: "Communication", v: rawScores.communication ?? rawScores.communication_skills ?? 0 },
    { k: "Problem Solving", v: rawScores.problem_solving ?? rawScores.problem_solving_ability ?? 0 },
    { k: "Overall", v: overallScore },
  ].map((s) => ({ ...s, v: Math.round(s.v) }));

  // Radar data: prefer topic_evaluations, fallback to scores keys
  let radarData = [];
  if (Array.isArray(report.topic_evaluations) && report.topic_evaluations.length > 0) {
    radarData = report.topic_evaluations.map((t) => ({
      axis: t.topic,
      s: Math.min(Math.round((t.score ?? 5) * 10), 100),
      score: t.score,
      summary: t.summary,
      topic: t.topic,
    }));
  } else if (Object.keys(rawScores).length > 0) {
    radarData = Object.entries(rawScores).map(([k, v]) => ({
      axis: k.replace(/_/g, " "),
      s: Math.round(v),
    }));
  }

  const strengths = report.strengths || [];
  const improvements = report.improvements || report.areas_for_improvement || [];
  const recommendations = report.recommendations || [];
  const topicEvals = report.topic_evaluations || [];

  return (
    <AppShell>
      <PageHeader
        title="Interview Report"
        badge={`Session · ${id?.slice(0, 8)}`}
        description={`${role} · ${difficulty} — AI-graded breakdown of your performance with personalized feedback.`}
        actions={
          <Button asChild className="bg-primary hover:bg-orange-600 text-white">
            <Link to="/app/interviews">
              Run another <ArrowRight className="ml-1.5 h-4 w-4" />
            </Link>
          </Button>
        }
      />

      <div className="space-y-6 px-4 py-6 md:px-8">

        {/* ── Overall Score Hero ── */}
        <Card className="border-border bg-card p-6 flex flex-col sm:flex-row items-center gap-6">
          <div className="relative flex items-center justify-center shrink-0">
            <svg width={120} height={120} viewBox="0 0 120 120">
              <circle cx={60} cy={60} r={52} fill="none" stroke="#1a1a1a" strokeWidth={10} />
              <circle
                cx={60} cy={60} r={52}
                fill="none"
                stroke={overallScore >= 75 ? "#f97316" : overallScore >= 55 ? "#eab308" : "#ef4444"}
                strokeWidth={10}
                strokeDasharray={`${(overallScore / 100) * 2 * Math.PI * 52} ${2 * Math.PI * 52}`}
                strokeLinecap="round"
                transform="rotate(-90 60 60)"
                style={{ transition: "stroke-dasharray 1s ease" }}
              />
            </svg>
            <div className="absolute flex flex-col items-center">
              <span className="text-3xl font-bold text-white">{overallScore}</span>
              <span className="text-[10px] text-zinc-500 uppercase tracking-wider">/ 100</span>
            </div>
          </div>
          <div className="flex-1 text-center sm:text-left">
            <div className="flex items-center gap-2 justify-center sm:justify-start mb-1">
              <Trophy className="h-5 w-5 text-primary" />
              <h2 className="text-lg font-bold text-white">Overall Performance</h2>
            </div>
            <p className="text-sm text-zinc-400 leading-relaxed">
              {overallScore >= 80
                ? "Excellent performance! You demonstrated strong technical expertise and clear communication."
                : overallScore >= 65
                ? "Good performance. With targeted practice you can reach the top tier."
                : "Keep practicing — review the improvement areas below to level up your skills."}
            </p>
            <div className="mt-3 flex flex-wrap gap-2 justify-center sm:justify-start">
              <Badge className="bg-primary/10 text-primary border-primary/20 font-semibold">{role}</Badge>
              <Badge variant="outline" className="border-zinc-700 text-zinc-400 capitalize">{difficulty}</Badge>
            </div>
          </div>
        </Card>

        {/* ── Score Cards ── */}
        <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
          {scoreCards.map((s) => (
            <ScoreRing key={s.k} value={s.v} label={s.k} />
          ))}
        </div>

        {/* ── Radar + Topic Evals ── */}
        <div className="grid gap-4 lg:grid-cols-2">
          {radarData.length > 0 && (
            <Card className="border-border bg-card p-5">
              <div className="flex items-center gap-2 mb-4">
                <Target className="h-4 w-4 text-primary" />
                <h3 className="text-sm font-semibold text-white">Skill Breakdown</h3>
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="hsl(var(--border))" />
                    <PolarAngleAxis
                      dataKey="axis"
                      tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                    />
                    <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 100]} />
                    <Radar
                      dataKey="s"
                      stroke="var(--color-primary, #f97316)"
                      fill="var(--color-primary, #f97316)"
                      fillOpacity={0.2}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: 8,
                        fontSize: 12,
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          {topicEvals.length > 0 && (
            <Card className="border-border bg-card p-5">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="h-4 w-4 text-primary" />
                <h3 className="text-sm font-semibold text-white">Topic Evaluations</h3>
              </div>
              <div className="space-y-2 overflow-auto max-h-72 pr-1">
                {topicEvals.map((t, i) => (
                  <TopicRow key={i} item={t} />
                ))}
              </div>
            </Card>
          )}
        </div>

        {/* ── Strengths + Improvements ── */}
        <div className="grid gap-4 lg:grid-cols-2">
          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold text-emerald-400 mb-3">✓ Strengths</h3>
            {strengths.length === 0 ? (
              <p className="text-xs text-zinc-600 italic">No strengths data available.</p>
            ) : (
              <ul className="space-y-2">
                {strengths.map((x, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-zinc-200">
                    <Check className="mt-0.5 h-4 w-4 text-emerald-400 shrink-0" />
                    <span>{typeof x === "string" ? x : x.text || x.description || JSON.stringify(x)}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card className="border-border bg-card p-5">
            <h3 className="text-sm font-semibold text-red-400 mb-3">✗ Areas to Improve</h3>
            {improvements.length === 0 ? (
              <p className="text-xs text-zinc-600 italic">No improvement areas identified.</p>
            ) : (
              <ul className="space-y-2">
                {improvements.map((x, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-zinc-200">
                    <X className="mt-0.5 h-4 w-4 text-red-400 shrink-0" />
                    <span>{typeof x === "string" ? x : x.text || x.description || JSON.stringify(x)}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>

        {/* ── Recommendations ── */}
        {recommendations.length > 0 && (
          <Card className="border-border bg-card p-5">
            <div className="flex items-center gap-2 mb-3">
              <BookOpen className="h-4 w-4 text-primary" />
              <h3 className="text-sm font-semibold text-white">Recommended Next Steps</h3>
            </div>
            <ul className="grid gap-2 md:grid-cols-3">
              {recommendations.map((x, i) => (
                <li
                  key={i}
                  className="rounded-lg border border-zinc-800/60 bg-zinc-900/30 px-4 py-3 text-sm text-zinc-200 leading-relaxed"
                >
                  {typeof x === "string" ? x : x.text || x.description || JSON.stringify(x)}
                </li>
              ))}
            </ul>
          </Card>
        )}
      </div>
    </AppShell>
  );
}

export default ReportPage;
