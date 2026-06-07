"""
Interleet Judge Engine — API v1 Router
Full FastAPI routes for the self-hosted execution engine.

Routes:
  POST   /api/v1/execute                → synchronous code execution
  POST   /api/v1/submissions            → async submission (returns immediately)
  GET    /api/v1/submissions/{id}       → poll submission status
  GET    /api/v1/results/{id}           → get full execution result
  GET    /api/v1/languages              → list supported languages
  GET    /api/v1/health                 → engine health check
  WS     /api/v1/ws/{submission_id}     → live execution stream (in ws_router)
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from app.engine.controllers.submission_controller import EngineSubmissionController
from app.engine.docker.pool import get_available_languages, verify_sandbox_images
from app.engine.executors.factory import LANGUAGE_META, ExecutorFactory
from app.engine.queue.redis_queue import get_execution_queue
from app.engine.schemas import ExecuteRequest, RunRequest, SubmissionRequest, InlineTestCase, TestCaseSchema
from app.engine.security.code_guard import CodeGuard

logger = logging.getLogger(__name__)

engine_router = APIRouter(prefix="/api/v1", tags=["Judge Engine v1"])


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/execute
# One-shot synchronous execution. Waits up to 30s for a result.
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.post("/execute", summary="Execute code (synchronous)")
async def execute_code(
    request: ExecuteRequest = Body(
        ...,
        examples={
            "python_hello": {
                "summary": "Python hello world",
                "value": {
                    "language": "python",
                    "code": "print(input())",
                    "stdin": "hello",
                    "expected_output": "hello",
                    "time_limit": 2,
                    "memory_limit": 256,
                },
            }
        },
    ),
) -> dict[str, Any]:
    """
    **Synchronous code execution.**

    Submit code and wait for the execution result (up to 30 seconds).
    Use for quick runs and playground-style execution.
    """
    # Security guard
    guard = CodeGuard.check(request.code, request.language.value)
    if not guard.allowed:
        raise HTTPException(status_code=400, detail=f"Code blocked by security policy: {guard.reason}")

    try:
        result = await EngineSubmissionController.create_execute(request)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Execute endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal execution error") from exc


# ─────────────────────────────────────────────────────────────────────────────────
# POST /api/v1/run
# Run against inline sample test cases. Fast path for the "Run" button.
# ─────────────────────────────────────────────────────────────────────────────────

@engine_router.post("/run", summary="Run against sample test cases (inline)")
async def run_code(
    request: RunRequest = Body(
        ...,
        examples={
            "two_sum_js": {
                "summary": "Run Two-Sum in JavaScript",
                "value": {
                    "language": "javascript",
                    "code": "const lines = require('fs').readFileSync('/dev/stdin','utf8').trim().split('\\n'); console.log(lines[0]);",
                    "test_cases": [
                        {"stdin": "[2,7,11,15]\\n9", "expected_output": "[0,1]", "name": "Example 1"},
                        {"stdin": "[3,2,4]\\n6",      "expected_output": "[1,2]", "name": "Example 2"},
                    ],
                },
            }
        },
    ),
) -> dict[str, Any]:
    """
    **Run code against visible sample test cases.**

    Test cases are passed inline (not fetched from DB).
    Returns per-testcase results immediately (synchronous, waits up to 30s).
    """
    # Security guard
    guard = CodeGuard.check(request.code, request.language.value)
    if not guard.allowed:
        raise HTTPException(status_code=400, detail=f"Code blocked: {guard.reason}")

    try:
        result = await EngineSubmissionController.create_run(request)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Run endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal execution error") from exc


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/submissions
# Async submission — returns submission_id immediately.
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.post("/submissions", summary="Submit code (async)")
async def create_submission(
    request: SubmissionRequest = Body(
        ...,
        examples={
            "python_submit": {
                "summary": "Python problem submission",
                "value": {
                    "language": "python",
                    "code": "n = int(input())\nprint(n * 2)",
                    "problem_slug": "two-sum",
                    "user_id": "user_abc123",
                    "time_limit": 2,
                    "memory_limit": 256,
                    "mode": "submit",
                },
            }
        },
    ),
) -> dict[str, Any]:
    """
    **Async code submission against a problem's testcases.**

    Returns immediately with a `submission_id`. Monitor progress via:
    - **WebSocket**: `WS /api/v1/ws/{submission_id}`
    - **Polling**: `GET /api/v1/results/{submission_id}`
    """
    # Security guard
    guard = CodeGuard.check(request.code, request.language.value)
    if not guard.allowed:
        raise HTTPException(status_code=400, detail=f"Code blocked: {guard.reason}")

    try:
        result = await EngineSubmissionController.create_submission(request)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Submission endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal submission error") from exc


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/submissions/{submission_id}
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.get("/submissions/{submission_id}", summary="Get submission status")
async def get_submission(submission_id: str) -> dict[str, Any]:
    """
    **Get submission status and result.**

    Returns the current status (QUEUED, RUNNING, COMPLETED, etc.)
    and the full result once execution is finished.
    """
    result = await EngineSubmissionController.get_submission(submission_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Submission '{submission_id}' not found")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/results/{submission_id}
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.get("/results/{submission_id}", summary="Get execution result")
async def get_result(submission_id: str) -> dict[str, Any]:
    """
    **Get the full execution result for a submission.**

    Includes per-testcase results, verdict, timing, memory usage.
    Hidden testcase outputs are redacted (stdout/expected_output = "").
    """
    result = await EngineSubmissionController.get_result(submission_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Result for submission '{submission_id}' not found. "
                   "The job may still be running — try again shortly.",
        )
    return result


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/languages
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.get("/languages", summary="List supported languages")
async def list_languages(
    available_only: bool = Query(False, description="Only return languages with Docker images ready"),
) -> dict[str, Any]:
    """
    **List all supported programming languages.**

    Set `available_only=true` to filter languages whose Docker images are built and ready.
    """
    if available_only:
        available = await get_available_languages()
        languages = [
            {
                "id": lang,
                "available": True,
                **LANGUAGE_META.get(__import__("app.engine.enums", fromlist=["Language"]).Language(lang), {}),
            }
            for lang in available
        ]
    else:
        from app.engine.enums import Language
        languages = [
            {
                "id": lang.value,
                "available": True,
                **LANGUAGE_META.get(lang, {}),
            }
            for lang in Language
        ]

    return {"languages": languages, "count": len(languages)}


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/health
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.get("/health", summary="Engine health check")
async def engine_health() -> dict[str, Any]:
    """
    **Judge engine health check.**

    Returns status of Redis queue, Docker images, and MongoDB.
    """
    queue = get_execution_queue()

    # Redis
    redis_ok = await queue.ping()
    queue_length = await queue.queue_length() if redis_ok else -1

    # Docker images
    image_statuses = await verify_sandbox_images()
    images_ready = sum(1 for s in image_statuses if s.available)

    # DB
    from app.engine.services.submission_service import SubmissionService
    db_health = await SubmissionService.health()

    return {
        "status": "ok" if redis_ok else "degraded",
        "engine": "interleet-judge-v1",
        "redis": {
            "connected": redis_ok,
            "queue_length": queue_length,
        },
        "docker": {
            "images_ready": images_ready,
            "images_total": len(image_statuses),
            "images": [
                {"language": s.language, "image": s.image, "available": s.available}
                for s in image_statuses
            ],
        },
        "database": db_health,
        "workers": {
            "count": int(__import__("os").environ.get("WORKER_COUNT", 4)),
        },
    }
