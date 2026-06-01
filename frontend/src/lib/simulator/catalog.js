// Component catalog grouped by category. Each entry: { kind, label, desc, category }
export const catalog = [
  { category: "Client", items: [
    { kind: "client", label: "Client", desc: "End-user device" },
    { kind: "mobile", label: "Mobile App", desc: "iOS / Android client" },
    { kind: "web", label: "Web App", desc: "Browser SPA" },
    { kind: "client-cluster", label: "Client Cluster", desc: "Many concurrent clients" },
  ]},
  { category: "Network", items: [
    { kind: "dns", label: "DNS", desc: "Domain resolution" },
    { kind: "cdn", label: "CDN", desc: "Edge cache" },
    { kind: "reverse-proxy", label: "Reverse Proxy", desc: "Nginx / Envoy" },
    { kind: "load-balancer", label: "Load Balancer", desc: "Traffic distribution" },
    { kind: "api-gateway", label: "API Gateway", desc: "Routing & auth" },
  ]},
  { category: "Application", items: [
    { kind: "web-server", label: "Web Server", desc: "HTTP server" },
    { kind: "app-server", label: "Application Server", desc: "Stateful runtime" },
    { kind: "rest-api", label: "REST API", desc: "JSON service" },
    { kind: "graphql", label: "GraphQL API", desc: "Schema service" },
    { kind: "auth", label: "Authentication Service", desc: "OAuth / JWT" },
    { kind: "microservice", label: "Microservice", desc: "Bounded service" },
  ]},
  { category: "Data", items: [
    { kind: "postgresql", label: "PostgreSQL", desc: "Relational DB" },
    { kind: "mysql", label: "MySQL", desc: "Relational DB" },
    { kind: "mongodb", label: "MongoDB", desc: "Document DB" },
    { kind: "redis", label: "Redis", desc: "In-memory cache" },
    { kind: "elasticsearch", label: "Elasticsearch", desc: "Search index" },
  ]},
  { category: "Messaging", items: [
    { kind: "kafka", label: "Kafka", desc: "Event streaming" },
    { kind: "rabbitmq", label: "RabbitMQ", desc: "Message broker" },
    { kind: "event-bus", label: "Event Bus", desc: "Pub/Sub" },
    { kind: "queue", label: "Queue", desc: "FIFO job queue" },
  ]},
  { category: "Monitoring", items: [
    { kind: "logging", label: "Logging Service", desc: "Log aggregation" },
    { kind: "metrics", label: "Metrics Service", desc: "TSDB" },
    { kind: "alert", label: "Alert Manager", desc: "Notifications" },
  ]},
  { category: "AI", items: [
    { kind: "llm", label: "LLM Service", desc: "Generation API" },
    { kind: "embedding", label: "Embedding Service", desc: "Vector encoder" },
    { kind: "vector-db", label: "Vector Database", desc: "Similarity search" },
  ]},
];

// Lookup by kind
export const kindMap = Object.fromEntries(
  catalog.flatMap(c => c.items.map(i => [i.kind, { ...i, category: c.category }]))
);

// Default per-kind properties used by the simulator
export const defaultPropsFor = (kind) => {
  const base = {
    enabled: true,
    health: "healthy",
    replicas: 1,
    throughput: 100,
    latency: 20,
    errorRate: 0,
    hourlyCost: 5,
    cpu: 12,
    memory: 24,
    tags: [],
    environment: "production",
    description: "",
  };
  const overrides = {
    client: { replicas: 1, throughput: 1000, latency: 5, hourlyCost: 0 },
    "load-balancer": { algorithm: "round-robin", ssl: true, sticky: false, maxConnections: 10000, throughput: 5000, latency: 2, hourlyCost: 8 },
    "api-gateway": { auth: true, rateLimit: 1000, validation: true, versioning: "v1", caching: false, throughput: 3000, latency: 5, hourlyCost: 12 },
    microservice: { serviceName: "service", language: "Node.js", version: "1.0.0", replicas: 3, autoscaling: true, throughput: 800, latency: 25, hourlyCost: 15 },
    postgresql: { storage: 100, replication: "primary-replica", backupStrategy: "daily", readCapacity: 2000, writeCapacity: 500, latency: 15, hourlyCost: 20 },
    mysql: { storage: 100, replication: "primary-replica", readCapacity: 1800, writeCapacity: 400, latency: 18, hourlyCost: 18 },
    mongodb: { storage: 150, replication: "replica-set", readCapacity: 2500, writeCapacity: 800, latency: 12, hourlyCost: 22 },
    redis: { memorySize: 4, ttl: 3600, replication: "primary-replica", evictionPolicy: "allkeys-lru", throughput: 50000, latency: 1, hourlyCost: 10 },
    kafka: { partitions: 12, replicationFactor: 3, retentionPeriod: 168, throughput: 20000, latency: 8, hourlyCost: 25 },
  };
  return { ...base, ...(overrides[kind] || {}) };
};
