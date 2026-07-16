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

from fastapi import APIRouter, Body, HTTPException, Query, Depends, WebSocket, WebSocketDisconnect

from app.middleware.user import Middleware as UserMiddleware
from app.core.db import get_db
from app.engine.controllers.submission_controller import EngineSubmissionController
from app.engine.docker.pool import get_available_languages, verify_sandbox_images
from app.engine.executors.factory import LANGUAGE_META, ExecutorFactory
from app.engine.queue.redis_queue import get_execution_queue
from app.engine.schemas import ExecuteRequest, RunRequest, SubmissionRequest, InlineTestCase, TestCaseSchema
from app.engine.security.code_guard import CodeGuard

logger = logging.getLogger(__name__)

engine_router = APIRouter(prefix="/api/v1", tags=["Judge Engine v1"])


@engine_router.get("/runtimes", summary="List execution runtimes")
async def list_runtimes() -> dict[str, Any]:
    """Return runtime metadata used to render execution workspaces."""
    from app.engine.runtimes.registry import RuntimeRegistry

    runtimes = RuntimeRegistry.get_all()
    return {"data": runtimes, "total": len(runtimes)}


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
    if request.execution_mode not in ("devops", "compose", "http"):
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
    if request.execution_mode not in ("devops", "compose", "http"):
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
    user_auth=Depends(UserMiddleware.me),
) -> dict[str, Any]:
    """
    **Async code submission against a problem's testcases.**

    Returns immediately with a `submission_id`. Monitor progress via:
    - **WebSocket**: `WS /api/v1/ws/{submission_id}`
    - **Polling**: `GET /api/v1/results/{submission_id}`
    """
    # Security guard
    if request.execution_mode not in ("devops", "compose", "http"):
        guard = CodeGuard.check(request.code, request.language.value)
        if not guard.allowed:
            raise HTTPException(status_code=400, detail=f"Code blocked: {guard.reason}")

    # Overwrite user_id with the authenticated user's ID to prevent spoofing
    user_doc = user_auth.get("user")
    request.user_id = str(user_doc["user_id"])

    # Access Control Security: check if challenge is premium
    if request.problem_slug:
        db = get_db()
        challenge = await db.problems.find_one({"slug": request.problem_slug})
        is_premium = False
        if challenge:
            is_premium = challenge.get("is_premium", False) or challenge.get("slug") in {"responsive-data-table", "design-twitter-feed", "k8s-blue-green"}
        else:
            from app.data.seed import CHALLENGES
            c_seed = next((c for c in CHALLENGES if c.get("slug") == request.problem_slug), None)
            if c_seed:
                is_premium = c_seed.get("is_premium", False) or c_seed.get("slug") in {"responsive-data-table", "design-twitter-feed", "k8s-blue-green"}

        # Verify if bypassed by contest
        bypassed = False
        if request.contest_id:
            contest = await db.contests.find_one({
                "$or": [
                    {"room_code": request.contest_id.upper()},
                    {"contest_id": request.contest_id}
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
                slug_in_contest = request.problem_slug in contest.get("challenges", [])
                if is_participant and slug_in_contest:
                    bypassed = True

        if is_premium and not user_doc.get("is_premium", False) and not bypassed:
            raise HTTPException(
                status_code=403,
                detail="This challenge requires an active Premium subscription. Please upgrade to unlock."
            )

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
# GET /api/v1/submissions/my/{problem_slug}
# Returns the current user's most recent submission for a problem slug.
# IMPORTANT: This route MUST be registered before /{submission_id} to avoid
# the static path "my" being captured as a submission_id wildcard.
# We achieve this by declaring it separately with a distinct prefix.
# ─────────────────────────────────────────────────────────────────────────────

@engine_router.get("/my-submissions/{problem_slug}", summary="Get my last submission for a problem")
async def get_my_submission(
    problem_slug: str,
    user_auth=Depends(UserMiddleware.me),
) -> dict[str, Any]:
    """
    **Get the current user's most recent submission for a specific problem.**

    Returns the submission code, language, verdict, score, and timestamp.
    Used by the editor to show an "Already Attempted" banner and pre-fill code.
    """
    user_doc = user_auth.get("user")
    user_id = str(user_doc["user_id"])
    db = get_db()

    # Find the most recent submission for this user+slug, any verdict
    submission = await db.submissions.find_one(
        {"user_id": user_id, "problem_slug": problem_slug},
        {"_id": 0},
        sort=[("created_at", -1)],
    )

    if not submission:
        return {"found": False}

    # Also check if there's an accepted submission
    accepted = await db.submissions.find_one(
        {"user_id": user_id, "problem_slug": problem_slug, "status": "accepted"},
        {"_id": 0},
        sort=[("created_at", -1)],
    )

    # Prefer the accepted submission's code over partial; use latest for metadata
    result_sub = accepted if accepted else submission

    return {
        "found": True,
        "is_accepted": accepted is not None,
        "submission_id": result_sub.get("submission_id") or result_sub.get("id"),
        "code": result_sub.get("source_code") or result_sub.get("code", ""),
        "language": result_sub.get("language", ""),
        "status": result_sub.get("status", ""),
        "score": result_sub.get("score", 0),
        "verdict": result_sub.get("verdict", ""),
        "created_at": str(result_sub.get("created_at", "")),
        "total_attempts": await db.submissions.count_documents(
            {"user_id": user_id, "problem_slug": problem_slug}
        ),
    }




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


# ─────────────────────────────────────────────────────────────────────────────
# DEVOPS LIVE INTERACTIVE TERMINAL ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

from pydantic import BaseModel
import uuid
import os
import shutil
from pathlib import Path
from app.engine.docker.sandbox import get_docker_client

WORKSPACE_BASE = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")

class DevOpsSessionStartRequest(BaseModel):
    slug: str

class DevOpsSessionSyncRequest(BaseModel):
    files: dict[str, str]

class DevOpsSessionExecRequest(BaseModel):
    command: str

@engine_router.post("/devops/session/start", summary="Start interactive DevOps session container")
async def api_start_devops_session(request: DevOpsSessionStartRequest):
    db = get_db()
    
    # 1. Fetch challenge details from DB to get starter code
    challenge = await db.problems.find_one({"slug": request.slug})
    if not challenge:
        from app.data.seed import CHALLENGES
        challenge = next((c for c in CHALLENGES if c.get("slug") == request.slug), None)
        
    if not challenge:
        raise HTTPException(status_code=404, detail="DevOps challenge not found")
        
    # Get starter files
    starter = challenge.get("starter_code", {})
    initial_files = {}
    if "multi" in starter:
        try:
            import json
            initial_files = json.loads(starter["multi"])
        except Exception:
            pass
            
    session_id = str(uuid.uuid4())
    client = get_docker_client()
    
    # Create the host workspace directory
    workspace_dir = Path(WORKSPACE_BASE) / f"devops_{session_id}"
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Write initial starter files to workspace
    for fname, content in initial_files.items():
        target_path = Path(workspace_dir / fname).resolve()
        if not str(target_path).startswith(str(workspace_dir.resolve())):
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        if fname.endswith(".sh"):
            target_path.chmod(0o755)
            
    # Start persistent container specific to this session
    container_name = f"interleet-devops-session-{session_id}"
    
    try:
        # Stop and remove any pre-existing container under same name
        old = client.containers.get(container_name)
        old.remove(force=True)
    except Exception:
        pass
        
    try:
        # Run container. Allow networking so the candidate can download packages, curl, etc.
        client.containers.run(
            image="interleet-devops:latest",
            command=["sleep", "infinity"],
            name=container_name,
            volumes={
                str(workspace_dir): {"bind": "/workspace", "mode": "rw"}
            },
            working_dir="/workspace",
            network_mode="bridge",
            detach=True,
            remove=True,
        )
    except Exception as exc:
        # Clean up workspace folder if start fails
        shutil.rmtree(workspace_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Failed to start sandbox container: {exc}")
        
    return {
        "session_id": session_id,
        "files": initial_files
    }

@engine_router.post("/devops/session/{session_id}/sync", summary="Sync files to DevOps container workspace")
async def api_sync_devops_session(session_id: str, request: DevOpsSessionSyncRequest):
    workspace_dir = Path(WORKSPACE_BASE) / f"devops_{session_id}"
    if not workspace_dir.exists():
        # Re-create if deleted somehow but container is still running
        os.makedirs(workspace_dir, exist_ok=True)
        
    for fname, content in request.files.items():
        target_path = Path(workspace_dir / fname).resolve()
        if not str(target_path).startswith(str(workspace_dir.resolve())):
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        if fname.endswith(".sh"):
            target_path.chmod(0o755)
            
    return {"success": True}

@engine_router.post("/devops/session/{session_id}/exec", summary="Run shell command in DevOps container")
async def api_exec_devops_session(session_id: str, request: DevOpsSessionExecRequest):
    client = get_docker_client()
    container_name = f"interleet-devops-session-{session_id}"
    
    try:
        container = client.containers.get(container_name)
    except Exception:
        raise HTTPException(status_code=404, detail="DevOps session not found or container has exited")
        
    # Execute the command inside the docker container
    try:
        exec_res = container.exec_run(
            cmd=["bash", "-c", request.command],
            workdir="/workspace",
            demux=True
        )
        
        exit_code = exec_res.exit_code
        stdout_bytes, stderr_bytes = exec_res.output or (b"", b"")
        stdout = (stdout_bytes or b"").decode("utf-8", errors="replace")
        stderr = (stderr_bytes or b"").decode("utf-8", errors="replace")
        
        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to execute command inside sandbox: {exc}")

@engine_router.post("/devops/session/{session_id}/stop", summary="Stop and clean up DevOps session")
async def api_stop_devops_session(session_id: str):
    client = get_docker_client()
    container_name = f"interleet-devops-session-{session_id}"
    
    # Remove container
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
    except Exception:
        pass
        
    # Remove workspace dir
    workspace_dir = Path(WORKSPACE_BASE) / f"devops_{session_id}"
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir, ignore_errors=True)
        
    return {"success": True}


@engine_router.websocket("/devops/session/{session_id}/ws")
async def api_ws_devops_session(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    client = get_docker_client()
    container_name = f"interleet-devops-session-{session_id}"
    
    try:
        container = client.containers.get(container_name)
    except Exception:
        await websocket.send_text("\r\n[Error: DevOps session container not found. Try resetting.]\r\n")
        await websocket.close()
        return

    import threading
    import asyncio
    import select
    import os
    
    try:
        exec_id = client.api.exec_create(
            container.id,
            cmd=["/bin/bash"],
            stdin=True,
            stdout=True,
            stderr=True,
            tty=True,
            workdir="/workspace"
        )
        sock = client.api.exec_start(exec_id, socket=True, tty=True)
    except Exception as exc:
        await websocket.send_text(f"\r\n[Error: Failed to spawn interactive terminal: {exc}]\r\n")
        await websocket.close()
        return

    loop = asyncio.get_running_loop()
    stop_event = threading.Event()
    fd = sock.fileno()
    
    def read_socket():
        """Read from the Docker exec socket using select() to properly block
        until data is available, avoiding premature EOF from buffered reads."""
        try:
            while not stop_event.is_set():
                ready, _, _ = select.select([fd], [], [], 1.0)
                if not ready:
                    continue
                try:
                    data = os.read(fd, 4096)
                except OSError:
                    break
                if not data:
                    break
                asyncio.run_coroutine_threadsafe(
                    websocket.send_text(data.decode("utf-8", errors="replace")),
                    loop
                )
        except Exception:
            pass
        finally:
            try:
                asyncio.run_coroutine_threadsafe(websocket.close(), loop)
            except Exception:
                pass

    t = threading.Thread(target=read_socket, daemon=True)
    t.start()

    try:
        while True:
            msg = await websocket.receive_text()
            try:
                os.write(fd, msg.encode("utf-8"))
            except OSError:
                break
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        stop_event.set()
        try:
            sock.close()
        except Exception:
            pass


