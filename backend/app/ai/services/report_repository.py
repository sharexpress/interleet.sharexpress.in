from __future__ import annotations

from datetime import datetime
from typing import Any

from app.core.db import get_db


class InterviewReportRepository:
    collection_name = "interview_reports"

    @classmethod
    async def save_report(
        cls,
        *,
        session_id: str,
        report: dict[str, Any],
        state: dict[str, Any],
    ) -> None:
        db = get_db()
        user_id = (
            state.get("user_id")
            or state.get("candidate_id")
            or (state.get("metadata") or {}).get("user_id")
        )
        document = {
            "session_id": session_id,
            "user_id": user_id,
            "role": state.get("role"),
            "interview_type": state.get("interview_type"),
            "report": report,
            "created_at": datetime.utcnow(),
        }

        # Check if this is a NEW report (upsert may be updating an existing one)
        existing = await db[cls.collection_name].find_one({"session_id": session_id})
        is_new_report = existing is None

        await db[cls.collection_name].update_one(
            {"session_id": session_id},
            {"$set": document},
            upsert=True,
        )

        # Update user stats only when this is the first time saving this session
        if is_new_report and user_id:
            overall_score = (
                report.get("overall_score")
                or report.get("average_score")
                or 0
            )
            try:
                await db.users.update_one(
                    {"user_id": user_id},
                    {
                        "$inc": {"interview_count": 1},
                        "$set": {
                            "last_interview_at": datetime.utcnow(),
                            "last_interview_role": state.get("role", ""),
                            "last_interview_score": overall_score,
                        },
                    },
                )
            except Exception:
                # Non-fatal — profile stats will still be computed from interview_reports
                pass

    @classmethod
    async def get_report(cls, session_id: str) -> dict[str, Any] | None:
        db = get_db()
        document = await db[cls.collection_name].find_one(
            {"session_id": session_id},
            {"_id": 0},
        )
        return document

    @classmethod
    async def list_reports(
        cls,
        *,
        user_id: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        db = get_db()
        query = {"user_id": user_id} if user_id else {}
        cursor = (
            db[cls.collection_name]
            .find(query, {"_id": 0})
            .sort("created_at", -1)
            .limit(limit)
        )
        return [document async for document in cursor]
