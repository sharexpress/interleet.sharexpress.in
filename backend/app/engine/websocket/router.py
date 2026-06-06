"""
Interleet Judge Engine — WebSocket Router
WS /api/v1/ws/{submission_id} — live execution status stream.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.engine.enums import ExecutionStatus, WebSocketEventType
from app.engine.queue.redis_queue import get_execution_queue
from app.engine.schemas import WebSocketEvent
from app.engine.websocket.manager import ws_manager

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = int(os.environ.get("WS_HEARTBEAT_SECONDS", 30))

ws_router = APIRouter(tags=["WebSocket"])


@ws_router.websocket("/api/v1/ws/{submission_id}")
async def websocket_submission(websocket: WebSocket, submission_id: str):
    """
    WebSocket endpoint for real-time execution status updates.

    Events emitted:
      - queued       → job entered queue
      - compiling    → compilation in progress
      - running      → testcases executing
      - judging      → scoring in progress
      - completed    → final result ready
      - failed       → internal error
      - heartbeat    → keep-alive ping (every 30s)

    The client receives JSON-serialized WebSocketEvent objects.
    Connection closes automatically when execution completes or fails.
    """
    queue = get_execution_queue()
    await ws_manager.connect(submission_id, websocket)

    # Send current status immediately on connect (in case job already started)
    try:
        current_status = await queue.get_status(submission_id)
        if current_status:
            status_value = current_status.get("status", ExecutionStatus.QUEUED.value)
            try:
                status_enum = ExecutionStatus(status_value)
            except ValueError:
                status_enum = ExecutionStatus.QUEUED

            init_event = WebSocketEvent(
                type=WebSocketEventType.QUEUED,
                submission_id=submission_id,
                status=status_enum,
                data=current_status,
            )
            await ws_manager.send_personal(websocket, init_event)
    except Exception as exc:
        logger.warning("Failed to send initial WebSocket status: %s", exc)

    heartbeat_task: asyncio.Task | None = None

    try:
        # Start heartbeat task
        heartbeat_task = asyncio.create_task(
            _send_heartbeats(websocket, submission_id)
        )

        # Keep connection alive until client disconnects
        while True:
            try:
                # Wait for client messages (ping/pong or close)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=HEARTBEAT_INTERVAL + 5)
                # Echo ping back as pong
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # Timeout is fine — heartbeat handles keep-alive
                pass
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        logger.debug("WebSocket client disconnected: submission=%s", submission_id)
    except Exception as exc:
        logger.warning("WebSocket error for submission=%s: %s", submission_id, exc)
    finally:
        if heartbeat_task:
            heartbeat_task.cancel()
        await ws_manager.disconnect(submission_id, websocket)


async def _send_heartbeats(websocket: WebSocket, submission_id: str) -> None:
    """Send periodic heartbeat events to keep the connection alive."""
    queue = get_execution_queue()
    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL)
        try:
            # Check if execution is done — if so, send final state and stop
            status_data = await queue.get_status(submission_id)
            status_str = status_data.get("status", "") if status_data else ""

            if status_str in (ExecutionStatus.COMPLETED.value, ExecutionStatus.FAILED.value):
                # Send completed/failed event so client can close
                try:
                    status_enum = ExecutionStatus(status_str)
                    event_type = (
                        WebSocketEventType.COMPLETED
                        if status_enum == ExecutionStatus.COMPLETED
                        else WebSocketEventType.FAILED
                    )
                    final_event = WebSocketEvent(
                        type=event_type,
                        submission_id=submission_id,
                        status=status_enum,
                        data=status_data,
                    )
                    await websocket.send_text(final_event.to_json())
                except Exception:
                    pass
                break

            # Send heartbeat
            heartbeat = WebSocketEvent(
                type=WebSocketEventType.HEARTBEAT,
                submission_id=submission_id,
                status=ExecutionStatus(status_str) if status_str else ExecutionStatus.QUEUED,
            )
            await websocket.send_text(heartbeat.to_json())
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.debug("Heartbeat send failed: %s", exc)
            break
