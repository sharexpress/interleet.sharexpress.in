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

export default function TermsPage() {
  useEffect(() => {
    document.title = "Terms of Service — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-8 select-text leading-relaxed">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
          Terms of Service
        </h1>
        <p className="text-muted-foreground font-mono text-[10px] uppercase tracking-wider">
          Last updated: July 2, 2026
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">1. Acceptance of Terms</h2>
          <p>
            By creating an account, compiling code, interacting with our design canvas tools, or searching profiles on Interleet, you agree to comply with and be bound by these Terms of Service. If you do not agree to these terms, do not access or use our services.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">2. Rules of Engagement & Code Compilation</h2>
          <p>
            Interleet provides isolated environment execution runtimes for practicing software engineering. To maintain system stability and platform integrity, you agree not to:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              Submit malicious code intended to exploit compiler VMs, breach namespace isolations, bypass networking controls, or access host metadata.
            </li>
            <li>
              Automate code evaluations or scraping using bots, unless accessing endpoints via approved recruiter API keys.
            </li>
            <li>
              Falsify scorecard statistics, cheat in weekly contests using external code generators, or attempt to compromise leaderboard Elo ratings.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">3. Intellectual Property Rights</h2>
          <p>
            The Interleet platform layout, code compilation engines, design canvas interface, mock evaluation rubrics, and overall content are owned by Interleet, Inc. and protected by copyright and intellectual property laws. You retain ownership of the specific solutions you write, but grant Interleet a license to compile, analyze, profile, and share those solutions for scoring.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">4. Service Limitations & Disclaimers</h2>
          <p>
            The platform is provided on an "as is" basis. While we strive to maintain high system uptime, we do not guarantee uninterrupted services, data retention for draft code submissions, or accuracy of AI grading reports. Interleet is not liable for system outages, data loss, or hiring decisions made by recruiters utilizing our candidate directory indices.
          </p>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
