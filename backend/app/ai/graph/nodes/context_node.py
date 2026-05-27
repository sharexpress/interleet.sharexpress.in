from app.ai.graph.state import InterviewState


async def context_node(state: InterviewState):
    topic = state.get("current_topic") or state.get("last_answer_topic", "")
    is_intro = topic == "self_introduction"
    covered_topics = list(state.get("covered_topics", []))
    if not is_intro:
        for covered_topic in _detect_covered_topics(state, topic):
            if covered_topic not in covered_topics:
                covered_topics.append(covered_topic)

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


def _detect_covered_topics(state: InterviewState, generated_topic: str) -> list[str]:
    target_topics = state.get("target_topics", [])
    haystack = " ".join(
        [
            generated_topic,
            state.get("current_question", ""),
            state.get("last_answer", ""),
        ]
    ).lower()

    matched = [
        topic
        for topic in target_topics
        if topic.lower() in haystack or haystack in topic.lower()
    ]

    if matched:
        return matched
    return [generated_topic] if generated_topic else []
