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

export default function CookiesPage() {
  useEffect(() => {
    document.title = "Cookie Policy — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-8 select-text leading-relaxed">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
          Cookie Policy
        </h1>
        <p className="text-muted-foreground font-mono text-[10px] uppercase tracking-wider">
          Last updated: July 2, 2026
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">1. What Are Cookies?</h2>
          <p>
            Cookies are small text files stored by your browser onto your computer or mobile device when you visit websites. They are widely used to make web applications run efficiently, store settings, and transmit telemetry to servers.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">2. How We Use Cookies</h2>
          <p>
            We use cookies and equivalent browser storage technologies (such as LocalStorage and SessionStorage) to support the following platform features:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>Authentication & Sessions:</strong> To verify your logged-in credentials as you navigate through dashboard challenges, compiler editors, and profile settings without requiring repeated logins.
            </li>
            <li>
              <strong>User Preferences:</strong> To persist editor preferences, dark/light theme choices, and code workspace configurations.
            </li>
            <li>
              <strong>Telemetry & Analytics:</strong> To count page views, track compile failure spikes, and measure layout loading durations to resolve issues and improve performance.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">3. Types of Cookies We Set</h2>
          <div className="space-y-3 text-xs md:text-sm text-muted-foreground">
            <div>
              <p className="font-semibold text-foreground">Strictly Necessary Cookies</p>
              <p>Essential for basic operations, including session authentication checks and cookie preference consent logs. These cannot be disabled.</p>
            </div>
            <div>
              <p className="font-semibold text-foreground">Functional & Settings Cookies</p>
              <p>Used to store preferences, such as Monaco tab spacing sizes, autocomplete configurations, and visual panel layout states.</p>
            </div>
            <div>
              <p className="font-semibold text-foreground">Performance & Monitoring Cookies</p>
              <p>Track request latencies, network load distribution, and interface load times to help debug service issues.</p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">4. Controlling Cookie Settings</h2>
          <p>
            You can configure your browser to block, delete, or alert you about cookies by adjusting your browser preferences. Note that blocking essential cookies will break session verification, preventing you from logging in, writing code, or saving system designs.
          </p>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
