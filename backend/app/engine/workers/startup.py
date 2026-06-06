"""
Interleet Judge Engine — Worker Startup
Launches async workers as background tasks on FastAPI startup.
"""

from __future__ import annotations

import asyncio
import logging

from app.engine.workers.execution_worker import WORKER_COUNT, WORKER_SHUTDOWN, ExecutionWorker

logger = logging.getLogger(__name__)

_worker_tasks: list[asyncio.Task] = []


async def start_workers() -> None:
    """
    Launch WORKER_COUNT async worker coroutines as asyncio tasks.
    Called from FastAPI lifespan on startup.
    """
    global _worker_tasks
    WORKER_SHUTDOWN.clear()

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
