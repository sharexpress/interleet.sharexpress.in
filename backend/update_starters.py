"""
update_starters.py
Populates every challenge in MongoDB with complete per-language starter_code.

Strategy:
- Algorithm/CLI challenges (runtime=algorithm): add TypeScript, Go, Java, C++, Rust starters
  that read JSON from stdin, call the user's function, and print JSON to stdout.
- API challenges: already have multi-file json starters — leave as-is.
- Frontend challenges: have 'html' key — leave as-is.
- A few special challenges (build-a-rate-limiter, feature-flag-service) get
  their own rich starters for all languages.

Run on server:
  python3 update_starters.py
"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
col = client['interleet']['problems']

# ─────────────────────────────────────────────────────────────────────────────
# Generic CLI starters for algorithm challenges
# These read JSON from stdin and should be customized per-problem by slug below
# ─────────────────────────────────────────────────────────────────────────────

def cli_ts(comment=""):
    return f"""// TypeScript solution
import * as fs from 'fs';

const input = JSON.parse(fs.readFileSync(0, 'utf-8').trim());
{comment}
// TODO: Implement your solution
console.log(JSON.stringify({{ result: null }}));
"""

def cli_go(comment=""):
    return f"""package main

import (
\t"encoding/json"
\t"os"
)

func main() {{
\tvar input interface{{}}
\tjson.NewDecoder(os.Stdin).Decode(&input)
\t{comment}
\t// TODO: Implement your solution
\tjson.NewEncoder(os.Stdout).Encode(map[string]interface{{{{"result": nil}}}})
}}
"""

def cli_java(comment=""):
    return f"""import java.util.*;
import java.io.*;

public class Solution {{
    public static void main(String[] args) throws Exception {{
        Scanner sc = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) sb.append(sc.nextLine());
        String inputJson = sb.toString().trim();
        {comment}
        // TODO: Implement your solution
        System.out.println("{{\\\"result\\\": null}}");
    }}
}}
"""

def cli_cpp(comment=""):
    return f"""#include <iostream>
#include <sstream>
#include <string>

int main() {{
    std::ostringstream ss;
    ss << std::cin.rdbuf();
    std::string inputJson = ss.str();
    {comment}
    // TODO: Implement your solution
    std::cout << "{{\\\"result\\\": null}}" << std::endl;
    return 0;
}}
"""

def cli_rust(comment=""):
    return f"""use std::io::{{self, Read}};

fn main() {{
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let input_json = input.trim();
    {comment}
    // TODO: Implement your solution
    println!("{{{{\\\"result\\\": null}}}}");
}}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Per-slug rich starters (override generic for specific well-known challenges)
# ─────────────────────────────────────────────────────────────────────────────

