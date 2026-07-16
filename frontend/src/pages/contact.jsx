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

export default function ContactPage() {
  useEffect(() => {
    document.title = "Contact Us — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-8 select-text leading-relaxed">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
          Contact Details & Support Channels
        </h1>
        <p className="text-muted-foreground font-mono text-[10px] uppercase tracking-wider">
          Last updated: July 2, 2026
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">1. Developer Relations & Platform Support</h2>
          <p>
            For inquiries regarding user account issues, password resets, Monaco editor configuration errors, leaderboard ranking disputes, or code runner execution failures:
          </p>
          <p className="font-mono text-sm font-semibold text-primary">
            Email: developer-support@interleet.com
          </p>
          <p className="text-xs text-muted-foreground">
            Our standard developer support queue is monitored Monday through Friday, 9:00 AM to 6:00 PM PST. Standard response turnaround times average 12 to 24 hours.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">2. Corporate Licensing & Enterprise Sales</h2>
          <p>
            If you are a recruiting agency, enterprise organization, or hiring team interested in custom sandbox instances, private team leaderboards, custom grading rubrics, candidate CRM integrations, or dedicated support agreements:
          </p>
          <p className="font-mono text-sm font-semibold text-primary">
            Email: sales-licensing@interleet.com
          </p>
          <p className="text-xs text-muted-foreground">
            Enterprise sales queries are routed to our regional account managers. Please include your company name, location, estimated candidate volume, and key assessment requirements.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">3. Security Vulnerability Reports</h2>
          <p>
            We run a private bug bounty program for responsible disclosure of security issues. If you have identified vulnerability details related to code execution breakouts, database security limits, or user credential leaks:
          </p>
          <p className="font-mono text-sm font-semibold text-primary">
            Email: security-disclosure@interleet.com
          </p>
          <p className="text-xs text-muted-foreground">
            Please encrypt report data using our PGP public keys (available on request). Do not share report details publicly until we have resolved the issue.
          </p>
        </section>

        <section className="space-y-4 border-t border-border/60 pt-8">
          <h2 className="text-xl font-bold tracking-tight text-foreground/90">4. Corporate Office Locations</h2>
          <p className="text-xs md:text-sm text-muted-foreground">
            Interleet Technologies, Inc. <br />
            548 Market Street, Suite 92431 <br />
            San Francisco, CA 94104 <br />
            United States
          </p>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
