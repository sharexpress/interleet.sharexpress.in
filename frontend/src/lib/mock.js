






















export const DOMAINS = [
"Frontend",
"Backend",
"DevOps",
"APIs",
"Databases",
"System Design"];


export const challenges = [
{
  id: "1",
  slug: "build-a-rate-limiter",
  title: "Build a Token Bucket Rate Limiter",
  domain: "Backend",
  difficulty: "Medium",
  minutes: 45,
  xp: 320,
  completion: 64,
  tags: ["Node.js", "Concurrency", "Redis"],
  summary: "Implement a thread-safe rate limiter with burst handling and refill logic."
},
{
  id: "2",
  slug: "responsive-data-table",
  title: "Responsive Virtualized Data Table",
  domain: "Frontend",
  difficulty: "Hard",
  minutes: 90,
  xp: 540,
  completion: 38,
  tags: ["React", "Performance", "Accessibility"],
  summary: "Render 100k rows with sticky headers, sorting, and keyboard navigation."
},
{
  id: "3",
  slug: "ci-pipeline-from-scratch",
  title: "Design a CI Pipeline From Scratch",
  domain: "DevOps",
  difficulty: "Medium",
  minutes: 60,
  xp: 380,
  completion: 52,
  tags: ["GitHub Actions", "Docker", "Caching"],
  summary: "Build a multi-stage pipeline with caching, parallel jobs, and artifact promotion."
},
{
  id: "4",
  slug: "design-twitter-feed",
  title: "Design Twitter's Home Feed",
  domain: "System Design",
  difficulty: "Hard",
  minutes: 120,
  xp: 720,
  completion: 28,
  tags: ["Fan-out", "Cache", "Sharding"],
  summary: "Architect a low-latency timeline service for 500M daily users."
},
{
  id: "5",
  slug: "rest-versioning",
  title: "Versioning a Public REST API",
  domain: "APIs",
  difficulty: "Easy",
  minutes: 30,
  xp: 180,
  completion: 78,
  tags: ["REST", "Backward-compat"],
  summary: "Choose a versioning strategy and migrate a v1 client smoothly to v2."
},
{
  id: "6",
  slug: "indexing-strategy",
  title: "Postgres Indexing Strategy",
  domain: "Databases",
  difficulty: "Medium",
  minutes: 40,
  xp: 280,
  completion: 56,
  tags: ["Postgres", "EXPLAIN", "B-tree"],
  summary: "Reduce a 12s analytics query to under 200ms using the right indexes."
},
{
  id: "7",
  slug: "feature-flag-service",
  title: "Build a Feature Flag Service",
  domain: "Backend",
  difficulty: "Hard",
  minutes: 90,
  xp: 560,
  completion: 34,
  tags: ["Streaming", "SDKs", "Targeting"],
  summary: "Realtime flag evaluation with audience targeting and rollouts."
},
{
  id: "8",
  slug: "k8s-blue-green",
  title: "Blue/Green Deploy on Kubernetes",
  domain: "DevOps",
  difficulty: "Expert",
  minutes: 120,
  xp: 820,
  completion: 18,
  tags: ["Kubernetes", "Helm", "Rollouts"],
  summary: "Zero-downtime release with automated rollback on SLO breach."
},
{
  id: "9",
  slug: "ssr-cache-strategy",
  title: "SSR Cache Strategy for an E-commerce App",
  domain: "Frontend",
  difficulty: "Medium",
  minutes: 60,
  xp: 360,
  completion: 47,
  tags: ["Next.js", "ISR", "Edge"],
  summary: "Cache product pages with personalization and inventory accuracy."
}];













export const leaderboard = [
{ rank: 1, username: "amelia.dev", rating: 2843, xp: 184200, country: "🇺🇸", delta: 24, badges: ["Top 1%", "DevOps"] },
{ rank: 2, username: "kenji_w", rating: 2790, xp: 172480, country: "🇯🇵", delta: 12, badges: ["Top 1%"] },
{ rank: 3, username: "priya.s", rating: 2755, xp: 168120, country: "🇮🇳", delta: -3, badges: ["Backend"] },
{ rank: 4, username: "lucasf", rating: 2710, xp: 161300, country: "🇧🇷", delta: 8, badges: ["System Design"] },
{ rank: 5, username: "noor.k", rating: 2682, xp: 158020, country: "🇦🇪", delta: 5, badges: ["APIs"] },
{ rank: 6, username: "aria.j", rating: 2654, xp: 152410, country: "🇰🇷", delta: 0, badges: ["Frontend"] },
{ rank: 7, username: "mateo.r", rating: 2611, xp: 148720, country: "🇪🇸", delta: -2, badges: ["Databases"] },
{ rank: 8, username: "fatima.b", rating: 2589, xp: 144000, country: "🇲🇦", delta: 11, badges: ["DevOps"] },
{ rank: 9, username: "yuki.t", rating: 2554, xp: 139220, country: "🇯🇵", delta: 4, badges: ["Backend"] },
{ rank: 10, username: "diego.v", rating: 2521, xp: 134110, country: "🇲🇽", delta: -1, badges: ["Frontend"] },
{ rank: 11, username: "hana.l", rating: 2498, xp: 130880, country: "🇩🇪", delta: 6, badges: ["System Design"] },
{ rank: 12, username: "samir.k", rating: 2470, xp: 127340, country: "🇮🇳", delta: 3, badges: ["APIs"] }];


