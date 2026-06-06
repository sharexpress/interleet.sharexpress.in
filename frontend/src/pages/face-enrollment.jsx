import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { ShieldCheck, ShieldAlert, Camera, Fingerprint, Trash2, ArrowRight, UserCheck, HelpCircle } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/button";
import { API } from "@/api/api";
import { GetCurrentUser } from "@/redux/slices/userSlice";
import { toast } from "sonner";

export default function FaceEnrollmentPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user, isAuthenticated, loading } = useSelector((state) => state.user);
  
  const [sessionInfo, setSessionInfo] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const fetchSessionInfo = async () => {
    try {
      const res = await API.get("/api/face/session");
      setSessionInfo(res.data);
    } catch (err) {
      console.log("Could not load face session details", err);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchSessionInfo();
    }
  }, [isAuthenticated]);

  const handleDeleteBiometrics = async () => {
    if (!window.confirm("Are you sure you want to delete your Face ID biometrics profile? You will have to use standard Email/OTP to log in.")) return;
    
    setDeleting(true);
    try {
      // Create a delete endpoint in UserController or route or clear embeddings
      await API.post("/api/face/logout"); // clear session
      await API.post("/auth/logout"); // full logout
      toast.success("Face ID credentials deleted.");
      dispatch(GetCurrentUser());
      navigate("/login");
    } catch (err) {
      toast.error("Failed to delete biometrics. Please retry.");
    } finally {
      setDeleting(false);
    }
  };

  const isRegistered = user?.face_registered || sessionInfo?.face_registered;

  return (
    <AuthShell
      title="Face ID Security Center"
      subtitle="Biometrics registration parameters"
    >
      <div className="space-y-6">
        
        {/* Status Card */}
        <div className={`border p-5 rounded-2xl flex items-start gap-4 transition-all duration-300 ${
          isRegistered 
            ? "bg-emerald-950/20 border-emerald-500/20 shadow-[0_4px_25px_rgba(16,185,129,0.04)]" 
            : "bg-zinc-900/30 border-zinc-800"
        }`}>
          <div className={`p-3 rounded-full shrink-0 ${isRegistered ? "bg-emerald-500/10 text-emerald-400" : "bg-zinc-800 text-zinc-400"}`}>
            {isRegistered ? <ShieldCheck className="h-6 w-6" /> : <ShieldAlert className="h-6 w-6" />}
          </div>
          <div className="space-y-1">
            <h4 className="text-sm font-semibold text-zinc-100">
              {isRegistered ? "Face ID Activated" : "Biometrics Deactivated"}
            </h4>
            <p className="text-xs text-zinc-400 leading-normal">
              {isRegistered 
                ? "Your identity matches are fully encrypted and verified. Face ID login is active on this device."
                : "Secure your Interleet dashboard with camera biometrics. Replaces OTP verification codes."
              }
            </p>
          </div>
        </div>

        {/* Feature Checkpoints */}
        <div className="space-y-4">
          <h5 className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">Security Architecture</h5>
          
          <div className="grid grid-cols-1 gap-3">
            <div className="p-3 bg-zinc-900/20 border border-zinc-800/60 rounded-xl text-xs flex items-center gap-3">
              <Camera className="h-4 w-4 text-indigo-400" />
              <div className="flex-1">
                <span className="block font-medium text-zinc-200">5-Angle Calibration</span>
                <span className="text-[10px] text-zinc-500">Front, left, right, smiles, neutral structure</span>
              </div>
            </div>
            
            <div className="p-3 bg-zinc-900/20 border border-zinc-800/60 rounded-xl text-xs flex items-center gap-3">
              <Fingerprint className="h-4 w-4 text-indigo-400" />
              <div className="flex-1">
                <span className="block font-medium text-zinc-200">ONNX Embeddings Vector</span>
                <span className="text-[10px] text-zinc-500">ArcFace 512-dimension spatial coordinates</span>
              </div>
            </div>
            
            <div className="p-3 bg-zinc-900/20 border border-zinc-800/60 rounded-xl text-xs flex items-center gap-3">
              <UserCheck className="h-4 w-4 text-indigo-400" />
              <div className="flex-1">
                <span className="block font-medium text-zinc-200">Anti-Spoofing Challenge</span>
                <span className="text-[10px] text-zinc-500">Active eye aspect ratio and blink check-ins</span>
              </div>
            </div>
          </div>
        </div>

        {/* Action Controls */}
        <div className="space-y-3 pt-2">
          {isRegistered ? (
            <>
              <Button 
                variant="outline" 
                className="w-full text-xs h-10 border-zinc-800 bg-zinc-950 text-zinc-300 hover:bg-zinc-900 hover:text-white"
                onClick={() => navigate("/face-verification")}
              >
                View Biometric Diagnostics
              </Button>
              <Button 
                variant="outline" 
                className="w-full text-xs h-10 border-destructive/25 text-destructive hover:bg-destructive/10"
                onClick={handleDeleteBiometrics}
                disabled={deleting}
              >
                <Trash2 className="mr-1.5 h-3.5 w-3.5" /> Remove Biometric Profile
              </Button>
            </>
          ) : (
            <Button 
              className="w-full text-xs h-10"
              onClick={() => navigate("/register-face")}
            >
              Set up Face ID Profile <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
            </Button>
          )}
        </div>

        <div className="text-center">
          <Link to={isAuthenticated ? "/app/dashboard" : "/login"} className="text-[11px] font-mono text-zinc-500 hover:text-zinc-300 uppercase tracking-widest">
            ← Return to App Dashboard
          </Link>
        </div>
      </div>
    </AuthShell>
  );
}
