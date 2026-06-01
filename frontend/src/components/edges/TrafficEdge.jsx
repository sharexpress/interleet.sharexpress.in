import { BaseEdge, EdgeLabelRenderer, getBezierPath } from "reactflow";

const KIND_COLOR = {
  request: "#FF6500",
  database: "#4FB286",
  cache: "#F2C14E",
  queue: "#B8B8B8",
  event: "#A78BFA",
};
const HEALTH_COLOR = { healthy: "#22C55E", warning: "#F59E0B", critical: "#EF4444" };

function TrafficEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data, selected, animated }) {
  const [path, labelX, labelY] = getBezierPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition });
  const kind = data?.kind || "request";
  const health = data?.health;
  const stroke = health ? HEALTH_COLOR[health] : (selected ? KIND_COLOR[kind] : "rgba(255,255,255,0.22)");
  const label = data?.label || (data?.metric ? `${data.metric} req/s` : null);

  return (
    <>
      <BaseEdge id={id} path={path} style={{ stroke, strokeWidth: selected ? 2.4 : 1.6 }} />
      {animated && (
        <circle r="3" fill={stroke}>
          <animateMotion dur="2.2s" repeatCount="indefinite" path={path} />
        </circle>
      )}
      {label && (
        <EdgeLabelRenderer>
          <div
            style={{ position: "absolute", transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`, pointerEvents: "all" }}
            className="rounded-md border border-white/10 bg-black/70 px-1.5 py-0.5 font-mono text-[10px] text-white/80"
          >
            {label}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}

export default TrafficEdge;
