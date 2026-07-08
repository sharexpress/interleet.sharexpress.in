import { memo } from "react";
import {
  RotateCw,
  Lock,
  Globe,
  Loader2,
  X,
  Check,
  CheckCircle2,
  AlertCircle
} from "lucide-react";

// ─── Program Output Specs ───────────────────────────────────────────────────

function getProgramOutput(slug) {
  switch (slug) {
    case "configure-nginx-proxy":
      return {
        log: "Workspace Ready\n✓\nConfiguration Loaded\n✓\nStarting Backend\n✓\nReloading Nginx\n✓\nRunning Health Checks\n✓\nValidation Passed\n\nAll HTTP checks passed successfully.",
        stats: [
          { label: "Nginx", value: "Running", tone: "text-success" },
          { label: "Backend", value: "Running", tone: "text-success" },
          { label: "Reverse Proxy", value: "Configured", tone: "text-success" },
        ],
      };
    case "orchestrate-redis-node":
      return {
        log: "Workspace Ready\n✓\nDocker Compose File Loaded\n✓\nStarting Containers\n✓\nWaiting for redis-db\n✓\nWaiting for node-api\n✓\nHTTP Check (Port 8080)\n✓\nValidation Passed",
        stats: [
          { label: "Redis DB", value: "Running", tone: "text-success" },
          { label: "Node API", value: "Running", tone: "text-success" },
          { label: "Orchestration", value: "OK", tone: "text-success" },
        ],
      };
    case "build-a-rate-limiter":
      return {
        log: "> TokenBucket(3, 1)\n> b.allow() → true\n> b.allow() → true\n> b.allow() → true\n> b.allow() → false\n[waiting 1000ms...]\n> b.allow() → true\n\n✓ Run finished in 1.04s",
        stats: [
          { label: "Calls", value: "5" },
          { label: "Allowed", value: "4", tone: "text-success" },
          { label: "Denied", value: "1", tone: "text-destructive" },
          { label: "Avg ms", value: "0.21" },
        ],
      };
    case "feature-flag-service":
      return {
        log: '> flags.isOn("new-checkout", { userId: "u_42" }) → true\n> flags.isOn("dark-mode", { userId: "u_7" })       → false\n> flags.rollout("beta-search", 25%)                → ok\n> 1,204 evaluations in 980ms\n\n✓ Run finished in 0.98s',
        stats: [
          { label: "Evals", value: "1204" },
          { label: "Cache hit", value: "94%", tone: "text-success" },
          { label: "p95 ms", value: "1.8" },
          { label: "Errors", value: "0", tone: "text-success" },
        ],
      };
    default:
      return {
        log: `> running ${slug}...\n✓ build ok\n✓ tests passed\n✓ Run finished in 1.21s`,
        stats: [
          { label: "Status", value: "OK", tone: "text-success" },
          { label: "Duration", value: "1.21s" },
          { label: "Warnings", value: "0" },
          { label: "Errors", value: "0", tone: "text-success" },
        ],
      };
  }
}

