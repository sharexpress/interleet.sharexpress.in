from __future__ import annotations

import uuid
from typing import Any

from app.ai.graph.nodes.completion_node import completion_node
from app.ai.graph.nodes.context_node import context_node
from app.ai.graph.nodes.difficulty_node import difficulty_node
from app.ai.graph.nodes.evaluation_node import evaluation_node
from app.ai.graph.nodes.question_node import question_node
from app.ai.graph.state import InterviewState
from app.ai.schemas.interview import InterviewStateModel


def build_initial_state(payload: dict[str, Any]) -> InterviewState:
    mock_test = payload.get("mock_test", payload)
    parsed_resume = payload.get("parsed_resume", {})

    role = mock_test.get("role") or mock_test.get("target_role") or payload.get("role", "")
    interview_type = _normalize_interview_type(
        mock_test.get("interview_type") or payload.get(
        "interview_type", "technical"
        )
    )
    skills = _as_list(parsed_resume.get("skills") or mock_test.get("skills"))
    projects = _as_list(parsed_resume.get("projects"))
    technologies = _as_list(
        parsed_resume.get("technologies") or mock_test.get("technologies")
    )
    experience = _as_list(parsed_resume.get("experience"))
    jd = mock_test.get("jd") or mock_test.get("job_description") or payload.get("jd", "")
    max_questions = int(mock_test.get("max_questions", payload.get("max_questions", 8)))
    min_questions = int(mock_test.get("min_questions", payload.get("min_questions", 5)))
    explicit_topics = _as_list(mock_test.get("topics"))
    target_topics = _select_target_topics(
        explicit_topics=explicit_topics,
        skills=skills,
        technologies=technologies,
        interview_type=interview_type,
        max_questions=max_questions,
    )

    if not target_topics:
        target_topics = _default_topics(interview_type)

    model = InterviewStateModel(
        session_id=payload.get("session_id") or str(uuid.uuid4()),
        role=role,
        interview_type=interview_type,
        difficulty=mock_test.get("difficulty", "medium"),
        jd=jd,
        additional_context=payload.get("additional_context", ""),
        candidate_summary=str(parsed_resume.get("summary", "")),
        skills=skills,
        projects=projects,
        technologies=technologies,
        experience=experience,
        target_topics=target_topics,
        remaining_topics=target_topics,
        max_questions=max_questions,
        min_questions=min_questions,
        metadata={
            "mock_test": mock_test,
            "question_budget_includes_intro": True,
            "assessment_dimensions": _assessment_dimensions(interview_type),
        },
    )
    return model.model_dump(mode="json")


async def run_interview_graph(state: InterviewState) -> InterviewState:
    graph = _build_langgraph()
    if graph is not None:
        return await graph.ainvoke(state)
    return await _run_manual_graph(state)


def _build_langgraph():
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError:
        return None

    workflow = StateGraph(InterviewState)
    workflow.add_node("question", question_node)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("context", context_node)
    workflow.add_node("difficulty", difficulty_node)
    workflow.add_node("completion", completion_node)

    workflow.add_conditional_edges(
        START,
        _entrypoint,
        {
            "answer": "evaluation",
            "intro_answer": "context",
            "question": "question",
        },
    )
    workflow.add_edge("evaluation", "context")
    workflow.add_conditional_edges(
        "context",
        _after_context,
        {
            "intro_continue": "question",
            "evaluate_completion": "difficulty",
        },
    )
    workflow.add_edge("difficulty", "completion")
    workflow.add_conditional_edges(
        "completion",
        _after_completion,
        {
            "complete": END,
            "continue": "question",
        },
    )
    workflow.add_edge("question", END)
    return workflow.compile()


async def _run_manual_graph(state: InterviewState) -> InterviewState:
    if _entrypoint(state) == "question":
        return {**state, **await question_node(state)}

    if _entrypoint(state) == "intro_answer":
        current = {**state, **await context_node(state)}
        return {**current, **await question_node(current)}

    current = {**state, **await evaluation_node(state)}
    current = {**current, **await context_node(current)}
    current = {**current, **await difficulty_node(current)}
    current = {**current, **await completion_node(current)}
    if _after_completion(current) == "complete":
        return current
    return {**current, **await question_node(current)}


def _entrypoint(state: InterviewState) -> str:
    if not state.get("last_answer"):
        return "question"
    if state.get("current_topic") == "self_introduction":
        return "intro_answer"
    return "answer"


def _after_completion(state: InterviewState) -> str:
    return "complete" if state.get("completed") else "continue"


def _after_context(state: InterviewState) -> str:
    if state.get("interview_phase") == "adaptive_questions" and not state.get("last_evaluation"):
        return "intro_continue"
    return "evaluate_completion"


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def _dedupe(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        normalized = value.strip()
        key = normalized.lower()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result


def _default_topics(interview_type: str) -> list[str]:
    presets = {
        "frontend": ["frontend architecture", "state management", "performance", "accessibility", "collaboration"],
        "backend": ["API design", "data modeling", "caching", "reliability", "communication"],
        "devops": ["CI/CD", "containers", "cloud infrastructure", "monitoring", "incident response"],
        "system_design": ["requirements", "data model", "scaling", "tradeoffs", "risk handling"],
        "behavioral": ["ownership", "conflict", "failure", "leadership", "communication"],
        "hr": ["motivation", "collaboration", "strengths", "role fit", "career goals"],
    }
    return presets.get(interview_type.lower(), presets["backend"])


def _normalize_interview_type(value: Any) -> str:
    normalized = str(value or "technical").strip().lower()
    aliases = {
        "behaviour": "behavioral",
        "behavioural": "behavioral",
        "behavior": "behavioral",
    }
    return aliases.get(normalized, normalized)


def _select_target_topics(
    *,
    explicit_topics: list[str],
    skills: list[str],
    technologies: list[str],
    interview_type: str,
    max_questions: int,
) -> list[str]:
    topic_budget = max(2, max_questions - 1)
    if explicit_topics:
        return _dedupe(explicit_topics)[:topic_budget]

    source_topics = _default_topics(interview_type)
    evidence = [*skills[:2], *technologies[:2]]
    return _dedupe([*source_topics, *evidence])[:topic_budget]


def _assessment_dimensions(interview_type: str) -> list[str]:
    common = ["communication clarity", "structured thinking", "role fit"]
    if interview_type in {"hr", "behavioral"}:
        return [*common, "self-awareness", "ownership", "collaboration", "emotional intelligence"]
    return [
        *common,
        "technical depth",
        "systems reasoning",
        "tradeoff analysis",
        "problem solving under ambiguity",
    ]
