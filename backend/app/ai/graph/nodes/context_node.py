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

"""
context_node.py
────────────────
The single node responsible for appending the completed turn to state.turns.

Turn record includes the evaluation from evaluation_node (via last_evaluation).
For the intro path (self_introduction), evaluation is skipped, so we record
an empty evaluation dict.
"""
from pydantic import BaseModel, Field
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
    target_topics = list(state.get("target_topics", []))
    covered_topics = list(state.get("covered_topics", []))

    if is_intro:
        # Dynamically build interview topics (nodes) from the candidate's introduction text
        target_topics = await _generate_topics_from_intro(state, state.get("last_answer", ""))

    if not is_intro:
        for matched in _detect_covered_topics(state, topic):
            if matched not in covered_topics:
                covered_topics.append(matched)

    remaining_topics = [
        t for t in target_topics
        if t not in covered_topics
    ]

    interview_phase = (
        "adaptive_questions"
        if is_intro
        else state.get("interview_phase", "adaptive_questions")
    )

    return {
        "turns":                  turns,
        "target_topics":          target_topics,
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


class extracted_topics(BaseModel):
    topics: list[str] = Field(default_factory=list)


async def _generate_topics_from_intro(state: InterviewState, intro_text: str) -> list[str]:
    from pydantic import BaseModel, Field
    from app.ai.prompts.system_prompt import INTRO_TOPICS_PROMPT
    from app.ai.services.ai_client import ai_client
    
    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
JD Context: {(state.get("jd") or "")[:1000]}
Skills context: {state.get("skills", [])}
Candidate Self-Introduction:
{intro_text}
"""
    try:
        res = await ai_client.generate_json(
            system=INTRO_TOPICS_PROMPT,
            user=user_prompt,
            schema=extracted_topics,
            temperature=0.3,
        )
        if res.topics:
            # Clean and return exactly 5 topics
            return [t.strip() for t in res.topics if t.strip()][:5]
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning(f"[context_node] Dynamic topic generation failed: {exc}")
        
    return state.get("target_topics", [])
