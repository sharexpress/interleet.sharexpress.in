"""
Interleet — Standalone Worker Entry Point
Run as: python -m app.engine.workers.main
Used by the `worker` Docker container in docker-compose.
"""

import asyncio
import logging
import os
import signal

from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    from app.engine.workers.startup import start_workers, stop_workers

    logger.info("=" * 60)
    logger.info("  Interleet Execution Worker")
    logger.info("  Worker Count: %s", os.environ.get("WORKER_COUNT", 4))
    logger.info("=" * 60)

    loop = asyncio.get_event_loop()

    def _handle_shutdown(sig):
        logger.info("Received signal %s, shutting down...", sig)
        loop.create_task(stop_workers())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _handle_shutdown, sig)

    await start_workers()

    # Keep running until shutdown is triggered
    from app.engine.workers.execution_worker import WORKER_SHUTDOWN
    while not WORKER_SHUTDOWN.is_set():
        await asyncio.sleep(1)

    logger.info("Worker process stopped.")


if __name__ == "__main__":
    asyncio.run(main())
