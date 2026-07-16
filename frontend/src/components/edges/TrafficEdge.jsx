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
        <>
          <g>
            <rect width="10" height="7" rx="1" fill={stroke} x="-5" y="-3.5" />
            <path d="M-5 -3.5 L0 0.5 L5 -3.5" stroke="#111111" strokeWidth="1" fill="none" />
            <animateMotion dur="2.4s" begin="0s" repeatCount="indefinite" path={path} />
          </g>
          <g>
            <rect width="10" height="7" rx="1" fill={stroke} x="-5" y="-3.5" />
            <path d="M-5 -3.5 L0 0.5 L5 -3.5" stroke="#111111" strokeWidth="1" fill="none" />
            <animateMotion dur="2.4s" begin="0.8s" repeatCount="indefinite" path={path} />
          </g>
          <g>
            <rect width="10" height="7" rx="1" fill={stroke} x="-5" y="-3.5" />
            <path d="M-5 -3.5 L0 0.5 L5 -3.5" stroke="#111111" strokeWidth="1" fill="none" />
            <animateMotion dur="2.4s" begin="1.6s" repeatCount="indefinite" path={path} />
          </g>
        </>
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
