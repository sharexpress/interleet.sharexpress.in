
import { Logo } from "@/components/brand/Logo";

export function AuthShell({
  title,
  subtitle,
  children,
  footer





}) {
  return (
    <div className="grid min-h-screen bg-background md:grid-cols-2">
      <div className="flex flex-col px-6 py-8 md:px-12">
        <Logo />

        <div className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center">
          <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
          {subtitle && <p className="mt-2 text-sm text-muted-foreground">{subtitle}</p>}
          <div className="mt-6">{children}</div>
          {footer && <div className="mt-6 text-sm text-muted-foreground">{footer}</div>}
        </div>
        <p className="text-xs text-muted-foreground">
          © 2026 Interleet, Inc. ·{" "}
          <a href="#" className="hover:text-foreground">Privacy</a> ·{" "}
          <a href="#" className="hover:text-foreground">Terms</a>
        </p>
      </div>
      <div className="relative hidden overflow-hidden border-l border-border bg-card/40 md:block">
        <div className="grid-bg absolute inset-0 opacity-30" />
        <div className="pointer-events-none absolute -top-40 left-1/2 h-[500px] w-[600px] -translate-x-1/2 rounded-full bg-primary/20 blur-3xl" />
        <div className="relative flex h-full items-center justify-center p-10">
          <div className="max-w-md">
            <p className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
              The complete engineering arena
            </p>
            <h2 className="mt-3 text-3xl font-semibold leading-tight tracking-tight">
              Engineers don't ship algorithms.
              <br /> They ship systems.
            </h2>
            <p className="mt-4 text-sm text-muted-foreground">
              Practice the real stack — frontend through infra — with rubric-graded interviews and
              recruiter-verified profiles.
            </p>
            <div className="mt-8 space-y-2">
              {[
              "12,000+ production-style challenges",
              "AI mock interviews with full transcripts",
              "Verified skill badges for hiring teams"].
              map((x) =>
              <div key={x} className="flex items-start gap-2 text-sm">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-primary" />
                  <span className="text-foreground/85">{x}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>);

}