import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "sonner";
import { UserCheck, CornerDownRight, ArrowRight, UserPlus, Info } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { FaceScanner } from "@/components/auth/FaceScanner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RegisterFace } from "@/redux/slices/userSlice";
import { API } from "@/api/api";

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
  
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [capturedData, setCapturedData] = useState({}); // { front: base64, left: base64... }
  const [blinkFrames, setBlinkFrames] = useState([]);
  
  const [scanStatus, setScanStatus] = useState("idle"); // idle, scanning, validating, success, error
  const [scanError, setScanError] = useState("");
  const [challengeProgress, setChallengeProgress] = useState(0);

  const activeStep = ENROLL_STEPS[currentStepIndex];

  // Auto-redirect if already logged in and face registered
  useEffect(() => {
    if (isAuthenticated) {
      // If user is already authed, they can complete the onboarding or go to dashboard
      navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
    }
  }, [isAuthenticated, onboardingCompleted, navigate]);

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    if (!emailInput.trim()) return;
    
    // Check if user exists
    try {
      setScanStatus("loading");
      const res = await API.post("/auth/send-otp", { email: emailInput.trim() });
      // If OTP goes through, user exists, we can enroll their face.
      setEmailSubmitted(true);
      setScanStatus("idle");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Account check failed. Register via OTP first.");
      setScanStatus("idle");
    }
  };

  const handleFrameCaptured = (frameB64) => {
    // For regular steps, we just wait for the auto interval to capture 1 frame
  };

  const handleCaptureComplete = async (frames) => {
    if (scanStatus === "validating" || scanStatus === "success") return;
    
    setScanStatus("validating");
    const frame = frames[0];

    if (activeStep.key !== "blink") {
      // Regular angle step: save frame and advance step
      setCapturedData(prev => ({ ...prev, [activeStep.key]: frame }));
      
      toast.success(`${activeStep.label} captured!`);
      
      setTimeout(() => {
        setScanStatus("idle");
        setCurrentStepIndex(prev => prev + 1);
      }, 800);
    } else {
      // Liveness step: captures 5 frames to verify blinking liveness on backend
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
          setCapturedData(prev => ({ ...prev, blink: frames[2] })); // Use middle frame for neural face
          setScanStatus("success");
          toast.success("Biometrics liveness verified!");
          
          // Complete full enrollment upload
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
      // Redirect to onboarding or dashboard
      setTimeout(() => {
        navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
      }, 1500);
    } else {
      setScanStatus("error");
      setScanError(result.payload?.detail || "Biometric registration failed. Please restart.");
    }
  };

  return (
    <AuthShell
      title="Enroll your Face ID"
      subtitle={!emailSubmitted ? "Verify email to set up custom biometrics." : `Step ${currentStepIndex + 1} of 5: Biometric Scanner`}
    >
      {!emailSubmitted ? (
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
      ) : (
        <div className="space-y-6">
          {/* Circular Stepper Visuals */}
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

          {/* Camera Frame Ingest component */}
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

          <div className="text-center">
            <button
              onClick={() => setEmailSubmitted(false)}
              className="text-[11px] font-mono text-zinc-500 hover:text-zinc-300 transition-colors uppercase tracking-widest"
            >
              ← Back to email verification
            </button>
          </div>
        </div>
      )}
    </AuthShell>
  );
}
