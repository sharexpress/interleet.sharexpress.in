from app.ai.graph.state import InterviewState
from app.ai.prompts.question_prompt import OPENING_PROMPT, QUESTION_PROMPT
from app.ai.prompts.system_prompt import INTERVIEW_SYSTEM_PROMPT
from app.ai.schemas.interview import GeneratedQuestion, OpeningQuestion
from app.ai.services.ai_client import ai_client


_CANNED_PHRASES = [
    "can you walk me through",
    "dive deeper",
    "great background",
    "valuable experience",
    "that's interesting",
    "thank you for sharing",
    "i appreciate",
    "great answer",
]


async def question_node(state: InterviewState):
    if state.get("interview_phase") == "intro" and not state.get("questions_asked"):
        opening = await _generate_opening_question(state)
        opening = await _repair_opening_if_canned(opening, state)
        message = _message(opening.preamble, opening.question)
        return {
            "current_question": opening.question,
            "current_preamble": opening.preamble,
            "current_affect": opening.affect,
            "current_answer_guidance": opening.answer_guidance,
            "current_topic": "self_introduction",
            "current_intent": "Understand the candidate's background and calibrate the interview.",
            "questions_asked": [opening.question],
            "interviewer_messages": [message],
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
Recent interviewer messages: {state.get("interviewer_messages", [])[-3:]}
Last candidate answer: {state.get("turns", [])[-1] if state.get("turns") else None}
Last evaluation: {state.get("last_evaluation")}
"""
    generated = await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{QUESTION_PROMPT}",
        user=user_prompt,
        schema=GeneratedQuestion,
        temperature=0.35,
    )
    generated = await _repair_question_if_needed(generated, state)

    questions_asked = [*state.get("questions_asked", []), generated.question]
    interviewer_messages = [
        *state.get("interviewer_messages", []),
        _message(generated.preamble, generated.question),
    ]

    return {
        "current_question": generated.question,
        "current_preamble": generated.preamble,
        "current_affect": generated.affect,
        "current_answer_guidance": generated.answer_guidance,
        "current_topic": generated.topic,
        "current_intent": generated.intent,
        "difficulty": generated.difficulty.value,
        "questions_asked": questions_asked,
        "interviewer_messages": interviewer_messages,
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


async def _repair_opening_if_canned(
    opening: OpeningQuestion,
    state: InterviewState,
) -> OpeningQuestion:
    text = _message(opening.preamble, opening.question)
    if not _has_canned_phrase(text):
        return opening

    return await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{OPENING_PROMPT}",
        user=f"""
Rewrite this opening so it sounds less scripted and avoids these phrases:
{_CANNED_PHRASES}

Original opening:
{text}

Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
JD: {state.get("jd", "")}

Keep the same purpose: ask for a self-introduction.
""",
        schema=OpeningQuestion,
        temperature=0.75,
    )


async def _repair_question_if_needed(
    generated: GeneratedQuestion,
    state: InterviewState,
) -> GeneratedQuestion:
    text = _message(generated.preamble, generated.question)
    if not _needs_repair(text, generated.question):
        return generated

    return await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{QUESTION_PROMPT}",
        user=f"""
Rewrite this interviewer turn so it sounds more natural, less robotic, and concise.
Avoid praise unless essential. Avoid these phrases:
{_CANNED_PHRASES}

Keep the question under 32 words.
Use at most one preamble sentence.

Original turn:
{text}

Recent interviewer messages:
{state.get("interviewer_messages", [])[-3:]}

Last candidate answer:
{state.get("turns", [])[-1] if state.get("turns") else None}

Keep the same topic and intent:
Topic: {generated.topic}
Intent: {generated.intent}
Difficulty: {generated.difficulty.value}
""",
        schema=GeneratedQuestion,
        temperature=0.7,
    )


def _has_canned_phrase(text: str) -> bool:
    normalized = text.lower()
    return any(phrase in normalized for phrase in _CANNED_PHRASES)


def _needs_repair(message: str, question: str) -> bool:
    return _has_canned_phrase(message) or len(question.split()) > 32


def _message(preamble: str, question: str) -> str:
    preamble = preamble.strip()
    question = question.strip()
    if preamble and question:
        return f"{preamble}\n\n{question}"
    return question
