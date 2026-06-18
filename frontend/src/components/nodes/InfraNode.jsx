import { memo } from "react";
import { Handle, Position, NodeResizer } from "reactflow";

// ==================== Cisco-Style Custom SVGs ====================

// 1. Client / Web UI
const ClientSVG = () => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(59,130,246,0.3)]">
    <rect x="4" y="6" width="40" height="26" rx="2" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
    <rect x="6" y="8" width="36" height="22" rx="1" fill="#09090b" />
    {/* Screen chart */}
    <path d="M10 24 L16 16 L22 22 L28 14 L34 20 L38 16" fill="none" stroke="#3b82f6" strokeWidth="1.5" strokeLinecap="round" />
    <circle cx="38" cy="16" r="2" fill="#60a5fa" className="animate-pulse" />
    {/* Stand */}
    <path d="M20 32 L16 42 L32 42 L28 32 Z" fill="#3f3f46" stroke="#4b5563" strokeWidth="1" />
    <rect x="12" y="42" width="24" height="2" fill="#52525b" />
  </svg>
);

// 2. Mobile Client
const MobileSVG = () => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(59,130,246,0.2)]">
    <rect x="11" y="4" width="26" height="40" rx="4" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
    <rect x="13" y="8" width="22" height="32" rx="2" fill="#09090b" />
    {/* Mobile UI elements */}
    <rect x="16" y="12" width="16" height="6" rx="1" fill="#3b82f6" fillOpacity="0.15" stroke="#3b82f6" strokeWidth="1" />
    <circle cx="24" cy="15" r="1.5" fill="#60a5fa" />
    <line x1="17" y1="24" x2="31" y2="24" stroke="#3f3f46" strokeWidth="1" />
    <line x1="17" y1="29" x2="27" y2="29" stroke="#3f3f46" strokeWidth="1" />
    <line x1="17" y1="34" x2="29" y2="34" stroke="#3f3f46" strokeWidth="1" />
    {/* Speaker and Button */}
    <line x1="21" y1="6" x2="27" y2="6" stroke="#52525b" strokeWidth="1.5" strokeLinecap="round" />
    <circle cx="24" cy="42" r="1.5" fill="#52525b" />
  </svg>
);

// 3. Router / DNS
const RouterSVG = () => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(59,130,246,0.4)]">
    {/* Outer circle bevel */}
    <circle cx="24" cy="24" r="21" fill="#2d3748" stroke="#4b5563" strokeWidth="1.5" />
    {/* Inner router disk */}
    <circle cx="24" cy="24" r="17" fill="#18181b" stroke="#3f3f46" strokeWidth="1.2" />
    {/* Directional cross arrows */}
    <g stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none">
      <path d="M24 20 L24 8 M21 11 L24 8 L27 11" />
      <path d="M24 28 L24 40 M21 37 L24 40 L27 37" />
      <path d="M20 24 L8 24 M11 21 L8 24 L11 27" />
      <path d="M28 24 L40 24 M37 21 L40 24 L37 27" />
    </g>
    {/* Core blinker */}
    <circle cx="24" cy="24" r="4" fill="#09090b" stroke="#3b82f6" strokeWidth="0.8" />
    <circle cx="24" cy="24" r="1.5" fill="#60a5fa" className="animate-ping" />
  </svg>
);

// 4. Switch / Load Balancer
const SwitchSVG = ({ active }) => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(99,102,241,0.25)]">
    <rect x="2" y="12" width="44" height="24" rx="2" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
    {/* Rack Ears */}
    <rect x="0" y="16" width="2" height="16" fill="#71717a" />
    <rect x="46" y="16" width="2" height="16" fill="#71717a" />
    {/* Port cluster */}
    <rect x="6" y="17" width="36" height="14" fill="#09090b" rx="1" />
    {Array.from({ length: 8 }).map((_, i) => {
      const x = 8 + i * 4.3;
      const glow = active ? (Math.random() > 0.4 ? "#22c55e" : "#f59e0b") : "#3f3f46";
      return (
        <g key={i}>
          <rect x={x} y={19} width="2.2" height="2.2" fill="#3f3f46" rx="0.3" />
          <circle cx={x + 1.1} cy={23} r="0.6" fill={glow} className={active ? "animate-pulse" : ""} />
          
          <rect x={x} y={26} width="2.2" height="2.2" fill="#3f3f46" rx="0.3" />
          <circle cx={x + 1.1} cy={30} r="0.6" fill={glow} className={active ? "animate-pulse" : ""} />
        </g>
      );
    })}
  </svg>
);

