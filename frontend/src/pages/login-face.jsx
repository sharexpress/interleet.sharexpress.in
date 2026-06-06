import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { toast } from "sonner";
import { KeyRound, Camera, ShieldCheck, Sparkles, CornerDownLeft } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { FaceScanner } from "@/components/auth/FaceScanner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LoginFace } from "@/redux/slices/userSlice";
import { API } from "@/api/api";

export default function LoginFacePage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const [emailInput, setEmailInput] = useState("");
  const [useEmailFilter, setUseEmailFilter] = useState(false);
  
  const [scanStatus, setScanStatus] = useState("idle"); // idle, scanning, validating, challenge, success, error
  const [statusMessage, setStatusMessage] = useState("Align your face to begin biometric authentication");
  const [scanError, setScanError] = useState("");
  
  // Challenge states
  const [activeChallenge, setActiveChallenge] = useState(null);
  const [challengeEmail, setChallengeEmail] = useState("");
  const [challengeProgress, setChallengeProgress] = useState(0);

  const handleFrameCaptured = async (frameB64) => {
    // If we're validating, success, error or in active challenge sequence, we don't do single frame capture logins
    if (scanStatus !== "idle" && scanStatus !== "scanning") return;
    
    setScanStatus("validating");
    setStatusMessage("Comparing facial landmarks...");
    
    try {
      const result = await dispatch(LoginFace({
        email: useEmailFilter && emailInput.trim() ? emailInput.trim() : null,
        frame: frameB64,
        deviceFingerprint: navigator.userAgent
      }));
      
      if (LoginFace.fulfilled.match(result)) {
        const data = result.payload;
        if (data.success) {
          setScanStatus("success");
          setStatusMessage("Face ID matches! Logging in...");
          toast.success("Identity verified successfully!");
          setTimeout(() => {
            navigate("/app/dashboard");
          }, 1500);
        }
      } else {
        const errorData = result.payload;
        if (errorData?.challenge_required) {
          // LLM/Rules requested a liveness check
          toast.info("Liveness confirmation required to trust this device.");
          startLivenessChallenge(errorData.email);
        } else {
          const detail = errorData?.detail || "";
          setScanStatus("error");
          setScanError(
            detail.includes("Face ID not registered")
              ? "You haven't set up Face ID yet. Go to Settings → Security to enroll."
              : detail || "Biometric credentials match failed."
          );
        }
      }
    } catch (err) {
      setScanStatus("error");
      setScanError("Connection error. Biometrics verification unavailable.");
    }
  };

  const startLivenessChallenge = async (email) => {
    setChallengeEmail(email);
    setScanStatus("challenge");
    setStatusMessage("Initializing threat check...");
    
    try {
      const startRes = await API.post("/api/face/liveness/start", { email });
      if (startRes.data.success) {
        setActiveChallenge(startRes.data.challenge_type);
        setStatusMessage(startRes.data.instruction);
        setChallengeProgress(20);
      } else {
        setScanStatus("error");
        setScanError("Failed to initiate challenge. Retry login.");
      }
    } catch (err) {
      setScanStatus("error");
      setScanError("Failed to connect for security challenge. Retry login.");
    }
  };

  const handleChallengeCaptureComplete = async (frames) => {
    setScanStatus("validating");
    setStatusMessage("Evaluating liveness checks...");
    
    try {
      const verifyRes = await API.post("/api/face/liveness", {
        email: challengeEmail,
        challenge_type: activeChallenge,
        frames: frames,
        device_fingerprint: navigator.userAgent
      });
      
      if (verifyRes.data.success) {
        setChallengeProgress(100);
        toast.success("Liveness verified! Retrying face match...");
        
        // Clear challenge, return to scanning. Next scan will bypass because of recently passed liveness log!
        setTimeout(() => {
          setActiveChallenge(null);
          setScanStatus("idle");
          setStatusMessage("Analyzing face biometrics...");
          setChallengeProgress(0);
        }, 1200);
      } else {
        setScanStatus("error");
        setScanError(verifyRes.data.metrics.reason || "Liveness challenge failed. Please retry.");
        setChallengeProgress(0);
      }
    } catch (err) {
      setScanStatus("error");
      setScanError("Network verification error during security check. Retry.");
      setChallengeProgress(0);
    }
  };

  return (
    <AuthShell
      title="Sign in with Face ID"
      subtitle="Symmetric structure biometric match"
    >
      <div className="space-y-6">
        
        {/* Toggle email filter */}
        {!activeChallenge && (
          <div className="flex flex-col space-y-3 p-3 bg-zinc-900/40 border border-zinc-800 rounded-xl">
            <div className="flex items-center justify-between">
              <span className="text-xs text-zinc-400 font-mono">biometric filter</span>
              <button 
                onClick={() => setUseEmailFilter(!useEmailFilter)}
                className="text-[10px] font-semibold text-indigo-400 hover:text-indigo-300 font-mono uppercase"
              >
                {useEmailFilter ? "Disable Email filter" : "Enable Email filter"}
              </button>
            </div>
            
            {useEmailFilter && (
              <div className="space-y-2 animate-scale-up">
                <Label htmlFor="email" className="text-[10px] uppercase font-mono tracking-wider text-zinc-500">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={emailInput}
                  onChange={(e) => setEmailInput(e.target.value)}
                  placeholder="you@company.com"
                  className="h-8 text-xs bg-zinc-950 border-zinc-800"
                />
              </div>
            )}
          </div>
        )}

        {/* Biometric webcam scanner */}
        <FaceScanner
          onFrameCaptured={activeChallenge ? null : handleFrameCaptured}
          onCaptureComplete={activeChallenge ? handleChallengeCaptureComplete : null}
          activeChallenge={activeChallenge}
          challengeProgress={challengeProgress}
          maxFrames={activeChallenge ? 5 : 1}
          autoCaptureInterval={activeChallenge ? 500 : 1500}
          statusMessage={statusMessage}
          isProcessing={scanStatus === "validating" || scanStatus === "loading"}
          isSuccess={scanStatus === "success"}
          isError={scanStatus === "error"}
          errorMessage={scanError}
        />

        {scanStatus === "error" && (
          <Button
            className="w-full text-xs"
            onClick={() => {
              setScanStatus("idle");
              setScanError("");
              setActiveChallenge(null);
              setChallengeProgress(0);
              setStatusMessage("Align face in frame to retry match");
            }}
          >
            Retry Face Scan
          </Button>
        )}

        <div className="flex flex-col items-center justify-center space-y-2 text-center pt-2">
          <Link to="/login" className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 font-mono uppercase tracking-wider">
            <KeyRound className="h-3.5 w-3.5" /> Sign in via Email/OTP fallback
          </Link>
          <Link to="/register-face" className="text-[10px] text-zinc-500 hover:text-zinc-400 font-mono uppercase tracking-wider">
            Register face biometrics
          </Link>
        </div>
      </div>
    </AuthShell>
  );
}
