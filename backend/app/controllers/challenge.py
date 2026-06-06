from __future__ import annotations

from datetime import datetime
from math import ceil
from typing import Optional
from fastapi import HTTPException

from app.core.db import get_db
from app.data.seed import CHALLENGES, DOMAINS
from app.models.challenge import ChallengeModel, ChallengeDomain, ChallengeDifficulty

db = get_db()


def _serialize(doc: dict) -> dict:
    doc = dict(doc)
    doc.pop("_id", None)
    return doc


def _to_frontend(doc: dict) -> dict:
    """Map DB/model field names → what the frontend expects."""
    return {
        "id": doc.get("id") or str(doc.get("challenge_id", "")),
        "slug": doc.get("slug", ""),
        "title": doc.get("title", ""),
        "domain": doc.get("domain", ""),
        "difficulty": doc.get("difficulty", ""),
        "minutes": doc.get("minutes") or doc.get("estimated_time_minutes", 0),
        "xp": doc.get("xp") or doc.get("xp_reward", 0),
        "completion": doc.get("completion") or doc.get("success_rate", 0),
        "tags": doc.get("tags", []),
        "summary": doc.get("summary") or doc.get("short_description", ""),
        "description": doc.get("description", ""),
        "hints": doc.get("hints", []),
        "starter_code": doc.get("starter_code", {}),
        "test_cases": doc.get("test_cases", []),
        "is_featured": doc.get("is_featured", False),
        "is_published": doc.get("is_published", True),
    }


async def _all_from_db() -> list[dict]:
    cursor = db.problems.find({"is_archived": {"$ne": True}})
    docs = [_serialize(doc) async for doc in cursor]

    return docs if docs else False


class ChallengeController:
    @staticmethod
    async def list_challenges(
        q: Optional[str] = None,
        domain: Optional[str] = None,
        difficulty: Optional[str] = None,
        sort: str = "popular",
        page: int = 1,
        limit: int = 50,
    ):
        all_docs = await _all_from_db()

        if all_docs is False:
            raise HTTPException(status_code=404, detail="challenges not found ")

        items = []
        for doc in all_docs:
            c = _to_frontend(doc)

            if domain and domain != "all" and c["domain"].lower() != domain.lower():
                continue
            if (
                difficulty
                and difficulty != "all"
                and c["difficulty"].lower() != difficulty.lower()
            ):
                continue
            if q:
                haystack = f"{c['title']} {' '.join(c['tags'])} {c['summary']}".lower()
                if q.lower() not in haystack:
                    continue
            items.append(c)

        if sort == "xp":
            items.sort(key=lambda c: c["xp"], reverse=True)
        elif sort == "time":
            items.sort(key=lambda c: c["minutes"])
        elif sort == "completion":
            items.sort(key=lambda c: c["completion"], reverse=True)

        total = len(items)
        start = (page - 1) * limit
        page_items = items[start : start + limit]

        return {
            "success": True,
            "data": page_items,
            "total": total,
            "domains": DOMAINS,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": ceil(total / limit) if total else 1,
            },
        }

    @staticmethod
    async def get_challenge(slug: str):
        doc = await db.problems.find_one({"slug": slug, "is_archived": {"$ne": True}})

        if not doc:
            doc = next((c for c in CHALLENGES if c.get("slug") == slug), None)

        if not doc:
            raise HTTPException(status_code=404, detail="Challenge not found")

        return {"success": True, "data": _to_frontend(_serialize(doc))}

    @staticmethod
    async def create_challenge(payload: dict):

        # Validate through Pydantic model — raises 422 on bad data
        try:
            validated = ChallengeModel(**payload)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        slug = validated.slug or validated.title.lower().replace(" ", "-")

        existing = await db.problems.find_one({"slug": slug})
        if existing:
            raise HTTPException(status_code=409, detail="Slug already exists")

        doc = validated.dict()
        doc["challenge_id"] = str(doc["challenge_id"])
        doc["slug"] = slug

        await db.problems.insert_one(doc)

        return {
            "success": True,
            "message": "Challenge created",
            "data": _to_frontend(_serialize(doc)),
        }

    @staticmethod
    async def update_challenge(slug: str, payload: dict):
        existing = await db.problems.find_one(
            {"slug": slug, "is_archived": {"$ne": True}}
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Challenge not found")

        for field in ("_id", "challenge_id", "created_at"):
            payload.pop(field, None)

        if "domain" in payload:
            payload["domain"] = payload["domain"].lower().replace(" ", "_")
        if "difficulty" in payload:
            payload["difficulty"] = payload["difficulty"].lower()

        new_slug = payload.get("slug", slug)
        if new_slug != slug:
            clash = await db.problems.find_one({"slug": new_slug})
            if clash:
                raise HTTPException(status_code=409, detail="Slug already taken")

        payload["updated_at"] = datetime.utcnow()

        await db.problems.update_one({"slug": slug}, {"$set": payload})
        updated = await db.problems.find_one({"slug": new_slug})

        return {
            "success": True,
            "message": "Challenge updated",
            "data": _to_frontend(_serialize(updated)),
        }

    @staticmethod
    async def delete_challenge(slug: str):
        doc = await db.problems.find_one({"slug": slug})
        if not doc:
            raise HTTPException(status_code=404, detail="Challenge not found")

        await db.problems.update_one(
            {"slug": slug},
            {"$set": {"is_archived": True, "updated_at": datetime.utcnow()}},
        )
        return {"success": True, "message": "Challenge archived"}

    @staticmethod
    async def toggle_featured(slug: str):
        doc = await db.problems.find_one({"slug": slug})
        if not doc:
            raise HTTPException(status_code=404, detail="Challenge not found")

        new_val = not doc.get("is_featured", False)
        await db.problems.update_one(
            {"slug": slug},
            {"$set": {"is_featured": new_val, "updated_at": datetime.utcnow()}},
        )
        return {"success": True, "is_featured": new_val}

    # ── TOGGLE PUBLISH ────────────────────────────────────────────────────────
    @staticmethod
    async def toggle_publish(slug: str):
        doc = await db.problems.find_one({"slug": slug})
        if not doc:
            raise HTTPException(status_code=404, detail="Challenge not found")

        new_val = not doc.get("is_published", True)
        await db.problems.update_one(
            {"slug": slug},
            {"$set": {"is_published": new_val, "updated_at": datetime.utcnow()}},
        )
        return {"success": True, "is_published": new_val}
