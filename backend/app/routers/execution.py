"""
Legacy Execution Router — /api/execution/*
Backward-compatible routes wired to the new Docker-based engine.

New routes:  POST /api/v1/execute  |  POST /api/v1/submissions
Legacy routes are preserved to avoid breaking existing frontend code.
"""

from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException, Depends

from app.middleware.user import Middleware as UserMiddleware
from app.core.db import get_db
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
async def submit_code(
    payload: SubmissionRequest = Body(...),
    user_auth=Depends(UserMiddleware.me),
):
    """
    Legacy submit endpoint — proxied to the new Docker-based engine.
    Prefer: POST /api/v1/submissions
    """
    # Overwrite user_id with the authenticated user's ID to prevent spoofing
    user_doc = user_auth.get("user")
    payload.user_id = str(user_doc["user_id"])

    # Access Control Security: check if challenge is premium
    if payload.problem_slug:
        db = get_db()
        challenge = await db.problems.find_one({"slug": payload.problem_slug})
        is_premium = False
        if challenge:
            is_premium = challenge.get("is_premium", False) or challenge.get("slug") in {"responsive-data-table", "design-twitter-feed", "k8s-blue-green"}
        else:
            from app.data.seed import CHALLENGES
            c_seed = next((c for c in CHALLENGES if c.get("slug") == payload.problem_slug), None)
            if c_seed:
                is_premium = c_seed.get("is_premium", False) or c_seed.get("slug") in {"responsive-data-table", "design-twitter-feed", "k8s-blue-green"}

        # Verify if bypassed by contest
        bypassed = False
        if payload.contest_id:
            contest = await db.contests.find_one({
                "$or": [
                    {"room_code": payload.contest_id.upper()},
                    {"contest_id": payload.contest_id}
                ],
                "status": "active"
            })
            if contest:
                participant = next((p for p in contest.get("participants", []) if str(p.get("user_id")) == str(user_doc.get("user_id"))), None)
                if participant:
                    if participant.get("disqualified", False):
                        raise HTTPException(
                            status_code=403,
                            detail="You are disqualified from this contest."
                        )
                    is_participant = True
                else:
                    is_participant = False
                slug_in_contest = payload.problem_slug in contest.get("challenges", [])
                if is_participant and slug_in_contest:
                    bypassed = True

        if is_premium and not user_doc.get("is_premium", False) and not bypassed:
            raise HTTPException(
                status_code=403,
                detail="This challenge requires an active Premium subscription. Please upgrade to unlock."
            )

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
