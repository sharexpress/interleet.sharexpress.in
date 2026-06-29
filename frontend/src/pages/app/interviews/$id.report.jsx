import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Check, 
  X, 
  ArrowRight, 
  AlertTriangle, 
  Trophy, 
  Target, 
  TrendingUp, 
  BookOpen,
  Zap,
  Activity,
  Award,
  Sparkles,
  ArrowLeft
} from "lucide-react";
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
    value >= 75 ? "text-emerald-500" : value >= 55 ? "text-amber-500" : "text-rose-500";
  const strokeColor =
    value >= 75 ? "#10b981" : value >= 55 ? "#f59e0b" : "#f43f5e";
  const shadowColor =
    value >= 75 ? "rgba(16,185,129,0.15)" : value >= 55 ? "rgba(245,158,11,0.15)" : "rgba(244,63,94,0.15)";

  return (
    <Card className="border border-zinc-800/80 bg-zinc-950/20 backdrop-blur-sm p-6 flex flex-col items-center justify-between hover:border-zinc-700/60 transition-all duration-300 shadow-xl">
      <div className="relative flex items-center justify-center">
        {/* Subtle radial glow */}
        <div 
          className="absolute w-14 h-14 rounded-full blur-xl opacity-20 transition-all duration-300"
          style={{ backgroundColor: strokeColor, boxShadow: `0 0 20px 10px ${shadowColor}` }}
        />
        <svg width={90} height={90} viewBox="0 0 90 90" className="drop-shadow-[0_4px_8px_rgba(0,0,0,0.6)]">
          <circle cx={45} cy={45} r={38} fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth={6} />
          <circle
            cx={45}
            cy={45}
            r={38}
            fill="none"
            stroke={strokeColor}
            strokeWidth={6}
            strokeDasharray={`${(value / 100) * 2 * Math.PI * 38} ${2 * Math.PI * 38}`}
            strokeLinecap="round"
            transform="rotate(-90 45 45)"
            style={{ transition: "stroke-dasharray 1s cubic-bezier(0.4, 0, 0.2, 1)" }}
          />
        </svg>
        <span className="absolute text-2xl font-black text-white tracking-tight">{value}</span>
      </div>
      <p className="mt-4 text-[10px] font-mono font-semibold uppercase tracking-widest text-zinc-500 text-center">
        {label}
      </p>
    </Card>
  );
}

// ─── Topic Evaluation Row ─────────────────────────────────────────────────────

