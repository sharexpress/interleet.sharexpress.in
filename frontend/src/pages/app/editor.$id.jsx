import { Link, useParams, useLoaderData } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Drawer, DrawerContent, DrawerTrigger } from "@/components/ui/drawer";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue } from
"@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import { challenges } from "@/lib/mock";
import {
  Play,
  Send,
  FileCode2,
  Terminal as TerminalIcon,
  Check,
  X,
  ArrowLeft,
  Clock,
  Sparkles,
  Users,
  BookOpen,
  Globe,
  RotateCw,
  Lock } from
"lucide-react";



const code = `// rate-limiter.ts
export class TokenBucket {
  private tokens: number;
  private last = Date.now();

  constructor(
    private readonly capacity: number,
    private readonly refillPerSec: number,
  ) {
    this.tokens = capacity;
  }

  allow(): boolean {
    const now = Date.now();
    const elapsed = (now - this.last) / 1000;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsed * this.refillPerSec,
    );
    this.last = now;
    if (this.tokens >= 1) {
      this.tokens -= 1;
      return true;
    }
    return false;
  }
}
`;

function EditorPage() {
  const c = useLoaderData();
  return (
    <AppShell>
      {/* Toolbar */}
      <div className="flex items-center justify-between border-b border-border bg-card/40 px-4 py-2 md:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="h-8 w-8">
            <Link to={`/app/challenges/${c.slug}`}>
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold">{c.title}</p>
            <p className="truncate text-xs text-muted-foreground">
              {c.domain} · {c.difficulty} · {c.minutes}m
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Select defaultValue="ts">
            <SelectTrigger className="h-8 w-[130px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ts">TypeScript</SelectItem>
              <SelectItem value="js">JavaScript</SelectItem>
              <SelectItem value="py">Python</SelectItem>
              <SelectItem value="go">Go</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm">
            <Play className="mr-1.5 h-3.5 w-3.5" /> Run
          </Button>
          <Button size="sm">
            <Send className="mr-1.5 h-3.5 w-3.5" /> Submit
          </Button>
          <Drawer>
            <DrawerTrigger asChild>
              <Button
                variant="outline"
                size="icon"
                className="xl:hidden"
                aria-label="Open browser preview">
                
                <Globe className="h-4 w-4" />
              </Button>
            </DrawerTrigger>
            <DrawerContent className="p-0">
              <div className="flex h-[85vh] flex-col overflow-hidden">
                <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} />
              </div>
            </DrawerContent>
          </Drawer>
        </div>
      </div>

      {/* Three-pane workspace: left = problem, center = editor + tests, right = browser preview */}
      <div className="grid h-[calc(100vh-56px-49px)] grid-cols-1 md:grid-cols-[340px_1fr] xl:grid-cols-[340px_1fr_420px]">
        {/* LEFT: problem / question panel */}
        <aside className="order-1 hidden flex-col overflow-hidden border-r border-border bg-card md:flex">
          <div className="border-b border-border px-4 py-3">
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-primary" />
              <p className="text-sm font-semibold">Problem</p>
            </div>
            <p className="mt-1 truncate text-base font-semibold">{c.title}</p>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <DifficultyPill d={c.difficulty} />
              <DomainTag d={c.domain} />
              <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                <Clock className="h-3 w-3" /> {c.minutes}m
              </span>
              <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                <Sparkles className="h-3 w-3" /> {c.xp} XP
              </span>
              <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
                <Users className="h-3 w-3" /> {c.completion}%
              </span>
            </div>
          </div>
          <div className="flex-1 overflow-auto px-4 py-4 text-sm leading-relaxed text-foreground/90">
            <p>{c.summary}</p>

            <h3 className="mt-5 text-sm font-semibold">Requirements</h3>
            <ul className="mt-2 list-inside list-disc space-y-1 text-muted-foreground">
              <li>Implement a thread-safe token bucket with capacity and refill rate.</li>
              <li>Expose <code className="font-mono text-foreground">allow()</code> returning a boolean.</li>
              <li>Refill is continuous, not bucketed by the second.</li>
              <li>Reject the request once tokens drop below 1.</li>
            </ul>

            <h3 className="mt-5 text-sm font-semibold">Example</h3>
            <pre className="mt-2 overflow-auto rounded-md border border-border bg-background/60 p-3 font-mono text-[11px] text-foreground/85">
{`const b = new TokenBucket(3, 1); // 3 tokens, 1/sec
b.allow(); // true
b.allow(); // true
b.allow(); // true
b.allow(); // false  -> bucket empty
// wait 1s
b.allow(); // true`}
            </pre>

            <h3 className="mt-5 text-sm font-semibold">Constraints</h3>
            <ul className="mt-2 list-inside list-disc space-y-1 text-muted-foreground">
              <li>1 ≤ capacity ≤ 10<sup>6</sup></li>
              <li>0 ≤ refillPerSec ≤ 10<sup>5</sup></li>
              <li>Must be O(1) per allow() call</li>
            </ul>

            <h3 className="mt-5 text-sm font-semibold">Hints</h3>
            <ol className="mt-2 list-inside list-decimal space-y-1 text-muted-foreground">
              <li>Track the timestamp of the last update, not every individual token.</li>
              <li>Clamp accumulated tokens to <code className="font-mono text-foreground">capacity</code>.</li>
            </ol>
          </div>
        </aside>

        {/* CENTER: editor stacked over submission/tests */}
        <div className="order-2 flex min-w-0 flex-col border-r border-border">
          {/* Editor (top) */}
          <div className="flex min-h-0 flex-1 flex-col">
            <div className="flex items-center gap-1 border-b border-border bg-background/60 px-2 py-1.5">
              {["rate-limiter.ts", "basic.test.ts"].map((t, i) =>
              <div
                key={t}
                className={`flex items-center gap-2 rounded-t border-b-2 px-3 py-1 font-mono text-xs ${
                i === 0 ?
                "border-primary bg-card text-foreground" :
                "border-transparent text-muted-foreground hover:text-foreground"}`
                }>
                
                  <FileCode2 className="h-3 w-3" /> {t}
                </div>
              )}
            </div>
            <div className="flex min-h-0 flex-1 overflow-auto">
              <div className="select-none border-r border-border bg-background/40 px-3 py-3 text-right font-mono text-[11px] leading-relaxed text-muted-foreground">
                {code.split("\n").map((_, i) =>
                <div key={i}>{i + 1}</div>
                )}
              </div>
              <pre className="flex-1 overflow-auto p-3 font-mono text-[12px] leading-relaxed text-foreground/90">
                <code dangerouslySetInnerHTML={{ __html: highlight(code) }} />
              </pre>
            </div>
          </div>

          {/* Submission / Tests / Console (bottom) */}
          <div className="border-t border-border bg-background/60">
            <Tabs defaultValue="testcase" className="flex flex-col">
              <div className="flex items-center justify-between border-b border-border px-3 py-1.5">
                <TabsList className="h-8 bg-transparent p-0">
                  <TabsTrigger value="testcase" className="h-7 px-3 text-xs">
                    Testcase
                  </TabsTrigger>
                  <TabsTrigger value="result" className="h-7 px-3 text-xs">
                    Test Result
                  </TabsTrigger>
                  <TabsTrigger value="console" className="h-7 px-3 text-xs">
                    <TerminalIcon className="mr-1 h-3 w-3" />
                    Console
                  </TabsTrigger>
                </TabsList>
                <Badge variant="outline" className="font-mono text-[10px]">
                  node v20.10
                </Badge>
              </div>

              <TabsContent value="testcase" className="m-0 max-h-64 overflow-auto p-3">
                <div className="grid gap-2 md:grid-cols-3">
                  {[
                  { name: "Case 1", input: "capacity=15, refill=5/s", expected: "allow×15 then deny" },
                  { name: "Case 2", input: "capacity=1, refill=1/s", expected: "deny within 999ms" },
                  { name: "Case 3", input: "capacity=10, refill=0/s", expected: "deny after 10" }].
                  map((t) =>
                  <div
                    key={t.name}
                    className="rounded-md border border-border bg-card/60 p-3 text-xs">
                    
                      <p className="font-mono text-[11px] text-muted-foreground">{t.name}</p>
                      <p className="mt-1.5 font-mono text-foreground">{t.input}</p>
                      <p className="mt-1 font-mono text-muted-foreground">→ {t.expected}</p>
                    </div>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="result" className="m-0 max-h-64 overflow-auto p-3">
                <div className="mb-3 flex items-center gap-3">
                  <Badge className="bg-success text-success-foreground hover:bg-success">
                    <Check className="mr-1 h-3 w-3" /> Accepted
                  </Badge>
                  <span className="text-xs text-muted-foreground">
                    Runtime <span className="font-mono text-foreground">42 ms</span> · Memory{" "}
                    <span className="font-mono text-foreground">38.1 MB</span>
                  </span>
                </div>
                <div className="space-y-1.5">
                  {[
                  { l: "allows up to capacity", p: true },
                  { l: "refills at configured rate", p: true },
                  { l: "handles concurrent allow()", p: true },
                  { l: "rejects burst overflow", p: true },
                  { l: "respects refill cap", p: true },
                  { l: "drops under zero refill", p: false }].
                  map((t) =>
                  <div
                    key={t.l}
                    className="flex items-center gap-2 rounded-md border border-border bg-background/40 px-3 py-1.5 text-xs">
                    
                      {t.p ?
                    <Check className="h-3.5 w-3.5 text-success" /> :

                    <X className="h-3.5 w-3.5 text-destructive" />
                    }
                      <span className="font-mono">{t.l}</span>
                    </div>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="console" className="m-0">
                <pre className="max-h-64 overflow-auto p-3 font-mono text-[11px] leading-relaxed text-muted-foreground">
{`$ npm test
PASS  tests/basic.test.ts (1.2s)
  ✓ allows up to capacity
  ✓ refills at configured rate
PASS  tests/burst.test.ts (0.8s)
  ✓ rejects 16th request in burst of 16 with capacity 15

Tests:       5 passed, 5 total
Time:        2.04 s`}
                </pre>
              </TabsContent>
            </Tabs>
          </div>
        </div>

        {/* RIGHT: live browser preview */}
        <aside className="order-3 hidden flex-col overflow-hidden bg-card xl:flex">
          <BrowserPreview domain={c.domain} slug={c.slug} title={c.title} />
        </aside>
      </div>
    </AppShell>);

}

function BrowserPreview({ domain, slug, title }) {
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

      <PreviewArea domain={domain} slug={slug} title={title} />
    </div>);

}

// ---------- Adaptive right-pane preview ----------

const FRONTEND_DOMAINS = new Set(["Frontend"]);

function PreviewArea({ domain, slug, title }) {
  const isFrontend = FRONTEND_DOMAINS.has(domain);

  if (isFrontend) {
    return (
      <div className="flex flex-1 flex-col overflow-hidden bg-white">
        <iframe
          title={`${title} preview`}
          srcDoc={getFrontendSrcDoc(slug, title)}
          sandbox="allow-scripts"
          className="h-full w-full flex-1 border-0 bg-white" />
        
      </div>);

  }

  const out = getProgramOutput(slug);
  return (
    <div className="flex flex-1 flex-col overflow-auto bg-[#0A0A0A] p-4">
      <div className="rounded-lg border border-border bg-card/60 p-4">
        <p className="text-xs uppercase tracking-wider text-muted-foreground">
          Program Output
        </p>
        <pre className="mt-3 whitespace-pre-wrap font-mono text-[12px] leading-relaxed text-success">
          {out.log}
        </pre>
      </div>

      <div className="mt-3 rounded-lg border border-border bg-card/60 p-4">
        <p className="text-xs uppercase tracking-wider text-muted-foreground">Stats</p>
        <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
          {out.stats.map((s) =>
          <div
            key={s.label}
            className="rounded border border-border bg-background/40 px-2 py-1.5">
            
              <p className="text-muted-foreground">{s.label}</p>
              <p className={`font-mono ${s.tone ?? "text-foreground"}`}>{s.value}</p>
            </div>
          )}
        </div>
      </div>
    </div>);

}

function getProgramOutput(slug)


{
  switch (slug) {
    case "build-a-rate-limiter":
      return {
        log: `> TokenBucket(3, 1)
> b.allow() → true
> b.allow() → true
> b.allow() → true
> b.allow() → false
[waiting 1000ms...]
> b.allow() → true

✓ Run finished in 1.04s`,
        stats: [
        { label: "Calls", value: "5" },
        { label: "Allowed", value: "4", tone: "text-success" },
        { label: "Denied", value: "1", tone: "text-destructive" },
        { label: "Avg ms", value: "0.21" }]

      };
    case "feature-flag-service":
      return {
        log: `> flags.isOn("new-checkout", { userId: "u_42" }) → true
> flags.isOn("dark-mode", { userId: "u_7" })       → false
> flags.rollout("beta-search", 25%)                → ok
> 1,204 evaluations in 980ms

✓ Run finished in 0.98s`,
        stats: [
        { label: "Evals", value: "1204" },
        { label: "Cache hit", value: "94%", tone: "text-success" },
        { label: "p95 ms", value: "1.8" },
        { label: "Errors", value: "0", tone: "text-success" }]

      };
    default:
      return {
        log: `> running ${slug}…
✓ build ok
✓ tests passed
✓ Run finished in 1.21s`,
        stats: [
        { label: "Status", value: "OK", tone: "text-success" },
        { label: "Duration", value: "1.21s" },
        { label: "Warnings", value: "0" },
        { label: "Errors", value: "0", tone: "text-success" }]

      };
  }
}

function getFrontendSrcDoc(slug, title) {
  const base = `
    <style>
      :root { color-scheme: light; }
      * { box-sizing: border-box; }
      body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; color: #0a0a0a; background: #fff; padding: 16px; }
      h1,h2,h3 { margin: 0 0 12px; }
      button { font: inherit; cursor: pointer; }
    </style>`;

  switch (slug) {
    case "responsive-data-table":
      return `<!doctype html><html><head>${base}<style>
        .wrap { max-width: 720px; margin: 0 auto; }
        .toolbar { display:flex; gap:8px; margin-bottom:12px; }
        input { flex:1; padding:8px 10px; border:1px solid #e5e5e5; border-radius:8px; font:inherit; }
        table { width:100%; border-collapse: collapse; font-size: 13px; }
        th, td { text-align:left; padding:10px 12px; border-bottom: 1px solid #eee; }
        th { background:#fafafa; }
        tr:hover td { background:#fafafa; }
        .pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px; }
        .ok { background:#dcfce7; color:#166534; }
        .warn { background:#fef9c3; color:#854d0e; }
        .err { background:#fee2e2; color:#991b1b; }
        @media (max-width: 520px) {
          thead { display:none; }
          tr { display:block; padding:8px 0; border-bottom:1px solid #eee; }
          td { display:flex; justify-content:space-between; border:0; padding:6px 0; }
          td::before { content: attr(data-label); color:#737373; font-size:11px; }
        }
      </style></head><body><div class="wrap">
        <h2>Users</h2>
        <div class="toolbar"><input id="q" placeholder="Search by name or email…"/></div>
        <table id="t"><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th></tr></thead><tbody></tbody></table>
      </div><script>
        const rows = [
          {name:"Ada Lovelace",email:"ada@interleet.dev",role:"Admin",status:"ok"},
          {name:"Linus Torvalds",email:"linus@interleet.dev",role:"Maintainer",status:"ok"},
          {name:"Grace Hopper",email:"grace@interleet.dev",role:"Member",status:"warn"},
          {name:"Alan Turing",email:"alan@interleet.dev",role:"Member",status:"err"},
          {name:"Margaret Hamilton",email:"margaret@interleet.dev",role:"Admin",status:"ok"},
        ];
        const tbody = document.querySelector("tbody");
        const q = document.getElementById("q");
        function render(filter){
          const f = (filter||"").toLowerCase();
          tbody.innerHTML = rows.filter(r => r.name.toLowerCase().includes(f) || r.email.toLowerCase().includes(f))
            .map(r => '<tr>' +
              '<td data-label="Name">'+r.name+'</td>' +
              '<td data-label="Email">'+r.email+'</td>' +
              '<td data-label="Role">'+r.role+'</td>' +
              '<td data-label="Status"><span class="pill '+r.status+'">'+r.status+'</span></td>' +
            '</tr>').join("");
        }
        q.addEventListener("input", e => render(e.target.value));
        render("");
      </script></body></html>`;

    case "ssr-cache-strategy":
      return `<!doctype html><html><head>${base}<style>
        .card{border:1px solid #e5e5e5;border-radius:10px;padding:14px;margin-bottom:10px}
        .row{display:flex;justify-content:space-between;font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#404040;padding:4px 0}
        .ok{color:#16a34a}.miss{color:#dc2626}
        button{padding:8px 12px;border:1px solid #0a0a0a;background:#0a0a0a;color:#fff;border-radius:8px}
      </style></head><body>
        <h2>SSR Cache Preview</h2>
        <div class="card">
          <div class="row"><span>GET /products</span><span id="s1" class="ok">HIT · 4ms</span></div>
          <div class="row"><span>GET /products/42</span><span id="s2" class="miss">MISS · 218ms</span></div>
          <div class="row"><span>GET /search?q=shoe</span><span id="s3" class="ok">HIT · 6ms</span></div>
        </div>
        <button onclick="bust()">Bust cache</button>
        <script>
          function bust(){
            for (const id of ["s1","s2","s3"]) {
              const el = document.getElementById(id);
              el.textContent = "MISS · " + (180 + Math.floor(Math.random()*120)) + "ms";
              el.className = "miss";
            }
          }
        </script>
      </body></html>`;

    default:
      return '<!doctype html><html><head>' + base + '</head><body><h2>' + title + '</h2><p style="color:#525252">Interactive preview for this challenge will render here.</p></body></html>';
  }
}

// VS Code "Dark+" inspired token colors
const TOK = {
  comment: "#6A9955",
  keyword: "#C586C0",
  control: "#569CD6",
  type: "#4EC9B0",
  klass: "#4EC9B0",
  func: "#DCDCAA",
  string: "#CE9178",
  number: "#B5CEA8",
  prop: "#9CDCFE",
  punct: "#D4D4D4"
};

function highlight(src) {
  const esc = src.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Use placeholders so later passes don't re-tokenize inside spans.
  const slots = [];
  const slot = (html) => {
    const i = slots.length;
    slots.push(html);
    return `\u0000${i}\u0000`;
  };
  const span = (color, text) =>
  slot(`<span style="color:${color}">${text}</span>`);

  let s = esc;

  // 1. Line comments
  s = s.replace(/\/\/[^\n]*/g, (m) => span(TOK.comment, m));
  // 2. Strings (single, double, backtick)
  s = s.replace(/(["'`])(?:\\.|(?!\1)[^\\\n])*\1/g, (m) => span(TOK.string, m));
  // 3. Numbers
  s = s.replace(/\b\d+(?:\.\d+)?\b/g, (m) => span(TOK.number, m));
  // 4. Control flow keywords (blue)
  s = s.replace(
    /\b(if|else|return|for|while|switch|case|break|continue|throw|try|catch|finally)\b/g,
    (m) => span(TOK.control, m)
  );
  // 5. Declaration keywords (purple)
  s = s.replace(
    /\b(export|import|from|class|interface|extends|implements|private|public|protected|readonly|static|constructor|new|const|let|var|function|async|await|of|in|this|true|false|null|undefined)\b/g,
    (m) => span(TOK.keyword, m)
  );
  // 6. Built-in types (teal)
  s = s.replace(
    /\b(number|boolean|string|void|any|never|unknown|object|Promise|Array|Date|Math)\b/g,
    (m) => span(TOK.type, m)
  );
  // 7. Class / type names (PascalCase) → teal
  s = s.replace(/\b([A-Z][A-Za-z0-9_]*)\b/g, (m) => span(TOK.klass, m));
  // 8. Function calls: identifier followed by (
  s = s.replace(/\b([a-z_][A-Za-z0-9_]*)(?=\s*\()/g, (m) => span(TOK.func, m));
  // 9. Member properties: .ident
  s = s.replace(/\.([a-z_][A-Za-z0-9_]*)/g, (_m, p1) => "." + span(TOK.prop, p1));

  // Restore slots
  return s.replace(/\u0000(\d+)\u0000/g, (_m, i) => slots[Number(i)]);
}
export const loader = ({ params }) => {
    const c = challenges.find((x) => x.slug === params.id);
    if (!c) throw new Error("Not found");
    return c;
  };
export default EditorPage;
