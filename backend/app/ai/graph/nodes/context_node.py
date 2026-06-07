"""
context_node.py
────────────────
The single node responsible for appending the completed turn to state.turns.

Turn record includes the evaluation from evaluation_node (via last_evaluation).
For the intro path (self_introduction), evaluation is skipped, so we record
an empty evaluation dict.
"""
from app.ai.graph.state import InterviewState


async def context_node(state: InterviewState):
    topic    = state.get("current_topic") or state.get("last_answer_topic", "")
    is_intro = topic == "self_introduction"

    # ── Append the completed turn ─────────────────────────────────────────────
    # For intro: no evaluation ran, so evaluation={}.
    # For regular answers: evaluation_node put the result in last_evaluation.
    turn = {
        "question":   state.get("current_question", ""),
        "answer":     state.get("last_answer", ""),
        "topic":      topic,
        "difficulty": state.get("difficulty", "medium"),
        "evaluation": {} if is_intro else (state.get("last_evaluation") or {}),
    }
    turns = [*state.get("turns", []), turn]

    # ── Covered / remaining topic tracking ────────────────────────────────────
    covered_topics = list(state.get("covered_topics", []))
    if not is_intro:
        for matched in _detect_covered_topics(state, topic):
            if matched not in covered_topics:
                covered_topics.append(matched)

    remaining_topics = [
        t for t in state.get("target_topics", [])
        if t not in covered_topics
    ]

    interview_phase = (
        "adaptive_questions"
        if is_intro
        else state.get("interview_phase", "adaptive_questions")
    )

    return {
        "turns":                  turns,
        "covered_topics":         covered_topics,
        "remaining_topics":       remaining_topics,
        "candidate_introduction": state.get("last_answer", "")
                                  if is_intro
                                  else state.get("candidate_introduction", ""),
        "interview_phase":        interview_phase,
        # Clear transient fields so entrypoint doesn't re-trigger evaluation
        "last_answer":       "",
        "last_answer_topic": "",
    }


def _detect_covered_topics(state: InterviewState, generated_topic: str) -> list[str]:
    target_topics = state.get("target_topics", [])
    haystack = " ".join([
        generated_topic,
        state.get("current_question", ""),
        state.get("last_answer", ""),
    ]).lower()

    matched = [
        t for t in target_topics
        if t.lower() in haystack or haystack in t.lower()
    ]
    return matched if matched else ([generated_topic] if generated_topic else [])
