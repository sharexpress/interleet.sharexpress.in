from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    STAFF = "staff"


class InterviewStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class InterviewPhase(str, Enum):
    INTRO = "intro"
    ADAPTIVE_QUESTIONS = "adaptive_questions"
    COMPLETED = "completed"


class InterviewTurn(BaseModel):
    question: str
    answer: str
    topic: str
    difficulty: Difficulty
    evaluation: "AnswerEvaluation"


class AnswerEvaluation(BaseModel):
    score: float = Field(ge=0, le=10)
    signal: Literal["strong", "mixed", "weak"]
    correctness: float = Field(ge=0, le=10)
    depth: float = Field(ge=0, le=10)
    communication: float = Field(ge=0, le=10)
    concerns: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    follow_up_needed: bool = False
    follow_up_reason: str = ""


class GeneratedQuestion(BaseModel):
    preamble: str = ""
    question: str
    topic: str
    difficulty: Difficulty
    intent: str = ""
    expected_signal: str = ""


class OpeningQuestion(BaseModel):
    preamble: str = ""
    question: str
    tone: str = "professional"


class InterviewStateModel(BaseModel):
    session_id: str
    role: str
    interview_type: str
    status: InterviewStatus = InterviewStatus.ACTIVE
    difficulty: Difficulty = Difficulty.MEDIUM
    jd: str = ""
    additional_context: str = ""
    candidate_summary: str = ""
    candidate_introduction: str = ""
    interview_phase: InterviewPhase = InterviewPhase.INTRO
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    target_topics: list[str] = Field(default_factory=list)
    covered_topics: list[str] = Field(default_factory=list)
    remaining_topics: list[str] = Field(default_factory=list)
    weak_topics: list[str] = Field(default_factory=list)
    current_question: str = ""
    current_preamble: str = ""
    current_topic: str = ""
    current_intent: str = ""
    current_question_index: int = 0
    questions_asked: list[str] = Field(default_factory=list)
    turns: list[InterviewTurn] = Field(default_factory=list)
    evaluations: list[AnswerEvaluation] = Field(default_factory=list)
    last_answer: str = ""
    last_answer_topic: str = ""
    last_evaluation: AnswerEvaluation | None = None
    max_questions: int = 8
    min_questions: int = 5
    completed: bool = False
    completion_reason: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


InterviewTurn.model_rebuild()
