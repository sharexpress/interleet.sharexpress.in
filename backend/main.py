"""
Interleet — FastAPI Application Entry Point
Self-hosted multi-language online judge engine + interview platform.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette.middleware.sessions import SessionMiddleware

load_dotenv(override=True)

from app.core.config import SESSION_SECRET_KEY
from app.core.db import get_db

# ─── Existing routers ──────────────────────────────────────────────
from app.routers.user import router as user_router
from app.routers.resume import router as resume_router
from app.routers.interview import router as interview_router
from app.routers.challenges import router as challenge_router
from app.routers.face import router as face_router
from app.routers.execution import router as execution_router

# ─── Judge Engine ──────────────────────────────────────────────────
from app.api.v1.execute import engine_router
from app.engine.websocket.router import ws_router
from app.engine.workers.startup import start_workers, stop_workers
from app.engine.docker.pool import verify_sandbox_images

logger = logging.getLogger(__name__)

# ─── Lifespan: startup + shutdown ─────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown tasks."""
    logger.info("=" * 60)
    logger.info("  Interleet Judge Engine — Starting Up")
    logger.info("=" * 60)

    # Check Docker sandbox images
    try:
        statuses = await verify_sandbox_images()
        available = sum(1 for s in statuses if s.available)
        logger.info("Docker sandbox images: %d/%d ready", available, len(statuses))
    except Exception as exc:
        logger.warning("Could not check Docker images (is Docker running?): %s", exc)

    # Start async execution workers (runs inside the API process)
    worker_count = int(os.environ.get("WORKER_COUNT", 4))
    if worker_count > 0:
        await start_workers()
        logger.info("Started %d in-process execution worker(s)", worker_count)
    else:
        logger.info("WORKER_COUNT=0 — workers disabled (using external worker container)")

    logger.info("🚀 Interleet API ready at http://0.0.0.0:8000")
    logger.info("📖 API Docs: http://0.0.0.0:8000/docs")

    yield

    # Shutdown
    logger.info("Shutting down Interleet...")
    if worker_count > 0:
        await stop_workers()
    logger.info("Goodbye.")


# ─── App ──────────────────────────────────────────────────────────

app = FastAPI(
    title="Interleet Judge Engine",
    description=(
        "Production-grade multi-language code execution engine. "
        "Supports Python, JavaScript, TypeScript, Go, C++, Rust, Java "
        "with Docker sandbox isolation, Redis queue, and WebSocket streaming."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ─── Middleware ────────────────────────────────────────────────────

CORS_ORIGINS = os.environ.get(
    "BACKEND_CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY or "fallback-session-secret",
    same_site="lax",
    https_only=False,
)


# ─── Routes ───────────────────────────────────────────────────────

# Health check
@app.get("/", tags=["Health"])
async def root(db: AsyncIOMotorDatabase = Depends(get_db)):
    collections = await db.list_collection_names()
    return {
        "service": "Interleet Judge Engine",
        "version": "2.0.0",
        "status": "ok",
        "collections": len(collections),
    }


# Uploads static files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ─── Judge Engine (v1) ────────────────────────────────────────────
app.include_router(engine_router)   # REST: /api/v1/execute, /submissions, /results, /health
app.include_router(ws_router)       # WebSocket: /api/v1/ws/{submission_id}

# ─── Existing Platform Routers ────────────────────────────────────
app.include_router(user_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(challenge_router)
app.include_router(face_router)
app.include_router(execution_router)  # Legacy: /api/execution/* (backward compat)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ.get("SERVER_HOST", "0.0.0.0"),
        port=int(os.environ.get("SERVER_PORT", 8000)),
        reload=True,
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
    )
