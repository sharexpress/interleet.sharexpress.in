"""
evaluation_node.py
──────────────────
Evaluates every candidate answer — including professionalism.

IMPORTANT: This node does NOT modify state.turns.
The context_node is the single owner of turn appending.
evaluation_node only produces last_evaluation, evaluations[], and weak_topics.
It also persists a partial report snapshot to DB so mid-session exits work.
"""
from __future__ import annotations

from app.ai.graph.state import InterviewState
from app.ai.prompts.evaluation_prompt import EVALUATION_PROMPT
from app.ai.prompts.system_prompt import INTERVIEW_SYSTEM_PROMPT
from app.ai.schemas.interview import AnswerEvaluation
from app.ai.services.ai_client import ai_client


async def evaluation_node(state: InterviewState):
    last_answer = (state.get("last_answer") or "").strip()
    turns       = state.get("turns", [])

    # Build conversation context so evaluator can judge professionalism patterns
    history_snippet   = _build_history_snippet(turns[-6:])
    all_behavior_flags = _all_behavior_flags(turns)

    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
Difficulty: {state.get("difficulty", "medium")}
Question: {state.get("current_question", "")}
Topic: {state.get("current_topic", "")}
Question intent: {state.get("current_intent", "")}
Expected signal: {state.get("current_expected_signal", "")}
JD (first 400 chars): {(state.get("jd") or "")[:400]}
Candidate summary: {state.get("candidate_summary", "")}

Candidate answer:
{last_answer}

Recent conversation context (for professionalism judgement):
{history_snippet}

Cumulative behavior flags so far: {all_behavior_flags}
"""

    evaluation = await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{EVALUATION_PROMPT}",
        user=user_prompt,
        schema=AnswerEvaluation,
        temperature=0,
    )

    # Enforce professionalism cap
    if evaluation.professionalism_score < 5:
        evaluation.score = min(evaluation.score, 5.0)

    eval_dict    = evaluation.model_dump()
    evaluations  = [*state.get("evaluations", []), eval_dict]

    # Mark weak topics
    weak_topics  = list(state.get("weak_topics", []))
    current_topic = state.get("current_topic", "")
    if evaluation.score < 6 and current_topic and current_topic not in weak_topics:
        weak_topics.append(current_topic)

    # ── Persist partial report snapshot after every evaluated turn ─────────
    # We build it from the current turns + the NEW evaluation we just produced.
    # context_node hasn't run yet, so we simulate what the new turn will look like.
    session_id = state.get("session_id")
    if session_id:
        _try_persist_snapshot(state, eval_dict, evaluations, weak_topics, session_id)

    return {
        "last_evaluation": eval_dict,
        "evaluations":     evaluations,
        "weak_topics":     weak_topics,
        # NOTE: "turns" is intentionally NOT returned here.
        # context_node owns all turn appending.
    }


def _try_persist_snapshot(state, eval_dict, evaluations, weak_topics, session_id):
    """Fire-and-forget partial report save (never blocks the graph)."""
    import asyncio

    async def _save():
        try:
            from app.ai.services.report_service import InterviewReportService
            from app.ai.services.report_repository import InterviewReportRepository

            # Simulate the upcoming turn record for an accurate snapshot
            pending_turn = {
                "question":   state.get("current_question", ""),
                "answer":     state.get("last_answer", ""),
                "topic":      state.get("current_topic", ""),
                "difficulty": state.get("difficulty", "medium"),
                "evaluation": eval_dict,
            }
            snapshot_state = {
                **state,
                "turns":       [*state.get("turns", []), pending_turn],
                "evaluations": evaluations,
                "weak_topics": weak_topics,
            }
            report = InterviewReportService.build_report(snapshot_state)
            report["status"] = "partial"
            await InterviewReportRepository.save_report(
                session_id=session_id,
                report=report,
                state=snapshot_state,
            )
        except Exception:
            pass  # Never let snapshot persistence crash the interview

    # Schedule as a background task so it doesn't block the graph pipeline
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(_save())
    except Exception:
        pass


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_history_snippet(recent_turns: list[dict]) -> str:
    lines = []
    for t in recent_turns:
        lines.append(f"Q: {t.get('question', '')}")
        lines.append(f"A: {t.get('answer', '')}")
        ev = t.get("evaluation") or {}
        if ev:
            flags = ev.get("behavior_flags") or []
            lines.append(
                f"Professionalism: {ev.get('professionalism_score', 10)}/10"
                + (f" — flags: {flags}" if flags else "")
            )
        lines.append("")
    return "\n".join(lines)


def _all_behavior_flags(turns: list[dict]) -> list[str]:
    flags: list[str] = []
    for t in turns:
        ev = t.get("evaluation") or {}
        flags.extend(ev.get("behavior_flags") or [])
    return flags
