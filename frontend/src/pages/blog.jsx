import { useEffect } from "react";
import { MarketingNav, MarketingFooter } from "@/components/marketing/Marketing";

export default function BlogPage() {
  useEffect(() => {
    document.title = "Engineering Blog — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-12 select-text leading-relaxed">
        <div className="space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
            Engineering Blog
          </h1>
          <p className="text-muted-foreground text-base">
            Technical breakdowns, scaling write-ups, and architectural evaluations prepared by the Interleet engineering team.
          </p>
        </div>

        <article className="space-y-4 border-b border-border/40 pb-10">
          <header className="space-y-1">
            <span className="text-xs uppercase font-mono text-primary font-semibold">Infrastructure Deep Dive</span>
            <h2 className="text-2xl font-bold tracking-tight text-foreground/90">
              How We Scaled Our Code Sandboxes to 10k Concurrent Executions
            </h2>
            <p className="text-[11px] text-muted-foreground font-mono">June 24, 2026 · 8 min read</p>
          </header>
          <p>
            Executing arbitrary user code safely in real-time is a complex infrastructure challenge. When a candidate submits code on Interleet, we run it within isolated containerized runtimes to profile execution metrics. At high concurrency (e.g. during weekly leaderboards), managing container initialization overhead becomes the primary bottleneck.
          </p>
          <p>
            Initially, we utilized standard Docker daemon container spawns. However, cold start latency averaged 800ms—far too slow for real-time compilation and evaluation feedback loops. 
          </p>
          <p>
            To address this, we transitioned to a pre-warmed pool architecture managed by a custom resource daemon in Go. We maintain pools of running, isolated micro-containers. When an execution request arrives, the daemon routes the payload to an available pre-warmed sandbox, running code in under 45ms.
          </p>
          <h3 className="text-lg font-semibold text-foreground/80 mt-4">Isolation & Telemetry Collection</h3>
          <p>
            To prevent system escalation, our sandboxes execute code within gVisor virtualization runtimes. This intercepts kernel syscalls, ensuring malicious code cannot affect host processes. Telemetry agents bind to host-side namespace APIs, measuring CPU runtime milliseconds and memory allocations directly without introducing container runtime overhead.
          </p>
        </article>

        <article className="space-y-4 border-b border-border/40 pb-10">
          <header className="space-y-1">
            <span className="text-xs uppercase font-mono text-primary font-semibold">System Architecture</span>
            <h2 className="text-2xl font-bold tracking-tight text-foreground/90">
              Designing a Distributed Rate Limiter: Algorithms & Tradeoffs
            </h2>
            <p className="text-[11px] text-muted-foreground font-mono">May 18, 2026 · 6 min read</p>
          </header>
          <p>
            Rate limiting is a fundamental component of system design. Under massive write volumes (e.g., 50k requests/sec), single-node rate limiters fail to scale, requiring distributed structures.
          </p>
          <p>
            In this case study, we evaluate the implementation of two primary algorithms: Token Bucket and Sliding Window Log.
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
            <li>
              <strong>Sliding Window Logs:</strong> Offer high precision, but require storing memory timestamps for every request. Under surge loads, memory consumption increases exponentially, making the approach cost-prohibitive.
            </li>
            <li>
              <strong>Token Buckets:</strong> Store simple count and timestamp variables per client, utilizing O(1) memory complexity. By using Redis script transactions (Lua scripts), we evaluate and decrement client budgets in a single round-trip.
            </li>
          </ul>
          <p>
            For distributed systems, Token Bucket algorithms configured with Redis clusters provide the optimal balance between performance overhead and memory efficiency.
          </p>
        </article>

        <article className="space-y-4">
          <header className="space-y-1">
            <span className="text-xs uppercase font-mono text-primary font-semibold">Databases</span>
            <h2 className="text-2xl font-bold tracking-tight text-foreground/90">
              Postgres Indexing Strategies Under Concurrency
            </h2>
            <p className="text-[11px] text-muted-foreground font-mono">April 09, 2026 · 10 min read</p>
          </header>
          <p>
            As a database grows, query speeds can degrade. Adding basic B-tree indexes is the standard approach to optimization, but it can introduce trade-offs in write-heavy tables.
          </p>
          <p>
            On our leaderboard engine, candidates commit code submissions continuously, resulting in write-heavy tables. Adding multiple indexes slows down inserts because index nodes must update synchronously.
          </p>
          <p>
            To optimize query latency without degrading write performance, we utilize partial indexes:
          </p>
          <pre className="p-4 bg-muted/40 rounded-lg text-xs font-mono text-foreground/80 overflow-x-auto">
            {"CREATE INDEX idx_user_submissions_verified \nON user_submissions (rating) \nWHERE verified = true;"}
          </pre>
          <p>
            This index stores only verified candidate records, reducing overall index size by 78%, speeding up leaderboards queries, and minimizing insert amplification.
          </p>
        </article>
      </main>
      <MarketingFooter />
    </div>
  );
}
