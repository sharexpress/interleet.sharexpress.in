/**
 * Interleet MongoDB Shell (mongosh) Seeder Script
 * 
 * This script seeds 50+ diverse engineering challenges directly into MongoDB.
 * 
 * HOW TO RUN:
 * mongosh mongodb://localhost:27017/interleet seed_challenges_mongosh.js
 */

// Connect to 'interleet' database
const currentDbName = db.getName();
const targetDb = currentDbName === 'test' || currentDbName === 'admin' 
  ? db.getSiblingDB('interleet') 
  : db;

print(`Seeding challenges into database: "${targetDb.getName()}"...`);

const challenges = [
  // ==================== BACKEND CODING CHALLENGES ====================
  {
    title: "Implement an LRU Cache",
    slug: "lru-cache-implementation",
    domain: "Backend",
    difficulty: "Medium",
    minutes: 45,
    xp: 350,
    tags: ["Data Structures", "Caching", "JavaScript"],
    summary: "Design and implement a Least Recently Used (LRU) cache with O(1) get and put operations.",
    description: "Implement the LRUCache class:\n- LRUCache(capacity) initializes the LRU cache with positive size capacity.\n- get(key) returns the value of the key if it exists, otherwise returns -1.\n- put(key, value) updates the value of the key if it exists. Otherwise, adds the key-value pair. If the number of keys exceeds the capacity, evict the least recently used key.",
    starter_code: {
      javascript: "class LRUCache {\n  constructor(capacity) {\n    this.capacity = capacity;\n    this.cache = new Map();\n  }\n  get(key) {\n    if (!this.cache.has(key)) return -1;\n    const val = this.cache.get(key);\n    this.cache.delete(key);\n    this.cache.set(key, val);\n    return val;\n  }\n  put(key, value) {\n    if (this.cache.has(key)) {\n      this.cache.delete(key);\n    } else if (this.cache.size >= this.capacity) {\n      const oldestKey = this.cache.keys().next().value;\n      this.cache.delete(oldestKey);\n    }\n    this.cache.set(key, value);\n  }\n}\n",
      python: "class LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = {}\n        self.order = []\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.order.remove(key)\n        self.order.append(key)\n        return self.cache[key]\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.order.remove(key)\n        elif len(self.cache) >= self.capacity:\n            oldest = self.order.pop(0)\n            del self.cache[oldest]\n        self.cache[key] = value\n        self.order.append(key)\n"
    },
    test_cases: [
      { id: "lru-tc-1", name: "basic get/put cache eviction", stdin: "2\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\n", expected_output: "1\n-1\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Implement Trie (Prefix Tree)",
    slug: "implement-trie-prefix-tree",
    domain: "Backend",
    difficulty: "Medium",
    minutes: 30,
    xp: 250,
    tags: ["Data Structures", "Strings", "Algorithms"],
    summary: "Implement a trie data structure supporting insert, search, and startsWith operations.",
    description: "A trie (pronounced as 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement Trie class.",
    starter_code: {
      javascript: "class TrieNode {\n  constructor() {\n    this.children = {};\n    this.isEnd = false;\n  }\n}\nclass Trie {\n  constructor() {\n    this.root = new TrieNode();\n  }\n  insert(word) {\n    let node = this.root;\n    for (const char of word) {\n      if (!node.children[char]) node.children[char] = new TrieNode();\n      node = node.children[char];\n    }\n    node.isEnd = true;\n  }\n  search(word) {\n    let node = this.root;\n    for (const char of word) {\n      if (!node.children[char]) return false;\n      node = node.children[char];\n    }\n    return node.isEnd;\n  }\n  startsWith(prefix) {\n    let node = this.root;\n    for (const char of prefix) {\n      if (!node.children[char]) return false;\n      node = node.children[char];\n    }\n    return true;\n  }\n}\n",
      python: "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word: str) -> None:\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                node.children[char] = TrieNode()\n            node = node.children[char]\n        node.is_end = True\n    def search(self, word: str) -> bool:\n        node = self.root\n        for char in word:\n            if char not in node.children: return False\n            node = node.children[char]\n        return node.is_end\n    def starts_with(self, prefix: str) -> bool:\n        node = self.root\n        for char in prefix:\n            if char not in node.children: return False\n            node = node.children[char]\n        return True\n"
    },
    test_cases: [
      { id: "trie-tc-1", name: "insert and search prefix tests", stdin: "apple\nsearch apple\nstartsWith app\n", expected_output: "true\ntrue\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Thread-Safe KV Store",
    slug: "thread-safe-kv-store",
    domain: "Backend",
    difficulty: "Hard",
    minutes: 60,
    xp: 450,
    tags: ["Concurrency", "Data Structures", "Thread-Safety"],
    summary: "Design an in-memory key-value store with read/write locks and TTL expiration.",
    description: "Build a thread-safe KV store with expiring keys. Support operations:\n- set(key, val, ttl_ms)\n- get(key)\n- delete(key)\nEnsure reads can happen in parallel but writes lock key-specific items.",
    starter_code: {
      javascript: "class KVStore {\n  constructor() {\n    this.store = new Map();\n  }\n  set(key, val, ttl) {\n    const expiresAt = ttl ? Date.now() + ttl : null;\n    this.store.set(key, { val, expiresAt });\n  }\n  get(key) {\n    if (!this.store.has(key)) return null;\n    const entry = this.store.get(key);\n    if (entry.expiresAt && entry.expiresAt < Date.now()) {\n      this.store.delete(key);\n      return null;\n    }\n    return entry.val;\n  }\n}\n"
    },
    test_cases: [
      { id: "kv-tc-1", name: "basic put get with ttl", stdin: "key1 val1 5000\nget key1\n", expected_output: "val1\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Consistent Hashing Ring Builder",
    slug: "consistent-hashing-ring",
    domain: "Backend",
    difficulty: "Hard",
    minutes: 50,
    xp: 400,
    tags: ["System Architecture", "Distributed Systems", "Hashing"],
    summary: "Implement consistent hashing to distribute requests across dynamic node partitions.",
    description: "Consistent hashing is a mechanism used to map requests to servers. Implement a hash ring supporting `addNode(node)`, `removeNode(node)`, and `getNode(key)`.",
    starter_code: {
      javascript: "class HashRing {\n  constructor(replicas = 3) {\n    this.replicas = replicas;\n    this.ring = [];\n    this.nodes = new Set();\n  }\n  addNode(node) {}\n  removeNode(node) {}\n  getNode(key) {}\n}\n"
    },
    test_cases: [
      { id: "ring-tc-1", name: "add node check mapping", stdin: "nodeA\nkey123\n", expected_output: "nodeA\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Write-Ahead Logging Engine",
    slug: "write-ahead-logger-engine",
    domain: "Backend",
    difficulty: "Hard",
    minutes: 45,
    xp: 380,
    tags: ["Databases", "IO", "Durability"],
    summary: "Write a transactional logging utility that serializes operations before applying to memory state.",
    description: "Write-ahead logging (WAL) guarantees transaction durability. Implement a WAL engine that writes log entries sequentially and replays logs to recover in-memory state after a crash.",
    starter_code: {
      javascript: "class WALEngine {\n  constructor(logFile) {\n    this.logFile = logFile;\n    this.state = {};\n  }\n  commit(op, key, val) {}\n  recover() {}\n}\n"
    },
    test_cases: [
      { id: "wal-tc-1", name: "commit and recover state", stdin: "SET name ant\nCOMMIT\n", expected_output: "ant\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Rate Limiter (Sliding Window Log)",
    slug: "sliding-window-rate-limiter",
    domain: "Backend",
    difficulty: "Medium",
    minutes: 40,
    xp: 300,
    tags: ["APIs", "Security", "Algorithms"],
    summary: "Implement a sliding window log rate limiter that tracks timestamps to block bursts.",
    description: "Design a sliding window log rate limiter. For each request, record the timestamp. Evict timestamps older than the window, and check if the count exceeds limit.",
    starter_code: {
      javascript: "class SlidingRateLimiter {\n  constructor(limit, windowMs) {\n    this.limit = limit;\n    this.windowMs = windowMs;\n    this.logs = new Map();\n  }\n  isAllowed(clientId) {\n    const now = Date.now();\n    if (!this.logs.has(clientId)) this.logs.set(clientId, []);\n    const timestamps = this.logs.get(clientId);\n    while(timestamps.length > 0 && timestamps[0] <= now - this.windowMs) {\n      timestamps.shift();\n    }\n    if (timestamps.length >= this.limit) return false;\n    timestamps.push(now);\n    return true;\n  }\n}\n"
    },
    test_cases: [
      { id: "sl-tc-1", name: "block third request in tight window", stdin: "2 1000\nclient1\nclient1\nclient1\n", expected_output: "true\ntrue\nfalse\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Pub-Sub Messaging Broker",
    slug: "pub-sub-messaging-broker",
    domain: "Backend",
    difficulty: "Medium",
    minutes: 45,
    xp: 320,
    tags: ["Event-Driven", "Asynchronous", "Architecture"],
    summary: "Build an asynchronous publish-subscribe message broker with pattern-matching topics.",
    description: "Build an event broker supporting exact and wildcard topic subscriptions (e.g. subscribing to `orders.*` matches publish to `orders.created` and `orders.cancelled`).",
    starter_code: {
      javascript: "class PubSubBroker {\n  constructor() {\n    this.subscriptions = new Map();\n  }\n  subscribe(topicPattern, callback) {}\n  publish(topic, message) {}\n}\n"
    },
    test_cases: [
      { id: "pub-tc-1", name: "publish matches wildcard", stdin: "subscribe orders.* \npublish orders.created Success\n", expected_output: "Success\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Circular Ring Buffer",
    slug: "circular-ring-buffer",
    domain: "Backend",
    difficulty: "Easy",
    minutes: 25,
    xp: 150,
    tags: ["Data Structures", "Memory", "Algorithms"],
    summary: "Implement a fixed-size queue ring buffer that overwrites oldest entries on overflow.",
    description: "Design a circular queue supporting: `write(item)`, `read()`, `isFull()`, and `isEmpty()`. If full, writes block or overwrite oldest depending on configuration.",
    starter_code: {
      javascript: "class CircularBuffer {\n  constructor(capacity) {\n    this.capacity = capacity;\n    this.buffer = new Array(capacity);\n    this.head = 0;\n    this.tail = 0;\n    this.size = 0;\n  }\n  write(item) {}\n  read() {}\n}\n"
    },
    test_cases: [
      { id: "circ-tc-1", name: "write read ring buffer", stdin: "3\nwrite A\nwrite B\nread\n", expected_output: "A\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Custom JSON Parser",
    slug: "custom-json-parser",
    domain: "Backend",
    difficulty: "Hard",
    minutes: 75,
    xp: 500,
    tags: ["Compilers", "Parsing", "Algorithms"],
    summary: "Write a recursive-descent parser that parses JSON strings into memory objects without eval/JSON.parse.",
    description: "Write a custom lexer and parser to convert a JSON string representation into actual JS primitives, arrays, and nested objects. Handle syntactically invalid exceptions.",
    starter_code: {
      javascript: "function parseJSON(str) {\n  let index = 0;\n  function parseValue() {}\n  return parseValue();\n}\n"
    },
    test_cases: [
      { id: "json-tc-1", name: "parse basic object", stdin: '{"a":1,"b":[true,null]}\n', expected_output: '{"a":1,"b":[true,null]}\n', hidden: false, weight: 1 }
    ]
  },
  {
    title: "Topological Task runner",
    slug: "topological-task-runner",
    domain: "Backend",
    difficulty: "Medium",
    minutes: 40,
    xp: 320,
    tags: ["Graphs", "Algorithms", "Task Queues"],
    summary: "Sequentially run tasks based on directional dependency graphs resolving circular paths.",
    description: "Given a list of tasks with directional prerequisite dependencies (e.g. A needs B), build a execution schedule ensuring topological order. Throw error on deadlock.",
    starter_code: {
      javascript: "function scheduleTasks(tasks, dependencies) {\n  return [];\n}\n"
    },
    test_cases: [
      { id: "topo-tc-1", name: "simple dependencies sequence", stdin: "A,B,C\nB->A\nC->B\n", expected_output: "C,B,A\n", hidden: false, weight: 1 }
    ]
  },

  // ==================== SYSTEM DESIGN CHALLENGES ====================
  {
    title: "Design TinyURL URL Shortener",
    slug: "design-url-shortener",
    domain: "System Design",
    difficulty: "Easy",
    minutes: 45,
    xp: 150,
    tags: ["Caching", "SQL/NoSQL", "HA"],
    summary: "Architect a scalable service to shorten URLs with high read-to-write ratio.",
    description: "Design a high throughput, low latency URL shortening service (like Bitly). Ensure redirect speeds are under 50ms, handles millions of daily operations, and prevents URL collisions.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design YouTube Video Platform",
    slug: "design-youtube-streaming",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 90,
    xp: 500,
    tags: ["CDN", "Transcoding", "Blob Storage"],
    summary: "Design a video sharing and streaming platform handling high-volume video processing and low-latency global delivery.",
    description: "Design a video streaming platform (like YouTube or Netflix). Detail transcoding worker pipelines, metadata databases, CDN caching edge nodes, and adaptive bitrate streaming logic (DASH/HLS).",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design Slack Messaging App",
    slug: "design-slack-chat",
    domain: "System Design",
    difficulty: "Medium",
    minutes: 60,
    xp: 350,
    tags: ["WebSockets", "Presence", "PubSub"],
    summary: "Architect a real-time messaging server supporting multiple channels, read status, and presence indications.",
    description: "Design a messaging chat system like Slack. Detail gateway WebSocket connections, real-time message routing, user online status heartbeat management, and offline message storage.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design a Distributed Web Crawler",
    slug: "design-distributed-web-crawler",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 90,
    xp: 600,
    tags: ["Distributed Queue", "Deduplication", "DNS Cache"],
    summary: "Design a web crawling service that scrapes billions of pages, handles deduplication, and respects robots.txt.",
    description: "Design a high-scale crawler. Detail URL frontier management, politeness delays, document checksum fingerprint storage to avoid duplicate content, and partition distribution across worker nodes.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design real-time Ad Click Aggregator",
    slug: "design-ad-click-aggregator",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 120,
    xp: 700,
    tags: ["Stream Processing", "Kafka", "Data Warehousing"],
    summary: "Design an analytics system collecting millions of ad click events per second with high accuracy.",
    description: "Design an click logging system. Address challenges including idempotency (preventing double clicks billing), stream processing windowing (Flink/Spark), cold vs hot path analytics, and partition sharding.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design Uber Ride-Hailing",
    slug: "design-uber-ride-hailing",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 90,
    xp: 550,
    tags: ["Geohashing", "Quadtree", "Real-time"],
    summary: "Architect a system to track driver positions and match riders to nearby drivers dynamically.",
    description: "Design a location-aware matching engine. Address driver location updates frequency, spatial queries optimizations using Geohashing or Quadtrees, trip dispatching state flow, and dynamic price adjustments.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design Ticketmaster Booking",
    slug: "design-ticketmaster-booking",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 90,
    xp: 500,
    tags: ["Distributed Locks", "Transactions", "Queueing"],
    summary: "Architect a high-concurrency ticket selling system preventing double booking during viral sales.",
    description: "Design a ticketing service. Tackle handling extreme sudden traffic spikes, distributed locking strategies on seat reservations, shopping cart session timeouts, and database consistency constraints.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design WhatsApp Chat System",
    slug: "design-whatsapp-chat",
    domain: "System Design",
    difficulty: "Medium",
    minutes: 60,
    xp: 380,
    tags: ["E2E Encryption", "WebSockets", "NoSQL"],
    summary: "Design WhatsApp's end-to-end encrypted messaging engine scaling to 2B users worldwide.",
    description: "Design a decentralized chat client-server interface. Discuss session initialization, Signal Protocol double-ratchet keys store, delivery confirmation tickers (sent, delivered, read), and multimedia uploads.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design Google Drive Storage",
    slug: "design-google-drive",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 80,
    xp: 450,
    tags: ["File Sync", "Block Storage", "Metadata Store"],
    summary: "Architect a distributed cloud storage service supporting automatic file synchronization and delta updates.",
    description: "Design a sync server like Google Drive or Dropbox. Detail block-level file chunking, checksum validations, delta indexing to upload only modified blocks, metadata tracking, and conflict resolutions.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Design Netflix Video Recommendations",
    slug: "design-netflix-recommendations",
    domain: "System Design",
    difficulty: "Hard",
    minutes: 90,
    xp: 500,
    tags: ["Machine Learning", "Databases", "Data Pipelines"],
    summary: "Design a personalized content recommendation engine processing real-time user stream activities.",
    description: "Design a movie recommendation pipeline. Discuss offline model training (collaborative filtering, deep learning), online candidate generation, vector databases, search relevance, and event aggregator logs.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },

  // ==================== DEVOPS CHALLENGES ====================
  {
    title: "Parse Semantic Versions (SemVer)",
    slug: "parse-semantic-versions",
    domain: "DevOps",
    difficulty: "Easy",
    minutes: 30,
    xp: 150,
    tags: ["SemVer", "Regex", "Formatting"],
    summary: "Create a utility to parse, compare, and sort semver release notations.",
    description: "Parse semantic versions string `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`. Implement a comparator function returning -1, 0, or 1 to support sort ordering.",
    starter_code: {
      javascript: "function compareSemVer(v1, v2) {\n  return 0;\n}\n"
    },
    test_cases: [
      { id: "sem-tc-1", name: "simple version compare", stdin: "1.2.3 1.2.4\n", expected_output: "-1\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Dockerfile Instruction Parser",
    slug: "dockerfile-instruction-parser",
    domain: "DevOps",
    difficulty: "Medium",
    minutes: 40,
    xp: 280,
    tags: ["Docker", "Parsers", "Containers"],
    summary: "Write a script to parse instructions from a Dockerfile and output structural AST nodes.",
    description: "Write a parser extracting instruction blocks like `FROM`, `RUN`, `ENV`, `COPY`, `EXPOSE` from raw Dockerfiles. Extract base image names and check for common security misconfigurations.",
    starter_code: {
      javascript: "function parseDockerfile(contents) {\n  return {};\n}\n"
    },
    test_cases: [
      { id: "dock-tc-1", name: "extract base image", stdin: "FROM node:20\nRUN npm install\n", expected_output: "node:20\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Cron Expression Solver",
    slug: "cron-expression-solver",
    domain: "DevOps",
    difficulty: "Hard",
    minutes: 60,
    xp: 400,
    tags: ["Cron", "Parsing", "Timezones"],
    summary: "Parse standard 5-field crontab string expressions and determine the next execution timestamps.",
    description: "Given a crontab schedule: `* * * * *` (minute, hour, day of month, month, day of week), parse boundaries and list next 5 UTC times the job triggers relative to a given starting timestamp.",
    starter_code: {
      javascript: "function getNextCronRuns(cronExpr, startTime) {\n  return [];\n}\n"
    },
    test_cases: [
      { id: "cron-tc-1", name: "every minute runs", stdin: "*/1 * * * * 2026-06-08T00:00:00Z\n", expected_output: "2026-06-08T00:01:00Z\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Path Routing Wildcard Matcher",
    slug: "path-routing-matcher",
    domain: "DevOps",
    difficulty: "Medium",
    minutes: 35,
    xp: 250,
    tags: ["HTTP Router", "Regex", "Infrastructure"],
    summary: "Match request paths against wildcard routing definitions extracting parameters.",
    description: "Write a router path matcher matching paths like `/users/:id/posts/*` and extracting values like `{ id: '42' }` and wildcard remainders.",
    starter_code: {
      javascript: "function matchRoute(pattern, path) {\n  return null;\n}\n"
    },
    test_cases: [
      { id: "route-tc-1", name: "extract route parameter id", stdin: "/users/:id/profile /users/10/profile\n", expected_output: "10\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "YAML Syntax Validator",
    slug: "yaml-syntax-validator",
    domain: "DevOps",
    difficulty: "Medium",
    minutes: 40,
    xp: 280,
    tags: ["YAML", "Parsers", "Validation"],
    summary: "Verify simple YAML syntax spacing indentation levels and output structure blocks.",
    description: "Write a simple validation checker that flags invalid spaces or incorrect structure hierarchies in basic YAML config files commonly used in Kubernetes manifests.",
    starter_code: {
      javascript: "function validateYAML(yamlStr) {\n  return true;\n}\n"
    },
    test_cases: [
      { id: "yaml-tc-1", name: "detect malformed indentation", stdin: "metadata:\n  name: app\n    labels:\n", expected_output: "false\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Health Status Aggregator",
    slug: "health-status-aggregator",
    domain: "DevOps",
    difficulty: "Easy",
    minutes: 20,
    xp: 120,
    tags: ["Monitoring", "APIs", "Reliability"],
    summary: "Aggregate statuses from several downstream dependency checks determining main server response.",
    description: "Given a JSON array of subcomponent health states (db, redis, third-party api), output overall server status (healthy, degraded, critical) based on service dependency weights.",
    starter_code: {
      javascript: "function aggregateHealth(components) {\n  return 'healthy';\n}\n"
    },
    test_cases: [
      { id: "health-tc-1", name: "aggregate database down", stdin: '[{"name":"db","critical":true,"status":"down"}]\n', expected_output: "critical\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Nginx Log Traffic Analyzer",
    slug: "nginx-log-analyzer",
    domain: "DevOps",
    difficulty: "Medium",
    minutes: 45,
    xp: 300,
    tags: ["Data Mining", "Logs", "Nginx"],
    summary: "Parse access logs in Common Log Format extracting stats like throughput, 500 error counts, and top IPs.",
    description: "Create an ingestion script that parses server access log arrays. Extract and count response status distributions (2xx, 4xx, 5xx) and list the top 3 requesting IPs.",
    starter_code: {
      javascript: "function analyzeLogs(logLines) {\n  return {};\n}\n"
    },
    test_cases: [
      { id: "log-tc-1", name: "count 404 logs", stdin: '127.0.0.1 - - [08/Jun/2026:12:00:00 +0000] "GET /404 HTTP/1.1" 404 15\n', expected_output: "1\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Subnet CIDR IP Range Checker",
    slug: "subnet-cidr-ip-checker",
    domain: "DevOps",
    difficulty: "Medium",
    minutes: 30,
    xp: 250,
    tags: ["Networking", "APIs", "Subnets"],
    summary: "Write a utility to check if a specific IPv4 belongs inside a given CIDR block range.",
    description: "Implement a function parsing CIDR ranges like `192.168.1.0/24`. Check if input IPs belong to this network range by calculating bitwise subnet masks.",
    starter_code: {
      javascript: "function ipInCIDR(ip, cidr) {\n  return false;\n}\n"
    },
    test_cases: [
      { id: "cidr-tc-1", name: "ip in local subnet range", stdin: "192.168.1.50 192.168.1.0/24\n", expected_output: "true\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Conventional Git Commit Lint",
    slug: "conventional-git-commit-lint",
    domain: "DevOps",
    difficulty: "Easy",
    minutes: 25,
    xp: 150,
    tags: ["Git", "Linting", "Automations"],
    summary: "Enforce Conventional Commits patterns on incoming git messages.",
    description: "Implement a linter to validate if a commit matches: `<type>(<scope>): <subject>`. Allowed types include `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.",
    starter_code: {
      javascript: "function lintCommit(message) {\n  return false;\n}\n"
    },
    test_cases: [
      { id: "lint-tc-1", name: "valid feature scope commit", stdin: "feat(auth): add google button\n", expected_output: "true\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Env File Secrets Sanitizer",
    slug: "env-file-secrets-sanitizer",
    domain: "DevOps",
    difficulty: "Easy",
    minutes: 20,
    xp: 120,
    tags: ["Security", "Scripting", "Regex"],
    summary: "Scan and strip potential private credential keys from configuration files before commit.",
    description: "Write a script checking `.env` variable key names for keywords like `KEY`, `SECRET`, `PASSWORD`, `TOKEN`. Replace values with asterisks `***`.",
    starter_code: {
      javascript: "function sanitizeEnv(contents) {\n  return '';\n}\n"
    },
    test_cases: [
      { id: "env-tc-1", name: "redact stripe key secret", stdin: "STRIPE_SECRET=sk_live_12345\n", expected_output: "STRIPE_SECRET=***\n", hidden: false, weight: 1 }
    ]
  },

  // ==================== FRONTEND CHALLENGES ====================
  {
    title: "Virtual Scrolling List Component",
    slug: "virtual-scrolling-list-component",
    domain: "Frontend",
    difficulty: "Hard",
    minutes: 90,
    xp: 450,
    tags: ["Performance", "React/Vue", "Optimization"],
    summary: "Create a list container rendering only visible nodes based on list offsets.",
    description: "Implement a virtualization container. Given 100k records and parent container heights, calculate start index, end index, offset translate, and buffer window rendering.",
    supports_system_design_canvas: false,
    supports_code_execution: true,
    starter_code: {
      javascript: "function calculateVisibleIndices(totalCount, rowHeight, scrollTop, containerHeight, bufferCount = 2) {\n  return {\n    startIndex: 0,\n    endIndex: 0,\n    offsetTop: 0\n  };\n}\n"
    },
    test_cases: [
      { id: "virt-tc-1", name: "calc visible bounds simple", stdin: "1000 50 100 200 0\n", expected_output: '{"startIndex":2,"endIndex":6,"offsetTop":100}\n', hidden: false, weight: 1 }
    ]
  },
  {
    title: "Modal Transitions Animation",
    slug: "modal-transitions-animator",
    domain: "Frontend",
    difficulty: "Medium",
    minutes: 40,
    xp: 260,
    tags: ["CSS Animations", "UX", "Web-API"],
    summary: "Build a state controller tracking transition animations during element mounting.",
    description: "When rendering modals, you must delay DOM unmounting until leave animations complete. Build an orchestrator tracking dynamic animation stages: `MOUNTED`, `ENTERING`, `ENTERED`, `LEAVING`, `UNMOUNTED`.",
    starter_code: {
      javascript: "class ModalTransitionController {\n  constructor(onStateChange) {}\n  open() {}\n  close(animationDurationMs) {}\n}\n"
    },
    test_cases: [
      { id: "mod-tc-1", name: "transition phases updates", stdin: "open close 300\n", expected_output: "MOUNTED->ENTERING->ENTERED->LEAVING->UNMOUNTED\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Toast Queue Manager",
    slug: "toast-queue-manager",
    domain: "Frontend",
    difficulty: "Medium",
    minutes: 35,
    xp: 220,
    tags: ["State Management", "Design System", "DOM"],
    summary: "Implement a debounced and auto-evicting notification toast state manager.",
    description: "Build a manager handling concurrent notification toasts. Evict toasts after specific timeouts, handle maximum visible limits (e.g. max 5 stacked toasts), and queue incoming ones.",
    starter_code: {
      javascript: "class ToastQueueManager {\n  constructor(maxToasts = 5) {\n    this.queue = [];\n    this.active = [];\n    this.maxToasts = maxToasts;\n  }\n  addToast(toast) {}\n  dismissToast(id) {}\n}\n"
    },
    test_cases: [
      { id: "toast-tc-1", name: "evict toast queue overflow", stdin: "add A add B add C max_2\n", expected_output: "B,C\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Debounced Query Suggestions Hook",
    slug: "debounced-suggestions-hook",
    domain: "Frontend",
    difficulty: "Easy",
    minutes: 25,
    xp: 180,
    tags: ["React Hooks", "Debounce", "APIs"],
    summary: "Write a react/javascript custom state tracker debouncing fast inputs.",
    description: "Design a debounce state hook. Prevent triggering expensive API requests on every keyboard keypress. Debounce suggestions for at least 300ms.",
    starter_code: {
      javascript: "function useDebounce(value, delayMs) {\n  // Implement state debouncing logic\n  return value;\n}\n"
    },
    test_cases: [
      { id: "deb-tc-1", name: "debounce value updates", stdin: "inputA inputB 300\n", expected_output: "inputB\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Nested File Folder Directory tree",
    slug: "nested-file-directory-tree",
    domain: "Frontend",
    difficulty: "Hard",
    minutes: 60,
    xp: 400,
    tags: ["Data Mapping", "Recursion", "UI Structure"],
    summary: "Convert linear flat file paths arrays into hierarchical nested folder objects.",
    description: "Transform an array of files like `['/src/components/button.jsx', '/src/index.js']` into a recursive node tree structure suitable for rendering sidebar folder collapse panels.",
    starter_code: {
      javascript: "function buildFileTree(flatPaths) {\n  return {};\n}\n"
    },
    test_cases: [
      { id: "tree-tc-1", name: "build simple tree from array", stdin: "/a/b/file.txt\n", expected_output: '{"name":"a","children":[{"name":"b","children":[{"name":"file.txt"}]}]}\n', hidden: false, weight: 1 }
    ]
  },
  {
    title: "Star Rating Feedback Engine",
    slug: "star-rating-feedback-engine",
    domain: "Frontend",
    difficulty: "Easy",
    minutes: 20,
    xp: 120,
    tags: ["DOM Events", "UI Layout", "Accessibility"],
    summary: "Manage selected rating and hover indices for a 5-star feedback rating widget.",
    description: "Tackle UI states for ratings. Output calculated hover index state, selected index state, and clear options when clicking outside the boundary.",
    starter_code: {
      javascript: "class StarRatingWidget {\n  constructor(totalStars = 5) {\n    this.rating = 0;\n    this.hoverRating = 0;\n  }\n  hover(starIndex) {}\n  click(starIndex) {}\n}\n"
    },
    test_cases: [
      { id: "star-tc-1", name: "hover selection state test", stdin: "hover 3 click 2\n", expected_output: "selected: 2, hovered: 3\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "CSS Grid Auto-placement Calculator",
    slug: "css-grid-autoplacement-calc",
    domain: "Frontend",
    difficulty: "Hard",
    minutes: 70,
    xp: 380,
    tags: ["Layout Algorithms", "CSS Grid", "Performance"],
    summary: "Simulate CSS Grid sparse/dense layout packing algorithm on grid tracks.",
    description: "Build a simplified version of CSS grid auto-placement. Given columns count, item spans (width x height), simulate grid matrix allocation under sparse/dense rules.",
    starter_code: {
      javascript: "function calculateGridPlacements(items, columnsCount, packingMode = 'sparse') {\n  return [];\n}\n"
    },
    test_cases: [
      { id: "grid-tc-1", name: "place span items sparse", stdin: "2x1 1x2\n", expected_output: "item1:[0,0],item2:[1,0]\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Custom Form Validator Engine",
    slug: "custom-form-validator-engine",
    domain: "Frontend",
    difficulty: "Medium",
    minutes: 45,
    xp: 300,
    tags: ["Form Validation", "Zod-clone", "Data Parsing"],
    summary: "Write a validation parsing schema supporting nested fields, numbers bounds, and regex emails.",
    description: "Build a mini validation library from scratch (like a simplified Zod). Support `.string()`, `.number()`, `.min()`, `.max()`, and object nesting schemas.",
    starter_code: {
      javascript: "class Validator {\n  string() {}\n  number() {}\n  object(schema) {}\n}\n"
    },
    test_cases: [
      { id: "val-tc-1", name: "validate simple schema properties", stdin: "string min_3 ant\n", expected_output: "true\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Markdown to HTML Parser",
    slug: "markdown-to-html-parser",
    domain: "Frontend",
    difficulty: "Medium",
    minutes: 40,
    xp: 280,
    tags: ["Regex", "Compilers", "Markup"],
    summary: "Convert basic markdown bold, italic, headings and lists syntax to valid HTML.",
    description: "Write a markdown string parser. Convert `# header` to `<h1>header</h1>`, `**bold**` to `<strong>bold</strong>`, and code blocks to `<pre><code>`.",
    starter_code: {
      javascript: "function parseMarkdown(mdText) {\n  return '';\n}\n"
    },
    test_cases: [
      { id: "md-tc-1", name: "parse headers and bold", stdin: "# Hello **World**\n", expected_output: "<h1>Hello <strong>World</strong></h1>\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Responsive Grid Breakpoint Helper",
    slug: "responsive-breakpoint-helper",
    domain: "Frontend",
    difficulty: "Easy",
    minutes: 15,
    xp: 100,
    tags: ["Responsive Design", "Media Queries", "UI Rules"],
    summary: "Map viewport widths to Tailwind-style breakpoints returning column span variables.",
    description: "Given a layout config for breakpoints (sm, md, lg, xl) and current viewport window size, return the active breakpoint label and grid column width layout percentages.",
    starter_code: {
      javascript: "function getGridBreakpoint(width) {\n  return 'sm';\n}\n"
    },
    test_cases: [
      { id: "bp-tc-1", name: "md width breakpoint evaluation", stdin: "800\n", expected_output: "md\n", hidden: false, weight: 1 }
    ]
  },

  // ==================== DATABASES CHALLENGES ====================
  {
    title: "Parse SQL SELECT query fields",
    slug: "parse-sql-select-query",
    domain: "Databases",
    difficulty: "Medium",
    minutes: 40,
    xp: 280,
    tags: ["SQL", "Parsers", "AST"],
    summary: "Extract SELECT targets, from tables, and basic equality where clauses.",
    description: "Implement a SQL query parser. Given a standard select query string, parse out the fields array, table name, and extract where keys and target lookup values.",
    starter_code: {
      javascript: "function parseSQLSelect(sqlStr) {\n  return {};\n}\n"
    },
    test_cases: [
      { id: "sql-tc-1", name: "parse query projection attributes", stdin: "SELECT name, age FROM users WHERE status = 'active'\n", expected_output: '{"fields":["name","age"],"table":"users","where":{"status":"active"}}\n', hidden: false, weight: 1 }
    ]
  },
  {
    title: "CSV Storage Data Query Engine",
    slug: "csv-storage-query-engine",
    domain: "Databases",
    difficulty: "Medium",
    minutes: 45,
    xp: 300,
    tags: ["File Database", "Data Processing", "I/O"],
    summary: "Run selection and sorting lookups on simple mock file system CSV structures.",
    description: "Write a CSV query parser. Support loading rows from raw CSV text and running queries like `select('name').where('age', '>', 25).sort('name')`.",
    starter_code: {
      javascript: "class CSVDatabase {\n  constructor(csvText) {\n    this.rows = [];\n  }\n  query(projection, filters, sortBy) {\n    return [];\n  }\n}\n"
    },
    test_cases: [
      { id: "csv-tc-1", name: "select fields with comparison filters", stdin: "id,name,age\n1,ant,30\n2,bob,20\n", expected_output: "ant\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Database Index B-Tree Simulator",
    slug: "btree-index-insertion-simulator",
    domain: "Databases",
    difficulty: "Hard",
    minutes: 75,
    xp: 500,
    tags: ["Tree Structures", "Index Algorithms", "Memory"],
    summary: "Simulate keys indexing insertions in B-Tree blocks handling node splits.",
    description: "Tackle indexing structures. Given key values array and B-Tree order degree M, simulate block partitioning and return node hierarchy output lists.",
    starter_code: {
      javascript: "class BTreeIndex {\n  constructor(orderDegree = 3) {\n    this.root = null;\n  }\n  insert(key) {}\n}\n"
    },
    test_cases: [
      { id: "btree-tc-1", name: "node splitting order degree 3", stdin: "10 20 30\n", expected_output: "root:[20],children:[[10],[30]]\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Database Migration Sequencer",
    slug: "db-migration-sequencer",
    domain: "Databases",
    difficulty: "Medium",
    minutes: 30,
    xp: 240,
    tags: ["Migration Sequence", "Graphs", "Orchestrations"],
    summary: "Calculate migration dependency sequences resolving circular foreign key dependencies.",
    description: "Given database migrations items metadata containing dependency references (e.g. table B has foreign key on table A), sort migration operations sequence correctly.",
    starter_code: {
      javascript: "function sortMigrations(migrationObjects) {\n  return [];\n}\n"
    },
    test_cases: [
      { id: "mig-tc-1", name: "sort ordered table creation migrations", stdin: "B:[A] A:[]\n", expected_output: "A,B\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "Transaction Deadlock Detector",
    slug: "transaction-deadlock-detector",
    domain: "Databases",
    difficulty: "Hard",
    minutes: 50,
    xp: 420,
    tags: ["Lock Manager", "Graphs", "Concurrency"],
    summary: "Implement transactional waits-for graph analyzer catching resource deadlocks.",
    description: "In concurrent SQL databases, locking keys can cause deadlocks. Given transaction lock requests: `T1 holds keyX, T2 wants keyX, T2 holds keyY, T1 wants keyY`, parse lock conflicts, build wait-for graphs, and detect loop cycles.",
    starter_code: {
      javascript: "function detectDeadlock(lockRequests) {\n  return false;\n}\n"
    },
    test_cases: [
      { id: "deadlock-tc-1", name: "detect circular holding requests", stdin: "T1->keyA T2->keyB T2:wait_keyA T1:wait_keyB\n", expected_output: "true\n", hidden: false, weight: 1 }
    ]
  },

  // ==================== APIs CHALLENGES ====================
  {
    title: "HTTP Request Signature Signer",
    slug: "http-request-signature-signer",
    domain: "APIs",
    difficulty: "Medium",
    minutes: 35,
    xp: 250,
    tags: ["HMAC", "API Security", "Hashing"],
    summary: "Calculate HMAC-SHA256 signature hashes for secure server API requests authentication.",
    description: "Implement secure request signing. Given an HTTP request payload, headers string, timestamp, and client secret, generate a SHA256 signature matching AWS/Stripe API styles.",
    starter_code: {
      javascript: "function signRequest(payload, secretKey, timestamp) {\n  return '';\n}\n"
    },
    test_cases: [
      { id: "sign-tc-1", name: "hmac signature generation payload", stdin: "secret_123 2026-06-08T12:00:00Z data\n", expected_output: "valid_sha256_hash_here\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "URL Query String Parser Decoder",
    slug: "url-query-string-parser",
    domain: "APIs",
    difficulty: "Easy",
    minutes: 25,
    xp: 150,
    tags: ["HTTP", "Query Params", "Formatting"],
    summary: "Implement query parameters parsing decoding arrays and nested paths.",
    description: "Write a query parser. Convert string fields `?a=1&b[]=2&b[]=3&c[d]=4` into nested JavaScript variables objects.",
    starter_code: {
      javascript: "function parseQuery(queryString) {\n  return {};\n}\n"
    },
    test_cases: [
      { id: "query-tc-1", name: "parse nested object query strings", stdin: "a=1&b[]=2&b[]=3\n", expected_output: '{"a":"1","b":["2","3"]}\n', hidden: false, weight: 1 }
    ]
  },
  {
    title: "JWT Token Claims Decoder",
    slug: "jwt-token-claims-decoder",
    domain: "APIs",
    difficulty: "Easy",
    minutes: 20,
    xp: 140,
    tags: ["JWT", "Auth", "Security"],
    summary: "Decode base64 encoded JWT header and body payload blocks returning claims validation state.",
    description: "Write a token decoder. Extract JWT body values. Flag tokens if expiry claims (`exp`) timestamp indicates expiration.",
    starter_code: {
      javascript: "function decodeAndValidateJWT(tokenStr) {\n  return { valid: false, payload: {} };\n}\n"
    },
    test_cases: [
      { id: "jwt-tc-1", name: "validate expired token payload claim", stdin: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEwMDAwMDB9.sig\n", expected_output: '{"valid":false}\n', hidden: false, weight: 1 }
    ]
  },
  {
    title: "CORS Header Rule Matcher Engine",
    slug: "cors-header-rule-matcher",
    domain: "APIs",
    difficulty: "Medium",
    minutes: 30,
    xp: 220,
    tags: ["CORS", "API Middleware", "HTTP Headers"],
    summary: "Match client request origin domains against CORS policies returning allow headers.",
    description: "Write a middleware function that matches request headers `Origin` and `Access-Control-Request-Headers` against allowed wildcards list. Output valid `Access-Control-Allow-Origin` values.",
    starter_code: {
      javascript: "function matchCORS(origin, allowedOrigins) {\n  return '';\n}\n"
    },
    test_cases: [
      { id: "cors-tc-1", name: "match domain wildcard pattern allowed", stdin: "https://app.dev.com https://*.dev.com\n", expected_output: "https://app.dev.com\n", hidden: false, weight: 1 }
    ]
  },
  {
    title: "API Link Header Pagination Builder",
    slug: "api-link-header-pagination",
    domain: "APIs",
    difficulty: "Easy",
    minutes: 20,
    xp: 130,
    tags: ["REST APIs", "Pagination", "Link Header"],
    summary: "Format standard REST API RFC-5988 page traversal navigation headers.",
    description: "Write a pagination helper formatting HTTP response header `Link`. Return `next`, `prev`, `first`, and `last` traversal links format from URL base, limits, and total items.",
    starter_code: {
      javascript: "function buildPaginationLinkHeader(baseUrl, page, limit, total) {\n  return '';\n}\n"
    },
    test_cases: [
      { id: "pag-tc-1", name: "first and next header format", stdin: "http://api.com/v1/posts 2 10 100\n", expected_output: '<http://api.com/v1/posts?page=1&limit=10>; rel="prev", <http://api.com/v1/posts?page=3&limit=10>; rel="next"\n', hidden: false, weight: 1 }
    ]
  },

  // ==================== FULLSTACK CHALLENGES ====================
  {
    title: "Build real-time collaborative doc",
    slug: "collaborative-document-sync",
    domain: "Fullstack",
    difficulty: "Expert",
    minutes: 120,
    xp: 750,
    tags: ["WebSockets", "Conflict Resolution", "OT/CRDT"],
    summary: "Design and implement a real-time text document syncing protocol with conflict resolution.",
    description: "Implement a collaborative editing backend and client. Handle concurrent edits from multiple users on a single document string. Ensure changes merge correctly using Operational Transformation (OT) or CRDT models.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "OAuth2 Code Authorization Flow",
    slug: "oauth2-code-auth-flow",
    domain: "Fullstack",
    difficulty: "Hard",
    minutes: 90,
    xp: 500,
    tags: ["OAuth2", "Identity", "Auth Flows"],
    summary: "Implement an OAuth2 authorization code flow with PKCE secure tokens generation.",
    description: "Create an OAuth2 authorization coordinator. Handle authorizing clients, issuing redirection codes, verifying PKCE code verifiers against code challenges, and exchanging codes for JWT access tokens.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Multi-tenant Analytics Aggregator",
    slug: "multi-tenant-analytics-aggregator",
    domain: "Fullstack",
    difficulty: "Medium",
    minutes: 60,
    xp: 380,
    tags: ["Multi-tenancy", "Aggregations", "API Architecture"],
    summary: "Tackle partition isolation of dashboard analytics metrics between distinct company namespaces.",
    description: "Design a fullstack analytics pipeline. Ensure queries are completely sandboxed to the tenant's workspace partition key, handle tenant-specific rate limiting, and structure real-time aggregated metric graphs.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Realtime Bid Auctions Engine",
    slug: "realtime-bid-auctions-engine",
    domain: "Fullstack",
    difficulty: "Hard",
    minutes: 80,
    xp: 480,
    tags: ["WebSockets", "Redis", "Auctions"],
    summary: "Build an live bidding platform server receiving, verifying, and distributing high frequency bids.",
    description: "Design a live bidding system. Handle bid lock contention under Redis transaction scripts, emit high-speed update streams over WebSockets to client grids, and handle auction timeouts gracefully.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  },
  {
    title: "Serverless File Upload Transcoder",
    slug: "serverless-file-upload-transcoder",
    domain: "Fullstack",
    difficulty: "Medium",
    minutes: 50,
    xp: 350,
    tags: ["Object Storage", "Serverless", "Webhooks"],
    summary: "Design direct-to-cloud presigned file upload flows notifying transcoding functions.",
    description: "Create a workflow for secure file uploads. Request presigned upload keys from AWS S3, verify file integrity metadata, execute async lambda transcoding functions via file-upload webhooks.",
    supports_system_design_canvas: true,
    supports_code_execution: false,
    test_cases: []
  }
];

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

let successCount = 0;
let skippedCount = 0;

for (let i = 0; i < challenges.length; i++) {
  const payload = challenges[i];
  const slug = payload.slug || payload.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  
  // Check if already exists in the problems collection
  const existing = targetDb.problems.findOne({ slug: slug });
  if (existing) {
    skippedCount++;
    continue;
  }

  // Map and build valid fields according to ChallengeModel schema
  const doc = {
    challenge_id: generateUUID(),
    title: payload.title,
    slug: slug,
    short_description: payload.summary || "",
    description: payload.description || "",
    domain: payload.domain,
    difficulty: payload.difficulty,
    tags: payload.tags || [],
    technologies: payload.technologies || [],
    hints: payload.hints || [],
    concepts: payload.concepts || [],
    starter_code: payload.starter_code || {
      typescript: "",
      javascript: "",
      python: "",
      go: ""
    },
    test_cases: (payload.test_cases || []).map(tc => ({
      id: tc.id,
      name: tc.name,
      stdin: tc.stdin || "",
      expected_output: tc.expected_output || "",
      hidden: tc.hidden || false,
      weight: tc.weight || 1
    })),
    learning_resources: payload.learning_resources || [],
    xp_reward: payload.xp || 0,
    rating_reward: payload.rating_reward || 0,
    estimated_time_minutes: payload.minutes || 0,
    attempts_count: 0,
    completion_count: 0,
    likes_count: 0,
    bookmarks_count: 0,
    success_rate: 0.0,
    average_score: 0.0,
    average_completion_time: 0.0,
    trending_score: 0.0,
    popularity_score: 0.0,
    recommended_for_beginner: payload.recommended_for_beginner || false,
    supports_ai_review: payload.supports_ai_review !== undefined ? payload.supports_ai_review : true,
    supports_code_execution: payload.supports_code_execution !== undefined ? payload.supports_code_execution : (payload.test_cases && payload.test_cases.length > 0),
    supports_system_design_canvas: payload.supports_system_design_canvas || false,
    is_published: payload.is_published !== undefined ? payload.is_published : true,
    is_featured: payload.is_featured || false,
    is_archived: false,
    created_by: "system_seeder",
    created_at: new Date(),
    updated_at: new Date()
  };

  targetDb.problems.insertOne(doc);
  successCount++;
  print(`  ✓ Created: "${payload.title}" (${slug})`);
}

print("\n========================================");
print("Seeding Completed via mongosh!");
print(`Total Created: ${successCount}`);
print(`Total Skipped (Duplicates): ${skippedCount}`);
print("========================================");
