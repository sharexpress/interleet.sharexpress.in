import { useState, useEffect, useRef } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { 
  Dialog, DialogContent, DialogHeader, DialogTitle, 
  DialogDescription, DialogFooter, DialogClose 
} from "@/components/ui/dialog";
import { 
  Mic, MicOff, Volume2, Upload, FileText, CheckCircle, 
  AlertTriangle, ArrowLeft, ArrowRight, Play, Sparkles, Check,
  Clock, DollarSign, Briefcase, RefreshCw, X, ShieldCheck
} from "lucide-react";
import { toast } from "sonner";
import { API } from "@/api/api";

const ROLE_JDS = {
  "Senior Backend Engineer": {
    "title": "Senior Backend Engineer",
    "overview": "Build resilient, distributed systems to support high-throughput services. Optimize backend flows, design scalable relational and NoSQL storage layers, and lead microservice migrations.",
    "responsibilities": [
      "Design, implement, and maintain microservice APIs using FastAPI/Python.",
      "Build robust caching layers and message queuing pipelines for event-driven logic.",
      "Refactor bottlenecked database queries and implement read-replicas/sharding.",
      "Set up health-check systems and end-to-end trace logging."
    ],
    "requirements": [
      "Strong proficiency in Python (FastAPI/Django), Go, or Java.",
      "Extensive experience with SQL (PostgreSQL/MySQL) and NoSQL (MongoDB, Redis).",
      "Experience building event pipelines using Kafka, RabbitMQ, or AWS SQS.",
      "Mastery of asynchronous programming and concurrency control."
    ],
    "focus_areas": [
      "System scale and database performance",
      "Concurrency and thread safety in Python/Go",
      "Caching policies and data eviction strategies"
    ],
    "technologies": ["Python", "FastAPI", "PostgreSQL", "MongoDB", "Redis", "Docker", "RabbitMQ"],
    "level": "L5 / Senior Engineer",
    "salary": "$140,000 - $180,000"
  },
  "Frontend Architect": {
    "title": "Frontend Architect",
    "overview": "Lead the design, scaffolding, and performance tuning of modern frontend web applications. Build reusable component libraries, architect global state strategies, and ensure optimal web vitals.",
    "responsibilities": [
      "Architect micro-frontend and multi-page monorepo systems.",
      "Optimize core web vitals, bundle size, caching, and asset pipelines.",
      "Standardize design systems and style tokens for accessibility (WCAG 2.1 AA).",
      "Standardize client-side telemetry, error logging, and user session monitoring."
    ],
    "requirements": [
      "Master of React, TypeScript, and ecosystem tooling (Webpack, Vite, Turborepo).",
      "Expertise in state managers (Redux Toolkit, Zustand, Recoil).",
      "Deep understanding of CSS layout models, preprocessors, and utility styling.",
      "Knowledge of server-side rendering (SSR), hydration, and edge-rendering architectures."
    ],
    "focus_areas": [
      "Component modularity and state lifecycle",
      "Core Web Vitals and performance budgets",
      "Responsive styles and cross-browser consistency"
    ],
    "technologies": ["React", "TypeScript", "Next.js", "Redux", "Tailwind CSS", "Vite", "Jest"],
    "level": "L6 / Staff Architect",
    "salary": "$160,000 - $210,000"
  },
  "System Design (L5)": {
    "title": "System Design (L5)",
    "overview": "Architect high-level distributed systems under extreme scale constraints. Establish data routing, high availability systems, failover mechanisms, and multi-region deployment blueprints.",
    "responsibilities": [
      "Propose scalable architectural diagrams resolving latency bottlenecks.",
      "Evaluate consistency trade-offs (CAP theorem) in distributed datastores.",
      "Implement rate limiters, API gateways, load balancers, and CDN networks.",
      "Architect failover topologies, write-ahead-logging, and split-brain resolution."
    ],
    "requirements": [
      "Proven experience designing platforms handling >10k requests per second.",
      "Mastery of load balancing algorithms, HTTP/2, gRPC, and WebSockets.",
      "Practical knowledge of sharding, hashing rings, and partition keys.",
      "Experience with distributed transaction patterns (Sagas, 2PC)."
    ],
    "focus_areas": [
      "System scalability, redundancy, and CAP tradeoffs",
      "Data routing, hashing, and load balancing",
      "Resilience policies (circuit breakers, retries)"
    ],
    "technologies": ["NGINX", "HAProxy", "gRPC", "Cassandra", "DynamoDB", "Redis", "AWS"],
    "level": "L5 / Senior Architect",
    "salary": "$150,000 - $190,000"
  },
  "DevOps Lead": {
    "title": "DevOps Lead",
    "overview": "Own the infrastructure, continuous integration pipelines, container configurations, and active monitoring frameworks of cloud-based platforms. Keep system availability >99.99%.",
    "responsibilities": [
      "Construct high-velocity CI/CD workflows and automated test runner integrations.",
      "Manage and scale Kubernetes clusters, ingress controllers, and service meshes.",
      "Automate infrastructure provisioning with declarative IaC state definitions.",
      "Configure telemetry dashboards, alert rules, and log collection daemons."
    ],
    "requirements": [
      "Deep familiarity with AWS, GCP, or Azure services.",
      "Mastery of Terraform, Helm, and Kubernetes administration.",
      "Experience with monitoring software (Prometheus, Grafana, ELK, Datadog).",
      "Solid knowledge of containerization (Docker) and networking topologies (VPCs, DNS, VPNs)."
    ],
    "focus_areas": [
      "Infrastructure orchestration and Terraform states",
      "Kubernetes resource quotas and ingress networks",
      "Zero-downtime rolling updates"
    ],
    "technologies": ["Kubernetes", "Docker", "Terraform", "GitLab CI", "Prometheus", "Grafana", "AWS"],
    "level": "L5 / Lead DevOps",
    "salary": "$135,000 - $175,000"
  },
  "API Design": {
    "title": "API Design",
    "overview": "Design and enforce standard contracts, request/response models, authorization rules, and lifecycle versioning rules for developer-facing APIs.",
    "responsibilities": [
      "Define clean RESTful and GraphQL endpoints using OpenAPI/Swagger schemas.",
      "Enforce security paradigms including OAuth2, JWT verification, and scope validation.",
      "Formulate version deprecation policies and backward-compatible schemas.",
      "Design robust batch execution endpoints and webhooks."
    ],
    "requirements": [
      "Expertise in REST, GraphQL, gRPC design paradigms.",
      "Experience writing clean OpenAPI specifications.",
      "Mastery of token-based authentication and rate limiting configurations.",
      "Experience building SDK libraries and developer portals."
    ],
    "focus_areas": [
      "OpenAPI definition standards and schemas",
      "Authentication protocols and API security profiles",
      "API caching policies and payload sizing"
    ],
    "technologies": ["OpenAPI", "GraphQL", "OAuth2", "JWT", "Kong Gateway", "Swagger"],
    "level": "L4 / Senior API Specialist",
    "salary": "$125,000 - $165,000"
  },
  "Full-Stack Generalist": {
    "title": "Full-Stack Generalist",
    "overview": "Build features end-to-end by stitching modern user interfaces with robust database services. Deliver feature requests quickly with an emphasis on customer-centric design and fast execution.",
    "responsibilities": [
      "Develop interactive UI views and integrate them with REST/GraphQL endpoints.",
      "Write clean server-side controllers, models, and data migrations.",
      "Troubleshoot bugs across frontend browsers, databases, and microservices.",
      "Maintain and extend unit test coverage for all code paths."
    ],
    "requirements": [
      "Professional experience using both frontend frameworks (React/Vue) and backend runtimes (Node, Python).",
      "Comfortable working with SQL database integrations and object-relational mapping (ORMs).",
      "Fast learner capable of pivoting across multiple language codebases.",
      "Understanding of Git workflows, code reviews, and basic server configurations."
    ],
    "focus_areas": [
      "Full-stack integration patterns",
      "Database query execution and ORM optimizations",
      "Clean code and automated test coverage"
    ],
    "technologies": ["React", "Node.js", "Express", "PostgreSQL", "Prisma", "Git", "Docker"],
    "level": "L4 / Senior Developer",
    "salary": "$120,000 - $160,000"
  }
};

function InterviewSetupPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const roleParam = searchParams.get("role") || "Senior Backend Engineer";
  const difficulty = searchParams.get("difficulty") || "Intermediate";

  // Get matching Job Description locally
  let jdData = ROLE_JDS[roleParam];
  if (!jdData) {
    // Fallback fuzzy match
    const matchedKey = Object.keys(ROLE_JDS).find(
      (k) => k.toLowerCase().includes(roleParam.toLowerCase()) || roleParam.toLowerCase().includes(k.toLowerCase())
    );
    jdData = ROLE_JDS[matchedKey || "Senior Backend Engineer"];
  }

  // Audio / Mic states (Modal states)
  const [isOpenDiagnostics, setIsOpenDiagnostics] = useState(false);
  const [micPermission, setMicPermission] = useState("prompt"); // prompt, granted, denied
  const [volumeLevel, setVolumeLevel] = useState(0);
  const [isSpeakerPlaying, setIsSpeakerPlaying] = useState(false);
  const [speakerVerified, setSpeakerVerified] = useState(false);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Resume states
  const [useResume, setUseResume] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isParsing, setIsParsing] = useState(false);
  const [parsedJD, setParsedJD] = useState(null);
  const [resumeUploaded, setResumeUploaded] = useState(false);

  // Handle microphone permissions and audio level analysis
  const requestMicPermission = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      setMicPermission("granted");
      toast.success("Microphone connected!");

      // Set up Audio Context for live volume visualizer
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      const audioContext = new AudioContext();
      audioContextRef.current = audioContext;

      const source = audioContext.createMediaStreamSource(stream);
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      analyserRef.current = analyser;

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateVolume = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);
        
        let total = 0;
        for (let i = 0; i < bufferLength; i++) {
          total += dataArray[i];
        }
        const average = total / bufferLength;
        const mapped = Math.min(Math.round((average / 80) * 100), 100);
        setVolumeLevel(mapped);
        animationFrameRef.current = requestAnimationFrame(updateVolume);
      };

      updateVolume();
    } catch (err) {
      console.error("Error accessing microphone:", err);
      setMicPermission("denied");
      toast.error("Could not access microphone. Please check browser privacy permissions.");
    }
  };

  // Stop microphone stream and animation
  const stopMic = () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    setVolumeLevel(0);
  };

  const handleOpenDiagnostics = () => {
    setIsOpenDiagnostics(true);
  };

  const handleCloseDiagnostics = () => {
    stopMic();
    setIsOpenDiagnostics(false);
  };

  // Speaker check sound play
  const playTestSound = () => {
    if (isSpeakerPlaying) return;
    setIsSpeakerPlaying(true);

    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioContext();
      const oscillator = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();

      oscillator.type = "sine";
      oscillator.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5 note
      gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);

      // Smooth fade out
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1.2);

      oscillator.connect(gainNode);
      gainNode.connect(audioCtx.destination);

      oscillator.start();
      oscillator.stop(audioCtx.currentTime + 1.2);

      setTimeout(() => {
        setIsSpeakerPlaying(false);
        setSpeakerVerified(true);
        toast.success("Test chime played successfully!");
      }, 1200);
    } catch (e) {
      console.error(e);
      setIsSpeakerPlaying(false);
    }
  };

  // Resume File handling
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== "application/pdf") {
        toast.error("Only PDF files are supported currently.");
        return;
      }
      if (file.size > 5 * 1024 * 1024) {
        toast.error("File size exceeds 5MB limit.");
        return;
      }
      setSelectedFile(file);
      setResumeUploaded(false);
    }
  };

  const handleUploadResume = async () => {
    if (!selectedFile) return;
    setIsParsing(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await API.post("/resume/parse", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = response.data;
      const resumeData = data?.parsed_resume || {};
      const mockTest = data?.mock_test || {};

      setResumeUploaded(true);
      setParsedJD({
        skills: resumeData.skills?.slice(0, 8) || [],
        technologies: resumeData.technologies?.slice(0, 6) || [],
        summary: resumeData.summary || "",
        topics: mockTest.topics || [],
        cloudinaryUrl: data?.cloudinary?.secure_url || "",
      });

      toast.success("Resume parsed and interview tailored!");
    } catch (err) {
      console.error("Resume parsing error:", err);
      const status = err?.response?.status;
      if (status === 422) {
        toast.error("Only PDF files are supported.");
      } else if (status === 413) {
        toast.error("File too large — max 5 MB.");
      } else {
        toast.error("Resume parsing failed. Using standard syllabus.");
      }
      // Still mark as "uploaded" so user can proceed
      setResumeUploaded(true);
      setParsedJD({ skills: [], technologies: [], summary: "", topics: [], cloudinaryUrl: "" });
    } finally {
      setIsParsing(false);
    }
  };

  const startInterview = () => {
    stopMic();
    let finalJD = "";
    if (useResume && resumeUploaded && parsedJD) {
      const topicsStr = parsedJD.topics?.length
        ? `Focus topics: ${parsedJD.topics.join(", ")}.`
        : "";
      const skillsStr = parsedJD.skills?.length
        ? `Key skills: ${parsedJD.skills.join(", ")}.`
        : "";
      finalJD = `${jdData.overview} ${topicsStr} ${skillsStr}`.trim();
    } else {
      finalJD = jdData.overview;
    }

    const path = `/app/interviews/live?role=${encodeURIComponent(roleParam)}&difficulty=${encodeURIComponent(difficulty)}&jd=${encodeURIComponent(finalJD)}`;
    navigate(path);
  };


  return (
    <AppShell>
      {/* Top Breadcrumb Bar */}
      <div className="flex items-center gap-3 border-b border-border px-4 py-3 md:px-8 bg-card/10">
        <Button asChild variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-foreground">
          <Link to="/app/interviews"><ArrowLeft className="h-4 w-4" /></Link>
        </Button>
        <div className="flex items-center gap-2 text-xs">
          <Link to="/app/interviews" className="text-muted-foreground hover:text-foreground">Mock Interviews</Link>
          <span className="text-zinc-600">/</span>
          <span className="text-zinc-400">{jdData.title}</span>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 py-6 md:px-8">
        
        {/* Page Header */}
        <PageHeader
          title={jdData.title}
          description="Read the detailed role specification. Prepare your speech and optionally upload a resume context before connecting."
          badge={`${difficulty} level`}
        />

        {/* Double Column Grid: Matches challenge detail structure */}
        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          
          {/* LEFT COLUMN (2/3 Width): Job Description details */}
          <div className="space-y-6 lg:col-span-2">
            
            <Card className="border-border bg-card p-6 md:p-8">
              
              {/* Role Title and Header */}
              <div className="border-b border-border pb-5">
                <Badge className="bg-primary/10 text-primary border-primary/20 font-semibold mb-2">
                  JOB SPECIFICATION
                </Badge>
                <h2 className="text-2xl font-bold text-white tracking-tight">{jdData.title}</h2>
                <div className="mt-2 flex flex-wrap gap-4 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5">
                    <Briefcase className="h-3.5 w-3.5 text-zinc-500" /> {jdData.level}
                  </span>
                  <span className="flex items-center gap-1.5">
                    <DollarSign className="h-3.5 w-3.5 text-zinc-500" /> {jdData.salary} / year
                  </span>
                  <span className="flex items-center gap-1.5">
                    <Clock className="h-3.5 w-3.5 text-zinc-500" /> 45 Minute Assessment
                  </span>
                </div>
              </div>

              {/* JD Body Details */}
              <div className="prose prose-invert mt-6 max-w-none text-sm text-foreground/80 space-y-6">
                
                {/* Overview */}
                <div className="space-y-2">
                  <h3 className="text-base font-semibold text-white">Role Overview</h3>
                  <p className="leading-relaxed text-zinc-300">
                    {jdData.overview}
                  </p>
                </div>

                {/* Tailored overlay notification */}
                {useResume && resumeUploaded && parsedJD && (
                  <Alert className="border-success/30 bg-success/5 text-success">
                    <Sparkles className="h-4 w-4 text-success" />
                    <AlertTitle className="font-semibold text-success">Resume Customization Active</AlertTitle>
                    <AlertDescription className="text-zinc-300 text-xs mt-1">
                      {parsedJD.topics?.length > 0 ? (
                        <>Interview will focus on: <strong>{parsedJD.topics.join(", ")}</strong>.</>
                      ) : (
                        "AI will adapt questions based on your resume."
                      )}
                      {parsedJD.summary && (
                        <p className="mt-2 text-zinc-400 italic line-clamp-2">{parsedJD.summary}</p>
                      )}
                    </AlertDescription>
                  </Alert>
                )}

                {/* Responsibilities */}
                <div className="space-y-2 pt-2">
                  <h3 className="text-base font-semibold text-white">Responsibilities</h3>
                  <ul className="list-disc list-inside space-y-1.5 text-zinc-300 pl-1">
                    {jdData.responsibilities.map((resp, i) => (
                      <li key={i}>{resp}</li>
                    ))}
                  </ul>
                </div>

                {/* Technical Requirements */}
                <div className="space-y-2 pt-2">
                  <h3 className="text-base font-semibold text-white">Requirements</h3>
                  <ul className="list-disc list-inside space-y-1.5 text-zinc-300 pl-1">
                    {jdData.requirements.map((req, i) => (
                      <li key={i}>{req}</li>
                    ))}
                  </ul>
                </div>

                {/* Interview Focus Areas */}
                <div className="space-y-2 pt-2">
                  <h3 className="text-base font-semibold text-white">Interview Focus Areas</h3>
                  <p className="text-xs text-zinc-400 mb-2">
                    Expect heavy probing on these topics during the active voice simulator:
                  </p>
                  <ul className="list-disc list-inside space-y-1.5 text-zinc-300 pl-1">
                    {jdData.focus_areas.map((area, i) => (
                      <li key={i}>{area}</li>
                    ))}
                  </ul>
                </div>

              </div>

            </Card>
          </div>

          {/* RIGHT COLUMN (1/3 Width): Sidebar widgets */}
          <div className="space-y-6">
            
            {/* Tech Stack card */}
            <Card className="border-border bg-card p-5">
              <h3 className="text-sm font-semibold text-white">Key Technologies</h3>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {jdData.technologies.map((tech) => (
                  <Badge key={tech} variant="outline" className="font-mono text-[10px] bg-zinc-950/60 border-zinc-800 text-zinc-300">
                    {tech}
                  </Badge>
                ))}
              </div>
            </Card>

            {/* Resume tailoring selector */}
            <Card className="border-border bg-card p-5">
              <h3 className="text-sm font-semibold text-white">Tailor Syllabus</h3>
              <p className="mt-1.5 text-xs text-muted-foreground leading-relaxed">
                Provide resume context to align the AI's grading parameters and questions to your past work.
              </p>
              
              {/* Option toggle tab */}
              <div className="mt-4 flex rounded-md border border-zinc-800 p-1 bg-zinc-950/60">
                <button
                  type="button"
                  onClick={() => setUseResume(false)}
                  className={`flex-1 rounded-sm py-1 text-center text-[11px] font-medium transition-all ${
                    !useResume 
                      ? "bg-zinc-900 text-white shadow-sm" 
                      : "text-zinc-400 hover:text-zinc-200"
                  }`}
                >
                  Standard Syllabus
                </button>
                <button
                  type="button"
                  onClick={() => setUseResume(true)}
                  className={`flex-1 rounded-sm py-1 text-center text-[11px] font-medium transition-all ${
                    useResume 
                      ? "bg-zinc-900 text-white shadow-sm" 
                      : "text-zinc-400 hover:text-zinc-200"
                  }`}
                >
                  Custom Resume
                </button>
              </div>

              {/* Upload controls */}
              {useResume && (
                <div className="mt-4 space-y-3">
                  <div className="group relative flex flex-col items-center justify-center rounded border border-dashed border-zinc-800 bg-zinc-950/40 p-4 text-center hover:border-primary/40 transition-colors">
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileChange}
                      className="absolute inset-0 cursor-pointer opacity-0"
                    />
                    <Upload className="mb-1.5 h-6 w-6 text-zinc-500 group-hover:text-primary transition-colors" />
                    <p className="text-[10px] font-medium text-zinc-300 truncate max-w-full px-1">
                      {selectedFile ? selectedFile.name : "Select PDF resume"}
                    </p>
                    <p className="text-[9px] text-zinc-500">PDF up to 5MB</p>
                  </div>

                  {selectedFile && !resumeUploaded && (
                    <Button
                      onClick={handleUploadResume}
                      disabled={isParsing}
                      size="sm"
                      className="w-full bg-orange-600 hover:bg-orange-500 text-white font-medium text-xs"
                    >
                      {isParsing ? (
                        <>
                          <div className="mr-1.5 h-3 w-3 animate-spin rounded-full border border-zinc-700 border-t-white" />
                          Parsing...
                        </>
                      ) : (
                        <>
                          <Sparkles className="mr-1.5 h-3.5 w-3.5" />
                          Apply Context
                        </>
                      )}
                    </Button>
                  )}

                  {resumeUploaded && (
                    <div className="flex items-center gap-1.5 text-[11px] font-semibold text-success bg-success/5 border border-success/20 p-2 rounded">
                      <CheckCircle className="h-3.5 w-3.5" /> Context tailored and loaded.
                    </div>
                  )}
                </div>
              )}
            </Card>

            {/* Launch CTA */}
            <Card className="border-border bg-card p-5 space-y-4">
              <h3 className="text-sm font-semibold text-white">Diagnostics Checklist</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Before beginning the conversation, we need to calibrate your speaker output and confirm browser microphone permissions.
              </p>
              
              <Button
                onClick={handleOpenDiagnostics}
                disabled={useResume && !resumeUploaded}
                className="w-full bg-primary hover:bg-orange-600 text-white font-semibold shadow-[0_0_15px_rgba(255,101,0,0.15)] hover:shadow-[0_0_20px_rgba(255,101,0,0.35)] transition-all"
              >
                Launch Device Check <ArrowRight className="ml-1.5 h-4 w-4" />
              </Button>
            </Card>

          </div>

        </div>

      </div>

      {/* ========================================== */}
      {/* RADIX UI DIALOG MODAL DIAGNOSTICS POPUP     */}
      {/* ========================================== */}
      <Dialog open={isOpenDiagnostics} onOpenChange={handleCloseDiagnostics}>
        <DialogContent className="border border-zinc-800 bg-[#0E0E0E] text-white max-w-md p-6">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-base font-semibold text-white">
              <ShieldCheck className="h-5 w-5 text-primary" /> Audio & Peripherals Check
            </DialogTitle>
            <DialogDescription className="text-zinc-400 text-xs">
              Verify your devices to ensure a seamless voice assessment session with the AI.
            </DialogDescription>
          </DialogHeader>

          <div className="my-4 space-y-5">
            {/* Mic verification block */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-zinc-300 uppercase tracking-wider">1. Microphone Input</span>
                {micPermission === "granted" ? (
                  <Badge className="bg-success/20 text-success border-success/30 text-[10px]">Active</Badge>
                ) : micPermission === "denied" ? (
                  <Badge className="bg-destructive/20 text-destructive border-destructive/30 text-[10px]">Access Denied</Badge>
                ) : (
                  <Badge variant="outline" className="text-zinc-500 text-[10px]">Authorization Required</Badge>
                )}
              </div>

              {micPermission !== "granted" ? (
                <div className="space-y-2">
                  {micPermission === "denied" && (
                    <Alert variant="destructive" className="border-destructive/30 bg-destructive/10 p-2.5 flex items-start gap-2">
                      <AlertTriangle className="h-4 w-4 text-destructive shrink-0 mt-0.5" />
                      <div>
                        <AlertTitle className="text-xs font-bold">Mic Disabled</AlertTitle>
                        <AlertDescription className="text-[10px] text-zinc-300">
                          Please unlock mic access in your browser settings bar.
                        </AlertDescription>
                      </div>
                    </Alert>
                  )}
                  <Button 
                    onClick={requestMicPermission}
                    className="w-full bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 text-white font-medium text-xs py-2 h-9"
                  >
                    <Mic className="mr-1.5 h-3.5 w-3.5 text-primary" /> Connect Microphone
                  </Button>
                </div>
              ) : (
                <div className="space-y-2 rounded border border-zinc-800 bg-zinc-950/60 p-3">
                  <div className="flex items-center justify-between text-[10px] text-zinc-400">
                    <span className="flex items-center gap-1"><Check className="h-3 w-3 text-success" /> Mic connected</span>
                    <span>Speak to verify level</span>
                  </div>
                  <div className="space-y-1">
                    <Progress value={volumeLevel} className="h-1.5 bg-zinc-900" indicatorClassName="bg-primary shadow-[0_0_8px_rgba(255,101,0,0.6)]" />
                  </div>
                </div>
              )}
            </div>

            {/* Speaker verification block */}
            <div className="space-y-3 border-t border-zinc-800/60 pt-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-zinc-300 uppercase tracking-wider">2. Speaker Output</span>
                {speakerVerified && (
                  <Badge className="bg-success/20 text-success border-success/30 text-[10px]">Verified</Badge>
                )}
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                Play a brief sine wave chime to confirm you can hear the AI's prompts clearly.
              </p>
              <Button
                onClick={playTestSound}
                disabled={isSpeakerPlaying}
                variant="outline"
                className="w-full border-zinc-800 bg-zinc-950 hover:bg-zinc-900 text-zinc-300 text-xs py-2 h-9"
              >
                <Volume2 className={`mr-1.5 h-3.5 w-3.5 text-primary ${isSpeakerPlaying ? "animate-bounce" : ""}`} />
                {isSpeakerPlaying ? "Playing chime..." : speakerVerified ? "Verify Speakers Again" : "Verify Speakers"}
              </Button>
            </div>
          </div>

          <DialogFooter className="mt-6 flex gap-2 sm:gap-0 sm:justify-between border-t border-zinc-800/60 pt-4">
            <DialogClose asChild>
              <Button 
                onClick={handleCloseDiagnostics}
                variant="ghost" 
                className="text-zinc-400 hover:text-white hover:bg-zinc-900 text-xs"
              >
                Cancel
              </Button>
            </DialogClose>
            
            <Button
              onClick={startInterview}
              disabled={micPermission !== "granted" || !speakerVerified}
              className="bg-primary hover:bg-orange-600 text-white font-medium text-xs px-6"
            >
              Enter Interview Arena <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppShell>
  );
}

export default InterviewSetupPage;
