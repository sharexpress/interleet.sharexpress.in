# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Literal, TypedDict


class AnswerEvaluationState(TypedDict, total=False):
    score: float
    signal: Literal["strong", "mixed", "weak"]
    correctness: float
    depth: float
    communication: float
    confidence: float
    structure: float
    clarity: float
    role_fit: float
    reasoning: float
    emotional_intelligence: float
    professionalism_score: float
    behavior_flags: list[str]
    concerns: list[str]
    strengths: list[str]
    follow_up_needed: bool
    follow_up_reason: str
    summary: str


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
    current_affect: str
    current_answer_guidance: str
    current_topic: str
    current_intent: str
    current_expected_signal: str
    questions_asked: list[str]
    interviewer_messages: list[str]
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
    closing_message: str
    user_id: str
    metadata: dict[str, Any]
