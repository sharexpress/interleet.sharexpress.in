"""
interview.py  ─  Interview API router
──────────────────────────────────────
IMPORTANT: Static routes (no path params) MUST be declared before wildcard
routes like /{session_id}, otherwise FastAPI matches the wildcard first.

Route order:
  POST  /start
  POST  /answer
  POST  /end
  GET   /reports/recent    ← must be before /{session_id}
  GET   /presets           ← must be before /{session_id}
  GET   /tts               ← must be before /{session_id}
  GET   /{session_id}
  GET   /{session_id}/report
  WS    /ws/{session_id}
"""
import io
import json

import anyio
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from openai import OpenAI

from app.ai.graph.interview_graph import build_initial_state, run_interview_graph
from app.ai.services.report_repository import InterviewReportRepository
from app.ai.services.report_service import InterviewReportService
from app.ai.services.session_service import SessionService
from app.core.config import OPENAI_API_KEY
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/interview", tags=["Interview"])


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _interviewer_message(state: dict) -> str:
    preamble = (state.get("current_preamble") or "").strip()
    question = (state.get("current_question") or "").strip()
    return f"{preamble}\n\n{question}" if preamble else question


# ─── POST /start ─────────────────────────────────────────────────────────────

@router.post("/start")
async def start_interview(payload: dict, user_auth=Depends(UserMiddleware.me)):
    user_doc = user_auth.get("user")
    if not user_doc.get("is_premium", False):
        raise HTTPException(
            status_code=403,
            detail="AI Mock Interviews require an active Premium subscription.",
        )
    state = build_initial_state(payload)
    state = await run_interview_graph(state)
    await SessionService.create_session(state["session_id"], state)
    return {
        "session_id":     state["session_id"],
        "message":        _interviewer_message(state),
        "question":       state.get("current_question", ""),
        "preamble":       state.get("current_preamble", ""),
        "affect":         state.get("current_affect", ""),
        "answer_guidance": state.get("current_answer_guidance", ""),
        "topic":          state.get("current_topic", ""),
        "difficulty":     state.get("difficulty", "medium"),
        "interview_phase": state.get("interview_phase", "intro"),
        "completed":      state.get("completed", False),
        "covered_topics": state.get("covered_topics", []),
        "remaining_topics": state.get("remaining_topics", []),
    }


# ─── POST /answer ─────────────────────────────────────────────────────────────

@router.post("/answer")
async def answer_question(payload: dict):
    session_id = payload.get("session_id")
    answer     = payload.get("answer", "").strip()
    if not session_id or not answer:
        raise HTTPException(status_code=400, detail="session_id and answer are required")

    state = await SessionService.get_session(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Interview session not found")

    state["last_answer"]       = answer
    state["last_answer_topic"] = payload.get("topic", state.get("current_topic", ""))

    state = await run_interview_graph(state)

    report = None
    if state.get("completed"):
        report = InterviewReportService.build_report(state)
        report["status"] = "completed"
        await InterviewReportRepository.save_report(
            session_id=session_id,
            report=report,
            state=state,
        )
        await SessionService.delete_session(session_id)
    else:
        await SessionService.update_session(session_id, state)

    response = {
        "session_id":       session_id,
        "completed":        state.get("completed", False),
        "completion_reason": state.get("completion_reason", ""),
        "closing_message":  state.get("closing_message", ""),
        "message":          state.get("closing_message", "") if state.get("completed") else _interviewer_message(state),
        "question":         "" if state.get("completed") else state.get("current_question", ""),
        "preamble":         "" if state.get("completed") else state.get("current_preamble", ""),
        "affect":           "" if state.get("completed") else state.get("current_affect", ""),
        "answer_guidance":  "" if state.get("completed") else state.get("current_answer_guidance", ""),
        "topic":            "" if state.get("completed") else state.get("current_topic", ""),
        "difficulty":       state.get("difficulty", "medium"),
        "interview_phase":  state.get("interview_phase", "adaptive_questions"),
        "evaluation":       state.get("last_evaluation"),
        "covered_topics":   state.get("covered_topics", []),
        "remaining_topics": state.get("remaining_topics", []),
    }
    if report is not None:
        response["report"] = report
    return response


# ─── POST /end ────────────────────────────────────────────────────────────────

@router.post("/end")
async def end_interview_early(payload: dict):
    """End an interview early (user hangs up mid-session).
    Builds a real partial report from whatever turns have been evaluated.
    """
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")

    state = await SessionService.get_session(session_id)
    if state is None:
        # Already ended — return saved report if available
        saved = await InterviewReportRepository.get_report(session_id)
        if saved:
            return {"session_id": session_id, "report": saved.get("report", {})}
        raise HTTPException(status_code=404, detail="Interview session not found")

    report = InterviewReportService.build_report(state)
    report["status"] = "ended_early"
    await InterviewReportRepository.save_report(
        session_id=session_id,
        report=report,
        state=state,
    )
    await SessionService.delete_session(session_id)
    return {"session_id": session_id, "report": report}


# ─── GET /reports/recent  (MUST be before /{session_id}) ─────────────────────

@router.get("/reports/recent")
async def list_interview_reports(user_auth=Depends(UserMiddleware.me), limit: int = 20):
    from datetime import datetime

    user_id = user_auth["user"]["user_id"]
    reports = await InterviewReportRepository.list_reports(user_id=user_id, limit=limit)

    formatted = []
    for r in reports:
        created_at = r.get("created_at")
        when_str   = "Recent"
        if isinstance(created_at, datetime):
            diff = datetime.utcnow() - created_at
            when_str = (
                "Today"        if diff.days == 0
                else "1d ago"  if diff.days == 1
                else f"{diff.days}d ago"
            )
        rep_data = r.get("report", {})
        score    = rep_data.get("overall_score") or rep_data.get("average_score") or 0
        formatted.append({
            "id":       r.get("session_id"),
            "role":     r.get("role") or "Software Engineer",
            "score":    score,
            "when":     when_str,
            "duration": 45,
            "status":   rep_data.get("status", "completed"),
        })
    return formatted


# ─── GET /presets  (MUST be before /{session_id}) ────────────────────────────

@router.get("/presets")
async def get_interview_presets():
    from app.controllers.admin import AdminController
    return await AdminController.list_presets()


# ─── GET /tts  (MUST be before /{session_id}) ────────────────────────────────

@router.get("/tts")
async def text_to_speech(text: str, voice: str = "nova"):
    """Generate professional, human-like voice speech for Sara's questions."""
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key is not configured. Add OPENAI_API_KEY to .env",
        )
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="text parameter is required")

    try:
        def _call_openai():
            client   = OpenAI(api_key=OPENAI_API_KEY)
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text.strip(),
            )
            return response.content

        audio_data = await anyio.to_thread.run_sync(_call_openai)
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Cache-Control": "public, max-age=86400",  # Cache TTS for 24h
                "Content-Disposition": "inline",
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ─── GET /{session_id}  (wildcard — MUST be after all static GET routes) ─────

