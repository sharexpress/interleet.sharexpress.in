from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from app.core.config import JUDGE0_API_KEY, JUDGE0_API_URL, JUDGE0_CALLBACK_URL, JUDGE0_RAPIDAPI_HOST
from app.core.db import get_db
from app.data.seed import CHALLENGES


LANGUAGE_IDS = {
    "python": 71,
    "javascript": 63,
    "typescript": 74,
    "java": 62,
    "cpp": 54,
    "go": 60,
}


PENDING_STATUS_IDS = {1, 2}
ACCEPTED_STATUS_ID = 3


class Judge0Client:
    def __init__(self):
        self.base_url = JUDGE0_API_URL.rstrip("/")

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if JUDGE0_API_KEY:
            headers["X-RapidAPI-Key"] = JUDGE0_API_KEY
            headers["X-RapidAPI-Host"] = JUDGE0_RAPIDAPI_HOST
        return headers

    async def submit(self, source_code: str, language: str, testcase: dict[str, Any]) -> str:
        if "rapidapi.com" in self.base_url and not JUDGE0_API_KEY:
            raise RuntimeError("JUDGE0_API_KEY is required for the default RapidAPI Judge0 endpoint")
        language_id = LANGUAGE_IDS.get(language)
        if language_id is None:
            raise ValueError(f"Unsupported language: {language}")

        payload = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": testcase.get("stdin", ""),
            "cpu_time_limit": testcase.get("time_limit"),
            "memory_limit": testcase.get("memory_limit"),
        }
        payload = {key: value for key, value in payload.items() if value is not None}
        if JUDGE0_CALLBACK_URL:
            payload["callback_url"] = JUDGE0_CALLBACK_URL

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{self.base_url}/submissions",
                params={"base64_encoded": "false", "wait": "false"},
                headers=self._headers(),
                json=payload,
            )
            response.raise_for_status()
            return response.json()["token"]

    async def get_result(self, token: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{self.base_url}/submissions/{token}",
                params={"base64_encoded": "false", "fields": "*"},
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()


class EvaluationEngine:
    @staticmethod
    def evaluate(judge0_result: dict[str, Any], testcase: dict[str, Any]) -> dict[str, Any]:
        status = judge0_result.get("status") or {}
        status_id = status.get("id")
        stdout = judge0_result.get("stdout") or ""
        stderr = judge0_result.get("stderr") or ""
        compile_output = judge0_result.get("compile_output") or ""
        expected = testcase.get("expected_output", "")
        output_matches = stdout.strip() == expected.strip()
        passed = status_id == ACCEPTED_STATUS_ID and output_matches

        return {
            "testcase_id": testcase.get("id"),
            "name": testcase.get("name"),
            "hidden": testcase.get("hidden", False),
            "passed": passed,
            "verdict": "Accepted" if passed else status.get("description", "Wrong Answer"),
            "stdout": "" if testcase.get("hidden") else stdout,
            "expected_output": "" if testcase.get("hidden") else expected,
            "stderr": stderr,
            "compile_output": compile_output,
            "runtime_ms": _seconds_to_ms(judge0_result.get("time")),
            "memory_kb": judge0_result.get("memory"),
            "weight": testcase.get("weight", 1),
        }


class ScoringEngine:
    @staticmethod
    def score(results: list[dict[str, Any]]) -> dict[str, Any]:
        total_weight = sum(float(result.get("weight", 1)) for result in results) or 1
        passed_weight = sum(float(result.get("weight", 1)) for result in results if result.get("passed"))
        score = round((passed_weight / total_weight) * 100, 2)
        passed = sum(1 for result in results if result.get("passed"))
        total = len(results)

        if passed == total:
            verdict = "Accepted"
        elif any("Compilation Error" in result.get("verdict", "") for result in results):
            verdict = "Compile Error"
        elif any("Time Limit" in result.get("verdict", "") for result in results):
            verdict = "Time Limit Exceeded"
        elif any("Runtime Error" in result.get("verdict", "") for result in results):
            verdict = "Runtime Error"
        else:
            verdict = "Wrong Answer"

        runtimes = [result["runtime_ms"] for result in results if result.get("runtime_ms") is not None]
        memories = [result["memory_kb"] for result in results if result.get("memory_kb") is not None]
        return {
            "score": score,
            "passed": passed,
            "total": total,
            "verdict": verdict,
            "runtime_ms": max(runtimes) if runtimes else None,
            "memory_kb": max(memories) if memories else None,
        }


class CodeExecutionService:
    judge0 = Judge0Client()
    db = get_db()

    @classmethod
    async def create_job(cls, payload, *, user_id: str | None = None) -> dict[str, Any]:
        problem = await cls._get_problem(payload.problem_slug or payload.problem_id)
        testcases = await cls._get_testcases(problem["slug"], include_hidden=payload.mode == "submit")
        if not testcases:
            raise ValueError("Problem has no executable test cases")

        job = {
            "id": _new_id("exec"),
            "user_id": user_id,
            "problem_id": payload.problem_id or problem.get("id"),
            "problem_slug": problem["slug"],
            "mode": payload.mode,
            "language": payload.language,
            "source_code": payload.source_code,
            "status": "running",
            "judge0_tokens": [],
            "testcase_ids": [case["id"] for case in testcases],
            "results": [],
            "passed": 0,
            "total": len(testcases),
            "score": 0,
            "verdict": "Running",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "completed_at": None,
        }

        try:
            tokens = []
            for testcase in testcases:
                tokens.append(await cls.judge0.submit(payload.source_code, payload.language, testcase))
            job["judge0_tokens"] = tokens
        except (httpx.HTTPError, RuntimeError) as exc:
            job.update({"status": "configuration_error", "verdict": "Judge0 Unavailable", "error": str(exc)})
        except ValueError as exc:
            job.update({"status": "failed", "verdict": "Unsupported Language", "error": str(exc)})

        await cls.db.execution_jobs.insert_one(job)
        if payload.mode == "submit":
            await cls.db.submissions.insert_one(cls._submission_from_job(job))
        return cls._public_job(job, include_hidden=False)

    @classmethod
    async def get_job(cls, job_id: str) -> dict[str, Any] | None:
        job = await cls.db.execution_jobs.find_one({"id": job_id})
        if not job:
            return None
        if job.get("status") == "running":
            job = await cls._refresh_job(job)
        return cls._public_job(job, include_hidden=job.get("mode") == "submit")

    @classmethod
    async def list_submissions(cls, problem_slug: str | None = None, limit: int = 20) -> dict[str, Any]:
        query = {"problem_slug": problem_slug} if problem_slug else {}
        submissions = [submission async for submission in cls.db.submissions.find(query)]
        submissions.sort(key=lambda item: item.get("created_at", datetime.min), reverse=True)
        items = []
        for submission in submissions[:limit]:
            item = dict(submission)
            item.pop("_id", None)
            items.append(item)
        return {"items": items, "count": len(items)}

    @classmethod
    async def get_submission(cls, submission_id: str) -> dict[str, Any] | None:
        submission = await cls.db.submissions.find_one({"id": submission_id})
        if not submission:
            return None
        submission.pop("_id", None)
        return submission

    @classmethod
    async def _refresh_job(cls, job: dict[str, Any]) -> dict[str, Any]:
        testcases = await cls._get_testcases(job["problem_slug"], include_hidden=job.get("mode") == "submit")
        results = []
        still_running = False

        try:
            for token, testcase in zip(job.get("judge0_tokens", []), testcases):
                judge0_result = await cls.judge0.get_result(token)
                status_id = (judge0_result.get("status") or {}).get("id")
                if status_id in PENDING_STATUS_IDS:
                    still_running = True
                    continue
                results.append(EvaluationEngine.evaluate(judge0_result, testcase))
        except httpx.HTTPError as exc:
            await cls.db.execution_jobs.find_one_and_update(
                {"id": job["id"]},
                {"$set": {"status": "failed", "verdict": "Judge0 Poll Failed", "error": str(exc), "updated_at": datetime.utcnow()}},
            )
            job.update({"status": "failed", "verdict": "Judge0 Poll Failed", "error": str(exc)})
            return job

        if still_running or len(results) < len(testcases):
            await cls.db.execution_jobs.find_one_and_update(
                {"id": job["id"]},
                {"$set": {"results": results, "updated_at": datetime.utcnow()}},
            )
            job["results"] = results
            return job

        scoring = ScoringEngine.score(results)
        status = "completed"
        completed = datetime.utcnow()
        updates = {
            "status": status,
            "results": results,
            "completed_at": completed,
            "updated_at": completed,
            **scoring,
        }
        await cls.db.execution_jobs.find_one_and_update({"id": job["id"]}, {"$set": updates})
        job.update(updates)
        for token, result in zip(job.get("judge0_tokens", []), results):
            await cls.db.execution_results.insert_one(
                {
                    "id": _new_id("result"),
                    "execution_job_id": job["id"],
                    "submission_id": job["id"].replace("exec", "sub", 1)
                    if job.get("mode") == "submit"
                    else None,
                    "problem_slug": job.get("problem_slug"),
                    "testcase_id": result.get("testcase_id"),
                    "judge0_token": token,
                    "status": job.get("status"),
                    "verdict": result.get("verdict"),
                    "passed": result.get("passed", False),
                    "runtime_ms": result.get("runtime_ms"),
                    "memory_kb": result.get("memory_kb"),
                    "stdout": result.get("stdout", ""),
                    "stderr": result.get("stderr", ""),
                    "compile_output": result.get("compile_output", ""),
                    "analytics": {
                        "hidden": result.get("hidden", False),
                        "weight": result.get("weight", 1),
                    },
                    "created_at": datetime.utcnow(),
                }
            )
        if job.get("mode") == "submit":
            await cls.db.submissions.find_one_and_update(
                {"id": job["id"].replace("exec", "sub", 1)},
                {"$set": cls._submission_from_job(job)},
            )
        return job

    @classmethod
    async def _get_problem(cls, slug_or_id: str | None) -> dict[str, Any]:
        if not slug_or_id:
            raise ValueError("problem_id or problem_slug is required")
        stored = await cls.db.problems.find_one({"slug": slug_or_id})
        if stored:
            return stored
        stored = await cls.db.problems.find_one({"id": slug_or_id})
        if stored:
            return stored
        for problem in CHALLENGES:
            if problem.get("slug") == slug_or_id or problem.get("id") == slug_or_id:
                return problem
        raise ValueError("Problem not found")

    @classmethod
    async def _get_testcases(cls, problem_slug: str, *, include_hidden: bool) -> list[dict[str, Any]]:
        stored = [
            case
            async for case in cls.db.test_cases.find(
                {"problem_slug": problem_slug}
            )
            if include_hidden or not case.get("hidden")
        ]
        if stored:
            return stored
        problem = await cls._get_problem(problem_slug)
        return [
            case
            for case in problem.get("test_cases", [])
            if include_hidden or not case.get("hidden")
        ]

    @staticmethod
    def _submission_from_job(job: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": job["id"].replace("exec", "sub", 1),
            "user_id": job.get("user_id"),
            "problem_slug": job.get("problem_slug"),
            "language": job.get("language"),
            "source_code": job.get("source_code"),
            "status": _submission_status(job.get("verdict", "Running")),
            "verdict": job.get("verdict", "Running"),
            "score": job.get("score", 0),
            "passed": job.get("passed", 0),
            "total": job.get("total", 0),
            "runtime_ms": job.get("runtime_ms"),
            "memory_kb": job.get("memory_kb"),
            "results": job.get("results", []),
            "created_at": job.get("created_at", datetime.utcnow()),
            "completed_at": job.get("completed_at"),
        }

    @staticmethod
    def _public_job(job: dict[str, Any], *, include_hidden: bool) -> dict[str, Any]:
        public = dict(job)
        public.pop("_id", None)
        if not include_hidden:
            public["results"] = [
                result for result in public.get("results", []) if not result.get("hidden")
            ]
        public["poll_url"] = f"/api/execution/{public['id']}"
        return public


def _seconds_to_ms(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value) * 1000, 2)
    except (TypeError, ValueError):
        return None


def _new_id(prefix: str) -> str:
    return f"{prefix}_{int(datetime.utcnow().timestamp() * 1000)}"


def _submission_status(verdict: str) -> str:
    mapping = {
        "Accepted": "accepted",
        "Wrong Answer": "wrong_answer",
        "Runtime Error": "runtime_error",
        "Time Limit Exceeded": "time_limit_exceeded",
        "Compile Error": "compile_error",
    }
    return mapping.get(verdict, "running")
