"""
completion_node.py
──────────────────
Decides whether the interview is done and generates a human-like closing.
The closing is context-aware — it reacts to the candidate's performance.
"""
from __future__ import annotations

from app.ai.graph.state import InterviewState


async def completion_node(state: InterviewState):
    turns = state.get("turns", [])
    # Only count substantive turns (skip self-intro)
    substantive_turns = [t for t in turns if t.get("topic") != "self_introduction"]
    turn_count = len(substantive_turns)

    max_q = max(1, int(state.get("max_questions", 8)) - 1)
    min_q = max(1, int(state.get("min_questions", 5)) - 1)
    remaining = state.get("remaining_topics", [])

    if turn_count >= max_q:
        return _done(state, "max_questions_reached")

    if turn_count >= min_q and not remaining:
        return _done(state, "topic_coverage_complete")

    return {
        "completed": False,
        "status": "active",
        "completion_reason": "",
        "closing_message": "",
    }


def _done(state: InterviewState, reason: str) -> dict:
    return {
        "completed": True,
        "status": "completed",
        "interview_phase": "completed",
        "completion_reason": reason,
        "closing_message": _closing_message(state, reason),
    }


def _closing_message(state: InterviewState, reason: str) -> str:
    role = state.get("role") or "this role"
    evaluations = state.get("evaluations", [])
    avg_score = 0.0
    if evaluations:
        scores = [float(e.get("score", 0)) for e in evaluations]
        avg_score = sum(scores) / len(scores)

    behavior_flags = []
    for e in evaluations:
        behavior_flags.extend(e.get("behavior_flags") or [])
    has_behavior_concerns = len(behavior_flags) > 0

    # Human-like closing based on overall performance
    if avg_score >= 8:
        performance_line = "You demonstrated strong command across the topics we covered."
    elif avg_score >= 6:
        performance_line = "There were solid moments — a few areas to sharpen, but a respectable run."
    elif avg_score >= 4:
        performance_line = "Mixed signals overall. There's a clear foundation, but depth and precision need work."
    else:
        performance_line = "We covered the key areas. There's meaningful ground to cover before a live loop."

    if has_behavior_concerns:
        behavior_line = " I'd also encourage approaching interviews with more patience — it matters how you show up."
    else:
        behavior_line = ""

    if reason == "max_questions_reached":
        return (
            f"That's all for the {role} session. "
            f"{performance_line}{behavior_line} "
            "Your full report is ready."
        )

    return (
        f"We've covered everything I wanted to assess for the {role} role. "
        f"{performance_line}{behavior_line} "
        "Your report is ready."
    )
