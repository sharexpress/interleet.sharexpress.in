from fastapi import APIRouter, Depends, HTTPException, Body
from datetime import datetime, timedelta
from typing import Dict, List
from app.core.db import get_db
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api/store", tags=["XP Store"])
db = get_db()

# Predefined list of store items
STORE_ITEMS = [
    {
        "id": "premium_30_days",
        "title": "30-Day Premium Pass",
        "cost": 3000,
        "description": "Unlock full Pro Elite access, including all premium coding challenges and real-time AI mock interviews.",
        "badge_icon": "Sparkles",
        "requirements": {
            "xp": 3000,
            "streak": 0,
            "challenges": 5
        }
    },
    {
        "id": "interleet_tshirt",
        "title": "Official Interleet Developer Tee",
        "cost": 5000,
        "description": "High-quality, ultra-soft cotton developer t-shirt with custom embroidered Interleet branding. Free shipping included.",
        "badge_icon": "Shirt",
        "requirements": {
            "xp": 5000,
            "streak": 7,
            "challenges": 15
        }
    },
    {
        "id": "interleet_bottle",
        "title": "Interleet Insulated Smart Bottle",
        "cost": 2500,
        "description": "Double-walled premium stainless steel thermal bottle keeping your drinks hot or cold for up to 24 hours.",
        "badge_icon": "GlassWater",
        "requirements": {
            "xp": 2500,
            "streak": 5,
            "challenges": 8
        }
    },
    {
        "id": "resume_review",
        "title": "AI Resume Review",
        "cost": 800,
        "description": "Get a comprehensive AI critique of your developer resume to bypass ATS screenings and optimize for top tech firms.",
        "badge_icon": "FileText",
        "requirements": {
            "xp": 800,
            "streak": 2,
            "challenges": 0
        }
    },
    {
        "id": "exclusive_badge",
        "title": "Quantum Coder Badge",
        "cost": 500,
        "description": "Showcase an exclusive 'Quantum Coder' badge on your public profile and the global leaderboard.",
        "badge_icon": "Award",
        "requirements": {
            "xp": 500,
            "streak": 5,
            "challenges": 1
        }
    },
    {
        "id": "interleet_notebook",
        "title": "Algorithmic Dotted Notebook",
        "cost": 1000,
        "description": "Premium hardcover notebook with grid dots, perfect for mapping out system architectures and brainstorming solutions.",
        "badge_icon": "BookOpen",
        "requirements": {
            "xp": 1000,
            "streak": 3,
            "challenges": 4
        }
    },
    {
        "id": "renewal_discount",
        "title": "20% Subscription Renewal Discount",
        "cost": 1200,
        "description": "Get a 20% discount coupon code for your next premium subscription renewal billing cycle.",
        "badge_icon": "Percent",
        "requirements": {
            "xp": 1200,
            "streak": 3,
            "challenges": 10
        }
    },
    {
        "id": "interleet_stickers",
        "title": "Elite Holographic Stickers Pack",
        "cost": 400,
        "description": "A pack of 10 premium vinyl holographic stickers to customize your workspace or laptop with coding flair.",
        "badge_icon": "Layers",
        "requirements": {
            "xp": 400,
            "streak": 0,
            "challenges": 2
        }
    }
]

async def get_user_stats(user_id: str, user_doc: dict):
    # 1. Fetch user's submissions
    submissions_cursor = db.submissions.find({"user_id": user_id})
    submissions = await submissions_cursor.to_list(length=1000)
    accepted_subs = [s for s in submissions if s.get("status") == "accepted"]
    solved_slugs = {s["problem_slug"] for s in accepted_subs if s.get("problem_slug")}
    
    # 2. Fetch all challenges from problems
    problems_cursor = db.problems.find({})
    all_problems = await problems_cursor.to_list(length=1000)
    problems_by_slug = {p["slug"]: p for p in all_problems}
    
    solved_count = len(solved_slugs)
    base_xp = sum(problems_by_slug[slug].get("xp_reward", 100) for slug in solved_slugs if slug in problems_by_slug)
    spent_xp = user_doc.get("spent_xp", 0)
    
    # Heatmap/Streak calculations (consistent with platform.py)
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
            
    streak = len(heatmap_dates)
    
    return {
        "xp": max(0, base_xp - spent_xp),
        "streak": streak,
        "challenges_solved": solved_count
    }

