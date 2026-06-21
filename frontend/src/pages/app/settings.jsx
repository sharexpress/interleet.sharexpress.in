import { AppShell } from "@/components/layout/AppShell";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import {
  User, Mail, Phone, KeyRound, ChevronRight, ExternalLink, Github
} from "lucide-react";
import React, { useState, useCallback } from "react";
import { useSelector, useDispatch } from "react-redux";
import { toast } from "sonner";
import { GetCurrentUser } from "@/redux/slices/userSlice";
import { API } from "@/api/api";

const nav = [
  { key: "profile", label: "Profile" },
  { key: "account", label: "Account" },
  { key: "security", label: "Security" },
  { key: "privacy", label: "Privacy" },
  { key: "billing", label: "Billing" },
  { key: "points", label: "Points" },
  { key: "orders", label: "Orders" },
  { key: "notifications", label: "Notifications" },
];

function Settings() {
  const location = useLocation();
  const query = React.useMemo(() => new URLSearchParams(location.search), [location.search]);
  const tabParam = query.get("tab");
  const [active, setActive] = useState(tabParam && nav.some(n => n.key === tabParam) ? tabParam : "account");

  React.useEffect(() => {
    if (tabParam && nav.some(n => n.key === tabParam)) {
      setActive(tabParam);
    }
  }, [tabParam]);

  return (
    <AppShell>
      <div className="grid min-h-[calc(100vh-56px)] grid-cols-1 md:grid-cols-[260px_1fr]">
        {/* Left nav */}
        <aside className="border-b border-border bg-card/40 px-4 py-6 md:border-b-0 md:border-r md:px-6 md:py-10">
          <h1 className="mb-6 text-2xl font-semibold">Settings</h1>
          <nav className="space-y-1">
            {nav.map((n) => (
              <button
                key={n.key}
                onClick={() => setActive(n.key)}
                className={`w-full rounded-md px-3 py-2 text-left text-sm transition-colors ${
                  active === n.key
                    ? "bg-secondary text-foreground"
                    : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground"
                }`}
              >
                {n.label}
              </button>
            ))}
            <button
              onClick={() => setActive("profile")}
              className={`mt-1 flex w-full items-center gap-1.5 rounded-md px-3 py-2 text-sm transition-colors ${
                active === "profile"
                  ? "text-foreground bg-secondary/50 font-semibold"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Profile Settings <ExternalLink className="h-3 w-3" />
            </button>
          </nav>
        </aside>

        {/* Content */}
        <div className="px-4 py-8 md:px-12 md:py-10">
          {active === "profile" && <ProfileSection />}
          {active === "account" && <AccountSection />}
          {active === "security" && <SecuritySection />}
          {active === "privacy" && <Placeholder title="Privacy" />}
          {active === "billing" && <Placeholder title="Billing" />}
          {active === "points" && <Placeholder title="Points" />}
          {active === "orders" && <Placeholder title="Orders" />}
          {active === "notifications" && <NotificationsSection />}
        </div>
      </div>
    </AppShell>
  );
}

function Row({ icon: Icon, label, value }) {
  return (
    <button className="flex w-full items-center justify-between border-b border-border px-5 py-4 text-left last:border-b-0 hover:bg-secondary/30">
      <div className="flex items-center gap-3">
        <Icon className="h-4 w-4 text-muted-foreground" />
        <span className="text-sm font-semibold">{label}</span>
        {value && <span className="text-sm text-muted-foreground">{value}</span>}
      </div>
      <ChevronRight className="h-4 w-4 text-muted-foreground" />
    </button>
  );
}

function AccountSection() {
  const { user } = useSelector((state) => state.user);

  const maskedEmail = user?.email
    ? `${user.email.slice(0, 4)}****@${user.email.split("@")[1]}`
    : "Not Set";

  const provider = user?.auth_provider?.toLowerCase();

  return (
    <div className="mx-auto max-w-3xl space-y-10">
      {/* GENERAL */}

      <section>
        <h2 className="text-base font-semibold">General</h2>

        <p className="mt-1 text-xs text-muted-foreground">
          Manage your account credentials, connected providers, and authentication preferences.{" "}
        </p>

        <div className="mt-4 overflow-hidden rounded-lg border border-border bg-card">
          <Row icon={User} label="Interleet ID" value={user?.username || "Not Set"} />

          <Row icon={Mail} label="Email" value={maskedEmail} />

          <Row icon={Phone} label="Phone Number" value="Not Set" />

          <Row
            icon={KeyRound}
            label="Password"
            value={provider === "otp" ? "Configured" : "Managed by provider"}
          />
        </div>
      </section>

      {/* SOCIAL */}

      <section>
        <h2 className="text-base font-semibold">Social Accounts</h2>

        <p className="mt-1 text-xs text-muted-foreground">
          Connect a social account to sign in to Interleet.
        </p>

        <div className="mt-4 space-y-3">
          {/* GOOGLE */}

          <div className="flex items-center justify-between rounded-lg border border-border bg-card px-5 py-4">
            <div className="flex items-center gap-3">
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-muted text-[10px] font-bold">
                G
              </span>

              <div>
                <p className="text-sm font-semibold">Google</p>

                {provider === "google" && (
                  <p className="text-xs text-muted-foreground">Connected as {user?.email}</p>
                )}
              </div>
            </div>

            {provider === "google" ? (
              <Button variant="secondary" size="sm">
                Connected
              </Button>
            ) : (
              <Button size="sm" className="bg-white text-black hover:bg-white/90">
                Connect
              </Button>
            )}
          </div>

          {/* GITHUB */}

          <div className="flex items-center justify-between rounded-lg border border-border bg-card px-5 py-4">
            <div className="flex items-center gap-3">
              <Github className="h-5 w-5" />

              <div>
                <p className="text-sm font-semibold">Github</p>

                {provider === "github" && (
                  <p className="text-xs text-muted-foreground">Connected account</p>
                )}
              </div>
            </div>

            {provider === "github" ? (
              <Button variant="secondary" size="sm">
                Connected
              </Button>
            ) : (
              <Button size="sm" className="bg-white text-black hover:bg-white/90">
                Connect
              </Button>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

/* ─── Security Section ───────────────────────────────────────────────────── */

function SecuritySection() {
  return (
    <div className="mx-auto max-w-3xl space-y-10">
      {/* ── Sessions (placeholder) ───────────────────────────── */}
      <section>
        <h2 className="text-base font-semibold">Sessions</h2>
        <p className="mt-1 text-xs text-muted-foreground">
          Manage active sign-in sessions and trusted devices.
        </p>
        <div className="mt-4 rounded-lg border border-border bg-card p-10 text-center text-sm text-muted-foreground">
          Nothing here yet.
        </div>
      </section>
    </div>
  );
}

function NotificationsSection() {
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      
      {/* Push Settings */}
      <div>
        <h2 className="text-base font-semibold text-white">Notification Preferences</h2>
        <p className="text-xs text-muted-foreground mt-0.5">
          Configure when and how you receive alerts across the Interleet platform.
        </p>

        <div className="mt-4 overflow-hidden rounded-lg border border-border bg-card">
          {[
            { title: "Contest Invitations", desc: "Get notified when a peer invites you to a coding battle." },
            { title: "Contest Start Alerts", desc: "Receive updates when matches you joined are ready to start." },
            { title: "Interview Report Ready", desc: "Get notified when AI completes reviewing your submission." },
            { title: "Weekly digest of new challenges", desc: "A periodic summary of new problems and algorithms." },
          ].map((n, i) => (
            <div
              key={n.title}
              className="flex items-center justify-between border-b border-border px-5 py-4 last:border-b-0"
            >
              <div className="space-y-0.5">
                <span className="text-sm font-medium text-zinc-200">{n.title}</span>
                <p className="text-[11px] text-zinc-500">{n.desc}</p>
              </div>
              <Switch defaultChecked={i < 3} />
            </div>
          ))}
        </div>
      </div>

      {/* Notifications Inbox / Log */}
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-border pb-2">
          <h3 className="text-sm font-bold text-white">Notifications Inbox</h3>
          {notifications.some(n => !n.read) && (
            <button
              onClick={handleMarkAllRead}
              className="text-xs text-primary hover:underline"
            >
              Mark all as read
            </button>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="h-5 w-5 animate-spin rounded-full border border-zinc-700 border-t-primary" />
          </div>
        ) : notifications.length === 0 ? (
          <div className="text-center py-10 border border-zinc-850 rounded-xl bg-zinc-900/10">
            <p className="text-xs text-zinc-500">Your notifications inbox is clean.</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-[350px] overflow-y-auto pr-1">
            {notifications.map((n) => (
              <div
                key={n.id}
                onClick={() => handleNotificationClick(n)}
                className={`p-3.5 rounded-xl border flex items-start justify-between gap-4 cursor-pointer transition-all ${
                  n.read
                    ? "bg-zinc-900/10 border-zinc-850 hover:bg-zinc-900/20"
                    : "bg-primary/5 border-primary/20 hover:bg-primary/10 shadow-[0_2px_12px_rgba(255,101,0,0.02)]"
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-semibold ${n.read ? "text-zinc-300" : "text-white"}`}>
                      {n.title}
                    </span>
                    {!n.read && (
                      <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                    )}
                  </div>
                  <p className="text-[11px] text-zinc-400 leading-relaxed">
                    {n.message}
                  </p>
                  <span className="text-[9px] text-zinc-500 font-mono block">
                    {new Date(n.created_at).toLocaleString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}

function Placeholder({ title }) {
  return (
    <div className="mx-auto max-w-3xl">
      <h2 className="text-base font-semibold">{title}</h2>
      <div className="mt-4 rounded-lg border border-border bg-card p-10 text-center text-sm text-muted-foreground">
        Nothing here yet.
      </div>
    </div>
  );
}

function ProfileSection() {
  const { user } = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const [location, setLocation] = useState(user?.location || "");
  const [githubUsername, setGithubUsername] = useState(user?.github_username || "");
  const [website, setWebsite] = useState(user?.website || "");
  const [saving, setSaving] = useState(false);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await API.put("/api/profile", {
        location: location.trim(),
        github_username: githubUsername.trim(),
        website: website.trim(),
      });
      if (res.data && res.data.success) {
        toast.success("Profile updated successfully!");
        dispatch(GetCurrentUser());
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to update profile.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-white">Profile Settings</h2>
        <p className="text-xs text-muted-foreground mt-0.5">
          Update your profile details displayed to other users on the leaderboard and contest lobbies.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-4 rounded-xl border border-border bg-card p-6">
        <div className="space-y-2">
          <label className="text-xs font-semibold text-zinc-300 block">Location</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. London, UK or SF"
            className="w-full h-10 rounded-md border border-border bg-secondary/30 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
          />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-zinc-300 block">GitHub Username</label>
          <input
            type="text"
            value={githubUsername}
            onChange={(e) => setGithubUsername(e.target.value)}
            placeholder="e.g. octocat"
            className="w-full h-10 rounded-md border border-border bg-secondary/30 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
          />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-zinc-300 block">Website or Portfolio URL</label>
          <input
            type="text"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            placeholder="e.g. devportfolio.com"
            className="w-full h-10 rounded-md border border-border bg-secondary/30 px-3 text-sm text-foreground focus:border-primary focus:outline-none transition-colors"
          />
        </div>

        <Button type="submit" disabled={saving} className="w-full h-10 text-sm font-medium mt-2">
          {saving ? "Saving changes..." : "Save Profile Details"}
        </Button>
      </form>
    </div>
  );
}

export default Settings;
