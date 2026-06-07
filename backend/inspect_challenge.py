import asyncio, os, json
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient(os.environ.get('MONGODB_URI', 'mongodb://localhost:27017'))
    db = client[os.environ.get('MONGODB_DB', 'interleet')]

    users_cursor = db.users.find({})
    users = await users_cursor.to_list(length=100)

    for user_doc in users:
        user_id = user_doc["user_id"]
        print(f"Migrating user: {user_doc.get('username')}")

        # 1. Fetch user's submissions
        submissions_cursor = db.submissions.find({"user_id": user_id})
        submissions = await submissions_cursor.to_list(length=1000)
        
        # Filter accepted submissions
        accepted_subs = [s for s in submissions if s.get("status") == "accepted"]
        solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}
        
        # 2. Fetch all challenges from problems
        problems_cursor = db.problems.find({})
        all_problems = await problems_cursor.to_list(length=1000)
        problems_by_slug = {p["slug"]: p for p in all_problems}
        
        # Calculate domain ratings
        domain_list = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]
        domain_challenges = {d: [] for d in domain_list}
        for p in all_problems:
            d = p.get("domain", "Backend")
            if d in domain_challenges:
                domain_challenges[d].append(p)
                
        updates = {}
        
        # Calculate score per domain
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
                
            key_name = f"{d.lower().replace(' ', '')}_rating"
            updates[key_name] = score
            
        # Overall rating & solved
        solved_count = len(solved_slugs)
        xp = sum(problems_by_slug[slug].get("xp_reward", 100) for slug in solved_slugs if slug in problems_by_slug)
        
        updates["overall_rating"] = 1000 + solved_count * 100 + int(xp * 0.1)
        updates["total_xp"] = xp
        updates["solved_problems"] = list(solved_slugs)
        
        # Heatmap count in last 182 days
        cutoff = datetime.utcnow() - timedelta(days=182)
        sub_activity_cursor = db.submissions.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff}
        })
        sub_activities = await sub_activity_cursor.to_list(length=1000)
        
        rep_activity_cursor = db.interview_reports.find({
            "user_id": user_id,
            "created_at": {"$gte": cutoff}
        })
        rep_activities = await rep_activity_cursor.to_list(length=1000)
        
        heatmap_dates = set()
        for act in sub_activities + rep_activities:
            dt = act.get("created_at")
            if isinstance(dt, datetime):
                heatmap_dates.add(dt.strftime("%Y-%m-%d"))
                
        updates["streak_count"] = len(heatmap_dates)
        
        # Calculate badges
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
            
        updates["badges"] = badges
        
        # Update user in DB
        await db.users.update_one({"user_id": user_id}, {"$set": updates})
        print(f"Updated user: {user_doc.get('username')} with updates {updates}")

async def run():
    await main()

if __name__ == '__main__':
    asyncio.run(run())
