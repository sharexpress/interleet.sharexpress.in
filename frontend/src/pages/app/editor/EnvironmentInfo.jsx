import { memo } from "react";

const EnvironmentInfo = memo(function EnvironmentInfo({ domain, lang }) {
  const isFrontend = domain === "Frontend";
  return (
    <div className="mt-4 rounded-lg border border-border bg-background/35 p-3 space-y-2 font-sans text-xs">
      <div className="flex items-center gap-1.5 border-b border-border/60 pb-1.5 text-[9px] uppercase font-mono tracking-wider text-muted-foreground">
        <span>⚙️ Execution Environment</span>
      </div>
      <div className="grid grid-cols-2 gap-2 text-[10px]">
        <div>
          <span className="text-zinc-500 block">Preview / Runtime</span>
          <span className="text-zinc-300 font-medium truncate block">
            {isFrontend ? "Live Browser Preview" : lang === "py" ? "Python 3.12 (Docker)" : lang === "js" ? "Node.js 20 (Docker)" : lang === "ts" ? "Node.js 20 (TS-Node)" : lang === "go" ? "Go 1.22 (Docker)" : "Docker Sandbox"}
          </span>
        </div>
        <div>
          <span className="text-zinc-500 block">Network Access</span>
          <span className="text-red-400 font-medium">Disabled (Isolated)</span>
        </div>
        <div>
          <span className="text-zinc-500 block">Memory Limit</span>
          <span className="text-zinc-300 font-medium">256 MB Hard Cap</span>
        </div>
        <div>
          <span className="text-zinc-500 block">Time Limit</span>
          <span className="text-zinc-300 font-medium">10.0 seconds</span>
        </div>
      </div>
      <div className="text-[9px] text-zinc-500 border-t border-border/60 pt-1.5 flex flex-wrap gap-1.5 items-center">
        <span>Preinstalled:</span>
        <span className="bg-secondary/40 px-1 py-0.5 rounded text-zinc-400 font-mono">lodash</span>
        <span className="bg-secondary/40 px-1 py-0.5 rounded text-zinc-400 font-mono">axios</span>
        {isFrontend && <span className="bg-secondary/40 px-1 py-0.5 rounded text-zinc-400 font-mono">jsdom</span>}
      </div>
    </div>
  );
});

export default EnvironmentInfo;