function TopicRow({ item }) {
  const score = item.score ?? item.s ?? 0;
  // Support both 0-10 and 0-100 scales
  const displayScore = score <= 10 ? score : score / 10;
  const percentage = displayScore * 10;

  const color =
    percentage >= 75 ? "text-emerald-400 border-emerald-950 bg-emerald-950/20"
    : percentage >= 55 ? "text-amber-400 border-amber-950 bg-amber-950/20"
    : "text-rose-400 border-rose-950 bg-rose-950/20";

  return (
    <div className="flex items-center justify-between gap-4 rounded-xl border border-zinc-900 bg-zinc-950/30 p-4 transition-all hover:bg-zinc-950/50 hover:border-zinc-800/80 duration-200">
      <div className="flex-1 min-w-0">
        <h4 className="text-sm font-semibold text-zinc-200 tracking-tight capitalize">
          {item.topic || item.axis}
        </h4>
        {item.summary ? (
          <p className="text-xs text-zinc-500 leading-relaxed mt-1">
            {item.summary}
          </p>
        ) : (
          <p className="text-[11px] text-zinc-600 mt-1">
            Topic evaluated and graded during the interactive chat session.
          </p>
        )}
      </div>
      <Badge className={`shrink-0 font-mono text-xs px-2.5 py-1 ${color} border`}>
        {score <= 10 ? `${score}/10` : score}
      </Badge>
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
    if (!report || report.session_id !== id) {
      dispatch(fetchReport(id));
    }
  }, [id]); // eslint-disable-line

  // ── Loading state ───────────────────────────────────────────────────────────
  if (reportLoading) {
    return (
      <AppShell>
        <div className="space-y-6 px-4 py-8 md:px-8 animate-pulse">
          {/* Header toolbar skeleton */}
          <div className="flex items-center justify-between border-b border-border bg-card/10 p-5 rounded-xl">
            <div className="space-y-2 w-1/3">
              <div className="h-5 w-32 rounded bg-zinc-800/40" />
              <div className="h-3 w-48 rounded bg-zinc-800/20" />
            </div>
            <div className="h-8 w-24 rounded bg-zinc-800/40" />
          </div>

          {/* Hero Overall Score Card skeleton */}
          <div className="border border-border bg-card/30 p-6 rounded-xl flex items-center gap-6">
            <div className="w-20 h-20 rounded-full border-4 border-dashed border-zinc-800/60 shrink-0" />
            <div className="space-y-2.5 w-2/3">
              <div className="h-4.5 w-40 rounded bg-zinc-800/40" />
              <div className="h-3.5 w-full rounded bg-zinc-800/20" />
              <div className="h-3 w-4/5 rounded bg-zinc-800/20" />
            </div>
          </div>

          {/* Grid score columns skeleton */}
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="border border-border bg-card/30 p-4 rounded-xl flex flex-col items-center gap-3">
                <div className="w-12 h-12 rounded-full border-4 border-dashed border-zinc-800/40" />
                <div className="h-3 w-16 rounded bg-zinc-800/30" />
              </div>
            ))}
          </div>

          {/* Radar & breakdown placeholders */}
          <div className="grid gap-4 lg:grid-cols-2">
            <div className="border border-border bg-card/30 p-5 rounded-xl h-64 space-y-4">
              <div className="h-4 w-32 rounded bg-zinc-800/40" />
              <div className="h-40 rounded bg-zinc-800/10 border border-dashed border-zinc-800" />
            </div>
            <div className="border border-border bg-card/30 p-5 rounded-xl h-64 space-y-3">
              <div className="h-4 w-36 rounded bg-zinc-800/40" />
              <div className="space-y-2 pt-2">
                <div className="h-7 w-full rounded bg-zinc-850" />
                <div className="h-7 w-full rounded bg-zinc-850" />
                <div className="h-7 w-full rounded bg-zinc-850" />
              </div>
            </div>
          </div>
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
  const overallScore = Math.round((report.overall_score ?? report.score ?? (report.average_score ? (report.average_score * 10) : 0)));

  // Score cards: try common backend field names
  const rawScores = report.scores || {};
  const matrix = report.performance_matrix || {};
  const scoreCards = [
    { 
      k: "Technical", 
      v: rawScores.technical ?? rawScores.technical_knowledge ?? (matrix.correctness ? (matrix.correctness * 10) : 0) 
    },
    { 
      k: "Communication", 
      v: rawScores.communication ?? rawScores.communication_skills ?? (matrix.communication ? (matrix.communication * 10) : 0) 
    },
    { 
      k: "Problem Solving", 
      v: rawScores.problem_solving ?? rawScores.problem_solving_ability ?? (matrix.reasoning ? (matrix.reasoning * 10) : 0) 
    },
    { k: "Overall", v: overallScore },
  ].map((s) => ({ ...s, v: Math.round(s.v) }));

  // Radar data: prefer topic_evaluations, fallback to topic_scores, then fallback to scores keys
  let radarData = [];
  if (Array.isArray(report.topic_evaluations) && report.topic_evaluations.length > 0) {
    radarData = report.topic_evaluations.map((t) => ({
      axis: t.topic,
      s: Math.min(Math.round((t.score ?? 5) * 10), 100),
      score: t.score,
      summary: t.summary,
      topic: t.topic,
    }));
  } else if (report.topic_scores && Object.keys(report.topic_scores).length > 0) {
    radarData = Object.entries(report.topic_scores).map(([k, v]) => ({
      axis: k.replace(/_/g, " "),
      s: Math.min(Math.round((v ?? 5) * 10), 100),
    }));
  } else if (Object.keys(rawScores).length > 0) {
    radarData = Object.entries(rawScores).map(([k, v]) => ({
      axis: k.replace(/_/g, " "),
      s: Math.round(v),
    }));
  }

  const strengths = report.strengths || [];
  const improvements = report.improvements || report.areas_for_improvement || report.concerns || [];
  const recommendations = Array.isArray(report.recommendations) 
    ? report.recommendations 
    : (typeof report.recommendation === "string" && report.recommendation.trim() !== "") 
      ? [report.recommendation] 
      : [];

  let topicEvals = report.topic_evaluations || [];
  if (topicEvals.length === 0 && report.topic_scores) {
    topicEvals = Object.entries(report.topic_scores).map(([k, v]) => ({
      topic: k.replace(/_/g, " "),
      score: v,
    }));
  }

  return (
    <AppShell>
      <div className="flex flex-col gap-1 border-b border-zinc-900 bg-zinc-950/20 px-4 py-6 md:px-8 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-zinc-500">
            <Link to="/app/interviews" className="hover:text-zinc-300 flex items-center gap-1">
              <ArrowLeft className="h-3 w-3" /> Interviews
            </Link>
            <span>/</span>
            <span className="text-zinc-400">Report</span>
          </div>
          <h1 className="text-xl font-bold tracking-tight text-white mt-1">Interview Report</h1>
          <p className="text-xs text-zinc-400 mt-0.5">
            Session · {id?.slice(0, 8)} • {role} ({difficulty})
          </p>
        </div>
        <div className="mt-4 md:mt-0">
          <Button asChild className="bg-primary hover:bg-orange-600 text-white font-medium shadow-md shadow-orange-500/10">
            <Link to="/app/interviews">
              Run another <ArrowRight className="ml-1.5 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>

      <div className="space-y-6 px-4 py-6 md:px-8 max-w-7xl mx-auto">

        {/* ── Overall Score Hero ── */}
        <Card className="border border-zinc-800/80 bg-zinc-950/30 p-6 flex flex-col sm:flex-row items-center gap-6 shadow-xl relative overflow-hidden backdrop-blur-md">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -z-10 pointer-events-none" />
          
          <div className="relative flex items-center justify-center shrink-0">
            {/* Glowing ring shadow */}
            <div className="absolute w-24 h-24 rounded-full blur-2xl opacity-15 bg-primary" />
            <svg width={130} height={130} viewBox="0 0 120 120" className="drop-shadow-[0_4px_10px_rgba(0,0,0,0.5)]">
              <circle cx={60} cy={60} r={52} fill="none" stroke="rgba(255,255,255,0.02)" strokeWidth={8} />
              <circle
                cx={60} cy={60} r={52}
                fill="none"
                stroke={overallScore >= 75 ? "#10b981" : overallScore >= 55 ? "#f59e0b" : "#f43f5e"}
                strokeWidth={8}
                strokeDasharray={`${(overallScore / 100) * 2 * Math.PI * 52} ${2 * Math.PI * 52}`}
                strokeLinecap="round"
                transform="rotate(-90 60 60)"
                style={{ transition: "stroke-dasharray 1.2s cubic-bezier(0.4, 0, 0.2, 1)" }}
              />
            </svg>
            <div className="absolute flex flex-col items-center">
              <span className="text-3xl font-black text-white tracking-tight">{overallScore}</span>
              <span className="text-[10px] text-zinc-500 font-bold uppercase tracking-wider">/ 100</span>
            </div>
          </div>
          
          <div className="flex-1 text-center sm:text-left">
            <div className="flex items-center gap-2 justify-center sm:justify-start mb-1.5">
              <Trophy className="h-5 w-5 text-primary animate-pulse" />
              <h2 className="text-lg font-bold text-white tracking-tight">Performance Assessment</h2>
            </div>
            <p className="text-sm text-zinc-400 leading-relaxed max-w-2xl">
              {overallScore >= 80
                ? "Outstanding! You displayed excellent architectural depth, solid technical fundamentals, and concise professional communication. Ready for high-stakes loops."
                : overallScore >= 65
                ? "Good performance. You mapped out clear baseline signals, but have specific points of code optimization or structural refinement to reach the top tier."
                : "Keep practicing. The session highlights key conceptual or structural improvement areas. Focus on deep-dives in the topics flagged below to unlock higher ratings."}
            </p>
            
            <div className="mt-4 flex flex-wrap gap-2 justify-center sm:justify-start items-center">
              <Badge className="bg-primary/10 text-primary border-primary/20 hover:bg-primary/20 font-semibold">{role}</Badge>
              <Badge variant="outline" className="border-zinc-800 bg-zinc-900/40 text-zinc-400 capitalize">{difficulty}</Badge>
              <span className="h-3 w-px bg-zinc-800 mx-1 hidden sm:inline" />
              <span className="text-xs text-zinc-500 flex items-center gap-1">
                <Activity className="h-3.5 w-3.5" /> Answers Graded: {report.questions_answered ?? 0}
              </span>
            </div>

            {report.behavior_flags && report.behavior_flags.length > 0 && (
              <div className="mt-3.5 flex flex-wrap gap-1.5 justify-center sm:justify-start items-center">
                <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider mr-1">Signals Detected:</span>
                {report.behavior_flags.map((f, i) => (
                  <Badge key={i} className="bg-rose-500/10 text-rose-400 border-rose-950 text-[10px] py-0.5 font-mono font-medium">
                    ⚠️ {f}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        </Card>

        {/* ── Score Cards Grid ── */}
        <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
          {scoreCards.map((s) => (
            <ScoreRing key={s.k} value={s.v} label={s.k} />
          ))}
        </div>

        {/* ── Radar + Topic Evals ── */}
        <div className="grid gap-6 lg:grid-cols-2">
          {radarData.length > 0 && (
            <Card className="border border-zinc-800/80 bg-zinc-950/20 backdrop-blur-sm p-6 shadow-xl flex flex-col justify-between">
              <div className="flex items-center gap-2 mb-6">
                <Target className="h-4.5 w-4.5 text-primary" />
                <h3 className="text-sm font-semibold text-white tracking-tight">Skills Analytics Radar</h3>
              </div>
              <div className="h-72 flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    {/* Dark Grid Lines */}
                    <PolarGrid stroke="rgba(255,255,255,0.05)" />
                    {/* Clear White Tick Labels on Dark Background */}
                    <PolarAngleAxis
                      dataKey="axis"
                      tick={{ fontSize: 10, fill: "#e4e4e7", fontWeight: 500 }}
                    />
                    <PolarRadiusAxis tick={false} axisLine={false} domain={[0, 100]} />
                    <Radar
                      dataKey="s"
                      stroke="#f97316"
                      fill="#f97316"
                      fillOpacity={0.18}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "#09090b",
                        border: "1px solid #27272a",
                        borderRadius: 8,
                        fontSize: 11,
                        color: "#f4f4f5"
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          {topicEvals.length > 0 && (
            <Card className="border border-zinc-800/80 bg-zinc-950/20 backdrop-blur-sm p-6 shadow-xl flex flex-col justify-between">
              <div className="flex items-center gap-2 mb-6">
                <TrendingUp className="h-4.5 w-4.5 text-primary" />
                <h3 className="text-sm font-semibold text-white tracking-tight">Topic Breakdowns</h3>
              </div>
              <div className="space-y-3 overflow-y-auto max-h-72 pr-1 custom-scrollbar">
                {topicEvals.map((t, i) => (
                  <TopicRow key={i} item={t} />
                ))}
              </div>
            </Card>
          )}
        </div>

        {/* ── Strengths + Improvements ── */}
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Strengths Card */}
          <Card className="border border-zinc-800/80 bg-zinc-950/20 backdrop-blur-sm p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="p-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <Check className="h-4 w-4 text-emerald-400" />
              </div>
              <h3 className="text-sm font-bold text-emerald-400 tracking-tight">✓ Strengths & Highlights</h3>
            </div>
            
            {strengths.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-center border border-dashed border-zinc-900 rounded-xl bg-zinc-950/10">
                <Sparkles className="h-7 w-7 text-zinc-700 mb-2.5" />
                <p className="text-xs font-semibold text-zinc-400">No core strengths highlighted yet</p>
                <p className="text-[10px] text-zinc-500 max-w-xs mt-1 leading-relaxed px-4">
                  Focus on providing detailed examples, mapping trade-offs, and showing core technical concepts in your next chat.
                </p>
              </div>
            ) : (
              <ul className="space-y-2.5">
                {strengths.map((x, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-zinc-300">
                    <span className="mt-1 w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" />
                    <span className="leading-relaxed">
                      {typeof x === "string" ? x : x.text || x.description || JSON.stringify(x)}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          {/* Areas to Improve Card */}
          <Card className="border border-zinc-800/80 bg-zinc-950/20 backdrop-blur-sm p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="p-1.5 rounded-lg bg-rose-500/10 border border-rose-500/20">
                <X className="h-4 w-4 text-rose-400" />
              </div>
              <h3 className="text-sm font-bold text-rose-400 tracking-tight">✗ Areas to Optimize</h3>
            </div>

            {improvements.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-center border border-dashed border-zinc-900 rounded-xl bg-zinc-950/10">
                <Award className="h-7 w-7 text-emerald-500/80 mb-2.5" />
                <p className="text-xs font-semibold text-zinc-400">No significant gaps flagged</p>
                <p className="text-[10px] text-zinc-500 max-w-xs mt-1 leading-relaxed px-4">
                  Excellent signal density! Keep pushing your difficulty level to explore senior design limits.
                </p>
              </div>
            ) : (
              <ul className="space-y-2.5">
                {improvements.map((x, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-zinc-300">
                    <span className="mt-1 w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0" />
                    <span className="leading-relaxed">
                      {typeof x === "string" ? x : x.text || x.description || JSON.stringify(x)}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>

        {/* ── Recommendations ── */}
        {recommendations.length > 0 && (
          <Card className="border border-zinc-800/80 bg-zinc-950/20 backdrop-blur-sm p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="p-1.5 rounded-lg bg-primary/10 border border-primary/20">
                <BookOpen className="h-4 w-4 text-primary" />
              </div>
              <h3 className="text-sm font-bold text-white tracking-tight">Evaluation & Next Milestones</h3>
            </div>
            <ul className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
              {recommendations.map((x, i) => (
                <li
                  key={i}
                  className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-4 text-xs text-zinc-400 leading-relaxed hover:border-zinc-850 hover:bg-zinc-950/50 transition-all duration-300"
                >
                  <div className="flex items-center gap-1.5 mb-1.5 font-bold font-mono text-[10px] text-zinc-500 uppercase tracking-wider">
                    <Zap className="h-3 w-3 text-primary animate-pulse" /> Milestone #{i+1}
                  </div>
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