function getFrontendSrcDoc(slug, title) {
  const base = `<style>:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Inter",sans-serif;color:#0a0a0a;background:#fff;padding:16px}h1,h2,h3{margin:0 0 12px}button{font:inherit;cursor:pointer}</style>`;
  switch (slug) {
    case "responsive-data-table":
      return `<!doctype html><html><head>${base}<style>.wrap{max-width:720px;margin:0 auto}.toolbar{display:flex;gap:8px;margin-bottom:12px}input{flex:1;padding:8px 10px;border:1px solid #e5e5e5;border-radius:8px;font:inherit}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #eee}th{background:#fafafa}tr:hover td{background:#fafafa}.pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px}.ok{background:#dcfce7;color:#166534}.warn{background:#fef9c3;color:#854d0e}.err{background:#fee2e2;color:#991b1b}</style></head><body><div class="wrap"><h2>Users</h2><div class="toolbar"><input id="q" placeholder="Search..."/></div><table><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th></tr></thead><tbody id="b"></tbody></table></div><script>const rows=[{name:"Ada Lovelace",email:"ada@interleet.dev",role:"Admin",status:"ok"},{name:"Linus Torvalds",email:"linus@interleet.dev",role:"Maintainer",status:"ok"},{name:"Grace Hopper",email:"grace@interleet.dev",role:"Member",status:"warn"},{name:"Alan Turing",email:"alan@interleet.dev",role:"Member",status:"err"},{name:"Margaret Hamilton",email:"margaret@interleet.dev",role:"Admin",status:"ok"}];const b=document.getElementById("b"),q=document.getElementById("q");function render(f){f=(f||"").toLowerCase();b.innerHTML=rows.filter(r=>r.name.toLowerCase().includes(f)||r.email.toLowerCase().includes(f)).map(r=>'<tr><td>'+r.name+'</td><td>'+r.email+'</td><td>'+r.role+'</td><td><span class="pill '+r.status+'">'+r.status+'</span></td></tr>').join("");}q.addEventListener("input",e=>render(e.target.value));render("");</script></body></html>`;
    case "ssr-cache-strategy":
      return `<!doctype html><html><head>${base}<style>.card{border:1px solid #e5e5e5;border-radius:10px;padding:14px;margin-bottom:10px}.row{display:flex;justify-content:space-between;font-family:monospace;font-size:12px;padding:4px 0}.ok{color:#16a34a}.miss{color:#dc2626}button{padding:8px 12px;border:1px solid #0a0a0a;background:#0a0a0a;color:#fff;border-radius:8px}</style></head><body><h2>SSR Cache Preview</h2><div class="card"><div class="row"><span>GET /products</span><span id="s1" class="ok">HIT · 4ms</span></div><div class="row"><span>GET /products/42</span><span id="s2" class="miss">MISS · 218ms</span></div><div class="row"><span>GET /search?q=shoe</span><span id="s3" class="ok">HIT · 6ms</span></div></div><button onclick="bust()">Bust cache</button><script>function bust(){["s1","s2","s3"].forEach(id=>{const el=document.getElementById(id);el.textContent="MISS · "+(180+Math.floor(Math.random()*120))+"ms";el.className="miss";});}</script></body></html>`;
    default:
      return `<!doctype html><html><head>${base}</head><body><h2>${title}</h2><p style="color:#525252">Interactive preview for this challenge will render here.</p></body></html>`;
  }
}

