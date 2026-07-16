"""
Badge Catalog & Service — Gamified achievement system
Full badge definitions with rarity tiers, unlock criteria, and progress tracking.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from app.core.db import get_db

logger = logging.getLogger(__name__)
db = get_db()


# ═══════════════════════════════════════════════════════════════════════════════
# Badge Catalog — All available badges with their unlock criteria
# ═══════════════════════════════════════════════════════════════════════════════

BADGE_CATALOG = [
    # ── Milestone Badges ───────────────────────────────────────────────────
    {
        "id": "first_solve",
        "name": "First Blood",
        "description": "Solve your very first coding challenge",
        "icon": "🎯",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_first_blood.png",
        "rarity": "Common",
        "category": "Milestone",
        "tier": "Bronze",
        "xp_reward": 50,
        "criteria": {"type": "challenges_solved", "count": 1},
    },
    {
        "id": "five_solves",
        "name": "Problem Slayer",
        "description": "Solve 5 coding challenges",
        "icon": "⚔️",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_problem_slayer.png",
        "rarity": "Common",
        "category": "Milestone",
        "tier": "Bronze",
        "xp_reward": 100,
        "criteria": {"type": "challenges_solved", "count": 5},
    },
    {
        "id": "ten_solves",
        "name": "Algorithm Master",
        "description": "Solve 10 coding challenges",
        "icon": "🧠",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_algorithm_master.png",
        "rarity": "Rare",
        "category": "Milestone",
        "tier": "Silver",
        "xp_reward": 200,
        "criteria": {"type": "challenges_solved", "count": 10},
    },
    {
        "id": "twenty_five_solves",
        "name": "Code Warrior",
        "description": "Solve 25 coding challenges",
        "icon": "⚡",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_gold.png",
        "rarity": "Epic",
        "category": "Milestone",
        "tier": "Gold",
        "xp_reward": 500,
        "criteria": {"type": "challenges_solved", "count": 25},
    },
    {
        "id": "fifty_solves",
        "name": "Legend of the Arena",
        "description": "Solve 50 coding challenges",
        "icon": "🏆",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_diamond.png",
        "rarity": "Legendary",
        "category": "Milestone",
        "tier": "Platinum",
        "xp_reward": 1000,
        "criteria": {"type": "challenges_solved", "count": 50},
    },

    # ── Domain Badges ─────────────────────────────────────────────────────
    {
        "id": "backend_specialist",
        "name": "Backend Specialist",
        "description": "Solve 5 Backend challenges",
        "icon": "🔧",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Domain",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "domain_solved", "domain": "Backend", "count": 5},
    },
    {
        "id": "frontend_specialist",
        "name": "Frontend Specialist",
        "description": "Solve 5 Frontend challenges",
        "icon": "🎨",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Domain",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "domain_solved", "domain": "Frontend", "count": 5},
    },
    {
        "id": "devops_specialist",
        "name": "DevOps Specialist",
        "description": "Solve 5 DevOps challenges",
        "icon": "🚀",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Domain",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "domain_solved", "domain": "DevOps", "count": 5},
    },
    {
        "id": "api_architect",
        "name": "API Architect",
        "description": "Solve 5 APIs challenges",
        "icon": "🔌",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Domain",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "domain_solved", "domain": "APIs", "count": 5},
    },
    {
        "id": "database_guru",
        "name": "Database Guru",
        "description": "Solve 5 Database challenges",
        "icon": "💾",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Domain",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "domain_solved", "domain": "Databases", "count": 5},
    },
    {
        "id": "fullstack_wizard",
        "name": "Fullstack Wizard",
        "description": "Solve challenges in 3+ different domains",
        "icon": "🧙",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_fullstack_wizard.png",
        "rarity": "Epic",
        "category": "Domain",
        "tier": "Gold",
        "xp_reward": 300,
        "criteria": {"type": "domains_count", "count": 3},
    },
    {
        "id": "system_designer",
        "name": "System Architect",
        "description": "Complete a system design challenge",
        "icon": "🏗️",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_system_architect.png",
        "rarity": "Rare",
        "category": "Domain",
        "tier": "Silver",
        "xp_reward": 200,
        "criteria": {"type": "system_design_completed", "count": 1},
    },

    # ── Streak Badges ─────────────────────────────────────────────────────
    {
        "id": "streak_3",
        "name": "On Fire",
        "description": "Maintain a 3-day activity streak",
        "icon": "🔥",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_on_fire.png",
        "rarity": "Common",
        "category": "Streak",
        "tier": "Bronze",
        "xp_reward": 50,
        "criteria": {"type": "streak", "count": 3},
    },
    {
        "id": "streak_7",
        "name": "Week Warrior",
        "description": "Maintain a 7-day activity streak",
        "icon": "💪",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_week_warrior.png",
        "rarity": "Rare",
        "category": "Streak",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "streak", "count": 7},
    },
    {
        "id": "streak_30",
        "name": "Iron Will",
        "description": "Maintain a 30-day activity streak",
        "icon": "🏅",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_gold.png",
        "rarity": "Epic",
        "category": "Streak",
        "tier": "Gold",
        "xp_reward": 500,
        "criteria": {"type": "streak", "count": 30},
    },
    {
        "id": "streak_100",
        "name": "Centurion",
        "description": "Maintain a 100-day activity streak",
        "icon": "👑",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_centurion.png",
        "rarity": "Legendary",
        "category": "Streak",
        "tier": "Diamond",
        "xp_reward": 2000,
        "criteria": {"type": "streak", "count": 100},
    },

    # ── Interview Badges ───────────────────────────────────────────────────
    {
        "id": "first_interview",
        "name": "Interview Scholar",
        "description": "Complete your first AI mock interview",
        "icon": "🎓",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_bronze.png",
        "rarity": "Common",
        "category": "Interview",
        "tier": "Bronze",
        "xp_reward": 75,
        "criteria": {"type": "interviews_completed", "count": 1},
    },
    {
        "id": "five_interviews",
        "name": "Interview Veteran",
        "description": "Complete 5 AI mock interviews",
        "icon": "🎤",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Interview",
        "tier": "Silver",
        "xp_reward": 200,
        "criteria": {"type": "interviews_completed", "count": 5},
    },
    {
        "id": "ace_interview",
        "name": "Interview Ace",
        "description": "Score 9+ on a mock interview",
        "icon": "💎",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_gold.png",
        "rarity": "Epic",
        "category": "Interview",
        "tier": "Gold",
        "xp_reward": 400,
        "criteria": {"type": "interview_score", "min_score": 9},
    },

    # ── Social Badges ──────────────────────────────────────────────────────
    {
        "id": "first_follower",
        "name": "Rising Star",
        "description": "Get your first follower",
        "icon": "⭐",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_bronze.png",
        "rarity": "Common",
        "category": "Social",
        "tier": "Bronze",
        "xp_reward": 25,
        "criteria": {"type": "followers", "count": 1},
    },
    {
        "id": "ten_followers",
        "name": "Community Builder",
        "description": "Reach 10 followers",
        "icon": "🌟",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_silver.png",
        "rarity": "Rare",
        "category": "Social",
        "tier": "Silver",
        "xp_reward": 150,
        "criteria": {"type": "followers", "count": 10},
    },

    # ── Contest Badges ─────────────────────────────────────────────────────
    {
        "id": "first_contest",
        "name": "Arena Fighter",
        "description": "Participate in your first contest",
        "icon": "🥊",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_bronze.png",
        "rarity": "Common",
        "category": "Contest",
        "tier": "Bronze",
        "xp_reward": 50,
        "criteria": {"type": "contests_participated", "count": 1},
    },
    {
        "id": "contest_winner",
        "name": "Champion",
        "description": "Win a coding contest (1st place)",
        "icon": "🏆",
        "image_url": "https://drive.sharexpress.in/interleet/badges/badge_champion.png",
        "rarity": "Legendary",
        "category": "Contest",
        "tier": "Diamond",
        "xp_reward": 1000,
        "criteria": {"type": "contest_wins", "count": 1},
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Badge Service — Check, award, and track badge progress
# ═══════════════════════════════════════════════════════════════════════════════

class BadgeService:

    @staticmethod
    async def check_and_award_badges(user_id: str) -> list[dict]:
        """
        Check all badge criteria against user stats and award any newly-earned badges.
        Returns list of newly awarded badges (for notification triggering).
        """
        user_doc = await db.users.find_one({"user_id": user_id})
        if not user_doc:
            return []

        # Gather all user stats needed for badge evaluation
        stats = await _gather_user_stats(user_id, user_doc)

        # Get already-earned badge IDs
        earned_badges = user_doc.get("badges", [])
        earned_ids = set()
        for b in earned_badges:
            if isinstance(b, dict):
                earned_ids.add(b.get("badge_id"))
            elif isinstance(b, str):
                earned_ids.add(b)

        newly_awarded = []

        for badge_def in BADGE_CATALOG:
            badge_id = badge_def["id"]
            if badge_id in earned_ids:
                continue  # Already earned

            if _check_criteria(badge_def["criteria"], stats):
                # Award the badge
                badge_entry = {
                    "badge_id": badge_id,
                    "earned_at": datetime.utcnow(),
                }

                await db.users.update_one(
                    {"user_id": user_id},
                    {
                        "$push": {"badges": badge_entry},
                        "$inc": {"total_xp": badge_def.get("xp_reward", 0)},
                    },
                )

                # Log XP transaction
                await db.xp_transactions.insert_one({
                    "id": str(uuid4()),
                    "user_id": user_id,
                    "type": "earned",
                    "amount": badge_def.get("xp_reward", 0),
                    "source": "badge",
                    "description": f"Badge unlocked: {badge_def['name']}",
                    "reference_id": badge_id,
                    "created_at": datetime.utcnow(),
                })

                newly_awarded.append(badge_def)
                logger.info(
                    "Badge awarded: %s → user %s (+%d XP)",
                    badge_def["name"], user_id, badge_def.get("xp_reward", 0),
                )

        return newly_awarded

    @staticmethod
    async def get_badge_progress(user_id: str) -> dict:
        """
        Get progress toward all badges. Returns earned + locked with progress %.
        """
        user_doc = await db.users.find_one({"user_id": user_id})
        if not user_doc:
            return {"earned": [], "locked": [], "total": len(BADGE_CATALOG)}

        stats = await _gather_user_stats(user_id, user_doc)

        earned_badges = user_doc.get("badges", [])
        earned_map = {}
        for b in earned_badges:
            if isinstance(b, dict):
                earned_map[b.get("badge_id")] = b.get("earned_at")
            elif isinstance(b, str):
                earned_map[b] = None

        earned = []
        locked = []

        for badge_def in BADGE_CATALOG:
            badge_id = badge_def["id"]
            badge_info = {
                "id": badge_id,
                "name": badge_def["name"],
                "description": badge_def["description"],
                "icon": badge_def["icon"],
                "image_url": badge_def.get("image_url"),
                "rarity": badge_def["rarity"],
                "category": badge_def["category"],
                "tier": badge_def["tier"],
                "xp_reward": badge_def.get("xp_reward", 0),
            }

            if badge_id in earned_map:
                badge_info["earned"] = True
                badge_info["earned_at"] = earned_map[badge_id]
                earned.append(badge_info)
            else:
                progress = _compute_progress(badge_def["criteria"], stats)
                badge_info["earned"] = False
                badge_info["progress"] = progress
                locked.append(badge_info)

        # Sort locked by progress (closest to unlock first)
        locked.sort(key=lambda b: b.get("progress", 0), reverse=True)

        return {
            "earned": earned,
            "locked": locked,
            "total": len(BADGE_CATALOG),
            "earned_count": len(earned),
        }

    @staticmethod
    async def get_earned_badges(user_id: str) -> list[dict]:
        """Get all earned badges with full metadata."""
        user_doc = await db.users.find_one({"user_id": user_id})
        if not user_doc:
            return []

        earned_badges = user_doc.get("badges", [])
        result = []

        for b in earned_badges:
            badge_id = b.get("badge_id") if isinstance(b, dict) else b
            earned_at = b.get("earned_at") if isinstance(b, dict) else None

            # Find badge definition
            badge_def = next(
                (bd for bd in BADGE_CATALOG if bd["id"] == badge_id),
                None,
            )

            if badge_def:
                result.append({
                    **badge_def,
                    "earned": True,
                    "earned_at": earned_at,
                })
            else:
                # Legacy string badge — create a basic entry
                result.append({
                    "id": badge_id,
                    "name": badge_id,
                    "description": "",
                    "icon": "🏅",
                    "rarity": "Common",
                    "category": "Legacy",
                    "tier": "Bronze",
                    "earned": True,
                    "earned_at": earned_at,
                })

        return result


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

async def _gather_user_stats(user_id: str, user_doc: dict) -> dict[str, Any]:
    """Gather all stats needed for badge criteria evaluation."""

    # Challenges solved (total + per domain)
    accepted_cursor = db.submissions.find(
        {"user_id": user_id, "status": "accepted"}
    )
    accepted_subs = await accepted_cursor.to_list(length=1000)
    solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}

    # Per-domain counts
    domain_counts: dict[str, int] = {}
    if solved_slugs:
        problems_cursor = db.problems.find({"slug": {"$in": list(solved_slugs)}})
        problems = await problems_cursor.to_list(length=1000)
        for p in problems:
            d = p.get("domain", "Backend")
            domain_counts[d] = domain_counts.get(d, 0) + 1

    # Interviews
    interviews_count = await db.interview_reports.count_documents(
        {"user_id": user_id}
    )

    # Best interview score
    best_score = 0
    if interviews_count > 0:
        interview_cursor = db.interview_reports.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(20)
        interviews = await interview_cursor.to_list(length=20)
        for iv in interviews:
            rep = iv.get("report", {})
            score = rep.get("average_score") or rep.get("overall_score") or 0
            best_score = max(best_score, float(score))

    # System design completed
    sd_completed = await db.user_system_design_progress.count_documents(
        {"user_id": user_id, "progress": "Completed"}
    )

    # Followers
    followers = len(user_doc.get("followers", []))

    # Contests
    contests_participated = user_doc.get("total_contests_participated", 0)
    contest_wins = user_doc.get("contest_wins", 0)

    # Streak
    streak = user_doc.get("streak_count", 0)

    return {
        "challenges_solved": len(solved_slugs),
        "domain_counts": domain_counts,
        "domains_count": len(domain_counts),
        "interviews_completed": interviews_count,
        "best_interview_score": best_score,
        "system_design_completed": sd_completed,
        "streak": streak,
        "followers": followers,
        "contests_participated": contests_participated,
        "contest_wins": contest_wins,
    }


def _check_criteria(criteria: dict, stats: dict) -> bool:
    """Check if a badge's criteria is met given user stats."""
    ctype = criteria.get("type")

    if ctype == "challenges_solved":
        return stats["challenges_solved"] >= criteria["count"]

    if ctype == "domain_solved":
        domain = criteria["domain"]
        return stats["domain_counts"].get(domain, 0) >= criteria["count"]

    if ctype == "domains_count":
        return stats["domains_count"] >= criteria["count"]

    if ctype == "streak":
        return stats["streak"] >= criteria["count"]

    if ctype == "interviews_completed":
        return stats["interviews_completed"] >= criteria["count"]

    if ctype == "interview_score":
        return stats["best_interview_score"] >= criteria["min_score"]

    if ctype == "system_design_completed":
        return stats["system_design_completed"] >= criteria["count"]

    if ctype == "followers":
        return stats["followers"] >= criteria["count"]

    if ctype == "contests_participated":
        return stats["contests_participated"] >= criteria["count"]

    if ctype == "contest_wins":
        return stats["contest_wins"] >= criteria["count"]

    return False


def _compute_progress(criteria: dict, stats: dict) -> float:
    """Compute progress percentage (0-100) toward a badge."""
    ctype = criteria.get("type")
    required = criteria.get("count", 1)

    if required == 0:
        return 100.0

    current = 0

    if ctype == "challenges_solved":
        current = stats["challenges_solved"]
    elif ctype == "domain_solved":
        current = stats["domain_counts"].get(criteria.get("domain", ""), 0)
    elif ctype == "domains_count":
        current = stats["domains_count"]
    elif ctype == "streak":
        current = stats["streak"]
    elif ctype == "interviews_completed":
        current = stats["interviews_completed"]
    elif ctype == "interview_score":
        required = criteria.get("min_score", 10)
        current = stats["best_interview_score"]
    elif ctype == "system_design_completed":
        current = stats["system_design_completed"]
    elif ctype == "followers":
        current = stats["followers"]
    elif ctype == "contests_participated":
        current = stats["contests_participated"]
    elif ctype == "contest_wins":
        current = stats["contest_wins"]

    return min(100.0, round((current / required) * 100, 1))
