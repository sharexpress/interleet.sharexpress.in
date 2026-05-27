from app.ai.graph.state import InterviewState


async def completion_node(state: InterviewState):
    turn_count = len(
        [
            turn
            for turn in state.get("turns", [])
            if turn.get("topic") != "self_introduction"
        ]
    )
    max_questions = max(1, int(state.get("max_questions", 8)) - 1)
    min_questions = max(1, int(state.get("min_questions", 5)) - 1)
    remaining_topics = state.get("remaining_topics", [])

    if turn_count >= max_questions:
        return {
            "completed": True,
            "status": "completed",
            "interview_phase": "completed",
            "completion_reason": "max_questions_reached",
        }

    if turn_count >= min_questions and not remaining_topics:
        return {
            "completed": True,
            "status": "completed",
            "interview_phase": "completed",
            "completion_reason": "topic_coverage_complete",
        }

    return {
        "completed": False,
        "status": "active",
        "completion_reason": "",
    }
