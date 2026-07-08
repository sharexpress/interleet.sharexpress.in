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
      className="group relative z-10 flex-shrink-0"
      style={{ width: 4, cursor: "col-resize" }}
    >
      <div
        className="absolute inset-y-0 left-0 right-0 bg-border opacity-0 transition-opacity group-hover:opacity-100"
        style={{ margin: "0 1px" }}
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
      className="group relative z-10 flex-shrink-0"
      style={{ height: 4, cursor: "row-resize" }}
    >
      <div
        className="absolute inset-x-0 top-0 bottom-0 bg-border opacity-0 transition-opacity group-hover:opacity-100"
        style={{ margin: "1px 0" }}
      />
    </div>
  );
});