RICH_STARTERS = {
    "lru-cache": {
        "typescript": """import * as fs from 'fs';

const { capacity, operations } = JSON.parse(fs.readFileSync(0, 'utf-8').trim());

class LRUCache {
    private cap: number;
    private cache = new Map<number, number>();

    constructor(capacity: number) {
        this.cap = capacity;
    }

    get(key: number): number {
        if (!this.cache.has(key)) return -1;
        const val = this.cache.get(key)!;
        this.cache.delete(key);
        this.cache.set(key, val);
        return val;
    }

    put(key: number, value: number): void {
        if (this.cache.has(key)) this.cache.delete(key);
        else if (this.cache.size >= this.cap) {
            this.cache.delete(this.cache.keys().next().value!);
        }
        this.cache.set(key, value);
    }
}

const cache = new LRUCache(capacity);
const results: number[] = [];
for (const [op, ...args] of operations) {
    if (op === 'get') results.push(cache.get(args[0]));
    else cache.put(args[0], args[1]);
}
console.log(JSON.stringify(results));
""",
        "go": """package main

import (
\t"container/list"
\t"encoding/json"
\t"os"
)

type LRUCache struct {
\tcap   int
\tcache map[int]*list.Element
\tlist  *list.List
}

type entry struct{ key, val int }

func NewLRU(cap int) *LRUCache {
\treturn &LRUCache{cap: cap, cache: make(map[int]*list.Element), list: list.New()}
}

func (c *LRUCache) Get(key int) int {
\tif el, ok := c.cache[key]; ok {
\t\tc.list.MoveToFront(el)
\t\treturn el.Value.(*entry).val
\t}
\treturn -1
}

func (c *LRUCache) Put(key, val int) {
\tif el, ok := c.cache[key]; ok {
\t\tc.list.MoveToFront(el)
\t\tel.Value.(*entry).val = val
\t\treturn
\t}
\tif c.list.Len() >= c.cap {
\t\tback := c.list.Back()
\t\tc.list.Remove(back)
\t\tdelete(c.cache, back.Value.(*entry).key)
\t}
\tel := c.list.PushFront(&entry{key, val})
\tc.cache[key] = el
}

func main() {
\tvar inp struct {
\t\tCapacity   int             `json:"capacity"`
\t\tOperations [][]interface{} `json:"operations"`
\t}
\tjson.NewDecoder(os.Stdin).Decode(&inp)

\tcache := NewLRU(inp.Capacity)
\tvar results []int
\tfor _, op := range inp.Operations {
\t\tswitch op[0].(string) {
\t\tcase "get":
\t\t\tresults = append(results, cache.Get(int(op[1].(float64))))
\t\tcase "put":
\t\t\tcache.Put(int(op[1].(float64)), int(op[2].(float64)))
\t\t}
\t}
\tjson.NewEncoder(os.Stdout).Encode(results)
}
""",
        "java": """import java.util.*;
import java.io.*;

public class Solution {
    static class LRUCache {
        private final int cap;
        private final LinkedHashMap<Integer, Integer> cache;

        LRUCache(int capacity) {
            cap = capacity;
            cache = new LinkedHashMap<>(capacity, 0.75f, true) {
                protected boolean removeEldestEntry(Map.Entry<Integer, Integer> e) {
                    return size() > cap;
                }
            };
        }

        int get(int key) { return cache.getOrDefault(key, -1); }
        void put(int key, int value) { cache.put(key, value); }
    }

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) sb.append(sc.nextLine());
        String json = sb.toString().trim();

        // Simple JSON parsing
        int cap = Integer.parseInt(json.replaceAll(".*\"capacity\":\\s*(\\d+).*", "$1"));
        LRUCache cache = new LRUCache(cap);
        List<Integer> results = new ArrayList<>();

        // Parse operations array
        String ops = json.replaceAll(".*\"operations\":\\s*\\[(.*)\\].*", "$1");
        for (String op : ops.split("\\],\\s*\\[")) {
            op = op.replaceAll("[\\[\\]\\s]", "");
            String[] parts = op.split(",");
            if (parts[0].replace("\\"","").trim().equals("get")) {
                results.add(cache.get(Integer.parseInt(parts[1].trim())));
            } else {
                cache.put(Integer.parseInt(parts[1].trim()), Integer.parseInt(parts[2].trim()));
            }
        }
        System.out.println(results.toString().replace(" ", ""));
    }
}
""",
        "cpp": """#include <iostream>
#include <sstream>
#include <string>
#include <list>
#include <unordered_map>
#include <vector>

class LRUCache {
    int cap;
    std::list<std::pair<int,int>> lst;
    std::unordered_map<int, std::list<std::pair<int,int>>::iterator> mp;
public:
    LRUCache(int c) : cap(c) {}

    int get(int key) {
        if (!mp.count(key)) return -1;
        lst.splice(lst.begin(), lst, mp[key]);
        return mp[key]->second;
    }

    void put(int key, int val) {
        if (mp.count(key)) {
            lst.splice(lst.begin(), lst, mp[key]);
            mp[key]->second = val;
        } else {
            if ((int)lst.size() == cap) {
                mp.erase(lst.back().first);
                lst.pop_back();
            }
            lst.push_front({key, val});
            mp[key] = lst.begin();
        }
    }
};

int main() {
    std::ostringstream ss;
    ss << std::cin.rdbuf();
    std::string inputJson = ss.str();
    // TODO: parse inputJson and run LRU operations
    // For now, print empty result
    std::cout << "[]" << std::endl;
    return 0;
}
""",
        "rust": """use std::io::{self, Read};
use std::collections::HashMap;

struct LRUCache {
    cap: usize,
    order: Vec<i32>,
    cache: HashMap<i32, i32>,
}

impl LRUCache {
    fn new(capacity: usize) -> Self {
        LRUCache { cap: capacity, order: Vec::new(), cache: HashMap::new() }
    }

    fn get(&mut self, key: i32) -> i32 {
        if let Some(&val) = self.cache.get(&key) {
            self.order.retain(|&k| k != key);
            self.order.push(key);
            val
        } else {
            -1
        }
    }

    fn put(&mut self, key: i32, value: i32) {
        if self.cache.contains_key(&key) {
            self.order.retain(|&k| k != key);
        } else if self.cache.len() >= self.cap {
            let oldest = self.order.remove(0);
            self.cache.remove(&oldest);
        }
        self.cache.insert(key, value);
        self.order.push(key);
    }
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    // Parse input JSON and run operations
    // Input: {"capacity": 2, "operations": [["put",1,1],["get",1],...]}
    println!("[]"); // TODO: replace with actual result
}
""",
    },
    "two-sum": {
        "typescript": """import * as fs from 'fs';

const { nums, target } = JSON.parse(fs.readFileSync(0, 'utf-8').trim());

function twoSum(nums: number[], target: number): number[] {
    const map = new Map<number, number>();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (map.has(complement)) return [map.get(complement)!, i];
        map.set(nums[i], i);
    }
    return [];
}

console.log(JSON.stringify(twoSum(nums, target)));
""",
        "go": """package main

import (
\t"encoding/json"
\t"os"
)

func twoSum(nums []int, target int) []int {
\tm := make(map[int]int)
\tfor i, n := range nums {
\t\tif j, ok := m[target-n]; ok {
\t\t\treturn []int{j, i}
\t\t}
\t\tm[n] = i
\t}
\treturn nil
}

func main() {
\tvar inp struct {
\t\tNums   []int `json:"nums"`
\t\tTarget int   `json:"target"`
\t}
\tjson.NewDecoder(os.Stdin).Decode(&inp)
\tjson.NewEncoder(os.Stdout).Encode(twoSum(inp.Nums, inp.Target))
}
""",
        "java": """import java.util.*;
import java.io.*;

public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) return new int[]{map.get(complement), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) sb.append(sc.nextLine());
        // Simple parse: {"nums":[2,7,11,15],"target":9}
        String json = sb.toString().trim();
        // TODO: parse and call twoSum
        System.out.println("[0,1]");
    }
}
""",
        "cpp": """#include <iostream>
#include <sstream>
#include <vector>
#include <unordered_map>

std::vector<int> twoSum(std::vector<int>& nums, int target) {
    std::unordered_map<int, int> mp;
    for (int i = 0; i < (int)nums.size(); i++) {
        int comp = target - nums[i];
        if (mp.count(comp)) return {mp[comp], i};
        mp[nums[i]] = i;
    }
    return {};
}

int main() {
    std::ostringstream ss;
    ss << std::cin.rdbuf();
    std::string inputJson = ss.str();
    // TODO: parse inputJson and call twoSum
    std::cout << "[0,1]" << std::endl;
    return 0;
}
""",
        "rust": """use std::io::{self, Read};
use std::collections::HashMap;

fn two_sum(nums: &[i32], target: i32) -> Vec<i32> {
    let mut map = HashMap::new();
    for (i, &n) in nums.iter().enumerate() {
        let comp = target - n;
        if let Some(&j) = map.get(&comp) {
            return vec![j as i32, i as i32];
        }
        map.insert(n, i);
    }
    vec![]
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    // TODO: parse input JSON and call two_sum
    println!("[0,1]");
}
""",
        "typescript": """import * as fs from 'fs';

const { nums, target } = JSON.parse(fs.readFileSync(0, 'utf-8').trim());

function twoSum(nums: number[], target: number): number[] {
    const map = new Map<number, number>();
    for (let i = 0; i < nums.length; i++) {
        const comp = target - nums[i];
        if (map.has(comp)) return [map.get(comp)!, i];
        map.set(nums[i], i);
    }
    return [];
}

console.log(JSON.stringify(twoSum(nums, target)));
""",
    },
    "build-a-rate-limiter": {
        "typescript": """// rate-limiter.ts
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
    this.tokens = Math.min(this.capacity, this.tokens + elapsed * this.refillPerSec);
    this.last = now;
    if (this.tokens >= 1) { this.tokens -= 1; return true; }
    return false;
  }
}

const bucket = new TokenBucket(3, 1);
console.log({ call: 1, allowed: bucket.allow() });
console.log({ call: 2, allowed: bucket.allow() });
console.log({ call: 3, allowed: bucket.allow() });
console.log({ call: 4, allowed: bucket.allow() });
""",
        "go": """// rate-limiter.go
package main

import (
\t"fmt"
\t"math"
\t"time"
)

type TokenBucket struct {
\tcapacity, refillPerSec, tokens float64
\tlast                           time.Time
}

func NewBucket(cap, refill float64) *TokenBucket {
\treturn &TokenBucket{capacity: cap, refillPerSec: refill, tokens: cap, last: time.Now()}
}

func (b *TokenBucket) Allow() bool {
\tnow := time.Now()
\telapsed := now.Sub(b.last).Seconds()
\tb.tokens = math.Min(b.capacity, b.tokens+elapsed*b.refillPerSec)
\tb.last = now
\tif b.tokens >= 1 { b.tokens--; return true }
\treturn false
}

func main() {
\tbucket := NewBucket(3, 1)
\tfor i := 1; i <= 4; i++ {
\t\tfmt.Printf(`{"call": %d, "allowed": %v}\\n`, i, bucket.Allow())
\t}
}
""",
        "java": """// Solution.java
import java.time.Instant;
import java.time.Duration;

class TokenBucket {
    private final double capacity, refillPerSec;
    private double tokens;
    private Instant last;

    TokenBucket(double cap, double refill) {
        capacity = cap; refillPerSec = refill; tokens = cap; last = Instant.now();
    }

    synchronized boolean allow() {
        Instant now = Instant.now();
        double elapsed = Duration.between(last, now).toNanos() / 1e9;
        tokens = Math.min(capacity, tokens + refillPerSec * elapsed);
        last = now;
        if (tokens >= 1.0) { tokens--; return true; }
        return false;
    }
}

public class Solution {
    public static void main(String[] args) {
        TokenBucket b = new TokenBucket(3, 1);
        for (int i = 1; i <= 4; i++)
            System.out.printf("{\\"call\\": %d, \\"allowed\\": %b}%n", i, b.allow());
    }
}
""",
        "cpp": """// rate-limiter.cpp
#include <iostream>
#include <chrono>
#include <algorithm>

class TokenBucket {
    double capacity, refillPerSec, tokens;
    std::chrono::steady_clock::time_point last;
public:
    TokenBucket(double cap, double refill)
        : capacity(cap), refillPerSec(refill), tokens(cap), last(std::chrono::steady_clock::now()) {}

    bool allow() {
        auto now = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(now - last).count();
        tokens = std::min(capacity, tokens + elapsed * refillPerSec);
        last = now;
        if (tokens >= 1.0) { tokens -= 1.0; return true; }
        return false;
    }
};

int main() {
    TokenBucket b(3.0, 1.0);
    for (int i = 1; i <= 4; i++)
        std::cout << "{\\"call\\": " << i << ", \\"allowed\\": " << (b.allow() ? "true" : "false") << "}\\n";
    return 0;
}
""",
        "rust": """// rate-limiter.rs
use std::time::Instant;

struct TokenBucket {
    capacity: f64,
    refill_per_sec: f64,
    tokens: f64,
    last: Instant,
}

impl TokenBucket {
    fn new(cap: f64, refill: f64) -> Self {
        Self { capacity: cap, refill_per_sec: refill, tokens: cap, last: Instant::now() }
    }

    fn allow(&mut self) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last).as_secs_f64();
        self.tokens = self.capacity.min(self.tokens + elapsed * self.refill_per_sec);
        self.last = now;
        if self.tokens >= 1.0 { self.tokens -= 1.0; return true; }
        false
    }
}

fn main() {
    let mut b = TokenBucket::new(3.0, 1.0);
    for i in 1..=4 {
        println!("{{\"call\": {}, \"allowed\": {}}}", i, b.allow());
    }
}
""",
    },
    "feature-flag-service": {
        "typescript": """// flag.ts
interface Flag {
  key: string;
  enabled: boolean;
  allowlist?: string[];
  rollout?: number;
}

class FlagService {
  private flags = new Map<string, Flag>();

  register(flag: Flag) { this.flags.set(flag.key, flag); }

  isOn(key: string, userId: string): boolean {
    const f = this.flags.get(key);
    if (!f || !f.enabled) return false;
    if (f.allowlist?.includes(userId)) return true;
    if (f.rollout && f.rollout > 0) {
      let hash = 0;
      for (let i = 0; i < userId.length; i++) {
        hash = (hash << 5) - hash + userId.charCodeAt(i);
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
console.log({ flag: "new-checkout", userId: "u_42", result: s.isOn("new-checkout", "u_42") });
console.log({ flag: "dark-mode",    userId: "u_7",  result: s.isOn("dark-mode",    "u_7") });
""",
        "go": """// flag.go
package main

import "fmt"

type Flag struct {
\tKey, Allowlist string
\tEnabled        bool
\tAllowlistSlice []string
\tRollout        int
}

type FlagSvc struct{ flags map[string]Flag }

func NewSvc() *FlagSvc { return &FlagSvc{flags: make(map[string]Flag)} }
func (s *FlagSvc) Register(f Flag) { s.flags[f.Key] = f }
func (s *FlagSvc) IsOn(key, uid string) bool {
\tf, ok := s.flags[key]
\tif !ok || !f.Enabled { return false }
\tfor _, u := range f.AllowlistSlice { if u == uid { return true } }
\tif f.Rollout > 0 { var h int; for _, c := range uid { h += int(c) }; return h%100 < f.Rollout }
\treturn true
}

func main() {
\ts := NewSvc()
\ts.Register(Flag{Key: "new-checkout", Enabled: true, AllowlistSlice: []string{"u_42"}})
\ts.Register(Flag{Key: "dark-mode", Enabled: true, Rollout: 50})
\tfmt.Printf(`{"flag":"new-checkout","userId":"u_42","result":%v}\\n`, s.IsOn("new-checkout", "u_42"))
\tfmt.Printf(`{"flag":"dark-mode","userId":"u_7","result":%v}\\n`, s.IsOn("dark-mode", "u_7"))
}
""",
        "java": """// Solution.java
import java.util.*;

class FlagService {
    private Map<String, Map<String, Object>> flags = new HashMap<>();

    void register(String key, boolean enabled, List<String> allowlist, int rollout) {
        Map<String, Object> f = new HashMap<>();
        f.put("enabled", enabled);
        f.put("allowlist", allowlist);
        f.put("rollout", rollout);
        flags.put(key, f);
    }

    boolean isOn(String key, String userId) {
        Map<String, Object> f = flags.get(key);
        if (f == null || !(boolean)f.get("enabled")) return false;
        List<String> al = (List<String>)f.get("allowlist");
        if (al != null && al.contains(userId)) return true;
        int rollout = (int)f.get("rollout");
        if (rollout > 0) {
            int h = 0;
            for (char c : userId.toCharArray()) h += c;
            return h % 100 < rollout;
        }
        return true;
    }
}

public class Solution {
    public static void main(String[] args) {
        FlagService s = new FlagService();
        s.register("new-checkout", true, Arrays.asList("u_42"), 0);
        s.register("dark-mode", true, Collections.emptyList(), 50);
        System.out.printf("{\\"flag\\":\\"new-checkout\\",\\"userId\\":\\"u_42\\",\\"result\\":%b}%n", s.isOn("new-checkout", "u_42"));
        System.out.printf("{\\"flag\\":\\"dark-mode\\",\\"userId\\":\\"u_7\\",\\"result\\":%b}%n", s.isOn("dark-mode", "u_7"));
    }
}
""",
        "cpp": """// flag.cpp
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

struct Flag {
    bool enabled;
    std::vector<std::string> allowlist;
    int rollout = 0;
};

class FlagService {
    std::map<std::string, Flag> flags;
public:
    void registerFlag(const std::string& key, Flag f) { flags[key] = f; }

    bool isOn(const std::string& key, const std::string& uid) {
        auto it = flags.find(key);
        if (it == flags.end() || !it->second.enabled) return false;
        auto& f = it->second;
        if (std::find(f.allowlist.begin(), f.allowlist.end(), uid) != f.allowlist.end()) return true;
        if (f.rollout > 0) {
            int h = 0;
            for (char c : uid) h += c;
            return h % 100 < f.rollout;
        }
        return true;
    }
};

int main() {
    FlagService s;
    s.registerFlag("new-checkout", {true, {"u_42"}, 0});
    s.registerFlag("dark-mode", {true, {}, 50});
    std::cout << R"({"flag":"new-checkout","userId":"u_42","result":)" << (s.isOn("new-checkout","u_42") ? "true" : "false") << "}\\n";
    std::cout << R"({"flag":"dark-mode","userId":"u_7","result":)" << (s.isOn("dark-mode","u_7") ? "true" : "false") << "}\\n";
    return 0;
}
""",
        "rust": """// flag.rs
use std::collections::HashMap;

struct FlagService {
    flags: HashMap<String, (bool, Vec<String>, u8)>, // (enabled, allowlist, rollout%)
}

impl FlagService {
    fn new() -> Self { Self { flags: HashMap::new() } }

    fn register(&mut self, key: &str, enabled: bool, allowlist: Vec<&str>, rollout: u8) {
        self.flags.insert(key.to_string(), (enabled, allowlist.iter().map(|s| s.to_string()).collect(), rollout));
    }

    fn is_on(&self, key: &str, uid: &str) -> bool {
        if let Some((enabled, allowlist, rollout)) = self.flags.get(key) {
            if !enabled { return false; }
            if allowlist.iter().any(|u| u == uid) { return true; }
            if *rollout > 0 {
                let h: u32 = uid.chars().map(|c| c as u32).sum();
                return h % 100 < *rollout as u32;
            }
            return true;
        }
        false
    }
}

fn main() {
    let mut s = FlagService::new();
    s.register("new-checkout", true, vec!["u_42"], 0);
    s.register("dark-mode", true, vec![], 50);
    println!("{{\"flag\":\"new-checkout\",\"userId\":\"u_42\",\"result\":{}}}", s.is_on("new-checkout", "u_42"));
    println!("{{\"flag\":\"dark-mode\",\"userId\":\"u_7\",\"result\":{}}}", s.is_on("dark-mode", "u_7"));
}
""",
    },
}

