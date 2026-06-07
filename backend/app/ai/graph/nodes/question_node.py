"""
question_node.py
────────────────
Generates the next interview question using full conversation history.
Each question is a natural continuation — not a scripted prompt.
"""
from __future__ import annotations

from app.ai.graph.state import InterviewState
from app.ai.prompts.evaluation_prompt import OPENING_PROMPT
from app.ai.prompts.question_prompt import QUESTION_PROMPT
from app.ai.prompts.system_prompt import INTERVIEW_SYSTEM_PROMPT
from app.ai.schemas.interview import GeneratedQuestion, OpeningQuestion
from app.ai.services.ai_client import ai_client


# Phrases that signal a canned / robotic response
_CANNED_PHRASES = [
    "great answer",
    "excellent",
    "that's a great",
    "that's interesting",
    "thank you for sharing",
    "i appreciate",
    "great background",
    "valuable experience",
    "absolutely",
    "of course",
    "certainly",
    "no problem",
]

# Opening-specific phrases to block
_CANNED_OPENING_PHRASES = [
    "thanks for joining",
    "i'm excited to",
    "can you start by telling me",
    "i'm looking forward",
    "it's great to have you",
]


async def question_node(state: InterviewState):
    # ── Opening question (first ever) ────────────────────────────────────────
    if state.get("interview_phase") == "intro" and not state.get("questions_asked"):
        opening = await _generate_opening(state)
        opening = await _repair_opening(opening, state)
        full_msg = _join(opening.preamble, opening.question)
        return {
            "current_question": opening.question,
            "current_preamble": opening.preamble,
            "current_affect": opening.affect,
            "current_answer_guidance": opening.answer_guidance,
            "current_topic": "self_introduction",
            "current_intent": "Understand the candidate's background and calibrate the interview.",
            "current_expected_signal": "Clear articulation of relevant experience, projects, and motivation.",
            "questions_asked": [opening.question],
            "interviewer_messages": [full_msg],
            "current_question_index": 1,
        }

    # ── Subsequent questions ─────────────────────────────────────────────────
    user_prompt = _build_question_prompt(state)
    generated = await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{QUESTION_PROMPT}",
        user=user_prompt,
        schema=GeneratedQuestion,
        temperature=0.75,
    )
    generated = await _repair_question(generated, state)

    full_msg = _join(generated.preamble, generated.question)
    questions_asked = [*state.get("questions_asked", []), generated.question]
    interviewer_messages = [*state.get("interviewer_messages", []), full_msg]

    return {
        "current_question":         generated.question,
        "current_preamble":         generated.preamble,
        "current_affect":           generated.affect,
        "current_answer_guidance":  generated.answer_guidance,
        "current_topic":            generated.topic,
        "current_intent":           generated.intent,
        "current_expected_signal":  generated.expected_signal,
        "difficulty":               generated.difficulty.value,
        "questions_asked":          questions_asked,
        "interviewer_messages":     interviewer_messages,
        "current_question_index":   len(questions_asked),
    }


# ── Internal helpers ──────────────────────────────────────────────────────────

def _build_question_prompt(state: InterviewState) -> str:
    turns = state.get("turns", [])
    behavior_summary = _behavior_summary(turns)

    history_lines: list[str] = []
    for idx, t in enumerate(turns):
        history_lines.append(f"Turn {idx + 1}:")
        history_lines.append(f"  Sara: {t.get('question', '')}")
        history_lines.append(f"  Candidate: {t.get('answer', '')}")
        ev = t.get("evaluation") or {}
        if ev:
            score = ev.get("score", "?")
            summary = ev.get("summary", "")
            prof = ev.get("professionalism_score", 10)
            flags = ev.get("behavior_flags") or []
            history_lines.append(
                f"  [Eval: {score}/10 · {summary}"
                + (f" · Professionalism: {prof}/10" if prof < 10 else "")
                + (f" · Flags: {flags}" if flags else "")
                + "]"
            )
        history_lines.append("")

    # interviewer_messages is a list[str] — extract the first line (preamble) of each
    recent_preambles = []
    for msg in (state.get("interviewer_messages") or [])[-4:]:
        if isinstance(msg, str):
            first_line = msg.split("\n")[0].strip()
            if first_line:
                recent_preambles.append(first_line)
        elif isinstance(msg, dict):
            recent_preambles.append(msg.get("preamble", ""))

    return f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
