import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, memo } from "react";
import { useSearchParams } from "react-router-dom";
import ReactFlow, {
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  ReactFlowProvider,
  addEdge as rfAddEdge,
  applyEdgeChanges,
  applyNodeChanges,
  useReactFlow,
} from "reactflow";
import "reactflow/dist/style.css";
import { useDispatch, useSelector } from "react-redux";
import { API } from "@/api/api";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play,
  Pause,
  RotateCcw,
  Search,
  Save,
  FolderOpen,
  Download,
  FileJson,
  FileImage,
  Image as ImageIcon,
  Layers as LayersIcon,
  Maximize2,
  Grid3x3,
  Activity,
  AlertTriangle,
  ZapOff,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Trash2,
  Network as NetIcon,
  Plus,
  Server,
  Bot,
  X,
  Circle,
  BookOpen,
  ArrowLeft,
  Clock,
  Users,
  Lock,
} from "lucide-react";
import InfraNode from "@/components/nodes/InfraNode";
import TrafficEdge from "@/components/edges/TrafficEdge";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import { Card } from "@/components/ui/card";
import UpgradeModal from "@/components/UpgradeModal";
import { Badge } from "@/components/ui/badge";
import { Input as UiInput } from "@/components/ui/input";
import {
  Select as UiSelect,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import {
  setNodes as setNodesAction,
  setEdges as setEdgesAction,
  addNode,
  addEdge as addEdgeAction,
  updateNodeData,
  selectNode,
  setSimulation,
  setMetrics,
  setFailure,
  loadTemplate,
  clearCanvas,
} from "@/redux/slices/simulatorSlice";
import { catalog, kindMap, defaultPropsFor } from "@/lib/simulator/catalog";
import { templates } from "@/lib/simulator/templates";
import { challenges, blankChallenge } from "@/lib/simulator/challenges";

const nodeTypes = { infra: InfraNode };
const edgeTypes = { traffic: TrafficEdge };

const Panel = ({ children, className = "", style }) => (
  <div
    className={`flex flex-col bg-[#111111] border-white/[0.08] ${className}`}
    style={{ borderColor: "rgba(255,255,255,0.08)", ...style }}
  >
    {children}
  </div>
);

const SectionLabel = ({ children, right }) => (
  <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-2.5">
    <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-white/50">
      {children}
    </div>
    {right}
  </div>
);

const DragHandle = memo(function DragHandle({ onDelta }) {
  const dragging = useRef(false);
  const startX = useRef(0);

  const onMouseDown = useCallback(
    (e) => {
      e.preventDefault();
      dragging.current = true;
      startX.current = e.clientX;
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";

      const onMove = (ev) => {
        if (!dragging.current) return;
        const delta = ev.clientX - startX.current;
        startX.current = ev.clientX;
        onDelta(delta);
      };
      const onUp = () => {
        dragging.current = false;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [onDelta],
  );

  return (
    <div
      onMouseDown={onMouseDown}
      className="group relative z-10 flex-shrink-0"
      style={{ width: 6, cursor: "col-resize" }}
    >
      <div
        className="absolute inset-y-0 left-0 right-0 bg-[#FF6500]/50 opacity-0 transition-opacity group-hover:opacity-100"
        style={{ margin: "0 2px" }}
      />
    </div>
  );
});

// ---------- Left: component library ----------
function ComponentLibrary({ width }) {
  const [q, setQ] = useState("");
  const filtered = useMemo(() => {
    const term = q.trim().toLowerCase();
    return catalog
      .map((c) => ({
        ...c,
        items: c.items.filter(
          (i) => !term || i.label.toLowerCase().includes(term) || i.kind.includes(term),
        ),
      }))
      .filter((c) => c.items.length);
  }, [q]);

  const onDragStart = (e, kind) => {
    e.dataTransfer.setData("application/x-simulator-kind", kind);
    e.dataTransfer.effectAllowed = "move";
  };

  return (
    <Panel style={{ width }} className="shrink-0 border-r h-full">
      <div className="border-b border-white/[0.08] px-4 py-3">
        <div className="text-[13px] font-semibold">Components</div>
        <div className="text-[11px] text-white/50">Drag onto the canvas</div>
      </div>
      <div className="border-b border-white/[0.08] p-3">
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-white/40" />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search components"
            className="w-full rounded-md border border-white/10 bg-black/40 pl-8 pr-2 py-1.5 text-[12px] text-white placeholder:text-white/30 outline-none focus:border-[#FF6500]/50"
          />
        </div>
      </div>
      <div className="flex-1 overflow-y-auto">
        {filtered.map((group) => (
          <div key={group.category}>
            <div className="sticky top-0 z-10 bg-[#111111] px-4 py-2 font-mono text-[10px] uppercase tracking-[0.18em] text-white/50 border-b border-white/[0.06]">
              {group.category}
            </div>
            <div className="p-2 grid gap-1.5">
              {group.items.map((item) => (
                <div
                  key={item.kind}
                  draggable
                  onDragStart={(e) => onDragStart(e, item.kind)}
                  className="cursor-grab active:cursor-grabbing rounded-md border border-white/10 bg-[#161616] px-3 py-2 hover:border-white/25 transition-colors"
                >
                  <div className="text-[12px] font-medium text-white">{item.label}</div>
                  <div className="text-[10px] text-white/45">{item.desc}</div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
}

// ---------- Top toolbar ----------
function TopToolbar({ onFitView, onToggleGrid, showGrid, onToggleMetrics, onInjectFailure }) {
  const dispatch = useDispatch();
  const simulation = useSelector((s) => s.simulator.simulation);

  const Btn = ({ icon: Icon, children, onClick, primary, active }) => (
    <button
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1.5 text-[12px] transition-colors ${
        primary
          ? "border-[#FF6500] bg-[#FF6500] text-white hover:bg-[#FF6500]/90"
          : active
            ? "border-[#FF6500]/60 bg-[#FF6500]/10 text-white"
            : "border-white/10 bg-[#161616] text-white/85 hover:border-white/25 hover:text-white"
      }`}
    >
      {Icon && <Icon className="h-3.5 w-3.5" />} {children}
    </button>
  );

  return (
    <div className="flex h-12 items-center justify-between border-b border-white/[0.08] bg-[#111111] px-3">
      <div className="flex items-center gap-1.5">
        <div className="mr-2 flex items-center gap-2">
          <span className="flex h-6 w-6 items-center justify-center rounded-md border border-white/10 bg-black">
            <NetIcon className="h-3.5 w-3.5 text-[#FF6500]" />
          </span>
          <div className="leading-tight">
            <div className="text-[12px] font-semibold">System Design Simulator</div>
            <div className="font-mono text-[9px] uppercase tracking-widest text-white/40">
              challenge workspace
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-1.5">
        <Btn icon={Circle} active={showGrid} onClick={onToggleGrid}>
          Dots
        </Btn>
        <Btn icon={LayersIcon} onClick={onToggleMetrics}>
          Metrics
        </Btn>
        <Btn icon={Maximize2} onClick={onFitView}>
          Fit
        </Btn>
        <div className="mx-1 h-6 w-px bg-white/10" />
        <Btn icon={AlertTriangle} onClick={onInjectFailure}>
          Inject Failure
        </Btn>
        <Btn icon={RotateCcw} onClick={() => dispatch(clearCanvas())}>
          Reset
        </Btn>
        {simulation.running ? (
          <Btn icon={Pause} primary onClick={() => dispatch(setSimulation({ running: false }))}>
            Pause
          </Btn>
        ) : (
          <Btn icon={Play} primary onClick={() => dispatch(setSimulation({ running: true }))}>
            Start Simulation
          </Btn>
        )}
      </div>
    </div>
  );
}

// ---------- Right: metrics + properties ----------
function MetricsPanel() {
  const metrics = useSelector((s) => s.simulator.metrics);
  const nodes = useSelector((s) => s.simulator.nodes);
  const edges = useSelector((s) => s.simulator.edges);
  const monthly = (metrics.costHr * 24 * 30).toFixed(0);

  const Stat = ({ label, value, hint, status }) => {
    const statusColor =
      status === "Critical"
        ? "text-red-400"
        : status === "Warning"
          ? "text-amber-400"
          : "text-emerald-400";
    return (
      <div className="border-b border-white/[0.06] px-4 py-3">
        <div className="flex items-center justify-between font-mono text-[10px] uppercase tracking-widest text-white/45">
          <span>{label}</span>
          {hint && <span>{hint}</span>}
        </div>
        <div
          className={`mt-1 text-[18px] font-semibold tabular-nums ${status ? statusColor : "text-white"}`}
        >
          {value}
        </div>
      </div>
    );
  };

  return (
    <div className="flex h-full flex-col">
      <SectionLabel
        right={
          <span
            className={`inline-flex items-center gap-1.5 text-[10px] ${metrics.health === "Critical" ? "text-red-400" : metrics.health === "Warning" ? "text-amber-400" : "text-emerald-400"}`}
          >
            <span
              className={`h-1.5 w-1.5 rounded-full ${metrics.health === "Critical" ? "bg-red-500" : metrics.health === "Warning" ? "bg-amber-500" : "bg-emerald-500"}`}
            />
            {metrics.health}
          </span>
        }
      >
        System Metrics
      </SectionLabel>
      <Stat label="Throughput" value={`${metrics.throughput} req/s`} />
      <Stat
        label="Avg Latency"
        value={`${metrics.latency} ms`}
        status={metrics.latency > 250 ? "Critical" : metrics.latency > 150 ? "Warning" : "Healthy"}
      />
      <Stat
        label="Error Rate"
        value={`${metrics.errorRate.toFixed(2)}%`}
        status={metrics.errorRate > 5 ? "Critical" : metrics.errorRate > 1 ? "Warning" : "Healthy"}
      />
      <Stat label="Cost / hour" value={`$${metrics.costHr.toFixed(2)}`} hint={`$${monthly}/mo`} />
      <div className="grid grid-cols-2 border-b border-white/[0.06]">
        <div className="px-4 py-3 border-r border-white/[0.06]">
          <div className="font-mono text-[10px] uppercase tracking-widest text-white/45">Nodes</div>
          <div className="text-[18px] font-semibold tabular-nums">{nodes.length}</div>
        </div>
        <div className="px-4 py-3">
          <div className="font-mono text-[10px] uppercase tracking-widest text-white/45">
            Connections
          </div>
          <div className="text-[18px] font-semibold tabular-nums">{edges.length}</div>
        </div>
      </div>
    </div>
  );
}

function PropertiesPanel() {
  const dispatch = useDispatch();
  const id = useSelector((s) => s.simulator.selectedNodeId);
  const node = useSelector((s) => s.simulator.nodes.find((n) => n.id === id));

  if (!node) {
    return (
      <div className="flex h-full flex-col">
        <SectionLabel>Properties</SectionLabel>
        <div className="flex flex-1 items-center justify-center px-6 text-center">
          <div>
            <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-md border border-white/10 bg-black">
              <Server className="h-4 w-4 text-white/50" />
            </div>
            <div className="mt-3 text-[12px] text-white/60">Select a node to inspect</div>
            <div className="mt-1 text-[11px] text-white/35">
              Configure performance, cost, and component-specific parameters.
            </div>
          </div>
        </div>
      </div>
    );
  }

  const d = node.data;
  const update = (patch) => dispatch(updateNodeData({ id: node.id, data: patch }));

  const Row = ({ label, children }) => (
    <div className="grid grid-cols-[110px_1fr] items-center gap-2 px-4 py-2">
      <div className="font-mono text-[10px] uppercase tracking-widest text-white/45">{label}</div>
      <div className="text-[12px] text-white">{children}</div>
    </div>
  );
  const Input = (props) => (
    <input
      {...props}
      className="w-full rounded-md border border-white/10 bg-black/40 px-2 py-1 text-[12px] text-white outline-none focus:border-[#FF6500]/50"
    />
  );
  const Select = ({ options, value, onChange }) => (
    <select
      value={value}
      onChange={onChange}
      className="w-full rounded-md border border-white/10 bg-black/40 px-2 py-1 text-[12px] text-white outline-none focus:border-[#FF6500]/50"
    >
      {options.map((o) => (
        <option key={o} value={o} className="bg-[#111]">
          {o}
        </option>
      ))}
    </select>
  );

  const specific = (() => {
    switch (d.kind) {
      case "client":
      case "mobile":
      case "web":
      case "client-cluster":
        return (
          <>
            <Row label="Client Type">
              <Select
                value={d.clientType || "web"}
                onChange={(e) => update({ clientType: e.target.value })}
                options={["web", "mobile", "iot", "desktop"]}
              />
            </Row>
            <Row label="Users">
              <Input
                type="number"
                value={d.concurrentUsers ?? 1000}
                onChange={(e) => update({ concurrentUsers: +e.target.value })}
              />
            </Row>
            <Row label="Req Rate">
              <Input
                type="number"
                value={d.requestRate ?? 5}
                onChange={(e) => update({ requestRate: +e.target.value })}
              />
            </Row>
            <Row label="Region">
              <Select
                value={d.region || "us-east-1"}
                onChange={(e) => update({ region: e.target.value })}
                options={["us-east-1", "us-west-2", "eu-west-1", "ap-south-1"]}
              />
            </Row>
          </>
        );
      case "load-balancer":
        return (
          <>
            <Row label="Algorithm">
              <Select
                value={d.algorithm || "round-robin"}
                onChange={(e) => update({ algorithm: e.target.value })}
                options={["round-robin", "least-conn", "ip-hash", "weighted"]}
              />
            </Row>
            <Row label="SSL">
              <Toggle value={!!d.ssl} onChange={(v) => update({ ssl: v })} />
            </Row>
            <Row label="Sticky">
              <Toggle value={!!d.sticky} onChange={(v) => update({ sticky: v })} />
            </Row>
            <Row label="Max Conn">
              <Input
                type="number"
                value={d.maxConnections ?? 10000}
                onChange={(e) => update({ maxConnections: +e.target.value })}
              />
            </Row>
          </>
        );
      case "api-gateway":
        return (
          <>
            <Row label="Auth">
              <Toggle value={!!d.auth} onChange={(v) => update({ auth: v })} />
            </Row>
            <Row label="Rate Limit">
              <Input
                type="number"
                value={d.rateLimit ?? 1000}
                onChange={(e) => update({ rateLimit: +e.target.value })}
              />
            </Row>
            <Row label="Validation">
              <Toggle value={!!d.validation} onChange={(v) => update({ validation: v })} />
            </Row>
            <Row label="Version">
              <Input
                value={d.versioning ?? "v1"}
                onChange={(e) => update({ versioning: e.target.value })}
              />
            </Row>
            <Row label="Caching">
              <Toggle value={!!d.caching} onChange={(v) => update({ caching: v })} />
            </Row>
          </>
        );
      case "microservice":
        return (
          <>
            <Row label="Service">
              <Input
                value={d.serviceName ?? "service"}
                onChange={(e) => update({ serviceName: e.target.value })}
              />
            </Row>
            <Row label="Language">
              <Select
                value={d.language || "Node.js"}
                onChange={(e) => update({ language: e.target.value })}
                options={["Node.js", "Go", "Python", "Java", "Rust"]}
              />
            </Row>
            <Row label="Version">
              <Input
                value={d.version ?? "1.0.0"}
                onChange={(e) => update({ version: e.target.value })}
              />
            </Row>
            <Row label="Replicas">
              <Input
                type="number"
                value={d.replicas ?? 3}
                onChange={(e) => update({ replicas: +e.target.value })}
              />
            </Row>
            <Row label="Autoscale">
              <Toggle value={!!d.autoscaling} onChange={(v) => update({ autoscaling: v })} />
            </Row>
          </>
        );
      case "postgresql":
      case "mysql":
      case "mongodb":
        return (
          <>
            <Row label="Storage GB">
              <Input
                type="number"
                value={d.storage ?? 100}
                onChange={(e) => update({ storage: +e.target.value })}
              />
            </Row>
            <Row label="Replication">
              <Select
                value={d.replication || "primary-replica"}
                onChange={(e) => update({ replication: e.target.value })}
                options={["single", "primary-replica", "multi-primary", "replica-set"]}
              />
            </Row>
            <Row label="Backup">
              <Select
                value={d.backupStrategy || "daily"}
                onChange={(e) => update({ backupStrategy: e.target.value })}
                options={["none", "daily", "hourly", "continuous"]}
              />
            </Row>
            <Row label="Read Cap">
              <Input
                type="number"
                value={d.readCapacity ?? 2000}
                onChange={(e) => update({ readCapacity: +e.target.value })}
              />
            </Row>
            <Row label="Write Cap">
              <Input
                type="number"
                value={d.writeCapacity ?? 500}
                onChange={(e) => update({ writeCapacity: +e.target.value })}
              />
            </Row>
          </>
        );
      case "redis":
        return (
          <>
            <Row label="Memory GB">
              <Input
                type="number"
                value={d.memorySize ?? 4}
                onChange={(e) => update({ memorySize: +e.target.value })}
              />
            </Row>
            <Row label="TTL (s)">
              <Input
                type="number"
                value={d.ttl ?? 3600}
                onChange={(e) => update({ ttl: +e.target.value })}
              />
            </Row>
            <Row label="Replication">
              <Select
                value={d.replication || "primary-replica"}
                onChange={(e) => update({ replication: e.target.value })}
                options={["single", "primary-replica", "cluster"]}
              />
            </Row>
            <Row label="Eviction">
              <Select
                value={d.evictionPolicy || "allkeys-lru"}
                onChange={(e) => update({ evictionPolicy: e.target.value })}
                options={["noeviction", "allkeys-lru", "allkeys-lfu", "volatile-ttl"]}
              />
            </Row>
          </>
        );
      case "kafka":
        return (
          <>
            <Row label="Partitions">
              <Input
                type="number"
                value={d.partitions ?? 12}
                onChange={(e) => update({ partitions: +e.target.value })}
              />
            </Row>
            <Row label="Replication">
              <Input
                type="number"
                value={d.replicationFactor ?? 3}
                onChange={(e) => update({ replicationFactor: +e.target.value })}
              />
            </Row>
            <Row label="Retention (h)">
              <Input
                type="number"
                value={d.retentionPeriod ?? 168}
                onChange={(e) => update({ retentionPeriod: +e.target.value })}
              />
            </Row>
          </>
        );
      default:
        return null;
    }
  })();

  return (
    <div className="flex h-full flex-col overflow-y-auto">
      <SectionLabel
        right={
          <button
            className="text-white/50 hover:text-white"
            onClick={() => dispatch(clearCanvas())}
          >
            <X className="h-3.5 w-3.5" />
          </button>
        }
      >
        Properties · {d.label}
      </SectionLabel>

      <div className="border-b border-white/[0.06] py-1">
        <Row label="Name">
          <Input value={d.label} onChange={(e) => update({ label: e.target.value })} />
        </Row>
        <Row label="Description">
          <Input
            value={d.description ?? ""}
            onChange={(e) => update({ description: e.target.value })}
            placeholder="Notes…"
          />
        </Row>
        <Row label="Environment">
          <Select
            value={d.environment || "production"}
            onChange={(e) => update({ environment: e.target.value })}
            options={["development", "staging", "production"]}
          />
        </Row>
      </div>

      <div className="border-b border-white/[0.06] py-1">
        <SubLabel>Status</SubLabel>
        <Row label="Enabled">
          <Toggle value={d.enabled !== false} onChange={(v) => update({ enabled: v })} />
        </Row>
        <Row label="Health">
          <Select
            value={d.health || "healthy"}
            onChange={(e) => update({ health: e.target.value })}
            options={["healthy", "warning", "critical"]}
          />
        </Row>
        <Row label="Replicas">
          <Input
            type="number"
            value={d.replicas ?? 1}
            onChange={(e) => update({ replicas: +e.target.value })}
          />
        </Row>
      </div>

      <div className="border-b border-white/[0.06] py-1">
        <SubLabel>Performance</SubLabel>
        <Row label="Throughput">
          <Input
            type="number"
            value={d.throughput ?? 100}
            onChange={(e) => update({ throughput: +e.target.value })}
          />
        </Row>
        <Row label="Latency">
          <Input
            type="number"
            value={d.latency ?? 20}
            onChange={(e) => update({ latency: +e.target.value })}
          />
        </Row>
        <Row label="Error Rate">
          <Input
            type="number"
            step="0.1"
            value={d.errorRate ?? 0}
            onChange={(e) => update({ errorRate: +e.target.value })}
          />
        </Row>
      </div>

      <div className="border-b border-white/[0.06] py-1">
        <SubLabel>Cost</SubLabel>
        <Row label="Hourly $">
          <Input
            type="number"
            value={d.hourlyCost ?? 0}
            onChange={(e) => update({ hourlyCost: +e.target.value })}
          />
        </Row>
        <Row label="Monthly $">
          <div className="font-mono text-white/70">
            ${((d.hourlyCost ?? 0) * 24 * 30).toFixed(0)}
          </div>
        </Row>
      </div>

      {specific && (
        <div className="border-b border-white/[0.06] py-1">
          <SubLabel>{kindMap[d.kind]?.label} settings</SubLabel>
          {specific}
        </div>
      )}
    </div>
  );
}

const SubLabel = ({ children }) => (
  <div className="px-4 pt-2 pb-1 font-mono text-[10px] uppercase tracking-widest text-white/35">
    {children}
  </div>
);

const Toggle = ({ value, onChange }) => (
  <button
    onClick={() => onChange(!value)}
    className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${value ? "bg-[#FF6500]" : "bg-white/15"}`}
  >
    <span
      className={`inline-block h-3.5 w-3.5 transform rounded-full bg-white transition-transform ${value ? "translate-x-5" : "translate-x-1"}`}
    />
  </button>
);

// ---------- Bottom: simulation control ----------
function SimulationDock({ suggestions }) {
  const dispatch = useDispatch();
  const sim = useSelector((s) => s.simulator.simulation);
  const [assistantOpen, setAssistantOpen] = useState(false);

  return (
    <>
      <motion.div
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="pointer-events-auto absolute bottom-4 left-1/2 z-20 -translate-x-1/2 rounded-xl border border-white/10 bg-[#111111]/95 px-3 py-2.5 backdrop-blur"
      >
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] uppercase tracking-widest text-white/50">
              User Load
            </span>
            <input
              type="range"
              min={1}
              max={100000}
              step={100}
              value={sim.userLoad}
              onChange={(e) => dispatch(setSimulation({ userLoad: +e.target.value }))}
              className="w-56 accent-[#FF6500]"
            />
            <span className="w-20 text-right font-mono text-[12px] text-white tabular-nums">
              {sim.userLoad.toLocaleString()} <span className="text-white/40">req/s</span>
            </span>
          </div>
          <div className="h-6 w-px bg-white/10" />
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] uppercase tracking-widest text-white/50">
              Pattern
            </span>
            <select
              value={sim.pattern}
              onChange={(e) => dispatch(setSimulation({ pattern: e.target.value }))}
              className="rounded-md border border-white/10 bg-black/40 px-2 py-1 text-[12px] text-white outline-none"
            >
              {["constant", "burst", "peak-hours", "random", "ddos"].map((p) => (
                <option key={p} value={p} className="bg-[#111]">
                  {p}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] uppercase tracking-widest text-white/50">
              Duration
            </span>
            <select
              value={sim.duration}
              onChange={(e) => dispatch(setSimulation({ duration: e.target.value }))}
              className="rounded-md border border-white/10 bg-black/40 px-2 py-1 text-[12px] text-white outline-none"
            >
              {["1m", "5m", "15m", "1h"].map((p) => (
                <option key={p} value={p} className="bg-[#111]">
                  {p}
                </option>
              ))}
            </select>
          </div>
          <div className="h-6 w-px bg-white/10" />
          <div className="flex items-center gap-1.5">
            {sim.running ? (
              <button
                onClick={() => dispatch(setSimulation({ running: false }))}
                className="inline-flex items-center gap-1 rounded-md border border-white/10 bg-[#161616] px-2.5 py-1.5 text-[12px] text-white hover:border-white/25"
              >
                <Pause className="h-3.5 w-3.5" /> Pause
              </button>
            ) : (
              <button
                onClick={() => dispatch(setSimulation({ running: true }))}
                className="inline-flex items-center gap-1 rounded-md border border-[#FF6500] bg-[#FF6500] px-2.5 py-1.5 text-[12px] text-white hover:bg-[#FF6500]/90"
              >
                <Play className="h-3.5 w-3.5" /> Start
              </button>
            )}
            <button
              onClick={() => setAssistantOpen((o) => !o)}
              className={`inline-flex items-center gap-1 rounded-md border px-2.5 py-1.5 text-[12px] transition-colors ${
                assistantOpen
                  ? "border-[#FF6500]/60 bg-[#FF6500]/10 text-white"
                  : "border-white/10 bg-[#161616] text-white hover:border-white/25"
              }`}
            >
              <Sparkles className="h-3.5 w-3.5 text-[#FF6500]" /> Optimization Assistant
            </button>
          </div>
        </div>
      </motion.div>

      <OptimizationAssistant
        suggestions={suggestions}
        open={assistantOpen}
        onClose={() => setAssistantOpen(false)}
      />
    </>
  );
}

// ---------- Optimization Assistant (floating) ----------

function OptimizationAssistant({ suggestions, open, onClose }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="pointer-events-auto absolute right-4 bottom-24 z-30 w-96 rounded-xl border border-white/10 bg-[#111111]/95 backdrop-blur"
        >
          <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-[#FF6500]" />
              <span className="font-semibold">Optimization Assistant</span>
            </div>

            <button onClick={onClose} className="text-white/50 hover:text-white">
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="max-h-[420px] overflow-y-auto p-3">
            {suggestions.length === 0 ? (
              <div className="text-[12px] text-white/45">
                System is healthy — no recommendations.
              </div>
            ) : (
              suggestions.map((s, i) => (
                <div key={i} className="mb-2 rounded-md border border-white/10 bg-[#161616] p-3">
                  <div className="text-[13px] font-semibold">{s.title}</div>
                  <div className="mt-1 text-[11px] text-white/55">{s.detail}</div>
                  <div className="mt-2 grid grid-cols-3 gap-2">
                    <Pill label="Latency" value={s.impact.latency} positive />
                    <Pill label="Throughput" value={s.impact.throughput} positive />
                    <Pill label="Cost" value={s.impact.cost} />
                  </div>
                </div>
              ))
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

const Pill = ({ label, value, positive }) => (
  <div className="rounded-md border border-white/10 bg-black/40 px-1.5 py-1">
    <div className="font-mono text-[9px] uppercase tracking-widest text-white/40">{label}</div>
    <div className={`font-mono ${positive ? "text-emerald-400" : "text-amber-400"}`}>{value}</div>
  </div>
);

// ---------- Templates bar ----------
function TemplatesStrip() {
  const dispatch = useDispatch();
  return (
    <div className="flex items-center gap-1.5 overflow-x-auto border-b border-white/[0.08] bg-[#111111] px-3 py-2">
      <span className="font-mono text-[10px] uppercase tracking-widest text-white/45 pr-2">
        Templates
      </span>
      {templates.map((t) => (
        <button
          key={t.id}
          onClick={() => dispatch(loadTemplate({ nodes: t.nodes, edges: t.edges }))}
          className="whitespace-nowrap rounded-md border border-white/10 bg-[#161616] px-2.5 py-1 text-[11px] text-white/85 hover:border-white/25 hover:text-white"
        >
          {t.name}
        </button>
      ))}
    </div>
  );
}

// ---------- Canvas ----------
function CanvasInner({ showGrid, showMetrics, suggestions }) {
  const dispatch = useDispatch();
  const nodes = useSelector((s) => s.simulator.nodes);
  const edges = useSelector((s) => s.simulator.edges);
  const simulation = useSelector((s) => s.simulator.simulation);
  const rf = useReactFlow();
  const wrapper = useRef(null);

  const onNodesChange = useCallback(
    (c) => dispatch(setNodesAction(applyNodeChanges(c, nodes))),
    [nodes, dispatch],
  );
  const onEdgesChange = useCallback(
    (c) => dispatch(setEdgesAction(applyEdgeChanges(c, edges))),
    [edges, dispatch],
  );
  const onConnect = useCallback(
    (p) =>
      dispatch(
        setEdgesAction(
          rfAddEdge({ ...p, type: "traffic", animated: true, data: { kind: "request" } }, edges),
        ),
      ),
    [edges, dispatch],
  );

  const onDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };
  const onDrop = (e) => {
    e.preventDefault();
    const kind = e.dataTransfer.getData("application/x-simulator-kind");
    if (!kind) return;
    const meta = kindMap[kind];
    const position = rf.screenToFlowPosition({ x: e.clientX, y: e.clientY });
    const id = `${kind}-${Date.now()}`;
    dispatch(
      addNode({
        id,
        type: "infra",
        position,
        data: { kind, label: meta.label, category: meta.category, ...defaultPropsFor(kind) },
      }),
    );
  };

  return (
    <div ref={wrapper} className="relative h-full w-full" onDragOver={onDragOver} onDrop={onDrop}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={(_, n) => dispatch(selectNode(n.id))}
        onPaneClick={() => dispatch(selectNode(null))}
        fitView
        fitViewOptions={{ padding: 0.25 }}
        proOptions={{ hideAttribution: true }}
        multiSelectionKeyCode="Shift"
        deleteKeyCode={["Backspace", "Delete"]}
        defaultEdgeOptions={{ type: "traffic", animated: true }}
        minZoom={0.2}
        maxZoom={2.5}
        style={{ background: "#0A0A0A" }}
      >
        {showGrid && (
          <Background
            variant={BackgroundVariant.Dots}
            gap={22}
            size={1.4}
            color="rgba(255,255,255,0.55)"
          />
        )}
        <Controls className="!bg-[#111111] !border !border-white/10 [&_button]:!bg-[#161616] [&_button]:!border-white/10 [&_button]:!text-white" />
        {showMetrics && (
          <MiniMap
            maskColor="rgba(0,0,0,0.6)"
            nodeColor={() => "#FF6500"}
            nodeStrokeColor={() => "#FF6500"}
            style={{ background: "#0A0A0A", border: "1px solid rgba(255,255,255,0.1)" }}
          />
        )}
      </ReactFlow>

      {/* <SimulationDock /> */}
      <SimulationDock suggestions={suggestions} />

      {simulation.running && (
        <div className="pointer-events-none absolute left-4 top-4 z-20 inline-flex items-center gap-2 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-2.5 py-1 text-[11px] text-emerald-300">
          <Activity className="h-3.5 w-3.5" /> Simulating · {simulation.pattern} ·{" "}
          {simulation.userLoad.toLocaleString()} req/s
        </div>
      )}
    </div>
  );
}

// ---------- Simulation engine ----------
function useSimulationEngine() {
  const dispatch = useDispatch();
  const sim = useSelector((s) => s.simulator.simulation);
  const nodes = useSelector((s) => s.simulator.nodes);
  const edges = useSelector((s) => s.simulator.edges);
  const failure = useSelector((s) => s.simulator.failure);

  // Refs keep the interval callback reading the latest state without
  // re-creating the interval (which would otherwise overwrite positions
  // mid-drag with a stale snapshot).
  const nodesRef = useRef(nodes);
  const edgesRef = useRef(edges);
  const simRef = useRef(sim);
  const failureRef = useRef(failure);
  useLayoutEffect(() => {
    nodesRef.current = nodes;
    edgesRef.current = edges;
    simRef.current = sim;
    failureRef.current = failure;
  }, [nodes, edges, sim, failure]);

  // Recalculate costHr reactively when nodes change in idle state
  useEffect(() => {
    if (!sim.running) {
      let costHr = 0;
      nodes.forEach((n) => {
        const cost = n.data.hourlyCost !== undefined && n.data.hourlyCost !== "" ? Number(n.data.hourlyCost) : 0;
        const reps = n.data.replicas !== undefined && n.data.replicas !== "" ? Number(n.data.replicas) : 1;
        costHr += (isNaN(cost) ? 0 : cost) * (isNaN(reps) || reps <= 0 ? 1 : reps);
      });
      dispatch(
        setMetrics({
          costHr,
        }),
      );
    }
  }, [nodes, sim.running, dispatch]);

  useEffect(() => {
    if (!sim.running) {
      // Reset active metrics on all nodes when simulation stops
      const idleNodes = nodesRef.current.map((n) => ({
        ...n,
        data: {
          ...n.data,
          cpu: 4,
          memory: 20,
          latency: n.data.latency || 20,
          health: "healthy",
          throughput: 0,
          errorRate: 0,
        },
      }));
      dispatch(setNodesAction(idleNodes));
      dispatch(
        setEdgesAction(
          edgesRef.current.map((e) => ({
            ...e,
            animated: false,
            data: {
              ...e.data,
              health: "healthy",
              metric: 0,
            },
          })),
        ),
      );

      let costHr = 0;
      nodesRef.current.forEach((n) => {
        const cost = n.data.hourlyCost !== undefined && n.data.hourlyCost !== "" ? Number(n.data.hourlyCost) : 0;
        const reps = n.data.replicas !== undefined && n.data.replicas !== "" ? Number(n.data.replicas) : 1;
        costHr += (isNaN(cost) ? 0 : cost) * (isNaN(reps) || reps <= 0 ? 1 : reps);
      });

      dispatch(
        setMetrics({
          throughput: 0,
          latency: 0,
          errorRate: 0,
          costHr,
          health: "Healthy",
        }),
      );
      return;
    }

    const id = setInterval(() => {
      const s = simRef.current;
      const f = failureRef.current;
      const currentNodes = nodesRef.current;
      const currentEdges = edgesRef.current;

      let multiplier = 1.0;
      if (s.pattern === "burst") multiplier = 0.6 + Math.random() * 1.8;
      else if (s.pattern === "peak-hours") multiplier = 0.9 + 0.4 * Math.sin(Date.now() / 5000);
      else if (s.pattern === "random") multiplier = 0.4 + Math.random() * 1.2;
      else if (s.pattern === "ddos") multiplier = 3 + Math.random() * 2;

      const running = s.running;

      // Helper to dynamically calculate node capacity robustly
      function getNodeCapacity(n) {
        const kind = n.data.kind;
        let baseCap = n.data.throughput !== undefined && n.data.throughput !== "" ? Number(n.data.throughput) : 1500;
        if (["postgresql", "mysql", "mongodb"].includes(kind)) {
          const rCap = n.data.readCapacity !== undefined && n.data.readCapacity !== "" ? Number(n.data.readCapacity) : 2000;
          const wCap = n.data.writeCapacity !== undefined && n.data.writeCapacity !== "" ? Number(n.data.writeCapacity) : 500;
          baseCap = rCap + wCap;
        }
        if (isNaN(baseCap) || baseCap <= 0) baseCap = 100;
        const reps = Number(n.data.replicas ?? 1);
        return baseCap * (isNaN(reps) || reps <= 0 ? 1 : reps);
      }

      // 1. Build adjacency list
      const adj = {};
      const revAdj = {};
      currentNodes.forEach((n) => {
        adj[n.id] = [];
        revAdj[n.id] = [];
      });
      currentEdges.forEach((e) => {
        if (adj[e.source] && adj[e.target]) {
          adj[e.source].push({ targetId: e.target, edgeId: e.id });
          revAdj[e.target].push({ sourceId: e.source, edgeId: e.id });
        }
      });

      // 2. Identify client nodes and generate load
      const clientKinds = ["client", "mobile", "web", "client-cluster"];
      const clientNodes = currentNodes.filter((n) => clientKinds.includes(n.data.kind));
      
      const nodeTrafficReceived = {};
      const nodeOwnErrorRate = {};
      const nodeErrorRate = {};
      const nodeOwnLatency = {};
      const edgeTraffic = {};

      currentNodes.forEach((n) => {
        nodeTrafficReceived[n.id] = 0;
        nodeOwnErrorRate[n.id] = 0;
        nodeErrorRate[n.id] = 0;
      });

      // Populate entry node traffic
      const entryNodes = currentNodes.filter((n) => revAdj[n.id].length === 0);
      if (clientNodes.length > 0) {
        // Distribute or scale the slider's userLoad proportionally based on client properties
        const totalConfiguredLoad = clientNodes.reduce((sum, c) => {
          return sum + (c.data.concurrentUsers ?? 1000) * (c.data.requestRate ?? 5);
        }, 0);

        clientNodes.forEach((c) => {
          const clientConfiguredLoad = (c.data.concurrentUsers ?? 1000) * (c.data.requestRate ?? 5);
          const share = totalConfiguredLoad > 0 ? (clientConfiguredLoad / totalConfiguredLoad) : (1 / clientNodes.length);
          const load = s.userLoad * share;
          nodeTrafficReceived[c.id] = running ? load * multiplier : 0;
        });
      } else {
        // Fallback: divide userLoad among all entry nodes
        const baseFallbackLoad = entryNodes.length > 0 ? (s.userLoad * multiplier) / entryNodes.length : 0;
        entryNodes.forEach((n) => {
          nodeTrafficReceived[n.id] = running ? baseFallbackLoad : 0;
        });
      }

      // 4. Topological Sort
      const sortedNodeIds = [];
      const visitedSort = new Set();
      const tempSort = new Set();

      function visit(nodeId) {
        if (tempSort.has(nodeId)) return; // cycle check
        if (visitedSort.has(nodeId)) return;
        tempSort.add(nodeId);
        const targets = adj[nodeId] || [];
        targets.forEach((t) => visit(t.targetId));
        tempSort.delete(nodeId);
        visitedSort.add(nodeId);
        sortedNodeIds.unshift(nodeId);
      }

      currentNodes.forEach((n) => {
        if (!visitedSort.has(n.id)) {
          visit(n.id);
        }
      });

      // Define which kinds split vs propagate fully
      const splitKinds = ["load-balancer", "api-gateway", "dns", "reverse-proxy"];

      // 5. Downstream traffic propagation pass
      sortedNodeIds.forEach((uId) => {
        const u = currentNodes.find((n) => n.id === uId);
        if (!u) return;

        const isFailed = (f && f.nodeId === uId) || u.data.enabled === false;
        const kind = u.data.kind;

        // Calculate node's own error rate based on overload
        let ownErrorRate = 0;
        if (isFailed) {
          ownErrorRate = 100;
        } else if (!clientKinds.includes(kind)) {
          // Client nodes generate traffic rather than process it, so they cannot be overloaded
          const cap = getNodeCapacity(u);
          const traffic = nodeTrafficReceived[uId];
          const loadRatio = cap > 0 ? traffic / cap : 0;
          if (loadRatio > 1.0) {
            ownErrorRate = Math.min(100, Math.round((loadRatio - 1.0) * 40));
          }
          if (kind === "api-gateway") {
            const rateLimit = (u.data.rateLimit || 3000) * (u.data.replicas || 1);
            if (traffic > rateLimit) {
              const droppedTraffic = traffic - rateLimit;
              const rateLimitError = (droppedTraffic / traffic) * 100;
              ownErrorRate = Math.min(100, ownErrorRate + Math.round(rateLimitError));
            }
          }
        }
        nodeOwnErrorRate[uId] = ownErrorRate;

        // Determine traffic to send downstream
        const traffic = nodeTrafficReceived[uId];
        let trafficSent = traffic;
        if (isFailed) {
          trafficSent = 0;
        } else {
          if (kind === "cdn") {
            trafficSent = traffic * 0.10; // 90% cache hits
          } else if (kind === "redis") {
            trafficSent = traffic * 0.15; // 85% cache hits
          } else if (kind === "api-gateway") {
            const rateLimit = (u.data.rateLimit || 3000) * (u.data.replicas || 1);
            trafficSent = Math.min(traffic, rateLimit);
          }
        }

        // Check targets to see if Redis cache is present alongside database
        const targets = adj[uId] || [];
        const targetNodes = targets.map(t => currentNodes.find(n => n.id === t.targetId)).filter(Boolean);
        const hasCacheTarget = targetNodes.some(n => n.data.kind === "redis");

        if (targets.length > 0) {
          const isSplit = splitKinds.includes(kind);
          targets.forEach((targetObj) => {
            const targetNode = currentNodes.find(n => n.id === targetObj.targetId);
            let edgeVal = trafficSent;

            if (isSplit) {
              edgeVal = trafficSent / targets.length;
            } else {
              if (targetNode && ["postgresql", "mysql", "mongodb"].includes(targetNode.data.kind) && hasCacheTarget) {
                // Redis absorbs 85% of reads
                edgeVal = trafficSent * 0.15;
              }
            }

            edgeTraffic[targetObj.edgeId] = edgeVal;
            nodeTrafficReceived[targetObj.targetId] += edgeVal;
          });
        }
      });

      // 6. Calculate own node latencies
      currentNodes.forEach((u) => {
        const isFailed = (f && f.nodeId === u.id) || u.data.enabled === false;
        const cap = getNodeCapacity(u);
        const traffic = nodeTrafficReceived[u.id];
        const loadRatio = cap > 0 ? traffic / cap : 0;

        let baseLat = u.data.latency || 20;
        if (isFailed) {
          nodeOwnLatency[u.id] = 500;
          return;
        }

        const kind = u.data.kind;
        if (clientKinds.includes(kind)) {
          // Client nodes have 0 internal latency contribution
          nodeOwnLatency[u.id] = 0;
          return;
        }

        if (kind === "cdn") baseLat = 5;
        if (kind === "redis") baseLat = 1;
        if (kind === "api-gateway") baseLat = 5;
        if (kind === "dns") baseLat = 2;

        let latency = baseLat;
        if (loadRatio > 0.8) {
          latency = Math.round(baseLat * (1 + Math.max(0, loadRatio - 0.7) * 4));
        }
        if (["postgresql", "mysql", "mongodb"].includes(kind) && loadRatio > 1.0) {
          latency = Math.round(baseLat * (1 + Math.pow(loadRatio, 3) * 5));
        }

        // Cap latency at 10000ms to represent query timeout and prevent overflow layout bugs
        nodeOwnLatency[u.id] = Math.min(10000, latency);
      });

      // 7. Calculate response error rate recursively (upstream propagation)
      const memoResponseErrorRate = {};
      function getResponseErrorRate(nodeId, visited = new Set()) {
        if (visited.has(nodeId)) return 0;
        if (memoResponseErrorRate[nodeId] !== undefined) {
          return memoResponseErrorRate[nodeId];
        }

        const node = currentNodes.find((n) => n.id === nodeId);
        if (!node) return 0;

        visited.add(nodeId);
        const ownErr = nodeOwnErrorRate[nodeId] || 0;
        const targets = adj[nodeId] || [];

        if (targets.length === 0) {
          memoResponseErrorRate[nodeId] = ownErr;
          visited.delete(nodeId);
          return ownErr;
        }

        const kind = node.data.kind;
        const isSplit = splitKinds.includes(kind);

        let downstreamErr = 0;
        if (targets.length > 0) {
          const targetErrs = targets.map((t) => getResponseErrorRate(t.targetId, visited));
          if (isSplit) {
            downstreamErr = targetErrs.reduce((a, b) => a + b, 0) / targets.length;
          } else {
            // Query node error rate is max of targets (if any critical target fails, query fails)
            // Note: redis failures bypass request failure since query falls back directly to the DB.
            const criticalTargetErrs = targets
              .filter((t) => {
                const dest = currentNodes.find((n) => n.id === t.targetId);
                return dest && dest.data.kind !== "redis";
              })
              .map((t) => getResponseErrorRate(t.targetId, visited));
            
            downstreamErr = criticalTargetErrs.length > 0 ? Math.max(...criticalTargetErrs) : 0;
          }
        }

        const totalErr = Math.min(100, Math.round(ownErr + (1 - ownErr / 100) * downstreamErr));
        memoResponseErrorRate[nodeId] = totalErr;

        visited.delete(nodeId);
        return totalErr;
      }

      currentNodes.forEach((n) => {
        nodeErrorRate[n.id] = getResponseErrorRate(n.id);
      });

      // 8. Calculate response latency recursively (upstream path accumulation)
      const memoResponseLatency = {};
      function getResponseLatency(nodeId, visited = new Set()) {
        if (visited.has(nodeId)) return 0;
        if (memoResponseLatency[nodeId] !== undefined) {
          return memoResponseLatency[nodeId];
        }

        const node = currentNodes.find((n) => n.id === nodeId);
        if (!node) return 0;

        visited.add(nodeId);
        const ownLat = nodeOwnLatency[nodeId] || 20;
        const targets = adj[nodeId] || [];

        if (targets.length === 0) {
          memoResponseLatency[nodeId] = ownLat;
          visited.delete(nodeId);
          return ownLat;
        }

        const kind = node.data.kind;
        let res = ownLat;
        if (kind === "cdn") {
          const targetLats = targets.map((t) => getResponseLatency(t.targetId, visited));
          const maxTargetLat = targetLats.length > 0 ? Math.max(...targetLats) : 0;
          res = Math.round(0.90 * ownLat + 0.10 * (ownLat + maxTargetLat));
        } else if (kind === "redis") {
          const targetLats = targets.map((t) => getResponseLatency(t.targetId, visited));
          const maxTargetLat = targetLats.length > 0 ? Math.max(...targetLats) : 0;
          res = Math.round(0.85 * ownLat + 0.15 * (ownLat + maxTargetLat));
        } else {
          const targetLats = targets.map((t) => getResponseLatency(t.targetId, visited));
          const maxTargetLat = targetLats.length > 0 ? Math.max(...targetLats) : 0;
          res = ownLat + maxTargetLat;
        }

        res = Math.min(10000, res); // Cap response latency at 10s timeout
        memoResponseLatency[nodeId] = res;

        visited.delete(nodeId);
        return res;
      }

      // 9. Overall metrics calculations
      const targetNodesForMetrics = clientNodes.length > 0 ? clientNodes : entryNodes;
      const nodesWithTraffic = targetNodesForMetrics.filter((n) => nodeTrafficReceived[n.id] > 0);

      let avgLatency = 0;
      if (nodesWithTraffic.length > 0) {
        const totalLat = nodesWithTraffic.reduce((sum, n) => sum + getResponseLatency(n.id), 0);
        avgLatency = Math.round(totalLat / nodesWithTraffic.length);
      } else if (targetNodesForMetrics.length > 0) {
        const totalLat = targetNodesForMetrics.reduce((sum, n) => sum + getResponseLatency(n.id), 0);
        avgLatency = Math.round(totalLat / targetNodesForMetrics.length);
      }

      let avgErrorRate = 0;
      if (nodesWithTraffic.length > 0) {
        const totalErr = nodesWithTraffic.reduce((sum, n) => sum + nodeErrorRate[n.id], 0);
        avgErrorRate = totalErr / nodesWithTraffic.length;
      } else if (targetNodesForMetrics.length > 0) {
        const totalErr = targetNodesForMetrics.reduce((sum, n) => sum + nodeErrorRate[n.id], 0);
        avgErrorRate = totalErr / targetNodesForMetrics.length;
      }

      let costHr = 0;
      currentNodes.forEach((n) => {
        const cost = n.data.hourlyCost !== undefined && n.data.hourlyCost !== "" ? Number(n.data.hourlyCost) : 0;
        const reps = n.data.replicas !== undefined && n.data.replicas !== "" ? Number(n.data.replicas) : 1;
        costHr += (isNaN(cost) ? 0 : cost) * (isNaN(reps) || reps <= 0 ? 1 : reps);
      });

      // Sum client throughput or fallback entry point throughput
      let totalSystemThroughput = 0;
      currentNodes.forEach((n) => {
        if (clientNodes.length > 0) {
          if (clientKinds.includes(n.data.kind)) {
            totalSystemThroughput += nodeTrafficReceived[n.id] || 0;
          }
        } else {
          if (revAdj[n.id].length === 0) {
            totalSystemThroughput += nodeTrafficReceived[n.id] || 0;
          }
        }
      });

      // 10. Map to Redux node updates
      const updated = currentNodes.map((n) => {
        const traffic = nodeTrafficReceived[n.id] || 0;
        const errRate = nodeErrorRate[n.id] || 0;
        const latency = nodeOwnLatency[n.id] || 20;

        const isFailed = (f && f.nodeId === n.id) || n.data.enabled === false;
        const cap = getNodeCapacity(n);
        const loadRatio = cap > 0 ? traffic / cap : 0;

        const cpu = Math.min(100, Math.round(loadRatio * 90 + (running ? 8 : 4)));
        const memory = Math.min(100, Math.round(loadRatio * 70 + 20));

        const health = isFailed || loadRatio > 1.1 || errRate > 50 ? "critical" : loadRatio > 0.8 ? "warning" : "healthy";

        return {
          ...n,
          data: {
            ...n.data,
            cpu,
            memory,
            latency,
            health,
            activeThroughput: traffic, // current active throughput (req/s)
            errorRate: errRate,
          },
        };
      });

      const health =
        avgErrorRate > 5 || updated.some((n) => n.data.health === "critical")
          ? "Critical"
          : updated.some((n) => n.data.health === "warning")
            ? "Warning"
            : "Healthy";

      dispatch(setNodesAction(updated));
      dispatch(
        setEdgesAction(
          currentEdges.map((e) => {
            const target = updated.find((n) => n.id === e.target);
            const h = target?.data.health || "healthy";
            const trafficVal = edgeTraffic[e.id] || 0;
            return {
              ...e,
              animated: running && trafficVal > 0,
              data: {
                ...e.data,
                health: h,
                metric: running ? Math.round(trafficVal) : 0,
              },
            };
          }),
        ),
      );

      dispatch(
        setMetrics({
          throughput: Math.round(running ? totalSystemThroughput : 0),
          latency: avgLatency,
          errorRate: avgErrorRate,
          costHr,
          health,
        }),
      );
    }, 900);
    return () => clearInterval(id);
  }, [sim.running, !!failure, dispatch]);
}

// ---------- Suggestions ----------
function useSuggestions() {
  const nodes = useSelector((s) => s.simulator.nodes);
  const edges = useSelector((s) => s.simulator.edges);
  const metrics = useSelector((s) => s.simulator.metrics);

  return useMemo(() => {
    const out = [];
    const has = (kind) => nodes.some((n) => n.data.kind === kind);
    if (!has("load-balancer"))
      out.push({
        title: "Add Load Balancer",
        detail: "Distribute traffic to prevent single-instance overload.",
        impact: { latency: "-30%", throughput: "+2x", cost: "+$8/hr" },
      });
    if (
      !has("redis") &&
      nodes.some((n) => ["postgresql", "mysql", "mongodb"].includes(n.data.kind))
    )
      out.push({
        title: "Add Redis Cache",
        detail: "Cache hot reads in front of the database.",
        impact: { latency: "-60%", throughput: "+3x", cost: "+$10/hr" },
      });
    if (!has("cdn") && nodes.some((n) => n.data.kind === "client"))
      out.push({
        title: "Add CDN",
        detail: "Serve static assets from the edge.",
        impact: { latency: "-40%", throughput: "+5x", cost: "+$6/hr" },
      });
    if (!has("kafka") && !has("queue"))
      out.push({
        title: "Introduce Kafka",
        detail: "Decouple services with an event log for spiky workloads.",
        impact: { latency: "neutral", throughput: "+4x", cost: "+$25/hr" },
      });
    nodes.forEach((n) => {
      if (
        ["microservice", "app-server", "web-server"].includes(n.data.kind) &&
        (n.data.replicas || 1) < 3
      ) {
        out.push({
          title: `Scale ${n.data.label}`,
          detail: `Increase replicas to handle bursts and remove SPOFs.`,
          impact: {
            latency: "-20%",
            throughput: "+2x",
            cost: `+$${(n.data.hourlyCost || 10) * 2}/hr`,
          },
        });
      }
    });
    if (metrics.errorRate > 1)
      out.push({
        title: "Investigate hot bottleneck",
        detail: "Error rate above target — focus on critical nodes.",
        impact: { latency: "TBD", throughput: "TBD", cost: "TBD" },
      });
    return out.slice(0, 6);
  }, [nodes, edges, metrics.errorRate]);
}

// ---------- Challenge picker ----------
function ChallengePicker({ onPick, onPickTemplate, customChallenges = [], customTemplates = [], loading, userProgress = {} }) {
  const user = useSelector((s) => s.user?.user);
  const [tab, setTab] = useState("challenges"); // "challenges" | "practice"
  const [q, setQ] = useState("");
  const [diff, setDiff] = useState("all");
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState("recommended");

  const finalChallenges = customChallenges.length > 0 ? customChallenges : challenges;
  const all = useMemo(() => [blankChallenge, ...finalChallenges], [customChallenges]);

  // Enrich challenges with metadata for a better UI experience
  const enrichedChallenges = useMemo(() => {
    const data = {
      "url-shortener": { duration: "30m", popularity: 94, attempts: 2420, completion: 82, lastAttempted: "2 days ago", type: "System Design", date: "2026-05-15" },
      "video-streaming": { duration: "45m", popularity: 88, attempts: 1850, completion: 45, lastAttempted: "1 week ago", type: "System Design", date: "2026-05-01" },
      "ride-sharing": { duration: "50m", popularity: 91, attempts: 1980, completion: 0, lastAttempted: "Not attempted", type: "Realtime Systems", date: "2026-04-20" },
      "chat-app": { duration: "35m", popularity: 96, attempts: 3200, completion: 74, lastAttempted: "Yesterday", type: "System Design", date: "2026-05-10" },
      "ecommerce": { duration: "40m", popularity: 92, attempts: 2100, completion: 0, lastAttempted: "Not attempted", type: "System Design", date: "2026-05-05" },
      "social-feed": { duration: "45m", popularity: 89, attempts: 1540, completion: 48, lastAttempted: "3 days ago", type: "System Design", date: "2026-04-25" },
      "blank": { duration: "Self-paced", popularity: 99, attempts: 5400, completion: 100, lastAttempted: "1 day ago", type: "Sandbox", date: "2026-01-01" }
    };
    
    return all.map(c => {
      const baseMeta = data[c.id] || { duration: "30m", popularity: 80, attempts: 500, completion: 0, lastAttempted: "Not attempted", type: "System Design", date: "2026-01-01" };
      const dynamicProgress = userProgress[c.id] || c.progress || "Not Started";
      return {
        ...baseMeta,
        ...c,
        progress: dynamicProgress
      };
    });
  }, [all, userProgress]);

  const finalTemplates = customTemplates.length > 0 ? customTemplates : templates;

  const enrichedTemplates = useMemo(() => {
    const categoriesMap = {
      "basic-web": "Basic",
      "ecommerce": "E-Commerce",
      "url-shortener": "Storage",
      "chat": "Messaging",
      "netflix": "Streaming",
      "instagram": "Social Media",
      "uber": "Distributed Systems",
      "whatsapp": "Messaging",
      "youtube": "Streaming",
      "ai-saas": "AI"
    };
    
    return finalTemplates.map(t => ({
      ...t,
      category: categoriesMap[t.id] || t.category || "Distributed Systems",
      description: t.description || `Prebuilt ${t.name} reference architecture. Tweak nodes, connect services, and simulate real load.`
    }));
  }, [customTemplates]);

  // Helper to map challenges to categories
  const getChallengeCategories = useCallback((ch) => {
    const list = ["Distributed Systems"];
    if (ch.tags.includes("Messaging") || ch.id === "chat-app") list.push("Messaging");
    if (ch.tags.includes("Feed") || ch.id === "social-feed" || ch.id === "ride-sharing") list.push("Social Media");
    if (ch.tags.includes("CDN") || ch.tags.includes("Encoding") || ch.id === "video-streaming") list.push("Streaming");
    if (ch.id === "ecommerce" || ch.tags.includes("Catalog") || ch.tags.includes("Orders") || ch.tags.includes("Payments")) list.push("E-Commerce");
    if (ch.tags.includes("Search") || ch.id === "ecommerce") list.push("Search");
    if (ch.tags.includes("Database") || ch.tags.includes("Storage") || ch.id === "url-shortener" || ch.id === "video-streaming" || ch.id === "social-feed") list.push("Storage");
    if (ch.tags.includes("CDN") || ch.id === "url-shortener" || ch.id === "video-streaming") list.push("CDN");
    return list;
  }, []);

  // Stats calculation
  const stats = useMemo(() => {
    const total = enrichedChallenges.length;
    const easy = enrichedChallenges.filter(c => c.difficulty === "Easy").length;
    const medium = enrichedChallenges.filter(c => c.difficulty === "Medium").length;
    const hard = enrichedChallenges.filter(c => c.difficulty === "Hard").length;
    const free = enrichedChallenges.filter(c => c.difficulty === "Free" || c.difficulty === "Template").length;
    
    const completed = enrichedChallenges.filter(c => c.progress === "Completed").length;
    const inProgress = enrichedChallenges.filter(c => c.progress === "In Progress").length;
    const notStarted = enrichedChallenges.filter(c => !c.progress || c.progress === "Not Started").length;

    return { total, easy, medium, hard, free, completed, inProgress, notStarted };
  }, [enrichedChallenges]);

  // Featured challenge
  const featuredChallenge = useMemo(() => {
    return enrichedChallenges.find(c => c.id === "url-shortener");
  }, [enrichedChallenges]);

  // Filtering challenges
  const filteredChallenges = useMemo(() => {
    return enrichedChallenges.filter((ch) => {
      // Difficulty filter
      if (diff !== "all" && ch.difficulty !== diff) return false;
      
      // Category filter
      if (category !== "all") {
        const cats = getChallengeCategories(ch);
        if (!cats.includes(category)) return false;
      }
      
      // Search text filter
      if (q) {
        const term = q.toLowerCase();
        const matchTitle = ch.title.toLowerCase().includes(term);
        const matchBrief = ch.brief.toLowerCase().includes(term);
        const matchTags = ch.tags.some(t => t.toLowerCase().includes(term));
        const matchCats = getChallengeCategories(ch).some(c => c.toLowerCase().includes(term));
        if (!matchTitle && !matchBrief && !matchTags && !matchCats) return false;
      }
      
      return true;
    });
  }, [enrichedChallenges, diff, category, q, getChallengeCategories]);

  // Sorting challenges
  const sortedChallenges = useMemo(() => {
    let list = [...filteredChallenges];
    
    if (sort === "popular") {
      list.sort((a, b) => (b.popularity || 0) - (a.popularity || 0));
    } else if (sort === "beginner") {
      const diffWeight = { "Easy": 1, "Medium": 2, "Hard": 3, "Free": 4 };
      list.sort((a, b) => (diffWeight[a.difficulty] || 99) - (diffWeight[b.difficulty] || 99));
    } else if (sort === "difficulty") {
      const diffWeight = { "Easy": 1, "Medium": 2, "Hard": 3, "Free": 4 };
      list.sort((a, b) => (diffWeight[a.difficulty] || 99) - (diffWeight[b.difficulty] || 99));
    } else if (sort === "newest") {
      list.sort((a, b) => new Date(b.date || "").getTime() - new Date(a.date || "").getTime());
    } else {
      // "recommended" - custom order: Blank canvas last
      list.sort((a, b) => {
        if (a.id === "blank") return 1;
        if (b.id === "blank") return -1;
        return (b.popularity || 0) - (a.popularity || 0); // then by popularity
      });
    }
    return list;
  }, [filteredChallenges, sort]);

  // Exclude featured challenge from grid list when displaying in the featured section
  const displayChallenges = useMemo(() => {
    const showFeatured = category === "all" && diff === "all" && !q && featuredChallenge;
    if (showFeatured) {
      return sortedChallenges.filter(c => c.id !== featuredChallenge.id);
    }
    return sortedChallenges;
  }, [sortedChallenges, category, diff, q, featuredChallenge]);

  // Filtering templates
  const filteredTemplates = useMemo(() => {
    return enrichedTemplates.filter((t) => {
      // Category filter
      if (category !== "all" && t.category !== category && category !== "Distributed Systems") {
        if (category === "Social Media" && t.category !== "Social Media") return false;
        if (category === "Messaging" && t.category !== "Messaging") return false;
        if (category === "Streaming" && t.category !== "Streaming") return false;
        if (category === "E-Commerce" && t.category !== "E-Commerce") return false;
        if (category === "Storage" && t.category !== "Storage") return false;
        if (category === "CDN" && t.category !== "CDN" && t.category !== "Streaming" && t.category !== "Social Media") return false;
        if (t.category !== category) return false;
      }

      // Search text filter
      if (q) {
        const term = q.toLowerCase();
        const matchName = t.name.toLowerCase().includes(term);
        const matchDesc = t.description.toLowerCase().includes(term);
        const matchCategory = t.category.toLowerCase().includes(term);
        if (!matchName && !matchDesc && !matchCategory) return false;
      }

      return true;
    });
  }, [enrichedTemplates, category, q]);

  const categories = [
    "Messaging",
    "Social Media",
    "Streaming",
    "E-Commerce",
    "Search",
    "Storage",
    "CDN",
    "Distributed Systems"
  ];

  if (loading) {
    return (
      <AppShell>
        <PageHeader
          title="System Design Simulator"
          description="Design and simulate scalable distributed systems."
        />
        <div className="px-4 py-6 md:px-8 max-w-7xl mx-auto space-y-6 animate-pulse">
          {/* Quick Stats Grid Skeleton */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
            {Array.from({ length: 7 }).map((_, i) => (
              <div key={i} className="h-[74px] rounded-xl border border-border bg-card/30 p-4" />
            ))}
          </div>
          {/* Tabs skeleton */}
          <div className="h-10 w-64 border-b border-border" />
          {/* Filters skeleton */}
          <div className="h-16 w-full rounded-xl border border-border bg-card/40" />
          {/* Category Filter Chips skeleton */}
          <div className="flex flex-wrap gap-2">
            <div className="h-7 w-24 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-20 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-28 rounded-full bg-zinc-800/40" />
            <div className="h-7 w-20 rounded-full bg-zinc-800/40" />
          </div>
          {/* Featured Challenge skeleton */}
          <div className="h-[140px] rounded-xl border border-border bg-card/30 p-6" />
          {/* Content Grid skeleton */}
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-[160px] rounded-xl border border-border bg-card/30 p-5 flex flex-col justify-between" />
            ))}
          </div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader
        title="System Design Simulator"
        description="Design and simulate scalable distributed systems."
        actions={
          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1.5 border-r border-border pr-4">
              <span className="font-semibold text-foreground">{stats.total}</span> Challenges
            </div>
            <div className="flex items-center gap-1.5 border-r border-border pr-4">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="font-semibold text-foreground">{stats.easy}</span> Easy
            </div>
            <div className="flex items-center gap-1.5 border-r border-border pr-4">
              <span className="h-2 w-2 rounded-full bg-amber-500" />
              <span className="font-semibold text-foreground">{stats.medium}</span> Medium
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-red-500" />
              <span className="font-semibold text-foreground">{stats.hard}</span> Hard
            </div>
          </div>
        }
      />

      <div className="px-4 py-6 md:px-8 max-w-7xl mx-auto">
        {/* Quick Stats Grid */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7 mb-6">
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground">Challenges</div>
            <div className="mt-1 text-2xl font-bold font-mono">{stats.total}</div>
          </div>
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-success animate-pulse" /> Easy
            </div>
            <div className="mt-1 text-2xl font-bold text-success font-mono">{stats.easy}</div>
          </div>
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-warning animate-pulse" /> Medium
            </div>
            <div className="mt-1 text-2xl font-bold text-warning font-mono">{stats.medium}</div>
          </div>
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-destructive animate-pulse" /> Hard
            </div>
            <div className="mt-1 text-2xl font-bold text-destructive font-mono">{stats.hard}</div>
          </div>
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground">Completed</div>
            <div className="mt-1 text-2xl font-bold text-emerald-500 font-mono">{stats.completed}</div>
          </div>
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground">In Progress</div>
            <div className="mt-1 text-2xl font-bold text-amber-500 font-mono">{stats.inProgress}</div>
          </div>
          <div className="rounded-xl border border-border bg-card p-4">
            <div className="text-xs text-muted-foreground">Not Started</div>
            <div className="mt-1 text-2xl font-bold text-muted-foreground font-mono">{stats.notStarted}</div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6 flex border-b border-border">
          <button
            onClick={() => {
              setTab("challenges");
              setCategory("all");
            }}
            className={cn(
              "pb-3 px-4 text-sm font-medium border-b-2 transition-colors cursor-pointer",
              tab === "challenges"
                ? "border-primary text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground"
            )}
          >
            Challenges
          </button>
          <button
            onClick={() => {
              setTab("practice");
              setCategory("all");
            }}
            className={cn(
              "pb-3 px-4 text-sm font-medium border-b-2 transition-colors cursor-pointer",
              tab === "practice"
                ? "border-primary text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground"
            )}
          >
            Practice / Templates
          </button>
        </div>

        {/* Filters */}
        <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-3 md:flex-row md:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <UiInput
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search by title, tags, or concepts..."
              className="h-9 border-transparent bg-background pl-9"
            />
          </div>
          {tab === "challenges" && (
            <div className="flex flex-wrap items-center gap-2">
              <UiSelect value={diff} onValueChange={setDiff}>
                <SelectTrigger className="h-9 w-[150px]">
                  <SelectValue placeholder="Difficulty" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Any difficulty</SelectItem>
                  <SelectItem value="Easy">Easy</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="Hard">Hard</SelectItem>
                </SelectContent>
              </UiSelect>

              <UiSelect value={sort} onValueChange={setSort}>
                <SelectTrigger className="h-9 w-[160px]">
                  <SelectValue placeholder="Sort" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="recommended">Recommended</SelectItem>
                  <SelectItem value="popular">Most Popular</SelectItem>
                  <SelectItem value="beginner">Beginner Friendly</SelectItem>
                  <SelectItem value="difficulty">Difficulty</SelectItem>
                  <SelectItem value="newest">Newest</SelectItem>
                </SelectContent>
              </UiSelect>
            </div>
          )}
        </div>

        {/* Category Filter Chips */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <button
            onClick={() => setCategory("all")}
            className={cn(
              "rounded-full border px-3 py-1 text-xs transition-colors cursor-pointer",
              category === "all"
                ? "border-primary/50 bg-primary/10 text-foreground"
                : "border-border text-muted-foreground hover:text-foreground"
            )}
          >
            All Categories
          </button>
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setCategory(category === c ? "all" : c)}
              className={cn(
                "rounded-full border px-3 py-1 text-xs transition-colors cursor-pointer",
                category === c
                  ? "border-primary/50 bg-primary/10 text-foreground"
                  : "border-border text-muted-foreground hover:text-foreground"
              )}
            >
              {c}
            </button>
          ))}
          <span className="ml-auto text-xs text-muted-foreground">
            {tab === "challenges" ? sortedChallenges.length : filteredTemplates.length} matches
          </span>
        </div>

        {/* Featured Section */}
        {tab === "challenges" && category === "all" && diff === "all" && !q && featuredChallenge && (
          <div className="mt-6">
            <div className="mb-3 text-xs font-mono uppercase tracking-wider text-muted-foreground">Featured Challenge</div>
            <div
              onClick={() => onPick(featuredChallenge)}
              className="group block cursor-pointer"
            >
              <Card className="border-border bg-card p-6 transition-all hover:border-primary/40 hover:shadow-md">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-2 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md border border-border bg-muted/40 px-2 py-0.5 font-mono text-[10px] text-muted-foreground uppercase tracking-wider">
                        {featuredChallenge.type}
                      </span>
                      <DifficultyPill d={featuredChallenge.difficulty} />
                      <Badge variant="outline" className="border-primary/30 bg-primary/10 text-primary rounded-full font-mono text-[10px] uppercase tracking-wider">
                        Recommended Start
                      </Badge>
                    </div>
                    <h3 className="text-xl font-bold group-hover:text-primary transition-colors flex items-center gap-2">
                      {!user?.is_premium && <Lock className="h-4 w-4 text-[#FF6500] shrink-0" />}
                      <span>{featuredChallenge.title}</span>
                      {featuredChallenge.progress === "Completed" && (
                        <span className="h-2 w-2 rounded-full bg-emerald-500" title="Completed" />
                      )}
                      {featuredChallenge.progress === "In Progress" && (
                        <span className="h-2 w-2 rounded-full bg-amber-500" title="In Progress" />
                      )}
                    </h3>
                    <p className="text-sm text-muted-foreground max-w-3xl">
                      {featuredChallenge.brief}
                    </p>
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {featuredChallenge.tags.map((t) => (
                        <span
                          key={t}
                          className="rounded-md border border-border bg-muted/40 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex flex-col justify-between border-t border-border pt-4 md:border-t-0 md:border-l md:pt-0 md:pl-6 md:min-w-[200px] text-xs text-muted-foreground space-y-2">
                    <div className="flex justify-between items-center">
                      <span>Duration</span>
                      <span className="font-semibold text-foreground flex items-center gap-1">
                        <Clock className="h-3.5 w-3.5" />
                        {featuredChallenge.duration}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Attempts</span>
                      <span className="font-semibold text-foreground flex items-center gap-1">
                        <Users className="h-3.5 w-3.5" />
                        {featuredChallenge.attempts.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Status</span>
                      <span className="font-semibold text-foreground flex items-center gap-1.5">
                        {featuredChallenge.progress === "Completed" && <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />}
                        {featuredChallenge.progress === "In Progress" && <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />}
                        {featuredChallenge.progress === "Not Started" && <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground" />}
                        {featuredChallenge.progress}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Last Attempted</span>
                      <span className="font-semibold text-foreground">{featuredChallenge.lastAttempted}</span>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        )}

        {/* Content Grid */}
        {tab === "challenges" ? (
          <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {displayChallenges.map((ch) => (
              <div
                key={ch.id}
                onClick={() => onPick(ch)}
                className="group block cursor-pointer"
              >
                <Card className="h-full border-border bg-card p-5 transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-md flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-2">
                      <span className="rounded-md border border-border bg-muted/40 px-2 py-0.5 font-mono text-[10px] text-muted-foreground uppercase tracking-wider">
                        {ch.type}
                      </span>
                      {ch.difficulty === "Free" ? (
                        <Badge variant="outline" className="border-primary/30 bg-primary/10 text-primary rounded-full font-mono text-[10px] uppercase tracking-wider">
                          Sandbox
                        </Badge>
                      ) : (
                        <DifficultyPill d={ch.difficulty} />
                      )}
                    </div>
                    <h3 className="mt-3 text-base font-semibold leading-snug tracking-tight group-hover:text-primary transition-colors flex items-center justify-between gap-2">
                      <span className="flex items-center gap-1.5">
                        {ch.id !== "blank" && !user?.is_premium && <Lock className="h-3.5 w-3.5 text-[#FF6500] shrink-0" />}
                        <span>{ch.title}</span>
                      </span>
                      {ch.progress === "Completed" && (
                        <span className="h-2 w-2 rounded-full bg-emerald-500 shrink-0" title="Completed" />
                      )}
                      {ch.progress === "In Progress" && (
                        <span className="h-2 w-2 rounded-full bg-amber-500 shrink-0" title="In Progress" />
                      )}
                    </h3>
                    <p className="mt-2 line-clamp-3 text-sm text-muted-foreground">{ch.brief}</p>
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {ch.tags.map((t) => (
                        <span
                          key={t}
                          className="rounded-md border border-border bg-muted/40 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mt-4 flex items-center justify-between border-t border-border pt-3 text-xs text-muted-foreground">
                    <span className="inline-flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5" />
                      {ch.duration}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <Users className="h-3.5 w-3.5" />
                      {ch.attempts.toLocaleString()}
                    </span>
                    <span className="inline-flex items-center gap-1.5">
                      {ch.progress === "Completed" && <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />}
                      {ch.progress === "In Progress" && <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />}
                      {ch.progress === "Not Started" && <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground" />}
                      {ch.progress}
                    </span>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        ) : (
          <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {filteredTemplates.map((t) => (
              <div
                key={t.id}
                onClick={() => onPickTemplate(t)}
                className="group block cursor-pointer"
              >
                <Card className="h-full border-border bg-card p-5 transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-md flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-2">
                      <span className="rounded-md border border-border bg-muted/40 px-2 py-0.5 font-mono text-[10px] text-muted-foreground uppercase tracking-wider">
                        {t.category}
                      </span>
                      <Badge variant="outline" className="border-border bg-muted/20 text-muted-foreground rounded-full font-mono text-[10px] uppercase tracking-wider">
                        Template
                      </Badge>
                    </div>
                    <h3 className="mt-3 text-base font-semibold leading-snug tracking-tight group-hover:text-primary transition-colors flex items-center gap-1.5">
                      {!user?.is_premium && <Lock className="h-3.5 w-3.5 text-[#FF6500] shrink-0" />}
                      <span>{t.name}</span>
                    </h3>
                    <p className="mt-2 line-clamp-3 text-sm text-muted-foreground">{t.description}</p>
                  </div>

                  <div className="mt-4 flex items-center gap-2 border-t border-border pt-3">
                    <span className="rounded-md border border-border bg-muted/40 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
                      {t.nodes.length} nodes
                    </span>
                    <span className="rounded-md border border-border bg-muted/40 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
                      {t.edges.length} connections
                    </span>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {((tab === "challenges" && sortedChallenges.length === 0) || (tab === "practice" && filteredTemplates.length === 0)) && (
          <div className="mt-10 rounded-xl border border-dashed border-border p-10 text-center">
            <Badge variant="outline" className="mx-auto">No matches</Badge>
            <p className="mt-3 text-sm text-muted-foreground">Try clearing some filters.</p>
          </div>
        )}
      </div>
    </AppShell>
  );
}

// ---------- Page ----------
export default function SystemDesignSimulator() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [challenge, setChallenge] = useState(null);
  const [template, setTemplate] = useState(null);
  const user = useSelector((state) => state.user?.user);
  const [upgradeOpen, setUpgradeOpen] = useState(false);
  const [customChallenges, setCustomChallenges] = useState([]);
  const [customTemplates, setCustomTemplates] = useState([]);
  const [userProgress, setUserProgress] = useState({});
  const [userCanvas, setUserCanvas] = useState({});
  const [loading, setLoading] = useState(true);

  const challengeId = searchParams.get("c");
  const templateId = searchParams.get("t");

  const loadSystemDesign = useCallback(async () => {
    try {
      const response = await API.get("/system-design");
      if (response.data.challenges) setCustomChallenges(response.data.challenges);
      if (response.data.templates) setCustomTemplates(response.data.templates);
      if (response.data.userProgress) setUserProgress(response.data.userProgress);
      if (response.data.userCanvas) setUserCanvas(response.data.userCanvas);
      setLoading(false);
    } catch (err) {
      console.error("Failed to load system design API configurations", err);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSystemDesign();
  }, [loadSystemDesign]);

  // Re-fetch challenges/progress whenever returning to the picker (challenge becomes null)
  useEffect(() => {
    if (!challenge) {
      loadSystemDesign();
    }
  }, [challenge, loadSystemDesign]);

  useEffect(() => {
    if (challengeId && !challenge) {
      const pool = customChallenges.length > 0 ? customChallenges : challenges;
      const found = pool.find((c) => c.id === challengeId);
      if (found) {
        setChallenge(found);
        setTemplate(null);
      }
    }
  }, [challengeId, customChallenges, challenge]);

  useEffect(() => {
    if (templateId && !template && customTemplates.length > 0) {
      const found = customTemplates.find((t) => t.id === templateId);
      if (found) {
        if (!user?.is_premium) {
          setUpgradeOpen(true);
        } else {
          setTemplate(found);
          setChallenge({
            id: `tpl-${found.id}`,
            title: found.name,
            difficulty: "Template",
            tags: ["Practice"],
            brief:
              found.description ||
              `Prebuilt ${found.name} reference architecture. Study it, tweak nodes, or simulate load.`,
            requirements: found.requirements || [],
            hints: found.hints || [],
          });
        }
      }
    }
  }, [templateId, customTemplates, template, user]);

  const handlePickChallenge = (c) => {
    if (c.id !== "blank" && !user?.is_premium) {
      setUpgradeOpen(true);
    } else {
      setChallenge(c);
      setTemplate(null);
    }
  };

  const handlePickTemplate = (t) => {
    if (!user?.is_premium) {
      setUpgradeOpen(true);
    } else {
      setTemplate(t);
      setChallenge({
        id: `tpl-${t.id}`,
        title: t.name,
        difficulty: "Template",
        tags: ["Practice"],
        brief:
          t.description ||
          `Prebuilt ${t.name} reference architecture. Study it, tweak nodes, or simulate load.`,
        requirements: t.requirements || [],
        hints: t.hints || [],
      });
    }
  };

  return (
    <ReactFlowProvider>
      {!challenge ? (
        <>
          <ChallengePicker
            onPick={handlePickChallenge}
            onPickTemplate={handlePickTemplate}
            customChallenges={customChallenges}
            customTemplates={customTemplates}
            loading={loading}
            userProgress={userProgress}
          />
          <UpgradeModal open={upgradeOpen} onOpenChange={setUpgradeOpen} />
        </>
      ) : (
        <Workspace
          challenge={challenge}
          template={template}
          userCanvas={userCanvas}
          onExit={() => {
            setChallenge(null);
            setTemplate(null);
            setSearchParams({});
          }}
        />
      )}
    </ReactFlowProvider>
  );
}

function Workspace({ challenge, template, userCanvas, onExit }) {
  const dispatch = useDispatch();
  const rf = useReactFlow();
  const nodes = useSelector((s) => s.simulator.nodes);
  const edges = useSelector((s) => s.simulator.edges);
  const [showGrid, setShowGrid] = useState(true);
  const [showMetrics, setShowMetrics] = useState(true);
  const [briefOpen, setBriefOpen] = useState(true);

  const containerRef = useRef(null);
  const [leftW, setLeftW] = useState(320);
  const [rightW, setRightW] = useState(320);
  const MIN_COL = 200;

  const [currentProgress, setCurrentProgress] = useState(challenge.progress || "Not Started");

  const getW = () => containerRef.current?.offsetWidth ?? window.innerWidth;

  const onDragLeft = useCallback((delta) => {
    setLeftW((w) => Math.max(MIN_COL, Math.min(w + delta, getW() - MIN_COL * 2)));
  }, []);

  const onDragRight = useCallback((delta) => {
    setRightW((w) => Math.max(MIN_COL, Math.min(w - delta, getW() - MIN_COL * 2)));
  }, []);

  // Load saved canvas layout from DB, template architecture, or start with empty.
  useEffect(() => {
    if (challenge && userCanvas && userCanvas[challenge.id]) {
      const saved = userCanvas[challenge.id];
      dispatch(loadTemplate({ nodes: saved.nodes, edges: saved.edges }));
    } else if (template) {
      dispatch(loadTemplate({ nodes: template.nodes, edges: template.edges }));
    } else {
      dispatch(clearCanvas());
    }
  }, [challenge?.id, template, userCanvas, dispatch]);

  // Debounced auto-save of custom canvas state (nodes & edges) to MongoDB
  const autoSaveTimeoutRef = useRef(null);
  useEffect(() => {
    if (!challenge || challenge.id === "blank") return;

    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }

    autoSaveTimeoutRef.current = setTimeout(async () => {
      try {
        await API.post("/system-design/canvas", {
          challenge_id: challenge.id,
          nodes,
          edges,
        });
      } catch (err) {
        console.error("Failed to auto-save system design canvas", err);
      }
    }, 2000);

    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [nodes, edges, challenge?.id]);

  // Synchronize state from props
  useEffect(() => {
    if (challenge.progress) {
      setCurrentProgress(challenge.progress);
    }
  }, [challenge.progress]);

  // Automatically start challenge if it was "Not Started"
  useEffect(() => {
    const autoStart = async () => {
      if (challenge && challenge.id && (challenge.progress === "Not Started" || !challenge.progress)) {
        try {
          const response = await API.post("/system-design/progress", {
            challenge_id: challenge.id,
            progress: "In Progress"
          });
          if (response.data.success) {
            setCurrentProgress("In Progress");
          }
        } catch (err) {
          console.error("Failed to automatically mark challenge as In Progress", err);
        }
      }
    };
    autoStart();
  }, [challenge]);

  const handleToggleCompletion = async () => {
    const nextProgress = currentProgress === "Completed" ? "In Progress" : "Completed";
    try {
      const response = await API.post("/system-design/progress", {
        challenge_id: challenge.id,
        progress: nextProgress
      });
      if (response.data.success) {
        setCurrentProgress(nextProgress);
        if (nextProgress === "Completed") {
          toast.success("Challenge marked as Completed! +100 XP");
        } else {
          toast.success("Challenge status reset to In Progress");
        }
      }
    } catch (err) {
      console.error("Failed to update challenge progress", err);
      toast.error("Failed to update challenge status");
    }
  };

  useSimulationEngine();
  const suggestions = useSuggestions();

  const injectFailure = () => {
    const candidates = nodes.filter((n) => !["client", "mobile", "web"].includes(n.data.kind));
    if (!candidates.length) return;
    const pick = candidates[Math.floor(Math.random() * candidates.length)];
    dispatch(setFailure({ nodeId: pick.id, type: "outage" }));
    setTimeout(() => dispatch(setFailure(null)), 8000);
  };

  return (
    <div ref={containerRef} className="fixed inset-0 flex flex-col bg-[#0A0A0A] text-white">
      <div className="flex items-center justify-between gap-3 border-b border-white/[0.08] bg-[#0d0d0d] px-3 py-2">
        <div className="flex min-w-0 items-center gap-2">
          <button
            onClick={onExit}
            className="inline-flex items-center gap-1 rounded-md border border-white/10 bg-[#161616] px-2 py-1 text-[11px] text-white/80 hover:border-white/25 hover:text-white"
          >
            <ArrowLeft className="h-3.5 w-3.5" />
            Back
          </button>

          <div className="ml-2 truncate text-[12px] font-semibold">{challenge.title}</div>

          <span className="rounded-md border border-white/10 bg-black/40 px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-widest text-white/55 mr-1">
            {challenge.difficulty}
          </span>

          {currentProgress === "Completed" ? (
            <button
              onClick={handleToggleCompletion}
              className="inline-flex items-center gap-1.5 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[11px] font-bold text-emerald-400 hover:bg-emerald-500/20 transition-all duration-300 cursor-pointer"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              Completed
            </button>
          ) : (
            <button
              onClick={handleToggleCompletion}
              className="inline-flex items-center gap-1.5 rounded-md border border-orange-500/30 bg-[#FF6500]/10 px-2 py-0.5 text-[11px] font-bold text-orange-400 hover:bg-[#FF6500]/20 transition-all duration-300 cursor-pointer"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-[#FF6500]" />
              Mark Completed
            </button>
          )}
        </div>

        <button
          onClick={() => setBriefOpen((o) => !o)}
          className="text-[11px] text-white/60 hover:text-white"
        >
          {briefOpen ? "Hide brief" : "Show brief"}
        </button>
      </div>

      <TopToolbar
        onFitView={() => rf.fitView({ padding: 0.25, duration: 300 })}
        onToggleGrid={() => setShowGrid((g) => !g)}
        showGrid={showGrid}
        onToggleMetrics={() => setShowMetrics((m) => !m)}
        onInjectFailure={injectFailure}
      />

      <div className="flex min-h-0 flex-1">
        <ComponentLibrary width={leftW} />

        <DragHandle onDelta={onDragLeft} />

        <div className="relative min-w-0 flex-1">
          <CanvasInner showGrid={showGrid} showMetrics={showMetrics} suggestions={suggestions} />

          {/* <OptimizationAssistant suggestions={suggestions} /> */}

          <AnimatePresence>
            {briefOpen && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                className="pointer-events-auto absolute left-4 top-4 z-20 w-[340px] rounded-xl border border-white/10 bg-[#111111]/95 backdrop-blur p-3"
              >
                <div className="flex items-center justify-between">
                  <div className="font-mono text-[10px] uppercase tracking-widest text-white/45">
                    Challenge Brief
                  </div>

                  <button
                    onClick={() => setBriefOpen(false)}
                    className="text-white/40 hover:text-white"
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                </div>

                <div className="mt-2 text-[13px] font-semibold">{challenge.title}</div>

                <div className="mt-1 text-[12px] text-white/65">{challenge.brief}</div>

                {challenge.requirements?.length > 0 && (
                  <div className="mt-3">
                    <div className="font-mono text-[10px] uppercase tracking-widest text-white/45">
                      Requirements
                    </div>

                    <ul className="mt-1 space-y-1 text-[12px] text-white/75">
                      {challenge.requirements.map((r, i) => (
                        <li key={i} className="flex gap-2">
                          <span className="text-[#FF6500]">›</span>
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {challenge.hints?.length > 0 && (
                  <div className="mt-3">
                    <div className="font-mono text-[10px] uppercase tracking-widest text-white/45">
                      Hints
                    </div>

                    <ul className="mt-1 space-y-1 text-[12px] text-white/60">
                      {challenge.hints.map((h, i) => (
                        <li key={i} className="flex gap-2">
                          <Sparkles className="mt-0.5 h-3 w-3 text-[#FF6500]" />
                          {h}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {nodes.length === 0 && (
                  <div className="mt-3 rounded-md border border-dashed border-white/15 bg-black/30 p-2 text-[11px] text-white/55">
                    Drag any component from the left panel onto the empty canvas to begin. Connect
                    them by dragging from the orange dots on each node.
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <DragHandle onDelta={onDragRight} />

        <Panel style={{ width: rightW }} className="shrink-0 border-l h-full">
          <div className="flex h-full flex-col">
            <div className="border-b border-white/[0.08]">
              <MetricsPanel />
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto">
              <PropertiesPanel />
            </div>
          </div>
        </Panel>
      </div>
    </div>
  );
}
