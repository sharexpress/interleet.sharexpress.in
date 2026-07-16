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

export default function PrivacyPage() {
  useEffect(() => {
    document.title = "Privacy Policy — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-8 select-text leading-relaxed">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
          Privacy Policy
        </h1>
        <p className="text-muted-foreground font-mono text-[10px] uppercase tracking-wider">
          Last updated: July 2, 2026
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">1. Information We Collect</h2>
          <p>
            At Interleet, we collect information necessary to support secure, sandboxed code execution, leaderboard metrics, and recruitment matches. The information collected falls under two main categories:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>Account Data:</strong> When registering, we store your full name, email, chosen username, password hashes, and user roles (developer, recruiter, or administrator).
            </li>
            <li>
              <strong>Code Runs & Submission History:</strong> We store candidate coding solutions, execution stats (such as cpu runtime milliseconds, memory footprints, and passing assertions), Elo ratings, and AI interviewer audio/text transcript sessions.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">2. How We Use Collected Data</h2>
          <p>
            We process your information to maintain the platform's core matching and evaluation systems:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>To compile, test, execute, and profile candidate coding submissions.</li>
            <li>To compute and update public user rankings on our Elo-based contest leaderboards.</li>
            <li>To display verified technical profiles to registered enterprise recruiters searching our candidates index.</li>
            <li>To analyze voice transcripts in AI system design interviews to generate objective scorecards.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">3. Data Sharing & Third Parties</h2>
          <p>
            We do not sell, rent, or trade your personal information to marketing databases. Your data is shared strictly under the following conditions:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>Recruiter Access:</strong> If your profile is configured as public or verified, registered recruiters can view your usernames, top skills, ratings, and scorecard metrics.
            </li>
            <li>
              <strong>Service Providers:</strong> We route voice transcripts through secure AI models to compute communication clarity. These providers are bound by data-processing agreements.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">4. Your Rights & Choice</h2>
          <p>
            You hold rights over your personal data. You can inspect your profile settings to edit visible profile details, toggle profile visibility to recruiters, request database dumps of your transcripts, or delete your account. Account deletion requests wipe personal identifiers from our databases within 30 days.
          </p>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
