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
        await db[cls.collection_name].update_one(
            {"session_id": session_id},
            {"$set": document},
            upsert=True,
        )

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
