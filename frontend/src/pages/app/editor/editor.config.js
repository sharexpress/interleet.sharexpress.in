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

export function getStarter(slug, lang, dbChallenge) {
  if (dbChallenge?.starter_code) {
    if (lang === "multi" && dbChallenge.starter_code.multi) {
      return dbChallenge.starter_code.multi;
    }
    if (lang === "html" && dbChallenge.starter_code.html) {
      return dbChallenge.starter_code.html;
    }
    const backendKey = lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang;
    if (dbChallenge.starter_code[backendKey]) {
      return dbChallenge.starter_code[backendKey];
    }
  }
  return STARTERS[slug]?.[lang] ?? DEFAULT_STARTER[lang] ?? DEFAULT_STARTER.ts;
}