// 5. Server Blade (API, Microservice)
const ServerSVG = ({ cpu, active }) => {
  const cpuColor = cpu > 80 ? "#ef4444" : cpu > 60 ? "#f59e0b" : "#10b981";
  const numLEDs = Math.max(1, Math.min(5, Math.ceil((cpu || 5) / 20)));

  return (
    <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(239,68,68,0.15)]">
      <rect x="2" y="10" width="44" height="28" rx="2" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
      {/* Ventilation grilles */}
      <g stroke="#09090b" strokeWidth="1.5">
        <line x1="8" y1="18" x2="24" y2="18" />
        <line x1="8" y1="24" x2="24" y2="24" />
        <line x1="8" y1="30" x2="24" y2="30" />
      </g>
      {/* Power switch */}
      <circle cx="38" cy="24" r="3.5" fill="#18181b" stroke="#52525b" strokeWidth="1" />
      <circle cx="38" cy="24" r="1.5" fill={active ? "#10b981" : "#52525b"} />
      {/* CPU load display */}
      <rect x="28" y="16" width="4" height="16" fill="#09090b" rx="1" />
      {Array.from({ length: 5 }).map((_, idx) => {
        const y = 28 - idx * 2.8;
        const lit = active && idx < numLEDs;
        return (
          <rect
            key={idx}
            x="29"
            y={y}
            width="2"
            height="1.8"
            fill={lit ? cpuColor : "#3f3f46"}
            rx="0.3"
          />
        );
      })}
    </svg>
  );
};

// 6. Relational Database / Cylinders
const DatabaseSVG = ({ active }) => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(16,185,129,0.3)]">
    {/* Disk 1 (Top) */}
    <ellipse cx="24" cy="14" rx="17" ry="5" fill="#27272a" stroke="#4b5563" strokeWidth="1.2" />
    <ellipse cx="24" cy="14" rx="13" ry="3.5" fill="#18181b" />
    {/* Disk 2 (Middle) */}
    <path d="M7 14 A17 5 0 0 0 41 14 V24 A17 5 0 0 1 7 24 Z" fill="#27272a" stroke="#4b5563" strokeWidth="1.2" />
    <ellipse cx="24" cy="24" rx="13" ry="3.5" fill="#18181b" />
    {/* Disk 3 (Bottom) */}
    <path d="M7 24 A17 5 0 0 0 41 24 V34 A17 5 0 0 1 7 34 Z" fill="#27272a" stroke="#4b5563" strokeWidth="1.2" />
    <ellipse cx="24" cy="34" rx="13" ry="3.5" fill="#18181b" />
    {/* Blinking Head LEDs */}
    <circle cx="13" cy="19" r="1" fill="#ef4444" className={active ? "animate-ping" : ""} />
    <circle cx="35" cy="29" r="1" fill="#22c55e" className={active ? "animate-pulse" : ""} />
  </svg>
);

// 7. RAM Cache (Redis)
const CacheSVG = ({ active }) => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(245,158,11,0.3)]">
    {/* PCB Board */}
    <rect x="4" y="16" width="40" height="16" rx="1.5" fill="#065f46" stroke="#047857" strokeWidth="1.5" />
    {/* Gold Pin Contacts */}
    {Array.from({ length: 14 }).map((_, i) => (
      <line
        key={i}
        x1={6.5 + i * 2.7}
        y1="30"
        x2={6.5 + i * 2.7}
        y2="32"
        stroke="#d97706"
        strokeWidth="1"
      />
    ))}
    {/* Memory Chips */}
    <rect x="7" y="19" width="6" height="8" fill="#1e293b" rx="0.5" />
    <rect x="16" y="19" width="6" height="8" fill="#1e293b" rx="0.5" />
    <rect x="25" y="19" width="6" height="8" fill="#1e293b" rx="0.5" />
    <rect x="34" y="19" width="6" height="8" fill="#1e293b" rx="0.5" />
    {/* Microcircuit details */}
    <path d="M5 23 H43" stroke="#10b981" strokeWidth="0.8" strokeDasharray="2 2" />
    {active && (
      <circle cx="24" cy="24" r="7" fill="#f59e0b" fillOpacity="0.25" className="animate-pulse" />
    )}
  </svg>
);

