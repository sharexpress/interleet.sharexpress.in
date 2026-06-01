// System Design challenges shown before opening the simulator.
// Each challenge opens with an empty canvas so the user drags & connects
// components manually to solve the prompt.
export const challenges = [
  {
    id: "url-shortener",
    title: "Design a URL Shortener",
    difficulty: "Easy",
    tags: ["Web", "Database", "Cache"],
    brief:
      "Design a service like bit.ly that shortens long URLs and redirects users with low latency. Handle ~10k req/s with high read traffic.",
    requirements: [
      "Generate unique short codes",
      "Sub-100ms redirects globally",
      "Analytics on click counts",
      "Handle read-heavy traffic (100:1 reads/writes)",
    ],
    hints: ["Cache hot keys in Redis", "Use a CDN for global reach", "Separate read replicas"],
  },
  {
    id: "video-streaming",
    title: "Design a Video Streaming Service",
    difficulty: "Hard",
    tags: ["CDN", "Storage", "Encoding"],
    brief:
      "Architect a Netflix-style streaming platform serving millions of concurrent viewers across multiple regions.",
    requirements: ["Adaptive bitrate streaming", "Global CDN distribution", "Recommendations service", "User auth & billing"],
    hints: ["Use CDN edge nodes", "Async transcoding via queue", "Recommendation microservice"],
  },
  {
    id: "ride-sharing",
    title: "Design a Ride-Sharing System",
    difficulty: "Hard",
    tags: ["Realtime", "Geo", "Queue"],
    brief:
      "Build an Uber-like system that matches drivers and riders in real time with live location tracking.",
    requirements: ["Realtime location updates", "Driver matching service", "Trip & payment service", "Surge pricing"],
    hints: ["Use Kafka for event streams", "Geospatial index in Redis", "Microservices per domain"],
  },
  {
    id: "chat-app",
    title: "Design a Chat Application",
    difficulty: "Medium",
    tags: ["Realtime", "Messaging"],
    brief:
      "Design WhatsApp-style messaging with 1:1 chats, group chats, presence and read receipts.",
    requirements: ["WebSocket fanout", "Message persistence", "Push notifications", "Read receipts"],
    hints: ["Message broker like Kafka", "Cache presence in Redis", "Sharded DB by user"],
  },
  {
    id: "ecommerce",
    title: "Design an E-Commerce Platform",
    difficulty: "Medium",
    tags: ["Catalog", "Orders", "Payments"],
    brief:
      "Build an Amazon-like store with catalog, cart, checkout, inventory and order processing.",
    requirements: ["Product catalog search", "Cart & checkout flow", "Inventory consistency", "Order pipeline"],
    hints: ["Elasticsearch for search", "Kafka for order events", "Redis for cart"],
  },
  {
    id: "social-feed",
    title: "Design a Social Media Feed",
    difficulty: "Hard",
    tags: ["Feed", "Cache", "Fanout"],
    brief:
      "Architect a Twitter-style feed handling fanout for users with millions of followers.",
    requirements: ["Timeline generation", "Fanout on write / read", "Media storage", "Notifications"],
    hints: ["Pre-compute feeds in cache", "Hybrid fanout strategy", "Object storage for media"],
  },
];

export const blankChallenge = {
  id: "blank",
  title: "Blank Canvas",
  difficulty: "Free",
  tags: ["Open"],
  brief: "Start from scratch. Drag components from the left panel and connect them to design any system you want.",
  requirements: [],
  hints: [],
};
