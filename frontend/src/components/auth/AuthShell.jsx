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


import { Logo } from "@/components/brand/Logo";
import { useState, useEffect } from "react";
import { API } from "@/api/api";
import { Link } from "react-router-dom";

export function AuthShell({
  title,
  subtitle,
  children,
  footer
}) {
  const [challengeCount, setChallengeCount] = useState(null);

  useEffect(() => {
    API.get("/api/public/stats")
      .then((res) => {
        if (res.data && typeof res.data.total_challenges === "number") {
          setChallengeCount(res.data.total_challenges);
        }
      })
      .catch((err) => {
        console.error("Error fetching public stats:", err);
      });
  }, []);

  return (
    <div className="grid min-h-screen bg-background md:grid-cols-2">
      <div className="flex flex-col px-6 py-8 md:px-12">
        <Logo />

        <div className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center">
          <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
          {subtitle && <p className="mt-2 text-sm text-muted-foreground">{subtitle}</p>}
          <div className="mt-6">{children}</div>
          {footer && <div className="mt-6 text-sm text-muted-foreground">{footer}</div>}
        </div>
        <p className="text-xs text-muted-foreground">
          © 2026 Interleet, Inc. ·{" "}
          <Link to="/privacy" className="hover:text-foreground">Privacy</Link> ·{" "}
          <Link to="/terms" className="hover:text-foreground">Terms</Link>
        </p>
      </div>
      <div className="relative hidden overflow-hidden border-l border-border bg-card/40 md:block">
        <div className="grid-bg absolute inset-0 opacity-30" />
        <div className="pointer-events-none absolute -top-40 left-1/2 h-[500px] w-[600px] -translate-x-1/2 rounded-full bg-primary/20 blur-3xl" />
        <div className="relative flex h-full items-center justify-center p-10">
          <div className="max-w-md">
            <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
              The complete engineering arena
            </p>
            <h2 className="mt-3 text-3xl font-semibold leading-tight tracking-tight">
              Engineers don't ship algorithms.
              <br /> They ship systems.
            </h2>
            <p className="mt-4 text-sm text-muted-foreground">
              Practice the real stack — frontend through infra — with rubric-graded interviews and
              recruiter-verified profiles.
            </p>
            <div className="mt-8 space-y-2.5">
              {[
                <span key="challenges" className="inline-flex items-center gap-1.5 align-middle">
                  {challengeCount === null ? (
                    <span className="inline-block h-3.5 w-8 animate-pulse rounded bg-foreground/15 align-middle" />
                  ) : (
                    <span className="font-semibold text-foreground">{challengeCount.toLocaleString()}</span>
                  )}
                  <span>production-style challenges</span>
                </span>,
                <span key="interviews">AI mock interviews with full transcripts</span>,
                <span key="badges">Verified skill badges for hiring teams</span>
              ].map((node, idx) => (
                <div key={idx} className="flex items-start gap-2.5 text-sm">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                  <span className="text-foreground/85 leading-tight">{node}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>);

}