import json

DOMAINS = ["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]

CHALLENGES = [
    {
        "id": "1",
        "slug": "debounce-event-simulator",
        "title": "Debounce Event Simulator",
        "domain": "Backend",
        "difficulty": "Easy",
        "minutes": 20,
        "xp": 150,
        "completion": 85,
        "tags": ["JavaScript", "Events", "Debounce"],
        "summary": "Simulate a debounce handler and filter events that fire within wait windows.",
        "starter_code": {
            "javascript": (
                "// // DEBOUNCE EVENT SIMULATOR\n"
                "// // Find which events fire after debounce filtering.\n\n"
                "// — Read input (do not modify) —\n"
                "const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());\n\n"
                "/**\n"
                " * Simulate debounce on a list of timestamped events.\n"
                " * Each event in events is { time: number, value: string }\n"
                " */\n"
                "function simulateDebounce(delayMs, events) {\n"
                "  // TODO: Return array of values of events that actually fire.\n"
                "  const fired = [];\n"
                "  return fired;\n"
                "}\n\n"
                "// — Output (do not modify) —\n"
                "console.log(JSON.stringify(simulateDebounce(input.delayMs, input.events)));\n"
            ),
            "python": (
                "# Python Debounce Event Simulator\n"
                "import sys, json\n\n"
                "# — Read input (do not modify) —\n"
                "input_data = json.loads(sys.stdin.read().strip())\n\n"
                "def simulate_debounce(delay_ms, events):\n"
                "    # TODO: Return list of values of events that actually fire.\n"
                "    # Each event is {\"time\": int, \"value\": str}\n"
                "    return []\n\n"
                "# — Output (do not modify) —\n"
                "print(json.dumps(simulate_debounce(input_data[\"delayMs\"], input_data[\"events\"])))\n"
            )
        },
        "test_cases": [
            {
                "id": "debounce-1",
                "problem_slug": "debounce-event-simulator",
                "name": "basic debounce filter",
                "stdin": "{\"delayMs\": 300, \"events\": [{\"time\": 0, \"value\": \"a\"}, {\"time\": 100, \"value\": \"b\"}, {\"time\": 500, \"value\": \"c\"}]}\n",
                "expected_output": "[\"b\",\"c\"]\n",
                "hidden": False,
                "weight": 1,
                "comparison_mode": "exact",
            },
            {
                "id": "debounce-2",
                "problem_slug": "debounce-event-simulator",
                "name": "rapid fire drops all but last",
                "stdin": "{\"delayMs\": 200, \"events\": [{\"time\": 0, \"value\": \"1\"}, {\"time\": 50, \"value\": \"2\"}, {\"time\": 100, \"value\": \"3\"}]}\n",
                "expected_output": "[\"3\"]\n",
                "hidden": False,
                "weight": 1,
                "comparison_mode": "exact",
            }
        ]
    },
    {
        "id": "2",
        "slug": "toast-queue-manager",
        "title": "Toast Notification Queue",
        "domain": "Backend",
        "difficulty": "Medium",
        "minutes": 30,
        "xp": 250,
        "completion": 68,
        "tags": ["Node.js", "Data Structures", "Queue"],
        "summary": "Implement a notification toast manager with capacity and manual dismiss eviction.",
        "starter_code": {
            "javascript": (
                "// // TOAST NOTIFICATION QUEUE\n"
                "// // Manage a capped queue of notification toasts.\n\n"
                "// — Read input (do not modify) —\n"
                "const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());\n\n"
                "class ToastManager {\n"
                "  constructor(maxToasts) {\n"
                "    this.maxToasts = maxToasts;\n"
                "    this.queue = [];\n"
                "  }\n"
                "  add(id) {\n"
                "    // TODO: Add toast ID to queue. If at capacity, evict the oldest first.\n"
                "  }\n"
                "  dismiss(id) {\n"
                "    // TODO: Remove toast by ID if it exists.\n"
                "  }\n"
                "  getActive() {\n"
                "    return this.queue;\n"
                "  }\n"
                "}\n\n"
                "// — Process and output (do not modify) —\n"
                "const manager = new ToastManager(input.maxToasts);\n"
                "for (const cmd of input.commands) {\n"
                "  if (cmd.action === 'add') manager.add(cmd.id);\n"
                "  else if (cmd.action === 'dismiss') manager.dismiss(cmd.id);\n"
                "}\n"
                "console.log(JSON.stringify(manager.getActive()));\n"
            )
        },
        "test_cases": [
            {
                "id": "toast-1",
                "problem_slug": "toast-queue-manager",
                "name": "adds within limit",
                "stdin": "{\"maxToasts\": 3, \"commands\": [{\"action\": \"add\", \"id\": \"t1\"}, {\"action\": \"add\", \"id\": \"t2\"}]}\n",
                "expected_output": "[\"t1\",\"t2\"]\n",
                "hidden": False,
                "weight": 1,
                "comparison_mode": "exact",
            },
            {
                "id": "toast-2",
                "problem_slug": "toast-queue-manager",
                "name": "evicts oldest when full",
                "stdin": "{\"maxToasts\": 2, \"commands\": [{\"action\": \"add\", \"id\": \"t1\"}, {\"action\": \"add\", \"id\": \"t2\"}, {\"action\": \"add\", \"id\": \"t3\"}]}\n",
                "expected_output": "[\"t2\",\"t3\"]\n",
                "hidden": False,
                "weight": 1,
                "comparison_mode": "exact",
            }
        ]
    },
    {
        "id": "3",
        "slug": "simple-click-counter",
        "title": "Simple Click Counter",
        "domain": "Frontend",
        "difficulty": "Easy",
        "minutes": 15,
        "xp": 100,
        "completion": 94,
        "tags": ["HTML", "CSS", "JavaScript"],
        "summary": "Build a responsive button that increments a counter, plus a reset button.",
        "runtime": "frontend",
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Click Counter</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n  <div class=\"card\">\n    <h1>Counter: <span id=\"count\">0</span></h1>\n    <div class=\"buttons\">\n      <button id=\"increment\" class=\"btn primary\">Increment</button>\n      <button id=\"reset\" class=\"btn secondary\">Reset</button>\n    </div>\n  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                  "body {\n  font-family: system-ui, -apple-system, sans-serif;\n  background: #09090b;\n  color: #fafafa;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 100vh;\n  margin: 0;\n}\n.card {\n  background: #18181b;\n  border: 1px solid #27272a;\n  border-radius: 12px;\n  padding: 32px;\n  text-align: center;\n  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);\n}\n.buttons {\n  display: flex;\n  gap: 12px;\n  margin-top: 24px;\n}\n.btn {\n  padding: 10px 20px;\n  border-radius: 8px;\n  border: none;\n  cursor: pointer;\n  font-weight: 600;\n  font-size: 14px;\n  transition: opacity 0.2s;\n}\n.btn:hover {\n  opacity: 0.9;\n}\n.primary {\n  background: #2563eb;\n  color: white;\n}\n.secondary {\n  background: #3f3f46;\n  color: white;\n}"
                ),
                "index.js": (
                  "let count = 0;\nconst countEl = document.getElementById('count');\nconst incBtn = document.getElementById('increment');\nconst resetBtn = document.getElementById('reset');\n\nincBtn.addEventListener('click', () => {\n  // TODO: Increment count and update countEl\n});\n\nresetBtn.addEventListener('click', () => {\n  // TODO: Reset count to 0 and update countEl\n});"
                )
            })
        }
    },
    {
        "id": "4",
        "slug": "responsive-data-table",
        "title": "Responsive Virtualized Data Table",
        "domain": "Frontend",
        "difficulty": "Medium",
        "minutes": 45,
        "xp": 300,
        "completion": 58,
        "tags": ["DOM", "Performance", "CSS"],
        "summary": "Render row items with sorting, filtering, and responsive container wrapping.",
        "runtime": "frontend",
        "starter_code": {
            "html": json.dumps({
                "index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Responsive Virtualized Data Table</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n  <div class=\"wrap\">\n    <h2>Users</h2>\n    <div class=\"toolbar\">\n      <input id=\"q\" placeholder=\"Search...\"/>\n    </div>\n    <table>\n      <thead>\n        <tr>\n          <th>Name</th>\n          <th>Email</th>\n          <th>Role</th>\n          <th>Status</th>\n        </tr>\n      </thead>\n      <tbody id=\"b\"></tbody>\n    </table>\n  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>",
                "index.css": "body {\n  font-family: system-ui, -apple-system, sans-serif;\n  color: #fafafa;\n  background: #09090b;\n  margin: 0;\n  padding: 24px;\n}\n.wrap {\n  max-width: 720px;\n  margin: 0 auto;\n}\n.toolbar {\n  display: flex;\n  gap: 8px;\n  margin-bottom: 12px;\n}\ninput {\n  flex: 1;\n  padding: 8px 10px;\n  border: 1px solid #27272a;\n  border-radius: 8px;\n  font: inherit;\n  background: #18181b;\n  color: #fafafa;\n}\ntable {\n  width: 100%;\n  border-collapse: collapse;\n  font-size: 13px;\n}\nth, td {\n  text-align: left;\n  padding: 10px 12px;\n  border-bottom: 1px solid #27272a;\n}\nth {\n  background: #18181b;\n  color: #a1a1aa;\n}\ntr:hover td {\n  background: #18181b;\n}\n.pill {\n  display: inline-block;\n  padding: 2px 8px;\n  border-radius: 999px;\n  font-size: 11px;\n}\n.ok {\n  background: #dcfce7;\n  color: #166534;\n}\n.warn {\n  background: #fef9c3;\n  color: #854d0e;\n}\n.err {\n  background: #fee2e2;\n  color: #991b1b;\n}",
                "index.js": "const rows = [\n  { name: \"Ada Lovelace\", email: \"ada@interleet.dev\", role: \"Admin\", status: \"ok\" },\n  { name: \"Linus Torvalds\", email: \"linus@interleet.dev\", role: \"Maintainer\", status: \"ok\" },\n  { name: \"Grace Hopper\", email: \"grace@interleet.dev\", role: \"Member\", status: \"warn\" },\n  { name: \"Alan Turing\", email: \"alan@interleet.dev\", role: \"Member\", status: \"err\" },\n  { name: \"Margaret Hamilton\", email: \"margaret@interleet.dev\", role: \"Admin\", status: \"ok\" }\n];\n\nconst b = document.getElementById(\"b\");\nconst q = document.getElementById(\"q\");\n\nfunction render(f) {\n  f = (f || \"\").toLowerCase();\n  b.innerHTML = rows\n    .filter(r => r.name.toLowerCase().includes(f) || r.email.toLowerCase().includes(f))\n    .map(r => `\n      <tr>\n        <td>${r.name}</td>\n        <td>${r.email}</td>\n        <td>${r.role}</td>\n        <td><span class=\"pill ${r.status}\">${r.status}</span></td>\n      </tr>\n    `).join(\"\");\n}\n\nq.addEventListener(\"input\", e => render(e.target.value));\nrender(\"\");"
            })
        }
    },
    {
        "id": "5",
        "slug": "nginx-static-site",
        "title": "Serve a Static Page with Nginx",
        "domain": "DevOps",
        "difficulty": "Easy",
        "minutes": 20,
        "xp": 150,
        "completion": 78,
        "tags": ["Nginx", "DevOps", "Config"],
        "summary": "Configure Nginx to serve an index.html file from /workspace/static/ on port 80.",
        "runtime": "devops",
        "starter_code": {
            "multi": json.dumps({
                "nginx.conf": (
                    "events {}\n"
                    "http {\n"
                    "    server {\n"
                    "        listen 80;\n"
                    "        # TODO: Configure root directory as /workspace/static\n"
                    "        # and serve index.html\n"
                    "    }\n"
                    "}"
                ),
                "static/index.html": "<h1>Hello from Nginx Static Sandbox!</h1>",
                "setup.sh": (
                    "#!/bin/bash\n"
                    "# Start Nginx with the workspace configuration\n"
                    "nginx -c /workspace/nginx.conf"
                )
            })
        },
        "test_cases": [
            {
                "id": "nginx-static-1",
                "problem_slug": "nginx-static-site",
                "name": "Nginx serves index.html on port 80",
                "stdin": "",
                "expected_output": "Hello from Nginx Static Sandbox!\n",
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "exact",
                "verification_script": (
                    "#!/bin/bash\n"
                    "sleep 2\n"
                    "curl -s http://localhost/ | grep -o 'Hello from Nginx Static Sandbox!'\n"
                )
            }
        ]
    },
    {
        "id": "6",
        "slug": "configure-nginx-proxy",
        "title": "Configure Nginx Reverse Proxy",
        "domain": "DevOps",
        "difficulty": "Medium",
        "minutes": 40,
        "xp": 300,
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
                "expected_output": "OK\n",
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "exact",
                "verification_script": "#!/bin/bash\n# Mock backend on port 3000\npython3 -m http.server 3000 &> /dev/null &\nsleep 2\ncurl -s http://localhost/ > /dev/null\nif [ $? -eq 0 ]; then echo \"OK\"; else echo \"FAIL\"; fi\n"
            }
        ]
    },
    {
        "id": "7",
        "slug": "orchestrate-redis-node",
        "title": "Orchestrate Redis + Node API",
        "domain": "DevOps",
        "difficulty": "Medium",
        "minutes": 50,
        "xp": 350,
        "completion": 45,
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
                "expected_output": "OK\n",
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
    }
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
