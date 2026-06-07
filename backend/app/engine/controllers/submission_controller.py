"""
Interleet Judge Engine — Submission Controller
Business logic for creating and retrieving executions and submissions.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from app.engine.enums import ComparisonMode, ExecutionStatus, Language, Verdict
from app.engine.executors.factory import ExecutorFactory
from app.engine.queue.redis_queue import ExecutionJob, get_execution_queue
from app.engine.schemas import (
    ExecuteRequest,
    ExecutionResult,
    RunRequest,
    SubmissionRequest,
    TestCaseSchema,
)
from app.engine.services.submission_service import SubmissionService

logger = logging.getLogger(__name__)

# Max wait time for synchronous /execute endpoint
SYNC_TIMEOUT_SECONDS = 30
SYNC_POLL_INTERVAL = 0.2


class EngineSubmissionController:
    """
    Controller that handles:
      - POST /api/v1/execute   → synchronous-style (wait for result)
      - POST /api/v1/submissions → async (enqueue and return submission_id)
      - GET  /api/v1/submissions/{id} → poll status
      - GET  /api/v1/results/{id}     → get full result
    """

    # ─── Execute (synchronous-style, waits for result) ─────────────────────

    @classmethod
    async def create_execute(cls, request: ExecuteRequest) -> dict[str, Any]:
        """
        One-shot execution:
        1. Create a job
        2. Enqueue it
        3. Poll Redis for result (up to SYNC_TIMEOUT_SECONDS)
        4. Return result

        This is the simplest path — no WebSocket needed.
        """
        submission_id = str(uuid4())
        queue = get_execution_queue()

        # Build single-testcase job
        testcase = None
        if request.expected_output is not None:
            testcase = TestCaseSchema(
                id="tc_single",
                stdin=request.stdin,
                expected_output=request.expected_output,
                hidden=False,
                weight=1.0,
                time_limit=request.time_limit,
                memory_limit=request.memory_limit,
            )

        job = ExecutionJob(
            submission_id=submission_id,
            language=request.language,
            code=request.code,
            stdin=request.stdin,
            expected_output=request.expected_output,
            time_limit=request.time_limit,
            memory_limit=request.memory_limit,
            comparison_mode=request.comparison_mode,
            mode="run",
            testcases=[testcase] if testcase else [],
        )

        # Set initial status
        await queue.set_status(submission_id, ExecutionStatus.QUEUED.value)

        # Enqueue
        await queue.enqueue(job)

        # Poll for result
        result = await cls._poll_for_result(submission_id, queue)
        if result:
            return result

        # Timeout fallback — return current status
        status = await queue.get_status(submission_id)
        return {
            "success": False,
            "submission_id": submission_id,
            "status": status.get("status", ExecutionStatus.QUEUED.value),
            "verdict": Verdict.INTERNAL_ERROR.value,
            "error": "Execution timed out waiting for worker. Check /api/v1/results/{submission_id} later.",
        }

    # ─── Run (inline test cases — for the "Run" button) ───────────────────

    @classmethod
    async def create_run(cls, request: RunRequest) -> dict[str, Any]:
        """
        Run code against inline test cases (from the frontend Run button).
        Converts inline test cases to TestCaseSchema and runs synchronously.
        """
        submission_id = str(uuid4())
        queue = get_execution_queue()

        # Convert InlineTestCase → TestCaseSchema
        testcases = [
            TestCaseSchema(
                id=tc.id,
                stdin=tc.stdin,
                expected_output=tc.expected_output,
                hidden=tc.hidden,
                name=tc.name,
                weight=1.0,
                time_limit=request.time_limit,
                memory_limit=request.memory_limit,
            )
            for tc in request.test_cases
        ]

        # Fall back to empty stdin run if no test cases provided
        if not testcases:
            testcases = [
                TestCaseSchema(
                    id="tc_default",
                    stdin="",
                    expected_output="",
                    hidden=False,
                    weight=1.0,
                )
            ]

        job = ExecutionJob(
            submission_id=submission_id,
            language=request.language,
            code=request.code,
            stdin=testcases[0].stdin,
            time_limit=request.time_limit,
            memory_limit=request.memory_limit,
            comparison_mode=request.comparison_mode,
            mode="run",
            testcases=testcases,
        )

        await queue.set_status(submission_id, ExecutionStatus.QUEUED.value)
        await queue.enqueue(job)

        result = await cls._poll_for_result(submission_id, queue)
        if result:
            return result

        # Timeout
        status = await queue.get_status(submission_id)
        return {
            "success": False,
            "submission_id": submission_id,
            "status": status.get("status", ExecutionStatus.QUEUED.value) if status else "QUEUED",
            "verdict": Verdict.INTERNAL_ERROR.value,
            "error": "Execution timed out. The sandbox may be busy.",
        }

    # ─── Submit (async — returns immediately) ─────────────────────────────

    @classmethod
    async def create_submission(cls, request: SubmissionRequest) -> dict[str, Any]:
        """
        Async submission:
        1. Create submission document in MongoDB
        2. Fetch testcases for problem (if problem_slug provided)
        3. Enqueue job
        4. Return {submission_id, status: QUEUED}
        """
        submission_id = str(uuid4())
        queue = get_execution_queue()

        # Fetch testcases from DB if this is a problem submission
        testcases: list[TestCaseSchema] = []
        if request.problem_slug and request.mode == "submit":
            raw_testcases = await SubmissionService.get_testcases_for_problem(
                request.problem_slug, include_hidden=True
            )
            testcases = [
                TestCaseSchema(
                    id=tc.get("id", str(uuid4())),
                    problem_slug=request.problem_slug,
                    stdin=tc.get("stdin", ""),
                    expected_output=tc.get("expected_output", ""),
                    hidden=tc.get("hidden", False),
                    weight=float(tc.get("weight", 1.0)),
                    time_limit=tc.get("time_limit"),
                    memory_limit=tc.get("memory_limit"),
                    name=tc.get("name"),
                )
                for tc in raw_testcases
            ]

        if not testcases and request.expected_output is not None:
            testcases = [
                TestCaseSchema(
                    id="tc_single",
                    stdin=request.stdin,
                    expected_output=request.expected_output,
                    hidden=False,
                    weight=1.0,
                    time_limit=request.time_limit,
                    memory_limit=request.memory_limit,
                )
            ]

        job = ExecutionJob(
            submission_id=submission_id,
            language=request.language,
            code=request.code,
            stdin=request.stdin,
            expected_output=request.expected_output,
            time_limit=request.time_limit,
            memory_limit=request.memory_limit,
            comparison_mode=request.comparison_mode,
            problem_slug=request.problem_slug,
            challenge_id=request.challenge_id,
            user_id=request.user_id,
            contest_id=getattr(request, "contest_id", None),
            mode=request.mode,
            testcases=testcases,
        )

        # Create submission record in MongoDB
        await SubmissionService.create_submission(
            submission_id=submission_id,
            job_data={
                "job_id": job.job_id,
                "user_id": request.user_id,
                "problem_slug": request.problem_slug,
                "challenge_id": request.challenge_id,
                "language": request.language.value,
                "code": request.code,
                "mode": request.mode,
                "total_testcases": len(testcases),
                "contest_id": getattr(request, "contest_id", None),
            },
        )

        # Set initial status in Redis
        await queue.set_status(submission_id, ExecutionStatus.QUEUED.value)

        # Enqueue job
        await queue.enqueue(job)

        return {
            "success": True,
            "submission_id": submission_id,
            "status": ExecutionStatus.QUEUED.value,
            "message": f"Submission queued with {len(testcases)} testcase(s)",
            "ws_url": f"/api/v1/ws/{submission_id}",
            "result_url": f"/api/v1/results/{submission_id}",
        }

    # ─── Get Submission Status ─────────────────────────────────────────────

    @classmethod
    async def get_submission(cls, submission_id: str) -> Optional[dict[str, Any]]:
        """
        Get current submission status.
        Checks Redis first (fast), falls back to MongoDB.
        """
        queue = get_execution_queue()

        # Check Redis for cached result
        result = await queue.get_result(submission_id)
        if result:
            return result

        # Check Redis for status
        status = await queue.get_status(submission_id)
        if status:
            return {
                "submission_id": submission_id,
                "status": status.get("status", ExecutionStatus.QUEUED.value),
                **status,
            }

        # Fall back to MongoDB
        return await SubmissionService.get_submission(submission_id)

    # ─── Get Full Result ───────────────────────────────────────────────────

    @classmethod
    async def get_result(cls, submission_id: str) -> Optional[dict[str, Any]]:
        """
        Get full execution result.
        Checks Redis cache first, then MongoDB.
        """
        queue = get_execution_queue()

        # Check Redis cache
        cached = await queue.get_result(submission_id)
        if cached:
            return cached

        # Fetch from MongoDB
        return await SubmissionService.get_result(submission_id)

    # ─── Internal ──────────────────────────────────────────────────────────

    @staticmethod
    async def _poll_for_result(
        submission_id: str,
        queue,
        timeout: float = SYNC_TIMEOUT_SECONDS,
    ) -> Optional[dict[str, Any]]:
        """Poll Redis for a result up to `timeout` seconds."""
        deadline = asyncio.get_event_loop().time() + timeout

        while asyncio.get_event_loop().time() < deadline:
            result = await queue.get_result(submission_id)
            if result:
                return result

            status = await queue.get_status(submission_id)
            current = status.get("status", "") if status else ""
            if current in (ExecutionStatus.COMPLETED.value, ExecutionStatus.FAILED.value):
                return result

            await asyncio.sleep(SYNC_POLL_INTERVAL)

        return None
