import json

DOMAINS = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]


CHALLENGES = [
    {
        "id": "1",
        "slug": "build-a-rate-limiter",
        "title": "Build a Token Bucket Rate Limiter",
        "domain": "Backend",
        "difficulty": "Medium",
        "minutes": 45,
        "xp": 320,
        "completion": 64,
        "tags": ["Node.js", "Concurrency", "Redis"],
        "summary": "Implement a thread-safe rate limiter with burst handling and refill logic.",
        "starter_code": {
            "typescript": "export class TokenBucket {\n  constructor(capacity: number, refillPerSec: number) {}\n  allow(): boolean {\n    return false;\n  }\n}\n",
            "javascript": "class TokenBucket {\n  constructor(capacity, refillPerSec) {}\n  allow() {\n    return false;\n  }\n}\nmodule.exports = { TokenBucket };\n",
            "python": "class TokenBucket:\n    def __init__(self, capacity, refill_per_sec):\n        pass\n\n    def allow(self):\n        return False\n",
        },
        "test_cases": [
            {
                "id": "rate-limit-visible-1",
                "problem_slug": "build-a-rate-limiter",
                "name": "allows up to capacity",
                "stdin": "3 1 3\n",
                "expected_output": "true\n",
                "hidden": False,
                "weight": 1,
                "comparison_mode": "semantic",
            },
            {
                "id": "rate-limit-visible-2",
                "problem_slug": "build-a-rate-limiter",
                "name": "rejects burst overflow",
                "stdin": "3 1 4\n",
                "expected_output": "false\n",
                "hidden": False,
                "weight": 1,
                "comparison_mode": "semantic",
            },
            {
                "id": "rate-limit-hidden-1",
                "problem_slug": "build-a-rate-limiter",
                "name": "handles zero refill",
                "stdin": "10 0 11\n",
                "expected_output": "false\n",
                "hidden": True,
                "weight": 2,
                "comparison_mode": "semantic",
            },
        ],
    },
    {
        "id": "2",
        "slug": "responsive-data-table",
        "title": "Responsive Virtualized Data Table",
        "domain": "Frontend",
        "difficulty": "Hard",
        "minutes": 90,
        "xp": 540,
        "completion": 38,
        "tags": ["React", "Performance", "Accessibility"],
        "summary": "Render 100k rows with sticky headers, sorting, and keyboard navigation.",
        "is_premium": True,
        "runtime": "frontend",
        "starter_code": {
            "html": json.dumps({
                "index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Responsive Virtualized Data Table</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n  <div class=\"wrap\">\n    <h2>Users</h2>\n    <div class=\"toolbar\">\n      <input id=\"q\" placeholder=\"Search...\"/>\n    </div>\n    <table>\n      <thead>\n        <tr>\n          <th>Name</th>\n          <th>Email</th>\n          <th>Role</th>\n          <th>Status</th>\n        </tr>\n      </thead>\n      <tbody id=\"b\"></tbody>\n    </table>\n  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>",
                "index.css": "body {\n  font-family: system-ui, -apple-system, sans-serif;\n  color: #fafafa;\n  background: #09090b;\n  margin: 0;\n  padding: 24px;\n}\n.wrap {\n  max-width: 720px;\n  margin: 0 auto;\n}\n.toolbar {\n  display: flex;\n  gap: 8px;\n  margin-bottom: 12px;\n}\ninput {\n  flex: 1;\n  padding: 8px 10px;\n  border: 1px solid #27272a;\n  border-radius: 8px;\n  font: inherit;\n  background: #18181b;\n  color: #fafafa;\n}\ntable {\n  width: 100%;\n  border-collapse: collapse;\n  font-size: 13px;\n}\nth, td {\n  text-align: left;\n  padding: 10px 12px;\n  border-bottom: 1px solid #27272a;\n}\nth {\n  background: #18181b;\n  color: #a1a1aa;\n}\ntr:hover td {\n  background: #18181b;\n}\n.pill {\n  display: inline-block;\n  padding: 2px 8px;\n  border-radius: 999px;\n  font-size: 11px;\n}\n.ok {\n  background: #dcfce7;\n  color: #166534;\n}\n.warn {\n  background: #fef9c3;\n  color: #854d0e;\n}\n.err {\n  background: #fee2e2;\n  color: #991b1b;\n}",
                "index.js": "const rows = [\n  { name: \"Ada Lovelace\", email: \"ada@interleet.dev\", role: \"Admin\", status: \"ok\" },\n  { name: \"Linus Torvalds\", email: \"linus@interleet.dev\", role: \"Maintainer\", status: \"ok\" },\n  { name: \"Grace Hopper\", email: \"grace@interleet.dev\", role: \"Member\", status: \"warn\" },\n  { name: \"Alan Turing\", email: \"alan@interleet.dev\", role: \"Member\", status: \"err\" },\n  { name: \"Margaret Hamilton\", email: \"margaret@interleet.dev\", role: \"Admin\", status: \"ok\" }\n];\n\nconst b = document.getElementById(\"b\");\nconst q = document.getElementById(\"q\");\n\nfunction render(f) {\n  f = (f || \"\").toLowerCase();\n  b.innerHTML = rows\n    .filter(r => r.name.toLowerCase().includes(f) || r.email.toLowerCase().includes(f))\n    .map(r => `\n      <tr>\n        <td>${r.name}</td>\n        <td>${r.email}</td>\n        <td>${r.role}</td>\n        <td><span class=\"pill ${r.status}\">${r.status}</span></td>\n      </tr>\n    `).join(\"\");\n}\n\nq.addEventListener(\"input\", e => render(e.target.value));\nrender(\"\");"
            })
        },
    },
    {
        "id": "3",
        "slug": "configure-nginx-proxy",
        "title": "Configure Nginx Reverse Proxy",
        "domain": "DevOps",
        "difficulty": "Medium",
        "minutes": 60,
        "xp": 380,
        "completion": 52,
        "tags": ["Nginx", "Linux", "Networking"],
        "summary": "Configure Nginx to reverse proxy traffic to a local backend on port 3000.",
        "runtime": "devops",
        "starter_code": {
            "multi": json.dumps({
                "nginx.conf": "server {\n    listen 80;\n    # Your proxy_pass configuration here\n}",
                "setup.sh": "#!/bin/bash\n# Install nginx and move your configuration file\n"
            })
        },
        "test_cases": [
            {
                "id": "nginx-proxy-1",
                "problem_slug": "configure-nginx-proxy",
                "name": "Nginx responds with proxy pass",
                "stdin": "",
                "expected_output": "OK\\n",
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "exact",
                "verification_script": "#!/bin/bash\n# Mock backend on port 3000\npython3 -m http.server 3000 &> /dev/null &\nsleep 2\ncurl -s http://localhost/ > /dev/null\nif [ $? -eq 0 ]; then echo \"OK\"; else echo \"FAIL\"; fi\n"
            }
        ]
    },
    {
        "id": "101",
        "slug": "orchestrate-redis-node",
        "title": "Orchestrate Redis + Node API",
        "domain": "System Design",
        "difficulty": "Hard",
        "minutes": 120,
        "xp": 600,
        "completion": 25,
        "tags": ["Docker Compose", "Redis", "Node.js"],
        "summary": "Write a docker-compose.yml to orchestrate a Node.js API and a Redis cache.",
        "runtime": "compose",
        "starter_code": {
            "multi": json.dumps({
                "docker-compose.yml": "version: '3.8'\nservices:\n  # Add your services here\n"
            })
        },
        "test_cases": [
            {
                "id": "compose-redis-1",
                "problem_slug": "orchestrate-redis-node",
                "name": "Services are up and responding",
                "stdin": "",
                "expected_output": "OK\\n",
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "exact",
                "verification_script": "#!/bin/bash\n# Wait for services\nsleep 5\ncurl -s http://localhost:8080/health > /dev/null\nif [ $? -eq 0 ]; then echo \"OK\"; else echo \"FAIL\"; fi\n",
                "files": {
                    "server.js": "const http = require('http');\nhttp.createServer((req, res) => { res.writeHead(200); res.end('OK'); }).listen(8080);\n",
                    "Dockerfile": "FROM node:20-alpine\nWORKDIR /app\nCOPY server.js .\nCMD [\"node\", \"server.js\"]\n"
                }
            }
        ]
    },

    {
        "id": "5",
        "slug": "rest-versioning",
        "title": "Versioning a Public REST API",
        "domain": "APIs",
        "difficulty": "Easy",
        "minutes": 30,
        "xp": 180,
        "completion": 78,
        "tags": ["REST", "Backward-compat"],
        "summary": "Choose a versioning strategy and migrate a v1 client smoothly to v2.",
    },
    {
        "id": "6",
        "slug": "indexing-strategy",
        "title": "Postgres Indexing Strategy",
        "domain": "Databases",
        "difficulty": "Medium",
        "minutes": 40,
        "xp": 280,
        "completion": 56,
        "tags": ["Postgres", "EXPLAIN", "B-tree"],
        "summary": "Reduce a 12s analytics query to under 200ms using the right indexes.",
    },
    {
        "id": "7",
        "slug": "feature-flag-service",
        "title": "Build a Feature Flag Service",
        "domain": "Backend",
        "difficulty": "Hard",
        "minutes": 90,
        "xp": 560,
        "completion": 34,
        "tags": ["Streaming", "SDKs", "Targeting"],
        "summary": "Realtime flag evaluation with audience targeting and rollouts.",
    },
    {
        "id": "8",
        "slug": "k8s-blue-green",
        "title": "Blue/Green Deploy on Kubernetes",
        "domain": "DevOps",
        "difficulty": "Expert",
        "minutes": 120,
        "xp": 820,
        "completion": 18,
        "tags": ["Kubernetes", "Helm", "Rollouts"],
        "summary": "Zero-downtime release with automated rollback on SLO breach.",
        "is_premium": True,
    },
    {
        "id": "9",
        "slug": "ssr-cache-strategy",
        "title": "SSR Cache Strategy for an E-commerce App",
        "domain": "Frontend",
        "difficulty": "Medium",
        "minutes": 60,
        "xp": 360,
        "completion": 47,
        "tags": ["Next.js", "ISR", "Edge"],
        "summary": "Cache product pages with personalization and inventory accuracy.",
        "runtime": "frontend",
        "starter_code": {
            "html": json.dumps({
                "index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>SSR Cache Strategy Preview</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n  <h2>SSR Cache Preview</h2>\n  <div class=\"card\">\n    <div class=\"row\">\n      <span>GET /products</span>\n      <span id=\"s1\" class=\"ok\">HIT · 4ms</span>\n    </div>\n    <div class=\"row\">\n      <span>GET /products/42</span>\n      <span id=\"s2\" class=\"miss\">MISS · 218ms</span>\n    </div>\n    <div class=\"row\">\n      <span>GET /search?q=shoe</span>\n      <span id=\"s3\" class=\"ok\">HIT · 6ms</span>\n    </div>\n  </div>\n  <button onclick=\"bust()\">Bust cache</button>\n\n  <script src=\"index.js\"></script>\n</body>\n</html>",
                "index.css": "body {\n  font-family: system-ui, -apple-system, sans-serif;\n  color: #fafafa;\n  background: #09090b;\n  margin: 0;\n  padding: 24px;\n}\n.card {\n  border: 1px solid #27272a;\n  border-radius: 10px;\n  padding: 14px;\n  margin-bottom: 10px;\n  background: #18181b;\n}\n.row {\n  display: flex;\n  justify-content: space-between;\n  font-family: monospace;\n  font-size: 12px;\n  padding: 4px 0;\n}\n.ok {\n  color: #10b981;\n}\n.miss {\n  color: #ef4444;\n}\nbutton {\n  padding: 8px 12px;\n  border: 1px solid #27272a;\n  background: #27272a;\n  color: #fff;\n  border-radius: 8px;\n  cursor: pointer;\n}\nbutton:hover {\n  background: #3f3f46;\n}",
                "index.js": "function bust() {\n  [\"s1\", \"s2\", \"s3\"].forEach(id => {\n    const el = document.getElementById(id);\n    el.textContent = \"MISS · \" + (180 + Math.floor(Math.random() * 120)) + \"ms\";\n    el.className = \"miss\";\n  });\n}"
            })
        },
    },
]