function compileFrontendCode(code, slug, title) {
  if (!code) return getFrontendSrcDoc(slug, title);
  try {
    const files = JSON.parse(code);
    if (files && typeof files === "object" && "index.html" in files) {
      let html = files["index.html"] || "";
      const css = files["index.css"] || "";
      const js = files["index.js"] || "";

      // Strip external stylesheet links and script tags for index.css/index.js to prevent 404 resource requests
      html = html.replace(/<link[^>]*href=["']\/?index\.css["'][^>]*>/gi, "");
      html = html.replace(/<script[^>]*src=["']\/?index\.js["'][^>]*><\/script>/gi, "");

      // Inject css
      const styleTag = `<style>\n${css}\n</style>`;
      if (html.includes("</head>")) {
        html = html.replace("</head>", `${styleTag}\n</head>`);
      } else {
        html = `${styleTag}\n${html}`;
      }

      // Inject js
      const scriptTag = `<script>\n${js}\n</script>`;
      if (html.includes("</body>")) {
        html = html.replace("</body>", `${scriptTag}\n</body>`);
      } else {
        html = `${html}\n${scriptTag}`;
      }

      return html;
    }
  } catch (e) {}

  return code;
}

// ─── BrowserPreview Component ───────────────────────────────────────────────

const FRONTEND_DOMAINS = new Set(["Frontend"]);

const PreviewArea = memo(function PreviewArea({ domain, slug, title, code, execState, isMultiFileDomain }) {
  if (FRONTEND_DOMAINS.has(domain)) {
    return (
      <div className="flex flex-1 flex-col overflow-hidden bg-white">
        <iframe
          title={`${title} preview`}
          srcDoc={compileFrontendCode(code, slug, title)}
          sandbox="allow-scripts"
          className="h-full w-full flex-1 border-0 bg-white"
        />
      </div>
    );
  }

  // Determine if we have real execution results
  const runResult = execState?.runResult;
  const submitResult = execState?.submitResult;
  const isRunning = execState?.runStatus === "loading";
  const isSubmitting = execState?.submitStatus === "loading";

  if (isRunning || isSubmitting) {
    const activeStatus = execState?.activeStatus;
    const stages = [
      { key: "QUEUED", label: "Queued", desc: "Waiting for container sandbox..." },
      { key: "COMPILING", label: "Compiling", desc: "Analyzing syntax and structure..." },
      { key: "RUNNING", label: "Running", desc: "Executing sandbox test suite..." },
      { key: "JUDGING", label: "Judging", desc: "Validating output against expectations..." },
    ];

    const activeIdx = stages.findIndex((s) => s.key === activeStatus);
    const currentIdx = activeIdx !== -1 ? activeIdx : isRunning ? 2 : 0;

    return (
      <div className="flex flex-1 flex-col items-center justify-center bg-[#0A0A0A] p-6 font-sans">
        <div className="max-w-xs w-full space-y-6">
          <div className="flex flex-col items-center text-center space-y-1.5">
            <Loader2 className="h-5 w-5 animate-spin text-primary" />
            <h4 className="text-zinc-200 text-xs font-semibold uppercase tracking-wider">
              {isSubmitting ? "Async Submitting" : "Executing Code"}
            </h4>
            <p className="text-zinc-500 text-[11px] italic min-h-[16px]">
              {stages[currentIdx]?.desc || "Running test cases on backend sandbox..."}
            </p>
          </div>

          <div className="relative px-2">
            <div className="absolute top-2.5 left-0 w-full h-[2px] bg-zinc-800 rounded-full" />
            <div
              className="absolute top-2.5 left-0 h-[2px] bg-primary rounded-full transition-all duration-500"
              style={{ width: `${(currentIdx / (stages.length - 1)) * 100}%` }}
            />
            <div className="relative flex justify-between">
              {stages.map((stage, idx) => {
                const isPassed = idx < currentIdx;
                const isActive = idx === currentIdx;
                
                return (
                  <div key={stage.key} className="flex flex-col items-center">
                    <div
                      className={`h-5 w-5 rounded-full flex items-center justify-center text-[9px] font-bold border transition-all duration-300 ${
                        isPassed
                          ? "bg-emerald-950 border-emerald-500 text-emerald-400"
                          : isActive
                          ? "bg-primary/20 border-primary text-primary animate-pulse font-extrabold"
                          : "bg-zinc-900 border-zinc-800 text-zinc-600"
                      }`}
                    >
                      {isPassed ? "✓" : idx + 1}
                    </div>
                    <span
                      className={`text-[9px] mt-1.5 font-mono ${
                        isActive
                          ? "text-primary font-bold animate-pulse"
                          : isPassed
                          ? "text-emerald-400"
                          : "text-zinc-600"
                      }`}
                    >
                      {stage.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!runResult && !submitResult) {
    const out = getProgramOutput(slug);
    return (
      <div className="flex flex-1 min-h-0 flex-col overflow-y-auto bg-[#0A0A0A] p-4 text-xs font-sans">
        <div className="rounded-lg border border-border bg-card/60 p-4">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
            {isMultiFileDomain ? "Infrastructure Logs" : "Backend Preview Console"}
          </p>
          <p className="mt-2 text-zinc-400 leading-relaxed">
            {isMultiFileDomain
              ? "No active execution session. Write configuration and click Run or Submit to verify results here."
              : "No active execution session. Write code and click Run or Submit to verify results here."}
          </p>
        </div>

        <div className="mt-3 rounded-lg border border-border bg-card/60 p-4">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
            {isMultiFileDomain ? "Validation Pipeline Spec" : "Expected Output Format"}
          </p>
          <pre className="mt-3 whitespace-pre-wrap font-mono text-[11px] leading-relaxed text-zinc-500">
            {out.log}
          </pre>
        </div>
      </div>
    );
  }

  const activeResult = runResult || submitResult;
  const isSubmitResult = !!submitResult && !runResult;
  const verdictStr = activeResult.verdict || "UNKNOWN";
  const tcResults = activeResult.testcase_results || [];
  const hasCompileError = !!activeResult.compile_output;

  const sumRuntime = (results) => results.reduce((acc, curr) => acc + (curr.runtime_ms || curr.wall_time_ms || 0), 0);
  const maxMemory = (results) => results.reduce((max, curr) => Math.max(max, curr.peak_memory_mb || 0), 0);

  const VERDICT_STYLES = {
    ACCEPTED:              { bg: "bg-emerald-500/10", border: "border-emerald-500/20", text: "text-emerald-400", label: "Accepted", icon: "✓" },
    WRONG_ANSWER:          { bg: "bg-red-500/10",     border: "border-red-500/20",     text: "text-red-400",     label: "Wrong Answer", icon: "✗" },
    RUNTIME_ERROR:         { bg: "bg-orange-500/10",   border: "border-orange-500/20",  text: "text-orange-400",  label: "Runtime Error", icon: "!" },
    TIME_LIMIT_EXCEEDED:   { bg: "bg-yellow-500/10",   border: "border-yellow-500/20",  text: "text-yellow-400",  label: "Time Limit Exceeded", icon: "⏱" },
    MEMORY_LIMIT_EXCEEDED: { bg: "bg-purple-500/10",   border: "border-purple-500/20",  text: "text-purple-400",  label: "Memory Limit Exceeded", icon: "💾" },
    COMPILATION_ERROR:     { bg: "bg-red-500/10",      border: "border-red-500/20",     text: "text-red-400",     label: "Compilation Error", icon: "⚠" },
    INTERNAL_ERROR:        { bg: "bg-zinc-500/10",     border: "border-zinc-500/20",    text: "text-zinc-400",    label: "Internal Error", icon: "⚙" },
  };

  const vs = VERDICT_STYLES[verdictStr] || VERDICT_STYLES.INTERNAL_ERROR;

  return (
    <div className="flex flex-1 min-h-0 flex-col overflow-y-auto bg-[#0A0A0A] p-4 font-sans text-xs space-y-3">
      <div className={`p-4 rounded-xl border flex items-center gap-3 ${vs.bg} ${vs.border}`}>
        <span className={`text-2xl ${vs.icon === "✓" ? "text-emerald-400" : vs.text}`}>{vs.icon}</span>
        <div className="space-y-0.5">
          <h4 className={`font-bold ${vs.text}`}>{vs.label}</h4>
          {isSubmitResult ? (
            <p className="text-[10px] text-zinc-500 font-medium">
              Submitted successfully · {activeResult.passed_testcases} / {activeResult.total_testcases} tests passed
            </p>
          ) : (
            <p className="text-[10px] text-zinc-500 font-medium">
              Run completed · {activeResult.passed_testcases} / {activeResult.total_testcases} tests passed
            </p>
          )}
        </div>

        <div className="ml-auto flex items-center gap-4 text-right">
          <div>
            <span className="text-zinc-500 block text-[9px] uppercase tracking-wider font-mono">Time</span>
            <span className="text-zinc-300 font-bold font-mono">{sumRuntime(tcResults).toFixed(0)} ms</span>
          </div>
          <div>
            <span className="text-zinc-500 block text-[9px] uppercase tracking-wider font-mono">Memory</span>
            <span className="text-zinc-300 font-bold font-mono">{maxMemory(tcResults).toFixed(1)} MB</span>
          </div>
        </div>
      </div>

      {hasCompileError && (
        <div className="rounded-lg border border-red-500/20 bg-red-950/15 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-red-400 font-bold font-mono">Compilation Error</p>
          <pre className="whitespace-pre-wrap text-red-300 bg-black/40 p-2.5 rounded border border-red-500/10 text-[10px]">{activeResult.compile_output}</pre>
        </div>
      )}

      {activeResult.stderr && !hasCompileError && (
        <div className="rounded-lg border border-orange-500/20 bg-orange-950/10 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-orange-400 font-bold font-mono">Standard Error (stderr)</p>
          <pre className="whitespace-pre-wrap text-orange-300 bg-black/40 p-2.5 rounded border border-orange-500/10 text-[10px]">{activeResult.stderr}</pre>
        </div>
      )}

      {activeResult.error && (
        <div className="rounded-lg border border-zinc-500/20 bg-zinc-900/40 p-4 space-y-2">
          <p className="text-[10px] uppercase tracking-wider text-zinc-400 font-bold font-mono">Internal Error</p>
          <pre className="whitespace-pre-wrap text-zinc-300 bg-black/40 p-2.5 rounded border border-zinc-500/10 text-[10px]">{activeResult.error}</pre>
        </div>
      )}

      {tcResults.map((tc, idx) => {
        const tcVerdict = tc.verdict || (tc.passed ? "ACCEPTED" : "WRONG_ANSWER");
        const tcVs = VERDICT_STYLES[tcVerdict] || VERDICT_STYLES.INTERNAL_ERROR;
        const tcRuntime = tc.runtime_ms || tc.wall_time_ms || 0;
        const tcMemory = tc.peak_memory_mb || 0;

        return (
          <div key={idx} className="rounded-lg border border-border bg-card/45 p-4 space-y-2.5">
            <div className="flex justify-between items-center border-b border-border pb-1.5">
              <span className="font-bold text-white text-xs">
                Test Case #{idx + 1}{tc.name ? `: ${tc.name}` : ""}
                {tc.hidden && <span className="ml-1.5 text-[9px] text-zinc-500 font-normal">(hidden)</span>}
              </span>
              <span className={`text-[9px] font-bold px-2 py-0.5 rounded ${tcVs.bg} ${tcVs.text}`}>
                {tcVs.icon} {tcVs.label}
              </span>
            </div>

            <div className="flex flex-wrap gap-3 text-[10px] text-zinc-500 font-mono">
              {tc.exit_code !== 0 && <span>Exit: <span className="text-orange-400">{tc.exit_code}</span></span>}
              {tcRuntime > 0 && <span>Runtime: <span className="text-zinc-300">{tcRuntime.toFixed(0)} ms</span></span>}
              {tcMemory > 0 && <span>Memory: <span className="text-zinc-300">{tcMemory.toFixed(1)} MB</span></span>}
            </div>

            {tc.stderr && (
              <div className="space-y-1">
                <span className="text-orange-400 text-[10px] block font-sans font-semibold">stderr:</span>
                <pre className="bg-orange-950/20 border border-orange-500/10 p-2 rounded text-orange-300 text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.stderr}</pre>
              </div>
            )}

            {!tc.hidden && (
              <div className="space-y-1">
                <span className="text-zinc-500 text-[10px] block font-sans">Your Output:</span>
                <pre className={`bg-black/50 p-2 rounded text-[10px] overflow-x-auto whitespace-pre-wrap ${
                  tc.stdout && !tc.stdout.startsWith("(no output") ? "text-zinc-300" : "text-zinc-600 italic"
                }`}>{tc.stdout || "(empty)"}</pre>
              </div>
            )}

            {tc.hidden && tc.revealed_input && (
              <div className="space-y-2 border border-yellow-500/10 bg-yellow-500/5 p-3 rounded mt-2">
                <p className="text-[10px] font-bold text-yellow-400 uppercase tracking-wider block font-sans">Failing Hidden Case Diagnostics:</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1">
                  <div>
                    <span className="text-zinc-500 text-[9px] font-sans">Input:</span>
                    <pre className="bg-zinc-950 p-2 rounded border border-border text-zinc-300 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap select-all">{tc.revealed_input}</pre>
                  </div>
                  {tc.revealed_expected && (
                    <div>
                      <span className="text-zinc-500 text-[9px] font-sans">Expected Output:</span>
                      <pre className="bg-zinc-950 p-2 rounded border border-border text-emerald-400 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap select-all">{tc.revealed_expected}</pre>
                    </div>
                  )}
                </div>
              </div>
            )}

            {!tc.passed && !tc.hidden && (
              <div className="grid grid-cols-2 gap-2 mt-1">
                <div>
                  <span className="text-zinc-500 text-[10px] font-sans">Expected:</span>
                  <pre className="bg-zinc-950 p-2 rounded text-emerald-400/70 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.expected_output || "(empty)"}</pre>
                </div>
                <div>
                  <span className="text-zinc-500 text-[10px] font-sans">Actual:</span>
                  <pre className="bg-zinc-950 p-2 rounded text-red-400/70 font-mono text-[10px] overflow-x-auto whitespace-pre-wrap">{tc.stdout || "(empty)"}</pre>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
});

export const BrowserPreview = memo(function BrowserPreview({ domain, slug, title, code, execState, isMultiFileDomain }) {
  return (
    <div className="flex min-h-0 flex-1 flex-col overflow-hidden bg-card">
      <div className="border-b border-border bg-background/60 px-3 py-2">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-destructive/70" />
            <span className="h-2.5 w-2.5 rounded-full bg-warning/70" />
            <span className="h-2.5 w-2.5 rounded-full bg-success/70" />
          </div>
          <button className="ml-1 rounded p-1 text-muted-foreground hover:bg-secondary hover:text-foreground">
            <RotateCw className="h-3.5 w-3.5" />
          </button>
          <div className="flex flex-1 items-center gap-1.5 rounded-md border border-border bg-background/80 px-2.5 py-1 font-mono text-[11px] text-muted-foreground">
            <Lock className="h-3 w-3 text-success" />
            <span className="truncate">localhost:3000/preview</span>
          </div>
          <button className="rounded p-1 text-muted-foreground hover:bg-secondary hover:text-foreground">
            <Globe className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
      <PreviewArea domain={domain} slug={slug} title={title} code={code} execState={execState} isMultiFileDomain={isMultiFileDomain} />
    </div>
  );
});
export { compileFrontendCode, getFrontendSrcDoc, getProgramOutput, PreviewArea };
