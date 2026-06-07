from __future__ import annotations

from typing import Any


class InterviewReportService:
    @staticmethod
    def build_report(state: dict[str, Any]) -> dict[str, Any]:
        evaluations = state.get("evaluations", [])
        turns = state.get("turns", [])

        # Exclude self-introduction from scored stats
        scored_turns = [t for t in turns if t.get("topic") != "self_introduction"]

        scores = [float(e.get("score", 0)) for e in evaluations]
        average_score = round(sum(scores) / len(scores), 2) if scores else 0

        # Per-topic rolling averages
        topic_scores: dict[str, list[float]] = {}
        for turn in scored_turns:
            topic = turn.get("topic", "unknown")
            ev = turn.get("evaluation") or {}
            score = float(ev.get("score", 0))
            topic_scores.setdefault(topic, []).append(score)

        topic_summary = {
            topic: round(sum(vals) / len(vals), 2)
            for topic, vals in topic_scores.items()
        }

        # Professionalism
        prof_scores = [float(e.get("professionalism_score", 10)) for e in evaluations]
        avg_professionalism = round(sum(prof_scores) / len(prof_scores), 2) if prof_scores else 10.0

        all_behavior_flags: list[str] = []
        for e in evaluations:
            all_behavior_flags.extend(e.get("behavior_flags") or [])
        # Deduplicate while preserving order
        seen: set[str] = set()
        unique_flags: list[str] = []
        for f in all_behavior_flags:
            norm = f.lower().strip()
            if norm not in seen:
                seen.add(norm)
                unique_flags.append(f)

        strengths = _top_items(evaluations, "strengths")
        concerns  = _top_items(evaluations, "concerns")
        performance_matrix = _performance_matrix(evaluations)

        return {
            "session_id":           state.get("session_id"),
            "role":                 state.get("role"),
            "interview_type":       state.get("interview_type"),
            "status":               state.get("status", "active"),
            "questions_answered":   len(scored_turns),
            "intro_answer":         state.get("candidate_introduction", ""),
            "average_score":        average_score,
            "avg_professionalism":  avg_professionalism,
            "behavior_flags":       unique_flags,
            "topic_scores":         topic_summary,
            "performance_matrix":   performance_matrix,
            "covered_topics":       state.get("covered_topics", []),
            "remaining_topics":     state.get("remaining_topics", []),
            "weak_topics":          state.get("weak_topics", []),
            "strengths":            strengths,
            "concerns":             concerns,
            "recommendation":       _recommendation(average_score, avg_professionalism),
            "turns":                turns,
        }


def _top_items(evaluations: list[dict[str, Any]], key: str) -> list[str]:
    seen: set[str] = set()
    items: list[str] = []
    for ev in evaluations:
        for item in ev.get(key, []):
            normalized = str(item).strip()
            marker = normalized.lower()
            if normalized and marker not in seen:
                seen.add(marker)
                items.append(normalized)
    return items[:8]


def _performance_matrix(evaluations: list[dict[str, Any]]) -> dict[str, float]:
    metrics = [
        "correctness",
        "depth",
        "communication",
        "confidence",
        "structure",
        "clarity",
        "role_fit",
        "reasoning",
        "emotional_intelligence",
        "professionalism_score",
    ]
    result: dict[str, float] = {}
    for metric in metrics:
        values = [
            float(ev.get(metric, 0))
            for ev in evaluations
            if ev.get(metric) is not None
        ]
        result[metric] = round(sum(values) / len(values), 2) if values else 0
    return result


def _recommendation(score: float, professionalism: float) -> str:
    if professionalism < 5:
        return (
            "The interview was significantly impacted by professionalism concerns. "
            "Technical skill alone is not enough — how you conduct yourself matters equally. "
            "Focus on communication style and professional etiquette before the next session."
        )
    if score >= 8:
        return "Strong interview performance. Increase difficulty and focus on senior-level tradeoffs."
    if score >= 6:
        return "Solid baseline. Continue targeted practice on weaker topics and answer depth."
    if score >= 4:
        return "Mixed signal. Prioritize fundamentals, clearer structure, and targeted follow-ups."
    return "Needs focused preparation before a high-stakes interview loop."
