"""
Interleet Judge Engine — WebSocket Connection Manager
Thread-safe manager for broadcasting execution events to connected clients.
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections import defaultdict

from fastapi import WebSocket

from app.engine.schemas import WebSocketEvent

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = int(os.environ.get("WS_HEARTBEAT_SECONDS", 30))


class WebSocketConnectionManager:
    """
    Manages WebSocket connections keyed by submission_id.
    Multiple clients can connect to the same submission stream.
    """

    def __init__(self):
        # submission_id → set of connected WebSockets
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, submission_id: str, websocket: WebSocket) -> None:
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        async with self._lock:
            self._connections[submission_id].add(websocket)
        logger.debug(
            "WebSocket connected: submission=%s total_connections=%d",
            submission_id,
            len(self._connections[submission_id]),
        )

    async def disconnect(self, submission_id: str, websocket: WebSocket) -> None:
        """Remove a disconnected WebSocket."""
        async with self._lock:
            conns = self._connections.get(submission_id, set())
            conns.discard(websocket)
            if not conns:
                self._connections.pop(submission_id, None)
        logger.debug("WebSocket disconnected: submission=%s", submission_id)

    async def broadcast(self, submission_id: str, event: WebSocketEvent) -> None:
        """
        Broadcast a WebSocketEvent to all clients watching this submission.
        Dead connections are silently removed.
        """
        async with self._lock:
            connections = set(self._connections.get(submission_id, set()))

        if not connections:
            return

        message = event.to_json()
        dead: list[WebSocket] = []

        for ws in connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)

        # Clean up dead connections
        if dead:
            async with self._lock:
                for ws in dead:
                    self._connections.get(submission_id, set()).discard(ws)

    async def send_personal(self, websocket: WebSocket, event: WebSocketEvent) -> None:
        """Send an event to a single WebSocket connection."""
        try:
            await websocket.send_text(event.to_json())
        except Exception as exc:
            logger.warning("Failed to send personal WebSocket message: %s", exc)

    def active_connections_count(self) -> int:
        """Return total number of active WebSocket connections."""
        return sum(len(v) for v in self._connections.values())

    def is_subscribed(self, submission_id: str) -> bool:
        """Check if any clients are watching this submission."""
        return bool(self._connections.get(submission_id))


# Singleton instance used across the application
ws_manager = WebSocketConnectionManager()