LEADERBOARD = [
    {"rank": 1, "username": "amelia.dev", "rating": 2843, "xp": 184200, "country": "US", "delta": 24, "badges": ["Top 1%", "DevOps"]},
    {"rank": 2, "username": "kenji_w", "rating": 2790, "xp": 172480, "country": "JP", "delta": 12, "badges": ["Top 1%"]},
    {"rank": 3, "username": "priya.s", "rating": 2755, "xp": 168120, "country": "IN", "delta": -3, "badges": ["Backend"]},
    {"rank": 4, "username": "lucasf", "rating": 2710, "xp": 161300, "country": "BR", "delta": 8, "badges": ["System Design"]},
    {"rank": 5, "username": "noor.k", "rating": 2682, "xp": 158020, "country": "AE", "delta": 5, "badges": ["APIs"]},
    {"rank": 6, "username": "aria.j", "rating": 2654, "xp": 152410, "country": "KR", "delta": 0, "badges": ["Frontend"]},
]


USER_PROFILE = {
    "name": "Alex Morgan",
    "username": "alex.morgan",
    "title": "Senior Software Engineer",
    "location": "Berlin, DE",
    "rating": 2184,
    "rank": 327,
    "xp": 48210,
    "streak": 28,
    "accuracy": 86,
    "solved": 184,
    "interviews": 14,
    "badges": ["Top 5% Backend", "100-Day Streak", "System Design I", "API Architect"],
    "domains": [
        {"domain": "Frontend", "score": 72},
        {"domain": "Backend", "score": 91},
        {"domain": "DevOps", "score": 68},
        {"domain": "APIs", "score": 84},
        {"domain": "Databases", "score": 76},
        {"domain": "System Design", "score": 80},
    ],
}