@router.get("/items")
async def get_store_items(user_auth=Depends(UserMiddleware.me)):
    user = user_auth["user"]
    user_id = user["user_id"]
    
    stats = await get_user_stats(user_id, user)
    
    items_with_eligibility = []
    for item in STORE_ITEMS:
        req = item["requirements"]
        
        xp_eligible = stats["xp"] >= req["xp"]
        streak_eligible = stats["streak"] >= req["streak"]
        challenges_eligible = stats["challenges_solved"] >= req["challenges"]
        
        already_redeemed = False
        if item["id"] == "exclusive_badge":
            already_redeemed = "Quantum Coder" in user.get("badges", [])
        else:
            already_redeemed = item["id"] in user.get("redeemed_items", [])
            
        eligible = xp_eligible and streak_eligible and challenges_eligible and not already_redeemed
        
        items_with_eligibility.append({
            **item,
            "user_stats": stats,
            "eligibility": {
                "xp_eligible": xp_eligible,
                "streak_eligible": streak_eligible,
                "challenges_eligible": challenges_eligible,
                "eligible": eligible,
                "already_redeemed": already_redeemed
            }
        })
        
    return {
        "success": True,
        "items": items_with_eligibility,
        "user_stats": stats
    }

@router.post("/redeem")
async def redeem_item(
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me)
):
    user = user_auth["user"]
    user_id = user["user_id"]
    item_id = payload.get("item_id")
    
    # Find the item
    item = next((i for i in STORE_ITEMS if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Store item not found.")
        
    req = item["requirements"]
    stats = await get_user_stats(user_id, user)
    
    # 1. Eligibility Checks
    if stats["xp"] < req["xp"]:
        raise HTTPException(status_code=400, detail="Insufficient XP points.")
    if stats["streak"] < req["streak"]:
        raise HTTPException(status_code=400, detail="Daily streak requirement not met.")
    if stats["challenges_solved"] < req["challenges"]:
        raise HTTPException(status_code=400, detail="Solved challenges requirement not met.")
        
    # Check already redeemed
    if item_id == "exclusive_badge":
        if "Quantum Coder" in user.get("badges", []):
            raise HTTPException(status_code=400, detail="Quantum Coder badge already redeemed.")
    else:
        if item_id in user.get("redeemed_items", []):
            raise HTTPException(status_code=400, detail="Item already redeemed.")
            
    # 2. Process Redemption
    # Deduct XP (increment spent_xp)
    await db.users.update_one(
        {"user_id": user_id},
        {"$inc": {"spent_xp": item["cost"]}}
    )

    # Update user's XP on the leaderboard entries
    await db.leaderboards.update_many(
        {"user_id": user_id},
        {"$set": {"xp": max(0, stats["xp"] - item["cost"])}}
    )
    
    now = datetime.utcnow()
    
    # Apply benefits
    if item_id == "premium_30_days":
        current_ends = user.get("subscription_ends_at")
        if current_ends and isinstance(current_ends, datetime) and current_ends > now:
            ends_at = current_ends + timedelta(days=30)
        else:
            ends_at = now + timedelta(days=30)
            
        updates = {
            "is_premium": True,
            "subscription_status": "active",
            "subscription_ends_at": ends_at,
            "updated_at": now
        }
        await db.users.update_one({"user_id": user_id}, {"$set": updates})
        
        # Update leaderboard cached premium status
        await db.leaderboards.update_many(
            {"user_id": user_id},
            {"$set": {"is_premium": True}}
        )
        
    elif item_id == "exclusive_badge":
        await db.users.update_one(
            {"user_id": user_id},
            {"$addToSet": {"badges": "Quantum Coder"}}
        )
        
    else:
        # Standard redemption tracking (e.g. for resume_review, renewal_discount)
        await db.users.update_one(
            {"user_id": user_id},
            {"$addToSet": {"redeemed_items": item_id}}
        )
        
    # Get updated user profile
    updated_user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    return {
        "success": True,
        "message": f"Successfully redeemed {item['title']}!",
        "user": updated_user
    }
