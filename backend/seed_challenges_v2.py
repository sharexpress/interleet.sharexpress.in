import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "interleet"

CHALLENGES = [
    # ─────────────────────────── Backend ──────────────────────────────────────
    {
        "title": "Debounce Event Simulator",
        "slug": "debounce-event-simulator",
        "short_description": "Simulate a debounce handler and filter events that fire within wait windows.",
        "description": "### Debounce Event Simulator\n\nImplement a debounce event simulator that takes a delay window `delayMs` and a list of timestamped events, returning only the values of the events that actually fire after applying the debounce filter.\n\nUnder debounce, a function call is postponed until after `delayMs` milliseconds have elapsed since the last time it was invoked.\n\n### Input Format\nA JSON object via stdin:\n```json\n{\n  \"delayMs\": 300,\n  \"events\": [\n    {\"time\": 0, \"value\": \"a\"},\n    {\"time\": 100, \"value\": \"b\"},\n    {\"time\": 500, \"value\": \"c\"}\n  ]\n}\n```\n\n### Output Format\nA JSON array printed to stdout containing the values of the triggered events.",
        "domain": "Backend",
        "difficulty": "Easy",
        "tags": ["JavaScript", "Events", "Debounce"],
        "technologies": ["javascript", "python"],
        "hints": [
            "Keep track of the last event time.",
            "An event fires if no other event occurs within delayMs after it."
        ],
        "concepts": ["Asynchronous Programming", "Event Loop"],
        "runtime": "algorithm",
        "execution_mode": "cli",
        "xp_reward": 150,
        "estimated_time_minutes": 20,
        "starter_code": {
            "javascript": """// JavaScript Debounce Event Simulator - Skeletal Stub
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0, 'utf-8').trim());

function simulateDebounce(delayMs, events) {
    // TODO: Implement the debounce event simulator logic.
    // Return only the values of the events that actually fire.
    return [];
}

console.log(JSON.stringify(simulateDebounce(input.delayMs, input.events)));
""",
            "python": """# Python Debounce Event Simulator - Skeletal Stub
import sys
import json

def simulate_debounce(delay_ms, events):
    # TODO: Implement the debounce event simulator logic.
    # Return only the values of the events that actually fire.
    return []

if __name__ == '__main__':
    data = json.loads(sys.stdin.read().strip())
    result = simulate_debounce(data['delayMs'], data['events'])
    print(json.dumps(result))
"""
        },
        "test_cases": [
            {
                "id": "debounce-tc-1",
                "name": "basic debounce filtering",
                "stdin": json.dumps({"delayMs": 300, "events": [{"time": 0, "value": "a"}, {"time": 100, "value": "b"}, {"time": 500, "value": "c"}]}),
                "expected_output": '["b","c"]\n',
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    # ─────────────────────────── Backend ──────────────────────────────────────
    {
        "title": "LRU Cache Implementation",
        "slug": "lru-cache",
        "short_description": "Design and implement a Least Recently Used (LRU) cache with O(1) operations.",
        "description": "### LRU Cache\n\nImplement an LRU cache with the following API:\n- `LRUCache(capacity)` — initialize with positive integer `capacity`\n- `get(key)` — return the cached value or `-1` if not found\n- `put(key, value)` — insert/update the entry, evicting the least recently used entry when capacity is exceeded\n\nBoth operations must run in **O(1)** time.\n\n### Input Format (stdin)\nA JSON object:\n```json\n{\n  \"capacity\": 2,\n  \"operations\": [[\"put\",1,1],[\"put\",2,2],[\"get\",1],[\"put\",3,3],[\"get\",2],[\"get\",3]]\n}\n```\n\n### Output Format\nA JSON array of results from `get` calls only (skip `put`).",
        "domain": "Backend",
        "difficulty": "Medium",
        "tags": ["Data Structures", "Hash Map", "Linked List"],
        "technologies": ["javascript", "python"],
        "hints": [
            "Use a HashMap combined with a Doubly Linked List.",
            "Move accessed nodes to the front on every get/put.",
        ],
        "concepts": ["Caching", "Data Structures", "Complexity"],
        "runtime": "algorithm",
        "execution_mode": "cli",
        "xp_reward": 200,
        "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": """// JavaScript LRU Cache
const fs = require('fs');
const { capacity, operations } = JSON.parse(fs.readFileSync(0, 'utf-8').trim());

class LRUCache {
    constructor(capacity) {
        this.cap = capacity;
        // TODO: Initialize your data structures
    }
    get(key) {
        // TODO: Return value for key or -1
        return -1;
    }
    put(key, value) {
        // TODO: Insert/update key-value, evict LRU if needed
    }
}

const cache = new LRUCache(capacity);
const results = [];
for (const [op, ...args] of operations) {
    if (op === 'get') results.push(cache.get(args[0]));
    else cache.put(args[0], args[1]);
}
console.log(JSON.stringify(results));
""",
            "python": """# Python LRU Cache
import sys, json

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        # TODO: Initialize your data structures

    def get(self, key: int) -> int:
        # TODO: Return value for key or -1
        return -1

    def put(self, key: int, value: int) -> None:
        # TODO: Insert/update key-value, evict LRU if needed
        pass

if __name__ == '__main__':
    data = json.loads(sys.stdin.read().strip())
    cache = LRUCache(data['capacity'])
    results = []
    for op in data['operations']:
        if op[0] == 'get':
            results.append(cache.get(op[1]))
        else:
            cache.put(op[1], op[2])
    print(json.dumps(results))
"""
        },
        "test_cases": [
            {
                "id": "lru-tc-1",
                "name": "basic eviction",
                "stdin": json.dumps({"capacity": 2, "operations": [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2], ["get", 3]]}),
                "expected_output": "[1,-1,3]\n",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    # ─────────────────────────── Frontend ─────────────────────────────────────
    {
        "title": "Simple Click Counter",
        "slug": "simple-click-counter",
        "short_description": "Build a responsive button that increments a counter, plus a reset button.",
        "description": "### Simple Click Counter\n\nBuild a basic interactive user interface containing:\n- A header text showing the current click count (starting at 0).\n- An 'Increment' button that increases the count.\n- A 'Reset' button that sets the count back to 0.",
        "domain": "Frontend",
        "difficulty": "Easy",
        "tags": ["HTML", "CSS", "JavaScript"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use document.getElementById() to link buttons to click handlers."],
        "concepts": ["DOM Manipulation", "Event Listeners"],
        "runtime": "frontend",
        "execution_mode": "browser",
        "xp_reward": 100,
        "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Click Counter</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n  <div class=\"card\">\n    <h1>Counter: <span id=\"count\">0</span></h1>\n    <div class=\"buttons\">\n      <button id=\"increment\" class=\"btn primary\">Increment</button>\n      <button id=\"reset\" class=\"btn secondary\">Reset</button>\n    </div>\n  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>",
                "index.css": "body {\n  font-family: system-ui, sans-serif;\n  background: #09090b;\n  color: #fafafa;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 100vh;\n  margin: 0;\n}\n.card {\n  background: #18181b;\n  border: 1px solid #27272a;\n  border-radius: 12px;\n  padding: 32px;\n  text-align: center;\n}\n.buttons {\n  display: flex;\n  gap: 12px;\n  margin-top: 24px;\n}\n.btn {\n  padding: 10px 20px;\n  border-radius: 8px;\n  border: none;\n  cursor: pointer;\n  font-weight: 600;\n}\n.primary {\n  background: #2563eb;\n  color: white;\n}\n.secondary {\n  background: #3f3f46;\n  color: white;\n}",
                "index.js": "// Write your event handler code here\n// TODO: Select the #count, #increment, and #reset elements\n// TODO: Implement click event listeners to increment and reset the counter"
            })
        },
        "test_cases": [
            {
                "id": "click-counter-tc-1",
                "name": "Increment button increases counter",
                "stdin": json.dumps({
                    "evaluation": "const incBtn = document.getElementById('increment'); const countSpan = document.getElementById('count'); if (!incBtn || !countSpan) return 'FAIL: missing elements'; for (let i = 0; i < 3; i++) incBtn.click(); const count = countSpan.textContent.trim(); return count === '3' ? 'PASS' : 'FAIL: expected 3 got ' + count;"
                }),
                "expected_output": "PASS\n",
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "exact"
            }
        ]
    },
    # ─────────────────────────── DevOps ───────────────────────────────────────
    {
        "title": "Serve Nginx Static Site",
        "slug": "serve-nginx-static",
        "short_description": "Configure Nginx to serve an index.html file from /workspace/static/ on port 80.",
        "description": "### Serve Nginx Static Site\n\nWrite an Nginx configuration file (`nginx.conf`) that listens on port `80` and serves the contents of `/workspace/static/index.html` as the default landing page.",
        "domain": "DevOps",
        "difficulty": "Easy",
        "tags": ["Nginx", "DevOps", "Config"],
        "technologies": ["nginx", "bash"],
        "concepts": ["Web Servers", "Configuration Management"],
        "runtime": "devops",
        "execution_mode": "devops",
        "xp_reward": 150,
        "estimated_time_minutes": 20,
        "starter_code": {
            "multi": json.dumps({
                "nginx.conf": "# TODO: Configure Nginx server to run on port 80 and serve /workspace/static",
                "static/index.html": "<h1>Hello from Nginx Static Sandbox!</h1>",
                "setup.sh": "#!/bin/bash\nnginx -c /workspace/nginx.conf"
            })
        },
        "test_cases": [
            {
                "id": "nginx-static-tc-1",
                "name": "Nginx serves static page on port 80",
                "stdin": "",
                "expected_output": "Hello from Nginx Static Sandbox!\n",
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "exact",
                "verification_script": "#!/bin/bash\nsleep 2\ncurl -s http://localhost/ | grep -o 'Hello from Nginx Static Sandbox!'"
            }
        ]
    },
    # ─────────────────────────── APIs ─────────────────────────────────────────
    {
        "title": "Build a Task Manager API",
        "slug": "task-manager-api",
        "short_description": "Build a RESTful CRUD Task API backed by MongoDB or SQLite.",
        "description": "### Task Manager API\n\nBuild a RESTful API inside the sandbox representing a simple Task Manager. You can use **MongoDB** (default), SQLite, PostgreSQL, or MySQL as the backing database.\n\nEndpoints:\n- `GET /health` responding with status `200` and body `{\"status\": \"ok\"}`\n- `GET /tasks` listing all task rows\n- `POST /tasks` adding a task row\n\nExamples\n\nHealth check responds with ok\n\nInput: `[{\"method\": \"GET\", \"path\": \"/health\"}]`\nOutput: `[{\"request\": {\"method\": \"GET\", \"path\": \"/health\"}, \"response\": {\"status\": 200, \"headers\": {}, \"body\": {\"status\": \"ok\"}}}]`",
        "domain": "APIs",
        "difficulty": "Medium",
        "tags": ["REST", "Express.js", "MongoDB", "FastAPI", "SQLite"],
        "technologies": ["javascript", "python", "mongodb", "sqlite"],
        "concepts": ["RESTful Design", "Database Integration"],
        "runtime": "api",
        "execution_mode": "http",
        "xp_reward": 300,
        "estimated_time_minutes": 45,
        "starter_code": {
            # MongoDB first = auto-detected as default DB by the editor
            "js_mongodb": json.dumps({
                "solution.js": """const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
app.use(express.json());

const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');
let db;

client.connect().then(() => {
    db = client.db('tasks_db');
});

// TODO: Implement GET /health
// app.get('/health', (req, res) => { res.json({ status: 'ok' }); });

// TODO: Implement GET /tasks
// app.get('/tasks', async (req, res) => { const tasks = await db.collection('tasks').find({}).toArray(); res.json(tasks); });

// TODO: Implement POST /tasks
// app.post('/tasks', async (req, res) => { const { title, description } = req.body; ... });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
"""
            }),
            "py_mongodb": json.dumps({
                "solution.py": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os

app = FastAPI()
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))
db = client['tasks_db']

# TODO: Implement GET /health
# @app.get('/health')
# def health():
#     return {'status': 'ok'}

# TODO: Implement GET /tasks
# @app.get('/tasks')
# def get_tasks():
#     tasks = list(db.tasks.find({}))
#     return [{'id': str(t['_id']), **{k: v for k, v in t.items() if k != '_id'}} for t in tasks]

# TODO: Implement POST /tasks
# class TaskCreate(BaseModel):
#     title: str
#     description: str | None = None
# @app.post('/tasks', status_code=201)
# def create_task(task: TaskCreate):
#     ...

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
            }),
            "go_mongodb": json.dumps({
                "main.go": """package main

import (
\t"context"
\t"os"
\t"github.com/gin-gonic/gin"
\t"go.mongodb.org/mongo-driver/mongo"
\t"go.mongodb.org/mongo-driver/mongo/options"
)

var collection *mongo.Collection

// TODO: Initialize MongoDB connection and implement routes

func main() {
\tctx := context.Background()
\tmongoURI := os.Getenv("MONGO_URI")
\tif mongoURI == "" { mongoURI = "mongodb://localhost:27017" }
\tclient, _ := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
\tcollection = client.Database("tasks_db").Collection("tasks")

\tr := gin.Default()
\t// r.GET("/health", func(c *gin.Context) { c.JSON(200, gin.H{"status": "ok"}) })

\tport := os.Getenv("PORT")
\tif port == "" { port = "3000" }
\tr.Run("127.0.0.1:" + port)
}
"""
            }),
            # SQLite variants as alternates
            "js_sqlite": json.dumps({
                "solution.js": """const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
app.use(express.json());

const db = new sqlite3.Database('db.sqlite');

// TODO: Implement GET /health
// app.get('/health', (req, res) => { res.json({ status: 'ok' }); });

// TODO: Implement GET /tasks
// app.get('/tasks', (req, res) => { db.all('SELECT * FROM tasks', [], (err, rows) => res.json(rows)); });

// TODO: Implement POST /tasks
// app.post('/tasks', (req, res) => { ... });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
"""
            }),
            "py_sqlite": json.dumps({
                "solution.py": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

def get_db():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# TODO: Implement GET /health
# @app.get('/health')
# def health():
#     return {'status': 'ok'}

# TODO: Implement GET /tasks + POST /tasks

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
            })
        },
        "test_cases": [
            {
                "id": "task-api-tc-1",
                "name": "Health check responds with ok",
                "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
                "expected_output": json.dumps([{
                    "request": {"method": "GET", "path": "/health"},
                    "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}
                }]),
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "json"
                # No seed.sql — MongoDB doesn't need SQL seeding
            }
        ]
    },
    # ─────────────────────────── DevOps ───────────────────────────────────────
    {
        "title": "Parse Semantic Versions (SemVer)",
        "slug": "parse-semver",
        "short_description": "Compare two semantic versions and return the precedence ordering.",
        "description": "### Parse Semantic Versions\n\nImplement a function comparing two semantic version strings `v1` and `v2`. Return `1` if `v1 > v2`, `-1` if `v1 < v2`, and `0` if they are equal.",
        "domain": "DevOps",
        "difficulty": "Easy",
        "tags": ["SemVer", "Strings"],
        "technologies": ["javascript", "python"],
        "concepts": ["Semantic Versioning", "Parsing"],
        "runtime": "algorithm",
        "execution_mode": "cli",
        "xp_reward": 120,
        "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": """const fs = require('fs');
const input = fs.readFileSync(0, 'utf-8').trim().split(' ');

function compareSemVer(v1, v2) {
    // TODO: Compare two semantic version strings
    return 0;
}

console.log(compareSemVer(input[0], input[1]));
""",
            "python": """import sys

def compare_semver(v1, v2):
    # TODO: Compare two semantic version strings
    return 0

if __name__ == '__main__':
    v = sys.stdin.read().strip().split()
    if len(v) >= 2:
        print(compare_semver(v[0], v[1]))
"""
        },
        "test_cases": [
            {
                "id": "semver-tc-1",
                "name": "basic major comparison",
                "stdin": "1.2.3 2.0.0",
                "expected_output": "-1\n",
                "hidden": False,
                "weight": 1
            }
        ]
    },
    # ─────────────────────────── Databases ────────────────────────────────────
    {
        "title": "Parse SQL SELECT Statement",
        "slug": "parse-sql-select",
        "short_description": "Extract target columns from a standard SQL SELECT statement.",
        "description": "### Parse SQL SELECT Statement\n\nExtract and return a list of projected column names from a standard SQL query string. Handles comma separation, spaces, and optionally alias definitions (`AS col_alias`).\n\n### Examples\nInput: `SELECT name, age FROM users`  \nOutput: `[\"name\",\"age\"]`\n\nInput: `SELECT first_name AS name, score FROM students`  \nOutput: `[\"first_name\",\"score\"]` (always extract the original source columns)",
        "domain": "Databases",
        "difficulty": "Medium",
        "tags": ["Databases", "SQL Parser", "Regex"],
        "technologies": ["javascript", "python"],
        "concepts": ["Lexical Analysis", "Syntax Parsing"],
        "runtime": "algorithm",
        "execution_mode": "cli",
        "xp_reward": 200,
        "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": """const fs = require('fs');
const sqlQuery = fs.readFileSync(0, 'utf-8').trim();

function parseSqlColumns(query) {
    // TODO: Extract target column names from the SELECT statement.
    // E.g. SELECT first_name AS name, score FROM students -> ["first_name", "score"]
    return [];
}

console.log(JSON.stringify(parseSqlColumns(sqlQuery)));
""",
            "python": """import sys
import json

def parse_sql_columns(query):
    # TODO: Extract target column names from the SELECT statement.
    # E.g. SELECT first_name AS name, score FROM students -> ["first_name", "score"]
    return []

if __name__ == '__main__':
    query = sys.stdin.read().strip()
    print(json.dumps(parse_sql_columns(query)))
"""
        },
        "test_cases": [
            {
                "id": "sql-select-tc-1",
                "name": "simple query parsing",
                "stdin": "SELECT name, age FROM users",
                "expected_output": '[\"name\",\"age\"]\n',
                "hidden": False,
                "weight": 1
            },
            {
                "id": "sql-select-tc-2",
                "name": "query with aliases",
                "stdin": "SELECT first_name AS name, score FROM students",
                "expected_output": '[\"first_name\",\"score\"]\n',
                "hidden": False,
                "weight": 1
            }
        ]
    },
    # ─────────────────────────── Fullstack ────────────────────────────────────
    {
        "title": "Realtime Bid Auctions Engine",
        "slug": "realtime-bid-auctions",
        "short_description": "Implement a real-time event-driven auction coordinator routing bid submissions.",
        "description": "### Realtime Bid Auctions Engine\n\nBuild an auction HTTP API to coordinate bids under constraints:\n- `POST /auctions` Create an auction with a start price.\n- `POST /auctions/:id/bids` Submit a higher bid. Return `200` if successful, or `400` if the bid is too low or invalid.",
        "domain": "Fullstack",
        "difficulty": "Hard",
        "tags": ["Fullstack", "API", "Concurrency"],
        "technologies": ["javascript", "python"],
        "concepts": ["State Synchronization", "Network Routing"],
        "runtime": "api",
        "execution_mode": "http",
        "xp_reward": 400,
        "estimated_time_minutes": 50,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": """const express = require('express');
const app = express();
app.use(express.json());

// In-memory store (no DB needed for this challenge)
const auctions = {};
let nextId = 1;

// TODO: POST /auctions  — create a new auction with title and startPrice
// app.post('/auctions', (req, res) => { ... });

// TODO: GET /auctions   — list all auctions
// app.get('/auctions', (req, res) => { ... });

// TODO: POST /auctions/:id/bids  — submit a bid (must be higher than current price)
// app.post('/auctions/:id/bids', (req, res) => { ... });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
"""
            }),
            "py_mongodb": json.dumps({
                "solution.py": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

auctions = {}
next_id = 1

# TODO: POST /auctions — create auction with title and startPrice
# TODO: GET /auctions  — list all auctions
# TODO: POST /auctions/{auction_id}/bids — submit a bid higher than current price

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
            })
        },
        "test_cases": [
            {
                "id": "bid-auction-tc-1",
                "name": "create and fetch auctions",
                "stdin": json.dumps([
                    {"method": "POST", "path": "/auctions", "body": {"title": "Vintage Lamp", "startPrice": 50}}
                ]),
                "expected_output": json.dumps([{
                    "request": {"method": "POST", "path": "/auctions"},
                    "response": {"status": 200, "headers": {}, "body": {"id": 1, "title": "Vintage Lamp", "startPrice": 50}}
                }]),
                "hidden": False,
                "weight": 1.0,
                "comparison_mode": "json"
            }
        ]
    }
]

async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    print("Deleting existing problems...")
    res = await db.problems.delete_many({})
    print(f"Deleted {res.deleted_count} problems.")
    
    print("Seeding new production challenges...")
    for idx, c in enumerate(CHALLENGES):
        doc = {
            "challenge_id": str(uuid4()),
            "title": c["title"],
            "slug": c["slug"],
            "short_description": c["short_description"],
            "description": c["description"],
            "domain": c["domain"],
            "difficulty": c["difficulty"],
            "tags": c.get("tags", []),
            "technologies": c.get("technologies", []),
            "hints": c.get("hints", []),
            "concepts": c.get("concepts", []),
            "starter_code": c.get("starter_code", {}),
            "test_cases": c.get("test_cases", []),
            "xp_reward": c.get("xp_reward", 100),
            "rating_reward": 10,
            "estimated_time_minutes": c.get("estimated_time_minutes", 30),
            "runtime": c.get("runtime"),
            "execution_mode": c.get("execution_mode"),
            "is_published": True,
            "is_featured": idx == 0,
            "is_archived": False
        }
        await db.problems.insert_one(doc)
        print(f"Inserted: {c['title']} ({c['slug']})")

if __name__ == '__main__':
    asyncio.run(seed())