// 8. Event Log Queue (Kafka / event-bus)
const QueueSVG = ({ active }) => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(139,92,246,0.3)]">
    {/* Stream path */}
    <rect x="4" y="15" width="40" height="18" rx="9" fill="#1e293b" stroke="#4b5563" strokeWidth="1.5" />
    {/* Partition barriers */}
    <line x1="14" y1="15" x2="14" y2="33" stroke="#4b5563" strokeWidth="1.2" />
    <line x1="24" y1="15" x2="24" y2="33" stroke="#4b5563" strokeWidth="1.2" />
    <line x1="34" y1="15" x2="34" y2="33" stroke="#4b5563" strokeWidth="1.2" />
    {/* Sliding packet blocks */}
    {active ? (
      <g className="animate-pulse">
        <rect x="6.5" y="18.5" width="5" height="11" rx="1" fill="#8b5cf6" />
        <rect x="16.5" y="18.5" width="5" height="11" rx="1" fill="#ec4899" />
        <rect x="26.5" y="18.5" width="5" height="11" rx="1" fill="#3b82f6" />
        <rect x="36.5" y="18.5" width="5" height="11" rx="1" fill="#10b981" />
      </g>
    ) : (
      <g opacity="0.4">
        <rect x="6.5" y="18.5" width="5" height="11" rx="1" fill="#6b7280" />
        <rect x="26.5" y="18.5" width="5" height="11" rx="1" fill="#6b7280" />
      </g>
    )}
  </svg>
);

// 9. API Gateway (Arch Shield)
const GatewaySVG = ({ active }) => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(167,139,250,0.3)]">
    <rect x="4" y="6" width="6" height="36" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
    <rect x="38" y="6" width="6" height="36" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
    <path d="M4 12 A20 20 0 0 1 44 12" fill="none" stroke="#4b5563" strokeWidth="2" />
    <rect x="14" y="14" width="20" height="28" fill="#09090b" rx="2" stroke="#a78bfa" strokeWidth="1" />
    {/* Grid matrix grids */}
    <line x1="20" y1="14" x2="20" y2="42" stroke="#a78bfa" strokeWidth="0.5" strokeOpacity="0.3" />
    <line x1="28" y1="14" x2="28" y2="42" stroke="#a78bfa" strokeWidth="0.5" strokeOpacity="0.3" />
    <line x1="14" y1="22" x2="34" y2="22" stroke="#a78bfa" strokeWidth="0.5" strokeOpacity="0.3" />
    <line x1="14" y1="32" x2="34" y2="32" stroke="#a78bfa" strokeWidth="0.5" strokeOpacity="0.3" />
    {/* Glowing shield overlay */}
    <path d="M24 20 L30 22.5 V27 C30 30.5 27 33 24 34.5 C21 33 18 30.5 18 27 V22.5 Z" fill={active ? "#a78bfa" : "#3f3f46"} fillOpacity="0.25" stroke={active ? "#c084fc" : "#4b5563"} strokeWidth="1.2" />
  </svg>
);

// 10. Edge Cloud (CDN)
const CloudSVG = () => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(59,130,246,0.35)]">
    <path d="M12 37 A 6 6 0 0 1 12 25 A 10 10 0 0 1 30 17 A 8 8 0 0 1 38 27 A 6 6 0 0 1 36 37 Z" fill="#1e293b" stroke="#3b82f6" strokeWidth="1.5" />
    {/* Embedded rack card inside Cloud */}
    <rect x="16" y="24" width="16" height="4" fill="#09090b" rx="0.5" stroke="#3b82f6" strokeWidth="0.5" />
    <circle cx="19" cy="26" r="0.6" fill="#10b981" className="animate-pulse" />
    <circle cx="29" cy="26" r="0.6" fill="#60a5fa" />
    <rect x="16" y="30" width="16" height="4" fill="#09090b" rx="0.5" stroke="#3b82f6" strokeWidth="0.5" />
    <circle cx="19" cy="32" r="0.6" fill="#10b981" />
    <circle cx="29" cy="32" r="0.6" fill="#f59e0b" className="animate-pulse" />
  </svg>
);

// 11. Monitoring Console
const MonitoringSVG = () => (
  <svg viewBox="0 0 48 48" className="h-10 w-10 drop-shadow-[0_2px_8px_rgba(16,185,129,0.2)]">
    <rect x="4" y="9" width="40" height="30" rx="3" fill="#27272a" stroke="#4b5563" strokeWidth="1.5" />
    <rect x="6" y="11" width="36" height="20" rx="1" fill="#041a12" />
    {/* Oscilloscope Grid line */}
    <line x1="6" y1="21" x2="42" y2="21" stroke="#064e3b" strokeWidth="0.5" strokeDasharray="1 1" />
    {/* Pulse Line */}
    <path d="M7 21 H15 L17 14 L19 28 L21 21 H27 L29 17 L31 25 L33 21 H41" fill="none" stroke="#10b981" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    {/* Dial Knobs */}
    <circle cx="12" cy="35" r="1.5" fill="#52525b" />
    <circle cx="24" cy="35" r="1.5" fill="#52525b" />
    <circle cx="36" cy="35" r="1.5" fill="#52525b" />
  </svg>
);

