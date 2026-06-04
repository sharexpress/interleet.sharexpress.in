import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { User, Mail, Phone, KeyRound, ChevronRight, ExternalLink, Github } from "lucide-react";
import { useState } from "react";
import { useSelector } from "react-redux";

const nav = [
  { key: "account", label: "Account" },
  { key: "privacy", label: "Privacy" },
  { key: "billing", label: "Billing" },
  { key: "points", label: "Points" },
  { key: "orders", label: "Orders" },
  { key: "notifications", label: "Notifications" },
];

function Settings() {
  const [active, setActive] = useState("account");

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
            <a
              href="#"
              className="mt-1 flex items-center gap-1.5 rounded-md px-3 py-2 text-sm text-muted-foreground hover:text-foreground"
            >
              Profile Settings <ExternalLink className="h-3 w-3" />
            </a>
          </nav>
        </aside>

        {/* Content */}
        <div className="px-4 py-8 md:px-12 md:py-10">
          {active === "account" && <AccountSection />}
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

function NotificationsSection() {
  return (
    <div className="mx-auto max-w-3xl">
      <h2 className="text-base font-semibold">Notifications</h2>
      <div className="mt-4 overflow-hidden rounded-lg border border-border bg-card">
        {[
          "Weekly digest of new challenges",
          "Interview report ready",
          "Rank changes (top 1000 only)",
          "Recruiter messages",
        ].map((n, i) => (
          <div
            key={n}
            className="flex items-center justify-between border-b border-border px-5 py-4 last:border-b-0"
          >
            <span className="text-sm">{n}</span>
            <Switch defaultChecked={i % 2 === 0} />
          </div>
        ))}
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
export default Settings;
