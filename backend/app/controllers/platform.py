from __future__ import annotations

from datetime import datetime, timedelta
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

def format_relative_time(dt: datetime) -> str:
    if not dt:
        return "Not attempted"
    now = datetime.utcnow()
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    diff = now - dt
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return "Just now"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)}m ago"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)}h ago"
    days = hours / 24
    if days < 7:
        if int(days) == 1:
            return "Yesterday"
        return f"{int(days)} days ago"
    weeks = days / 7
    if weeks < 4:
        if int(weeks) == 1:
            return "1 week ago"
        return f"{int(weeks)} weeks ago"
    months = days / 30
    if months < 12:
        if int(months) == 1:
            return "1 month ago"
        return f"{int(months)} months ago"
    years = days / 365
    if int(years) == 1:
        return "1 year ago"
    return f"{int(years)} years ago"


class PlatformController:
    @staticmethod
    async def dashboard(username: str | None = None):
        user_doc = None
        if username:
            user_doc = await db.users.find_one({"username": username})
        
        if not user_doc:
            user_doc = await db.users.find_one({})
            
        if not user_doc:
            # No fallback to mock — return zero/empty for production
            return {
                "user": {
                    "name": "New User",
                    "username": "",
                    "email": "",
                    "avatar": None,
                    "location": "",
                    "rating": 1000,
                    "rank": 0,
                    "xp": 0,
                    "streak": 0,
                    "solved": 0,
                    "interviews": 0,
                    "domains": [],
                    "badges": [],
                    "heatmap": {},
                    "frontend_rating": 0,
                    "backend_rating": 0,
                    "fullstack_rating": 0,
                    "devops_rating": 0,
                    "overall_rating": 1000,
                    "streak_count": 0,
                },
                "activityWeekly": [],
                "recentActivity": [],
                "recommendedChallenges": [],
                "interviewTrend": [],
                "badgeProgress": {"earned": [], "locked": [], "total": 0, "earned_count": 0},
                "quests": [],
            }

        user_id = user_doc["user_id"]
        
        # 1. Fetch user's submissions
        submissions_cursor = db.submissions.find({"user_id": user_id})
        submissions = await submissions_cursor.to_list(length=1000)
        
        # Filter accepted submissions
        accepted_subs = [s for s in submissions if s.get("status") == "accepted"]
        solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}
        
        # 2. Fetch all challenges from problems collection
        problems_cursor = db.problems.find({})
        all_problems = [_serialize(p) for p in await problems_cursor.to_list(length=1000)]
        problems_by_slug = {p["slug"]: p for p in all_problems}
        
        # 3. Calculate solved count and XP
        solved_count = len(solved_slugs)
        base_xp = sum(problems_by_slug[slug].get("xp_reward", 100) for slug in solved_slugs if slug in problems_by_slug)
        spent_xp = user_doc.get("spent_xp", 0)
        xp = max(0, base_xp - spent_xp)
        
        # 4. Calculate domains proficiency
        domain_list = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]
        domain_challenges = {d: [] for d in domain_list}
        for p in all_problems:
            d = p.get("domain", "Backend")
            if d in domain_challenges:
                domain_challenges[d].append(p)
                
        domain_proficiencies = []
        for d in domain_list:
            ch_list = domain_challenges[d]
            total_in_domain = len(ch_list)
            solved_in_domain = sum(1 for p in ch_list if p["slug"] in solved_slugs)
            
            if total_in_domain > 0:
                score = min(100, int((solved_in_domain / total_in_domain) * 100))
                if solved_in_domain > 0:
                    score = min(100, max(score, 30 + solved_in_domain * 20))
                else:
                    score = 10
            else:
                score = 10
            domain_proficiencies.append({"domain": d, "score": score})

        # Calculate ratings for stats cards
        rating = 1000 + solved_count * 100 + int(xp * 0.1)
        
        # Rank: Let's query all users and sort them to calculate the rank
        all_users_cursor = db.users.find({})
        all_users = await all_users_cursor.to_list(length=1000)
        user_scores = []
        for u in all_users:
            u_id = u["user_id"]
            u_subs = await db.submissions.count_documents({"user_id": u_id, "status": "accepted"})
            user_scores.append((u_id, u_subs))
        user_scores.sort(key=lambda x: x[1], reverse=True)
        
        rank = 1
        for i, (uid, _) in enumerate(user_scores):
            if uid == user_id:
                rank = i + 1
                break
                
        # Heatmap contributions — 365 days for full-year LeetCode-style view
        cutoff_date = datetime.utcnow() - timedelta(days=365)
        sub_activity_cursor = db.submissions.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff_date}
        })
        sub_activities = await sub_activity_cursor.to_list(length=2000)
        
        rep_activity_cursor = db.interview_reports.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff_date}
        })
        rep_activities = await rep_activity_cursor.to_list(length=500)
        
        heatmap_map = {}
        for act in sub_activities:
            dt_val = act.get("created_at")
            if isinstance(dt_val, datetime):
                dt_str = dt_val.strftime("%Y-%m-%d")
                heatmap_map[dt_str] = heatmap_map.get(dt_str, 0) + 1
                
        for act in rep_activities:
            dt_val = act.get("created_at")
            if isinstance(dt_val, datetime):
                dt_str = dt_val.strftime("%Y-%m-%d")
                heatmap_map[dt_str] = heatmap_map.get(dt_str, 0) + 1

        # Badges — use the BadgeService for gamified badges
        from app.services.badge_service import BadgeService
        newly_awarded = await BadgeService.check_and_award_badges(user_id)
        earned_badges = await BadgeService.get_earned_badges(user_id)
        badge_progress = await BadgeService.get_badge_progress(user_id)
        badges = [b.get("name", b.get("id")) for b in earned_badges]
        if not badges:
            badges = ["Novice Engineer"]

        # Trigger notifications for newly-awarded badges
        if newly_awarded:
            from app.services.notification_service import NotificationService
            for badge in newly_awarded:
                await NotificationService.on_badge_earned(user_id, badge)

        # Interview reports history list
        interviews_cursor = db.interview_reports.find({"user_id": user_id}).sort("created_at", -1)
        interviews_db = await interviews_cursor.to_list(length=50)
        
        interview_history = []
        for rep in interviews_db:
            created_at = rep.get("created_at")
            when_str = "Recent"
            if isinstance(created_at, datetime):
                diff = datetime.utcnow() - created_at
                if diff.days == 0:
                    when_str = "Today"
                elif diff.days == 1:
                    when_str = "1d ago"
                else:
                    when_str = f"{diff.days}d ago"
                    
            rep_data = rep.get("report", {})
            interview_history.append({
                "id": rep.get("session_id"),
                "role": rep.get("role") or "Software Engineer",
                "score": rep_data.get("overall_score") or rep_data.get("average_score") or 75,
                "when": when_str,
                "duration": 45,
            })

        # --- A. Weekly Activity (real-time data) ---
        start_of_week = datetime.utcnow() - timedelta(days=7)
        weekly_subs_cursor = db.submissions.find({
            "user_id": user_id,
            "created_at": {"$gte": start_of_week}
        })
        weekly_subs = await weekly_subs_cursor.to_list(length=100)
        
        days_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
        # Compute dynamic weekly activity. We seed a small default background level so empty charts still look pretty.
        activity_weekly_dict = {days_map[i]: {"solved": 0, "minutes": 0} for i in range(7)}
        
        # Populate with actual weekly solved challenges
        for sub in weekly_subs:
            dt = sub.get("created_at")
            if isinstance(dt, datetime) and sub.get("status") == "accepted":
                weekday = dt.weekday()
                day_name = days_map[weekday]
                activity_weekly_dict[day_name]["solved"] += 1
                activity_weekly_dict[day_name]["minutes"] += 35
                
        # Transform back to list format
        activity_weekly = [
            {"day": day, "solved": data["solved"], "minutes": data["minutes"]}
            for day, data in activity_weekly_dict.items()
        ]


        # --- B. Recent Activity (real-time data) ---
        recent_activities = []
        for sub in accepted_subs[:4]:
            prob = problems_by_slug.get(sub.get("problem_slug"))
            if prob:
                dt_val = sub.get("created_at")
                when_str = "2h ago"
                if isinstance(dt_val, datetime):
                    diff = datetime.utcnow() - dt_val
                    if diff.days == 0:
                        when_str = "Today"
                    else:
                        when_str = f"{diff.days}d ago"
                recent_activities.append({
                    "type": "solved",
                    "text": f"Solved {prob.get('title')}",
                    "when": when_str,
                    "domain": prob.get("domain", "Backend"),
                    "created_at": dt_val,
                    "link": f"/app/challenges/{prob.get('slug')}"
                })
                
        for rep in interviews_db[:2]:
            dt_val = rep.get("created_at")
            when_str = "1d ago"
            if isinstance(dt_val, datetime):
                diff = datetime.utcnow() - dt_val
                if diff.days == 0:
                    when_str = "Today"
                else:
                    when_str = f"{diff.days}d ago"
            recent_activities.append({
                "type": "interview",
                "text": f"Completed AI Interview - {rep.get('role')}",
                "when": when_str,
                "domain": "Interview",
                "created_at": dt_val,
                "link": f"/app/interviews/{rep.get('session_id')}/report"
            })

        # Fetch user's latest notifications to show them in the activity feed
        notifs_cursor = db.notifications.find({"user_id": user_id}).sort("created_at", -1)
        db_notifs = await notifs_cursor.to_list(length=10)
        
        for n in db_notifs:
            dt_val = n.get("created_at")
            if isinstance(dt_val, str):
                try:
                    dt_val = datetime.fromisoformat(dt_val.replace("Z", "+00:00"))
                except ValueError:
                    dt_val = datetime.utcnow()
            elif not isinstance(dt_val, datetime):
                dt_val = datetime.utcnow()

            diff = datetime.utcnow() - dt_val
            if diff.days == 0:
                when_str = "Today"
            elif diff.days == 1:
                when_str = "1d ago"
            else:
                when_str = f"{diff.days}d ago"

            recent_activities.append({
                "id": n.get("id"),
                "type": "notification",
                "notification_type": n.get("type", "system"),
                "text": n.get("message") or n.get("title"),
                "when": when_str,
                "domain": "Contest" if n.get("type") == "invite" else "Alert",
                "created_at": dt_val,
                "link": n.get("link"),
                "read": n.get("read", False)
            })

        # Sort all activities chronologically (newest first)
        recent_activities.sort(key=lambda x: x.get("created_at") or datetime.min, reverse=True)


        # --- C. Recommended Challenges (not yet solved) ---
        recommended = []
        for p in all_problems:
            if p.get("slug") not in solved_slugs:
                recommended.append(p)
        if len(recommended) < 4:
            recommended.extend(all_problems)
            
        # --- D. Interview Score Trend ---
        interview_trend = []
        reversed_history = list(reversed(interview_history[:8]))
        for idx, iv in enumerate(reversed_history):
            interview_trend.append({
                "d": f"W{idx+1}",
                "s": iv.get("score", 75)
            })


        # Compile flat user profile details
        user_profile_data = {
            "name": user_doc.get("full_name", user_doc.get("username")),
            "username": user_doc.get("username"),
            "email": user_doc.get("email"),
            "avatar": user_doc.get("avatar"),
            "location": user_doc.get("location"),
            "github_username": user_doc.get("github_username"),
            "website": user_doc.get("website"),
            "rating": rating,
            "rank": rank,
            "xp": xp,
            "streak": user_doc.get("streak_count", 0),
            "solved": solved_count,
            "interviews": len(interview_history),
            "domains": domain_proficiencies,
            "badges": badges,
            "heatmap": heatmap_map,
            "frontend_rating": user_doc.get("frontend_rating", 0),
            "backend_rating": user_doc.get("backend_rating", 0),
            "fullstack_rating": user_doc.get("fullstack_rating", 0),
            "devops_rating": user_doc.get("devops_rating", 0),
            "overall_rating": user_doc.get("overall_rating", rating),
            "streak_count": user_doc.get("streak_count", 0),
            "is_premium": user_doc.get("is_premium", False),
        }

        return {
            "user": user_profile_data,
            "activityWeekly": activity_weekly,
            "recentActivity": recent_activities[:5],
            "recommendedChallenges": recommended[:4],
            "interviewTrend": interview_trend,
            "badgeProgress": badge_progress,
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
            # Inject is_premium dynamically
            challenge["is_premium"] = challenge.get("is_premium", False) or challenge.get("slug") in {"responsive-data-table", "design-twitter-feed", "k8s-blue-green"}
            items.append(challenge)

        if sort == "xp":
            items.sort(key=lambda c: c.get("xp", 0), reverse=True)
        elif sort == "time":
            items.sort(key=lambda c: c.get("minutes", 0))
        elif sort == "completion":
            items.sort(key=lambda c: c.get("completion", 0), reverse=True)

        return {"items": items, "count": len(items), "domains": DOMAINS}

    @staticmethod
    async def get_challenge(slug: str, requesting_user: dict | None = None):
        challenges = await _collection_or_seed("problems", CHALLENGES)
        challenge = next((item for item in challenges if item.get("slug") == slug or item.get("id") == slug), None)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        
        # Inject is_premium dynamically
        challenge["is_premium"] = challenge.get("is_premium", False) or challenge.get("slug") in {"responsive-data-table", "design-twitter-feed", "k8s-blue-green"}
        
        # Access control: redact sensitive details for non-premium users on premium challenges
        if challenge.get("is_premium"):
            is_premium_user = requesting_user.get("is_premium", False) if requesting_user else False
            if not is_premium_user:
                redacted = dict(challenge)
                redacted["locked"] = True
                redacted["starter_code"] = {k: "/* PREMIUM CONTENT LOCKED */" for k in redacted.get("starter_code", {})}
                redacted["test_cases"] = []
                redacted["description"] = "This is a premium engineering challenge. Subscribe to unlock the interactive editor, test cases, and AI review."
                return redacted
                
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
    async def leaderboard(page: int = 1, limit: int = 25, q: str | None = None):
        # Query users from MongoDB users collection
        cursor = db.users.find({"is_active": {"$ne": False}})
        users = await cursor.to_list(length=1000)
        
        # If only 1 or 2 users exist in the DB, seed other participants to make the arena active
        if len(users) <= 2:
            seed_users = [
                {"user_id": str(uuid4()), "username": "amelia.dev", "full_name": "Amelia Dev", "rating": 2843, "total_xp": 184200, "country": "US", "delta": 24, "badges": ["Top 1%", "DevOps"], "email": "amelia@example.com"},
                {"user_id": str(uuid4()), "username": "kenji_w", "full_name": "Kenji Watanabe", "rating": 2790, "total_xp": 172480, "country": "JP", "delta": 12, "badges": ["Top 1%"], "email": "kenji@example.com"},
                {"user_id": str(uuid4()), "username": "priya.s", "full_name": "Priya Sharma", "rating": 2755, "total_xp": 168120, "country": "IN", "delta": -3, "badges": ["Backend"], "email": "priya@example.com"},
                {"user_id": str(uuid4()), "username": "lucasf", "full_name": "Lucas Ferraz", "rating": 2710, "total_xp": 161300, "country": "BR", "delta": 8, "badges": ["System Design"], "email": "lucas@example.com"},
                {"user_id": str(uuid4()), "username": "noor.k", "full_name": "Noor Khan", "rating": 2682, "total_xp": 158020, "country": "AE", "delta": 5, "badges": ["APIs"], "email": "noor@example.com"},
                {"user_id": str(uuid4()), "username": "aria.j", "full_name": "Aria Jeong", "rating": 2654, "total_xp": 152410, "country": "KR", "delta": 0, "badges": ["Frontend"], "email": "aria@example.com"}
            ]
            for su in seed_users:
                await db.users.update_one({"username": su["username"]}, {"$set": su}, upsert=True)
            cursor = db.users.find({"is_active": {"$ne": False}})
            users = await cursor.to_list(length=1000)
            
        items = []
        for u in users:
            user_id = u["user_id"]
            # Count accepted submissions
            subs_count = await db.submissions.count_documents({"user_id": user_id, "status": "accepted"})
            
            # Count interview reports
            interviews_count = await db.interview_reports.count_documents({"user_id": user_id})
            
            # Find accepted problem slugs
            accepted_subs = await db.submissions.find({"user_id": user_id, "status": "accepted"}).to_list(length=1000)
            solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}
            
            # Count system design completed
            completed_sys_design = await db.user_system_design_progress.count_documents({"user_id": user_id, "progress": "Completed"})
            
            # Fetch problem definitions to sum XP
            problems_cursor = db.problems.find({"slug": {"$in": list(solved_slugs)}})
            problems_list = await problems_cursor.to_list(length=1000)
            problems_by_slug = {p["slug"]: p for p in problems_list}
            
            base_xp = sum(problems_by_slug[slug].get("xp_reward", 100) for slug in solved_slugs if slug in problems_by_slug)
            sys_design_xp = completed_sys_design * 100
            
            spent_xp = u.get("spent_xp", 0)
            xp = max(0, base_xp + sys_design_xp - spent_xp)
            
            # Fall back to user document details if no calculated progress (e.g. for mock seeded users)
            if xp == 0:
                xp = u.get("total_xp") or u.get("xp") or 0
                
            rating = 1000 + subs_count * 100 + completed_sys_design * 50 + int(xp * 0.1)
            if subs_count == 0 and completed_sys_design == 0:
                rating = u.get("rating") or u.get("overall_rating") or 1000
                
            badges = []
            db_badges = u.get("badges", [])
            for b in db_badges:
                if isinstance(b, dict):
                    badges.append(b.get("badge_id"))
                elif isinstance(b, str):
                    badges.append(b)
                    
            if subs_count >= 1 and "First Milestone" not in badges:
                badges.append("First Milestone")
            if completed_sys_design >= 1 and "System Design" not in badges:
                badges.append("System Design")
                
            if not badges:
                badges = ["Novice Engineer"]
                
            items.append({
                "username": u.get("username") or "developer",
                "rating": rating,
                "xp": xp,
                "country": u.get("country") or "GLOBAL",
                "delta": u.get("delta", 0),
                "badges": badges,
                "avatar": u.get("avatar"),
                "is_premium": u.get("is_premium", False)
            })
            
        # Sort by rating, then by xp
        items.sort(key=lambda x: (x["rating"], x["xp"]), reverse=True)
        
        # Assign ranks
        for idx, item in enumerate(items):
            item["rank"] = idx + 1
            
        # Filter by query
        if q:
            query_str = q.strip().lower()
            items = [entry for entry in items if query_str in entry.get("username", "").lower()]
            
        total = len(items)
        
        # Slicing
        start = (page - 1) * limit
        end = start + limit
        paginated_items = items[start:end]
        
        return {
            "items": paginated_items,
            "total": total,
            "page": page,
            "limit": limit
        }

    @staticmethod
    async def profile(username: str | None = None, requesting_user_id: str | None = None):
        user_doc = None
        if username:
            user_doc = await db.users.find_one({"username": username})
        
        if not user_doc:
            # Fallback to the first user in DB if no username matched
            user_doc = await db.users.find_one({})
            
        if not user_doc:
            # No fallback to mock — return empty for production
            return {
                "success": True,
                "user": {
                    "name": "Unknown", "username": username or "", "email": "",
                    "avatar": None, "location": "", "rating": 1000, "rank": 0,
                    "xp": 0, "solved": 0, "interviews": 0, "domains": [],
                    "badges": [], "heatmap": {}, "following_count": 0,
                    "followers_count": 0, "is_following": False, "bio": "",
                    "country": "", "linkedin_url": "", "portfolio_url": "",
                },
                "challenges": [],
                "interviews_history": [],
                "badge_progress": {"earned": [], "locked": [], "total": 0, "earned_count": 0},
            }

        user_id = user_doc["user_id"]
        
        # 1. Fetch user's submissions
        submissions_cursor = db.submissions.find({"user_id": user_id})
        submissions = await submissions_cursor.to_list(length=1000)
        
        # Filter accepted submissions
        accepted_subs = [s for s in submissions if s.get("status") == "accepted"]
        solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}
        
        # 2. Fetch all challenges from problems collection
        problems_cursor = db.problems.find({})
        all_problems = [_serialize(p) for p in await problems_cursor.to_list(length=1000)]
        problems_by_slug = {p["slug"]: p for p in all_problems}
        
        # 3. Calculate solved count and XP
        solved_count = len(solved_slugs)
        
        # Sum of XP rewards for solved challenges
        base_xp = sum(problems_by_slug[slug].get("xp_reward", 100) for slug in solved_slugs if slug in problems_by_slug)
        spent_xp = user_doc.get("spent_xp", 0)
        xp = max(0, base_xp - spent_xp)
        
        # 4. Calculate domains proficiency
        domain_list = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]
        domain_challenges = {d: [] for d in domain_list}
        for p in all_problems:
            d = p.get("domain", "Backend")
            if d in domain_challenges:
                domain_challenges[d].append(p)
                
        domain_proficiencies = []
        for d in domain_list:
            ch_list = domain_challenges[d]
            total_in_domain = len(ch_list)
            solved_in_domain = sum(1 for p in ch_list if p["slug"] in solved_slugs)
            
            if total_in_domain > 0:
                score = min(100, int((solved_in_domain / total_in_domain) * 100))
                # Boost presentation score slightly for single completions to keep it attractive
                if solved_in_domain > 0:
                    score = min(100, max(score, 30 + solved_in_domain * 20))
                else:
                    score = 10
            else:
                score = 10
            domain_proficiencies.append({"domain": d, "score": score})
            
        # 5. Calculate overall rating
        rating = 1000 + solved_count * 100 + int(xp * 0.1)
        
        # 6. Rank: Let's query all users and sort them to calculate the rank
        all_users_cursor = db.users.find({})
        all_users = await all_users_cursor.to_list(length=1000)
        user_scores = []
        for u in all_users:
            u_id = u["user_id"]
            u_subs = await db.submissions.count_documents({"user_id": u_id, "status": "accepted"})
            user_scores.append((u_id, u_subs))
        user_scores.sort(key=lambda x: x[1], reverse=True)
        
        rank = 1
        for i, (uid, _) in enumerate(user_scores):
            if uid == user_id:
                rank = i + 1
                break
                
        # 7. Heatmap: activity in the last 365 days (LeetCode-style)
        cutoff_date = datetime.utcnow() - timedelta(days=365)
        
        sub_activity_cursor = db.submissions.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff_date}
        })
        sub_activities = await sub_activity_cursor.to_list(length=2000)
        
        rep_activity_cursor = db.interview_reports.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff_date}
        })
        rep_activities = await rep_activity_cursor.to_list(length=500)
        
        heatmap_map = {}
        for act in sub_activities:
            dt_val = act.get("created_at")
            if isinstance(dt_val, datetime):
                dt_str = dt_val.strftime("%Y-%m-%d")
                heatmap_map[dt_str] = heatmap_map.get(dt_str, 0) + 1
                
        for act in rep_activities:
            dt_val = act.get("created_at")
            if isinstance(dt_val, datetime):
                dt_str = dt_val.strftime("%Y-%m-%d")
                heatmap_map[dt_str] = heatmap_map.get(dt_str, 0) + 1
        
        # 8. Badges — use gamified BadgeService
        from app.services.badge_service import BadgeService
        await BadgeService.check_and_award_badges(user_id)
        earned_badges = await BadgeService.get_earned_badges(user_id)
        badge_progress = await BadgeService.get_badge_progress(user_id)
        badges = [b.get("name", b.get("id")) for b in earned_badges]
        if not badges:
            badges = ["Novice Engineer"]
            
        # 9. Solved challenges detail list
        solved_challenges_list = []
        for slug in solved_slugs:
            p = problems_by_slug.get(slug)
            if p:
                solved_challenges_list.append({
                    "id": p.get("id"),
                    "slug": p.get("slug"),
                    "title": p.get("title"),
                    "domain": p.get("domain"),
                    "difficulty": p.get("difficulty"),
                    "xp": p.get("xp_reward", 100),
                })
                
        # 10. Interview history list
        interviews_cursor = db.interview_reports.find({"user_id": user_id}).sort("created_at", -1)
        interviews_db = await interviews_cursor.to_list(length=50)
        
        interview_history = []
        for rep in interviews_db:
            created_at = rep.get("created_at")
            when_str = "Recent"
            if isinstance(created_at, datetime):
                diff = datetime.utcnow() - created_at
                if diff.days == 0:
                    when_str = "Today"
                elif diff.days == 1:
                    when_str = "1d ago"
                else:
                    when_str = f"{diff.days}d ago"
                    
            rep_data = rep.get("report", {})
            interview_history.append({
                "id": rep.get("session_id"),
                "role": rep.get("role") or "Software Engineer",
                "score": rep_data.get("overall_score") or rep_data.get("average_score") or 75,
                "when": when_str,
                "duration": 45,
            })
            
        return {
            "success": True,
            "user": {
                "name": user_doc.get("full_name", user_doc.get("username")),
                "username": user_doc.get("username"),
                "email": user_doc.get("email"),
                "avatar": user_doc.get("avatar"),
                "location": user_doc.get("location"),
                "github_username": user_doc.get("github_username"),
                "website": user_doc.get("website"),
                "rating": rating,
                "rank": rank,
                "xp": xp,
                "solved": solved_count,
                "interviews": len(interview_history),
                "domains": domain_proficiencies,
                "badges": badges,
                "heatmap": heatmap_map,
                "following_count": len(user_doc.get("following", [])),
                "followers_count": len(user_doc.get("followers", [])),
                "is_following": requesting_user_id in user_doc.get("followers", []) if requesting_user_id else False,
                "bio": user_doc.get("bio", ""),
                "country": user_doc.get("country", ""),
                "linkedin_url": user_doc.get("linkedin_url", ""),
                "portfolio_url": user_doc.get("portfolio_url", ""),
                "is_premium": user_doc.get("is_premium", False),
            },
            "challenges": solved_challenges_list,
            "interviews_history": interview_history,
            "badge_progress": badge_progress,
        }

    @staticmethod
    async def follow_user(username: str, requesting_user_id: str):
        # 1. Retrieve the target user
        target_user = await db.users.find_one({"username": username})
        if not target_user:
            raise HTTPException(status_code=404, detail="Target user not found.")

        target_user_id = target_user["user_id"]

        # 2. Check if trying to follow self
        if target_user_id == requesting_user_id:
            raise HTTPException(status_code=400, detail="You cannot follow yourself.")

        # 3. Add to followers and following collections atomically
        await db.users.update_one(
            {"user_id": target_user_id},
            {"$addToSet": {"followers": requesting_user_id}}
        )
        await db.users.update_one(
            {"user_id": requesting_user_id},
            {"$addToSet": {"following": target_user_id}}
        )

        return {"success": True, "message": f"Successfully followed @{username}"}

    @staticmethod
    async def unfollow_user(username: str, requesting_user_id: str):
        # 1. Retrieve the target user
        target_user = await db.users.find_one({"username": username})
        if not target_user:
            raise HTTPException(status_code=404, detail="Target user not found.")

        target_user_id = target_user["user_id"]

        # 2. Remove from followers and following collections atomically
        await db.users.update_one(
            {"user_id": target_user_id},
            {"$pull": {"followers": requesting_user_id}}
        )
        await db.users.update_one(
            {"user_id": requesting_user_id},
            {"$pull": {"following": target_user_id}}
        )

        return {"success": True, "message": f"Successfully unfollowed @{username}"}

    @staticmethod
    async def activity():
        return {"weekly": ACTIVITY_WEEKLY, "recent": RECENT_ACTIVITY}

    @staticmethod
    async def interviews():
        return {"history": INTERVIEW_HISTORY}

    @staticmethod
    async def system_design(user_id: str):
        from app.controllers.admin import AdminController
        ch = await AdminController.list_system_design_challenges()
        tpl = await AdminController.list_system_design_templates()
        
        # Fetch user's progress
        progress_cursor = db.user_system_design_progress.find({"user_id": user_id})
        progress_list = await progress_cursor.to_list(length=100)
            
        user_progress = {
            (p.get("challenge_id") or p.get("id")): p.get("progress", "Not Started")
            for p in progress_list if (p.get("challenge_id") or p.get("id"))
        }
        user_canvas = {
            (p.get("challenge_id") or p.get("id")): {
                "nodes": p["nodes"],
                "edges": p["edges"]
            } for p in progress_list if (p.get("challenge_id") or p.get("id")) and "nodes" in p and "edges" in p
        }
        
        base_attempts_map = {
            "url-shortener": 2420,
            "video-streaming": 1850,
            "ride-sharing": 1980,
            "chat-app": 3200,
            "ecommerce": 2100,
            "social-feed": 1540,
            "blank": 5400
        }
        
        # Merge progress, attempts and relative times with challenges
        for c in ch:
            user_entry = next((p for p in progress_list if (p.get("challenge_id") or p.get("id")) == c["id"]), None)
            c["progress"] = user_entry.get("progress", "Not Started") if user_entry else "Not Started"
            
            if user_entry and user_entry.get("updated_at"):
                c["lastAttempted"] = format_relative_time(user_entry["updated_at"])
            else:
                c["lastAttempted"] = "Not attempted" if c["progress"] == "Not Started" else "Recent"
                
            db_attempts = await db.user_system_design_progress.count_documents({"challenge_id": c["id"]})
            c["attempts"] = base_attempts_map.get(c["id"], 500) + db_attempts
            
        base_tpl_attempts_map = {
            "basic-web": 1200,
            "ecommerce": 1450,
            "url-shortener": 980,
            "chat": 1600,
            "netflix": 2100,
            "instagram": 1750,
            "uber": 1300,
            "whatsapp": 1900,
            "youtube": 1500,
            "ai-saas": 2200
        }
        
        # Merge progress, attempts and relative times with templates
        for t in tpl:
            user_entry = next((p for p in progress_list if (p.get("challenge_id") or p.get("id")) == t["id"]), None)
            t["progress"] = user_entry.get("progress", "Not Started") if user_entry else "Not Started"
            
            if user_entry and user_entry.get("updated_at"):
                t["lastAttempted"] = format_relative_time(user_entry["updated_at"])
            else:
                t["lastAttempted"] = "Not attempted" if t["progress"] == "Not Started" else "Recent"
                
            db_attempts = await db.user_system_design_progress.count_documents({"challenge_id": t["id"]})
            t["attempts"] = base_tpl_attempts_map.get(t["id"], 400) + db_attempts
            t["duration"] = "Self-paced"
            
        return {
            "topics": SYSTEM_DESIGN_TOPICS,
            "challenges": ch,
            "templates": tpl,
            "userProgress": user_progress,
            "userCanvas": user_canvas
        }

    @staticmethod
    async def update_system_design_progress(user_id: str, challenge_id: str, progress: str):
        if progress not in ("Completed", "In Progress", "Not Started"):
            raise HTTPException(status_code=400, detail="Invalid progress status value")
            
        prev = await db.user_system_design_progress.find_one({
            "user_id": user_id,
            "$or": [{"challenge_id": challenge_id}, {"id": challenge_id}]
        })
        prev_progress = prev.get("progress") if prev else None
        
        await db.user_system_design_progress.update_one(
            {
                "user_id": user_id,
                "$or": [{"challenge_id": challenge_id}, {"id": challenge_id}]
            },
            {
                "$set": {
                    "user_id": user_id,
                    "challenge_id": challenge_id,
                    "progress": progress,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        if progress == "Completed" and prev_progress != "Completed":
            await db.users.update_one(
                {"user_id": user_id},
                {
                    "$inc": {
                        "total_system_design_completed": 1,
                        "total_xp": 100,
                        "system_design_rating": 50
                    }
                }
            )
        elif prev_progress == "Completed" and progress != "Completed":
            await db.users.update_one(
                {"user_id": user_id},
                {
                    "$inc": {
                        "total_system_design_completed": -1,
                        "total_xp": -100,
                        "system_design_rating": -50
                    }
                }
            )
            
        return {"success": True, "progress": progress}

    @staticmethod
    async def save_system_design_canvas(user_id: str, challenge_id: str, nodes: list, edges: list):
        await db.user_system_design_progress.update_one(
            {
                "user_id": user_id,
                "$or": [{"challenge_id": challenge_id}, {"id": challenge_id}]
            },
            {
                "$set": {
                    "user_id": user_id,
                    "challenge_id": challenge_id,
                    "nodes": nodes,
                    "edges": edges,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        return {"success": True}

    @staticmethod
    async def candidates():
        cursor = db.users.find({"role": "user"})
        candidates_list = []
        async for u in cursor:
            # Determine their top domain track based on individual ratings
            ratings = {
                "Backend": u.get("backend_rating", 0) or 0,
                "Frontend": u.get("frontend_rating", 0) or 0,
                "DevOps": u.get("devops_rating", 0) or 0,
                "System Design": u.get("system_design_rating", 0) or 0,
                "Databases": u.get("database_rating", 0) or 0,
                "APIs": u.get("api_rating", 0) or 0,
            }
            top_track = max(ratings, key=ratings.get) if any(ratings.values()) else "Backend"

            # Retrieve database domain strengths
            ds = u.get("domain_strengths") or {}
            if hasattr(ds, "dict"):
                ds = ds.dict()
            elif not isinstance(ds, dict):
                ds = {}

            technical = ds.get("backend", 0) or ds.get("frontend", 0) or ds.get("fullstack", 0) or 75
            system_design = ds.get("system_design", 0) or 70
            communication = int(u.get("average_interview_score", 0) or 80)

            candidates_list.append({
                "name": u.get("full_name") or u.get("username") or "Anonymous Engineer",
                "username": u.get("username") or "",
                "rating": u.get("overall_rating", 1200) or 1200,
                "top": top_track,
                "verified": u.get("is_verified", False),
                "location": u.get("location") or u.get("country") or "Remote",
                "technical": technical,
                "systemDesign": system_design,
                "communication": communication
            })

        if not candidates_list:
            candidates_list = CANDIDATES

        return {"items": candidates_list}

    @staticmethod
    async def ai_evaluation(username: str | None = None, force_refresh: bool = False):
        import json
        from app.ai.services.ai_client import ai_client
        from pydantic import BaseModel

        class AIEvaluationReport(BaseModel):
            profile_summary: str
            strengths: list[str]
            improvements: list[str]
            suggested_paths: list[str]
            next_challenges: list[str]

        user_doc = None
        if username:
            user_doc = await db.users.find_one({"username": username})
        
        if not user_doc:
            user_doc = await db.users.find_one({})
            
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
            
        user_id = user_doc["user_id"]
        
        # Check cache if not force_refresh
        if not force_refresh:
            cached = await db.ai_evaluations.find_one({"user_id": user_id})
            if cached:
                created_at = cached.get("created_at")
                if isinstance(created_at, datetime) and (datetime.utcnow() - created_at).total_seconds() < 86400:
                    return {"success": True, "evaluation": cached["evaluation"]}
                    
        # 1. Fetch user's solved challenges
        submissions_cursor = db.submissions.find({"user_id": user_id, "status": "accepted"})
        accepted_subs = await submissions_cursor.to_list(length=100)
        solved_slugs = [s["problem_slug"] for s in accepted_subs if s.get("problem_slug")]
        
        problems_cursor = db.problems.find({"slug": {"$in": solved_slugs}})
        problems = await problems_cursor.to_list(length=100)
        solved_titles = [p.get("title") for p in problems if p.get("title")]
        
        # 2. Fetch attempted but not solved
        all_subs_cursor = db.submissions.find({"user_id": user_id})
        all_subs = await all_subs_cursor.to_list(length=200)
        attempted_slugs = {s["problem_slug"] for s in all_subs if s.get("problem_slug") and s.get("problem_slug") not in solved_slugs}
        attempted_problems_cursor = db.problems.find({"slug": {"$in": list(attempted_slugs)}})
        attempted_problems = await attempted_problems_cursor.to_list(length=100)
        attempted_titles = [p.get("title") for p in attempted_problems if p.get("title")]
        
        # 3. Fetch interview reports
        interviews_cursor = db.interview_reports.find({"user_id": user_id}).sort("created_at", -1)
        interviews_db = await interviews_cursor.to_list(length=5)
        
        recent_interviews = []
        for rep in interviews_db:
            rep_data = rep.get("report", {})
            recent_interviews.append({
                "role": rep.get("role") or "Software Engineer",
                "score": rep_data.get("overall_score") or rep_data.get("average_score") or 75,
                "feedback": rep_data.get("overall_feedback") or rep_data.get("feedback") or ""
            })
            
        # 4. Generate report via Groq LLM
        prompt = f"""
        Candidate: {user_doc.get('full_name')}
        Username: {user_doc.get('username')}
        Solved Challenges: {', '.join(solved_titles) if solved_titles else 'None yet'}
        Attempted but not solved challenges: {', '.join(attempted_titles) if attempted_titles else 'None yet'}
        Recent Interview Performance: {json.dumps(recent_interviews, default=str)}
        """
        
        system_prompt = """You are a world-class AI Career Advisor and Senior Technical Recruiter at Interleet. 
        Analyze the candidate's solved and attempted coding challenges and mock interview performances on our platform. 
        Synthesize a highly professional, realistic, and inspiring profile report.
        """
        
        try:
            report_json = await ai_client.generate_json(
                system=system_prompt,
                user=prompt,
                schema=AIEvaluationReport,
                temperature=0.3
            )
            evaluation_data = report_json.model_dump()
        except Exception as exc:
            # Fallback evaluation report in case of API keys/timeouts issues
            evaluation_data = {
                "profile_summary": f"Active developer profiling for {user_doc.get('full_name')}. Solved {len(solved_titles)} challenges.",
                "strengths": ["Demonstrates strong learning agility by actively solving algorithms.", "Language proficiency in TypeScript/JavaScript."],
                "improvements": ["Deepen knowledge in system scalability and concurrency models.", "Gain more experience with SQL index optimizations."],
                "suggested_paths": ["Software Engineer (Generalist)", "Fullstack developer"],
                "next_challenges": ["Build a Token Bucket Rate Limiter", "Postgres Indexing Strategy"]
            }
            
        # Save to cache
        await db.ai_evaluations.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "evaluation": evaluation_data,
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return {"success": True, "evaluation": evaluation_data}

    @staticmethod
    async def update_profile(payload: dict, requesting_user: dict):
        user_info = requesting_user.get("user")
        if not user_info:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        user_id = user_info.get("user_id")
        
        allowed_updates = {}
        fields = [
            "location", "github_username", "website", 
            "full_name", "avatar", "bio", "country", 
            "linkedin_url", "portfolio_url"
        ]
        for field in fields:
            if field in payload:
                # Store empty strings or strip strings
                val = payload[field]
                allowed_updates[field] = val.strip() if isinstance(val, str) else val
            
        if not allowed_updates:
            return {"success": True, "message": "No fields to update"}
            
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": allowed_updates}
        )
        
        return {"success": True, "message": "Profile updated successfully"}

    @staticmethod
    async def public_stats():
        """Public stats for the landing page — no auth required."""
        # 1. Aggregate counts
        total_challenges = await db.problems.count_documents({})
        total_users = await db.users.count_documents({})
        total_interviews = await db.interview_reports.count_documents({})
        total_submissions = await db.submissions.count_documents({})
        total_contests = await db.contests.count_documents({})

        # 2. Per-domain challenge counts
        domain_list = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "Fullstack", "System Design"]
        domains = []
        for d in domain_list:
            count = await db.problems.count_documents({"domain": d})
            if count > 0:
                domains.append({"name": d, "challenge_count": count})

        # 3. Top 5 users by rating/activity (lightweight — no N+1 queries)
        all_users = await db.users.find(
            {},
            {"user_id": 1, "username": 1, "full_name": 1, "avatar": 1, "overall_rating": 1, "delta": 1, "_id": 0}
        ).to_list(length=100)

        # Sort by overall_rating descending, then assign ranks
        all_users.sort(key=lambda u: u.get("overall_rating", 0), reverse=True)
        top_users = []
        for idx, u in enumerate(all_users[:5]):
            top_users.append({
                "rank": idx + 1,
                "username": u.get("username", "developer"),
                "rating": u.get("overall_rating", 0),
                "avatar": u.get("avatar"),
                "delta": u.get("delta", 0),
            })

        # 4. Showcase user (highest rated) for dashboard preview
        showcase_user = None
        if all_users:
            top = all_users[0]
            uid = top.get("user_id")
            solved_count = await db.submissions.count_documents({"user_id": uid, "status": "accepted"})
            streak = 0
            user_full = await db.users.find_one({"user_id": uid})
            if user_full:
                streak = user_full.get("streak_count", 0)

            # Domain strengths for showcase
            problems_cursor = db.problems.find({})
            all_problems = await problems_cursor.to_list(length=500)

            accepted_subs = await db.submissions.find({"user_id": uid, "status": "accepted"}).to_list(length=500)
            solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}

            domain_strengths = []
            for d in ["Backend", "APIs", "System Design", "Frontend", "DevOps", "Databases"]:
                total_in_d = sum(1 for p in all_problems if p.get("domain") == d)
                solved_in_d = sum(1 for p in all_problems if p.get("domain") == d and p.get("slug") in solved_slugs)
                if total_in_d > 0:
                    score = min(100, int((solved_in_d / total_in_d) * 100))
                    if solved_in_d > 0:
                        score = min(100, max(score, 30 + solved_in_d * 20))
                    else:
                        score = 10
                else:
                    score = 10
                domain_strengths.append({"name": d, "score": score})

            # Sort by score, take top 3
            domain_strengths.sort(key=lambda x: x["score"], reverse=True)

            showcase_user = {
                "name": top.get("full_name", top.get("username", "Engineer")),
                "rating": top.get("overall_rating", 0),
                "xp": solved_count * 200,
                "rank": 1,
                "streak": streak,
                "solved": solved_count,
                "domain_strengths": domain_strengths[:3],
            }

        return {
            "total_challenges": total_challenges,
            "total_users": total_users,
            "total_interviews": total_interviews,
            "total_submissions": total_submissions,
            "total_contests": total_contests,
            "domains": domains,
            "top_users": top_users,
            "showcase_user": showcase_user,
        }

