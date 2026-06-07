import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { toast } from "sonner";
import { KeyRound, Camera, ShieldCheck, Sparkles, CornerDownLeft, Fingerprint, Cpu } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { FaceScanner } from "@/components/auth/FaceScanner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LoginFace } from "@/redux/slices/userSlice";
import { API } from "@/api/api";
import { base64urlToBuffer, bufferToBase64url, isLocalBiometricsAvailable } from "@/lib/webauthn";

export default function LoginFacePage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const [emailInput, setEmailInput] = useState("");
  const [scanActive, setScanActive] = useState(false);
  const [biometricsAvailable, setBiometricsAvailable] = useState(false);
  
  const [scanStatus, setScanStatus] = useState("idle"); // idle, scanning, validating, challenge, success, error, loading
  const [statusMessage, setStatusMessage] = useState("Align your face to begin biometric authentication");
  const [scanError, setScanError] = useState("");
  
  // Challenge states
  const [activeChallenge, setActiveChallenge] = useState(null);
  const [challengeEmail, setChallengeEmail] = useState("");
  const [challengeProgress, setChallengeProgress] = useState(0);

  // Check if native biometrics (like Apple Face ID) are available on this browser/device
  useEffect(() => {
    isLocalBiometricsAvailable().then(setBiometricsAvailable);
  }, []);

  // Inactivity timeout timer to turn off camera
  useEffect(() => {
    if (!scanActive || scanStatus === "success" || scanStatus === "validating" || activeChallenge) {
      return;
    }

    const timer = setTimeout(() => {
      setScanActive(false);
      setScanStatus("error");
      setScanError("Biometric scanner timed out due to inactivity. Please try again.");
      toast.warning("Camera turned off due to inactivity.");
    }, 20000); // 20 seconds timeout

    return () => clearTimeout(timer);
  }, [scanActive, scanStatus, activeChallenge]);

  const handlePasskeyLogin = async () => {
    if (!emailInput.trim()) {
      toast.error("Please enter your registered email address first.");
      return;
    }

    setScanStatus("loading");
    setStatusMessage("Awaiting native biometrics prompt...");
    setScanError("");
    setScanActive(false); // Make sure webcam scanner is disabled during passkey flow

    try {
      // 1. Fetch authentication options from backend
      const optionsRes = await API.post("/api/passkey/login/options", {
        email: emailInput.trim().lower(),
      });
      const options = optionsRes.data;

      // 2. Decode base64url strings to ArrayBuffers
      options.challenge = base64urlToBuffer(options.challenge);
      if (options.allowCredentials) {
        options.allowCredentials = options.allowCredentials.map(cred => ({
          ...cred,
          id: base64urlToBuffer(cred.id)
        }));
      }

      toast.info("Follow your browser's prompt to verify native biometrics.");

      // 3. Invoke browser credentials API to get assertion
      const assertion = await navigator.credentials.get({
        publicKey: options
      });

      if (!assertion) {
        throw new Error("Failed to capture native credentials");
      }

      setScanStatus("validating");
      setStatusMessage("Verifying signature with platform secure enclave...");

      // 4. Encode ArrayBuffers to base64url strings
      const verifyPayload = {
        email: emailInput.trim().lower(),
        credential: {
          id: assertion.id,
          rawId: bufferToBase64url(assertion.rawId),
          type: assertion.type,
          response: {
            authenticatorData: bufferToBase64url(assertion.response.authenticatorData),
            clientDataJSON: bufferToBase64url(assertion.response.clientDataJSON),
            signature: bufferToBase64url(assertion.response.signature),
            userHandle: assertion.response.userHandle ? bufferToBase64url(assertion.response.userHandle) : null,
          }
        }
      };

      // 5. Submit to backend to verify signature and sign in
      const verifyRes = await API.post("/api/passkey/login/verify", verifyPayload);
      
      if (verifyRes.data.success) {
        setScanStatus("success");
        setStatusMessage("Face ID matches! Logging in...");
        toast.success("Welcome back! Biometrics verified.");
        setTimeout(() => {
          navigate("/app/dashboard");
        }, 1500);
      } else {
        setScanStatus("error");
        setScanError("Verification failed on the security server.");
      }

    } catch (err) {
      console.error("Passkey login error:", err);
      setScanStatus("error");
      if (err.name === "NotAllowedError") {
        setScanError("Biometric verification prompt was cancelled.");
      } else {
        setScanError(err.response?.data?.detail || "Passkey login failed. Check email or biometrics registration.");
      }
    }
  };

  const handleFrameCaptured = async (frameB64) => {
    if (scanStatus !== "idle" && scanStatus !== "scanning") return;
    
    setScanStatus("validating");
    setStatusMessage("Comparing facial landmarks...");
    
    try {
      const result = await dispatch(LoginFace({
        email: emailInput.trim(),
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
        const detail = errorData?.detail || "";
        if (errorData?.challenge_required) {
          toast.info("Liveness confirmation required to trust this device.");
          startLivenessChallenge(errorData.email);
        } else if (detail.toLowerCase().includes("not registered") || detail.toLowerCase().includes("enroll")) {
          setScanStatus("error");
          setScanError("Face ID not set up yet. Go to Settings → Security to enroll your face first.");
        } else {
          setScanStatus("error");
          setScanError(detail || "Biometric credentials match failed.");
        }
      }
    } catch (err) {
      const status = err?.response?.status || err?.status;
      if (status === 403) {
        setScanStatus("error");
        setScanError("Face ID not set up yet. Go to Settings → Security to enroll your face first.");
      } else {
        setScanStatus("error");
        setScanError("Connection error. Biometrics verification unavailable.");
      }
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
      <div className="space-y-6 flex flex-col items-center">
        
        {/* Email input field */}
        {!activeChallenge && (
          <div className="w-full space-y-3 p-3 bg-zinc-900/40 border border-zinc-800 rounded-xl">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-[10px] uppercase font-mono tracking-wider text-zinc-400">
                Email Address
              </Label>
              <Input
                id="email"
                type="email"
                value={emailInput}
                onChange={(e) => setEmailInput(e.target.value)}
                placeholder="you@company.com"
                className="h-9 text-xs bg-zinc-950 border-zinc-800"
                disabled={scanActive || scanStatus === "loading" || scanStatus === "validating"}
              />
            </div>
            
            {!scanActive && (
              <div className="flex flex-col gap-2 pt-1">
                {biometricsAvailable && (
                  <Button
                    type="button"
                    className="w-full text-xs font-mono uppercase tracking-wider bg-indigo-650 hover:bg-indigo-650/90 text-white shadow-lg shadow-indigo-950/20 border border-indigo-500/20 relative overflow-hidden group transition-all duration-300"
                    disabled={scanStatus === "loading" || scanStatus === "validating"}
                    onClick={handlePasskeyLogin}
                  >
                    <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <Fingerprint className="h-4 w-4 mr-2 text-indigo-200 animate-pulse group-hover:scale-110 transition-transform" />
                    Use Native Face ID
                  </Button>
                )}
                
                <Button
                  type="button"
                  variant="outline"
                  className="w-full text-xs font-mono uppercase tracking-wider border-zinc-800 hover:bg-zinc-900 hover:text-zinc-200"
                  disabled={scanStatus === "loading" || scanStatus === "validating"}
                  onClick={() => {
                    if (!emailInput.trim()) {
                      toast.error("Please enter your registered email address first.");
                      return;
                    }
                    setScanActive(true);
                    setScanStatus("idle");
                    setStatusMessage("Analyzing face biometrics...");
                  }}
                >
                  <Camera className="h-4 w-4 mr-2 text-zinc-400" />
                  Custom Face Scanner
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Display Status of Native Verification during Passkey flow */}
        {scanStatus === "loading" && !scanActive && (
          <div className="flex flex-col items-center justify-center h-[280px] w-[280px] rounded-full border-4 border-dashed border-indigo-500 bg-zinc-950/50 transition-all duration-300">
            <Cpu className="h-10 w-10 text-indigo-400 animate-pulse mb-3" />
            <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-widest text-center px-6 leading-relaxed">
              {statusMessage}
            </span>
          </div>
        )}

        {/* Biometric webcam scanner or placeholder */}
        {scanActive ? (
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
        ) : (
          scanStatus !== "loading" && (
            <div className="flex flex-col items-center justify-center h-[280px] w-[280px] rounded-full border-4 border-zinc-900 bg-zinc-950 shadow-[0_0_50px_rgba(99,102,241,0.05)] ring-4 ring-offset-4 ring-offset-black ring-zinc-800 transition-all duration-300">
              <Camera className="h-10 w-10 text-indigo-500/60 animate-pulse mb-3" />
              <span className="text-[11px] font-mono text-zinc-500 uppercase tracking-widest text-center px-6 leading-relaxed">
                {scanStatus === "error" ? "Verification Failed" : "Enter Email to Scan"}
              </span>
              {scanStatus === "error" && (
                <span className="text-[9px] text-rose-500/80 max-w-[200px] text-center font-mono mt-1 leading-normal px-2 truncate">
                  {scanError}
                </span>
              )}
            </div>
          )
        )}

        {(scanActive || scanStatus === "error" || scanStatus === "loading") && (
          <div className="w-full flex gap-3">
            {(scanStatus === "error" || scanStatus === "loading") && (
              <Button
                className="flex-1 text-xs font-mono uppercase tracking-wider"
                onClick={() => {
                  setScanStatus("idle");
                  setScanError("");
                  setActiveChallenge(null);
                  setChallengeProgress(0);
                  setStatusMessage("Align face in frame to retry match");
                  if (biometricsAvailable && !scanActive) {
                    handlePasskeyLogin();
                  } else {
                    setScanActive(true);
                  }
                }}
              >
                Retry
              </Button>
            )}
            <Button
              variant="outline"
              className="flex-1 text-xs font-mono uppercase tracking-wider border-zinc-800 hover:bg-zinc-900 text-zinc-400 hover:text-zinc-200"
              onClick={() => {
                setScanActive(false);
                setScanStatus("idle");
                setScanError("");
                setActiveChallenge(null);
                setChallengeProgress(0);
                setStatusMessage("Align your face to begin biometric authentication");
              }}
            >
              Change Email
            </Button>
          </div>
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
