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
        user_doc = None
        if username:
            user_doc = await db.users.find_one({"username": username})
        
        if not user_doc:
            # Fallback to the first user in DB if no username matched
            user_doc = await db.users.find_one({})
            
        if not user_doc:
            # Fallback to static mock USER_PROFILE
            return {
                "success": True,
                "user": USER_PROFILE,
                "challenges": CHALLENGES[:3],
                "interviews_history": INTERVIEW_HISTORY
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
        all_problems = await problems_cursor.to_list(length=1000)
        problems_by_slug = {p["slug"]: p for p in all_problems}
        
        # 3. Calculate solved count and XP
        solved_count = len(solved_slugs)
        
        # Sum of XP rewards for solved challenges
        xp = sum(problems_by_slug[slug].get("xp_reward", 100) for slug in solved_slugs if slug in problems_by_slug)
        
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
                
        # 7. Heatmap: activity in the last 182 days
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=182)
        
        sub_activity_cursor = db.submissions.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff_date}
        })
        sub_activities = await sub_activity_cursor.to_list(length=1000)
        
        rep_activity_cursor = db.interview_reports.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff_date}
        })
        rep_activities = await rep_activity_cursor.to_list(length=1000)
        
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
        
        # 8. Badges
        badges = []
        if solved_count >= 1:
            badges.append("First Milestone")
        if len(rep_activities) >= 1:
            badges.append("Interview Scholar")
        if "build-a-rate-limiter" in solved_slugs:
            badges.append("Concurrency Expert")
        if "rest-versioning" in solved_slugs:
            badges.append("API Architect")
            
        solved_domains = set()
        for slug in solved_slugs:
            if slug in problems_by_slug:
                solved_domains.add(problems_by_slug[slug].get("domain"))
        if "Backend" in solved_domains:
            badges.append("Top 5% Backend")
        if len(solved_domains) >= 3:
            badges.append("Fullstack Wizard")
        if solved_count >= 5:
            badges.append("Algorithm Master")
            
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
                "location": user_doc.get("location", "Berlin, DE"),
                "rating": rating,
                "rank": rank,
                "xp": xp,
                "solved": solved_count,
                "interviews": len(interview_history),
                "domains": domain_proficiencies,
                "badges": badges,
                "heatmap": heatmap_map,
            },
            "challenges": solved_challenges_list,
            "interviews_history": interview_history
        }

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
