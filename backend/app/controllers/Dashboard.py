from fastapi import HTTPException
from datetime import datetime, timedelta

from app.core.db import get_db

db = get_db()


class DashboardController:
    @staticmethod
    async def get_dashboard(user: dict):
        try:
            db_user = await db.users.find_one({"user_id": user["user_id"]})

            if not db_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found",
                )

            stats = {
                "xp": db_user.get("overall_rating", 0),
                "frontend_rating": db_user.get("frontend_rating", 0),
                "backend_rating": db_user.get("backend_rating", 0),
                "fullstack_rating": db_user.get("fullstack_rating", 0),
                "devops_rating": db_user.get("devops_rating", 0),
                "streak_count": db_user.get("streak_count", 0),
            }

            domain_strengths = [
                {
                    "domain": "Frontend",
                    "score": db_user.get("frontend_rating", 0),
                },
                {
                    "domain": "Backend",
                    "score": db_user.get("backend_rating", 0),
                },
                {
                    "domain": "Fullstack",
                    "score": db_user.get("fullstack_rating", 0),
                },
                {
                    "domain": "DevOps",
                    "score": db_user.get("devops_rating", 0),
                },
            ]

            weekly_activity = [
                {"day": "Mon", "solved": 2},
                {"day": "Tue", "solved": 5},
                {"day": "Wed", "solved": 1},
                {"day": "Thu", "solved": 6},
                {"day": "Fri", "solved": 4},
                {"day": "Sat", "solved": 7},
                {"day": "Sun", "solved": 3},
            ]

            recent_activity = [
                {
                    "text": "Solved Postgres Indexing Strategy",
                    "domain": "Databases",
                    "when": "2h ago",
                },
                {
                    "text": "Completed AI Interview — Senior Backend",
                    "domain": "Backend",
                    "when": "1d ago",
                },
                {
                    "text": "Earned 100-Day Streak badge",
                    "domain": "-",
                    "when": "2d ago",
                },
                {
                    "text": "Placed #18 in Weekly Engineering Cup",
                    "domain": "System Design",
                    "when": "4d ago",
                },
            ]

            interview_trend = [
                {"week": "W1", "score": 62},
                {"week": "W2", "score": 65},
                {"week": "W3", "score": 71},
                {"week": "W4", "score": 70},
                {"week": "W5", "score": 76},
                {"week": "W6", "score": 78},
                {"week": "W7", "score": 81},
                {"week": "W8", "score": 84},
            ]

            badges = db_user.get("badges", [])

            return {
                "success": True,
                "dashboard": {
                    "profile": {
                        "full_name": db_user.get("full_name"),
                        "username": db_user.get("username"),
                        "avatar": db_user.get("avatar"),
                        "email": db_user.get("email"),
                    },
                    "stats": stats,
                    "domain_strengths": domain_strengths,
                    "weekly_activity": weekly_activity,
                    "recent_activity": recent_activity,
                    "interview_trend": interview_trend,
                    "badges": badges,
                },
            }

        except HTTPException:
            raise

        except Exception as e:
            print("DASHBOARD ERROR =", repr(e))

            raise HTTPException(
                status_code=500,
                detail="Failed to fetch dashboard",
            )
