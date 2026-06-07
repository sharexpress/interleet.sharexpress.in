import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "sonner";
import { UserCheck, CornerDownRight, ArrowRight, UserPlus, Info, Fingerprint, Camera, Cpu, Sparkles } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { FaceScanner } from "@/components/auth/FaceScanner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RegisterFace } from "@/redux/slices/userSlice";
import { API } from "@/api/api";
import { base64urlToBuffer, bufferToBase64url, isLocalBiometricsAvailable } from "@/lib/webauthn";

const ENROLL_STEPS = [
  { key: "front", label: "Front Look", instruction: "Look directly at the camera with a neutral face", angle: "front" },
  { key: "left", label: "Left Angle", instruction: "Turn your head slightly to the left", angle: "left" },
  { key: "right", label: "Right Angle", instruction: "Turn your head slightly to the right", angle: "right" },
  { key: "smile", label: "Smiling Face", instruction: "Smile widely showing your teeth", angle: "smile" },
  { key: "blink", label: "Liveness Check", instruction: "Blink twice clearly to verify liveness", angle: "neutral" }
];

export default function RegisterFacePage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { loading, isAuthenticated, onboardingCompleted } = useSelector((state) => state.user);

  const [emailInput, setEmailInput] = useState("");
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  
  // Method selection states
  const [methodSelected, setMethodSelected] = useState(null); // null, 'passkey', 'scanner'
  const [biometricsAvailable, setBiometricsAvailable] = useState(false);
  
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [capturedData, setCapturedData] = useState({}); // { front: base64, left: base64... }
  const [blinkFrames, setBlinkFrames] = useState([]);
  
  const [scanStatus, setScanStatus] = useState("idle"); // idle, loading, scanning, validating, success, error, uploading
  const [scanError, setScanError] = useState("");
  const [challengeProgress, setChallengeProgress] = useState(0);

  const activeStep = ENROLL_STEPS[currentStepIndex];

  // Auto-redirect if already logged in and face registered
  useEffect(() => {
    if (isAuthenticated) {
      navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
    }
  }, [isAuthenticated, onboardingCompleted, navigate]);

  // Check if native biometrics (like Apple Face ID) are available on this browser/device
  useEffect(() => {
    isLocalBiometricsAvailable().then(setBiometricsAvailable);
  }, []);

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    if (!emailInput.trim()) return;
    
    try {
      setScanStatus("loading");
      // Verify user has set up an account
      await API.post("/auth/send-otp", { email: emailInput.trim() });
      setEmailSubmitted(true);
      setScanStatus("idle");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Account check failed. Register via OTP first.");
      setScanStatus("idle");
    }
  };

  const handlePasskeyEnroll = async () => {
    setScanStatus("loading");
    setScanError("");
    
    try {
      // 1. Fetch registration options from backend
      const optionsRes = await API.post("/api/passkey/register/options", {
        email: emailInput.trim().lower(),
      });
      const options = optionsRes.data;

      // 2. Decode base64url strings to ArrayBuffers for browser credentials API
      options.challenge = base64urlToBuffer(options.challenge);
      options.user.id = base64urlToBuffer(options.user.id);
      if (options.excludeCredentials) {
        options.excludeCredentials = options.excludeCredentials.map(cred => ({
          ...cred,
          id: base64urlToBuffer(cred.id)
        }));
      }

      toast.info("Follow your browser's prompt to register native biometrics.");

      // 3. Trigger native Apple Face ID / biometric registration prompt
      const credential = await navigator.credentials.create({
        publicKey: options
      });

      if (!credential) {
        throw new Error("Failed to capture native credentials");
      }

      setScanStatus("validating");

      // 4. Encode ArrayBuffers to base64url strings for JSON transmission
      const verificationPayload = {
        email: emailInput.trim().lower(),
        credential: {
          id: credential.id,
          rawId: bufferToBase64url(credential.rawId),
          type: credential.type,
          response: {
            clientDataJSON: bufferToBase64url(credential.response.clientDataJSON),
            attestationObject: bufferToBase64url(credential.response.attestationObject),
          }
        }
      };

      // 5. Send to backend to verify and store the credential key
      const verifyRes = await API.post("/api/passkey/register/verify", verificationPayload);

      if (verifyRes.data.success) {
        setScanStatus("success");
        toast.success("Native biometrics registered successfully!");
        setTimeout(() => {
          navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
        }, 1500);
      } else {
        setScanStatus("error");
        setScanError("Verification failed on the security server.");
      }

    } catch (err) {
      console.error("Passkey registration error:", err);
      setScanStatus("error");
      if (err.name === "NotAllowedError") {
        setScanError("Biometric verification prompt was cancelled or timed out.");
      } else {
        setScanError(err.response?.data?.detail || "Passkey registration failed. Please try again.");
      }
    }
  };

  const handleFrameCaptured = (frameB64) => {
    // For regular steps, we wait for auto capture
  };

  const handleCaptureComplete = async (frames) => {
    if (scanStatus === "validating" || scanStatus === "success") return;
    
    setScanStatus("validating");
    const frame = frames[0];

    if (activeStep.key !== "blink") {
      setCapturedData(prev => ({ ...prev, [activeStep.key]: frame }));
      toast.success(`${activeStep.label} captured!`);
      
      setTimeout(() => {
        setScanStatus("idle");
        setCurrentStepIndex(prev => prev + 1);
      }, 800);
    } else {
      setBlinkFrames(frames);
      setChallengeProgress(50);
      
      try {
        const livenessRes = await API.post("/api/face/liveness", {
          email: emailInput.trim().lower(),
          challenge_type: "blink",
          frames: frames,
          device_fingerprint: navigator.userAgent
        });
        
        if (livenessRes.data.success) {
          setChallengeProgress(100);
          setCapturedData(prev => ({ ...prev, blink: frames[2] })); // Middle frame for embedding
          setScanStatus("success");
          toast.success("Biometrics liveness verified!");
          
          setTimeout(() => {
            submitFullRegistration({
              ...capturedData,
              blink: frames[2]
            });
          }, 1000);
        } else {
          setScanStatus("error");
          setScanError(livenessRes.data.metrics.reason || "Liveness check failed. Please blink twice.");
          setChallengeProgress(0);
        }
      } catch (err) {
        setScanStatus("error");
        setScanError(err.response?.data?.detail || "Network liveness check failed. Retry scan.");
        setChallengeProgress(0);
      }
    }
  };

  const submitFullRegistration = async (completeData) => {
    setScanStatus("uploading");
    
    const framesList = [];
    const anglesList = [];
    
    ENROLL_STEPS.forEach(step => {
      if (completeData[step.key]) {
        framesList.push(completeData[step.key]);
        anglesList.push(step.angle);
      }
    });

    const result = await dispatch(RegisterFace({
      email: emailInput.trim().lower(),
      frames: framesList,
      angles: anglesList,
      deviceFingerprint: navigator.userAgent
    }));

    if (RegisterFace.fulfilled.match(result)) {
      setScanStatus("success");
      toast.success("Face ID enrolled successfully!");
      setTimeout(() => {
        navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
      }, 1500);
    } else {
      setScanStatus("error");
      setScanError(result.payload?.detail || "Biometric registration failed. Please restart.");
    }
  };

  const getSubtitle = () => {
    if (!emailSubmitted) return "Verify email to set up custom biometrics.";
    if (!methodSelected) return "Choose your preferred biometric security method.";
    if (methodSelected === "passkey") return "Enroll Apple Face ID / native platform biometrics.";
    return `Step ${currentStepIndex + 1} of 5: Biometric Scanner`;
  };

  return (
    <AuthShell
      title="Enroll your Face ID"
      subtitle={getSubtitle()}
    >
      {!emailSubmitted ? (
        // Step 1: Email verification
        <form onSubmit={handleEmailSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Confirm Account Email</Label>
            <Input
              id="email"
              type="email"
              required
              value={emailInput}
              onChange={(e) => setEmailInput(e.target.value)}
              placeholder="you@company.com"
              autoComplete="email"
            />
          </div>
          <Button type="submit" className="w-full" disabled={scanStatus === "loading"}>
            {scanStatus === "loading" ? "Verifying..." : "Verify Account Email"}
          </Button>
          <div className="bg-zinc-900/40 border border-zinc-800 rounded-lg p-3 text-xs text-zinc-500 leading-normal flex items-start gap-2">
            <Info className="h-4 w-4 text-indigo-500 shrink-0 mt-0.5" />
            <span>Ensure you have registered an account first via standard Email/OTP. Set up Face ID is added to secure existing profile logins.</span>
          </div>
        </form>
      ) : !methodSelected ? (
        // Step 2: Choose Method
        <div className="space-y-4">
          <div className="text-center pb-2">
            <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Select Enrolment Type</span>
          </div>
          
          <div className="grid grid-cols-1 gap-4">
            {/* Passkey option */}
            <button
              type="button"
              onClick={() => setMethodSelected("passkey")}
              className={`flex items-start text-left gap-4 p-4 rounded-xl border transition-all duration-300 ${
                biometricsAvailable 
                  ? "bg-zinc-900/30 border-zinc-800 hover:border-indigo-500 hover:bg-zinc-900/60 cursor-pointer group" 
                  : "bg-zinc-950/20 border-zinc-900 opacity-60 cursor-not-allowed"
              }`}
            >
              <div className={`p-2.5 rounded-lg border transition-all duration-300 ${
                biometricsAvailable 
                  ? "bg-indigo-950/20 border-indigo-900 group-hover:border-indigo-500/50 group-hover:bg-indigo-950/40 text-indigo-400" 
                  : "bg-zinc-900 border-zinc-800 text-zinc-600"
              }`}>
                <Fingerprint className="h-5 w-5" />
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-1.5">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-zinc-200">Native Face ID</h4>
                  {biometricsAvailable && (
                    <span className="text-[9px] bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-1.5 py-0.5 rounded-full font-mono font-bold uppercase tracking-wider">
                      Recommended
                    </span>
                  )}
                </div>
                <p className="text-[11px] text-zinc-500 leading-relaxed">
                  Uses Apple's native biometric engine. Safe, 100% private, runs entirely inside the secure hardware enclave.
                </p>
                {!biometricsAvailable && (
                  <span className="text-[9px] text-rose-500/80 font-mono uppercase tracking-wider block pt-1">
                    Not supported on this device/browser
                  </span>
                )}
              </div>
            </button>

            {/* Custom Face Scan option */}
            <button
              type="button"
              onClick={() => setMethodSelected("scanner")}
              className="flex items-start text-left gap-4 p-4 rounded-xl border border-zinc-800 bg-zinc-900/30 hover:border-zinc-700 hover:bg-zinc-900/60 cursor-pointer group transition-all duration-300"
            >
              <div className="p-2.5 rounded-lg border border-zinc-800 bg-zinc-900 text-zinc-400 group-hover:text-zinc-200 transition-all duration-300">
                <Camera className="h-5 w-5" />
              </div>
              <div className="space-y-1">
                <h4 className="text-xs font-mono uppercase tracking-wider text-zinc-200">Custom Face Scanner</h4>
                <p className="text-[11px] text-zinc-500 leading-relaxed">
                  Generates biometric embeddings via multi-angle webcam scans. Verified using our servers.
                </p>
              </div>
            </button>
          </div>

          <div className="text-center pt-4 border-t border-zinc-900/60">
            <button
              onClick={() => setEmailSubmitted(false)}
              className="text-[10px] font-mono text-zinc-500 hover:text-zinc-300 transition-colors uppercase tracking-widest"
            >
              ← Back to email
            </button>
          </div>
        </div>
      ) : methodSelected === "passkey" ? (
        // Passkey flow screen
        <div className="space-y-6 flex flex-col items-center">
          <div className="relative flex items-center justify-center h-[200px] w-[200px] rounded-full border border-zinc-800/80 bg-zinc-950 shadow-[0_0_50px_rgba(99,102,241,0.02)]">
            <div className="absolute inset-0 rounded-full border border-dashed border-indigo-500/20 animate-spin" style={{ animationDuration: '40s' }} />
            {scanStatus === "loading" ? (
              <div className="flex flex-col items-center justify-center text-center px-4">
                <Cpu className="h-8 w-8 text-indigo-500 animate-pulse mb-2" />
                <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest">Awaiting Prompt...</span>
              </div>
            ) : scanStatus === "validating" ? (
              <div className="flex flex-col items-center justify-center text-center px-4">
                <UserCheck className="h-8 w-8 text-emerald-500 animate-bounce mb-2" />
                <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest">Verifying Passkey...</span>
              </div>
            ) : scanStatus === "success" ? (
              <div className="flex flex-col items-center justify-center text-center px-4">
                <Sparkles className="h-8 w-8 text-indigo-400 mb-2" />
                <span className="text-[10px] font-mono text-indigo-400 font-bold uppercase tracking-widest">Enrolled!</span>
              </div>
            ) : scanStatus === "error" ? (
              <div className="flex flex-col items-center justify-center text-center px-4">
                <Fingerprint className="h-8 w-8 text-rose-500 mb-2" />
                <span className="text-[10px] font-mono text-rose-400 uppercase tracking-widest">Failed</span>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center text-center px-4">
                <Fingerprint className="h-8 w-8 text-indigo-500/60 mb-2" />
                <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest">Ready</span>
              </div>
            )}
          </div>

          {scanStatus === "error" && (
            <div className="w-full text-center px-3 py-2 bg-rose-950/20 border border-rose-900/50 rounded-lg text-[11px] font-mono text-rose-400">
              {scanError}
            </div>
          )}

          <div className="w-full space-y-3">
            {scanStatus !== "success" && (
              <Button
                type="button"
                className="w-full text-xs font-mono uppercase tracking-wider"
                disabled={scanStatus === "loading" || scanStatus === "validating"}
                onClick={handlePasskeyEnroll}
              >
                Trigger Biometric Enrollment
              </Button>
            )}
            
            <Button
              variant="outline"
              className="w-full text-xs font-mono uppercase tracking-wider border-zinc-800 hover:bg-zinc-900 text-zinc-400 hover:text-zinc-200"
              disabled={scanStatus === "loading" || scanStatus === "validating"}
              onClick={() => {
                setMethodSelected(null);
                setScanStatus("idle");
                setScanError("");
              }}
            >
              Change Method
            </Button>
          </div>
        </div>
      ) : (
        // Step 3: Webcam Scanner (Option 2)
        <div className="space-y-6">
          <div className="flex justify-between items-center px-6">
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
                  {idx < currentStepIndex ? "✓" : idx + 1}
                </div>
                {idx < ENROLL_STEPS.length - 1 && (
                  <div 
                    className={`h-0.5 w-8 transition-all duration-300 ${
                      idx < currentStepIndex ? "bg-indigo-600" : "bg-zinc-800"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>

          <FaceScanner
            onFrameCaptured={handleFrameCaptured}
            onCaptureComplete={handleCaptureComplete}
            activeChallenge={activeStep.key === "blink" ? "blink" : null}
            challengeProgress={challengeProgress}
            maxFrames={activeStep.key === "blink" ? 5 : 1}
            autoCaptureInterval={activeStep.key === "blink" ? 500 : 2500}
            statusMessage={
              scanStatus === "uploading" 
                ? "Securing embeddings in vector DB..." 
                : scanStatus === "validating" 
                ? "Processing face crop landmarks..." 
                : activeStep.instruction
            }
            isProcessing={scanStatus === "validating" || scanStatus === "uploading" || scanStatus === "loading"}
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
                setChallengeProgress(0);
              }}
            >
              Retry Step
            </Button>
          )}

          <div className="text-center space-y-2">
            <button
              onClick={() => {
                setMethodSelected(null);
                setScanStatus("idle");
                setScanError("");
                setCurrentStepIndex(0);
              }}
              className="text-[10px] font-mono text-indigo-400 hover:text-indigo-300 transition-colors uppercase tracking-widest block mx-auto"
            >
              ← Choose another method
            </button>
            <button
              onClick={() => {
                setEmailSubmitted(false);
                setMethodSelected(null);
                setScanStatus("idle");
                setScanError("");
                setCurrentStepIndex(0);
              }}
              className="text-[10px] font-mono text-zinc-500 hover:text-zinc-300 transition-colors uppercase tracking-widest block mx-auto"
            >
              ← Back to email verification
            </button>
          </div>
        </div>
      )}
    </AuthShell>
  );
}
