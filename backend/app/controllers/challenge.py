from __future__ import annotations

from datetime import datetime
from math import ceil
from typing import Optional

from fastapi import HTTPException

from app.core.db import get_db
from app.data.seed import CHALLENGES, DOMAINS

db = get_db()


def _serialize(doc: dict) -> dict:
    """Strip Mongo _id and normalise field names to match the frontend."""
    doc = dict(doc)
    doc.pop("_id", None)
    return doc


def _to_frontend(doc: dict) -> dict:
    """
    Map DB field names → frontend field names.
    DB may store verbose names (xp_reward, estimated_time_minutes, etc.)
    from the old ChallengeModel. The frontend always expects the short names.
    """
    return {
        "id": doc.get("id") or doc.get("challenge_id", ""),
        "slug": doc.get("slug", ""),
        "title": doc.get("title", ""),
        "domain": doc.get("domain", ""),
        "difficulty": doc.get("difficulty", ""),
        "minutes": doc.get("minutes") or doc.get("estimated_time_minutes", 0),
        "xp": doc.get("xp") or doc.get("xp_reward", 0),
        "completion": doc.get("completion") or doc.get("success_rate", 0),
        "tags": doc.get("tags", []),
        "summary": doc.get("summary") or doc.get("short_description", ""),
        # detail-page extras (optional, safe to be empty)
        "description": doc.get("description", ""),
        "starter_code": doc.get("starter_code", {}),
        "test_cases": doc.get("test_cases", []),
        "hints": doc.get("hints", []),
        "is_featured": doc.get("is_featured", False),
        "is_published": doc.get("is_published", True),
    }


async def _all_from_db() -> list[dict]:
    """Return all non-archived challenges from DB, falling back to seed data."""
    cursor = db.problems.find({"is_archived": {"$ne": True}})
    docs = [_serialize(doc) async for doc in cursor]
    return docs if docs else CHALLENGES


class ChallengeController:
    # ── LIST ──────────────────────────────────────────────────────────────────
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

        # filter
        items = []
        for doc in all_docs:
            c = _to_frontend(doc)

            if domain and domain != "all" and c["domain"] != domain:
                continue
            if difficulty and difficulty != "all" and c["difficulty"] != difficulty:
                continue
            if q:
                haystack = f"{c['title']} {' '.join(c['tags'])} {c['summary']}".lower()
                if q.lower() not in haystack:
                    continue
            items.append(c)

        # sort
        if sort == "xp":
            items.sort(key=lambda c: c["xp"], reverse=True)
        elif sort == "time":
            items.sort(key=lambda c: c["minutes"])
        elif sort == "completion":
            items.sort(key=lambda c: c["completion"], reverse=True)
        # "popular" → natural DB order (insertion order / trending)

        total = len(items)

        # paginate
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
            # fall back to seed
            doc = next((c for c in CHALLENGES if c.get("slug") == slug), None)

        if not doc:
            raise HTTPException(status_code=404, detail="Challenge not found")

        return {"success": True, "data": _to_frontend(_serialize(doc))}

    # ── CREATE ────────────────────────────────────────────────────────────────
    @staticmethod
    async def create_challenge(payload: dict):
        slug = payload.get("slug") or payload["title"].lower().replace(" ", "-")

        existing = await db.problems.find_one({"slug": slug})
        if existing:
            raise HTTPException(status_code=409, detail="Slug already exists")

        now = datetime.utcnow()
        doc = {
            **payload,
            "slug": slug,
            "completion": payload.get("completion", 0),
            "is_archived": False,
            "is_published": payload.get("is_published", True),
            "is_featured": payload.get("is_featured", False),
            "created_at": now,
            "updated_at": now,
        }

        await db.problems.insert_one(doc)
        return {
            "success": True,
            "message": "Challenge created",
            "data": _to_frontend(_serialize(doc)),
        }

    # ── UPDATE ────────────────────────────────────────────────────────────────
    @staticmethod
    async def update_challenge(slug: str, payload: dict):
        existing = await db.problems.find_one(
            {"slug": slug, "is_archived": {"$ne": True}}
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Challenge not found")

        # don't allow overwriting immutable fields
        for field in ("_id", "created_at"):
            payload.pop(field, None)

        # if slug is changing, check it won't collide
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

    # ── DELETE (soft) ─────────────────────────────────────────────────────────
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

    # ── TOGGLE FEATURED ───────────────────────────────────────────────────────
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
