import { useEffect } from "react";
import { MarketingNav, MarketingFooter } from "@/components/marketing/Marketing";

export default function SecurityPage() {
  useEffect(() => {
    document.title = "Security Posture — Interleet";
    document.dispatchEvent(new Event("prerender-ready"));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <MarketingNav />
      <div className="h-14" />
      <main className="flex-1 max-w-3xl mx-auto px-6 py-16 space-y-8 select-text leading-relaxed">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl border-b border-border/60 pb-4">
          Security Controls & Infrastructure Compliance
        </h1>
        <p className="text-muted-foreground font-mono text-[10px] uppercase tracking-wider">
          Last updated: July 2, 2026
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">1. Virtualization & Code Execution Sandboxing</h2>
          <p>
            The primary security requirement of the Interleet platform is isolating arbitrary user-submitted code. To guarantee that candidate compiles and runtime executions cannot access host systems or peer processes, we enforce strict isolation levels:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>gVisor Secure Kernels:</strong> Submissions are executed inside Docker containers run inside a gVisor user-space kernel. This intercepts kernel operations, preventing VM breakouts.
            </li>
            <li>
              <strong>Air-gapped Networking:</strong> Execution containers are completely disconnected from internal networks and standard internet routes, preventing data egress.
            </li>
            <li>
              <strong>Resource Exhaustion Limits:</strong> Execution containers are hard-limited to 256MB memory and 1 vCPU allocation. Process limits are enforced to mitigate fork bomb attacks.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">2. Data Security & Storage Compliance</h2>
          <p>
            All candidate transaction records, ELO ratings, submission logs, and recruiter details are protected using industry-standard security protocols:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground text-xs md:text-sm">
            <li>
              <strong>Encryption at Rest:</strong> Database storage instances are encrypted utilizing AES-256 keys managed by secure Key Management Services.
            </li>
            <li>
              <strong>Encryption in Transit:</strong> Session connections are secured using TLS 1.3 protocols, protecting transactions against interception.
            </li>
            <li>
              <strong>Access Audits:</strong> Backend logs track access to recruitment databases. Employee database access is strictly restricted through Multi-Factor Authentication.
            </li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight text-foreground/90">3. Cryptographically Signed Credentials</h2>
          <p>
            To prevent ELO score falsification, all profile certification badges are cryptographically signed using public/private key pairs. Recruiters verifying profiles can check candidate credentials against the public key directory, ensuring scorecards are unmodified.
          </p>
        </section>

        <section className="space-y-4 border-t border-border/60 pt-8">
          <h2 className="text-xl font-bold tracking-tight text-foreground/90">4. Vulnerability Disclosure Policy</h2>
          <p className="text-xs md:text-sm text-muted-foreground">
            We support security researchers investigating our platform limits. If you identify security flaws, report them to security@interleet.com. We acknowledge disclosures and reward verified issues.
          </p>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
