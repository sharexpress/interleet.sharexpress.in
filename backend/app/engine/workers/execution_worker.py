"""
Interleet Judge Engine — Async Execution Worker
Consumes jobs from Redis queue and executes them in Docker sandboxes.

Each worker coroutine:
  1. Dequeues a job from Redis
  2. Updates status → QUEUED → COMPILING → RUNNING → JUDGING
  3. Broadcasts WebSocket events at each stage
  4. Runs the executor for each testcase
  5. Scores results via JudgeEngine
  6. Saves final result to MongoDB
  7. Broadcasts COMPLETED / FAILED
"""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime

from app.engine.enums import ExecutionStatus, Verdict, WebSocketEventType
from app.engine.executors.factory import ExecutorFactory
from app.engine.judge import JudgeEngine
from app.engine.queue.redis_queue import ExecutionJob, get_execution_queue
from app.engine.schemas import (
    ExecutionResult,
    TestCaseResult,
    TestCaseSchema,
    WebSocketEvent,
)
from app.core.db import get_db

logger = logging.getLogger(__name__)

WORKER_COUNT = int(os.environ.get("WORKER_COUNT", 4))
WORKER_SHUTDOWN = asyncio.Event()


class ExecutionWorker:
    """Single async worker that processes one job at a time from the queue."""

    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.queue = get_execution_queue()

    async def run(self) -> None:
        """Main worker loop — runs until WORKER_SHUTDOWN is set."""
        logger.info("Worker #%d started", self.worker_id)
        while not WORKER_SHUTDOWN.is_set():
            try:
                job = await self.queue.dequeue(timeout=5)
                if job is None:
                    continue  # timeout, check shutdown flag and retry
                await self._process_job(job)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.exception("Worker #%d unexpected error: %s", self.worker_id, exc)
                await asyncio.sleep(1)

        logger.info("Worker #%d stopped", self.worker_id)

    async def _process_job(self, job: ExecutionJob) -> None:
        """Full execution pipeline for a single job."""
        submission_id = job.submission_id
        logger.info(
            "Worker #%d processing job=%s lang=%s mode=%s",
            self.worker_id, job.job_id, job.language, job.mode,
        )

        try:
            # ── Phase 1: Queued ──────────────────────────────────────────
            await self._update_status(submission_id, ExecutionStatus.QUEUED)
            await self._broadcast(submission_id, WebSocketEventType.QUEUED, ExecutionStatus.QUEUED)

            executor = ExecutorFactory.get(job.language)

            # Determine testcases
            testcases = job.testcases
            if not testcases:
                # Single-testcase run (direct execute mode)
                testcases = [
                    TestCaseSchema(
                        id="tc_single",
                        stdin=job.stdin,
                        expected_output=job.expected_output or "",
                        hidden=False,
                        weight=1.0,
                    )
                ]

            # ── Phase 2: Compile (if needed) ────────────────────────────
            compile_output = ""
            if executor.requires_compile:
                await self._update_status(submission_id, ExecutionStatus.COMPILING)
                await self._broadcast(submission_id, WebSocketEventType.COMPILING, ExecutionStatus.COMPILING)

            # ── Phase 3: Run testcases ───────────────────────────────────
            await self._update_status(submission_id, ExecutionStatus.RUNNING)
            await self._broadcast(submission_id, WebSocketEventType.RUNNING, ExecutionStatus.RUNNING)

            testcase_results: list[TestCaseResult] = []

            for i, testcase in enumerate(testcases):
                logger.debug(
                    "Worker #%d running testcase %d/%d for %s",
                    self.worker_id, i + 1, len(testcases), submission_id,
                )
                try:
                    sandbox_result, compile_result = await executor.run_testcase(
                        code=job.code,
                        testcase=testcase,
                        time_limit=testcase.time_limit or job.time_limit,
                        memory_limit=testcase.memory_limit or job.memory_limit,
                        comparison_mode=job.comparison_mode,
                    )
                    if compile_result is not None:
                        compile_output = compile_result.error or compile_result.output

                    tc_result = JudgeEngine.evaluate(
                        sandbox_result=sandbox_result,
                        testcase=testcase,
                        compile_output=compile_output if compile_result and not compile_result.success else "",
                        comparison_mode=job.comparison_mode,
                    )
                    testcase_results.append(tc_result)

                    # Early exit on compilation error
                    if tc_result.verdict == Verdict.COMPILATION_ERROR:
                        break

                except Exception as exc:
                    logger.exception(
                        "Worker #%d testcase %d error: %s", self.worker_id, i, exc
                    )
                    testcase_results.append(
                        TestCaseResult(
                            testcase_id=testcase.id,
                            hidden=testcase.hidden,
                            verdict=Verdict.INTERNAL_ERROR,
                            passed=False,
                            stderr=str(exc),
                        )
                    )

            # ── Phase 4: Judge ───────────────────────────────────────────
            await self._update_status(submission_id, ExecutionStatus.JUDGING)
            await self._broadcast(submission_id, WebSocketEventType.JUDGING, ExecutionStatus.JUDGING)

            scoring = JudgeEngine.score(testcase_results)

            # Build first testcase stdout/stderr for non-submission runs
            first_result = testcase_results[0] if testcase_results else None
            stdout = first_result.stdout if first_result else ""
            stderr = first_result.stderr if first_result else ""
            exit_code = first_result.exit_code if first_result else 0

            execution_result = ExecutionResult(
                success=(scoring.verdict == Verdict.ACCEPTED),
                submission_id=submission_id,
                status=ExecutionStatus.COMPLETED,
                verdict=scoring.verdict,
                stdout=stdout,
                stderr=stderr,
                compile_output=compile_output,
                memory=scoring.max_memory_mb,
                time=round(scoring.max_time_ms / 1000, 4),
                exit_code=exit_code,
                testcase_results=testcase_results,
                passed_testcases=scoring.passed,
                total_testcases=scoring.total,
                score=scoring.score,
                completed_at=datetime.utcnow(),
            )

            # ── Phase 5: Persist to MongoDB ──────────────────────────────
            await self._save_result(job, execution_result)

            # ── Phase 6: Cache in Redis ──────────────────────────────────
            await self.queue.store_result(
                submission_id,
                execution_result.model_dump(mode="json"),
            )

            # ── Phase 7: Broadcast Completed ─────────────────────────────
            await self._update_status(
                submission_id,
                ExecutionStatus.COMPLETED,
                {
                    "verdict": scoring.verdict.value,
                    "score": scoring.score,
                    "passed": scoring.passed,
                    "total": scoring.total,
                },
            )
            await self._broadcast(
                submission_id,
                WebSocketEventType.COMPLETED,
                ExecutionStatus.COMPLETED,
                {
                    "verdict": scoring.verdict.value,
                    "score": scoring.score,
                    "passed": scoring.passed,
                    "total": scoring.total,
                    "time": execution_result.time,
                    "memory": execution_result.memory,
                },
            )

            logger.info(
                "Worker #%d completed job=%s verdict=%s score=%.1f",
                self.worker_id, job.job_id, scoring.verdict, scoring.score,
            )

        except Exception as exc:
            logger.exception(
                "Worker #%d failed job=%s: %s", self.worker_id, job.job_id, exc
            )
            await self._update_status(
                submission_id, ExecutionStatus.FAILED, {"error": str(exc)}
            )
            await self._broadcast(
                submission_id,
                WebSocketEventType.FAILED,
                ExecutionStatus.FAILED,
                {"error": str(exc)},
            )
            await self._save_failed(job, str(exc))

    # ─── Internal Helpers ──────────────────────────────────────────────────

    async def _update_status(
        self, submission_id: str, status: ExecutionStatus, data: dict | None = None
    ) -> None:
        try:
            await self.queue.set_status(submission_id, status.value, data)
        except Exception as exc:
            logger.warning("Failed to update Redis status: %s", exc)

    async def _broadcast(
        self,
        submission_id: str,
        event_type: WebSocketEventType,
        status: ExecutionStatus,
        data: dict | None = None,
    ) -> None:
        try:
            from app.engine.websocket.manager import ws_manager

            event = WebSocketEvent(
                type=event_type,
                submission_id=submission_id,
                status=status,
                data=data,
            )
            await ws_manager.broadcast(submission_id, event)
        except Exception as exc:
            logger.warning("WebSocket broadcast failed: %s", exc)

    @staticmethod
    async def _save_result(job: ExecutionJob, result: ExecutionResult) -> None:
        """Persist execution result to MongoDB."""
        try:
            db = get_db()
            doc = {
                "submission_id": job.submission_id,
                "job_id": job.job_id,
                "user_id": job.user_id,
                "problem_slug": job.problem_slug,
                "challenge_id": job.challenge_id,
                "language": job.language.value,
                "mode": job.mode,
                "verdict": result.verdict.value,
                "status": result.status.value,
                "score": result.score,
                "passed_testcases": result.passed_testcases,
                "total_testcases": result.total_testcases,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "compile_output": result.compile_output,
                "time_seconds": result.time,
                "memory_mb": result.memory,
                "exit_code": result.exit_code,
                "testcase_results": [tc.model_dump(mode="json") for tc in result.testcase_results],
                "created_at": datetime.utcnow(),
                "completed_at": result.completed_at,
            }

            # Store in engine_results collection
            await db.engine_results.insert_one(doc)

            # For submissions (mode=submit), also update the submissions collection
            if job.mode == "submit" and job.problem_slug:
                submission_doc = {
                    "id": job.submission_id,
                    "user_id": job.user_id,
                    "problem_slug": job.problem_slug,
                    "challenge_id": job.challenge_id,
                    "language": job.language.value,
                    "source_code": job.code,
                    "status": _map_verdict_to_status(result.verdict),
                    "verdict": result.verdict.value,
                    "score": result.score,
                    "passed": result.passed_testcases,
                    "total": result.total_testcases,
                    "runtime_ms": round(result.time * 1000, 2),
                    "memory_mb": result.memory,
                    "results": [tc.model_dump(mode="json") for tc in result.testcase_results],
                    "created_at": datetime.utcnow(),
                    "completed_at": result.completed_at,
                }
                # Upsert to submissions
                await db.submissions.update_one(
                    {"id": job.submission_id},
                    {"$set": submission_doc},
                    upsert=True,
                )
        except Exception as exc:
            logger.error("Failed to save result to MongoDB: %s", exc)

    @staticmethod
    async def _save_failed(job: ExecutionJob, error: str) -> None:
        """Persist a failed job to MongoDB."""
        try:
            db = get_db()
            await db.engine_results.insert_one({
                "submission_id": job.submission_id,
                "job_id": job.job_id,
                "language": job.language.value,
                "mode": job.mode,
                "verdict": Verdict.INTERNAL_ERROR.value,
                "status": ExecutionStatus.FAILED.value,
                "error": error,
                "created_at": datetime.utcnow(),
                "completed_at": datetime.utcnow(),
            })
        except Exception as exc:
            logger.error("Failed to save error result to MongoDB: %s", exc)


def _map_verdict_to_status(verdict: Verdict) -> str:
    mapping = {
        Verdict.ACCEPTED: "accepted",
        Verdict.WRONG_ANSWER: "wrong_answer",
        Verdict.TIME_LIMIT_EXCEEDED: "time_limit_exceeded",
        Verdict.MEMORY_LIMIT_EXCEEDED: "memory_limit_exceeded",
        Verdict.COMPILATION_ERROR: "compilation_error",
        Verdict.RUNTIME_ERROR: "runtime_error",
        Verdict.INTERNAL_ERROR: "failed",
    }
    return mapping.get(verdict, "failed")
