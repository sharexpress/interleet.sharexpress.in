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

            seven_days_ago = datetime.utcnow() - timedelta(days=7)

            activity_pipeline = [
                {
                    "$match": {
                        "user_id": user["user_id"],
                        "created_at": {"$gte": seven_days_ago},
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {"format": "%a", "date": "$created_at"}
                        },
                        "solved": {
                            "$sum": {
                                "$cond": [{"$eq": ["$type", "challenge_solved"]}, 1, 0]
                            }
                        },
                        "minutes_practiced": {"$sum": "$metadata.duration_minutes"},
                    }
                },
            ]

            activity_result = await db.user_activity.aggregate(
                activity_pipeline
            ).to_list(length=7)

            activity_map = {item["_id"]: item for item in activity_result}

            ordered_days = [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
            ]

            weekly_activity = []

            for day in ordered_days:
                item = activity_map.get(day)

                weekly_activity.append(
                    {
                        "day": day,
                        "solved": item["solved"] if item else 0,
                        "minutes_practiced": (item["minutes_practiced"] if item else 0),
                    }
                )

            # =====================================================
            # DOMAIN STRENGTHS
            # =====================================================

            domain_strengths = [
                {
                    "domain": "Frontend",
                    "score": db_user.get(
                        "frontend_rating",
                        0,
                    ),
                },
                {
                    "domain": "Backend",
                    "score": db_user.get(
                        "backend_rating",
                        0,
                    ),
                },
                {
                    "domain": "Fullstack",
                    "score": db_user.get(
                        "fullstack_rating",
                        0,
                    ),
                },
                {
                    "domain": "DevOps",
                    "score": db_user.get(
                        "devops_rating",
                        0,
                    ),
                },
            ]

            # =====================================================
            # RECENT ACTIVITY
            # =====================================================

            recent_activity_cursor = (
                db.user_activity.find({"user_id": user["user_id"]})
                .sort("created_at", -1)
                .limit(5)
            )

            recent_activity_db = await recent_activity_cursor.to_list(length=5)

            recent_activity = []

            for activity in recent_activity_db:
                recent_activity.append(
                    {
                        "text": activity.get("title"),
                        "domain": activity.get("domain"),
                        "when": activity.get("created_at"),
                    }
                )

            # =====================================================
            # INTERVIEW TREND
            # =====================================================

            interview_cursor = (
                db.interview_sessions.find(
                    {
                        "user_id": user["user_id"],
                        "status": "completed",
                    }
                )
                .sort("completed_at", -1)
                .limit(8)
            )

            interviews = await interview_cursor.to_list(length=8)

            interviews.reverse()

            interview_trend = []

            for index, interview in enumerate(interviews):
                interview_trend.append(
                    {
                        "week": f"W{index + 1}",
                        "score": interview.get(
                            "overall_score",
                            0,
                        ),
                    }
                )

            # =====================================================
            # RECOMMENDED CHALLENGES
            # =====================================================

            weakest_domain = min(
                [
                    (
                        "frontend",
                        db_user.get(
                            "frontend_rating",
                            0,
                        ),
                    ),
                    (
                        "backend",
                        db_user.get(
                            "backend_rating",
                            0,
                        ),
                    ),
                    (
                        "fullstack",
                        db_user.get(
                            "fullstack_rating",
                            0,
                        ),
                    ),
                    (
                        "devops",
                        db_user.get(
                            "devops_rating",
                            0,
                        ),
                    ),
                ],
                key=lambda x: x[1],
            )[0]

            recommended_cursor = db.challenges.find(
                {
                    "domain": weakest_domain,
                    "is_published": True,
                }
            ).limit(4)

            recommended_db = await recommended_cursor.to_list(length=4)

            recommended_challenges = []

            for challenge in recommended_db:
                recommended_challenges.append(
                    {
                        "challenge_id": str(challenge["challenge_id"]),
                        "title": challenge["title"],
                        "domain": challenge["domain"],
                        "difficulty": challenge["difficulty"],
                        "xp_reward": challenge.get(
                            "xp_reward",
                            0,
                        ),
                        "estimated_time_minutes": challenge.get(
                            "estimated_time_minutes",
                            0,
                        ),
                        "success_rate": challenge.get(
                            "success_rate",
                            0,
                        ),
                        "tags": challenge.get(
                            "tags",
                            [],
                        ),
                    }
                )

            # =====================================================
            # DASHBOARD RESPONSE
            # =====================================================

            return {
                "success": True,
                "dashboard": {
                    "profile": {
                        "full_name": db_user.get("full_name"),
                        "username": db_user.get("username"),
                        "avatar": db_user.get("avatar"),
                        "email": db_user.get("email"),
                    },
                    "stats": {
                        "total_xp": db_user.get(
                            "total_xp",
                            0,
                        ),
                        "weekly_xp": db_user.get(
                            "weekly_xp",
                            0,
                        ),
                        "streak_count": db_user.get(
                            "streak_count",
                            0,
                        ),
                        "global_rank": db_user.get(
                            "global_rank",
                            0,
                        ),
                        "frontend_rating": db_user.get(
                            "frontend_rating",
                            0,
                        ),
                        "backend_rating": db_user.get(
                            "backend_rating",
                            0,
                        ),
                        "fullstack_rating": db_user.get(
                            "fullstack_rating",
                            0,
                        ),
                        "devops_rating": db_user.get(
                            "devops_rating",
                            0,
                        ),
                        "overall_rating": db_user.get(
                            "overall_rating",
                            0,
                        ),
                        "success_rate": db_user.get(
                            "success_rate",
                            0,
                        ),
                    },
                    "weekly_activity": weekly_activity,
                    "domain_strengths": domain_strengths,
                    "recent_activity": recent_activity,
                    "interview_trend": interview_trend,
                    "recommended_challenges": recommended_challenges,
                    "badges": db_user.get(
                        "badges",
                        [],
                    ),
                },
            }

        except HTTPException:
            raise

        except Exception as e:
            print(
                "DASHBOARD ERROR =",
                repr(e),
            )

            raise HTTPException(
                status_code=500,
                detail="Failed to fetch dashboard",
            )
