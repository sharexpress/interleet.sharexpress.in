from app.ai.graph.state import InterviewState
from app.ai.prompts.question_prompt import OPENING_PROMPT, QUESTION_PROMPT
from app.ai.prompts.system_prompt import INTERVIEW_SYSTEM_PROMPT
from app.ai.schemas.interview import GeneratedQuestion, OpeningQuestion
from app.ai.services.ai_client import ai_client


async def question_node(state: InterviewState):
    if state.get("interview_phase") == "intro" and not state.get("questions_asked"):
        opening = await _generate_opening_question(state)
        return {
            "current_question": opening.question,
            "current_preamble": opening.preamble,
            "current_topic": "self_introduction",
            "current_intent": "Understand the candidate's background and calibrate the interview.",
            "questions_asked": [opening.question],
            "current_question_index": 1,
        }

    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
Difficulty: {state.get("difficulty", "medium")}
JD: {state.get("jd", "")}
Candidate summary: {state.get("candidate_summary", "")}
Candidate self-introduction: {state.get("candidate_introduction", "")}
Skills: {state.get("skills", [])}
Projects: {state.get("projects", [])}
Technologies: {state.get("technologies", [])}
Experience: {state.get("experience", [])}
Target topics: {state.get("target_topics", [])}
Covered topics: {state.get("covered_topics", [])}
Remaining topics: {state.get("remaining_topics", [])}
Weak topics: {state.get("weak_topics", [])}
Assessment dimensions: {(state.get("metadata") or {}).get("assessment_dimensions", [])}
Question budget remaining: {max(0, int(state.get("max_questions", 8)) - len(state.get("questions_asked", [])))}
Previous questions: {state.get("questions_asked", [])}
Last candidate answer: {state.get("turns", [])[-1] if state.get("turns") else None}
Last evaluation: {state.get("last_evaluation")}
"""
    generated = await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{QUESTION_PROMPT}",
        user=user_prompt,
        schema=GeneratedQuestion,
        temperature=0.35,
    )

    questions_asked = [*state.get("questions_asked", []), generated.question]

    return {
        "current_question": generated.question,
        "current_preamble": generated.preamble,
        "current_topic": generated.topic,
        "current_intent": generated.intent,
        "difficulty": generated.difficulty.value,
        "questions_asked": questions_asked,
        "current_question_index": len(questions_asked),
    }


async def _generate_opening_question(state: InterviewState) -> OpeningQuestion:
    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
JD: {state.get("jd", "")}
Candidate summary: {state.get("candidate_summary", "")}
Skills: {state.get("skills", [])}
Projects: {state.get("projects", [])}
Experience: {state.get("experience", [])}
Additional context: {state.get("additional_context", "")}
"""
    return await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{OPENING_PROMPT}",
        user=user_prompt,
        schema=OpeningQuestion,
        temperature=0.65,
    )
