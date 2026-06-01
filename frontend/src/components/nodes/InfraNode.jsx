import { memo } from "react";
import { Handle, Position, NodeResizer } from "reactflow";
import {
  Monitor, Smartphone, Globe, Users, Server, ShieldCheck, Network, Workflow,
  Database, HardDrive, Boxes, Layers, Cpu, Cloud, Activity, Gauge, BellRing,
  Bot, Sparkles, FileSearch, Search, MessageSquare, Send, ListOrdered, Radio,
} from "lucide-react";

const ICONS = {
  client: Monitor, mobile: Smartphone, web: Globe, "client-cluster": Users,
  dns: Network, cdn: Cloud, "reverse-proxy": Workflow, "load-balancer": Workflow, "api-gateway": ShieldCheck,
  "web-server": Server, "app-server": Server, "rest-api": Layers, graphql: Layers, auth: ShieldCheck, microservice: Boxes,
  postgresql: Database, mysql: Database, mongodb: Database, redis: HardDrive, elasticsearch: Search,
  kafka: Radio, rabbitmq: MessageSquare, "event-bus": Send, queue: ListOrdered,
  logging: FileSearch, metrics: Gauge, alert: BellRing,
  llm: Bot, embedding: Sparkles, "vector-db": Cpu,
};

const HEALTH = {
  healthy: { dot: "bg-emerald-500", label: "Healthy", text: "text-emerald-400" },
  warning: { dot: "bg-amber-500", label: "Warning", text: "text-amber-400" },
  critical: { dot: "bg-red-500", label: "Critical", text: "text-red-400" },
};

function InfraNode({ data, selected }) {
  const Icon = ICONS[data.kind] || Server;
  const h = HEALTH[data.health || "healthy"];
  const throughput = data.throughput ?? 0;
  const latency = data.latency ?? 0;
  const cpu = data.cpu ?? 12;
  const memory = data.memory ?? 24;
  const cost = data.hourlyCost ?? 0;

  return (
    <div
      className="group relative rounded-xl border bg-[#161616] text-white shadow-[0_1px_0_0_rgba(255,255,255,0.04)_inset] transition-colors"
      style={{
        borderColor: selected ? "#FF6500" : "rgba(255,255,255,0.10)",
        minWidth: 220,
        padding: 16,
      }}
    >
      <NodeResizer minWidth={200} minHeight={140} isVisible={selected} lineClassName="!border-[#FF6500]/40" handleClassName="!bg-[#FF6500] !border-none !w-2 !h-2" />
      <Handle type="target" position={Position.Left} className="!h-3 !w-3 !bg-[#FF6500] !border-2 !border-white/80 hover:!scale-125 transition-transform" />
      <Handle type="source" position={Position.Right} className="!h-3 !w-3 !bg-[#FF6500] !border-2 !border-white/80 hover:!scale-125 transition-transform" />
      <Handle type="target" position={Position.Top} id="t" className="!h-3 !w-3 !bg-[#FF6500] !border-2 !border-white/80 hover:!scale-125 transition-transform" />
      <Handle type="source" position={Position.Bottom} id="b" className="!h-3 !w-3 !bg-[#FF6500] !border-2 !border-white/80 hover:!scale-125 transition-transform" />

      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-white/10 bg-black/40">
            <Icon className="h-4 w-4 text-white/80" />
          </span>
          <div className="min-w-0">
            <div className="truncate text-[13px] font-semibold leading-tight">{data.label}</div>
            <div className="font-mono text-[10px] uppercase tracking-widest text-white/40">{data.category}</div>
          </div>
        </div>
        <div className="flex items-center gap-1.5 rounded-md border border-white/10 bg-black/40 px-2 py-1">
          <span className={`h-1.5 w-1.5 rounded-full ${h.dot}`} />
          <span className={`font-mono text-[10px] ${h.text}`}>{h.label}</span>
        </div>
      </div>

      <div className="mt-3 grid grid-cols-2 gap-2 text-[11px]">
        <div className="rounded-md border border-white/10 bg-black/30 px-2 py-1.5">
          <div className="font-mono text-[9px] uppercase tracking-widest text-white/40">Throughput</div>
          <div className="font-mono text-white">{throughput} <span className="text-white/40">req/s</span></div>
        </div>
        <div className="rounded-md border border-white/10 bg-black/30 px-2 py-1.5">
          <div className="font-mono text-[9px] uppercase tracking-widest text-white/40">Latency</div>
          <div className="font-mono text-white">{latency} <span className="text-white/40">ms</span></div>
        </div>
      </div>

      <div className="mt-2 grid grid-cols-3 gap-2 text-[11px]">
        <Metric label="CPU" value={`${cpu}%`} pct={cpu} />
        <Metric label="MEM" value={`${memory}%`} pct={memory} />
        <div className="rounded-md border border-white/10 bg-black/30 px-2 py-1.5">
          <div className="font-mono text-[9px] uppercase tracking-widest text-white/40">Cost</div>
          <div className="font-mono text-white">${cost}<span className="text-white/40">/hr</span></div>
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value, pct }) {
  const color = pct > 80 ? "bg-red-500" : pct > 60 ? "bg-amber-500" : "bg-emerald-500";
  return (
    <div className="rounded-md border border-white/10 bg-black/30 px-2 py-1.5">
      <div className="flex items-center justify-between font-mono text-[9px] uppercase tracking-widest text-white/40">
        <span>{label}</span><span className="text-white/70">{value}</span>
      </div>
      <div className="mt-1 h-1 w-full overflow-hidden rounded-full bg-white/5">
        <div className={`h-full ${color}`} style={{ width: `${Math.min(100, pct)}%` }} />
      </div>
    </div>
  );
}

export default memo(InfraNode);
