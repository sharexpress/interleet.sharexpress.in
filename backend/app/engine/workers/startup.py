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
Interleet Judge Engine — Worker Startup
Launches async workers and pre-warms Docker containers on FastAPI startup.

Pre-warming ensures the FIRST code execution is just as fast as subsequent ones
by creating all persistent containers before any user request arrives.
"""

from __future__ import annotations

import asyncio
import logging

from app.engine.workers.execution_worker import WORKER_COUNT, WORKER_SHUTDOWN, ExecutionWorker

logger = logging.getLogger(__name__)

_worker_tasks: list[asyncio.Task] = []

# All language Docker images to pre-warm at startup
_PREWARM_IMAGES = [
    "interleet-python:latest",
    "interleet-node:latest",      # JavaScript
    "interleet-typescript:latest", # TypeScript
    "interleet-cpp:latest",
    "interleet-go:latest",
    "interleet-rust:latest",
    "interleet-java:latest",
]


async def start_workers() -> None:
    """
    Launch WORKER_COUNT async worker coroutines as asyncio tasks.
    Also pre-warms all Docker containers so the first execution is instant.
    Called from FastAPI lifespan on startup.
    """
    global _worker_tasks
    WORKER_SHUTDOWN.clear()

    # Pre-warm Docker containers in a background thread (non-blocking)
    loop = asyncio.get_event_loop()
    try:
        from app.engine.docker.sandbox import prewarm_containers
        await loop.run_in_executor(None, prewarm_containers, _PREWARM_IMAGES)
        logger.info("🐳 Pre-warmed %d Docker containers", len(_PREWARM_IMAGES))
    except Exception as exc:
        logger.warning("Container pre-warm failed (will create on demand): %s", exc)

    # Start workers
    for i in range(WORKER_COUNT):
        worker = ExecutionWorker(worker_id=i + 1)
        task = asyncio.create_task(worker.run(), name=f"exec-worker-{i + 1}")
        _worker_tasks.append(task)

    logger.info("🚀 Started %d execution worker(s)", WORKER_COUNT)


async def stop_workers() -> None:
    """
    Signal all workers to stop and await their completion.
    Called from FastAPI lifespan on shutdown.
    """
    global _worker_tasks
    WORKER_SHUTDOWN.set()

    if _worker_tasks:
        logger.info("Stopping %d worker(s)...", len(_worker_tasks))
        # Give workers time to finish current job (max 30s)
        done, pending = await asyncio.wait(_worker_tasks, timeout=30)
        for task in pending:
            task.cancel()
        _worker_tasks.clear()
        logger.info("All workers stopped.")
