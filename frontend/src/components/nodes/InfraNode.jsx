/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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
  const throughput = data.activeThroughput !== undefined ? data.activeThroughput : (data.throughput ?? 0);
  const cpu = data.cpu ?? 12;

  return (
    <div
      className="group relative flex flex-col items-center justify-center"
      style={{
        width: 80,
        height: 80,
      }}
    >
      {/* Connection Handles */}
      <Handle
        type="target"
        position={Position.Left}
        className="!h-2.5 !w-2.5 !rounded-full !bg-[#FF6500] !border !border-white/20 hover:!scale-125 transition-transform shadow-[0_0_6px_rgba(255,101,0,0.4)] opacity-30 group-hover:opacity-100 transition-opacity"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="!h-2.5 !w-2.5 !rounded-full !bg-[#FF6500] !border !border-white/20 hover:!scale-125 transition-transform shadow-[0_0_6px_rgba(255,101,0,0.4)] opacity-30 group-hover:opacity-100 transition-opacity"
      />
      <Handle
        type="target"
        position={Position.Top}
        id="t"
        className="!h-2.5 !w-2.5 !rounded-full !bg-[#FF6500] !border !border-white/20 hover:!scale-125 transition-transform shadow-[0_0_6px_rgba(255,101,0,0.4)] opacity-30 group-hover:opacity-100 transition-opacity"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="b"
        className="!h-2.5 !w-2.5 !rounded-full !bg-[#FF6500] !border !border-white/20 hover:!scale-125 transition-transform shadow-[0_0_6px_rgba(255,101,0,0.4)] opacity-30 group-hover:opacity-100 transition-opacity"
      />

      {/* Central Device Circular Backdrop & Glows */}
      <div
        className={`relative h-16 w-16 rounded-full flex items-center justify-center bg-zinc-950/80 border transition-all duration-300 ${
          selected ? "border-[#FF6500] shadow-[0_0_15px_rgba(255,101,0,0.35)]" : "border-white/[0.08]"
        }`}
      >
        {/* Glow rings based on health */}
        <div className={`absolute inset-0 rounded-full transition-all duration-300 ${
          isFailed ? "ring-4 ring-red-500/20 border-red-500/50 animate-pulse bg-red-500/5" :
          data.health === "warning" ? "ring-4 ring-amber-500/15 border-amber-500/40 bg-amber-500/5" :
          active ? "ring-2 ring-emerald-500/10 border-emerald-500/30 bg-emerald-500/5" : ""
        }`} />
        
        {/* Device Graphic SVG */}
        <div className={`z-10 transition-transform duration-300 group-hover:scale-110 ${isFailed ? "opacity-50 grayscale" : ""}`}>
          <DeviceGraphic active={active} cpu={cpu} />
        </div>
      </div>

      {/* Replica mini-badge */}
      {data.replicas > 1 && (
        <span className="absolute top-1 right-1 z-20 rounded-full bg-zinc-900 border border-zinc-700 px-1 py-0.5 font-mono text-[8px] font-bold text-zinc-300 select-none shadow-md">
          x{data.replicas}
        </span>
      )}

      {/* Label and details underneath */}
      <div className="absolute top-[68px] flex flex-col items-center justify-center text-center w-36 pointer-events-none select-none">
        <span className="truncate text-[11px] font-bold text-zinc-200 font-mono tracking-wide drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">
          {data.label}
        </span>
        <span className="text-[8px] font-semibold text-zinc-500 uppercase tracking-widest mt-0.5">
          {throughput > 0 ? `${(throughput).toLocaleString()} r/s` : data.category}
        </span>
      </div>
    </div>
  );
}

export default memo(InfraNode);
