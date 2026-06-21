import { useState, useEffect, useRef, useMemo } from "react";
import { createPortal } from "react-dom";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Code2,
  Network,
  User,
  X,
  LayoutDashboard,
  Bot,
  Trophy,
  Swords,
  ShoppingBag,
  Settings,
  Sparkles,
  History,
  CornerDownLeft,
} from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { challenges as localSystemDesignChallenges } from "@/lib/simulator/challenges";
import { challenges as mockCodingChallenges, leaderboard as mockLeaderboard } from "@/lib/mock";

// Static pages configuration for fast client-side navigation search
const PLATFORM_PAGES = [
  { label: "Dashboard", path: "/app/dashboard", icon: LayoutDashboard, category: "Pages" },
  { label: "Challenges", path: "/app/challenges", icon: Code2, category: "Pages" },
  { label: "AI Interviews", path: "/app/interviews", icon: Bot, category: "Pages" },
  { label: "System Design", path: "/app/system-design", icon: Network, category: "Pages" },
  { label: "Leaderboard", path: "/app/leaderboard", icon: Trophy, category: "Pages" },
  { label: "Contest", path: "/app/contest", icon: Swords, category: "Pages" },
  { label: "Store", path: "/app/store", icon: ShoppingBag, category: "Pages" },
  { label: "Settings", path: "/app/settings", icon: Settings, category: "Pages" },
];

const POPULAR_SUGGESTIONS = [
  { label: "Rate Limiter", query: "rate limiter" },
  { label: "System Design", query: "system design" },
  { label: "Twitter", query: "twitter" },
  { label: "Leaderboard", query: "leaderboard" },
];

