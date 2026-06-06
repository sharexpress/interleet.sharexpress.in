"""
Legacy Execution Router — /api/execution/*
Backward-compatible routes wired to the new Docker-based engine.

New routes:  POST /api/v1/execute  |  POST /api/v1/submissions
Legacy routes are preserved to avoid breaking existing frontend code.
"""

from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from app.engine.controllers.submission_controller import EngineSubmissionController
from app.engine.schemas import ExecuteRequest, SubmissionRequest

router = APIRouter(prefix="/api/execution", tags=["Code Execution (Legacy)"])


@router.post("/run", summary="Run code (legacy route)")
async def run_code(payload: ExecuteRequest = Body(...)):
    """
    Legacy run endpoint — proxied to the new Docker-based engine.
    Prefer: POST /api/v1/execute
    """
    try:
        return await EngineSubmissionController.create_execute(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/submit", summary="Submit code (legacy route)")
async def submit_code(payload: SubmissionRequest = Body(...)):
    """
    Legacy submit endpoint — proxied to the new Docker-based engine.
    Prefer: POST /api/v1/submissions
    """
    try:
        return await EngineSubmissionController.create_submission(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/submissions/recent", summary="List recent submissions")
async def list_submissions(problem_slug: str | None = None, limit: int = 20):
    from app.engine.services.submission_service import SubmissionService
    return await SubmissionService.list_submissions(problem_slug=problem_slug, limit=limit)


@router.get("/submissions/{submission_id}", summary="Get submission")
async def get_submission(submission_id: str):
    result = await EngineSubmissionController.get_submission(submission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    return result


@router.get("/{submission_id}", summary="Get execution result (legacy)")
async def get_execution_result(submission_id: str):
    result = await EngineSubmissionController.get_result(submission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Execution result not found")
    return result