Difficulty: {state.get("difficulty", "medium")}
JD (first 500 chars): {(state.get("jd") or "")[:500]}
Candidate summary: {state.get("candidate_summary", "")}
Candidate intro: {state.get("candidate_introduction", "")}
Skills: {state.get("skills", [])}
Projects: {state.get("projects", [])}
Technologies: {state.get("technologies", [])}
Experience: {state.get("experience", [])}

Topics to cover: {state.get("target_topics", [])}
Already covered: {state.get("covered_topics", [])}
Remaining: {state.get("remaining_topics", [])}
Weak topics (revisit if budget allows): {state.get("weak_topics", [])}

Question budget remaining: {max(0, int(state.get("max_questions", 8)) - len(state.get("questions_asked", [])))}

Last 3 preamble styles used (do NOT repeat the same style): {recent_preambles}

Candidate professionalism note: {behavior_summary}

=== Full Conversation History ===
{chr(10).join(history_lines)}

Last evaluation detail: {state.get("last_evaluation")}
"""


async def _generate_opening(state: InterviewState) -> OpeningQuestion:
    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
JD (first 500 chars): {(state.get("jd") or "")[:500]}
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


async def _repair_opening(opening: OpeningQuestion, state: InterviewState) -> OpeningQuestion:
    text = _join(opening.preamble, opening.question).lower()
    canned = [p for p in (_CANNED_PHRASES + _CANNED_OPENING_PHRASES) if p in text]
    if not canned:
        return opening

    return await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{OPENING_PROMPT}",
        user=f"""
Rewrite this opening. It sounds scripted.
Specifically, remove or rephrase these canned phrases: {canned}

Original:
{_join(opening.preamble, opening.question)}

Role: {state.get("role", "")}
Keep the same purpose: ask for self-introduction.
""",
        schema=OpeningQuestion,
        temperature=0.75,
    )


async def _repair_question(generated: GeneratedQuestion, state: InterviewState) -> GeneratedQuestion:
    text = _join(generated.preamble, generated.question)
    canned = [p for p in _CANNED_PHRASES if p in text.lower()]
    too_long = len(generated.question.split()) > 32

    if not canned and not too_long:
        return generated

    return await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{QUESTION_PROMPT}",
        user=f"""
Rewrite this interviewer turn. Issues found:
{f"- Canned phrases present: {canned}" if canned else ""}
{f"- Question too long ({len(generated.question.split())} words, limit 32)" if too_long else ""}

Original:
{text}

Recent turns (avoid repeating preamble style):
{state.get("interviewer_messages", [])[-3:]}

Keep the same topic: {generated.topic}
Keep the same intent: {generated.intent}
Keep difficulty: {generated.difficulty.value}
""",
        schema=GeneratedQuestion,
        temperature=0.75,
    )


def _behavior_summary(turns: list[dict]) -> str:
    flags: list[str] = []
    low_prof_count = 0
    for t in turns:
        ev = t.get("evaluation") or {}
        flags.extend(ev.get("behavior_flags") or [])
        if ev.get("professionalism_score", 10) < 7:
            low_prof_count += 1

    if not flags and low_prof_count == 0:
        return "Professional throughout."

    summary = f"Professionalism concerns in {low_prof_count} turn(s)."
    if flags:
        unique_flags = list(dict.fromkeys(flags))[:5]
        summary += f" Observed: {unique_flags}. Use professional-only tone — no warmth."
    return summary


def _join(preamble: str, question: str) -> str:
    p = (preamble or "").strip()
    q = (question or "").strip()
    return f"{p}\n\n{q}" if p else q
