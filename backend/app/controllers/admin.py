# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from fastapi import HTTPException, BackgroundTasks
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
        "id": "ecommerce",
        "name": "E-Commerce Platform",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 260 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "cdn", "type": "infra", "position": { "x": 260, "y": 140 }, "data": { "kind": "cdn", "label": "CDN", "category": "Network" } },
            { "id": "lb", "type": "infra", "position": { "x": 260, "y": 360 }, "data": { "kind": "load-balancer", "label": "Load Balancer", "category": "Network" } },
            { "id": "gw", "type": "infra", "position": { "x": 500, "y": 360 }, "data": { "kind": "api-gateway", "label": "API Gateway", "category": "Network" } },
            { "id": "svc", "type": "infra", "position": { "x": 740, "y": 260 }, "data": { "kind": "microservice", "label": "Catalog Service", "category": "Application" } },
            { "id": "ord", "type": "infra", "position": { "x": 740, "y": 460 }, "data": { "kind": "microservice", "label": "Order Service", "category": "Application" } },
            { "id": "r", "type": "infra", "position": { "x": 980, "y": 260 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 980, "y": 460 }, "data": { "kind": "postgresql", "label": "PostgreSQL", "category": "Data" } },
            { "id": "q", "type": "infra", "position": { "x": 1220, "y": 360 }, "data": { "kind": "kafka", "label": "Kafka", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-cdn", "source": "c", "target": "cdn", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "c-lb", "source": "c", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-gw", "source": "lb", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-svc", "source": "gw", "target": "svc", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-ord", "source": "gw", "target": "ord", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "svc-r", "source": "svc", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "ord-db", "source": "ord", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "ord-q", "source": "ord", "target": "q", "type": "traffic", "animated": True, "data": { "kind": "queue" } }
        ]
    },
    {
        "id": "url-shortener",
        "name": "URL Shortener",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 60, "y": 280 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "lb", "type": "infra", "position": { "x": 300, "y": 240 }, "data": { "kind": "load-balancer", "label": "LB", "category": "Network" } },
            { "id": "svc", "type": "infra", "position": { "x": 540, "y": 240 }, "data": { "kind": "microservice", "label": "Shortener API", "category": "Application" } },
            { "id": "r", "type": "infra", "position": { "x": 780, "y": 140 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 780, "y": 340 }, "data": { "kind": "postgresql", "label": "Postgres", "category": "Data" } }
        ],
        "edges": [
            { "id": "c-lb", "source": "c", "target": "lb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "lb-svc", "source": "lb", "target": "svc", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "svc-r", "source": "svc", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "svc-db", "source": "svc", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } }
        ]
    },
    {
        "id": "chat",
        "name": "Chat Application",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 240 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 240 }, "data": { "kind": "api-gateway", "label": "Gateway", "category": "Network" } },
            { "id": "ws", "type": "infra", "position": { "x": 500, "y": 240 }, "data": { "kind": "app-server", "label": "WebSocket Server", "category": "Application" } },
            { "id": "svc", "type": "infra", "position": { "x": 740, "y": 140 }, "data": { "kind": "microservice", "label": "Chat Service", "category": "Application" } },
            { "id": "presence", "type": "infra", "position": { "x": 740, "y": 340 }, "data": { "kind": "microservice", "label": "Presence", "category": "Application" } },
            { "id": "r", "type": "infra", "position": { "x": 980, "y": 140 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 980, "y": 340 }, "data": { "kind": "mongodb", "label": "MongoDB", "category": "Data" } },
            { "id": "k", "type": "infra", "position": { "x": 1220, "y": 240 }, "data": { "kind": "kafka", "label": "Kafka", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-ws", "source": "gw", "target": "ws", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "ws-svc", "source": "ws", "target": "svc", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "ws-presence", "source": "ws", "target": "presence", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "svc-r", "source": "svc", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "svc-db", "source": "svc", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "svc-k", "source": "svc", "target": "k", "type": "traffic", "animated": True, "data": { "kind": "event" } }
        ]
    },
    {
        "id": "netflix",
        "name": "Netflix Architecture",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 260 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "cdn", "type": "infra", "position": { "x": 260, "y": 140 }, "data": { "kind": "cdn", "label": "CDN", "category": "Network" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 380 }, "data": { "kind": "api-gateway", "label": "API Gateway", "category": "Network" } },
            { "id": "rec", "type": "infra", "position": { "x": 500, "y": 140 }, "data": { "kind": "microservice", "label": "Recommendations", "category": "Application" } },
            { "id": "play", "type": "infra", "position": { "x": 500, "y": 380 }, "data": { "kind": "microservice", "label": "Playback", "category": "Application" } },
            { "id": "meta", "type": "infra", "position": { "x": 500, "y": 620 }, "data": { "kind": "microservice", "label": "Metadata", "category": "Application" } },
            { "id": "r", "type": "infra", "position": { "x": 760, "y": 140 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 760, "y": 380 }, "data": { "kind": "mongodb", "label": "MongoDB", "category": "Data" } },
            { "id": "es", "type": "infra", "position": { "x": 760, "y": 620 }, "data": { "kind": "elasticsearch", "label": "Elasticsearch", "category": "Data" } },
            { "id": "k", "type": "infra", "position": { "x": 1000, "y": 380 }, "data": { "kind": "kafka", "label": "Kafka", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-cdn", "source": "c", "target": "cdn", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-rec", "source": "gw", "target": "rec", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-play", "source": "gw", "target": "play", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-meta", "source": "gw", "target": "meta", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "rec-r", "source": "rec", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "play-db", "source": "play", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "meta-es", "source": "meta", "target": "es", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "play-k", "source": "play", "target": "k", "type": "traffic", "animated": True, "data": { "kind": "event" } }
        ]
    },
    {
        "id": "instagram",
        "name": "Instagram Architecture",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 260 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "cdn", "type": "infra", "position": { "x": 260, "y": 140 }, "data": { "kind": "cdn", "label": "CDN", "category": "Network" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 380 }, "data": { "kind": "api-gateway", "label": "Gateway", "category": "Network" } },
            { "id": "feed", "type": "infra", "position": { "x": 500, "y": 260 }, "data": { "kind": "microservice", "label": "Feed Service", "category": "Application" } },
            { "id": "media", "type": "infra", "position": { "x": 500, "y": 500 }, "data": { "kind": "microservice", "label": "Media Service", "category": "Application" } },
            { "id": "r", "type": "infra", "position": { "x": 760, "y": 140 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 760, "y": 380 }, "data": { "kind": "postgresql", "label": "Postgres", "category": "Data" } },
            { "id": "k", "type": "infra", "position": { "x": 1000, "y": 260 }, "data": { "kind": "kafka", "label": "Kafka", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-cdn", "source": "c", "target": "cdn", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-feed", "source": "gw", "target": "feed", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-media", "source": "gw", "target": "media", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "feed-r", "source": "feed", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "feed-db", "source": "feed", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "media-k", "source": "media", "target": "k", "type": "traffic", "animated": True, "data": { "kind": "event" } }
        ]
    },
    {
        "id": "uber",
        "name": "Uber Architecture",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 140 }, "data": { "kind": "mobile", "label": "Rider App", "category": "Client" } },
            { "id": "d", "type": "infra", "position": { "x": 40, "y": 380 }, "data": { "kind": "mobile", "label": "Driver App", "category": "Client" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 260 }, "data": { "kind": "api-gateway", "label": "Gateway", "category": "Network" } },
            { "id": "match", "type": "infra", "position": { "x": 500, "y": 140 }, "data": { "kind": "microservice", "label": "Matching", "category": "Application" } },
            { "id": "trip", "type": "infra", "position": { "x": 500, "y": 380 }, "data": { "kind": "microservice", "label": "Trip Service", "category": "Application" } },
            { "id": "r", "type": "infra", "position": { "x": 760, "y": 140 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 760, "y": 380 }, "data": { "kind": "postgresql", "label": "Postgres", "category": "Data" } },
            { "id": "k", "type": "infra", "position": { "x": 1000, "y": 260 }, "data": { "kind": "kafka", "label": "Kafka", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "d-gw", "source": "d", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-match", "source": "gw", "target": "match", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-trip", "source": "gw", "target": "trip", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "match-r", "source": "match", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "trip-db", "source": "trip", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "match-k", "source": "match", "target": "k", "type": "traffic", "animated": True, "data": { "kind": "event" } }
        ]
    },
    {
        "id": "whatsapp",
        "name": "WhatsApp Architecture",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 240 }, "data": { "kind": "mobile", "label": "Client", "category": "Client" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 240 }, "data": { "kind": "api-gateway", "label": "Gateway", "category": "Network" } },
            { "id": "ws", "type": "infra", "position": { "x": 500, "y": 240 }, "data": { "kind": "app-server", "label": "WebSocket", "category": "Application" } },
            { "id": "msg", "type": "infra", "position": { "x": 740, "y": 240 }, "data": { "kind": "microservice", "label": "Message Service", "category": "Application" } },
            { "id": "db", "type": "infra", "position": { "x": 980, "y": 140 }, "data": { "kind": "mongodb", "label": "MongoDB", "category": "Data" } },
            { "id": "q", "type": "infra", "position": { "x": 980, "y": 340 }, "data": { "kind": "queue", "label": "Queue", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-ws", "source": "gw", "target": "ws", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "ws-msg", "source": "ws", "target": "msg", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "msg-db", "source": "msg", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "msg-q", "source": "msg", "target": "q", "type": "traffic", "animated": True, "data": { "kind": "queue" } }
        ]
    },
    {
        "id": "youtube",
        "name": "YouTube Architecture",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 260 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "cdn", "type": "infra", "position": { "x": 260, "y": 140 }, "data": { "kind": "cdn", "label": "CDN", "category": "Network" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 380 }, "data": { "kind": "api-gateway", "label": "Gateway", "category": "Network" } },
            { "id": "up", "type": "infra", "position": { "x": 500, "y": 140 }, "data": { "kind": "microservice", "label": "Upload", "category": "Application" } },
            { "id": "watch", "type": "infra", "position": { "x": 500, "y": 380 }, "data": { "kind": "microservice", "label": "Watch Service", "category": "Application" } },
            { "id": "trans", "type": "infra", "position": { "x": 500, "y": 620 }, "data": { "kind": "microservice", "label": "Transcoder", "category": "Application" } },
            { "id": "db", "type": "infra", "position": { "x": 760, "y": 380 }, "data": { "kind": "mysql", "label": "MySQL", "category": "Data" } },
            { "id": "es", "type": "infra", "position": { "x": 760, "y": 620 }, "data": { "kind": "elasticsearch", "label": "Search", "category": "Data" } },
            { "id": "k", "type": "infra", "position": { "x": 1000, "y": 380 }, "data": { "kind": "kafka", "label": "Kafka", "category": "Messaging" } }
        ],
        "edges": [
            { "id": "c-cdn", "source": "c", "target": "cdn", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-up", "source": "gw", "target": "up", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-watch", "source": "gw", "target": "watch", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "up-trans", "source": "up", "target": "trans", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "watch-db", "source": "watch", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "watch-es", "source": "watch", "target": "es", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "trans-k", "source": "trans", "target": "k", "type": "traffic", "animated": True, "data": { "kind": "event" } }
        ]
    },
    {
        "id": "ai-saas",
        "name": "AI SaaS Platform",
        "nodes": [
            { "id": "c", "type": "infra", "position": { "x": 40, "y": 260 }, "data": { "kind": "client", "label": "Client", "category": "Client" } },
            { "id": "gw", "type": "infra", "position": { "x": 260, "y": 260 }, "data": { "kind": "api-gateway", "label": "Gateway", "category": "Network" } },
            { "id": "orch", "type": "infra", "position": { "x": 500, "y": 260 }, "data": { "kind": "microservice", "label": "Orchestrator", "category": "Application" } },
            { "id": "llm", "type": "infra", "position": { "x": 740, "y": 140 }, "data": { "kind": "llm", "label": "LLM Service", "category": "AI" } },
            { "id": "emb", "type": "infra", "position": { "x": 740, "y": 380 }, "data": { "kind": "embedding", "label": "Embeddings", "category": "AI" } },
            { "id": "vdb", "type": "infra", "position": { "x": 980, "y": 380 }, "data": { "kind": "vector-db", "label": "Vector DB", "category": "AI" } },
            { "id": "r", "type": "infra", "position": { "x": 980, "y": 140 }, "data": { "kind": "redis", "label": "Redis", "category": "Data" } },
            { "id": "db", "type": "infra", "position": { "x": 1220, "y": 260 }, "data": { "kind": "postgresql", "label": "Postgres", "category": "Data" } }
        ],
        "edges": [
            { "id": "c-gw", "source": "c", "target": "gw", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "gw-orch", "source": "gw", "target": "orch", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "orch-llm", "source": "orch", "target": "llm", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "orch-emb", "source": "orch", "target": "emb", "type": "traffic", "animated": True, "data": { "kind": "request" } },
            { "id": "emb-vdb", "source": "emb", "target": "vdb", "type": "traffic", "animated": True, "data": { "kind": "database" } },
            { "id": "orch-r", "source": "orch", "target": "r", "type": "traffic", "animated": True, "data": { "kind": "cache" } },
            { "id": "orch-db", "source": "orch", "target": "db", "type": "traffic", "animated": True, "data": { "kind": "database" } }
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
        new_ids = [t["id"] for t in DEFAULT_SYSTEM_DESIGN_TEMPLATES]
        await db.system_design_templates.delete_many({"id": {"$nin": new_ids}})
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

    @staticmethod
    async def send_mail_campaign(payload: dict, background_tasks: BackgroundTasks):
        from app.utils.email import send_custom_html_email
        import os
        import json

        subject = payload.get("subject")
        html_template = payload.get("html_template")
        test_email = payload.get("test_email")
        target_group = payload.get("target", "all") # "all", "on_platform", "off_platform"

        if not subject or not html_template:
            raise HTTPException(status_code=400, detail="subject and html_template are required")

        async def run_dispatch():
            if test_email:
                html_body = html_template.replace("{{username}}", "Admin (Test)")
                await send_custom_html_email(test_email, subject, html_body)
                return

            targets = []
            seen = set()

            # 1. On-platform users (MongoDB)
            if target_group in ["on_platform", "all"]:
                cursor = db.users.find({"email": {"$exists": True, "$ne": ""}})
                users = [doc async for doc in cursor]
                for user in users:
                    email = user.get("email")
                    if email and email not in seen:
                        seen.add(email)
                        username = user.get("username") or user.get("full_name") or "Engineer"
                        targets.append((email, username))

            # 2. Off-platform candidates (candidates_info.json)
            if target_group in ["off_platform", "all"]:
                root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                candidates_file = os.path.join(root_dir, "candidates_info.json")
                if os.path.exists(candidates_file):
                    try:
                        with open(candidates_file, "r") as f:
                            candidates = json.load(f)
                            for c in candidates:
                                email = c.get("Email") or c.get("email")
                                if email and email not in seen:
                                    seen.add(email)
                                    name = c.get("Name") or c.get("name") or email.split("@")[0].capitalize()
                                    targets.append((email, name))
                    except Exception as e:
                        print(f"Error reading candidates_info.json: {e}")

            print(f"Dispatching campaign '{subject}' to {len(targets)} recipient(s)...")
            for email, uname in targets:
                html_body = html_template.replace("{{username}}", uname)
                await send_custom_html_email(email, subject, html_body)

        background_tasks.add_task(run_dispatch)
        return {
            "success": True,
            "message": f"Mail dispatch campaign ({target_group}) queued successfully in background"
        }

