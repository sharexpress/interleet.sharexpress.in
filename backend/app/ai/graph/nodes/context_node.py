from app.ai.graph.state import InterviewState


async def context_node(state: InterviewState):
    topic = state.get("current_topic") or state.get("last_answer_topic", "")
    is_intro = topic == "self_introduction"
    covered_topics = list(state.get("covered_topics", []))
    if topic and not is_intro and topic not in covered_topics:
        covered_topics.append(topic)

    remaining_topics = [
        item for item in state.get("target_topics", []) if item not in covered_topics
    ]

    turn = {
        "question": state.get("current_question", ""),
        "answer": state.get("last_answer", ""),
        "topic": topic,
        "difficulty": state.get("difficulty", "medium"),
        "evaluation": state.get("last_evaluation") or {},
    }

    return {
        "turns": [*state.get("turns", []), turn],
        "covered_topics": covered_topics,
        "remaining_topics": remaining_topics,
        "candidate_introduction": state.get("last_answer", "")
        if is_intro
        else state.get("candidate_introduction", ""),
        "interview_phase": "adaptive_questions" if is_intro else state.get("interview_phase", "adaptive_questions"),
        "last_answer": "",
        "last_answer_topic": "",
    }
