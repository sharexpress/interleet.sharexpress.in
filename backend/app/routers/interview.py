import json

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from app.ai.graph.interview_graph import build_initial_state, run_interview_graph
from app.ai.services.report_repository import InterviewReportRepository
from app.ai.services.report_service import InterviewReportService
from app.ai.services.session_service import SessionService

router = APIRouter(prefix="/interview", tags=["Interview"])


def _interviewer_message(state: dict) -> str:
    preamble = state.get("current_preamble", "").strip()
    question = state.get("current_question", "").strip()
    if preamble and question:
        return f"{preamble}\n\n{question}"
    return question


@router.post("/start")
async def start_interview(payload: dict):
    state = build_initial_state(payload)
    state = await run_interview_graph(state)
    await SessionService.create_session(state["session_id"], state)
    return {
        "session_id": state["session_id"],
        "message": _interviewer_message(state),
        "question": state.get("current_question", ""),
        "preamble": state.get("current_preamble", ""),
        "topic": state.get("current_topic", ""),
        "difficulty": state.get("difficulty", "medium"),
        "interview_phase": state.get("interview_phase", "intro"),
        "completed": state.get("completed", False),
    }


@router.post("/answer")
async def answer_question(payload: dict):
    session_id = payload.get("session_id")
    answer = payload.get("answer", "")
    if not session_id or not answer:
        raise HTTPException(status_code=400, detail="session_id and answer are required")

    state = await SessionService.get_session(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Interview session not found")

    state["last_answer"] = answer
    state["last_answer_topic"] = payload.get("topic", state.get("current_topic", ""))
    state = await run_interview_graph(state)
    report = None
    if state.get("completed"):
        report = InterviewReportService.build_report(state)
        await InterviewReportRepository.save_report(
            session_id=session_id,
            report=report,
            state=state,
        )
        await SessionService.delete_session(session_id)
    else:
        await SessionService.update_session(session_id, state)

    response = {
        "session_id": session_id,
        "completed": state.get("completed", False),
        "completion_reason": state.get("completion_reason", ""),
        "message": "" if state.get("completed") else _interviewer_message(state),
        "question": "" if state.get("completed") else state.get("current_question", ""),
        "preamble": "" if state.get("completed") else state.get("current_preamble", ""),
        "topic": "" if state.get("completed") else state.get("current_topic", ""),
        "difficulty": state.get("difficulty", "medium"),
        "interview_phase": state.get("interview_phase", "adaptive_questions"),
        "evaluation": state.get("last_evaluation"),
        "covered_topics": state.get("covered_topics", []),
        "remaining_topics": state.get("remaining_topics", []),
    }
    if report is not None:
        response["report"] = report
    return response


@router.get("/{session_id}")
async def get_interview_session(session_id: str):
    state = await SessionService.get_session(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Interview session not found")
    return state


@router.get("/{session_id}/report")
async def get_interview_report(session_id: str):
    state = await SessionService.get_session(session_id)
    if state is None:
        saved_report = await InterviewReportRepository.get_report(session_id)
        if saved_report is None:
            raise HTTPException(status_code=404, detail="Interview report not found")
        return saved_report
    report = InterviewReportService.build_report(state)
    await InterviewReportRepository.save_report(
        session_id=session_id,
        report=report,
        state=state,
    )
    await SessionService.delete_session(session_id)
    return report


@router.get("/reports/recent")
async def list_interview_reports(user_id: str | None = None, limit: int = 20):
    return await InterviewReportRepository.list_reports(user_id=user_id, limit=limit)


@router.websocket("/ws/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    state = await SessionService.get_session(session_id)
    if state is None:
        await websocket.send_json({"type": "error", "message": "Interview session not found"})
        await websocket.close(code=1008)
        return

    await websocket.send_json(
        {
            "type": "question",
            "question": state.get("current_question", ""),
            "message": _interviewer_message(state),
            "preamble": state.get("current_preamble", ""),
            "topic": state.get("current_topic", ""),
            "difficulty": state.get("difficulty", "medium"),
        }
    )

    try:
        while True:
            message = await websocket.receive_text()
            payload = json.loads(message)
            if payload.get("type") != "answer":
                await websocket.send_json({"type": "error", "message": "Unsupported message type"})
                continue

            state["last_answer"] = payload.get("answer", "")
            state["last_answer_topic"] = payload.get("topic", state.get("current_topic", ""))
            state = await run_interview_graph(state)
            await SessionService.update_session(session_id, state)

            if state.get("completed"):
                report = InterviewReportService.build_report(state)
                await InterviewReportRepository.save_report(
                    session_id=session_id,
                    report=report,
                    state=state,
                )
                await SessionService.delete_session(session_id)
                await websocket.send_json(
                    {
                        "type": "completed",
                        "completion_reason": state.get("completion_reason", ""),
                        "report": report,
                    }
                )
                await websocket.close()
                return

            await websocket.send_json(
                {
                    "type": "question",
                    "question": state.get("current_question", ""),
                    "message": _interviewer_message(state),
                    "preamble": state.get("current_preamble", ""),
                    "topic": state.get("current_topic", ""),
                    "difficulty": state.get("difficulty", "medium"),
                    "evaluation": state.get("last_evaluation"),
                }
            )
    except WebSocketDisconnect:
        await SessionService.update_session(session_id, state)
