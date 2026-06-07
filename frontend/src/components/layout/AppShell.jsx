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
  ShieldCheck,
  Swords,
  ShoppingBag,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { API } from "@/api/api";

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
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger, SheetTitle, SheetHeader } from "@/components/ui/sheet";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

import { LogoutUser } from "@/redux/slices/userSlice";

const nav = [
  { to: "/app/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/app/challenges", label: "Challenges", icon: Code2 },
  { to: "/app/interviews", label: "AI Interviews", icon: Bot },
  { to: "/app/system-design", label: "System Design", icon: Network },
  { to: "/app/leaderboard", label: "Leaderboard", icon: Trophy },
  { to: "/app/contest", label: "Contest", icon: Swords },
  { to: "/app/store", label: "Store", icon: ShoppingBag },
];

function NavLinks({ user, orientation = "horizontal", onNavigate }) {
  const path = useLocation().pathname;

  const items = [...nav];
  if (orientation === "vertical") {
    items.push({ to: "/app/settings", label: "Settings", icon: Settings });
    if (user?.role === "recruiter") {
      items.push({ to: "/recruiter", label: "Recruiter", icon: Briefcase });
    }
    if (user?.role === "admin") {
      items.push({ to: "/admin", label: "Admin", icon: ShieldCheck });
    }
  }

  return (
    <nav
      className={cn(
        orientation === "horizontal"
          ? "hidden items-center gap-1 lg:flex"
          : "flex flex-1 flex-col gap-1 px-2",
      )}
    >
      {items.map((item) => {
        const active =
          path.startsWith(item.to) || (item.to === "/app/dashboard" && path === "/app");
        const Icon = item.icon;
        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            className={cn(
              "flex items-center gap-2 rounded-md px-3 py-1.5 text-sm transition-colors",
              active
                ? "bg-accent text-foreground"
                : "text-muted-foreground hover:bg-accent/60 hover:text-foreground",
              orientation === "vertical" && "px-2.5 py-2",
            )}
          >
            <Icon className="h-4 w-4 shrink-0" />
            <span className="truncate">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}

export function AppShell({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { user } = useSelector((state) => state.user);

  // Command Palette Search State
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState({ challenges: [], users: [], topics: [] });
  const [isSearching, setIsSearching] = useState(false);

  // Keyboard shortcut listener (⌘K or Ctrl+K)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandPaletteOpen(prev => !prev);
      }
      if (e.key === "Escape") {
        setCommandPaletteOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Debounced Search API fetcher
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults({ challenges: [], users: [], topics: [] });
      return;
    }

    const delayDebounce = setTimeout(async () => {
      setIsSearching(true);
      try {
        const res = await API.get(`/api/search?q=${encodeURIComponent(searchQuery)}`);
        if (res.data && res.data.success) {
          setSearchResults(res.data.results);
        }
      } catch (err) {
        console.error("Failed to query global search", err);
      } finally {
        setIsSearching(false);
      }
    }, 300);

    return () => clearTimeout(delayDebounce);
  }, [searchQuery]);

  const quickNavs = [
    { label: "Dashboard", path: "/app/dashboard", icon: LayoutDashboard },
    { label: "Challenges", path: "/app/challenges", icon: Code2 },
    { label: "AI Interviews", path: "/app/interviews", icon: Bot },
    { label: "System Design", path: "/app/system-design", icon: Network },
    { label: "Leaderboard", path: "/app/leaderboard", icon: Trophy },
    { label: "Contests", path: "/app/contest", icon: Swords },
    { label: "Store", path: "/app/store", icon: ShoppingBag },
    { label: "Settings", path: "/app/settings", icon: Settings },
  ];

  const commands = [
    { name: "Start New Mock Interview", icon: Bot, hint: "Action", action: () => navigate("/app/interviews/setup") },
    { name: "Register Face ID", icon: ShieldCheck, hint: "Action", action: () => navigate("/face-enrollment") },
    { name: "Verify Face ID Status", icon: ShieldCheck, hint: "Action", action: () => navigate("/face-verification") },
    { name: "Sign Out", icon: LogOut, hint: "Action", action: () => handleLogout() },
  ];

  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  const fetchNotifications = async () => {
    try {
      const res = await API.get("/api/notifications");
      if (res.data && res.data.success) {
        setNotifications(res.data.data);
        setUnreadCount(res.data.data.filter((n) => !n.read).length);
      }
    } catch (err) {
      console.error("Failed to fetch notifications", err);
    }
  };

  useEffect(() => {
    if (!user) return;
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 8000);
    return () => clearInterval(interval);
  }, [user]);

  const handleNotificationClick = async (notif) => {
    try {
      await API.post(`/api/notifications/${notif.id}/read`);
      fetchNotifications();
      if (notif.link) {
        navigate(notif.link);
      }
    } catch (err) {
      console.error("Error marking notification as read", err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await API.post("/api/notifications/read-all");
      fetchNotifications();
      toast.success("All notifications marked as read");
    } catch (err) {
      console.error("Error marking all read", err);
    }
  };

  // Initials from full_name e.g. "Santusht Kotai" → "SK"
  const initials = user?.full_name
    ? user.full_name
      .split(" ")
      .map((n) => n[0])
      .slice(0, 2)
      .join("")
      .toUpperCase()
    : "??";

  const firstName = user?.full_name?.split(" ")[0] || "Engineer";

  const handleLogout = async () => {
    await dispatch(LogoutUser());
    navigate("/login", { replace: true });
  };

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
              <NavLinks user={user} orientation="vertical" onNavigate={() => setMobileOpen(false)} />
            </div>
          </SheetContent>
        </Sheet>

        <div className="flex items-center gap-6">
          <Logo />
          <NavLinks user={user} />
        </div>

        {/* Global Search Option (Command Palette Trigger) */}
        <div 
          onClick={() => setCommandPaletteOpen(true)}
          className="relative ml-4 hidden flex-1 max-w-sm md:block cursor-pointer group"
        >
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground group-hover:text-foreground transition-colors" />
          <div className="h-9 bg-card border border-border rounded-md pl-9 pr-14 flex items-center text-xs text-muted-foreground hover:bg-accent/40 hover:text-foreground transition-all">
            Search challenges, topics, people…
          </div>
          <kbd className="pointer-events-none absolute right-2 top-1/2 hidden h-5 -translate-y-1/2 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[9px] text-muted-foreground md:inline-flex">
            ⌘K
          </kbd>
        </div>

        <div className="ml-auto flex items-center gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-4 w-4" />
                {unreadCount > 0 && (
                  <span className="absolute right-1 top-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[8px] font-bold text-primary-foreground">
                    {unreadCount}
                  </span>
                )}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80">
              <DropdownMenuLabel className="flex items-center justify-between">
                <span>Notifications</span>
                {unreadCount > 0 && (
                  <button
                    onClick={handleMarkAllRead}
                    className="text-[10px] text-primary hover:underline"
                  >
                    Mark all as read
                  </button>
                )}
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <div className="max-h-72 overflow-y-auto">
                {notifications.length === 0 ? (
                  <p className="p-4 text-center text-xs text-muted-foreground">
                    No notifications yet.
                  </p>
                ) : (
                  notifications.map((n) => (
                    <DropdownMenuItem
                      key={n.id}
                      onClick={() => handleNotificationClick(n)}
                      className={cn(
                        "flex flex-col items-start gap-1 p-3 cursor-pointer",
                        !n.read && "bg-accent/40"
                      )}
                    >
                      <div className="flex w-full items-start justify-between gap-2">
                        <span className="font-semibold text-xs text-foreground">
                          {n.title}
                        </span>
                        {!n.read && (
                          <span className="h-1.5 w-1.5 rounded-full bg-primary shrink-0 mt-1" />
                        )}
                      </div>
                      <p className="text-[11px] text-muted-foreground leading-snug">
                        {n.message}
                      </p>
                      <span className="text-[9px] text-muted-foreground/60 mt-0.5">
                        {new Date(n.created_at).toLocaleDateString()}
                      </span>
                    </DropdownMenuItem>
                  ))
                )}
              </div>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => navigate("/app/settings")}
                className="justify-center text-xs font-semibold text-primary hover:underline cursor-pointer"
              >
                View all settings & history
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 rounded-md p-1 pr-2 hover:bg-accent">
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
              </button>
            </DropdownMenuTrigger>

            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>
                <div className="flex flex-col">
                  <span className="text-sm font-medium">{user?.full_name || "Engineer"}</span>
                  <span className="text-xs text-muted-foreground">@{user?.username || ""}</span>
                </div>
              </DropdownMenuLabel>

              <DropdownMenuSeparator />

              <DropdownMenuItem asChild>
                <Link to={`/app/profile/${user?.username}`}>
                  <User className="mr-2 h-4 w-4" />
                  View profile
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link to="/app/settings">
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </Link>
              </DropdownMenuItem>
              {user?.role === "recruiter" && (
                <DropdownMenuItem asChild>
                  <Link to="/recruiter">
                    <Briefcase className="mr-2 h-4 w-4" />
                    Recruiter
                  </Link>
                </DropdownMenuItem>
              )}
              {user?.role === "admin" && (
                <DropdownMenuItem asChild>
                  <Link to="/admin">
                    <ShieldCheck className="mr-2 h-4 w-4" />
                    Admin
                  </Link>
                </DropdownMenuItem>
              )}

              <DropdownMenuSeparator />

              <DropdownMenuItem
                onClick={handleLogout}
                className="text-destructive focus:text-destructive cursor-pointer"
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sign out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <main className="min-w-0 flex-1">{children}</main>

      {/* Global Search Command Palette Modal */}
      {commandPaletteOpen && (
        <div 
          className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4 bg-black/80 backdrop-blur-sm animate-fade-in"
          onClick={() => setCommandPaletteOpen(false)}
        >
          <Card 
            className="w-full max-w-2xl border-zinc-800 bg-zinc-950 p-0 overflow-hidden shadow-2xl relative"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Search Header */}
            <div className="flex items-center border-b border-zinc-900 px-4 py-3">
              <Search className="h-5 w-5 text-muted-foreground mr-3 shrink-0" />
              <input
                autoFocus
                type="text"
                placeholder="Type to search challenges, topics, developers, or commands..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 bg-transparent border-none text-white placeholder-zinc-500 text-sm focus:outline-none focus:ring-0 min-w-0"
              />
              <Badge variant="outline" className="font-mono text-[9px] text-zinc-500 bg-zinc-900 border-zinc-850 px-2 py-0.5 shrink-0 ml-2">ESC</Badge>
            </div>
            
            {/* Results / Suggestions panel */}
            <div className="max-h-[50vh] overflow-y-auto p-2 space-y-4 animate-fade-in">
              {!searchQuery.trim() ? (
                <div className="space-y-4">
                  {/* Suggestions Panel */}
                  <div className="p-2">
                    <h4 className="text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-500 px-2 py-1">Quick Navigation</h4>
                    <div className="grid grid-cols-2 gap-1 mt-2">
                      {quickNavs.map((n) => (
                        <button
                          key={n.path}
                          onClick={() => {
                            navigate(n.path);
                            setCommandPaletteOpen(false);
                          }}
                          className="flex items-center gap-3 w-full text-left px-3 py-2.5 rounded-lg hover:bg-zinc-900/80 text-zinc-300 hover:text-white text-xs font-semibold group transition-all"
                        >
                          <n.icon className="h-4 w-4 text-zinc-500 group-hover:text-primary transition-colors shrink-0" />
                          <span className="truncate">{n.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="p-2 border-t border-zinc-900/60">
                    <h4 className="text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-500 px-2 py-1">System Actions</h4>
                    <div className="space-y-0.5 mt-2">
                      {commands.map((c) => (
                        <button
                          key={c.name}
                          onClick={() => {
                            c.action();
                            setCommandPaletteOpen(false);
                          }}
                          className="flex items-center justify-between w-full text-left px-3 py-2.5 rounded-lg hover:bg-zinc-900/80 text-zinc-300 hover:text-white text-xs font-semibold group transition-all"
                        >
                          <span className="flex items-center gap-3">
                            <c.icon className="h-4 w-4 text-zinc-500 group-hover:text-primary transition-colors shrink-0" />
                            {c.name}
                          </span>
                          <span className="text-[9px] text-zinc-650 font-mono group-hover:text-zinc-500">{c.hint}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              ) : isSearching ? (
                <div className="py-12 text-center text-muted-foreground">
                  <Sparkles className="h-5 w-5 animate-spin mx-auto text-[#FF6500] mb-2" />
                  <p className="font-mono text-[11px]">Scanning the arena databases...</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Challenges search result list */}
                  {searchResults.challenges?.length > 0 && (
                    <div className="p-2">
                      <h4 className="text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-500 px-2 py-1">Challenges</h4>
                      <div className="space-y-0.5 mt-2">
                        {searchResults.challenges.map((c) => (
                          <button
                            key={c.slug}
                            onClick={() => {
                              navigate(`/app/challenges/${c.slug}`);
                              setCommandPaletteOpen(false);
                            }}
                            className="flex items-center justify-between w-full text-left px-3 py-2.5 rounded-lg hover:bg-zinc-900/80 text-zinc-200 hover:text-white text-xs font-semibold group transition-all"
                          >
                            <span className="flex items-center gap-3 min-w-0">
                              <Code2 className="h-4 w-4 text-zinc-500 group-hover:text-primary transition-colors shrink-0" />
                              <span className="truncate">{c.title}</span>
                            </span>
                            <Badge variant="outline" className="text-[9px] uppercase font-mono px-1.5 shrink-0 border-zinc-800 text-zinc-400 bg-zinc-900">{c.difficulty}</Badge>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* System Design results */}
                  {searchResults.topics?.length > 0 && (
                    <div className="p-2 border-t border-zinc-900/60">
                      <h4 className="text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-500 px-2 py-1">System Design Topics</h4>
                      <div className="space-y-0.5 mt-2">
                        {searchResults.topics.map((t) => (
                          <button
                            key={t.title}
                            onClick={() => {
                              navigate("/app/system-design");
                              setCommandPaletteOpen(false);
                            }}
                            className="flex items-center justify-between w-full text-left px-3 py-2.5 rounded-lg hover:bg-zinc-900/80 text-zinc-200 hover:text-white text-xs font-semibold group transition-all"
                          >
                            <span className="flex items-center gap-3 min-w-0">
                              <Network className="h-4 w-4 text-zinc-500 group-hover:text-primary transition-colors shrink-0" />
                              <span className="truncate">{t.title}</span>
                            </span>
                            <span className="text-[10px] text-zinc-500 group-hover:text-zinc-400 font-mono shrink-0">System Design</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Users search result list */}
                  {searchResults.users?.length > 0 && (
                    <div className="p-2 border-t border-zinc-900/60">
                      <h4 className="text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-500 px-2 py-1">Developers</h4>
                      <div className="space-y-0.5 mt-2">
                        {searchResults.users.map((u) => (
                          <button
                            key={u.username}
                            onClick={() => {
                              navigate(`/app/profile/${u.username}`);
                              setCommandPaletteOpen(false);
                            }}
                            className="flex items-center justify-between w-full text-left px-3 py-2.5 rounded-lg hover:bg-zinc-900/80 text-zinc-200 hover:text-white text-xs font-semibold group transition-all"
                          >
                            <div className="flex items-center gap-3 min-w-0">
                              <Avatar className="h-6 w-6 border border-zinc-800 shrink-0">
                                <AvatarImage src={u.avatar} />
                                <AvatarFallback className="text-[9px] bg-zinc-800 text-zinc-300 font-bold">{u.username.slice(0, 2).toUpperCase()}</AvatarFallback>
                              </Avatar>
                              <div className="min-w-0">
                                <p className="truncate font-semibold text-xs text-white text-left">@{u.username}</p>
                                <p className="text-[9px] text-muted-foreground truncate text-left">{u.full_name || u.email}</p>
                              </div>
                            </div>
                            <span className="text-[10px] text-zinc-500 group-hover:text-zinc-400 font-mono shrink-0">Profile</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Empty Result */}
                  {(!searchResults.challenges?.length && !searchResults.topics?.length && !searchResults.users?.length) && (
                    <div className="py-12 text-center text-muted-foreground">
                      <p className="font-mono text-xs">No records found matching "{searchQuery}".</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

export function PageHeader({ title, description, actions, badge }) {
  return (
    <div className="flex flex-col gap-2 border-b border-border px-4 py-3 md:flex-row md:items-center md:justify-between md:px-8 md:py-4">
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <h1 className="truncate text-lg font-semibold tracking-tight md:text-xl">{title}</h1>
          {badge && (
            <Badge variant="outline" className="font-mono text-[10px] uppercase tracking-wider">
              {badge}
            </Badge>
          )}
        </div>
        {description && <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
    </div>
  );
}
