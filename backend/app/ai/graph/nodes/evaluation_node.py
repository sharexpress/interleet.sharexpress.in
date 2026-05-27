from app.ai.graph.state import InterviewState
from app.ai.prompts.evaluation_prompt import EVALUATION_PROMPT
from app.ai.prompts.system_prompt import INTERVIEW_SYSTEM_PROMPT
from app.ai.schemas.interview import AnswerEvaluation
from app.ai.services.ai_client import ai_client


async def evaluation_node(state: InterviewState):
    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
Difficulty: {state.get("difficulty", "medium")}
Question: {state.get("current_question", "")}
Topic: {state.get("current_topic", "")}
Question intent: {state.get("current_intent", "")}
Candidate answer: {state.get("last_answer", "")}
JD: {state.get("jd", "")}
Candidate summary: {state.get("candidate_summary", "")}
Previous evaluations: {state.get("evaluations", [])[-3:]}
"""
    evaluation = await ai_client.generate_json(
        system=f"{INTERVIEW_SYSTEM_PROMPT}\n\n{EVALUATION_PROMPT}",
        user=user_prompt,
        schema=AnswerEvaluation,
        temperature=0,
    )

    evaluations = [*state.get("evaluations", []), evaluation.model_dump()]
    weak_topics = list(state.get("weak_topics", []))
    current_topic = state.get("current_topic", "")
    if evaluation.score < 6 and current_topic and current_topic not in weak_topics:
        weak_topics.append(current_topic)

    return {
        "last_evaluation": evaluation.model_dump(),
        "evaluations": evaluations,
        "weak_topics": weak_topics,
    }