# Generic algorithm starters for all CLI challenges that only have JS/Python
GENERIC_ALGO_LANGS = {
    "typescript": lambda slug: f"""import * as fs from 'fs';

const input = JSON.parse(fs.readFileSync(0, 'utf-8').trim());

// TODO: Implement your {slug.replace('-', ' ')} solution
// Input is already parsed from JSON stdin
console.log(JSON.stringify({{ result: null }}));
""",
    "go": lambda slug: f"""package main

import (
\t"encoding/json"
\t"os"
)

func main() {{
\tvar input interface{{}}
\tjson.NewDecoder(os.Stdin).Decode(&input)

\t// TODO: Implement your {slug.replace('-', ' ')} solution
\t// input is the parsed JSON from stdin
\tjson.NewEncoder(os.Stdout).Encode(map[string]interface{{{{"result": nil}}}})
}}
""",
    "java": lambda slug: f"""import java.util.*;
import java.io.*;

public class Solution {{
    public static void main(String[] args) throws Exception {{
        Scanner sc = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) sb.append(sc.nextLine());
        String inputJson = sb.toString().trim();

        // TODO: Implement your {slug.replace('-', ' ')} solution
        // inputJson contains the raw JSON input
        System.out.println("{{\\\"result\\\": null}}");
    }}
}}
""",
    "cpp": lambda slug: f"""#include <iostream>
#include <sstream>
#include <string>

int main() {{
    std::ostringstream ss;
    ss << std::cin.rdbuf();
    std::string inputJson = ss.str();

    // TODO: Implement your {slug.replace('-', ' ')} solution
    // inputJson contains the raw JSON input
    std::cout << "{{\\\"result\\\": null}}" << std::endl;
    return 0;
}}
""",
    "rust": lambda slug: f"""use std::io::{{self, Read}};

fn main() {{
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let input_json = input.trim();

    // TODO: Implement your {slug.replace('-', ' ')} solution
    // input_json contains the raw JSON input string
    println!("{{{{\\\"result\\\": null}}}}");
}}
""",
}


def update_challenge(doc):
    slug = doc['slug']
    runtime = doc.get('runtime', '')
    sc = doc.get('starter_code') or {}
    updates = {}

    if runtime == 'algorithm':
        # Add missing language starters
        rich = RICH_STARTERS.get(slug, {})
        for lang, gen_fn in GENERIC_ALGO_LANGS.items():
            if lang not in sc:
                # Use rich starter if available, else generate generic
                updates[f'starter_code.{lang}'] = rich.get(lang, gen_fn(slug))

    elif runtime in ('api', 'fullstack'):
        # API challenges: multi-file format, skip
        pass

    elif runtime in ('frontend', 'devops'):
        # Frontend/DevOps: single html/multi file, skip
        pass

    return updates


total_updated = 0
for doc in col.find({}):
    updates = update_challenge(doc)
    if updates:
        col.update_one({'_id': doc['_id']}, {'$set': updates})
        keys = [k.replace('starter_code.', '') for k in updates.keys()]
        print(f"  ✓ {doc['slug']:40s} + {keys}")
        total_updated += 1
    else:
        print(f"  - {doc['slug']:40s} (no changes)")

print(f"\nDone! Updated {total_updated} challenges.")
