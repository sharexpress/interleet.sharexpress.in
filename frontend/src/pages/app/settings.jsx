import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import {
  User, Mail, Phone, KeyRound, ChevronRight, ExternalLink, Github,
  ShieldCheck, ShieldAlert, Camera, Fingerprint, Trash2, ArrowRight, Scan, CheckCircle2
} from "lucide-react";
import React, { useState, useCallback } from "react";
import { useSelector, useDispatch } from "react-redux";
import { toast } from "sonner";
import { FaceScanner } from "@/components/auth/FaceScanner";
import { RegisterFace, GetCurrentUser } from "@/redux/slices/userSlice";
import { API } from "@/api/api";

const nav = [
  { key: "account", label: "Account" },
  { key: "security", label: "Security" },
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

/* ─── Face ID Enrollment Flow Constants ──────────────────────────────────── */

const ENROLL_STEPS = [
  { key: "front", label: "Front Look", instruction: "Look directly at the camera with a neutral face", angle: "front" }
];

/* ─── Security Section ───────────────────────────────────────────────────── */

function SecuritySection() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.user);
  const isRegistered = user?.face_registered === true;

  // Enrollment state
  const [enrolling, setEnrolling] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  // scannerKey is what's passed as key= to FaceScanner — only changes AFTER the 800ms delay
  // so the camera doesn't remount and re-fire before we're ready
  const [scannerKey, setScannerKey] = useState(0);
  const [capturedData, setCapturedData] = useState({});
  const [scanStatus, setScanStatus] = useState("idle");
  const [scanError, setScanError] = useState("");
  const [deleting, setDeleting] = useState(false);
  // Hard lock ref — prevents double-fire even within the same render cycle
  const processingRef = React.useRef(false);

  const activeStep = ENROLL_STEPS[currentStepIndex];
  const allCaptured = currentStepIndex >= ENROLL_STEPS.length;

  /* ── Capture handlers ────────────────────────────────────────────────── */

  const handleCaptureComplete = useCallback(async (frames) => {
    // Hard ref lock: prevents re-entry even during async gaps
    if (processingRef.current) return;
    if (scanStatus === "validating" || scanStatus === "success" || scanStatus === "uploading") return;
    processingRef.current = true;

    setScanStatus("validating");
    const frame = frames[0];
    const isLastStep = currentStepIndex === ENROLL_STEPS.length - 1;

    // Capture frame for this step
    setCapturedData((prev) => {
      const next = { ...prev, [activeStep.key]: frame };

      if (isLastStep) {
        // Last step done — submit everything after a short pause
        toast.success(`${activeStep.label} captured!`);
        setTimeout(() => submitRegistration(next), 600);
      }

      return next;
    });

    if (!isLastStep) {
      toast.success(`${activeStep.label} captured!`);
      setTimeout(() => {
        setScanStatus("idle");
        setScannerKey((k) => k + 1);
        setCurrentStepIndex((prev) => prev + 1);
        processingRef.current = false;
      }, 900);
    } else {
      // Keep status as "validating" until submitRegistration takes over
      setScanStatus("uploading");
    }
  }, [scanStatus, activeStep, currentStepIndex, user]);

  const submitRegistration = async (completeData) => {
    setScanStatus("uploading");

    const framesList = [];
    const anglesList = [];

    ENROLL_STEPS.forEach((step) => {
      if (completeData[step.key]) {
        framesList.push(completeData[step.key]);
        anglesList.push(step.angle);
      }
    });

    const result = await dispatch(
      RegisterFace({
        email: user?.email,
        frames: framesList,
        angles: anglesList,
        deviceFingerprint: navigator.userAgent,
      })
    );

    processingRef.current = false;

    if (RegisterFace.fulfilled.match(result)) {
      setScanStatus("success");
      toast.success("Face ID enrolled successfully! You can now log in with Face ID.");
      await dispatch(GetCurrentUser());
      setTimeout(() => {
        setEnrolling(false);
        setCurrentStepIndex(0);
        setScannerKey(0);
        setCapturedData({});
        setScanStatus("idle");
      }, 2000);
    } else {
      setScanStatus("error");
      setScanError(result.payload?.detail || "Face ID registration failed. Please retry.");
    }
  };

  /* ── Delete handler ──────────────────────────────────────────────────── */

  const handleDeleteBiometrics = async () => {
    if (!window.confirm("Are you sure you want to remove Face ID? You will need to use Email/OTP to log in.")) return;

    setDeleting(true);
    try {
      await API.delete("/api/face/biometrics");
      toast.success("Face ID removed successfully.");
      await dispatch(GetCurrentUser());
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to remove Face ID.");
    } finally {
      setDeleting(false);
    }
  };

  /* ── Start enrollment ────────────────────────────────────────────────── */

  const startEnrollment = () => {
    processingRef.current = false;
    setEnrolling(true);
    setCurrentStepIndex(0);
    setScannerKey(0);
    setCapturedData({});
    setScanStatus("idle");
    setScanError("");
  };

  const cancelEnrollment = () => {
    processingRef.current = false;
    setEnrolling(false);
    setCurrentStepIndex(0);
    setScannerKey(0);
    setCapturedData({});
    setScanStatus("idle");
    setScanError("");
  };

  /* ─── Render ─────────────────────────────────────────────────────────── */

  return (
    <div className="mx-auto max-w-3xl space-y-10">
      <section>
        <h2 className="text-base font-semibold">Face ID Authentication</h2>
        <p className="mt-1 text-xs text-muted-foreground">
          Set up camera-based biometric login to replace OTP verification.
        </p>

        {/* ── Status Card ──────────────────────────────────────────────── */}
        <div
          className={`mt-4 border p-5 rounded-xl flex items-start gap-4 transition-all duration-300 ${
            isRegistered
              ? "bg-emerald-950/20 border-emerald-500/20 shadow-[0_4px_25px_rgba(16,185,129,0.06)]"
              : "bg-zinc-900/30 border-zinc-800"
          }`}
        >
          <div
            className={`p-3 rounded-full shrink-0 ${
              isRegistered ? "bg-emerald-500/10 text-emerald-400" : "bg-zinc-800 text-zinc-400"
            }`}
          >
            {isRegistered ? <ShieldCheck className="h-6 w-6" /> : <ShieldAlert className="h-6 w-6" />}
          </div>
          <div className="space-y-1 flex-1">
            <h4 className="text-sm font-semibold text-zinc-100">
              {isRegistered ? "Face ID Activated" : "Face ID Not Configured"}
            </h4>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {isRegistered
                ? "Your face biometrics are securely enrolled. You can use Face ID to sign in on the login page."
                : "Enroll your face to enable passwordless biometric authentication. This captures your face at 5 angles for secure identity matching."}
            </p>
          </div>
        </div>

        {/* ── Feature Highlights ───────────────────────────────────────── */}
        {!enrolling && (
          <div className="mt-6 space-y-4">
            <h5 className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Security Architecture</h5>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { icon: Camera, title: "5-Angle Calibration", desc: "Front, left, right, smile, neutral" },
                { icon: Fingerprint, title: "ONNX Embeddings", desc: "ArcFace 512-dim vector match" },
                { icon: Scan, title: "Anti-Spoofing", desc: "Active eye blink liveness check" },
              ].map(({ icon: Icon, title, desc }) => (
                <div key={title} className="p-3 bg-zinc-900/20 border border-zinc-800/60 rounded-xl text-xs flex items-center gap-3">
                  <Icon className="h-4 w-4 text-indigo-400 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <span className="block font-medium text-zinc-200 truncate">{title}</span>
                    <span className="text-[10px] text-zinc-500">{desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Enrollment Scanner Flow ──────────────────────────────────── */}
        {enrolling && !allCaptured && (
          <div className="mt-6 space-y-5">
            {/* Step indicator */}
            <div className="flex justify-between items-center px-2">
              {ENROLL_STEPS.map((step, idx) => (
                <div key={step.key} className="flex items-center">
                  <div
                    className={`h-7 w-7 rounded-full flex items-center justify-center text-[10px] font-mono font-bold border transition-all duration-300 ${
                      idx < currentStepIndex
                        ? "bg-indigo-600 border-indigo-600 text-white"
                        : idx === currentStepIndex
                        ? "bg-zinc-950 border-indigo-500 text-indigo-400 ring-2 ring-indigo-500/20"
                        : "bg-zinc-950 border-zinc-800 text-zinc-600"
                    }`}
                  >
                    {idx < currentStepIndex ? <CheckCircle2 className="h-3.5 w-3.5" /> : idx + 1}
                  </div>
                  {idx < ENROLL_STEPS.length - 1 && (
                    <div
                      className={`h-0.5 w-6 sm:w-10 transition-all duration-300 ${
                        idx < currentStepIndex ? "bg-indigo-600" : "bg-zinc-800"
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>

            <p className="text-center text-xs text-zinc-400 font-medium">
              Step {currentStepIndex + 1} of {ENROLL_STEPS.length}: {activeStep.label}
            </p>

            {/* Camera — key=scannerKey means it only remounts when we explicitly allow it */}
            <FaceScanner
              key={scannerKey}
              onFrameCaptured={null}
              onCaptureComplete={handleCaptureComplete}
              activeChallenge={null}
              challengeProgress={0}
              maxFrames={1}
              autoCaptureInterval={3000}
              statusMessage={
                scanStatus === "uploading"
                  ? "Saving your Face ID — please wait..."
                  : scanStatus === "validating"
                  ? "Processing face..."
                  : activeStep?.instruction ?? ""
              }
              isProcessing={scanStatus === "validating" || scanStatus === "uploading"}
              isSuccess={scanStatus === "success"}
              isError={scanStatus === "error"}
              errorMessage={scanError}
            />

            {scanStatus === "error" && (
              <Button
                className="w-full text-xs"
                onClick={() => {
                  processingRef.current = false;
                  setScanStatus("idle");
                  setScanError("");
                  setChallengeProgress(0);
                  // Remount FaceScanner cleanly on retry
                  setScannerKey((k) => k + 1);
                }}
              >
                Retry Step
              </Button>
            )}

            <button
              onClick={cancelEnrollment}
              className="block mx-auto text-[11px] font-mono text-zinc-500 hover:text-zinc-300 transition-colors uppercase tracking-widest"
            >
              ← Cancel Enrollment
            </button>
          </div>
        )}

        {/* ── Action Buttons ───────────────────────────────────────────── */}
        {!enrolling && (
          <div className="mt-6 space-y-3">
            {isRegistered ? (
              <Button
                variant="outline"
                className="w-full text-xs h-10 border-destructive/25 text-destructive hover:bg-destructive/10"
                onClick={handleDeleteBiometrics}
                disabled={deleting}
              >
                <Trash2 className="mr-1.5 h-3.5 w-3.5" />
                {deleting ? "Removing..." : "Remove Face ID"}
              </Button>
            ) : (
              <Button className="w-full text-xs h-10" onClick={startEnrollment}>
                <Camera className="mr-1.5 h-3.5 w-3.5" />
                Enable Face ID Login
                <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
              </Button>
            )}
          </div>
        )}
      </section>

      {/* ── Password & Sessions (placeholder) ───────────────────────────── */}
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
