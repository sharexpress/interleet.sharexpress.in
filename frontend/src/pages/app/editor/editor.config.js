export const LANG_TO_MONACO = {
  ts: "typescript", js: "javascript", py: "python", go: "go",
  html: "html", css: "css",
  java: "java", cpp: "cpp", rust: "rust",
  shell: "shell", yaml: "yaml", dockerfile: "dockerfile", plaintext: "plaintext",
  javascript: "javascript", typescript: "typescript", python: "python",
  multi: "shell",
};

export const LANG_LABEL = { ts: "TypeScript", js: "JavaScript", py: "Python", go: "Go", java: "Java", cpp: "C++", rust: "Rust" };
export const LANG_BADGE = { ts: "node v20.10", js: "node v20.10", py: "python 3.12", go: "go 1.22", java: "openjdk 21", cpp: "gcc 13.2", rust: "rustc 1.75" };
export const LANG_FILE = { ts: "solution.ts", js: "solution.js", py: "solution.py", go: "main.go", java: "Solution.java", cpp: "solution.cpp", rust: "solution.rs" };

export const BACKEND_LANG_TO_SHORT = {
  typescript: "ts",
  javascript: "js",
  python: "py",
  go: "go",
  cpp: "cpp",
  rust: "rust",
  java: "java",
  multi: "multi",
  html: "html",
};

