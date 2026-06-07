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
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
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

        <div className="relative ml-4 hidden flex-1 max-w-sm md:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search challenges, topics, people…"
            className="h-9 bg-card pl-9 pr-14"
          />
          <kbd className="pointer-events-none absolute right-2 top-1/2 hidden h-5 -translate-y-1/2 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] text-muted-foreground md:inline-flex">
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
