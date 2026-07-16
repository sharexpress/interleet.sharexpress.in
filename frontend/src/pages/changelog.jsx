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

export default function ChangelogPage() {
  useEffect(() => {
    document.title = "Changelog — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-10 select-text leading-relaxed">
        <div className="space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
            Platform Changelog
          </h1>
          <p className="text-muted-foreground text-base">
            System release logs, new challenges, container updates, and platform optimizations.
          </p>
        </div>

        <section className="space-y-4 border-b border-border/40 pb-8">
          <header className="space-y-1">
            <h2 className="text-2xl font-bold tracking-tight text-foreground/90">v1.2.0 (June 30, 2026)</h2>
            <p className="text-xs font-mono text-muted-foreground">Interactive System Design Canvas & Telemetry Benchmarks</p>
          </header>
          <p>
            This release introduces our new System Design Studio sandbox, moving away from simple static diagrams to fully simulated configurations.
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>Active Canvas Nodes:</strong> Added support for designing component layouts with API Gateways, Load Balancers, Redis cache instances, write-ahead queues, and sharded Postgres schemas.
            </li>
            <li>
              <strong>Packet Flow Simulator:</strong> Integrated visual traffic simulators showcasing network communication paths between component interfaces in real-time.
            </li>
            <li>
              <strong>Operational Latency Telemetry:</strong> Simulated database lookup costs and caching hits, generating estimates for p95 and p99 response limits.
            </li>
          </ul>
        </section>

        <section className="space-y-4 border-b border-border/40 pb-8">
          <header className="space-y-1">
            <h2 className="text-2xl font-bold tracking-tight text-foreground/90">v1.1.5 (May 14, 2026)</h2>
            <p className="text-xs font-mono text-muted-foreground">FastAPI Migration & Autocomplete Packages</p>
          </header>
          <p>
            Re-architected backend handlers, transitioning to a single unified Python FastAPI application to reduce system overhead.
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>FastAPI backend unified:</strong> Replaced fragmented Flask microservices with a single FastAPI server, reducing controller latency by 35%.
            </li>
            <li>
              <strong>Monaco autocomplete indexer:</strong> Configured syntax support and code completion models for Node.js, Go, Python, and Java on the Monaco editor.
            </li>
            <li>
              <strong>Recruiter database sync:</strong> Connected the public recruiter search dashboard directly to candidates' database records for real-time ELO updates.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <header className="space-y-1">
            <h2 className="text-2xl font-bold tracking-tight text-foreground/90">v1.1.0 (March 28, 2026)</h2>
            <p className="text-xs font-mono text-muted-foreground">AI voice-enabled mock interviews</p>
          </header>
          <p>
            Introduced real-time voice sessions using low-latency WebRTC streams.
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>Voice-enabled WebRTC integration:</strong> Integrated voice streams with real-time transcription to power our AI system architect mock interviews.
            </li>
            <li>
              <strong>Structured rubrics:</strong> Configured grading matrices assessing technical depth, systems planning, and communication structuredness.
            </li>
            <li>
              <strong>Candidate transcript logs:</strong> Enabled automated text exports of voice transcriptions and metric scorecards.
            </li>
          </ul>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