const DEVICE_RENDERERS = {
  client: ClientSVG,
  mobile: MobileSVG,
  web: ClientSVG,
  "client-cluster": ClientSVG,
  dns: RouterSVG,
  router: RouterSVG,
  cdn: CloudSVG,
  "reverse-proxy": SwitchSVG,
  "load-balancer": SwitchSVG,
  "api-gateway": GatewaySVG,
  "web-server": ServerSVG,
  "app-server": ServerSVG,
  "rest-api": ServerSVG,
  graphql: ServerSVG,
  auth: GatewaySVG,
  microservice: ServerSVG,
  postgresql: DatabaseSVG,
  mysql: DatabaseSVG,
  mongodb: DatabaseSVG,
  redis: CacheSVG,
  elasticsearch: DatabaseSVG,
  kafka: QueueSVG,
  rabbitmq: QueueSVG,
  "event-bus": QueueSVG,
  queue: QueueSVG,
  logging: MonitoringSVG,
  metrics: MonitoringSVG,
  alert: MonitoringSVG,
  llm: ServerSVG,
  embedding: ServerSVG,
  "vector-db": DatabaseSVG,
};

const HEALTH = {
  healthy: { dot: "bg-emerald-500 shadow-[0_0_10px_#10b981]", label: "Healthy", text: "text-emerald-400" },
  warning: { dot: "bg-amber-500 shadow-[0_0_10px_#f59e0b] animate-pulse", label: "Warning", text: "text-amber-400" },
  critical: { dot: "bg-red-500 shadow-[0_0_12px_#ef4444] animate-ping", label: "Critical", text: "text-red-400" },
};