@router.get("/{session_id}")
async def get_interview_session(session_id: str):
    state = await SessionService.get_session(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Interview session not found")
    return state


# ─── GET /{session_id}/report ─────────────────────────────────────────────────

@router.get("/{session_id}/report")
async def get_interview_report(session_id: str):
    # Try live session first (most up-to-date)
    state = await SessionService.get_session(session_id)
    if state is not None:
        report = InterviewReportService.build_report(state)
        report["status"] = "completed"
        await InterviewReportRepository.save_report(
            session_id=session_id,
            report=report,
            state=state,
        )
        await SessionService.delete_session(session_id)
        return report

    # Fall back to saved report (session already ended)
    saved_report = await InterviewReportRepository.get_report(session_id)
    if saved_report is None:
        raise HTTPException(status_code=404, detail="Interview report not found")
    return saved_report.get("report", saved_report)


# ─── WS /ws/{session_id} ─────────────────────────────────────────────────────

@router.websocket("/ws/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    state = await SessionService.get_session(session_id)
    if state is None:
        await websocket.send_json({"type": "error", "message": "Interview session not found"})
        await websocket.close(code=1008)
        return

    await websocket.send_json({
        "type":           "question",
        "question":       state.get("current_question", ""),
        "message":        _interviewer_message(state),
        "preamble":       state.get("current_preamble", ""),
        "affect":         state.get("current_affect", ""),
        "answer_guidance": state.get("current_answer_guidance", ""),
        "topic":          state.get("current_topic", ""),
        "difficulty":     state.get("difficulty", "medium"),
    })

    try:
        while True:
            raw     = await websocket.receive_text()
            payload = json.loads(raw)
            if payload.get("type") != "answer":
                await websocket.send_json({"type": "error", "message": "Unsupported message type"})
                continue

            state["last_answer"]       = payload.get("answer", "")
            state["last_answer_topic"] = payload.get("topic", state.get("current_topic", ""))
            state = await run_interview_graph(state)
            await SessionService.update_session(session_id, state)

            if state.get("completed"):
                report = InterviewReportService.build_report(state)
                report["status"] = "completed"
                await InterviewReportRepository.save_report(
                    session_id=session_id, report=report, state=state,
                )
                await SessionService.delete_session(session_id)
                await websocket.send_json({
                    "type":             "completed",
                    "completion_reason": state.get("completion_reason", ""),
                    "message":          state.get("closing_message", ""),
                    "closing_message":  state.get("closing_message", ""),
                    "report":           report,
                })
                await websocket.close()
                return

            await websocket.send_json({
                "type":           "question",
                "question":       state.get("current_question", ""),
                "message":        _interviewer_message(state),
                "preamble":       state.get("current_preamble", ""),
                "affect":         state.get("current_affect", ""),
                "answer_guidance": state.get("current_answer_guidance", ""),
                "topic":          state.get("current_topic", ""),
                "difficulty":     state.get("difficulty", "medium"),
                "evaluation":     state.get("last_evaluation"),
            })
    except WebSocketDisconnect:
        await SessionService.update_session(session_id, state)
