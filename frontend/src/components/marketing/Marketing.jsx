import { Link } from "react-router-dom";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/brand/Logo";

const links = [
{ href: "#features", label: "Features" },
{ href: "#interviews", label: "AI Interviews" },
{ href: "#system-design", label: "System Design" },
{ href: "#recruiters", label: "For Recruiters" }];


export function MarketingNav() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 md:px-8">
        <Logo />
        <nav className="hidden items-center gap-7 md:flex">
          {links.map((l) =>
          <a
            key={l.href}
            href={l.href}
            className="text-sm text-muted-foreground transition-colors hover:text-foreground">
            
              {l.label}
            </a>
          )}
        </nav>
        <div className="hidden items-center gap-2 md:flex">
          <Button asChild variant="ghost" size="sm">
            <Link to="/login">Sign in</Link>
          </Button>
          <Button asChild size="sm">
            <Link to="/signup">Get started</Link>
          </Button>
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
            onClick={() => setOpen(false)}
            className="rounded-md px-2 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-foreground">
            
                {l.label}
              </a>
          )}
            <div className="mt-2 flex gap-2">
              <Button asChild variant="outline" size="sm" className="flex-1">
                <Link to="/login">Sign in</Link>
              </Button>
              <Button asChild size="sm" className="flex-1">
                <Link to="/signup">Get started</Link>
              </Button>
            </div>
          </div>
        </div>
      }
    </header>);

}

export function MarketingFooter() {
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
        {[
        {
          title: "Product",
          items: ["Challenges", "AI Interviews", "System Design", "Leaderboards"]
        },
        { title: "Company", items: ["About", "Careers", "Blog", "Contact"] },
        { title: "Resources", items: ["Docs", "Changelog", "Status", "Security"] }].
        map((col) =>
        <div key={col.title}>
            <p className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
              {col.title}
            </p>
            <ul className="mt-3 space-y-2">
              {col.items.map((i) =>
            <li key={i}>
                  <a href="#" className="text-sm text-foreground/80 hover:text-foreground">
                    {i}
                  </a>
                </li>
            )}
            </ul>
          </div>
        )}
      </div>
      <div className="border-t border-border">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-2 px-4 py-5 text-xs text-muted-foreground md:flex-row md:items-center md:px-8">
          <p>© 2026 Interleet, Inc. Built for engineers.</p>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-foreground">Privacy</a>
            <a href="#" className="hover:text-foreground">Terms</a>
            <a href="#" className="hover:text-foreground">Cookies</a>
          </div>
        </div>
      </div>
    </footer>);

}