export const STARTERS = {
  "build-a-rate-limiter": {
    ts: `// rate-limiter.ts
export class TokenBucket {
  private tokens: number;
  private last = Date.now();

  constructor(
    private readonly capacity: number,
    private readonly refillPerSec: number,
  ) {
    this.tokens = capacity;
  }

  allow(): boolean {
    const now = Date.now();
    const elapsed = (now - this.last) / 1000;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsed * this.refillPerSec,
    );
    this.last = now;
    if (this.tokens >= 1) {
      this.tokens -= 1;
      return true;
    }
    return false;
  }
}

const bucket = new TokenBucket(3, 1);
console.log({ call: 1, allowed: bucket.allow() });
console.log({ call: 2, allowed: bucket.allow() });
console.log({ call: 3, allowed: bucket.allow() });
console.log({ call: 4, allowed: bucket.allow() });
`,
    js: `// rate-limiter.js
class TokenBucket {
  #tokens;
  #last = Date.now();

  constructor(capacity, refillPerSec) {
    this.capacity = capacity;
    this.refillPerSec = refillPerSec;
    this.#tokens = capacity;
  }

  allow() {
    const now = Date.now();
    const elapsed = (now - this.#last) / 1000;
    this.#tokens = Math.min(this.capacity, this.#tokens + elapsed * this.refillPerSec);
    this.#last = now;
    if (this.#tokens >= 1) { this.#tokens -= 1; return true; }
    return false;
  }
}

const bucket = new TokenBucket(3, 1);
console.log({ call: 1, allowed: bucket.allow() });
console.log({ call: 2, allowed: bucket.allow() });
console.log({ call: 3, allowed: bucket.allow() });
console.log({ call: 4, allowed: bucket.allow() });
`,
    py: `# rate-limiter.py
import time

class TokenBucket:
    def __init__(self, capacity: float, refill_per_sec: float):
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self.tokens = capacity
        self.last = time.time()

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_sec)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

bucket = TokenBucket(3, 1)
print({"call": 1, "allowed": bucket.allow()})
print({"call": 2, "allowed": bucket.allow()})
print({"call": 3, "allowed": bucket.allow()})
print({"call": 4, "allowed": bucket.allow()})
`,
    go: `// rate-limiter.go
package main

import (
	"fmt"
	"math"
	"time"
)

type TokenBucket struct {
	capacity     float64
	refillPerSec float64
	tokens       float64
	last         time.Time
}

func NewBucket(capacity, refill float64) *TokenBucket {
	return &TokenBucket{
		capacity:     capacity,
		refillPerSec: refill,
		tokens:       capacity,
		last:         time.Now(),
	}
}

func (b *TokenBucket) Allow() bool {
	now := time.Now()
	elapsed := now.Sub(b.last).Seconds()
	b.tokens = math.Min(b.capacity, b.tokens+elapsed*b.refillPerSec)
	b.last = now

	if b.tokens >= 1 {
		b.tokens -= 1
		return true
	}
	return false
}

func main() {
	bucket := NewBucket(3, 1)
	fmt.Printf("%+v\\n", map[string]any{"call": 1, "allowed": bucket.Allow()})
	fmt.Printf("%+v\\n", map[string]any{"call": 2, "allowed": bucket.Allow()})
	fmt.Printf("%+v\\n", map[string]any{"call": 3, "allowed": bucket.Allow()})
	fmt.Printf("%+v\\n", map[string]any{"call": 4, "allowed": bucket.Allow()})
}
`,
    cpp: `// rate-limiter.cpp
#include <iostream>
#include <chrono>
#include <algorithm>
#include <thread>

class TokenBucket {
private:
    double capacity;
    double refillPerSec;
    double tokens;
    std::chrono::steady_clock::time_point last;

public:
    TokenBucket(double cap, double refill) 
        : capacity(cap), refillPerSec(refill), tokens(cap), last(std::chrono::steady_clock::now()) {}

    bool allow() {
        auto now = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(now - last).count();
        tokens = std::min(capacity, tokens + elapsed * refillPerSec);
        last = now;

        if (tokens >= 1.0) {
            tokens -= 1.0;
            return true;
        }
        return false;
    }
};

int main() {
    TokenBucket bucket(3.0, 1.0);
    std::cout << "{\\"call\\": 1, \\"allowed\\": " << (bucket.allow() ? "true" : "false") << "}" << std::endl;
    std::cout << "{\\"call\\": 2, \\"allowed\\": " << (bucket.allow() ? "true" : "false") << "}" << std::endl;
    std::cout << "{\\"call\\": 3, \\"allowed\\": " << (bucket.allow() ? "true" : "false") << "}" << std::endl;
    std::cout << "{\\"call\\": 4, \\"allowed\\": " << (bucket.allow() ? "true" : "false") << "}" << std::endl;
    return 0;
}
`,
    rust: `// rate-limiter.rs
use std::time::{Instant, Duration};
use std::cmp;

struct TokenBucket {
    capacity: f64,
    refill_per_sec: f64,
    tokens: f64,
    last: Instant,
}

impl TokenBucket {
    fn new(capacity: f64, refill: f64) -> Self {
        Self {
            capacity,
            refill_per_sec: refill,
            tokens: capacity,
            last: Instant::now(),
        }
    }

    fn allow(&mut self) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last).as_secs_f64();
        self.tokens = (self.capacity).min(self.tokens + elapsed * self.refill_per_sec);
        self.last = now;

        if self.tokens >= 1.0 {
            self.tokens -= 1.0;
            return true;
        }
        false
    }
}

fn main() {
    let mut bucket = TokenBucket::new(3.0, 1.0);
    println!("{{\\"call\\": 1, \\"allowed\\": {}}}", bucket.allow());
    println!("{{\\"call\\": 2, \\"allowed\\": {}}}", bucket.allow());
    println!("{{\\"call\\": 3, \\"allowed\\": {}}}", bucket.allow());
    println!("{{\\"call\\": 4, \\"allowed\\": {}}}", bucket.allow());
}
`,
    java: `// Solution.java
import java.time.Instant;
import java.time.Duration;

class TokenBucket {
    private final double capacity;
    private final double refillPerSec;
    private double tokens;
    private Instant last;

    public TokenBucket(double capacity, double refillPerSec) {
        this.capacity = capacity;
        this.refillPerSec = refillPerSec;
        this.tokens = capacity;
        this.last = Instant.now();
    }

    public synchronized boolean allow() {
        Instant now = Instant.now();
        double elapsed = Duration.between(last, now).toNanos() / 1_000_000_000.0;
        tokens = Math.min(capacity, tokens + refillPerSec * elapsed);
        last = now;

        if (tokens >= 1.0) {
            tokens -= 1.0;
            return true;
        }
        return false;
    }
}

public class Solution {
    public static void main(String[] args) {
        TokenBucket bucket = new TokenBucket(3, 1);
        System.out.println("{\\"call\\": 1, \\"allowed\\": " + bucket.allow() + "}");
        System.out.println("{\\"call\\": 2, \\"allowed\\": " + bucket.allow() + "}");
        System.out.println("{\\"call\\": 3, \\"allowed\\": " + bucket.allow() + "}");
        System.out.println("{\\"call\\": 4, \\"allowed\\": " + bucket.allow() + "}");
    }
}
`
  },
  "feature-flag-service": {
    ts: `// flag.ts
export interface UserContext {
  userId: string;
  attributes?: Record<string, string | number | boolean>;
}

export interface Flag {
  key: string;
  enabled: boolean;
  allowlist?: string[];
  rollout?: number; // 0-100 percentage
}

export class FlagService {
  private flags = new Map<string, Flag>();

  register(flag: Flag) {
    this.flags.set(flag.key, flag);
  }

  isOn(key: string, ctx: UserContext): boolean {
    const f = this.flags.get(key);
    if (!f || !f.enabled) return false;

    // 1. Allowlist Check
    if (f.allowlist?.includes(ctx.userId)) return true;

    // 2. Rollout Check (deterministic murmur-like hash)
    if (f.rollout && f.rollout > 0) {
      let hash = 0;
      for (let i = 0; i < ctx.userId.length; i++) {
        hash = (hash << 5) - hash + ctx.userId.charCodeAt(i);
        hash |= 0;
      }
      return Math.abs(hash) % 100 < f.rollout;
    }

    return true;
  }
}

const s = new FlagService();
s.register({ key: "new-checkout", enabled: true, allowlist: ["u_42"] });
s.register({ key: "dark-mode", enabled: true, rollout: 50 });

console.log({ flag: "new-checkout", userId: "u_42", result: s.isOn("new-checkout", { userId: "u_42" }) });
console.log({ flag: "dark-mode", userId: "u_7", result: s.isOn("dark-mode", { userId: "u_7" }) });
`,
    js: `// flag.js
class FlagService {
  constructor() { this.flags = new Map(); }
  register(flag) { this.flags.set(flag.key, flag); }
  isOn(key, ctx) {
    const f = this.flags.get(key);
    if (!f || !f.enabled) return false;
    if (f.allowlist?.includes(ctx.userId)) return true;
    if (f.rollout) {
      let hash = 0;
      for (let i = 0; i < ctx.userId.length; i++) {
        hash = (hash << 5) - hash + ctx.userId.charCodeAt(i);
        hash |= 0;
      }
      return Math.abs(hash) % 100 < f.rollout;
    }
    return true;
  }
}

const s = new FlagService();
s.register({ key: "new-checkout", enabled: true, allowlist: ["u_42"] });
s.register({ key: "dark-mode", enabled: true, rollout: 50 });
console.log({ flag: "new-checkout", userId: "u_42", result: s.isOn("new-checkout", { userId: "u_42" }) });
console.log({ flag: "dark-mode", userId: "u_7", result: s.isOn("dark-mode", { userId: "u_7" }) });
`,
    py: `# flag.py
class FlagService:
    def __init__(self):
        self.flags = {}

    def register(self, flag: dict):
        self.flags[flag["key"]] = flag

    def is_on(self, key: str, ctx: dict) -> bool:
        f = self.flags.get(key)
        if not f or not f.get("enabled", False):
            return False
        if ctx["userId"] in f.get("allowlist", []):
            return True
        rollout = f.get("rollout", 0)
        if rollout > 0:
            h = sum(ord(c) for c in ctx["userId"])
            return h % 100 < rollout
        return True

s = FlagService()
s.register({"key": "new-checkout", "enabled": True, "allowlist": ["u_42"]})
s.register({"key": "dark-mode", "enabled": True, "rollout": 50})
print({"flag": "new-checkout", "userId": "u_42", "result": s.is_on("new-checkout", {"userId": "u_42"})})
print({"flag": "dark-mode", "userId": "u_7", "result": s.is_on("dark-mode", {"userId": "u_7"})})
`,
    go: `// flag.go
package main

import "fmt"

type Flag struct {
	Key       string
	Enabled   bool
	Allowlist []string
	Rollout   int
}

type FlagSvc struct {
	flags map[string]Flag
}

func NewSvc() *FlagSvc { return &FlagSvc{flags: make(map[string]Flag)} }
func (s *FlagSvc) Register(f Flag) { s.flags[f.Key] = f }
func (s *FlagSvc) IsOn(key, uid string) bool {
	f, ok := s.flags[key]
	if !ok || !f.Enabled { return false }
	for _, u := range f.Allowlist { if u == uid { return true } }
	if f.Rollout > 0 { var h int; for _, c := range uid { h += int(c) }; return h%100 < f.Rollout }
	return true
}

func main() {
	s := NewSvc()
	s.Register(Flag{Key: "new-checkout", Enabled: true, Allowlist: []string{"u_42"}})
	s.Register(Flag{Key: "dark-mode",    Enabled: true, Rollout: 50})
	fmt.Printf("%+v\\n", map[string]any{"flag": "new-checkout", "userId": "u_42", "result": s.IsOn("new-checkout", "u_42")})
	fmt.Printf("%+v\\n", map[string]any{"flag": "dark-mode",    "userId": "u_7",  "result": s.IsOn("dark-mode",    "u_7")})
}
`,
  },
  "task-manager-api": {
    js_sqlite: JSON.stringify({
      "solution.js": `const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
app.use(express.json());

const db = new sqlite3.Database('db.sqlite');

// Health check (required by sandbox)
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// GET /tasks - Get all tasks
app.get('/tasks', (req, res) => {
  db.all('SELECT * FROM tasks', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows.map(r => ({ ...r, completed: !!r.completed })));
  });
});

// POST /tasks - Create a task
app.post('/tasks', (req, res) => {
  const { title, description } = req.body;
  if (!title) return res.status(400).json({ error: 'Title is required' });
  
  db.run('INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)', [title, description], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.status(201).json({ id: this.lastID, title, description, completed: false });
  });
});

// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});`
    }),
    js_postgres: JSON.stringify({
      "solution.js": `const express = require('express');
const { Client } = require('pg');
const app = express();
app.use(express.json());

const client = new Client({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/tasks'
});
client.connect();

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/tasks', async (req, res) => {
  try {
    const result = await client.query('SELECT * FROM tasks');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/tasks', async (req, res) => {
  const { title, description } = req.body;
  if (!title) return res.status(400).json({ error: 'Title is required' });
  
  try {
    const result = await client.query(
      'INSERT INTO tasks (title, description, completed) VALUES ($1, $2, false) RETURNING *',
      [title, description]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});`
    }),
    js_mongodb: JSON.stringify({
      "solution.js": `const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');
const app = express();
app.use(express.json());

const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');
let db;

client.connect().then(() => {
  db = client.db('tasks_db');
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/tasks', async (req, res) => {
  try {
    const tasks = await db.collection('tasks').find({}).toArray();
    res.json(tasks.map(t => ({
      id: t._id,
      title: t.title,
      description: t.description,
      completed: t.completed
    })));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/tasks', async (req, res) => {
  const { title, description } = req.body;
  if (!title) return res.status(400).json({ error: 'Title is required' });
  
  try {
    const task = { title, description, completed: false };
    const result = await db.collection('tasks').insertOne(task);
    res.status(201).json({ id: result.insertedId, ...task });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});`
    }),
    js_mysql: JSON.stringify({
      "solution.js": `const express = require('express');
const mysql = require('mysql2/promise');
const app = express();
app.use(express.json());

let pool;
mysql.createPool({
  uri: process.env.DATABASE_URL || 'mysql://root:root@localhost:3306/tasks'
}).then(p => pool = p);

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/tasks', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM tasks');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/tasks', async (req, res) => {
  const { title, description } = req.body;
  if (!title) return res.status(400).json({ error: 'Title is required' });
  
  try {
    const [result] = await pool.query(
      'INSERT INTO tasks (title, description, completed) VALUES (?, ?, false)',
      [title, description]
    );
    res.status(201).json({ id: result.insertId, title, description, completed: false });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});`
    }),
    py_sqlite: JSON.stringify({
      "solution.py": `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

def get_db():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.get('/health')
def health():
    return {'status': 'ok'}

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

@app.get('/tasks')
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    return [{**dict(r), 'completed': bool(r['completed'])} for r in rows]

@app.post('/tasks', status_code=201)
def create_task(task: TaskCreate):
    if not task.title:
        raise HTTPException(status_code=400, detail='Title is required')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)', (task.title, task.description))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {'id': task_id, 'title': task.title, 'description': task.description, 'completed': False}

# TODO: Implement GET /tasks/{task_id}, PUT /tasks/{task_id}, and DELETE /tasks/{task_id}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)`
    }),
    py_postgres: JSON.stringify({
      "solution.py": `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

def get_db():
    return psycopg2.connect(os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/tasks'))

@app.get('/health')
def health():
    return {'status': 'ok'}

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

@app.get('/tasks')
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, completed FROM tasks')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'id': r[0], 'title': r[1], 'description': r[2], 'completed': r[3]} for r in rows]

@app.post('/tasks', status_code=201)
def create_task(task: TaskCreate):
    if not task.title:
        raise HTTPException(status_code=400, detail='Title is required')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, description, completed) VALUES (%s, %s, false) RETURNING id, title, description, completed',
        (task.title, task.description)
    )
    new_task = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return {'id': new_task[0], 'title': new_task[1], 'description': new_task[2], 'completed': new_task[3]}

# TODO: Implement GET /tasks/{task_id}, PUT /tasks/{task_id}, and DELETE /tasks/{task_id}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)`
    }),
    py_mongodb: JSON.stringify({
      "solution.py": `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))
db = client['tasks_db']

@app.get('/health')
def health():
    return {'status': 'ok'}

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

@app.get('/tasks')
def get_tasks():
    tasks = list(db.tasks.find({}))
    return [{'id': str(t['_id']), 'title': t.get('title'), 'description': t.get('description'), 'completed': t.get('completed', False)} for t in tasks]

@app.post('/tasks', status_code=201)
def create_task(task: TaskCreate):
    if not task.title:
        raise HTTPException(status_code=400, detail='Title is required')
    new_task = {'title': task.title, 'description': task.description, 'completed': False}
    result = db.tasks.insert_one(new_task)
    return {'id': str(result.inserted_id), **new_task}

# TODO: Implement GET /tasks/{task_id}, PUT /tasks/{task_id}, and DELETE /tasks/{task_id}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)`
    }),
    py_mysql: JSON.stringify({
      "solution.py": `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
import os

app = FastAPI()

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        database=os.environ.get('DB_NAME', 'tasks'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get('/health')
def health():
    return {'status': 'ok'}

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

@app.get('/tasks')
def get_tasks():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
    conn.close()
    return rows

@app.post('/tasks', status_code=201)
def create_task(task: TaskCreate):
    if not task.title:
        raise HTTPException(status_code=400, detail='Title is required')
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (%s, %s, false)', (task.title, task.description))
        task_id = conn.insert_id()
    conn.commit()
    conn.close()
    return {'id': task_id, 'title': task.title, 'description': task.description, 'completed': False}

# TODO: Implement GET /tasks/{task_id}, PUT /tasks/{task_id}, and DELETE /tasks/{task_id}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)`
    }),
    go_sqlite: JSON.stringify({
      "main.go": `package main

import (
	"database/sql"
	"net/http"
	"os"
	"github.com/gin-gonic/gin"
	_ "github.com/glebarez/go-sqlite"
)

type Task struct {
	ID          int    \`json:"id"\`
	Title       string \`json:"title"\`
	Description string \`json:"description"\`
	Completed   bool   \`json:"completed"\`
}

var db *sql.DB

func main() {
	var err error
	db, err = sql.Open("sqlite", "db.sqlite")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	r.GET("/tasks", func(c *gin.Context) {
		rows, err := db.Query("SELECT id, title, description, completed FROM tasks")
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		var tasks []Task
		for rows.Next() {
			var t Task
			var completed int
			rows.Scan(&t.ID, &t.Title, &t.Description, &completed)
			t.Completed = completed == 1
			tasks = append(tasks, t)
		}
		c.JSON(http.StatusOK, tasks)
	})

	r.POST("/tasks", func(c *gin.Context) {
		var t Task
		c.BindJSON(&t)
		if t.Title == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Title is required"})
			return
		}
		res, _ := db.Exec("INSERT INTO tasks (title, description, completed) VALUES (?, ?, 0)", t.Title, t.Description)
		id, _ := res.LastInsertId()
		t.ID = int(id)
		c.JSON(http.StatusCreated, t)
	})

	// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}`
    }),
    go_postgres: JSON.stringify({
      "main.go": `package main

import (
	"database/sql"
	"net/http"
	"os"
	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

type Task struct {
	ID          int    \`json:"id"\`
	Title       string \`json:"title"\`
	Description string \`json:"description"\`
	Completed   bool   \`json:"completed"\`
}

var db *sql.DB

func main() {
	var err error
	db, err = sql.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	r.GET("/tasks", func(c *gin.Context) {
		rows, err := db.Query("SELECT id, title, description, completed FROM tasks")
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		var tasks []Task
		for rows.Next() {
			var t Task
			rows.Scan(&t.ID, &t.Title, &t.Description, &t.Completed)
			tasks = append(tasks, t)
		}
		c.JSON(http.StatusOK, tasks)
	})

	r.POST("/tasks", func(c *gin.Context) {
		var t Task
		c.BindJSON(&t)
		if t.Title == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Title is required"})
			return
		}
		err := db.QueryRow("INSERT INTO tasks (title, description, completed) VALUES ($1, $2, false) RETURNING id", t.Title, t.Description).Scan(&t.ID)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, t)
	})

	// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}`
    }),
    go_mongodb: JSON.stringify({
      "main.go": `package main

import (
	"context"
	"net/http"
	"os"
	"time"
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Task struct {
	ID          string \`json:"id" bson:"_id,omitempty"\`
	Title       string \`json:"title" bson:"title"\`
	Description string \`json:"description" bson:"description"\`
	Completed   bool   \`json:"completed" bson:"completed"\`
}

var collection *mongo.Collection

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(os.Getenv("MONGO_URI")))
	if err != nil {
		panic(err)
	}
	collection = client.Database("tasks_db").Collection("tasks")

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	r.GET("/tasks", func(c *gin.Context) {
		cursor, err := collection.Find(context.Background(), bson.M{})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer cursor.Close(context.Background())

		var tasks []Task
		for cursor.Next(context.Background()) {
			var t Task
			cursor.Decode(&t)
			tasks = append(tasks, t)
		}
		c.JSON(http.StatusOK, tasks)
	})

	r.POST("/tasks", func(c *gin.Context) {
		var t Task
		c.BindJSON(&t)
		if t.Title == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Title is required"})
			return
		}
		t.Completed = false
		res, err := collection.InsertOne(context.Background(), t)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		t.ID = res.InsertedID.(primitive.ObjectID).Hex()
		c.JSON(http.StatusCreated, t)
	})

	// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}`
    }),
    go_mysql: JSON.stringify({
      "main.go": `package main

import (
	"database/sql"
	"net/http"
	"os"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

type Task struct {
	ID          int    \`json:"id"\`
	Title       string \`json:"title"\`
	Description string \`json:"description"\`
	Completed   bool   \`json:"completed"\`
}

var db *sql.DB

func main() {
	var err error
	db, err = sql.Open("mysql", os.Getenv("DATABASE_URL"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	r.GET("/tasks", func(c *gin.Context) {
		rows, err := db.Query("SELECT id, title, description, completed FROM tasks")
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		var tasks []Task
		for rows.Next() {
			var t Task
			rows.Scan(&t.ID, &t.Title, &t.Description, &t.Completed)
			tasks = append(tasks, t)
		}
		c.JSON(http.StatusOK, tasks)
	})

	r.POST("/tasks", func(c *gin.Context) {
		var t Task
		c.BindJSON(&t)
		if t.Title == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Title is required"})
			return
		}
		res, err := db.Exec("INSERT INTO tasks (title, description, completed) VALUES (?, ?, false)", t.Title, t.Description)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		id, _ := res.LastInsertId()
		t.ID = int(id)
		c.JSON(http.StatusCreated, t)
	})

	// TODO: Implement GET /tasks/:id, PUT /tasks/:id, and DELETE /tasks/:id

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}`
    })
  },
};

