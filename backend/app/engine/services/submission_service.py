"""
Interleet Judge Engine — Submission Service
MongoDB CRUD operations for engine submissions and results.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

from app.core.db import get_db
from app.engine.enums import ExecutionStatus

logger = logging.getLogger(__name__)


class SubmissionService:
    """
    Data access layer for:
      - engine_submissions: async submissions linked to problems
      - engine_results: all execution results (including one-shot runs)
    """

    # ─── Submission CRUD ───────────────────────────────────────────────────

    @staticmethod
    async def create_submission(
        submission_id: str,
        job_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Insert a new submission record with QUEUED status."""
        db = get_db()
        doc = {
            "id": submission_id,
            "status": ExecutionStatus.QUEUED.value,
            "verdict": None,
            "created_at": datetime.utcnow(),
            "completed_at": None,
            **job_data,
        }
        await db.engine_submissions.insert_one(doc)
        doc.pop("_id", None)
        return doc

    @staticmethod
    async def get_submission(submission_id: str) -> Optional[dict[str, Any]]:
        """Get a submission by ID."""
        db = get_db()
        doc = await db.engine_submissions.find_one({"id": submission_id})
        if doc:
            doc.pop("_id", None)
        return doc

    @staticmethod
    async def update_submission(
        submission_id: str, updates: dict[str, Any]
    ) -> None:
        """Update a submission document."""
        db = get_db()
        updates["updated_at"] = datetime.utcnow()
        await db.engine_submissions.update_one(
            {"id": submission_id},
            {"$set": updates},
            upsert=True,
        )

    @staticmethod
    async def list_submissions(
        user_id: Optional[str] = None,
        problem_slug: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
    ) -> dict[str, Any]:
        """List submissions with optional filters."""
        db = get_db()
        query: dict[str, Any] = {}
        if user_id:
            query["user_id"] = user_id
        if problem_slug:
            query["problem_slug"] = problem_slug

        cursor = db.engine_submissions.find(query).sort("created_at", -1).skip(skip).limit(limit)
        items = []
        async for doc in cursor:
            doc.pop("_id", None)
            items.append(doc)

        total = await db.engine_submissions.count_documents(query)
        return {"items": items, "total": total, "limit": limit, "skip": skip}

    # ─── Execution Result CRUD ─────────────────────────────────────────────

    @staticmethod
    async def get_result(submission_id: str) -> Optional[dict[str, Any]]:
        """Get execution result by submission ID."""
        db = get_db()
        # Try engine_results first
        doc = await db.engine_results.find_one(
            {"submission_id": submission_id},
            sort=[("created_at", -1)],
        )
        if doc:
            doc.pop("_id", None)
            return doc
        return None

    @staticmethod
    async def get_result_by_id(result_id: str) -> Optional[dict[str, Any]]:
        """Get execution result by its own ID."""
        db = get_db()
        doc = await db.engine_results.find_one({"id": result_id})
        if doc:
            doc.pop("_id", None)
        return doc

    @staticmethod
    async def get_testcases_for_problem(
        problem_slug: str,
        include_hidden: bool = False,
    ) -> list[dict[str, Any]]:
        """Fetch test cases for a problem from MongoDB."""
        db = get_db()
        query: dict[str, Any] = {"problem_slug": problem_slug}
        if not include_hidden:
            query["hidden"] = {"$ne": True}

        testcases = []
        async for doc in db.test_cases.find(query).sort("weight", 1):
            doc.pop("_id", None)
            testcases.append(doc)
        return testcases

    @staticmethod
    async def health() -> dict[str, Any]:
        """Basic DB health check."""
        try:
            db = get_db()
            count = await db.engine_results.count_documents({})
            return {"status": "ok", "engine_results_count": count}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}
