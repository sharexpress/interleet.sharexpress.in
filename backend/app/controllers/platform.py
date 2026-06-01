from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

from app.core.db import get_db
from app.data.seed import (
    ACTIVITY_WEEKLY,
    CANDIDATES,
    CHALLENGES,
    DOMAINS,
    INTERVIEW_HISTORY,
    LEADERBOARD,
    RECENT_ACTIVITY,
    SYSTEM_DESIGN_TOPICS,
    USER_PROFILE,
)

db = get_db()


def _serialize(doc: dict) -> dict:
    result = dict(doc)
    result["_id"] = str(result["_id"]) if "_id" in result else result.get("id")
    return result


async def _collection_or_seed(collection_name: str, seed: list[dict]) -> list[dict]:
    collection = db[collection_name]
    docs = [_serialize(doc) async for doc in collection.find({})]
    return docs or seed


def _matches_text(challenge: dict, query: str) -> bool:
    haystack = " ".join(
        [
            challenge.get("title", ""),
            challenge.get("summary", ""),
            " ".join(challenge.get("tags", [])),
        ]
    ).lower()
    return query.lower() in haystack


class PlatformController:
    @staticmethod
    async def dashboard():
        return {
            "user": USER_PROFILE,
            "activityWeekly": ACTIVITY_WEEKLY,
            "recentActivity": RECENT_ACTIVITY,
            "recommendedChallenges": CHALLENGES[:4],
            "interviewTrend": [
                {"d": "W1", "s": 62},
                {"d": "W2", "s": 65},
                {"d": "W3", "s": 71},
                {"d": "W4", "s": 70},
                {"d": "W5", "s": 76},
                {"d": "W6", "s": 78},
                {"d": "W7", "s": 81},
                {"d": "W8", "s": 84},
            ],
        }

    @staticmethod
    async def list_challenges(
        q: str | None = None,
        domain: str | None = None,
        difficulty: str | None = None,
        sort: str = "popular",
    ):
        challenges = await _collection_or_seed("problems", CHALLENGES)
        items = []
        for challenge in challenges:
            if domain and domain != "all" and challenge.get("domain") != domain:
                continue
            if difficulty and difficulty != "all" and challenge.get("difficulty") != difficulty:
                continue
            if q and not _matches_text(challenge, q):
                continue
            items.append(challenge)

        if sort == "xp":
            items.sort(key=lambda c: c.get("xp", 0), reverse=True)
        elif sort == "time":
            items.sort(key=lambda c: c.get("minutes", 0))
        elif sort == "completion":
            items.sort(key=lambda c: c.get("completion", 0), reverse=True)

        return {"items": items, "count": len(items), "domains": DOMAINS}

    @staticmethod
    async def get_challenge(slug: str):
        challenges = await _collection_or_seed("problems", CHALLENGES)
        challenge = next((item for item in challenges if item.get("slug") == slug or item.get("id") == slug), None)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        return challenge

    @staticmethod
    async def create_challenge(payload: dict):
        now = datetime.utcnow()
        slug = payload.get("slug") or payload.get("title", "").lower().replace(" ", "-")
        challenge = {
            "id": payload.get("id") or str(uuid4()),
            "slug": slug,
            "completion": 0,
            "created_at": now,
            "updated_at": now,
            "is_active": True,
            **payload,
        }
        await db.problems.insert_one(challenge)
        return {"success": True, "challenge": challenge}

    @staticmethod
    async def leaderboard(limit: int = 50):
        items = await _collection_or_seed("leaderboards", LEADERBOARD)
        items.sort(key=lambda entry: entry.get("rank", 999999))
        return {"items": items[:limit], "count": min(len(items), limit)}

    @staticmethod
    async def profile(username: str | None = None):
        if username and username != USER_PROFILE["username"]:
            user = await db.users.find_one({"username": username}, {"_id": 0})
            if user:
                return user
        return USER_PROFILE

    @staticmethod
    async def activity():
        return {"weekly": ACTIVITY_WEEKLY, "recent": RECENT_ACTIVITY}

    @staticmethod
    async def interviews():
        return {"history": INTERVIEW_HISTORY}

    @staticmethod
    async def system_design():
        return {"topics": SYSTEM_DESIGN_TOPICS}

    @staticmethod
    async def candidates():
        return {"items": CANDIDATES}
