import { useEffect, useRef, useState } from "react";
import { Camera, CameraOff, RefreshCw, CheckCircle2, ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";

export function FaceScanner({
  onFrameCaptured,
  activeChallenge = null,
  challengeProgress = 0,
  statusMessage = "Position your face in the circular frame",
  isProcessing = false,
  isSuccess = false,
  isError = false,
  errorMessage = "",
  autoCaptureInterval = 500, // ms
  maxFrames = 1,
  onCaptureComplete = null
}) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  
  const [streamActive, setStreamActive] = useState(false);
  const [permissionError, setPermissionError] = useState(null);
  const [capturedFrames, setCapturedFrames] = useState([]);
  
  const animationFrameId = useRef(null);
  const captureIntervalId = useRef(null);

  // 1. Initialize Webcam Stream
  const startCamera = async () => {
    setPermissionError(null);
    try {
      const constraints = {
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: "user"
        },
        audio: false
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setStreamActive(true);
      }
    } catch (err) {
      console.error("Webcam access error:", err);
      setPermissionError("Camera access denied. Please enable webcam permissions.");
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setStreamActive(false);
  };

  // Start camera on mount
  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
      if (captureIntervalId.current) clearInterval(captureIntervalId.current);
      if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current);
    };
  }, []);

  // 2. Premium Biometric Overlay Animation
  useEffect(() => {
    if (!streamActive) return;
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    
    let angle1 = 0;
    let angle2 = 0;
    
    const drawOverlay = () => {
      const width = canvas.width;
      const height = canvas.height;
      const cx = width / 2;
      const cy = height / 2;
      const radius = Math.min(cx, cy) - 20;
      
      ctx.clearRect(0, 0, width, height);
      
      // Draw Circular Crop Outline
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(63, 63, 70, 0.4)";
      ctx.lineWidth = 4;
      ctx.stroke();
      ctx.restore();
      
      // Biometric Scanning Ring 1 (Rotating dash stroke)
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(angle1);
      ctx.beginPath();
      ctx.arc(0, 0, radius + 5, 0, Math.PI * 2);
      ctx.strokeStyle = isSuccess 
        ? "#22c55e" 
        : isError 
        ? "#ef4444" 
        : isProcessing 
        ? "#eab308" 
        : "rgba(99, 102, 241, 0.85)"; // Indigo
      ctx.lineWidth = 2;
      ctx.setLineDash([15, 30, 40, 20]);
      ctx.stroke();
      ctx.restore();
      
      // Biometric Scanning Ring 2 (Reversed direction)
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(-angle2);
      ctx.beginPath();
      ctx.arc(0, 0, radius - 5, 0, Math.PI * 2);
      ctx.strokeStyle = isSuccess 
        ? "#10b981" 
        : isError 
        ? "#f87171" 
        : isProcessing 
        ? "#facc15" 
        : "rgba(6, 182, 212, 0.6)"; // Cyan
      ctx.lineWidth = 1.5;
      ctx.setLineDash([5, 10, 15, 20]);
      ctx.stroke();
      ctx.restore();

      // Sweeping Scanning Radar Matrix (Grid line)
      if (isProcessing && !isSuccess && !isError) {
        ctx.save();
        const scanY = cy + Math.sin(angle1 * 2) * radius;
        ctx.beginPath();
        ctx.rect(cx - radius, cx - radius, radius * 2, radius * 2);
        ctx.clip();
        
        const gradient = ctx.createLinearGradient(0, scanY - 20, 0, scanY + 20);
        gradient.addColorStop(0, "rgba(99, 102, 241, 0.0)");
        gradient.addColorStop(0.5, "rgba(99, 102, 241, 0.4)");
        gradient.addColorStop(1, "rgba(99, 102, 241, 0.0)");
        
        ctx.fillStyle = gradient;
        ctx.fillRect(cx - radius, scanY - 20, radius * 2, 40);
        ctx.restore();
      }
      
      // Angle updates
      angle1 += 0.015;
      angle2 += 0.025;
      
      animationFrameId.current = requestAnimationFrame(drawOverlay);
    };
    
    drawOverlay();
    
    return () => {
      if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current);
    };
  }, [streamActive, isProcessing, isSuccess, isError]);

  // 3. Automate Frame Capture Sequences
  useEffect(() => {
    if (!streamActive || isProcessing || isSuccess || isError) {
      if (captureIntervalId.current) {
        clearInterval(captureIntervalId.current);
        captureIntervalId.current = null;
      }
      return;
    }

    setCapturedFrames([]);

    // Clear previous interval if any
    if (captureIntervalId.current) clearInterval(captureIntervalId.current);

    captureIntervalId.current = setInterval(() => {
      const canvas = document.createElement("canvas");
      const video = videoRef.current;
      if (!video) return;
      
      canvas.width = 300; // Optimal size for embedding analysis
      canvas.height = 300;
      const ctx = canvas.getContext("2d");
      
      // Capture a square crop in the center of the video frame
      const minDim = Math.min(video.videoWidth, video.videoHeight);
      const sx = (video.videoWidth - minDim) / 2;
      const sy = (video.videoHeight - minDim) / 2;
      
      ctx.drawImage(video, sx, sy, minDim, minDim, 0, 0, 300, 300);
      const base64Frame = canvas.toDataURL("image/jpeg", 0.9);
      
      // Send individual frame up for active analysis
      if (onFrameCaptured) {
        onFrameCaptured(base64Frame);
      }

      setCapturedFrames(prev => {
        const next = [...prev, base64Frame];
        if (onCaptureComplete && next.length >= maxFrames) {
          clearInterval(captureIntervalId.current);
          onCaptureComplete(next);
        }
        return next;
      });

    }, autoCaptureInterval);

    return () => {
      if (captureIntervalId.current) clearInterval(captureIntervalId.current);
    };
  }, [streamActive, maxFrames, isProcessing, isSuccess, isError, activeChallenge]);

  return (
    <div className="flex flex-col items-center justify-center space-y-6" ref={containerRef}>
      {/* Circle Camera Window */}
      <div className="relative h-[280px] w-[280px] overflow-hidden rounded-full border-4 border-zinc-900 bg-zinc-950 shadow-[0_0_50px_rgba(99,102,241,0.15)] ring-4 ring-offset-4 ring-offset-black ring-zinc-800 transition-all duration-300">
        
        {/* HTML5 Video Element */}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="h-full w-full object-cover scale-x-[-1]"
          style={{ display: streamActive ? "block" : "none" }}
        />

        {/* Canvas Biometric Grid/Target Overlay */}
        <canvas
          ref={canvasRef}
          width={280}
          height={280}
          className="absolute inset-0 pointer-events-none z-10"
        />

        {/* Camera Off / Fallback States */}
        {!streamActive && !permissionError && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-zinc-500">
            <Camera className="h-10 w-10 animate-pulse text-indigo-500" />
            <span className="mt-2 text-xs">Connecting camera...</span>
          </div>
        )}

        {permissionError && (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center text-zinc-400">
            <CameraOff className="h-10 w-10 text-destructive mb-2" />
            <span className="text-xs font-semibold text-destructive">Webcam Required</span>
            <p className="mt-1 text-[10px] text-zinc-500 leading-normal">{permissionError}</p>
            <Button size="sm" variant="outline" className="mt-3 text-[10px] h-7 px-3" onClick={startCamera}>
              <RefreshCw className="mr-1 h-3 w-3" /> Retry
            </Button>
          </div>
        )}

        {/* Success Checkmark overlay */}
        {isSuccess && (
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center z-20 animate-fade-in">
            <CheckCircle2 className="h-14 w-14 text-emerald-500 animate-scale-up" />
            <span className="mt-3 text-xs font-medium text-emerald-400 uppercase tracking-widest font-mono">Biometrics Verified</span>
          </div>
        )}

        {/* Error overlay */}
        {isError && (
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center z-20 animate-fade-in">
            <ShieldAlert className="h-14 w-14 text-destructive animate-bounce" />
            <span className="mt-3 text-xs font-semibold text-destructive uppercase tracking-widest font-mono">Scan Failed</span>
            <p className="mt-2 text-[11px] text-zinc-400 leading-normal">{errorMessage}</p>
            <Button size="sm" variant="outline" className="mt-3 text-[10px] h-7 px-3 bg-zinc-900 border-zinc-800" onClick={() => {
              startCamera();
              if (onCaptureComplete) setCapturedFrames([]);
            }}>
              <RefreshCw className="mr-1 h-3 w-3" /> Scan Again
            </Button>
          </div>
        )}
      </div>

      {/* Dynamic Status / Liveness Commands Panel */}
      <div className="w-full max-w-sm text-center px-4">
        {activeChallenge ? (
          <div className="bg-indigo-950/30 border border-indigo-500/20 rounded-xl p-4 shadow-[0_4px_20px_rgba(99,102,241,0.05)] backdrop-blur-md animate-scale-up">
            <span className="text-[10px] font-semibold text-indigo-400 uppercase tracking-widest font-mono">Active Challenge</span>
            <h4 className="mt-1 text-sm font-semibold text-zinc-100">{statusMessage}</h4>
            
            {/* Liveness meter bar */}
            <div className="mt-3 h-1.5 w-full bg-zinc-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-indigo-500 transition-all duration-300 rounded-full shadow-[0_0_8px_rgba(99,102,241,0.8)]"
                style={{ width: `${Math.min(100, challengeProgress)}%` }}
              />
            </div>
            <span className="mt-1 block text-[10px] font-mono text-zinc-500">Processing frames... ({capturedFrames.length}/{maxFrames})</span>
          </div>
        ) : (
          <p className={`text-xs ${isProcessing ? "text-indigo-400 font-medium animate-pulse" : "text-zinc-400"}`}>
            {statusMessage}
          </p>
        )}
      </div>
    </div>
  );
}
