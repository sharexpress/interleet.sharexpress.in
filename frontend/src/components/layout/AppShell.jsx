import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Code2,
  Bot,
  Network,
  Trophy,
  User,
  Settings,
  Menu,
  Search,
  Bell,
  LogOut,
  Briefcase,
  ShieldCheck } from
"lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { Logo } from "@/components/brand/Logo";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger } from
"@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger, SheetTitle, SheetHeader } from "@/components/ui/sheet";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { user } from "@/lib/mock";

const nav = [
{ to: "/app/dashboard", label: "Dashboard", icon: LayoutDashboard },
{ to: "/app/challenges", label: "Challenges", icon: Code2 },
{ to: "/app/interviews", label: "AI Interviews", icon: Bot },
{ to: "/app/system-design", label: "System Design", icon: Network },
{ to: "/app/leaderboard", label: "Leaderboard", icon: Trophy }];


const more = [
{ to: "/app/profile/alex.morgan", label: "Profile", icon: User },
{ to: "/app/settings", label: "Settings", icon: Settings },
{ to: "/recruiter", label: "Recruiter", icon: Briefcase },
{ to: "/admin", label: "Admin", icon: ShieldCheck }];


function NavLinks({
  orientation = "horizontal",
  onNavigate



}) {
  const path = useLocation().pathname;
  const items = orientation === "vertical" ? [...nav, ...more] : nav;
  return (
    <nav
      className={cn(
        orientation === "horizontal" ?
        "hidden items-center gap-1 lg:flex" :
        "flex flex-1 flex-col gap-1 px-2"
      )}>
      
      {items.map((item) => {
        const active =
        path.startsWith(item.to) || item.to === "/app/dashboard" && path === "/app";
        const Icon = item.icon;
        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            className={cn(
              "flex items-center gap-2 rounded-md px-3 py-1.5 text-sm transition-colors",
              active ?
              "bg-accent text-foreground" :
              "text-muted-foreground hover:bg-accent/60 hover:text-foreground",
              orientation === "vertical" && "px-2.5 py-2"
            )}>
            
            <Icon className="h-4 w-4 shrink-0" />
            <span className="truncate">{item.label}</span>
          </Link>);

      })}
    </nav>);

}

export function AppShell({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b border-border bg-background/85 px-4 backdrop-blur md:px-6">
        {/* Mobile menu */}
        <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="lg:hidden">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[260px] p-0">
            <SheetHeader className="h-14 border-b border-border px-3">
              <SheetTitle className="flex items-center">
                <Logo />
              </SheetTitle>
            </SheetHeader>
            <div className="flex h-[calc(100vh-56px)] flex-col py-2">
              <NavLinks orientation="vertical" onNavigate={() => setMobileOpen(false)} />
            </div>
          </SheetContent>
        </Sheet>

        <div className="flex items-center gap-6">
          <Logo />
          <NavLinks />
        </div>

        <div className="relative ml-4 hidden flex-1 max-w-sm md:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search challenges, topics, people…"
            className="h-9 bg-card pl-9 pr-14" />
          
          <kbd className="pointer-events-none absolute right-2 top-1/2 hidden h-5 -translate-y-1/2 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] text-muted-foreground md:inline-flex">
            ⌘K
          </kbd>
        </div>

        <div className="ml-auto flex items-center gap-2">
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="h-4 w-4" />
            <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-primary" />
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 rounded-md p-1 pr-2 hover:bg-accent">
                <Avatar className="h-7 w-7 border border-border">
                  <AvatarFallback className="bg-accent text-[11px]">AM</AvatarFallback>
                </Avatar>
                <span className="hidden text-sm font-medium md:inline">Alex</span>
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>
                <div className="flex flex-col">
                  <span className="text-sm font-medium">{user.name}</span>
                  <span className="text-xs text-muted-foreground">{user.title}</span>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link to="/app/profile/alex.morgan">View profile</Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link to="/app/settings">Settings</Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link to="/recruiter">Recruiter</Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link to="/admin">Admin</Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link to="/login" className="text-destructive">
                  <LogOut className="mr-2 h-4 w-4" />
                  Sign out
                </Link>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
      <main className="min-w-0 flex-1">{children}</main>
    </div>);

}

export function PageHeader({
  title,
  description,
  actions,
  badge





}) {
  return (
    <div className="flex flex-col gap-3 border-b border-border px-4 py-5 md:flex-row md:items-center md:justify-between md:px-8 md:py-6">
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <h1 className="truncate text-xl font-semibold tracking-tight md:text-2xl">{title}</h1>
          {badge &&
          <Badge variant="outline" className="font-mono text-[10px] uppercase tracking-wider">
              {badge}
            </Badge>
          }
        </div>
        {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
    </div>);

}