function InfraNode({ data, selected }) {
  const isFailed = data.health === "critical";
  const active = (data.activeThroughput ?? 0) > 0 && !isFailed;
  
  const DeviceGraphic = DEVICE_RENDERERS[data.kind] || ServerSVG;
  const h = HEALTH[data.health || "healthy"];
  const throughput = data.activeThroughput !== undefined ? data.activeThroughput : (data.throughput ?? 0);
  const latency = data.latency ?? 0;
  const cpu = data.cpu ?? 12;
  const memory = data.memory ?? 24;
  const cost = data.hourlyCost ?? 0;

  return (
    <div
      className="group relative rounded-xl bg-zinc-950 text-white shadow-[0_4px_20px_rgba(0,0,0,0.5),0_1px_0_0_rgba(255,255,255,0.06)_inset] transition-all hover:shadow-[0_4px_30px_rgba(0,0,0,0.7)]"
      style={{
        borderColor: selected ? "#FF6500" : "rgba(255,255,255,0.08)",
        borderWidth: "1.5px",
        minWidth: 240,
        padding: 0,
      }}
    >
      <NodeResizer minWidth={200} minHeight={140} isVisible={selected} lineClassName="!border-[#FF6500]/50" handleClassName="!bg-[#FF6500] !border-none !w-2.5 !h-2.5" />
      
      {/* Ethernet RJ45 handles */}
      <Handle
        type="target"
        position={Position.Left}
        className="!h-3.5 !w-3.5 !rounded-sm !bg-zinc-900 !border !border-zinc-700 hover:!border-primary hover:!scale-110 transition-transform shadow-[inset_0_1px_4px_rgba(0,0,0,0.8)] flex items-center justify-center after:content-[''] after:w-1.5 after:h-1 after:bg-amber-500/80 after:rounded-t-sm"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="!h-3.5 !w-3.5 !rounded-sm !bg-zinc-900 !border !border-zinc-700 hover:!border-primary hover:!scale-110 transition-transform shadow-[inset_0_1px_4px_rgba(0,0,0,0.8)] flex items-center justify-center after:content-[''] after:w-1.5 after:h-1 after:bg-amber-500/80 after:rounded-t-sm"
      />
      <Handle
        type="target"
        position={Position.Top}
        id="t"
        className="!h-3.5 !w-3.5 !rounded-sm !bg-zinc-900 !border !border-zinc-700 hover:!border-primary hover:!scale-110 transition-transform shadow-[inset_0_1px_4px_rgba(0,0,0,0.8)] flex items-center justify-center after:content-[''] after:w-1.5 after:h-1 after:bg-amber-500/80 after:rounded-t-sm"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="b"
        className="!h-3.5 !w-3.5 !rounded-sm !bg-zinc-900 !border !border-zinc-700 hover:!border-primary hover:!scale-110 transition-transform shadow-[inset_0_1px_4px_rgba(0,0,0,0.8)] flex items-center justify-center after:content-[''] after:w-1.5 after:h-1 after:bg-amber-500/80 after:rounded-t-sm"
      />

      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-900 bg-zinc-900/60 px-4 py-3 rounded-t-xl">
        <div className="flex items-center gap-3 min-w-0">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-zinc-800 bg-black/60 shadow-[inset_0_2px_4px_rgba(0,0,0,0.7)]">
            <DeviceGraphic active={active} cpu={cpu} />
          </span>
          <div className="min-w-0">
            <div className="truncate text-[13px] font-bold tracking-wide text-zinc-100">{data.label}</div>
            <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-zinc-500">{data.category}</div>
          </div>
        </div>
        
        <div className="flex flex-col items-end gap-1">
          <div className="flex items-center gap-1.5 bg-black/45 border border-zinc-800/80 rounded px-1.5 py-0.5">
            <span className={`h-1.5 w-1.5 rounded-full ${h.dot}`} />
            <span className={`font-mono text-[8px] uppercase tracking-wider ${h.text}`}>{h.label}</span>
          </div>
          {data.replicas > 1 && (
            <span className="text-[9px] font-mono text-zinc-400 bg-zinc-800/50 px-1 rounded">
              x{data.replicas} repl
            </span>
          )}
        </div>
      </div>

      {/* Physical details (screws) */}
      <div className="absolute top-1.5 left-1.5 h-1 w-1 rounded-full bg-zinc-700/85 border border-zinc-500 shadow-inner" />
      <div className="absolute top-1.5 right-1.5 h-1 w-1 rounded-full bg-zinc-700/85 border border-zinc-500 shadow-inner" />
      <div className="absolute bottom-1.5 left-1.5 h-1 w-1 rounded-full bg-zinc-700/85 border border-zinc-500 shadow-inner" />
      <div className="absolute bottom-1.5 right-1.5 h-1 w-1 rounded-full bg-zinc-700/85 border border-zinc-500 shadow-inner" />

      {/* Readings */}
      <div className="p-3.5 space-y-3">
        <div className="grid grid-cols-2 gap-2 text-[11px]">
          <div className="rounded-lg border border-zinc-900 bg-[#0c0d0e] px-2.5 py-2 shadow-inner">
            <div className="font-mono text-[8px] uppercase tracking-wider text-zinc-500">Throughput</div>
            <div className="font-mono font-bold text-zinc-200 mt-0.5 tabular-nums">
              {throughput.toLocaleString()} <span className="text-[9px] text-zinc-500">req/s</span>
            </div>
          </div>
          
          <div className="rounded-lg border border-zinc-900 bg-[#0c0d0e] px-2.5 py-2 shadow-inner">
            <div className="font-mono text-[8px] uppercase tracking-wider text-zinc-500">Latency</div>
            <div className="font-mono font-bold text-zinc-200 mt-0.5 tabular-nums">
              {latency} <span className="text-[9px] text-zinc-500">ms</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2 text-[10px] border-t border-zinc-900 pt-3">
          <Metric label="CPU" value={`${cpu}%`} pct={cpu} />
          <Metric label="MEM" value={`${memory}%`} pct={memory} />
          
          <div className="rounded-lg border border-zinc-900 bg-[#0c0d0e] px-2 py-1.5 text-center flex flex-col justify-between">
            <span className="font-mono text-[8px] uppercase tracking-wider text-zinc-500">Cost/Hr</span>
            <span className="font-mono font-semibold text-amber-500 mt-0.5">${cost.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value, pct }) {
  const color = pct > 80 ? "bg-red-500 shadow-[0_0_8px_#ef4444]" : pct > 60 ? "bg-amber-500 shadow-[0_0_8px_#f59e0b]" : "bg-emerald-500 shadow-[0_0_8px_#10b981]";
  return (
    <div className="rounded-lg border border-zinc-900 bg-[#0c0d0e] px-2 py-1.5 flex flex-col justify-between">
      <div className="flex items-center justify-between font-mono text-[8px] uppercase tracking-wider text-zinc-500">
        <span>{label}</span>
        <span className="text-zinc-300 font-semibold">{value}</span>
      </div>
      <div className="mt-1.5 h-1 w-full overflow-hidden rounded-full bg-zinc-800">
        <div className={`h-full ${color} transition-all duration-300`} style={{ width: `${Math.min(100, pct)}%` }} />
      </div>
    </div>
  );
}

export default memo(InfraNode);
