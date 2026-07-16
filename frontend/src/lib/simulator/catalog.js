/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Curated component catalog shown in the draggable sidebar library to keep the UI clean and simple.
export const catalog = [
  { category: "Client / Users", items: [
    { kind: "client", label: "Web / Desktop Client", desc: "Generic web browser or desktop client" },
    { kind: "mobile", label: "Mobile Client", desc: "Native iOS / Android mobile application" },
  ]},
  { category: "Network", items: [
    { kind: "dns", label: "DNS", desc: "Domain Name System resolution" },
    { kind: "cdn", label: "CDN Edge", desc: "Global Content Delivery Network cache" },
    { kind: "load-balancer", label: "Load Balancer", desc: "Traffic distribution (Nginx / HAProxy)" },
    { kind: "api-gateway", label: "API Gateway", desc: "API entrypoint routing, auth, and rate-limiting" },
  ]},
  { category: "Compute / Runtimes", items: [
    { kind: "web-server", label: "Web Server", desc: "HTTP application hosting layer" },
    { kind: "microservice", label: "Microservice", desc: "Independent domain microservice runtime" },
  ]},
  { category: "Databases & Caches", items: [
    { kind: "postgresql", label: "SQL Database", desc: "Relational transactional database (Postgres/MySQL)" },
    { kind: "mongodb", label: "NoSQL Database", desc: "Document / Key-Value NoSQL database (MongoDB)" },
    { kind: "redis", label: "Memory Cache", desc: "High-speed in-memory database & cache (Redis)" },
    { kind: "elasticsearch", label: "Search Index", desc: "Distributed search & analytics index" },
  ]},
  { category: "Messaging & Streams", items: [
    { kind: "kafka", label: "Event Stream", desc: "High-throughput append-only log (Kafka)" },
    { kind: "queue", label: "Job Queue", desc: "Asynchronous worker task queue (RabbitMQ/SQS)" },
  ]},
  { category: "Artificial Intelligence", items: [
    { kind: "llm", label: "AI LLM Service", desc: "LLM server endpoint (Gemini/OpenAI)" },
    { kind: "vector-db", label: "Vector Database", desc: "Similarity search vector storage" },
  ]},
  { category: "Observability", items: [
    { kind: "metrics", label: "Monitoring Console", desc: "Metrics, logging, and alert dashboard" },
  ]},
];

// Full kind lookup (retains deprecated kinds for loading older templates without crashes)
export const kindMap = {
  client: { kind: "client", label: "Web Client", category: "Client / Users" },
  mobile: { kind: "mobile", label: "Mobile Client", category: "Client / Users" },
  web: { kind: "web", label: "Web App", category: "Client / Users" },
  "client-cluster": { kind: "client-cluster", label: "Client Cluster", category: "Client / Users" },
  
  dns: { kind: "dns", label: "DNS", category: "Network" },
  cdn: { kind: "cdn", label: "CDN Edge", category: "Network" },
  "reverse-proxy": { kind: "reverse-proxy", label: "Reverse Proxy", category: "Network" },
  "load-balancer": { kind: "load-balancer", label: "Load Balancer", category: "Network" },
  "api-gateway": { kind: "api-gateway", label: "API Gateway", category: "Network" },
  
  "web-server": { kind: "web-server", label: "Web Server", category: "Compute / Runtimes" },
  "app-server": { kind: "app-server", label: "Application Server", category: "Compute / Runtimes" },
  "rest-api": { kind: "rest-api", label: "REST API", category: "Compute / Runtimes" },
  graphql: { kind: "graphql", label: "GraphQL API", category: "Compute / Runtimes" },
  auth: { kind: "auth", label: "Authentication Service", category: "Compute / Runtimes" },
  microservice: { kind: "microservice", label: "Microservice", category: "Compute / Runtimes" },
  
  postgresql: { kind: "postgresql", label: "SQL Database", category: "Databases & Caches" },
  mysql: { kind: "mysql", label: "SQL Database (MySQL)", category: "Databases & Caches" },
  mongodb: { kind: "mongodb", label: "NoSQL Database", category: "Databases & Caches" },
  redis: { kind: "redis", label: "Memory Cache", category: "Databases & Caches" },
  elasticsearch: { kind: "elasticsearch", label: "Search Index", category: "Databases & Caches" },
  
  kafka: { kind: "kafka", label: "Event Stream", category: "Messaging & Streams" },
  rabbitmq: { kind: "rabbitmq", label: "Job Queue (RabbitMQ)", category: "Messaging & Streams" },
  "event-bus": { kind: "event-bus", label: "Event Bus", category: "Messaging & Streams" },
  queue: { kind: "queue", label: "Job Queue", category: "Messaging & Streams" },
  
  logging: { kind: "logging", label: "Logging", category: "Observability" },
  metrics: { kind: "metrics", label: "Monitoring Console", category: "Observability" },
  alert: { kind: "alert", label: "Alert Manager", category: "Observability" },
  
  llm: { kind: "llm", label: "AI LLM Service", category: "Artificial Intelligence" },
  embedding: { kind: "embedding", label: "Embeddings Service", category: "Artificial Intelligence" },
  "vector-db": { kind: "vector-db", label: "Vector Database", category: "Artificial Intelligence" },
};

