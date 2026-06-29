"""
Settings Controller — Production-ready settings management
All data is server-authoritative; no client-side trust.
"""

from __future__ import annotations

import logging
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

from app.core.db import get_db

logger = logging.getLogger(__name__)
db = get_db()

# Default settings for new users (written to DB on first access)
DEFAULT_SETTINGS = {
    "notifications": {
        "email_challenges": True,
        "email_interviews": True,
        "email_contests": True,
        "email_weekly_digest": True,
        "push_challenges": True,
        "push_interviews": True,
        "push_contests": True,
        "push_achievements": True,
        "push_streak_reminders": True,
        "push_social": True,
    },
    "privacy": {
        "profile_visible": True,
        "show_activity": True,
        "show_heatmap": True,
        "show_badges": True,
        "show_interviews": False,
        "show_email": False,
        "allow_follow": True,
        "searchable": True,
    },
    "preferences": {
        "theme": "dark",
        "editor_font_size": 14,
        "editor_tab_size": 2,
        "preferred_language": "javascript",
        "timezone": "UTC",
        "code_execution_timeout": 10,
    },
}


class SettingsController:

    @staticmethod
    async def get_settings(user: dict) -> dict:
        """Get full user settings from DB. Creates defaults if not found."""
        user_id = user["user_id"]

        settings_doc = await db.user_settings.find_one({"user_id": user_id})
        if not settings_doc:
            # First time — create default settings
            settings_doc = {
                "user_id": user_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                **DEFAULT_SETTINGS,
            }
            await db.user_settings.insert_one(settings_doc)

        settings_doc.pop("_id", None)
        return {"success": True, "settings": settings_doc}

    @staticmethod
    async def update_settings(user: dict, payload: dict) -> dict:
        """Update user settings atomically. Only whitelisted fields are accepted."""
        user_id = user["user_id"]

        # Ensure settings doc exists
        existing = await db.user_settings.find_one({"user_id": user_id})
        if not existing:
            existing = {
                "user_id": user_id,
                "created_at": datetime.utcnow(),
                **DEFAULT_SETTINGS,
            }
            await db.user_settings.insert_one(existing)

        # Build $set update from payload (only whitelisted sections)
        updates = {"updated_at": datetime.utcnow()}
        allowed_sections = {"notifications", "privacy", "preferences"}

        for section in allowed_sections:
            if section in payload and isinstance(payload[section], dict):
                for key, value in payload[section].items():
                    updates[f"{section}.{key}"] = value

        if len(updates) <= 1:
            return {"success": True, "message": "No valid settings to update"}

        await db.user_settings.update_one(
            {"user_id": user_id},
            {"$set": updates},
        )

        return {"success": True, "message": "Settings updated successfully"}

    @staticmethod
    async def get_billing_info(user: dict) -> dict:
        """Get billing/payment info from actual payment records."""
        user_id = user["user_id"]
        user_doc = await db.users.find_one({"user_id": user_id})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch payment orders
        orders_cursor = db.payment_orders.find(
            {"user_id": user_id}
        ).sort("created_at", -1)
        orders = await orders_cursor.to_list(length=50)

        for o in orders:
            o.pop("_id", None)

        # Calculate subscription status
        is_premium = user_doc.get("is_premium", False)
        premium_until = user_doc.get("premium_until")

        # Find the most recent successful payment
        last_payment = None
        for o in orders:
            if o.get("status") == "completed":
                last_payment = o
                break

        return {
            "success": True,
            "billing": {
                "is_premium": is_premium,
                "premium_until": premium_until,
                "plan": user_doc.get("plan", "free"),
                "last_payment": last_payment,
                "payment_history": orders,
                "total_spent": sum(
                    o.get("amount", 0) for o in orders
                    if o.get("status") == "completed"
                ),
            },
        }

    @staticmethod
    async def get_xp_history(user: dict, limit: int = 50) -> dict:
        """Get XP transaction history — every XP earn/spend event."""
        user_id = user["user_id"]

        # Fetch XP transactions
        xp_cursor = db.xp_transactions.find(
            {"user_id": user_id}
        ).sort("created_at", -1)
        transactions = await xp_cursor.to_list(length=limit)

        for t in transactions:
            t.pop("_id", None)

        # If no transaction history exists, compute from submissions
        if not transactions:
            transactions = await _rebuild_xp_history(user_id)

        # Calculate totals
        total_earned = sum(
            t.get("amount", 0) for t in transactions
            if t.get("type") == "earned"
        )
        total_spent = sum(
            abs(t.get("amount", 0)) for t in transactions
            if t.get("type") == "spent"
        )

        user_doc = await db.users.find_one({"user_id": user_id})
        current_xp = user_doc.get("total_xp", 0) if user_doc else 0

        return {
            "success": True,
            "xp": {
                "current": current_xp,
                "total_earned": total_earned,
                "total_spent": total_spent,
                "level": (current_xp // 1000) + 1,
                "xp_in_level": current_xp % 1000,
                "xp_to_next_level": 1000 - (current_xp % 1000),
                "transactions": transactions,
            },
        }

    @staticmethod
    async def get_active_sessions(user: dict) -> dict:
        """Get devices/sessions with login activity."""
        user_id = user["user_id"]

        sessions_cursor = db.user_sessions.find(
            {"user_id": user_id}
        ).sort("last_active", -1)
        sessions = await sessions_cursor.to_list(length=10)

        for s in sessions:
            s.pop("_id", None)

        return {"success": True, "sessions": sessions}

    @staticmethod
    async def delete_account(user: dict) -> dict:
        """Soft-delete user account. Marks as inactive, anonymizes PII."""
        user_id = user["user_id"]

        user_doc = await db.users.find_one({"user_id": user_id})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")

        # Soft delete — mark inactive and anonymize
        await db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_active": False,
                    "is_locked": True,
                    "email": f"deleted_{user_id}@interleet.local",
                    "full_name": "Deleted User",
                    "username": f"deleted_{user_id[:8]}",
                    "avatar": None,
                    "bio": None,
                    "location": None,
                    "github_username": None,
                    "linkedin_url": None,
                    "portfolio_url": None,
                    "website": None,
                    "deleted_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        # Remove settings
        await db.user_settings.delete_one({"user_id": user_id})

        return {
            "success": True,
            "message": "Account has been deactivated. Your data has been anonymized.",
        }


async def _rebuild_xp_history(user_id: str) -> list[dict]:
    """
    Rebuild XP transaction history from submissions and interview reports.
    Used when the xp_transactions collection is empty (migration).
    """
    transactions = []

    # From accepted submissions
    accepted_cursor = db.submissions.find(
        {"user_id": user_id, "status": "accepted"}
    ).sort("created_at", 1)
    accepted = await accepted_cursor.to_list(length=500)

    seen_slugs = set()
    for sub in accepted:
        slug = sub.get("problem_slug")
        if slug and slug not in seen_slugs:
            seen_slugs.add(slug)
            # Look up XP reward for this problem
            problem = await db.problems.find_one({"slug": slug})
            xp_reward = problem.get("xp_reward", 100) if problem else 100

            txn = {
                "id": str(uuid4()),
                "user_id": user_id,
                "type": "earned",
                "amount": xp_reward,
                "source": "challenge",
                "description": f"Solved: {problem.get('title', slug) if problem else slug}",
                "reference_id": slug,
                "created_at": sub.get("created_at", datetime.utcnow()),
            }
            transactions.append(txn)

    # From interview reports
    interview_cursor = db.interview_reports.find(
        {"user_id": user_id}
    ).sort("created_at", 1)
    interviews = await interview_cursor.to_list(length=100)

    for iv in interviews:
        txn = {
            "id": str(uuid4()),
            "user_id": user_id,
            "type": "earned",
            "amount": 50,
            "source": "interview",
            "description": f"Interview: {iv.get('role', 'Mock Interview')}",
            "reference_id": iv.get("session_id"),
            "created_at": iv.get("created_at", datetime.utcnow()),
        }
        transactions.append(txn)

    # From system design completions
    sd_cursor = db.user_system_design_progress.find(
        {"user_id": user_id, "progress": "Completed"}
    ).sort("updated_at", 1)
    sd_list = await sd_cursor.to_list(length=100)

    for sd in sd_list:
        txn = {
            "id": str(uuid4()),
            "user_id": user_id,
            "type": "earned",
            "amount": 100,
            "source": "system_design",
            "description": f"System Design: {sd.get('challenge_id', 'challenge')}",
            "reference_id": sd.get("challenge_id"),
            "created_at": sd.get("updated_at", datetime.utcnow()),
        }
        transactions.append(txn)

    # From store purchases (spent)
    purchases_cursor = db.store_purchases.find(
        {"user_id": user_id}
    ).sort("created_at", 1)
    purchases = await purchases_cursor.to_list(length=100)

    for p in purchases:
        txn = {
            "id": str(uuid4()),
            "user_id": user_id,
            "type": "spent",
            "amount": -abs(p.get("xp_cost", 0)),
            "source": "store",
            "description": f"Purchased: {p.get('item_name', 'Store Item')}",
            "reference_id": p.get("purchase_id"),
            "created_at": p.get("created_at", datetime.utcnow()),
        }
        transactions.append(txn)

    # Sort by date and bulk-insert for future queries
    transactions.sort(key=lambda t: t.get("created_at", datetime.min))

    if transactions:
        await db.xp_transactions.insert_many(transactions)

    return transactions
