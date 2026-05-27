from __future__ import annotations

from typing import Any


class InterviewReportService:
    @staticmethod
    def build_report(state: dict[str, Any]) -> dict[str, Any]:
        evaluations = state.get("evaluations", [])
        turns = state.get("turns", [])
        evaluated_turns = [
            turn for turn in turns if turn.get("topic") != "self_introduction"
        ]
        scores = [float(item.get("score", 0)) for item in evaluations]
        average_score = round(sum(scores) / len(scores), 2) if scores else 0

        topic_scores: dict[str, list[float]] = {}
        for turn in evaluated_turns:
            topic = turn.get("topic", "unknown")
            score = float((turn.get("evaluation") or {}).get("score", 0))
            topic_scores.setdefault(topic, []).append(score)

        topic_summary = {
            topic: round(sum(values) / len(values), 2)
            for topic, values in topic_scores.items()
        }

        strengths = _top_items(evaluations, "strengths")
        concerns = _top_items(evaluations, "concerns")

        return {
            "session_id": state.get("session_id"),
            "role": state.get("role"),
            "interview_type": state.get("interview_type"),
            "status": state.get("status", "active"),
            "questions_answered": len(evaluated_turns),
            "intro_answer": state.get("candidate_introduction", ""),
            "average_score": average_score,
            "topic_scores": topic_summary,
            "covered_topics": state.get("covered_topics", []),
            "remaining_topics": state.get("remaining_topics", []),
            "weak_topics": state.get("weak_topics", []),
            "strengths": strengths,
            "concerns": concerns,
            "recommendation": _recommendation(average_score),
            "turns": turns,
        }


def _top_items(evaluations: list[dict[str, Any]], key: str) -> list[str]:
    seen = set()
    items: list[str] = []
    for evaluation in evaluations:
        for item in evaluation.get(key, []):
            normalized = str(item).strip()
            marker = normalized.lower()
            if normalized and marker not in seen:
                seen.add(marker)
                items.append(normalized)
    return items[:8]


def _recommendation(score: float) -> str:
    if score >= 8:
        return "Strong interview performance. Increase difficulty and focus on senior-level tradeoffs."
    if score >= 6:
        return "Solid baseline. Continue targeted practice on weaker topics and answer depth."
    if score >= 4:
        return "Mixed signal. Prioritize fundamentals, clearer structure, and targeted follow-ups."
    return "Needs focused preparation before a high-stakes interview loop."
