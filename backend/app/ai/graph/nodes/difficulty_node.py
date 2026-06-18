from app.ai.graph.state import InterviewState


_DIFFICULTY_ORDER = ["easy", "medium", "hard", "staff"]


async def difficulty_node(state: InterviewState):
    evaluation = state.get("last_evaluation") or {}
    current = state.get("difficulty", "medium")
    index = _DIFFICULTY_ORDER.index(current) if current in _DIFFICULTY_ORDER else 1
    score = float(evaluation.get("score", 0))

    # Read target difficulty limit from metadata
    metadata = state.get("metadata") or {}
    target = metadata.get("target_difficulty", "medium")
    max_allowed = _DIFFICULTY_ORDER.index(target) if target in _DIFFICULTY_ORDER else 2

    if score >= 8 and index < len(_DIFFICULTY_ORDER) - 1:
        if index < max_allowed:
            index += 1
    elif score < 5 and index > 0:
        index -= 1

    return {"difficulty": _DIFFICULTY_ORDER[index]}
