import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { API } from "@/api/api";
import { AuthShell } from "@/components/auth/AuthShell";
import { ShieldCheck, ShieldAlert, Cpu, Sparkles, RefreshCw, BarChart } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function FaceVerificationPage() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useSelector((state) => state.user);
  
  const [loading, setLoading] = useState(true);
  const [diagnostics, setDiagnostics] = useState(null);
  const [selectedAngle, setSelectedAngle] = useState("front");

  const loadDiagnostics = async () => {
    setLoading(true);
    try {
      const res = await API.get("/api/face/landmarks");
      setDiagnostics(res.data);
    } catch (err) {
      console.error("Failed to load biometrics diagnostics", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadDiagnostics();
    } else {
      navigate("/login");
    }
  }, [isAuthenticated]);

  const activeRecord = diagnostics?.records?.find(r => r.angle === selectedAngle) || diagnostics?.records?.[0];

  const getFullImageUrl = (url) => {
    if (!url) return "";
    if (url.startsWith("http")) return url;
    const backendBase = import.meta.env?.VITE_BACKEND_URL || "http://localhost:8000";
    return `${backendBase}${url}`;
  };

  // Render SVG Landmark Mesh
  const renderMesh = (landmarks) => {
    if (!landmarks || landmarks.length === 0) return null;
    
    // We only take a subset of landmarks to draw a clean mesh (e.g. 100 points)
    // Scale and center landmarks into a 240x240 SVG viewbox
    const xs = landmarks.map(pt => pt[0]);
    const ys = landmarks.map(pt => pt[1]);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    
    const w = maxX - minX;
    const h = maxY - minY;
    
    const scaledPoints = landmarks.map(pt => {
      // Scale coordinates to fit 30 to 210 padding
      const px = 30 + ((pt[0] - minX) / w) * 180;
      const py = 30 + ((pt[1] - minY) / h) * 180;
      return [px, py];
    });

    // Simple triangulation: connect points close to each other
    const lines = [];
    // Eye circles
    const leftEye = [33, 160, 158, 133, 153, 144];
    const rightEye = [362, 385, 387, 263, 373, 380];
    const mouth = [61, 291, 13, 14];
    
    const drawLoop = (indices) => {
      for (let i = 0; i < indices.length; i++) {
        const p1 = scaledPoints[indices[i]];
        const p2 = scaledPoints[indices[(i + 1) % indices.length]];
        if (p1 && p2) {
          lines.push(<line key={`l-${indices[i]}-${i}`} x1={p1[0]} y1={p1[1]} x2={p2[0]} y2={p2[1]} stroke="rgba(99, 102, 241, 0.4)" strokeWidth={1} />);
        }
      }
    };
    
    drawLoop(leftEye);
    drawLoop(rightEye);
    drawLoop(mouth);

    // Draw subset dots
    const dots = scaledPoints.filter((_, idx) => idx % 6 === 0).map((pt, idx) => (
      <circle 
        key={`pt-${idx}`} 
        cx={pt[0]} 
        cy={pt[1]} 
        r={1.5} 
        fill="#a5b4fc"
        className="animate-pulse"
        style={{ animationDelay: `${idx * 0.05}s` }}
      />
    ));

    return (
      <svg className="w-full h-full bg-zinc-950 border border-zinc-900 rounded-2xl" viewBox="0 0 240 240">
        {lines}
        {dots}
      </svg>
    );
  };

  return (
    <AuthShell
      title="Biometrics Diagnostics"
      subtitle="Face ID structural landmark cloud"
    >
      {loading ? (
        <div className="flex flex-col items-center justify-center p-8 text-zinc-500">
          <RefreshCw className="h-8 w-8 animate-spin text-indigo-500 mb-2" />
          <span className="text-xs">Loading face structure logs...</span>
        </div>
      ) : !diagnostics?.records || diagnostics.records.length === 0 ? (
        <div className="text-center p-6 space-y-4">
          <ShieldAlert className="h-12 w-12 text-destructive mx-auto" />
          <p className="text-xs text-zinc-400">No biometrics record registered for this account.</p>
          <Button onClick={() => navigate("/register-face")} className="w-full text-xs">
            Start Enrollment
          </Button>
        </div>
      ) : (
        <div className="space-y-6">
          
          {/* Angle Picker Tabs */}
          <div className="flex gap-1.5 p-1 bg-zinc-900/60 border border-zinc-800 rounded-xl overflow-x-auto">
            {diagnostics.records.map((r) => (
              <button
                key={r.angle}
                onClick={() => setSelectedAngle(r.angle)}
                className={`text-[10px] font-mono px-3 py-1.5 rounded-lg font-semibold uppercase tracking-wider transition-all duration-200 shrink-0 ${
                  selectedAngle === r.angle 
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/10" 
                    : "text-zinc-500 hover:text-zinc-300"
                }`}
              >
                {r.angle}
              </button>
            ))}
          </div>

          {/* Visualization Split (Image vs Landmark Mesh) */}
          <div className="grid grid-cols-2 gap-4">
            {/* 1. Aligned Crop */}
            <div className="space-y-1.5">
              <span className="text-[9px] font-mono uppercase tracking-widest text-zinc-500 block">Cropped Face</span>
              <div className="relative aspect-square w-full bg-zinc-950 border border-zinc-900 rounded-2xl overflow-hidden flex items-center justify-center">
                {activeRecord?.cropUrl ? (
                  <img 
                    src={getFullImageUrl(activeRecord.cropUrl)} 
                    alt={activeRecord.angle} 
                    className="w-full h-full object-cover scale-x-[-1]"
                  />
                ) : (
                  <span className="text-[10px] text-zinc-600">No crop URL</span>
                )}
              </div>
            </div>

            {/* 2. Vector Landmark Mesh */}
            <div className="space-y-1.5">
              <span className="text-[9px] font-mono uppercase tracking-widest text-zinc-500 block">Biometric Mesh</span>
              <div className="aspect-square w-full">
                {renderMesh(activeRecord?.landmarks)}
              </div>
            </div>
          </div>

          {/* Telemetry Statistics Card */}
          {activeRecord && (
            <div className="p-4 bg-zinc-900/20 border border-zinc-800 rounded-2xl space-y-3 font-mono text-[11px]">
              <div className="flex items-center gap-2 border-b border-zinc-800/80 pb-2">
                <Cpu className="h-4 w-4 text-indigo-400" />
                <span className="font-semibold text-zinc-200 uppercase text-xs tracking-wider">Spatial Telemetry</span>
              </div>
              
              <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-zinc-400">
                <div className="flex justify-between">
                  <span>head yaw:</span>
                  <span className="text-zinc-200">{activeRecord.pose?.yaw?.toFixed(1) || "0.0"}°</span>
                </div>
                <div className="flex justify-between">
                  <span>symmetry index:</span>
                  <span className="text-emerald-400">{(activeRecord.symmetryScore * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>head pitch:</span>
                  <span className="text-zinc-200">{activeRecord.pose?.pitch?.toFixed(1) || "0.0"}°</span>
                </div>
                <div className="flex justify-between">
                  <span>landmarks read:</span>
                  <span className="text-zinc-200">{activeRecord.landmarks?.length || 468} pts</span>
                </div>
                <div className="flex justify-between">
                  <span>head roll:</span>
                  <span className="text-zinc-200">{activeRecord.pose?.roll?.toFixed(1) || "0.0"}°</span>
                </div>
                <div className="flex justify-between">
                  <span>vector depth:</span>
                  <span className="text-zinc-200">512 dims</span>
                </div>
              </div>
            </div>
          )}

          <div className="text-center pt-2">
            <Link to="/face-enrollment" className="text-[11px] font-mono text-zinc-500 hover:text-zinc-300 uppercase tracking-widest">
              ← Return to Security Center
            </Link>
          </div>
        </div>
      )}
    </AuthShell>
  );
}