export const DEFAULT_STARTER = {
  ts: `// Write your TypeScript solution here

function solution(): void {
  console.log({ status: "ready", message: "Start coding!" });
}

solution();
`,
  js: `// Write your JavaScript solution here
function solution() {
  console.log({ status: "ready", message: "Start coding!" });
}
solution();
`,
  py: `# Write your Python solution here
def solution():
    print({"status": "ready", "message": "Start coding!"})
solution()
`,
  go: `package main
import "fmt"
func main() {
  fmt.Printf("%+v\\n", map[string]any{"status": "ready", "message": "Start coding!"})
}
`,
  java: `import java.util.Map;

public class Solution {
    public static void main(String[] args) {
        System.out.println("{\\"status\\": \\"ready\\", \\"message\\": \\"Start coding!\\"}");
    }
}
`,
  cpp: `#include <iostream>

int main() {
    std::cout << "{\\"status\\": \\"ready\\", \\"message\\": \\"Start coding!\\"}" << std::endl;
    return 0;
}
`,
  rust: `fn main() {
    println!("{{\\"status\\": \\"ready\\", \\"message\\": \\"Start coding!\\"}}");
}
`,
};

export function getStarter(slug, lang, dbChallenge, selectedDb = "sqlite") {
  const dbKey = `${lang}_${selectedDb}`;
  if (dbChallenge?.starter_code) {
    if (lang === "multi" && dbChallenge.starter_code.multi) {
      return dbChallenge.starter_code.multi;
    }
    if (lang === "html" && dbChallenge.starter_code.html) {
      return dbChallenge.starter_code.html;
    }
    if (dbChallenge.starter_code[dbKey]) {
      return dbChallenge.starter_code[dbKey];
    }
    if (selectedDb === "sqlite") {
      const backendKey = lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang;
      if (dbChallenge.starter_code[backendKey]) {
        return dbChallenge.starter_code[backendKey];
      }
      if (dbChallenge.starter_code[lang]) {
        return dbChallenge.starter_code[lang];
      }
    }
  }
  return STARTERS[slug]?.[dbKey] ?? STARTERS[slug]?.[lang] ?? DEFAULT_STARTER[lang] ?? DEFAULT_STARTER.ts;
}
