"""
Notification Service — Proactive engagement notifications
Generates meaningful notifications: streak warnings, challenge suggestions,
achievement unlocks, weekly recaps, and more.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from uuid import uuid4

from app.core.db import get_db

logger = logging.getLogger(__name__)
db = get_db()


class NotificationService:
    """Handles creation, delivery, and management of user notifications."""

    @staticmethod
    async def create(
        user_id: str,
        title: str,
        message: str,
        *,
        type: str = "system",
        priority: str = "medium",
        icon: str = "bell",
        link: str | None = None,
        action_label: str | None = None,
        category: str = "general",
        expires_at: datetime | None = None,
        **kwargs,
    ) -> dict:
        """Create a single notification for a user."""
        notification = {
            "id": str(uuid4()),
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": type,
            "priority": priority,
            "icon": icon,
            "link": link,
            "action_label": action_label,
            "category": category,
            "read": False,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "dedup_key": kwargs.get("dedup_key"),
        }

        await db.notifications.insert_one(notification)
        return notification

    @staticmethod
    async def get_unread_count(user_id: str) -> int:
        """Get count of unread notifications."""
        return await db.notifications.count_documents({
            "user_id": user_id,
            "read": False,
            "$or": [
                {"expires_at": None},
                {"expires_at": {"$gt": datetime.utcnow()}},
            ],
        })

    @staticmethod
    async def _already_notified(user_id: str, dedup_key: str) -> bool:
        """Return True if a notification with this dedup_key already exists for this user."""
        existing = await db.notifications.find_one({
            "user_id": user_id,
            "dedup_key": dedup_key,
        })
        return existing is not None

    @staticmethod
    async def on_badge_earned(user_id: str, badge: dict) -> None:
        """Notify user when a badge is earned (once per badge, ever)."""
        dedup_key = f"badge:{badge['id']}"
        if await NotificationService._already_notified(user_id, dedup_key):
            return  # Already sent this badge notification — skip
        await NotificationService.create(
            user_id,
            title="🏆 Badge Unlocked!",
            message=f"You earned the \"{badge['name']}\" badge! +{badge.get('xp_reward', 0)} XP",
            type="achievement",
            priority="high",
            icon="trophy",
            link="/app/profile",
            action_label="View Badge",
            category="achievement",
            dedup_key=dedup_key,
        )

    @staticmethod
    async def on_submission_accepted(
        user_id: str, challenge_title: str, xp_earned: int, problem_slug: str = ""
    ) -> None:
        """Notify user when a challenge submission is accepted (once per problem)."""
        dedup_key = f"solved:{problem_slug}" if problem_slug else None
        if dedup_key and await NotificationService._already_notified(user_id, dedup_key):
            return  # Already notified for this challenge
        await NotificationService.create(
            user_id,
            title="✅ Challenge Solved!",
            message=f"Great job! You solved \"{challenge_title}\". +{xp_earned} XP earned.",
            type="challenge",
            priority="medium",
            icon="check-circle",
            link="/app/challenges",
            action_label="Continue Practicing",
            category="challenge",
            dedup_key=dedup_key,
        )

    @staticmethod
    async def on_interview_completed(
        user_id: str, role: str, score: float, session_id: str = ""
    ) -> None:
        """Notify user when an interview report is generated (once per session)."""
        dedup_key = f"interview:{session_id}" if session_id else None
        if dedup_key and await NotificationService._already_notified(user_id, dedup_key):
            return
        await NotificationService.create(
            user_id,
            title="🎤 Interview Complete!",
            message=f"Your \"{role}\" interview scored {score:.1f}/10. Check your report.",
            type="interview",
            priority="medium",
            icon="mic",
            link="/app/interviews",
            action_label="View Report",
            category="interview",
            dedup_key=dedup_key,
        )

    @staticmethod
    async def generate_daily_notifications(user_id: str) -> list[dict]:
        """
        Generate personalized daily notifications based on user activity patterns.
        Called by the daily scheduler.
        """
        user_doc = await db.users.find_one({"user_id": user_id})
        if not user_doc:
            return []

        notifications_created = []
        now = datetime.utcnow()
        today_str = now.strftime("%Y-%m-%d")

        # Check if we already generated today's notifications
        existing = await db.notifications.find_one({
            "user_id": user_id,
            "category": "daily",
            "created_at": {"$gte": datetime(now.year, now.month, now.day)},
        })
        if existing:
            return []  # Already generated today

        # ── 1. Streak at risk ───────────────────────────────────────────
        streak = user_doc.get("streak_count", 0)
        if streak >= 2:
            # Check if user has submitted anything today
            today_start = datetime(now.year, now.month, now.day)
            today_subs = await db.submissions.count_documents({
                "user_id": user_id,
                "created_at": {"$gte": today_start},
            })
            if today_subs == 0:
                n = await NotificationService.create(
                    user_id,
                    title="🔥 Streak at Risk!",
                    message=f"Your {streak}-day streak is at risk! Solve a challenge today to keep it alive.",
                    type="streak",
                    priority="high",
                    icon="flame",
                    link="/app/challenges",
                    action_label="Solve Now",
                    category="daily",
                    expires_at=now + timedelta(hours=24),
                )
                notifications_created.append(n)

        # ── 2. Weak domain suggestion ─────────────────────────────────
        accepted_cursor = db.submissions.find(
            {"user_id": user_id, "status": "accepted"}
        )
        accepted_subs = await accepted_cursor.to_list(length=500)
        solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}

        if solved_slugs:
            problems_cursor = db.problems.find({"slug": {"$in": list(solved_slugs)}})
            solved_problems = await problems_cursor.to_list(length=500)
            domain_counts = {}
            for p in solved_problems:
                d = p.get("domain", "Backend")
                domain_counts[d] = domain_counts.get(d, 0) + 1

            all_domains = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]
            weak_domain = min(all_domains, key=lambda d: domain_counts.get(d, 0))
            weak_count = domain_counts.get(weak_domain, 0)

            # Find an unsolved challenge in that domain
            unsolved_challenge = await db.problems.find_one({
                "domain": weak_domain,
                "slug": {"$nin": list(solved_slugs)},
            })

            if unsolved_challenge and weak_count < 3:
                n = await NotificationService.create(
                    user_id,
                    title=f"💡 Try {weak_domain}",
                    message=f"Your {weak_domain} skills could use a boost. Try \"{unsolved_challenge.get('title', 'a challenge')}\".",
                    type="suggestion",
                    priority="low",
                    icon="lightbulb",
                    link=f"/app/editor/{unsolved_challenge.get('slug', '')}",
                    action_label="Start Challenge",
                    category="daily",
                    expires_at=now + timedelta(days=2),
                )
                notifications_created.append(n)

        # ── 3. Badge proximity ────────────────────────────────────────
        from app.services.badge_service import BadgeService
        badge_progress = await BadgeService.get_badge_progress(user_id)
        closest_badges = [
            b for b in badge_progress.get("locked", [])
            if 60 <= b.get("progress", 0) < 100
        ][:1]  # Only notify about the closest one

        for b in closest_badges:
            n = await NotificationService.create(
                user_id,
                title=f"🎯 Almost there!",
                message=f"You're {b['progress']:.0f}% toward the \"{b['name']}\" badge. Keep going!",
                type="badge_progress",
                priority="low",
                icon="target",
                link="/app/profile",
                action_label="View Progress",
                category="daily",
                expires_at=now + timedelta(days=3),
            )
            notifications_created.append(n)

        return notifications_created

    @staticmethod
    async def generate_weekly_recap(user_id: str) -> dict | None:
        """Generate a weekly recap notification for the user."""
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        # Count this week's activity
        subs_count = await db.submissions.count_documents({
            "user_id": user_id,
            "status": "accepted",
            "created_at": {"$gte": week_ago},
        })
        interviews_count = await db.interview_reports.count_documents({
            "user_id": user_id,
            "created_at": {"$gte": week_ago},
        })

        if subs_count == 0 and interviews_count == 0:
            # No activity — send a "come back" notification
            return await NotificationService.create(
                user_id,
                title="📊 Weekly Recap",
                message="You were quiet this week. Jump back in and solve a challenge!",
                type="recap",
                priority="low",
                icon="bar-chart",
                link="/app/challenges",
                action_label="Practice Now",
                category="weekly",
                expires_at=now + timedelta(days=7),
            )

        return await NotificationService.create(
            user_id,
            title="📊 Weekly Recap",
            message=f"This week: {subs_count} challenges solved, {interviews_count} interviews completed. Keep the momentum!",
            type="recap",
            priority="medium",
            icon="bar-chart",
            link="/app/dashboard",
            action_label="View Dashboard",
            category="weekly",
            expires_at=now + timedelta(days=7),
        )
