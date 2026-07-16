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

import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/brand/Logo";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

const links = [
{ href: "#features", label: "Features" },
{ href: "#interviews", label: "AI Interviews" },
{ href: "#system-design", label: "System Design" },
{ href: "#recruiters", label: "For Recruiters" }];


export function MarketingNav() {
  const [open, setOpen] = useState(false);
  const { isAuthenticated, user } = useSelector((state) => state.user || {});
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  const handleScroll = (e, href) => {
    e.preventDefault();
    const id = href.replace("#", "");
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  const initials = user?.full_name
    ? user.full_name
      .split(" ")
      .map((n) => n[0])
      .slice(0, 2)
      .join("")
      .toUpperCase()
    : "??";

  const firstName = user?.full_name?.split(" ")[0] || "Profile";

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 md:px-8">
        <Logo />
        <nav className="hidden items-center gap-7 md:flex">
          {links.map((l) =>
          <a
            key={l.href}
            href={l.href}
            onClick={(e) => handleScroll(e, l.href)}
            className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            
              {l.label}
            </a>
          )}
        </nav>
        <div className="hidden items-center gap-2 md:flex">
          {isAuthenticated ? (
            <div className="flex items-center gap-4">
              <Button asChild variant="ghost" size="sm">
                <Link to="/app/dashboard">Dashboard</Link>
              </Button>
              <Link to={`/app/profile/${user?.username}`} className="flex items-center gap-2 rounded-md p-1 pr-2 hover:bg-accent">
                <Avatar className="h-7 w-7 border border-border">
                  {user?.avatar ? (
                    <img
                      src={user.avatar}
                      alt={firstName}
                      className="h-full w-full object-cover rounded-full"
                    />
                  ) : (
                    <AvatarFallback className="bg-accent text-[11px]">{initials}</AvatarFallback>
                  )}
                </Avatar>
                <span className="hidden text-sm font-medium md:inline">{firstName}</span>
              </Link>
            </div>
          ) : (
            <>
              <Button asChild variant="ghost" size="sm">
                <Link to="/login">Sign in</Link>
              </Button>
              <Button asChild size="sm">
                <Link to="/signup">Get started</Link>
              </Button>
            </>
          )}
        </div>
        <button
          className="md:hidden"
          onClick={() => setOpen((o) => !o)}
          aria-label="Toggle menu">
          
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>
      {open &&
      <div className="border-t border-border bg-background px-4 py-3 md:hidden">
          <div className="flex flex-col gap-1">
            {links.map((l) =>
          <a
            key={l.href}
            href={l.href}
            onClick={(e) => {
              setOpen(false);
              handleScroll(e, l.href);
            }}
            className="rounded-md px-2 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-foreground">
            
                {l.label}
              </a>
          )}
            {isAuthenticated ? (
              <div className="mt-2 flex flex-col gap-2">
                <Button asChild variant="outline" size="sm" className="w-full">
                  <Link to="/app/dashboard" onClick={() => setOpen(false)}>Dashboard</Link>
                </Button>
                <Button asChild size="sm" className="w-full">
                  <Link to={`/app/profile/${user?.username}`} onClick={() => setOpen(false)}>
                    View Profile ({firstName})
                  </Link>
                </Button>
              </div>
            ) : (
              <div className="mt-2 flex gap-2">
                <Button asChild variant="outline" size="sm" className="flex-1">
                  <Link to="/login">Sign in</Link>
                </Button>
                <Button asChild size="sm" className="flex-1">
                  <Link to="/signup">Get started</Link>
                </Button>
              </div>
            )}
          </div>
        </div>
      }
    </header>);

}

export function MarketingFooter() {
  const columns = [
    {
      title: "Product",
      items: [
        { label: "Challenges", to: "/app/challenges" },
        { label: "AI Interviews", to: "/app/interviews" },
        { label: "System Design", to: "/app/system-design" },
        { label: "Leaderboards", to: "/app/leaderboard" },
      ],
    },
    {
      title: "Company",
      items: [
        { label: "About", to: "/about" },
        { label: "Blog", to: "/blog" },
        { label: "Contact", to: "/contact" },
      ],
    },
    {
      title: "Resources",
      items: [
        { label: "Changelog", to: "/changelog" },
        { label: "Status", to: "/status" },
        { label: "Security", to: "/security" },
      ],
    },
  ];

  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-12 md:grid-cols-5 md:px-8">
        <div className="md:col-span-2">
          <Logo />
          <p className="mt-3 max-w-sm text-sm text-muted-foreground">
            The complete engineering arena — practice the full stack, prove your skills, and get
            recruiter-verified.
          </p>
        </div>
        {columns.map((col) => (
          <div key={col.title}>
            <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
              {col.title}
            </p>
            <ul className="mt-3 space-y-2">
              {col.items.map((i) => (
                <li key={i.label}>
                  <Link to={i.to} className="text-sm text-foreground/80 hover:text-foreground">
                    {i.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="border-t border-border">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-2 px-4 py-5 text-xs text-muted-foreground md:flex-row md:items-center md:px-8">
          <p>© 2026 Interleet, Inc. Built for engineers.</p>
          <div className="flex items-center gap-4">
            <Link to="/privacy" className="hover:text-foreground">Privacy</Link>
            <Link to="/terms" className="hover:text-foreground">Terms</Link>
            <Link to="/cookies" className="hover:text-foreground">Cookies</Link>
          </div>
        </div>
      </div>
    </footer>);

}