ACTIVITY_WEEKLY = [
    {"day": "Mon", "solved": 3, "minutes": 75},
    {"day": "Tue", "solved": 5, "minutes": 110},
    {"day": "Wed", "solved": 2, "minutes": 50},
    {"day": "Thu", "solved": 6, "minutes": 140},
    {"day": "Fri", "solved": 4, "minutes": 95},
    {"day": "Sat", "solved": 7, "minutes": 180},
    {"day": "Sun", "solved": 5, "minutes": 130},
]


RECENT_ACTIVITY = [
    {"type": "solved", "text": "Solved Postgres Indexing Strategy", "when": "2h ago", "domain": "Databases"},
    {"type": "interview", "text": "Completed AI Interview - Senior Backend", "when": "1d ago", "domain": "Backend"},
    {"type": "badge", "text": "Earned 100-Day Streak badge", "when": "2d ago", "domain": "-"},
    {"type": "contest", "text": "Placed #18 in Weekly Engineering Cup", "when": "4d ago", "domain": "System Design"},
]


INTERVIEW_HISTORY = [
    {"id": "iv-21", "role": "Senior Backend", "score": 84, "when": "1d ago", "duration": 42},
    {"id": "iv-20", "role": "System Design (L5)", "score": 78, "when": "5d ago", "duration": 55},
    {"id": "iv-19", "role": "Frontend Architect", "score": 71, "when": "12d ago", "duration": 48},
]


SYSTEM_DESIGN_TOPICS = [
    {"title": "Scalability", "items": ["Vertical vs horizontal", "Load balancers", "Stateless services", "Backpressure"]},
    {"title": "Caching", "items": ["CDN strategy", "Read-through / write-back", "Cache invalidation", "Hot keys"]},
    {"title": "Databases", "items": ["Sharding", "Replication", "CAP & consistency", "Indexing for scale"]},
    {"title": "Distributed Systems", "items": ["Consensus", "Idempotency", "Event sourcing", "Sagas"]},
]


CANDIDATES = [
    {"name": "Jordan Lee", "username": "jlee", "rating": 2410, "top": "Backend", "verified": True, "location": "NYC"},
    {"name": "Maya Chen", "username": "mchen", "rating": 2356, "top": "System Design", "verified": True, "location": "SF"},
    {"name": "Ravi Shankar", "username": "rshankar", "rating": 2298, "top": "DevOps", "verified": True, "location": "Bengaluru"},
    {"name": "Sofia Romero", "username": "sromero", "rating": 2244, "top": "Frontend", "verified": False, "location": "Madrid"},
]