export const user = {
  name: "Alex Morgan",
  username: "alex.morgan",
  title: "Senior Software Engineer",
  location: "Berlin, DE",
  rating: 2184,
  rank: 327,
  xp: 48210,
  streak: 28,
  accuracy: 86,
  solved: 184,
  interviews: 14,
  badges: ["Top 5% Backend", "100-Day Streak", "System Design I", "API Architect"],
  domains: [
  { domain: "Frontend", score: 72 },
  { domain: "Backend", score: 91 },
  { domain: "DevOps", score: 68 },
  { domain: "APIs", score: 84 },
  { domain: "Databases", score: 76 },
  { domain: "System Design", score: 80 }]

};

export const activityWeekly = [
{ day: "Mon", solved: 3, minutes: 75 },
{ day: "Tue", solved: 5, minutes: 110 },
{ day: "Wed", solved: 2, minutes: 50 },
{ day: "Thu", solved: 6, minutes: 140 },
{ day: "Fri", solved: 4, minutes: 95 },
{ day: "Sat", solved: 7, minutes: 180 },
{ day: "Sun", solved: 5, minutes: 130 }];


export const recentActivity = [
{ type: "solved", text: "Solved Postgres Indexing Strategy", when: "2h ago", domain: "Databases" },
{ type: "interview", text: "Completed AI Interview — Senior Backend", when: "1d ago", domain: "Backend" },
{ type: "badge", text: "Earned 100-Day Streak badge", when: "2d ago", domain: "—" },
{ type: "contest", text: "Placed #18 in Weekly Engineering Cup", when: "4d ago", domain: "System Design" },
{ type: "solved", text: "Solved Responsive Data Table", when: "5d ago", domain: "Frontend" }];


export const interviewHistory = [
{ id: "iv-21", role: "Senior Backend", score: 84, when: "1d ago", duration: 42 },
{ id: "iv-20", role: "System Design (L5)", score: 78, when: "5d ago", duration: 55 },
{ id: "iv-19", role: "Frontend Architect", score: 71, when: "12d ago", duration: 48 },
{ id: "iv-18", role: "DevOps Lead", score: 82, when: "21d ago", duration: 39 }];


export const systemDesignTopics = [
{
  title: "Scalability",
  items: ["Vertical vs horizontal", "Load balancers", "Stateless services", "Backpressure"]
},
{
  title: "Caching",
  items: ["CDN strategy", "Read-through / write-back", "Cache invalidation", "Hot keys"]
},
{
  title: "Databases",
  items: ["Sharding", "Replication", "CAP & consistency", "Indexing for scale"]
},
{
  title: "Distributed Systems",
  items: ["Consensus (Raft/Paxos)", "Idempotency", "Event sourcing", "Sagas"]
},
{
  title: "Infrastructure",
  items: ["Service mesh", "Observability", "Edge compute", "Blue/Green & canary"]
},
{
  title: "Load Balancing",
  items: ["L4 vs L7", "Consistent hashing", "Health checks", "Geo routing"]
}];


export const candidates = [
{ name: "Jordan Lee", username: "jlee", rating: 2410, top: "Backend", verified: true, location: "NYC" },
{ name: "Maya Chen", username: "mchen", rating: 2356, top: "System Design", verified: true, location: "SF" },
{ name: "Ravi Shankar", username: "rshankar", rating: 2298, top: "DevOps", verified: true, location: "Bengaluru" },
{ name: "Sofia Romero", username: "sromero", rating: 2244, top: "Frontend", verified: false, location: "Madrid" },
{ name: "Tomás Alves", username: "talves", rating: 2189, top: "APIs", verified: true, location: "Lisbon" }];