export function GlobalSearch() {
  const navigate = useNavigate();
  const modalInputRef = useRef(null);
  const dropdownRef = useRef(null);

  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [recentSearches, setRecentSearches] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);

  // Load recent searches on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem("interleet_recent_searches");
      if (stored) {
        setRecentSearches(JSON.parse(stored));
      }
    } catch (e) {
      console.error("Failed to load recent searches", e);
    }
  }, []);

  // Save recent search helper
  const addRecentSearch = (item) => {
    const term = item.title || item.label || item.username;
    if (!term) return;
    
    const updated = [term, ...recentSearches.filter((t) => t !== term)].slice(0, 4);
    setRecentSearches(updated);
    try {
      localStorage.setItem("interleet_recent_searches", JSON.stringify(updated));
    } catch (e) {
      console.error("Failed to save recent searches", e);
    }
  };

  // Keyboard shortcut CMD+K / CTRL+K to open
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Auto-focus input when modal opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        modalInputRef.current?.focus();
      }, 100);
      setActiveIndex(0);
      setQuery("");
    }
  }, [isOpen]);

  // Client-side search filters with safety checks (No Backend Calls)
  const filteredPages = useMemo(() => {
    if (!query.trim()) return [];
    const term = query.toLowerCase();
    return PLATFORM_PAGES.filter((p) => p.label?.toLowerCase().includes(term));
  }, [query]);

  const filteredSystemDesign = useMemo(() => {
    if (!query.trim()) return [];
    const term = query.toLowerCase();
    return (localSystemDesignChallenges || []).filter(
      (c) =>
        c.title?.toLowerCase().includes(term) ||
        c.brief?.toLowerCase().includes(term) ||
        (c.tags && c.tags.some((t) => t?.toLowerCase().includes(term)))
    );
  }, [query]);

  const filteredCodingChallenges = useMemo(() => {
    if (!query.trim()) return [];
    const term = query.toLowerCase();
    return (mockCodingChallenges || []).filter(
      (c) =>
        c.title?.toLowerCase().includes(term) ||
        c.summary?.toLowerCase().includes(term) ||
        (c.tags && c.tags.some((t) => t?.toLowerCase().includes(term)))
    );
  }, [query]);

  const filteredUsers = useMemo(() => {
    if (!query.trim()) return [];
    const term = query.toLowerCase();
    return (mockLeaderboard || []).filter(
      (u) =>
        u.username?.toLowerCase().includes(term) ||
        (u.badges && u.badges.some((b) => b?.toLowerCase().includes(term)))
    );
  }, [query]);

  // Flattened results array for keyboard navigation
  const flatItems = useMemo(() => {
    const list = [];
    
    // Group 1: Pages
    filteredPages.forEach((p) => {
      list.push({ ...p, type: "page" });
    });

    // Group 2: System Design
    filteredSystemDesign.forEach((c) => {
      list.push({ ...c, type: "system-design", title: c.title, id: c.id });
    });

    // Group 3: Coding Challenges
    filteredCodingChallenges.forEach((c) => {
      list.push({ ...c, type: "challenge", title: c.title, slug: c.slug });
    });

    // Group 4: Users / Profiles
    filteredUsers.forEach((u) => {
      list.push({ ...u, type: "user", username: u.username });
    });

    return list;
  }, [filteredPages, filteredSystemDesign, filteredCodingChallenges, filteredUsers]);

  // Keep index within bounds
  useEffect(() => {
    if (flatItems.length > 0 && activeIndex >= flatItems.length) {
      setActiveIndex(0);
    }
  }, [flatItems, activeIndex]);

  const handleSelect = (item) => {
    if (!item) return;
    addRecentSearch(item);
    setIsOpen(false);
    setQuery("");

    if (item.type === "page") {
      navigate(item.path);
    } else if (item.type === "system-design") {
      navigate(`/app/system-design?c=${item.id}`);
    } else if (item.type === "challenge") {
      navigate(`/app/challenges/${item.slug}`);
    } else if (item.type === "user") {
      navigate(`/app/profile/${item.username}`);
    }
  };

  const handleKeyDown = (e) => {
    if (!isOpen) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((prev) => (flatItems.length > 0 ? (prev + 1) % flatItems.length : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((prev) => (flatItems.length > 0 ? (prev - 1 + flatItems.length) % flatItems.length : 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (flatItems.length > 0 && activeIndex >= 0 && activeIndex < flatItems.length) {
        handleSelect(flatItems[activeIndex]);
      }
    } else if (e.key === "Escape") {
      e.preventDefault();
      setIsOpen(false);
    }
  };

  // Grouped results map
  const groupedResultSections = useMemo(() => {
    return [
      { title: "Pages", items: filteredPages.map((p) => ({ ...p, type: "page" })) },
      { title: "System Design", items: filteredSystemDesign.map((c) => ({ ...c, type: "system-design" })) },
      { title: "Coding Challenges", items: filteredCodingChallenges.map((c) => ({ ...c, type: "challenge" })) },
      { title: "People", items: filteredUsers.map((u) => ({ ...u, type: "user" })) },
    ].filter((section) => section.items.length > 0);
  }, [filteredPages, filteredSystemDesign, filteredCodingChallenges, filteredUsers]);

  return (
    <>
      {/* Navbar Trigger Box */}
      <div 
        onClick={() => setIsOpen(true)}
        className="relative ml-4 hidden md:block w-48 group cursor-pointer"
      >
        <div className="flex h-9 items-center w-full bg-card hover:bg-accent/40 border border-border/60 hover:border-primary/40 rounded-lg pl-9 pr-12 text-muted-foreground select-none transition-all duration-300">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground/60 group-hover:text-primary transition-colors" />
          <span className="text-xs group-hover:text-foreground transition-colors">Search…</span>
          <kbd className="absolute right-2 top-1/2 h-5 -translate-y-1/2 select-none items-center gap-1 rounded border border-border/80 bg-muted/80 px-1.5 font-mono text-[10px] text-muted-foreground group-hover:text-foreground transition-colors md:inline-flex">
            ⌘K
          </kbd>
        </div>
      </div>

      {/* Modal Popup Search UI wrapped in a React Portal to escape header backdrop-filter boundary */}
      {typeof document !== "undefined" && createPortal(
        <AnimatePresence>
          {isOpen && (
            <div className="fixed inset-0 z-[9999] flex items-start justify-center pt-24 overflow-hidden text-white">
              {/* Backdrop with high opacity black and beautiful backdrop blur */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setIsOpen(false)}
                className="absolute inset-0 bg-black/85 backdrop-blur-[8px]"
              />

              {/* Modal Body with glassmorphism, soft border, glow shadow */}
              <motion.div
                initial={{ scale: 0.95, opacity: 0, y: -10 }}
                animate={{ scale: 1, opacity: 1, y: 0 }}
                exit={{ scale: 0.95, opacity: 0, y: -10 }}
                transition={{ type: "spring", duration: 0.35, bounce: 0.15 }}
                className="relative w-full max-w-xl bg-zinc-950/85 backdrop-blur-xl border border-white/[0.08] shadow-[0_0_80px_rgba(255,101,0,0.18)] rounded-xl overflow-hidden flex flex-col z-10 mx-4"
              >
                {/* Header Input Area using standard HTML input for layout compatibility */}
                <div className="flex items-center gap-3 px-4 py-4 border-b border-white/[0.05] bg-white/[0.02]">
                  <Search className="h-5 w-5 text-primary shrink-0 animate-pulse" />
                  <input
                    ref={modalInputRef}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type a command or search term..."
                    className="flex-1 h-8 bg-transparent border-0 outline-none p-0 text-sm placeholder:text-muted-foreground/60 text-white font-medium focus:outline-none focus:ring-0"
                  />
                  {query && (
                    <button
                      onClick={() => {
                        setQuery("");
                        modalInputRef.current?.focus();
                      }}
                      className="h-5 w-5 flex items-center justify-center rounded-full hover:bg-white/10 text-muted-foreground hover:text-foreground transition-colors"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  )}
                  <kbd className="h-5 items-center rounded border border-white/[0.08] bg-white/[0.04] px-2 font-mono text-[9px] text-muted-foreground hidden sm:flex shrink-0">
                    ESC
                  </kbd>
                </div>

                {/* Middle Results Content */}
                <div 
                  ref={dropdownRef}
                  className="max-h-[300px] overflow-y-auto p-2 space-y-3 scrollbar-thin"
                >
                  {/* Search query entered - Results list */}
                  {query && groupedResultSections.map((section) => (
                    <div key={section.title} className="space-y-1">
                      <div className="px-3 py-1 font-mono text-[9px] font-bold tracking-widest text-[#FF6500]/70 uppercase border-b border-white/[0.03] pb-0.5 mb-1.5">
                        {section.title}
                      </div>
                      <div className="space-y-0.5">
                        {section.items.map((item) => {
                          const globalIdx = flatItems.findIndex((fi) => {
                            if (fi.type !== item.type) return false;
                            if (item.type === "page") return fi.path === item.path;
                            if (item.type === "system-design") return fi.id === item.id;
                            if (item.type === "challenge") return fi.slug === item.slug;
                            if (item.type === "user") return fi.username === item.username;
                            return false;
                          });

                          const isActive = globalIdx === activeIndex;
                          const Icon = item.icon || (item.type === "system-design" ? Network : item.type === "challenge" ? Code2 : User);

                          return (
                            <div
                              key={item.slug || item.id || item.username || item.path}
                              onClick={() => handleSelect(item)}
                              onMouseEnter={() => setActiveIndex(globalIdx)}
                              className={cn(
                                "flex w-full items-center justify-between rounded-lg px-3 py-2 text-left cursor-pointer transition-all duration-150 border border-transparent",
                                isActive 
                                  ? "bg-gradient-to-r from-[#FF6500]/15 to-transparent text-white border-l-2 border-l-[#FF6500] border-y-white/[0.02] border-r-white/[0.02] pl-[10px]" 
                                  : "hover:bg-white/[0.02] text-muted-foreground hover:text-white"
                              )}
                            >
                              <div className="flex items-center gap-3 min-w-0">
                                {item.type === "user" ? (
                                  <Avatar className="h-5 w-5 border border-white/[0.08]">
                                    {item.avatar ? (
                                      <img
                                        src={item.avatar}
                                        alt={item.username}
                                        className="h-full w-full object-cover rounded-full"
                                      />
                                    ) : (
                                      <AvatarFallback className="text-[9px] font-bold bg-zinc-900 text-zinc-300">
                                        {item.username?.slice(0, 2).toUpperCase()}
                                      </AvatarFallback>
                                    )}
                                  </Avatar>
                                ) : (
                                  <div className={cn(
                                    "flex h-5 w-5 items-center justify-center rounded bg-white/[0.03] text-zinc-400 border border-white/[0.05] transition-colors",
                                    isActive && "bg-[#FF6500]/25 text-[#FF6500] border-[#FF6500]/30"
                                  )}>
                                    <Icon className="h-3 w-3" />
                                  </div>
                                )}
                                
                                <div className="truncate">
                                  <span className={cn("text-xs font-semibold block leading-none transition-colors", isActive ? "text-[#FF6500]" : "text-zinc-200")}>
                                    {item.title || item.label || `@${item.username}`}
                                  </span>
                                  {item.summary && (
                                    <span className="text-[10px] text-muted-foreground/75 block truncate mt-0.5 max-w-[340px]">
                                      {item.summary}
                                    </span>
                                  )}
                                </div>
                              </div>

                              <div className="flex items-center gap-1.5 shrink-0 pl-2">
                                {item.difficulty && (
                                  <span className={cn(
                                    "text-[8px] font-bold px-1.5 py-0.5 rounded font-mono border",
                                    item.difficulty === "Easy" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/15" :
                                    item.difficulty === "Medium" ? "bg-amber-500/10 text-amber-400 border-amber-500/15" :
                                    item.difficulty === "Hard" ? "bg-red-500/10 text-red-400 border-red-500/15" :
                                    "bg-indigo-500/10 text-indigo-400 border-indigo-500/15"
                                  )}>
                                    {item.difficulty}
                                  </span>
                                )}
                                {item.rating && (
                                  <span className="text-[10px] font-mono font-bold text-[#FF6500]">
                                    {item.rating}
                                  </span>
                                )}
                                {isActive && (
                                  <CornerDownLeft className="h-3 w-3 text-primary animate-pulse" />
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  ))}

                  {/* No results state */}
                  {query && groupedResultSections.length === 0 && (
                    <div className="flex flex-col items-center justify-center py-12 text-center px-4">
                      <div className="p-3 rounded-full bg-white/[0.02] border border-white/[0.04] mb-3">
                        <Sparkles className="h-6 w-6 text-[#FF6500] opacity-50" />
                      </div>
                      <p className="text-xs font-semibold text-zinc-200">No matching items found</p>
                      <p className="text-[10px] text-muted-foreground mt-1 max-w-[240px]">
                        No matched pages, challenges, or user profiles for "{query}"
                      </p>
                    </div>
                  )}

                  {/* Empty query - Default/Recent search suggestions list */}
                  {!query && (
                    <div className="space-y-4">
                      {recentSearches.length > 0 && (
                        <div className="space-y-1.5">
                          <div className="px-3 py-1 font-mono text-[9px] font-bold tracking-widest text-muted-foreground/50 uppercase flex items-center gap-1.5">
                            <History className="h-3 w-3 text-primary" />
                            <span>Recent Searches</span>
                          </div>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-1 px-1">
                            {recentSearches.map((term) => (
                              <button
                                key={term}
                                onClick={() => setQuery(term)}
                                className="flex items-center gap-2 rounded-lg px-3 py-2 text-xs text-muted-foreground hover:bg-white/[0.03] hover:text-white transition-all text-left border border-white/[0.03]"
                              >
                                <Search className="h-3 w-3 shrink-0 opacity-60 text-primary" />
                                <span className="truncate">{term}</span>
                              </button>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Quick navigation guides */}
                      <div className="space-y-1.5">
                        <div className="px-3 py-1 font-mono text-[9px] font-bold tracking-widest text-[#FF6500]/70 uppercase">
                          Quick Jumps
                        </div>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 px-1">
                          {PLATFORM_PAGES.slice(0, 4).map((p) => {
                            const Icon = p.icon;
                            return (
                              <button
                                key={p.path}
                                onClick={() => handleSelect({ ...p, type: "page" })}
                                className="flex flex-col items-center justify-center p-3.5 rounded-lg border border-white/[0.03] bg-white/[0.01] hover:bg-[#FF6500]/10 hover:border-[#FF6500]/30 transition-all text-center gap-2 group/btn"
                              >
                                <Icon className="h-4.5 w-4.5 text-muted-foreground group-hover/btn:text-[#FF6500] transition-colors" />
                                <span className="text-[10px] font-semibold text-zinc-300 group-hover/btn:text-white transition-colors">{p.label}</span>
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Suggestions and Keymap at the Bottom (Requested) */}
                <div className="mt-auto bg-[#0a0a0c]/90 border-t border-white/[0.04] px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-[10px] text-muted-foreground/80">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-semibold text-muted-foreground/50">Suggestions:</span>
                    {POPULAR_SUGGESTIONS.map((item) => (
                      <button
                        key={item.label}
                        onClick={() => setQuery(item.query)}
                        className="px-2 py-0.5 rounded bg-white/[0.02] hover:bg-[#FF6500]/10 text-zinc-300 hover:text-white border border-white/[0.05] hover:border-[#FF6500]/30 transition-all"
                      >
                        {item.label}
                      </button>
                    ))}
                  </div>

                  <div className="flex items-center gap-3 font-mono text-[9px] text-muted-foreground/50 self-end sm:self-auto">
                    <span className="flex items-center gap-1">
                      <span className="border border-white/[0.08] px-1 rounded bg-white/[0.03]">↑↓</span> navigate
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="border border-white/[0.08] px-1 rounded bg-white/[0.03]">↵</span> open
                    </span>
                  </div>
                </div>
              </motion.div>
            </div>
          )}
        </AnimatePresence>,
        document.body
      )}
    </>
  );
}
