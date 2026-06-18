from datetime import datetime
from fastapi import HTTPException
from app.core.db import get_db

db = get_db()

# Default presets to seed if DB collection is empty
DEFAULT_INTERVIEW_PRESETS = [
    { "id": "backend", "title": "Senior Backend Engineer", "description": "Concurrency, services, databases, scaling.", "duration_minutes": 45 },
    { "id": "frontend", "title": "Frontend Architect", "description": "Performance, state, design systems, accessibility.", "duration_minutes": 45 },
    { "id": "sysdesign", "title": "System Design (L5)", "description": "End-to-end architecture for production systems.", "duration_minutes": 60 },
    { "id": "devops", "title": "DevOps Lead", "description": "CI/CD, infrastructure, reliability, on-call.", "duration_minutes": 45 },
    { "id": "apidesign", "title": "API Design", "description": "REST, contracts, versioning, evolvability.", "duration_minutes": 30 },
    { "id": "fullstack", "title": "Full-Stack Generalist", "description": "Mixed scenarios across the stack.", "duration_minutes": 50 },
    { "id": "mern", "title": "MERN Stack Developer", "description": "MongoDB, Express, React, Node.js, full-stack API integration.", "duration_minutes": 45 }
]

DEFAULT_SYSTEM_DESIGN_CHALLENGES = [
    {
        "id": "url-shortener",
        "title": "Design a URL Shortener",
        "difficulty": "Easy",
        "tags": ["Web", "Database", "Cache"],
        "brief": "Design a service like bit.ly that shortens long URLs and redirects users with low latency. Handle ~10k req/s with high read traffic.",
        "requirements": ["Generate unique short codes", "Sub-100ms redirects globally", "Analytics on click counts", "Handle read-heavy traffic (100:1 reads/writes)"],
        "hints": ["Cache hot keys in Redis", "Use a CDN for global reach", "Separate read replicas"]
    },
    {
        "id": "video-streaming",
        "title": "Design a Video Streaming Service",
        "difficulty": "Hard",
        "tags": ["CDN", "Storage", "Encoding"],
        "brief": "Architect a Netflix-style streaming platform serving millions of concurrent viewers across multiple regions.",
        "requirements": ["Adaptive bitrate streaming", "Global CDN distribution", "Recommendations service", "User auth & billing"],
        "hints": ["Use CDN edge nodes", "Async transcoding via queue", "Recommendation microservice"]
    }
]

DEFAULT_SYSTEM_DESIGN_TEMPLATES = [
    {
        "id": "basic-web",
        "name": "Basic Web App",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 60, "y": 240 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "lb", "type": "infra", "position": { "x": 320, "y": 240 }, "data": { "kind": "load-balancer", "label": "Load Balancer", "category": "Network" } },
            { "id": "ws", "type": "infra", "position": { "x": 580, "y": 240 }, "data": { "kind": "web-server", "label": "Web Server", "category": "Application" } },
            { "id": "db", "type": "infra", "position": { "x": 840, "y": 240 }, "data": { "kind": "postgresql", "label": "PostgreSQL", "category": "Data" } }
        ],
        "edges": [
            { "id": "c-lb", "source": "c", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-ws", "source": "lb", "target": "ws", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "ws-db", "source": "ws", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } }
        ]
    }
]

