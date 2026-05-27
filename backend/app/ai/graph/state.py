from typing import Any, Literal, TypedDict


class AnswerEvaluationState(TypedDict, total=False):
    score: float
    signal: Literal["strong", "mixed", "weak"]
    correctness: float
    depth: float
    communication: float
    concerns: list[str]
    strengths: list[str]
    follow_up_needed: bool
    follow_up_reason: str


class InterviewTurnState(TypedDict, total=False):
    question: str
    answer: str
    topic: str
    difficulty: str
    evaluation: AnswerEvaluationState


class InterviewState(TypedDict, total=False):
    session_id: str
    role: str
    interview_type: str
    difficulty: str
    status: str
    jd: str
    additional_context: str
    candidate_summary: str
    candidate_introduction: str
    interview_phase: str
    skills: list[str]
    projects: list[str]
    technologies: list[str]
    experience: list[str]
    target_topics: list[str]
    current_question: str
    current_preamble: str
    current_topic: str
    current_intent: str
    questions_asked: list[str]
    turns: list[InterviewTurnState]
    evaluations: list[AnswerEvaluationState]
    covered_topics: list[str]
    remaining_topics: list[str]
    weak_topics: list[str]
    current_question_index: int
    last_answer: str
    last_answer_topic: str
    last_evaluation: AnswerEvaluationState | None
    max_questions: int
    min_questions: int
    completed: bool
    completion_reason: str
    metadata: dict[str, Any]
