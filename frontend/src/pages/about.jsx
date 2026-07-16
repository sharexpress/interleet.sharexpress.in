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

import { useEffect } from "react";
import { MarketingNav, MarketingFooter } from "@/components/marketing/Marketing";

export default function AboutPage() {
  useEffect(() => {
    document.title = "About Us — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-8 select-text leading-relaxed">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
          About Interleet
        </h1>
        <p className="text-muted-foreground font-mono text-[10px] uppercase tracking-wider">
          Published: July 2, 2026
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">1. Our Core Mission</h2>
          <p>
            Interleet was established in response to a widespread issue in software engineering recruitment: the over-reliance on abstract algorithmic puzzles (commonly referred to as LeetCode-style data structures and algorithms) to assess senior engineering capabilities.
          </p>
          <p>
            While algorithmic efficiency is a critical aspect of computer science, it does not represent the entirety of professional software engineering. In production, engineers spend less time balancing binary search trees and more time resolving concurrency bottlenecks, debugging distributed race conditions, analyzing container telemetry, optimizing database queries, and aligning APIs.
          </p>
          <p>
            Our mission is simple: to create a metrics-driven, production-grade practice arena where software engineers can sharpen their skills on the exact scenarios they encounter in real-world environments, and where hiring teams can evaluate verified technical competencies.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">2. Real-World Engineering Constraints</h2>
          <p>
            Every coding exercise on Interleet is modeled after actual operational issues, production tickets, incident write-ups, or architectural design specs. When you start a challenge, you are not just writing code to pass a unit test; you are building software within a set of realistic system constraints:
          </p>
          <ul className="list-disc pl-6 space-y-3 text-muted-foreground">
            <li>
              <strong>Latency Budgets:</strong> Submissions are profiled for execution performance. An optimal solution must return responses within target p95 or p99 limits under simulated concurrency loads.
            </li>
            <li>
              <strong>Memory Footprints:</strong> Code runs within container allocations. Solutions that leak memory, exceed garbage collection intervals, or fail under spike conditions are rejected.
            </li>
            <li>
              <strong>Consistency and Scalability Trade-offs:</strong> When designing systems in our System Design Studio, engineers must defend their choices regarding read-through caching, database replication, write-ahead queues, and consistent hashing.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">3. Rubric-Backed Assessments</h2>
          <p>
            To complement code execution, Interleet features an AI Mock Interview module. Rather than checking simple keyword inputs, our AI interviewers engage candidates in structured design conversations. Every session is graded against rigorous rubrics mapping to:
          </p>
          <ul className="list-decimal pl-6 space-y-2 text-muted-foreground">
            <li><strong>Technical Breadth:</strong> Deep understanding of concurrency, lock contention, protocols, and database isolation levels.</li>
            <li><strong>Communication Quality:</strong> Structural layout of proposals, clear articulation of trade-offs, and responsiveness to interviewer feedback.</li>
            <li><strong>Operational Competency:</strong> Awareness of failure states, recovery procedures, and edge-case handling.</li>
          </ul>
        </section>

        <section className="space-y-4 border-t border-border/60 pt-8">
          <h2 className="text-xl font-bold tracking-tight text-foreground/90">4. Our Commitment to Developers</h2>
          <p>
            We are dedicated to building a platform that developers trust. This means ensuring complete data security, isolated code runtimes, transparent ELO-based ranking leaderboards, and recruiter badges backed by actual measured execution data. We do not evaluate based on resume keywords; we evaluate based on clean code, performance profiling, and systems specialization.
          </p>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
