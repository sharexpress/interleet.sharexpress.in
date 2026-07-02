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
        "hints": ["Cache hot keys in Redis", "Use a CDN for global reach", "Separate read replicas"],
        "duration": "30m"
    },
    {
        "id": "video-streaming",
        "title": "Design a Video Streaming Service",
        "difficulty": "Hard",
        "tags": ["CDN", "Storage", "Encoding"],
        "brief": "Architect a Netflix-style streaming platform serving millions of concurrent viewers across multiple regions.",
        "requirements": ["Adaptive bitrate streaming", "Global CDN distribution", "Recommendations service", "User auth & billing"],
        "hints": ["Use CDN edge nodes", "Async transcoding via queue", "Recommendation microservice"],
        "duration": "45m"
    },
    {
        "id": "ride-sharing",
        "title": "Design a Ride-Sharing System",
        "difficulty": "Hard",
        "tags": ["Realtime", "Geo", "Queue"],
        "brief": "Build an Uber-like system that matches drivers and riders in real time with live location tracking.",
        "requirements": ["Realtime location updates", "Driver matching service", "Trip & payment service", "Surge pricing"],
        "hints": ["Use Kafka for event streams", "Geospatial index in Redis", "Microservices per domain"],
        "duration": "50m"
    },
    {
        "id": "chat-app",
        "title": "Design a Chat Application",
        "difficulty": "Medium",
        "tags": ["Realtime", "Messaging"],
        "brief": "Design WhatsApp-style messaging with 1:1 chats, group chats, presence and read receipts.",
        "requirements": ["WebSocket fanout", "Message persistence", "Push notifications", "Read receipts"],
        "hints": ["Message broker like Kafka", "Cache presence in Redis", "Sharded DB by user"],
        "duration": "35m"
    },
    {
        "id": "ecommerce",
        "title": "Design an E-Commerce Platform",
        "difficulty": "Medium",
        "tags": ["Catalog", "Orders", "Payments"],
        "brief": "Build an Amazon-like store with catalog, cart, checkout, inventory and order processing.",
        "requirements": ["Product catalog search", "Cart & checkout flow", "Inventory consistency", "Order pipeline"],
        "hints": ["Elasticsearch for search", "Kafka for order events", "Redis for cart"],
        "duration": "40m"
    },
    {
        "id": "social-feed",
        "title": "Design a Social Media Feed",
        "difficulty": "Hard",
        "tags": ["Feed", "Cache", "Fanout"],
        "brief": "Architect a Twitter-style feed handling fanout for users with millions of followers.",
        "requirements": ["Timeline generation", "Fanout on write / read", "Media storage", "Notifications"],
        "hints": ["Pre-compute feeds in cache", "Hybrid fanout strategy", "Object storage for media"],
        "duration": "45m"
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
    },
    {
        "id": "ecommerce-prod",
        "name": "Production E-Commerce Platform",
        "description": "A high-level, production-grade e-commerce system architecture with catalog search, caching, order processing, and payment streaming.",
        "category": "E-Commerce",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 50, "y": 280 }, "data": { "kind": "client", "label": "Web Client", "category": "Client", "replicas": 1 } },
            { "id": "dns", "type": "infra", "position": { "x": 240, "y": 120 }, "data": { "kind": "dns", "label": "DNS", "category": "Network" } },
            { "id": "cdn", "type": "infra", "position": { "x": 240, "y": 420 }, "data": { "kind": "cdn", "label": "CDN Edge", "category": "Network" } },
            { "id": "lb", "type": "infra", "position": { "x": 420, "y": 280 }, "data": { "kind": "load-balancer", "label": "API Gateway / LB", "category": "Network" } },
            { "id": "svc-cat", "type": "infra", "position": { "x": 620, "y": 140 }, "data": { "kind": "web-server", "label": "Catalog Service", "category": "Compute" } },
            { "id": "svc-ord", "type": "infra", "position": { "x": 620, "y": 280 }, "data": { "kind": "web-server", "label": "Order Service", "category": "Compute" } },
            { "id": "svc-pay", "type": "infra", "position": { "x": 620, "y": 420 }, "data": { "kind": "web-server", "label": "Payment Service", "category": "Compute" } },
            { "id": "db-mongo", "type": "infra", "position": { "x": 860, "y": 60 }, "data": { "kind": "mongodb", "label": "MongoDB Catalog", "category": "Data" } },
            { "id": "db-es", "type": "infra", "position": { "x": 860, "y": 160 }, "data": { "kind": "elasticsearch", "label": "Search Index (ES)", "category": "Data" } },
            { "id": "cache-redis", "type": "infra", "position": { "x": 860, "y": 260 }, "data": { "kind": "redis", "label": "Redis Cache", "category": "Data" } },
            { "id": "db-sql", "type": "infra", "position": { "x": 860, "y": 360 }, "data": { "kind": "postgresql", "label": "PostgreSQL Orders", "category": "Data" } },
            { "id": "stream-kafka", "type": "infra", "position": { "x": 860, "y": 460 }, "data": { "kind": "kafka", "label": "Kafka Order Stream", "category": "Data" } },
            { "id": "q-notif", "type": "infra", "position": { "x": 860, "y": 560 }, "data": { "kind": "queue", "label": "Receipt Queue", "category": "Data" } }
        ],
        "edges": [
            { "id": "c-dns", "source": "c", "target": "dns", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "c-cdn", "source": "c", "target": "cdn", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "dns-lb", "source": "dns", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "cdn-lb", "source": "cdn", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-cat", "source": "lb", "target": "svc-cat", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-ord", "source": "lb", "target": "svc-ord", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-pay", "source": "lb", "target": "svc-pay", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "cat-mongo", "source": "svc-cat", "target": "db-mongo", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "cat-es", "source": "svc-cat", "target": "db-es", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "cat-redis", "source": "svc-cat", "target": "cache-redis", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "ord-sql", "source": "svc-ord", "target": "db-sql", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "ord-kafka", "source": "svc-ord", "target": "stream-kafka", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "stream-pay", "source": "stream-kafka", "target": "svc-pay", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "pay-sql", "source": "svc-pay", "target": "db-sql", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "pay-q", "source": "svc-pay", "target": "q-notif", "type": "traffic", "animated": True, "data": { "kind": "database" } }
        ]
    },
    {
        "id": "url-shortener-prod",
        "name": "Production URL Shortener",
        "description": "High-throughput production URL shortener with CDN edge redirect caching, scalable app servers, Redis key-value caching, and database read replication.",
        "category": "Web",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 60, "y": 280 }, "data": { "kind": "client", "label": "Global Users", "category": "Client", "replicas": 1 } },
            { "id": "dns", "type": "infra", "position": { "x": 220, "y": 140 }, "data": { "kind": "dns", "label": "Geo DNS", "category": "Network" } },
            { "id": "cdn", "type": "infra", "position": { "x": 220, "y": 420 }, "data": { "kind": "cdn", "label": "CDN Edge redirects", "category": "Network" } },
            { "id": "lb", "type": "infra", "position": { "x": 380, "y": 280 }, "data": { "kind": "load-balancer", "label": "API Load Balancer", "category": "Network" } },
            { "id": "ws", "type": "infra", "position": { "x": 560, "y": 280 }, "data": { "kind": "web-server", "label": "URL Shortener Servers", "category": "Compute", "replicas": 3 } },
            { "id": "redis", "type": "infra", "position": { "x": 740, "y": 180 }, "data": { "kind": "redis", "label": "Redis Hotkey Cache", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 740, "y": 380 }, "data": { "kind": "postgresql", "label": "Primary DB (Writes)", "category": "Data" } },
            { "id": "db-rep", "type": "infra", "position": { "x": 920, "y": 380 }, "data": { "kind": "postgresql", "label": "Replica DB (Reads)", "category": "Data" } }
        ],
        "edges": [
            { "id": "c-dns", "source": "c", "target": "dns", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "c-cdn", "source": "c", "target": "cdn", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "dns-lb", "source": "dns", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "cdn-lb", "source": "cdn", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-ws", "source": "lb", "target": "ws", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "ws-redis", "source": "ws", "target": "redis", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "ws-db", "source": "ws", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "ws-dbrep", "source": "ws", "target": "db-rep", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "db-sync", "source": "db", "target": "db-rep", "type": "traffic", "animated": True, "data": { "kind": "database" } }
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
        for c in DEFAULT_SYSTEM_DESIGN_CHALLENGES:
            await db.system_design_challenges.update_one({"id": c["id"]}, {"$set": c}, upsert=True)
        cursor = db.system_design_challenges.find({}, {"_id": 0})
        return [c async for c in cursor]

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
        for t in DEFAULT_SYSTEM_DESIGN_TEMPLATES:
            await db.system_design_templates.update_one({"id": t["id"]}, {"$set": t}, upsert=True)
        cursor = db.system_design_templates.find({}, {"_id": 0})
        return [t async for t in cursor]

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
