import { AppShell } from "@/components/layout/AppShell";
import { useNavigate, useLocation, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardContent, CardDescription, CardTitle } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import {
  User, Mail, Phone, KeyRound, ChevronRight, ExternalLink, Github,
  Lock, Shield, EyeOff, CreditCard, Award, ShoppingBag, Bell,
  Globe, Sparkles, Terminal, Cpu, Brain, Database, Bug, GitBranch,
  RefreshCw, Trash2, Plus, Check, Laptop, Smartphone, Eye, HelpCircle,
  FileDown, Star, AlertTriangle, ShieldCheck, MapPin, Link as LinkIcon,
  ChevronDown
} from "lucide-react";
import React, { useState, useCallback, useMemo, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { toast } from "sonner";
import { GetCurrentUser } from "@/redux/slices/userSlice";
import { API } from "@/api/api";

const getDivisionTier = (rating, rank) => {
  if (rank === 1) return { name: "Grandmaster Elite", color: "bg-purple-500/15 text-purple-400 border-purple-500/30" };
  if (rank <= 3) return { name: "Grandmaster", color: "bg-pink-500/15 text-pink-400 border-pink-500/30" };
  if (rank <= 5) return { name: "Master Architect", color: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30" };
  if (rating >= 2500) return { name: "Diamond Stack", color: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30" };
  if (rating >= 2000) return { name: "Gold Tech", color: "bg-amber-500/15 text-amber-400 border-amber-500/30" };
  if (rating >= 1500) return { name: "Silver Developer", color: "bg-slate-400/15 text-slate-300 border-slate-400/30" };
  return { name: "Bronze Apprentice", color: "bg-orange-950/20 text-orange-400 border-orange-900/30" };
};

const navItems = [
  { key: "profile", label: "Profile Settings", icon: User },
  { key: "account", label: "Account Settings", icon: Shield },
  { key: "security", label: "Security & Passkeys", icon: Lock },
  { key: "privacy", label: "Privacy Details", icon: EyeOff },
  { key: "billing", label: "Billing & Plans", icon: CreditCard },
  { key: "points", label: "Points & XP", icon: Award },
  { key: "orders", label: "Orders History", icon: ShoppingBag },
  { key: "notifications", label: "Notification Prefs", icon: Bell },
];

const AVAILABLE_AVATARS = [
  { id: "https://api.dicebear.com/7.x/bottts/svg?seed=Buster", name: "Cyber Bot" },
  { id: "https://api.dicebear.com/7.x/adventurer/svg?seed=Felix", name: "Adventurer" },
  { id: "https://api.dicebear.com/7.x/pixel-art/svg?seed=Wizard", name: "Pixel Wizard" },
  { id: "https://api.dicebear.com/7.x/shapes/svg?seed=Shape", name: "Abstract" },
  { id: "https://api.dicebear.com/7.x/micah/svg?seed=Aria", name: "Neo Human" },
  { id: "https://api.dicebear.com/7.x/identicon/svg?seed=Matrix", name: "Identicon" }
];

function Settings() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get("tab") || "profile";
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const active = useMemo(() => {
    return navItems.some(n => n.key === activeTab) ? activeTab : "profile";
  }, [activeTab]);

  const setActive = (tabKey) => {
    setSearchParams({ tab: tabKey });
    setMobileMenuOpen(false);
  };

  return (
    <AppShell>
      <div className="grid min-h-[calc(100vh-56px)] grid-cols-1 md:grid-cols-[260px_1fr]">
        
        {/* Sidebar Nav */}
        <aside className="border-b border-border bg-card/20 px-4 py-4 md:border-b-0 md:border-r md:px-6 md:py-8">
          <div className="flex items-center justify-between md:block">
            <h1 className="text-xl md:text-2xl font-bold tracking-tight text-white mb-0 md:mb-6">Settings</h1>
            
            {/* Mobile Nav Button */}
            <Button 
              variant="outline" 
              size="sm" 
              className="md:hidden flex items-center gap-1.5 text-xs border-zinc-800"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span>{navItems.find(n => n.key === active)?.label || "Menu"}</span>
              <ChevronDown className="h-3 w-3" />
            </Button>
          </div>

          <nav className={`mt-4 md:mt-0 space-y-1 ${mobileMenuOpen ? "block" : "hidden md:block"}`}>
            {navItems.map((n) => {
              const Icon = n.icon;
              const isSelected = active === n.key;
              return (
                <button
                  key={n.key}
                  onClick={() => setActive(n.key)}
                  className={`flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-left text-sm font-medium transition-all ${
                    isSelected
                      ? "bg-primary/10 text-primary border border-primary/20 shadow-sm"
                      : "text-muted-foreground border border-transparent hover:bg-zinc-850/50 hover:text-foreground"
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isSelected ? "text-primary" : "text-muted-foreground"}`} />
                  <span>{n.label}</span>
                </button>
              );
            })}
          </nav>
        </aside>

        {/* Dynamic Content Panel */}
        <main className="px-4 py-6 md:px-12 md:py-8 bg-zinc-950/10">
          <div className="max-w-5xl">
            {active === "profile" && <ProfileSection />}
            {active === "account" && <AccountSection />}
            {active === "security" && <SecuritySection />}
            {active === "privacy" && <PrivacySection />}
            {active === "billing" && <BillingSection />}
            {active === "points" && <PointsSection />}
            {active === "orders" && <OrdersSection />}
            {active === "notifications" && <NotificationsSection />}
          </div>
        </main>

      </div>
    </AppShell>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 1. PROFILE SECTION                                                         */
/* ────────────────────────────────────────────────────────────────────────── */
function ProfileSection() {
  const { user } = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const [saving, setSaving] = useState(false);
  const [formState, setFormState] = useState({
    full_name: "",
    location: "",
    github_username: "",
    website: "",
    bio: "",
    country: "",
    linkedin_url: "",
    portfolio_url: "",
    avatar: ""
  });

  useEffect(() => {
    if (user) {
      setFormState({
        full_name: user.full_name || user.name || "",
        location: user.location || "",
        github_username: user.github_username || "",
        website: user.website || "",
        bio: user.bio || "",
        country: user.country || "",
        linkedin_url: user.linkedin_url || "",
        portfolio_url: user.portfolio_url || "",
        avatar: user.avatar || ""
      });
    }
  }, [user]);

  const handleChange = (field, value) => {
    setFormState(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await API.put("/api/profile", formState);
      if (res.data && res.data.success) {
        toast.success("Profile details saved successfully!");
        dispatch(GetCurrentUser());
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to save profile changes.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Profile Settings</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Customize your public presence across the Interleet arena. Any modifications will instantly update your public developer card.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-6 items-start">
        
        {/* Profile Inputs */}
        <form onSubmit={handleSave} className="space-y-6 bg-card border border-border rounded-xl p-5 md:p-6 shadow-sm">
          
          {/* Avatar Selector */}
          <div className="space-y-3">
            <label className="text-xs font-semibold text-zinc-300 block">Select Avatar Character</label>
            <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
              {AVAILABLE_AVATARS.map((av) => {
                const isSelected = formState.avatar === av.id;
                return (
                  <button
                    key={av.id}
                    type="button"
                    onClick={() => handleChange("avatar", av.id)}
                    className={`relative aspect-square rounded-lg border-2 bg-zinc-900/50 p-1 flex items-center justify-center overflow-hidden hover:bg-zinc-800 transition-all ${
                      isSelected ? "border-primary" : "border-zinc-800"
                    }`}
                  >
                    <img src={av.id} alt={av.name} className="w-full h-full object-cover" />
                    {isSelected && (
                      <span className="absolute bottom-1 right-1 bg-primary text-white rounded-full p-0.5">
                        <Check className="h-2 w-2" />
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
            
            <div className="pt-2">
              <label className="text-[10px] font-semibold text-zinc-400 block mb-1">Or paste a custom avatar URL</label>
              <input
                type="text"
                value={formState.avatar}
                onChange={(e) => handleChange("avatar", e.target.value)}
                placeholder="e.g. https://domain.com/my-photo.jpg"
                className="w-full h-9 rounded-md border border-zinc-800 bg-zinc-950 px-3 text-xs text-foreground focus:border-primary focus:outline-none transition-colors"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-zinc-300 block">Full Name</label>
              <input
                type="text"
                value={formState.full_name}
                onChange={(e) => handleChange("full_name", e.target.value)}
                placeholder="e.g. John Doe"
                className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
                required
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-zinc-300 block">Country</label>
              <input
                type="text"
                value={formState.country}
                onChange={(e) => handleChange("country", e.target.value)}
                placeholder="e.g. India or United States"
                className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-zinc-300 block">Short Bio</label>
            <textarea
              value={formState.bio}
              onChange={(e) => handleChange("bio", e.target.value)}
              placeholder="Tell the community about your stack, engineering goals, or hobbies..."
              rows={3}
              className="w-full rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-foreground focus:border-primary focus:outline-none transition-colors resize-none"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-zinc-300 block">Location</label>
              <input
                type="text"
                value={formState.location}
                onChange={(e) => handleChange("location", e.target.value)}
                placeholder="e.g. San Francisco, CA"
                className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-zinc-300 block">Personal Portfolio Website</label>
              <input
                type="text"
                value={formState.website}
                onChange={(e) => handleChange("website", e.target.value)}
                placeholder="e.g. my-portfolio.com"
                className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-zinc-300 block">GitHub Username</label>
              <div className="relative">
                <Github className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  value={formState.github_username}
                  onChange={(e) => handleChange("github_username", e.target.value)}
                  placeholder="username"
                  className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 pl-9 pr-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-zinc-300 block">LinkedIn Username</label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-xs font-bold text-muted-foreground select-none">in/</span>
                <input
                  type="text"
                  value={formState.linkedin_url}
                  onChange={(e) => handleChange("linkedin_url", e.target.value)}
                  placeholder="username"
                  className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 pl-9 pr-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
                />
              </div>
            </div>
          </div>

          <Button type="submit" disabled={saving} className="w-full h-10 text-sm font-semibold">
            {saving ? "Saving Changes..." : "Save Profile Details"}
          </Button>

        </form>

        {/* Live Leaderboard Card Preview */}
        <div className="space-y-2 lg:sticky lg:top-4">
          <label className="text-xs font-bold text-zinc-400 tracking-wider uppercase block">Real-time Card Preview</label>
          <LeaderboardCardPreview formState={formState} user={user} />
        </div>

      </div>
    </div>
  );
}

function LeaderboardCardPreview({ formState, user }) {
  const level = Math.floor((user?.xp || 0) / 1000) + 1;
  const rating = user?.rating || 1000;
  const rank = user?.rank || 1;
  const division = getDivisionTier(rating, rank);

  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-5 shadow-lg backdrop-blur-md relative overflow-hidden h-fit space-y-5">
      {/* Background radial highlight */}
      <div className="absolute right-0 top-0 h-24 w-24 rounded-full bg-primary/5 blur-2xl pointer-events-none" />

      <div className="flex flex-col items-center text-center space-y-2">
        <div className="relative">
          <div className="w-20 h-20 rounded-full border border-zinc-700 bg-zinc-800/40 overflow-hidden flex items-center justify-center">
            {formState.avatar ? (
              <img src={formState.avatar} alt="Avatar" className="w-full h-full object-cover" />
            ) : (
              <span className="text-lg font-bold text-muted-foreground">?</span>
            )}
          </div>
          <Badge className="absolute -bottom-1 -right-1 bg-success/10 text-success border border-success/30 px-1 py-0 h-4 flex items-center gap-0.5">
            <ShieldCheck className="h-2.5 w-2.5" />
            <span className="text-[8px]">PRO</span>
          </Badge>
        </div>

        <div className="space-y-0.5">
          <h3 className="font-bold text-sm text-white truncate max-w-[180px]">
            {formState.full_name || "New Coder"}
          </h3>
          <p className="text-[11px] text-muted-foreground">@{user?.username || "developer"}</p>
        </div>

        <div className="flex flex-wrap justify-center gap-1.5 pt-1">
          <Badge className="font-mono text-[9px] bg-primary/10 text-primary border border-primary/20">
            Lvl {level}
          </Badge>
          <Badge className={`font-mono text-[9px] border ${division.color}`}>
            {division.name}
          </Badge>
        </div>
      </div>

      <div className="space-y-2.5 border-t border-zinc-850 pt-3 text-center">
        <p className="text-[11px] text-zinc-400 italic leading-relaxed max-w-[200px] mx-auto min-h-[30px] line-clamp-3">
          "{formState.bio || "No bio description set yet."}"
        </p>

        <div className="flex flex-col gap-1 text-[11px] text-muted-foreground items-center pt-1">
          {formState.location && (
            <span className="flex items-center gap-1">
              <MapPin className="h-3 w-3 shrink-0" />
              <span className="truncate max-w-[160px]">{formState.location}</span>
            </span>
          )}
          {formState.website && (
            <span className="flex items-center gap-1">
              <LinkIcon className="h-3 w-3 shrink-0" />
              <span className="truncate max-w-[160px] text-primary">{formState.website}</span>
            </span>
          )}
          {formState.github_username && (
            <span className="flex items-center gap-1">
              <Github className="h-3 w-3 shrink-0" />
              <span className="truncate max-w-[160px]">github.com/{formState.github_username}</span>
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 border-t border-zinc-850 pt-3 text-center">
        <div className="p-1 rounded bg-zinc-950/40">
          <span className="text-[8px] uppercase font-mono text-zinc-500 block">Rating</span>
          <p className="text-xs font-bold text-white mt-0.5">{rating}</p>
        </div>
        <div className="p-1 rounded bg-zinc-950/40">
          <span className="text-[8px] uppercase font-mono text-zinc-500 block">Rank</span>
          <p className="text-xs font-bold text-white mt-0.5">#{rank}</p>
        </div>
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 2. ACCOUNT SECTION                                                         */
/* ────────────────────────────────────────────────────────────────────────── */
function AccountSection() {
  const { user } = useSelector((state) => state.user);
  const [googleConnected, setGoogleConnected] = useState(user?.auth_provider === "google");
  const [githubConnected, setGithubConnected] = useState(user?.auth_provider === "github");
  const [connectingGoogle, setConnectingGoogle] = useState(false);
  const [connectingGithub, setConnectingGithub] = useState(false);

  const maskedEmail = user?.email
    ? `${user.email.slice(0, 4)}****@${user.email.split("@")[1]}`
    : "Not Set";

  const handleGoogleToggle = () => {
    setConnectingGoogle(true);
    setTimeout(() => {
      setGoogleConnected(!googleConnected);
      setConnectingGoogle(false);
      toast.success(googleConnected ? "Google account disconnected." : "Google account linked successfully!");
    }, 1200);
  };

  const handleGithubToggle = () => {
    setConnectingGithub(true);
    setTimeout(() => {
      setGithubConnected(!githubConnected);
      setConnectingGithub(false);
      toast.success(githubConnected ? "GitHub account disconnected." : "GitHub account linked successfully!");
    }, 1200);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Account Settings</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Review credentials, linked identity providers, and authentication methods.
        </p>
      </div>

      <div className="space-y-6">
        
        {/* Credentials */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white">General Account Details</h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-3.5 rounded-lg bg-zinc-950 border border-zinc-900">
              <span className="text-[10px] font-mono text-muted-foreground uppercase">Username</span>
              <p className="text-sm font-medium text-white mt-0.5">@{user?.username || "Not Set"}</p>
            </div>

            <div className="p-3.5 rounded-lg bg-zinc-950 border border-zinc-900">
              <span className="text-[10px] font-mono text-muted-foreground uppercase">Registration Email</span>
              <p className="text-sm font-medium text-white mt-0.5">{maskedEmail}</p>
            </div>

            <div className="p-3.5 rounded-lg bg-zinc-950 border border-zinc-900">
              <span className="text-[10px] font-mono text-muted-foreground uppercase">Registered On</span>
              <p className="text-sm font-medium text-white mt-0.5">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "Jun 2026"}
              </p>
            </div>

            <div className="p-3.5 rounded-lg bg-zinc-950 border border-zinc-900">
              <span className="text-[10px] font-mono text-muted-foreground uppercase">OAuth Provider</span>
              <p className="text-sm font-medium text-primary mt-0.5 capitalize">{user?.auth_provider || "Credentials"}</p>
            </div>
          </div>
        </section>

        {/* Social Linker */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white font-mono uppercase tracking-wider text-xs">Connected Providers</h3>
          <p className="text-xs text-muted-foreground">Sync your external services to log in with single click authentication.</p>
          
          <div className="space-y-3">
            
            {/* Google */}
            <div className="flex items-center justify-between rounded-lg border border-zinc-900 bg-zinc-950 p-4">
              <div className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-zinc-900 text-xs font-black text-red-500 border border-zinc-800">
                  G
                </span>
                <div>
                  <p className="text-sm font-semibold text-white">Google SSO</p>
                  <p className="text-[10px] text-muted-foreground">
                    {googleConnected ? "Linked with authentication scope" : "Authorize Google login credentials"}
                  </p>
                </div>
              </div>

              <Button
                variant={googleConnected ? "secondary" : "outline"}
                size="sm"
                onClick={handleGoogleToggle}
                disabled={connectingGoogle}
                className="h-8 text-xs min-w-[90px]"
              >
                {connectingGoogle ? (
                  <RefreshCw className="h-3 w-3 animate-spin" />
                ) : googleConnected ? (
                  "Disconnect"
                ) : (
                  "Link Account"
                )}
              </Button>
            </div>

            {/* GitHub */}
            <div className="flex items-center justify-between rounded-lg border border-zinc-900 bg-zinc-950 p-4">
              <div className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-zinc-900 text-xs border border-zinc-800">
                  <Github className="h-4 w-4 text-white" />
                </span>
                <div>
                  <p className="text-sm font-semibold text-white">GitHub OAuth</p>
                  <p className="text-[10px] text-muted-foreground">
                    {githubConnected ? "Synced with profile fetch scope" : "Link your GitHub repository identity"}
                  </p>
                </div>
              </div>

              <Button
                variant={githubConnected ? "secondary" : "outline"}
                size="sm"
                onClick={handleGithubToggle}
                disabled={connectingGithub}
                className="h-8 text-xs min-w-[90px]"
              >
                {connectingGithub ? (
                  <RefreshCw className="h-3 w-3 animate-spin" />
                ) : githubConnected ? (
                  "Disconnect"
                ) : (
                  "Link Account"
                )}
              </Button>
            </div>

          </div>
        </section>

        {/* Danger Zone */}
        <section className="bg-red-500/5 border border-red-500/20 rounded-xl p-5 md:p-6 space-y-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-red-500 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <h4 className="text-sm font-bold text-red-500">Deactivate Account</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Permanently delete all your challenge submissions, points, contest leaderboard placements, and AI interview reports. This process is irreversible.
              </p>
            </div>
          </div>

          <Dialog>
            <DialogTrigger asChild>
              <Button variant="destructive" size="sm" className="bg-red-950/20 text-red-400 border border-red-500/30 hover:bg-red-900/40">
                Permanent Delete
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-zinc-950 border-zinc-800 text-white">
              <DialogHeader>
                <DialogTitle className="text-red-500 flex items-center gap-1.5 text-base">
                  <AlertTriangle className="h-4 w-4" />
                  Are you absolutely sure?
                </DialogTitle>
                <DialogDescription className="text-xs text-zinc-400">
                  This actions cannot be undone. It will purge all your progress from our database.
                </DialogDescription>
              </DialogHeader>
              <div className="py-2">
                <p className="text-xs text-zinc-400 font-mono">To confirm, type your username <strong className="text-white">@{user?.username}</strong> below:</p>
                <input
                  type="text"
                  placeholder={user?.username}
                  className="w-full mt-2 h-9 rounded bg-zinc-900 border border-zinc-850 px-3 text-xs focus:outline-none focus:border-red-500"
                />
              </div>
              <DialogFooter className="gap-2 sm:gap-0">
                <Button variant="ghost" size="sm" className="text-zinc-400">Cancel</Button>
                <Button variant="destructive" size="sm" onClick={() => toast.error("Account deactivation restricted in demo workspace.")}>
                  Confirm Purge
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </section>

      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 3. SECURITY & PASSKEYS SECTION                                             */
/* ────────────────────────────────────────────────────────────────────────── */
function SecuritySection() {
  const [sessions, setSessions] = useState([
    { id: 1, device: "Chrome on macOS", location: "Mumbai, India", ip: "103.241.12.89", current: true, date: "Active now" },
    { id: 2, device: "Safari on iPhone 15", location: "Pune, India", ip: "223.189.14.22", current: false, date: "2 hours ago" },
    { id: 3, device: "VS Code Client", location: "Mumbai, India", ip: "103.241.12.90", current: false, date: "1 day ago" }
  ]);

  const [passkeys, setPasskeys] = useState([
    { id: 1, name: "MacBook Touch ID", created: "Jun 10, 2026", lastUsed: "Jun 21, 2026" },
    { id: 2, name: "iPhone Face ID", created: "Jun 12, 2026", lastUsed: "Jun 20, 2026" }
  ]);

  const [registeringPasskey, setRegisteringPasskey] = useState(false);
  const [passkeyModalOpen, setPasskeyModalOpen] = useState(false);
  const [newPasskeyName, setNewPasskeyName] = useState("");

  const handleRevokeSession = (id) => {
    setSessions(prev => prev.filter(s => s.id !== id));
    toast.success("Session revoked successfully.");
  };

  const handleRemovePasskey = (id) => {
    setPasskeys(prev => prev.filter(p => p.id !== id));
    toast.success("Passkey removed.");
  };

  const handleAddPasskey = (e) => {
    e.preventDefault();
    if (!newPasskeyName.trim()) return;
    setRegisteringPasskey(true);
    
    // Simulate biometric credential registration flow
    setTimeout(() => {
      setPasskeys(prev => [
        ...prev,
        {
          id: Date.now(),
          name: newPasskeyName,
          created: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }),
          lastUsed: "Never"
        }
      ]);
      setRegisteringPasskey(false);
      setPasskeyModalOpen(false);
      setNewPasskeyName("");
      toast.success("Biometric WebAuthn Passkey configured successfully!");
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Security & Passkeys</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Configure multi-factor credentials, biometric passkeys, and monitor active sessions.
        </p>
      </div>

      <div className="space-y-6">
        
        {/* Passkeys Area */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <h3 className="text-sm font-semibold text-white">WebAuthn Passkeys</h3>
              <p className="text-xs text-muted-foreground">Sign in securely using Apple Touch ID, Windows Hello, or Android Biometrics.</p>
            </div>
            
            <Dialog open={passkeyModalOpen} onOpenChange={setPasskeyModalOpen}>
              <DialogTrigger asChild>
                <Button size="sm" className="h-8 gap-1">
                  <Plus className="h-3.5 w-3.5" />
                  <span>Register Passkey</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-zinc-950 border-zinc-800 text-white">
                <form onSubmit={handleAddPasskey} className="space-y-4">
                  <DialogHeader>
                    <DialogTitle className="text-white text-base">Configure Hardware Passkey</DialogTitle>
                    <DialogDescription className="text-xs text-zinc-400">
                      Link a secure credential authenticator on your local device.
                    </DialogDescription>
                  </DialogHeader>
                  
                  {registeringPasskey ? (
                    <div className="py-6 flex flex-col items-center justify-center text-center gap-3">
                      <RefreshCw className="h-8 w-8 text-primary animate-spin" />
                      <p className="text-xs font-semibold text-white">Triggering device prompt...</p>
                      <p className="text-[10px] text-zinc-400 max-w-[280px]">Scan your fingerprint, face, or enter device PIN on the system authenticator window.</p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <label className="text-xs font-semibold text-zinc-300 block">Authenticator Label</label>
                      <input
                        type="text"
                        value={newPasskeyName}
                        onChange={(e) => setNewPasskeyName(e.target.value)}
                        placeholder="e.g. My MacBook Touch ID"
                        className="w-full h-10 rounded-md border border-zinc-800 bg-zinc-950 px-3 text-sm focus:outline-none focus:border-primary"
                        required
                        autoFocus
                      />
                    </div>
                  )}

                  {!registeringPasskey && (
                    <DialogFooter>
                      <Button type="button" variant="ghost" size="sm" onClick={() => setPasskeyModalOpen(false)}>Cancel</Button>
                      <Button type="submit" size="sm">Initiate Registration</Button>
                    </DialogFooter>
                  )}
                </form>
              </DialogContent>
            </Dialog>
          </div>

          <div className="divide-y divide-zinc-900 border border-zinc-900 rounded-lg overflow-hidden bg-zinc-950/20">
            {passkeys.length === 0 ? (
              <div className="p-6 text-center text-xs text-muted-foreground">No passkeys linked. Lock down your account using biometric keys.</div>
            ) : (
              passkeys.map(pk => (
                <div key={pk.id} className="flex items-center justify-between p-4">
                  <div className="flex items-center gap-3">
                    <span className="p-2 rounded bg-zinc-900 border border-zinc-850">
                      <KeyRound className="h-4 w-4 text-primary" />
                    </span>
                    <div>
                      <h4 className="text-sm font-semibold text-white">{pk.name}</h4>
                      <p className="text-[10px] text-muted-foreground">Added {pk.created} · Last active {pk.lastUsed}</p>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon" onClick={() => handleRemovePasskey(pk.id)} className="h-8 w-8 text-zinc-500 hover:text-red-400">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))
            )}
          </div>
        </section>

        {/* Password Reset */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white">Reset Account Password</h3>
          <div className="space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-zinc-400 uppercase">Current Password</label>
                <input type="password" placeholder="••••••••" className="w-full h-9 rounded bg-zinc-950 border border-zinc-900 px-3 text-xs focus:outline-none focus:border-primary" />
              </div>
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-zinc-400 uppercase">New Password</label>
                <input type="password" placeholder="••••••••" className="w-full h-9 rounded bg-zinc-950 border border-zinc-900 px-3 text-xs focus:outline-none focus:border-primary" />
              </div>
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-zinc-400 uppercase">Confirm Password</label>
                <input type="password" placeholder="••••••••" className="w-full h-9 rounded bg-zinc-950 border border-zinc-900 px-3 text-xs focus:outline-none focus:border-primary" />
              </div>
            </div>
            <Button size="sm" variant="secondary" onClick={() => toast.success("Password reset request successfully updated (Simulation).")} className="h-8">Change Password</Button>
          </div>
        </section>

        {/* Sessions Area */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white">Active Login Sessions</h3>
          <p className="text-xs text-muted-foreground">List of clients currently holding session tokens. Revoking will terminate the access immediately.</p>
          
          <div className="divide-y divide-zinc-900 border border-zinc-900 rounded-lg overflow-hidden bg-zinc-950/20">
            {sessions.map(s => (
              <div key={s.id} className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <span className="p-2 rounded bg-zinc-900 border border-zinc-850">
                    {s.device.toLowerCase().includes("phone") ? (
                      <Smartphone className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <Laptop className="h-4 w-4 text-muted-foreground" />
                    )}
                  </span>
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-semibold text-white">{s.device}</h4>
                      {s.current && <Badge className="bg-success/10 text-success border border-success/20 text-[8px] h-3.5">Current Session</Badge>}
                    </div>
                    <p className="text-[10px] text-muted-foreground">{s.location} · IP: {s.ip} · {s.date}</p>
                  </div>
                </div>

                {!s.current && (
                  <Button variant="ghost" size="sm" onClick={() => handleRevokeSession(s.id)} className="h-7 text-xs text-zinc-500 hover:text-red-400 px-2">
                    Revoke
                  </Button>
                )}
              </div>
            ))}
          </div>
        </section>

      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 4. PRIVACY SECTION                                                         */
/* ────────────────────────────────────────────────────────────────────────── */
function PrivacySection() {
  const [prefs, setPrefs] = useState({
    publicProfile: true,
    showLeaderboard: true,
    onlineStatus: false,
    directMessages: true
  });

  const handleToggle = (key) => {
    setPrefs(prev => {
      const next = { ...prev, [key]: !prev[key] };
      toast.success("Privacy preferences updated successfully.");
      return next;
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Privacy Settings</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Manage visual visibility settings, data sharing, and user interactions.
        </p>
      </div>

      <TooltipProvider>
        <div className="bg-card border border-border rounded-xl divide-y divide-border overflow-hidden shadow-sm">
          
          <div className="flex items-center justify-between p-5 md:p-6">
            <div className="space-y-0.5 max-w-[400px]">
              <div className="flex items-center gap-1">
                <span className="text-sm font-semibold text-zinc-200">Public Profile visibility</span>
                <Tooltip>
                  <TooltipTrigger>
                    <HelpCircle className="h-3 w-3 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent className="bg-zinc-900 border-zinc-800 text-[10px] text-zinc-300">
                    If disabled, users can't visit your custom profile URL page.
                  </TooltipContent>
                </Tooltip>
              </div>
              <p className="text-[11px] text-muted-foreground">Expose your ratings, certifications, and solved counts to search bots and anonymous visits.</p>
            </div>
            <Switch checked={prefs.publicProfile} onCheckedChange={() => handleToggle("publicProfile")} />
          </div>

          <div className="flex items-center justify-between p-5 md:p-6">
            <div className="space-y-0.5 max-w-[400px]">
              <div className="flex items-center gap-1">
                <span className="text-sm font-semibold text-zinc-200">Appear on Leaderboards</span>
                <Tooltip>
                  <TooltipTrigger>
                    <HelpCircle className="h-3 w-3 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent className="bg-zinc-900 border-zinc-800 text-[10px] text-zinc-300">
                    Removes your global rank and stats lists completely.
                  </TooltipContent>
                </Tooltip>
              </div>
              <p className="text-[11px] text-muted-foreground">Show your name and overall XP score on the global leaderboard rank tracking pages.</p>
            </div>
            <Switch checked={prefs.showLeaderboard} onCheckedChange={() => handleToggle("showLeaderboard")} />
          </div>

          <div className="flex items-center justify-between p-5 md:p-6">
            <div className="space-y-0.5 max-w-[400px]">
              <div className="flex items-center gap-1">
                <span className="text-sm font-semibold text-zinc-200">Display Online status</span>
                <Tooltip>
                  <TooltipTrigger>
                    <HelpCircle className="h-3 w-3 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent className="bg-zinc-900 border-zinc-800 text-[10px] text-zinc-300">
                    Shows a green dot beside your username when active.
                  </TooltipContent>
                </Tooltip>
              </div>
              <p className="text-[11px] text-muted-foreground">Allows opponent match workers to see if you are actively inside the arena lobby.</p>
            </div>
            <Switch checked={prefs.onlineStatus} onCheckedChange={() => handleToggle("onlineStatus")} />
          </div>

          <div className="flex items-center justify-between p-5 md:p-6">
            <div className="space-y-0.5 max-w-[400px]">
              <div className="flex items-center gap-1">
                <span className="text-sm font-semibold text-zinc-200">Allow Direct Battle invites</span>
                <Tooltip>
                  <TooltipTrigger>
                    <HelpCircle className="h-3 w-3 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent className="bg-zinc-900 border-zinc-800 text-[10px] text-zinc-300">
                    Toggles 1v1 battle challenge request blocks.
                  </TooltipContent>
                </Tooltip>
              </div>
              <p className="text-[11px] text-muted-foreground">Allow peers to send battle notifications requesting to start a custom coding match.</p>
            </div>
            <Switch checked={prefs.directMessages} onCheckedChange={() => handleToggle("directMessages")} />
          </div>

        </div>
      </TooltipProvider>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 5. BILLING & SUBSCRIPTION SECTION                                          */
/* ────────────────────────────────────────────────────────────────────────── */
function BillingSection() {
  const [billingCycle, setBillingCycle] = useState("monthly"); // monthly or annual

  const invoices = [
    { id: "INV-2026-003", date: "Jun 15, 2026", amount: "$19.00", status: "Paid" },
    { id: "INV-2026-002", date: "May 15, 2026", amount: "$19.00", status: "Paid" },
    { id: "INV-2026-001", date: "Apr 15, 2026", amount: "$19.00", status: "Paid" }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Billing & Plans</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Review premium plans, update billing details, and view payment invoices.
        </p>
      </div>

      <div className="space-y-6">
        
        {/* Toggle billing cycle */}
        <div className="flex justify-center">
          <div className="inline-flex rounded-lg bg-zinc-950 p-1 border border-zinc-900">
            <button
              onClick={() => setBillingCycle("monthly")}
              className={`rounded-md px-4 py-1.5 text-xs font-semibold transition-all ${
                billingCycle === "monthly" ? "bg-primary text-white" : "text-muted-foreground"
              }`}
            >
              Monthly billing
            </button>
            <button
              onClick={() => setBillingCycle("annual")}
              className={`rounded-md px-4 py-1.5 text-xs font-semibold transition-all ${
                billingCycle === "annual" ? "bg-primary text-white" : "text-muted-foreground"
              }`}
            >
              Annual billing (Save 20%)
            </button>
          </div>
        </div>

        {/* Subscription cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          {/* Free Tier */}
          <Card className="border-zinc-850 bg-card p-5 space-y-4">
            <div className="space-y-1">
              <span className="text-[9px] uppercase font-mono tracking-wider bg-zinc-900 px-2 py-0.5 rounded border border-zinc-800 text-zinc-400">Free Tier</span>
              <h3 className="text-lg font-bold text-white mt-1.5">Free Developer</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">Core features to test your algorithms and solve base sandboxes.</p>
            </div>
            
            <div className="text-2xl font-black text-white">$0</div>

            <ul className="space-y-2 text-xs text-zinc-300">
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-success shrink-0" />
                <span>Solve 3 free challenges/day</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-success shrink-0" />
                <span>1 execution sandbox access</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-success shrink-0" />
                <span>Base leaderboard listing</span>
              </li>
            </ul>

            <Button variant="outline" className="w-full text-xs font-semibold border-zinc-850" disabled>
              Current Active Plan
            </Button>
          </Card>

          {/* Pro Coder */}
          <Card className="border-primary bg-zinc-900/10 p-5 space-y-4 relative overflow-hidden shadow-lg shadow-primary/5">
            <div className="absolute right-0 top-0 h-16 w-16 bg-primary/10 rounded-bl-full flex items-center justify-end pr-2.5 pb-2">
              <Star className="h-4 w-4 text-primary" />
            </div>

            <div className="space-y-1">
              <span className="text-[9px] uppercase font-mono tracking-wider bg-primary/20 px-2 py-0.5 rounded border border-primary/30 text-primary">Recommended</span>
              <h3 className="text-lg font-bold text-white mt-1.5">Pro Coder Premium</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">Full access package built for senior developers preparing for career milestones.</p>
            </div>

            <div className="flex items-baseline gap-1">
              <span className="text-2xl font-black text-white">
                {billingCycle === "monthly" ? "$19" : "$15"}
              </span>
              <span className="text-xs text-muted-foreground">/ month</span>
            </div>

            <ul className="space-y-2 text-xs text-zinc-300">
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-primary shrink-0" />
                <span>Unlimited Premium Challenges</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-primary shrink-0" />
                <span>Unlimited AI Interview Coach Reports</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-primary shrink-0" />
                <span>Access all 7 docker compiler sandboxes</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-primary shrink-0" />
                <span>Profile verified badge & custom styling</span>
              </li>
            </ul>

            <Button className="w-full text-xs font-semibold bg-primary hover:bg-primary/90 text-white" onClick={() => toast.info("Stripe payment portal checkout simulated.")}>
              Upgrade to Pro
            </Button>
          </Card>

        </div>

        {/* Invoice List */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white">Invoice History</h3>
          
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left text-xs">
              <thead>
                <tr className="border-b border-zinc-900 text-zinc-500 uppercase font-mono tracking-wider pb-2">
                  <th className="py-2.5 font-medium">Invoice ID</th>
                  <th className="py-2.5 font-medium">Date</th>
                  <th className="py-2.5 font-medium">Amount</th>
                  <th className="py-2.5 font-medium">Status</th>
                  <th className="py-2.5 font-medium text-right">Receipt</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900 text-zinc-300">
                {invoices.map(inv => (
                  <tr key={inv.id} className="hover:bg-zinc-850/10">
                    <td className="py-3 font-semibold text-white">{inv.id}</td>
                    <td className="py-3">{inv.date}</td>
                    <td className="py-3 font-mono">{inv.amount}</td>
                    <td className="py-3">
                      <Badge className="bg-success/15 text-success border border-success/20 text-[9px] px-1.5 py-0 h-4">
                        {inv.status}
                      </Badge>
                    </td>
                    <td className="py-3 text-right">
                      <Button variant="ghost" size="icon" className="h-7 w-7 text-zinc-500 hover:text-white" onClick={() => toast.success("PDF invoice download started.")}>
                        <FileDown className="h-3.5 w-3.5" />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 6. POINTS & LEVEL SECTION                                                  */
/* ────────────────────────────────────────────────────────────────────────── */
function PointsSection() {
  const { user } = useSelector((state) => state.user);
  
  const xp = user?.xp || 0;
  const level = Math.floor(xp / 1000) + 1;
  const nextLevelXp = level * 1000;
  const currentLevelXp = (level - 1) * 1000;
  const xpProgress = xp - currentLevelXp;
  const progressPercent = (xpProgress / 1000) * 100;

  const pointsHistory = [
    { id: 1, action: "Solved 'Responsive Data Table' (Medium)", change: "+40 XP", date: "Today, 14:32" },
    { id: 2, action: "Completed System Design Mock Interview", change: "+120 XP", date: "Yesterday, 19:15" },
    { id: 3, action: "Solved 'Token Bucket Rate Limiter' (Hard)", change: "+60 XP", date: "Jun 19, 2026" },
    { id: 4, action: "5-Day Coding Streak Bonus", change: "+50 XP", date: "Jun 18, 2026" },
    { id: 5, action: "First Milestone Achievement", change: "+100 XP", date: "Jun 08, 2026" }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Points & Achievements</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Monitor your developer rank levels, active coding scores, and score histories.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        {/* XP Progress Card */}
        <Card className="border-border bg-card p-5 md:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-[10px] uppercase font-mono text-zinc-500">Arena Ranking Level</span>
              <h3 className="text-xl font-bold text-white mt-0.5">Level {level}</h3>
            </div>
            <Badge className="bg-primary/20 text-primary border border-primary/30 text-xs font-mono px-2 py-0.5">
              Rank Tier Pro
            </Badge>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-muted-foreground">{xpProgress} / 1000 XP in Level</span>
              <span className="text-primary font-bold">{progressPercent.toFixed(0)}%</span>
            </div>
            <Progress value={progressPercent} className="h-2.5 bg-zinc-950" />
            <p className="text-[10px] text-muted-foreground leading-normal">
              You need {1000 - xpProgress} more XP to reach Level {level + 1}. You earn XP rewards by solving coding targets and completing mock recruiter evaluations.
            </p>
          </div>
        </Card>

        {/* Quick Stats */}
        <Card className="border-border bg-card p-5 flex flex-col justify-between">
          <div className="space-y-1">
            <span className="text-[10px] uppercase font-mono text-zinc-500">Total Accumulation</span>
            <p className="text-2xl font-black text-white">{xp} XP</p>
          </div>
          <div className="border-t border-zinc-900 pt-3 mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <span>Next Level</span>
            <span className="font-mono text-white font-bold">{nextLevelXp} XP</span>
          </div>
        </Card>

      </div>

      {/* Point History */}
      <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
        <h3 className="text-sm font-semibold text-white">Points History Log</h3>
        
        <div className="divide-y divide-zinc-900 border border-zinc-900 rounded-lg overflow-hidden bg-zinc-950/20">
          {pointsHistory.map(ph => (
            <div key={ph.id} className="flex items-center justify-between p-3.5 text-xs">
              <div className="space-y-0.5">
                <p className="font-semibold text-zinc-200">{ph.action}</p>
                <p className="text-[10px] text-muted-foreground">{ph.date}</p>
              </div>
              <span className="font-mono font-bold text-success text-sm shrink-0">{ph.change}</span>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 7. ORDERS SECTION                                                          */
/* ────────────────────────────────────────────────────────────────────────── */
function OrdersSection() {
  const orders = [
    { id: "ORD-98421", date: "Jun 15, 2026", item: "Pro Coder Monthly Subscription", amount: "$19.00", status: "Completed" },
    { id: "ORD-98105", date: "Jun 08, 2026", item: "DevOps & System Design Badge Pack", amount: "$4.99", status: "Completed" },
    { id: "ORD-97500", date: "May 25, 2026", item: "Cyberpunk IDE Theme Customization", amount: "$2.99", status: "Completed" }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Orders History</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Review details of past transaction purchases and digital asset receipts.
        </p>
      </div>

      <div className="bg-card border border-border rounded-xl p-5 md:p-6 shadow-sm space-y-4">
        <h3 className="text-sm font-semibold text-white">Transactions Log</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-xs">
            <thead>
              <tr className="border-b border-zinc-900 text-zinc-500 uppercase font-mono tracking-wider pb-2">
                <th className="py-2.5 font-medium">Order ID</th>
                <th className="py-2.5 font-medium">Date</th>
                <th className="py-2.5 font-medium">Product Item</th>
                <th className="py-2.5 font-medium">Charged</th>
                <th className="py-2.5 font-medium text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-900 text-zinc-300">
              {orders.map(ord => (
                <tr key={ord.id} className="hover:bg-zinc-850/10">
                  <td className="py-3 font-semibold text-white font-mono">{ord.id}</td>
                  <td className="py-3">{ord.date}</td>
                  <td className="py-3">{ord.item}</td>
                  <td className="py-3 font-mono">{ord.amount}</td>
                  <td className="py-3 text-right">
                    <Badge className="bg-success/15 text-success border border-success/20 text-[9px] px-1.5 py-0 h-4">
                      {ord.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/* 8. NOTIFICATION PREFERENCES SECTION                                        */
/* ────────────────────────────────────────────────────────────────────────── */
function NotificationsSection() {
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState("all");

  const [notificationPrefs, setNotificationPrefs] = useState({
    invitations: true,
    startAlerts: true,
    reportAlerts: true,
    digests: false
  });

  const fetchNotifications = async () => {
    try {
      const res = await API.get("/api/notifications");
      if (res.data && res.data.success) {
        setNotifications(res.data.data);
      }
    } catch (err) {
      console.error(err);
      toast.error("Failed to load notifications history.");
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    fetchNotifications();
  }, []);

  const handleTogglePref = (key) => {
    setNotificationPrefs(prev => {
      const next = { ...prev, [key]: !prev[key] };
      toast.success("Notification preferences updated.");
      return next;
    });
  };

  const handleNotificationClick = async (notif) => {
    try {
      await API.post(`/api/notifications/${notif.id}/read`);
      fetchNotifications();
      if (notif.link) {
        navigate(notif.link);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await API.post("/api/notifications/read-all");
      fetchNotifications();
      toast.success("All notifications marked as read");
    } catch (err) {
      console.error(err);
    }
  };

  const filteredNotifications = useMemo(() => {
    if (activeFilter === "unread") {
      return notifications.filter(n => !n.read);
    }
    return notifications;
  }, [notifications, activeFilter]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Notifications Settings</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Configure battle prompts and review your live platform notifications history.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-6 items-start">
        
        {/* Preference Settings */}
        <section className="bg-card border border-border rounded-xl p-5 md:p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white">Alert Preferences</h3>
          <p className="text-xs text-muted-foreground">Select what prompts trigger local and email integrations.</p>

          <div className="border border-zinc-900 rounded-lg overflow-hidden divide-y divide-zinc-900 bg-zinc-950/20">
            <div className="flex items-center justify-between p-4">
              <div className="space-y-0.5 max-w-[340px]">
                <span className="text-xs font-semibold text-zinc-200 block">Contest Invitations</span>
                <p className="text-[10px] text-muted-foreground">Receive instant alerts when another developer challenges you to a 1v1 battle.</p>
              </div>
              <Switch checked={notificationPrefs.invitations} onCheckedChange={() => handleTogglePref("invitations")} />
            </div>

            <div className="flex items-center justify-between p-4">
              <div className="space-y-0.5 max-w-[340px]">
                <span className="text-xs font-semibold text-zinc-200 block">Match Readiness Updates</span>
                <p className="text-[10px] text-muted-foreground">Get notified when a battle room finishes matchmaking and is ready to load.</p>
              </div>
              <Switch checked={notificationPrefs.startAlerts} onCheckedChange={() => handleTogglePref("startAlerts")} />
            </div>

            <div className="flex items-center justify-between p-4">
              <div className="space-y-0.5 max-w-[340px]">
                <span className="text-xs font-semibold text-zinc-200 block">AI Evaluation Ready</span>
                <p className="text-[10px] text-muted-foreground">Get notified immediately when the AI career advisor finishes compiling interview report logs.</p>
              </div>
              <Switch checked={notificationPrefs.reportAlerts} onCheckedChange={() => handleTogglePref("reportAlerts")} />
            </div>

            <div className="flex items-center justify-between p-4">
              <div className="space-y-0.5 max-w-[340px]">
                <span className="text-xs font-semibold text-zinc-200 block">Weekly challenge digest</span>
                <p className="text-[10px] text-muted-foreground">Receive a weekly catalog summarizing new problem sets, tags, and contest agendas.</p>
              </div>
              <Switch checked={notificationPrefs.digests} onCheckedChange={() => handleTogglePref("digests")} />
            </div>
          </div>
        </section>

        {/* Notifications Log / Inbox */}
        <section className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-900 pb-3">
            <div className="space-y-0.5">
              <h3 className="text-sm font-semibold text-white">Notifications Inbox</h3>
            </div>
            
            {notifications.some(n => !n.read) && (
              <button onClick={handleMarkAllRead} className="text-xs text-primary hover:underline font-medium">
                Mark all read
              </button>
            )}
          </div>

          {/* Filters */}
          <div className="flex items-center gap-1.5 pb-1">
            <button
              onClick={() => setActiveFilter("all")}
              className={`rounded px-2.5 py-1 text-[11px] font-semibold border transition-all ${
                activeFilter === "all"
                  ? "bg-zinc-800 border-zinc-700 text-white"
                  : "border-transparent text-muted-foreground hover:text-white"
              }`}
            >
              All logs
            </button>
            <button
              onClick={() => setActiveFilter("unread")}
              className={`rounded px-2.5 py-1 text-[11px] font-semibold border transition-all ${
                activeFilter === "unread"
                  ? "bg-zinc-800 border-zinc-700 text-white"
                  : "border-transparent text-muted-foreground hover:text-white"
              }`}
            >
              Unread
            </button>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-4 w-4 text-primary animate-spin" />
            </div>
          ) : filteredNotifications.length === 0 ? (
            <div className="text-center py-12 border border-dashed border-zinc-850 rounded-xl bg-zinc-950/20">
              <Bell className="h-6 w-6 text-zinc-700 mx-auto mb-2" />
              <p className="text-[11px] text-zinc-500">Inbox empty.</p>
            </div>
          ) : (
            <div className="space-y-2 max-h-[360px] overflow-y-auto pr-1">
              {filteredNotifications.map((n) => (
                <div
                  key={n.id}
                  onClick={() => handleNotificationClick(n)}
                  className={`p-3 rounded-lg border flex items-start justify-between gap-3 cursor-pointer transition-all ${
                    n.read
                      ? "bg-zinc-950/20 border-zinc-900 hover:bg-zinc-950/40"
                      : "bg-primary/5 border-primary/20 hover:bg-primary/10"
                  }`}
                >
                  <div className="space-y-0.5 flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className={`text-xs font-semibold truncate ${n.read ? "text-zinc-300" : "text-white"}`}>
                        {n.title}
                      </span>
                      {!n.read && <span className="h-1.5 w-1.5 rounded-full bg-primary shrink-0" />}
                    </div>
                    <p className="text-[10px] text-zinc-400 leading-normal line-clamp-2">
                      {n.message}
                    </p>
                    <span className="text-[8px] text-zinc-500 block pt-0.5">
                      {new Date(n.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}

export default Settings;