// Default props per kind used by the simulator
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
    client: { replicas: 1, throughput: 1000, latency: 0, hourlyCost: 0 },
    mobile: { replicas: 1, throughput: 1000, latency: 0, hourlyCost: 0 },
    web: { replicas: 1, throughput: 1000, latency: 0, hourlyCost: 0 },
    "client-cluster": { replicas: 1, throughput: 2500, latency: 0, hourlyCost: 0 },
    
    dns: { throughput: 20000, latency: 2, hourlyCost: 2 },
    cdn: { throughput: 50000, latency: 6, hourlyCost: 4 },
    "reverse-proxy": { throughput: 12000, latency: 2, hourlyCost: 3 },
    "load-balancer": { algorithm: "round-robin", ssl: true, sticky: false, maxConnections: 20000, throughput: 20000, latency: 2, hourlyCost: 8 },
    "api-gateway": { auth: true, rateLimit: 3000, validation: true, versioning: "v1", caching: false, throughput: 8000, latency: 5, hourlyCost: 12 },
    
    "web-server": { replicas: 2, throughput: 1500, latency: 12, hourlyCost: 6 },
    "app-server": { replicas: 2, throughput: 1500, latency: 18, hourlyCost: 8 },
    "rest-api": { replicas: 2, throughput: 1500, latency: 12, hourlyCost: 6 },
    graphql: { replicas: 2, throughput: 1500, latency: 18, hourlyCost: 8 },
    auth: { replicas: 2, throughput: 4000, latency: 8, hourlyCost: 10 },
    microservice: { serviceName: "service", language: "Node.js", version: "1.0.0", replicas: 2, autoscaling: true, throughput: 1500, latency: 18, hourlyCost: 15 },
    
    postgresql: { storage: 100, replication: "primary-replica", backupStrategy: "daily", readCapacity: 2000, writeCapacity: 500, latency: 15, hourlyCost: 20 },
    mysql: { storage: 100, replication: "primary-replica", readCapacity: 1800, writeCapacity: 400, latency: 18, hourlyCost: 18 },
    mongodb: { storage: 150, replication: "replica-set", readCapacity: 2500, writeCapacity: 800, latency: 12, hourlyCost: 22 },
    redis: { memorySize: 4, ttl: 3600, replication: "primary-replica", evictionPolicy: "allkeys-lru", throughput: 85000, latency: 1, hourlyCost: 10 },
    elasticsearch: { throughput: 5000, latency: 8, hourlyCost: 24 },
    
    kafka: { partitions: 12, replicationFactor: 3, retentionPeriod: 168, throughput: 40000, latency: 4, hourlyCost: 25 },
    rabbitmq: { throughput: 15000, latency: 3, hourlyCost: 15 },
    "event-bus": { throughput: 15000, latency: 2, hourlyCost: 12 },
    queue: { throughput: 15000, latency: 3, hourlyCost: 10 },
    
    logging: { throughput: 25000, latency: 5, hourlyCost: 5 },
    metrics: { throughput: 25000, latency: 3, hourlyCost: 5 },
    alert: { throughput: 20000, latency: 2, hourlyCost: 3 },
    
    llm: { throughput: 200, latency: 150, hourlyCost: 50 },
    embedding: { throughput: 800, latency: 35, hourlyCost: 20 },
    "vector-db": { throughput: 3000, latency: 8, hourlyCost: 30 },
  };
  
  return { ...base, ...(overrides[kind] || {}) };
};