class AdminController:
    # ─── USER OPERATIONS ──────────────────────────────────────────────────
    @staticmethod
    async def list_users():
        cursor = db.users.find({}, {"_id": 0})
        return [user async for user in cursor]

    @staticmethod
    async def update_user_status(user_id: str, payload: dict):
        existing = await db.users.find_one({"user_id": user_id})
        if not existing:
            raise HTTPException(status_code=404, detail="User not found")

        updates = {}
        for key in ("role", "is_active", "is_premium", "is_locked"):
            if key in payload:
                updates[key] = payload[key]

        if updates:
            updates["updated_at"] = datetime.utcnow()
            await db.users.update_one({"user_id": user_id}, {"$set": updates})

        updated_user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
        return {"success": True, "user": updated_user}

    # ─── INTERVIEW PRESETS ────────────────────────────────────────────────
    @staticmethod
    async def list_presets():
        # Upsert default presets to guarantee any updates are always available in DB
        for p in DEFAULT_INTERVIEW_PRESETS:
            await db.interview_presets.update_one({"id": p["id"]}, {"$set": p}, upsert=True)
        cursor = db.interview_presets.find({}, {"_id": 0})
        return [p async for p in cursor]

    @staticmethod
    async def save_preset(preset_id: str, payload: dict):
        preset_data = {
            "id": preset_id,
            "title": payload.get("title", "Untitled Role"),
            "description": payload.get("description", ""),
            "duration_minutes": int(payload.get("duration_minutes", 45)),
            "updated_at": datetime.utcnow()
        }
        await db.interview_presets.update_one({"id": preset_id}, {"$set": preset_data}, upsert=True)
        return {"success": True, "preset": preset_data}

    @staticmethod
    async def delete_preset(preset_id: str):
        res = await db.interview_presets.delete_one({"id": preset_id})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Preset not found")
        return {"success": True, "message": "Preset deleted"}

    # ─── SYSTEM DESIGN CHALLENGES ──────────────────────────────────────────
    @staticmethod
    async def list_system_design_challenges():
        cursor = db.system_design_challenges.find({}, {"_id": 0})
        items = [c async for c in cursor]
        if not items:
            for c in DEFAULT_SYSTEM_DESIGN_CHALLENGES:
                await db.system_design_challenges.update_one({"id": c["id"]}, {"$set": c}, upsert=True)
            cursor = db.system_design_challenges.find({}, {"_id": 0})
            items = [c async for c in cursor]
        return items

    @staticmethod
    async def save_system_design_challenge(challenge_id: str, payload: dict):
        challenge_data = {
            "id": challenge_id,
            "title": payload.get("title", ""),
            "difficulty": payload.get("difficulty", "Medium"),
            "tags": payload.get("tags", []),
            "brief": payload.get("brief", ""),
            "requirements": payload.get("requirements", []),
            "hints": payload.get("hints", []),
            "updated_at": datetime.utcnow()
        }
        await db.system_design_challenges.update_one({"id": challenge_id}, {"$set": challenge_data}, upsert=True)
        return {"success": True, "challenge": challenge_data}

    @staticmethod
    async def delete_system_design_challenge(challenge_id: str):
        res = await db.system_design_challenges.delete_one({"id": challenge_id})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Challenge not found")
        return {"success": True, "message": "Challenge deleted"}

    # ─── SYSTEM DESIGN TEMPLATES ───────────────────────────────────────────
    @staticmethod
    async def list_system_design_templates():
        cursor = db.system_design_templates.find({}, {"_id": 0})
        items = [t async for t in cursor]
        if not items:
            for t in DEFAULT_SYSTEM_DESIGN_TEMPLATES:
                await db.system_design_templates.update_one({"id": t["id"]}, {"$set": t}, upsert=True)
            cursor = db.system_design_templates.find({}, {"_id": 0})
            items = [t async for t in cursor]
        return items

    @staticmethod
    async def save_system_design_template(template_id: str, payload: dict):
        template_data = {
            "id": template_id,
            "name": payload.get("name", ""),
            "nodes": payload.get("nodes", []),
            "edges": payload.get("edges", []),
            "description": payload.get("description", ""),
            "category": payload.get("category", "General"),
            "updated_at": datetime.utcnow()
        }
        await db.system_design_templates.update_one({"id": template_id}, {"$set": template_data}, upsert=True)
        return {"success": True, "template": template_data}

    @staticmethod
    async def delete_system_design_template(template_id: str):
        res = await db.system_design_templates.delete_one({"id": template_id})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Template not found")
        return {"success": True, "message": "Template deleted"}
