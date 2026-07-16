# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Interleet Judge Engine — Redis Execution Queue
Async-safe queue backed by Redis BRPOP/LPUSH.

Performance optimization:
  - In-process asyncio.Event notification registry
  - When a result is stored, the waiter is notified instantly
  - Eliminates 200ms polling loops in the submission controller
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any, Optional

import redis.asyncio as aioredis

from app.engine.schemas import ExecutionJob

logger = logging.getLogger(__name__)

QUEUE_KEY = os.environ.get("REDIS_QUEUE_KEY", "interleet:execution_jobs")
STATUS_PREFIX = "interleet:status:"
RESULT_PREFIX = "interleet:result:"

# Status TTL in Redis (1 hour)
STATUS_TTL_SECONDS = 3600


class ExecutionQueue:
    """
    Redis-backed async execution queue.

    Jobs are serialized JSON pushed to a Redis list.
    Workers BRPOP (blocking pop) to receive jobs.
    Status updates are stored in Redis hashes for fast WebSocket polling.
    
    Includes an in-process notification system (asyncio.Event registry)
    so synchronous endpoints can await results without polling.
    """

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client
        # In-process notification: submission_id → asyncio.Event
        self._result_events: dict[str, asyncio.Event] = {}
        # Cached results for instant pickup after notification
        self._result_cache: dict[str, dict] = {}

    # ─── Job Queue Operations ──────────────────────────────────────────────

    async def enqueue(self, job: ExecutionJob) -> str:
        """Push a job to the tail of the queue. Returns the job_id."""
        payload = job.to_redis()
        await self._redis.lpush(QUEUE_KEY, payload)
        logger.debug("Enqueued job %s (lang=%s)", job.job_id, job.language)
        return job.job_id

    async def dequeue(self, timeout: int = 5) -> Optional[ExecutionJob]:
        """
        Blocking pop from queue. Waits up to `timeout` seconds.
        Returns None on timeout (allows graceful shutdown checks).
        """
        result = await self._redis.brpop(QUEUE_KEY, timeout=timeout)
        if result is None:
            return None
        _, raw = result
        try:
            return ExecutionJob.from_redis(raw)
        except Exception as exc:
            logger.error("Failed to deserialize job from queue: %s", exc)
            return None

    async def queue_length(self) -> int:
        """Return current number of jobs in the queue."""
        return await self._redis.llen(QUEUE_KEY)

    # ─── Instant Notification System ───────────────────────────────────────

    def register_waiter(self, submission_id: str) -> asyncio.Event:
        """
        Register a waiter for a submission result.
        Returns an asyncio.Event that will be set when the result arrives.
        """
        event = asyncio.Event()
        self._result_events[submission_id] = event
        return event

    def unregister_waiter(self, submission_id: str) -> None:
        """Clean up waiter registration."""
        self._result_events.pop(submission_id, None)
        self._result_cache.pop(submission_id, None)

    def _notify_waiter(self, submission_id: str, result: dict) -> None:
        """Notify a waiting controller that the result is ready."""
        event = self._result_events.get(submission_id)
        if event:
            self._result_cache[submission_id] = result
            event.set()

    async def wait_for_result(
        self,
        submission_id: str,
        timeout: float = 20.0,
    ) -> Optional[dict[str, Any]]:
        """
        Wait for a submission result.
        Uses in-process asyncio.Event combined with Redis Pub/Sub for multi-process support.
        """
        event = self.register_waiter(submission_id)
        
        # Check in-process cache first (fastest)
        cached = self._result_cache.get(submission_id)
        if cached:
            self.unregister_waiter(submission_id)
            return cached
            
        # Check Redis (in case it completed before we registered)
        redis_cached = await self.get_result(submission_id)
        if redis_cached:
            self.unregister_waiter(submission_id)
            return redis_cached

        # Subscribe to Redis Pub/Sub channel
        pubsub = self._redis.pubsub()
        channel = f"interleet:channel:{submission_id}"
        await pubsub.subscribe(channel)

        async def listen_pubsub():
            try:
                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            result_data = json.loads(message['data'])
                            self._notify_waiter(submission_id, result_data)
                            break
                        except Exception:
                            pass
            except Exception:
                pass

        listener_task = asyncio.create_task(listen_pubsub())

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
            return self._result_cache.get(submission_id)
        except asyncio.TimeoutError:
            # Fallback check one last time
            return await self.get_result(submission_id)
        finally:
            listener_task.cancel()
            try:
                await pubsub.unsubscribe(channel)
                await pubsub.close()
            except Exception:
                pass
            self.unregister_waiter(submission_id)

    # ─── Status / Result Storage ───────────────────────────────────────────

    async def set_status(
        self,
        submission_id: str,
        status: str,
        data: Optional[dict[str, Any]] = None,
    ) -> None:
        """Store execution status in Redis hash (for WebSocket polling)."""
        key = f"{STATUS_PREFIX}{submission_id}"
        payload: dict[str, Any] = {"status": status}
        if data:
            payload.update(data)
        await self._redis.hset(key, mapping={k: json.dumps(v) if not isinstance(v, str) else v for k, v in payload.items()})
        await self._redis.expire(key, STATUS_TTL_SECONDS)

    async def get_status(self, submission_id: str) -> dict[str, Any]:
        """Retrieve execution status from Redis."""
        key = f"{STATUS_PREFIX}{submission_id}"
        raw = await self._redis.hgetall(key)
        if not raw:
            return {}
        result = {}
        for k, v in raw.items():
            key_str = k.decode() if isinstance(k, bytes) else k
            val_str = v.decode() if isinstance(v, bytes) else v
            try:
                result[key_str] = json.loads(val_str)
            except (json.JSONDecodeError, ValueError):
                result[key_str] = val_str
        return result

    async def store_result(
        self, submission_id: str, result: dict[str, Any]
    ) -> None:
        """
        Store the final execution result in Redis (for fast retrieval).
        Also notifies any in-process waiter and publishes to Redis Pub/Sub.
        """
        key = f"{RESULT_PREFIX}{submission_id}"
        payload = json.dumps(result, default=str)
        await self._redis.set(key, payload, ex=STATUS_TTL_SECONDS)
        
        # Instantly notify the waiting controller in this process
        self._notify_waiter(submission_id, result)
        
        # Publish to other processes via Pub/Sub
        channel = f"interleet:channel:{submission_id}"
        await self._redis.publish(channel, payload)

    async def get_result(self, submission_id: str) -> Optional[dict[str, Any]]:
        """Retrieve cached execution result from Redis."""
        key = f"{RESULT_PREFIX}{submission_id}"
        raw = await self._redis.get(key)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    # ─── Health Check ──────────────────────────────────────────────────────

    async def ping(self) -> bool:
        """Check Redis connectivity."""
        try:
            return await self._redis.ping()
        except Exception:
            return False


# ─── Singleton Redis client factory ───────────────────────────────────────

_redis_client: aioredis.Redis | None = None
_queue_instance: ExecutionQueue | None = None


def get_redis_client() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        host = os.environ.get("REDIS_HOST", "localhost")
        port = int(os.environ.get("REDIS_PORT", 6379))
        db = int(os.environ.get("REDIS_DB", 0))
        password = os.environ.get("REDIS_PASSWORD") or None
        _redis_client = aioredis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=False,
            socket_connect_timeout=5,
            socket_timeout=10,
            retry_on_timeout=True,
        )
    return _redis_client


def get_execution_queue() -> ExecutionQueue:
    global _queue_instance
    if _queue_instance is None:
        _queue_instance = ExecutionQueue(get_redis_client())
    return _queue_instance
