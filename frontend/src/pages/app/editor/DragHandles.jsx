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

import { useCallback, memo, useRef } from "react";

export const DragHandle = memo(function DragHandle({ onDelta, onDragStart, onDragEnd }) {
  const dragging = useRef(false);
  const startX = useRef(0);

  const onMouseDown = useCallback(
    (e) => {
      e.preventDefault();
      dragging.current = true;
      startX.current = e.clientX;
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      if (onDragStart) onDragStart();

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
        if (onDragEnd) onDragEnd();
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [onDelta, onDragStart, onDragEnd],
  );

  return (
    <div
      onMouseDown={onMouseDown}
      className="group relative z-10 h-full flex-shrink-0 transition-colors duration-200"
      style={{ width: 8, cursor: "col-resize" }}
    >
      {/* Centered thin vertical line matching VS Code */}
      <div
        className="absolute inset-y-0 left-1/2 w-[1px] -translate-x-1/2 bg-border/40 group-hover:bg-primary transition-colors duration-200"
      />
    </div>
  );
});

export const VerticalDragHandle = memo(function VerticalDragHandle({ onDelta, onDragStart, onDragEnd }) {
  const dragging = useRef(false);
  const startY = useRef(0);

  const onMouseDown = useCallback(
    (e) => {
      e.preventDefault();
      dragging.current = true;
      startY.current = e.clientY;
      document.body.style.cursor = "row-resize";
      document.body.style.userSelect = "none";
      if (onDragStart) onDragStart();

      const onMove = (ev) => {
        if (!dragging.current) return;
        const delta = ev.clientY - startY.current;
        startY.current = ev.clientY;
        onDelta(delta);
      };
      const onUp = () => {
        dragging.current = false;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
        if (onDragEnd) onDragEnd();
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [onDelta, onDragStart, onDragEnd],
  );

  return (
    <div
      onMouseDown={onMouseDown}
      className="group relative z-10 flex-shrink-0 transition-colors duration-200"
      style={{ height: 8, cursor: "row-resize" }}
    >
      {/* Centered thin horizontal line matching VS Code */}
      <div
        className="absolute inset-x-0 top-1/2 h-[1px] -translate-y-1/2 bg-border/40 group-hover:bg-primary transition-colors duration-200"
      />
    </div>
  );
});
