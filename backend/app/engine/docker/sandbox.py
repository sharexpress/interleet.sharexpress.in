"""
Interleet Judge Engine — Docker Sandbox
Secure isolated container execution using the Docker SDK.

Architecture:
  - ONE persistent container per language image (centralized execution engine)
  - Container runs `sleep infinity` and stays alive forever
  - Code execution uses `container.exec_run()` — no container create/destroy per run
  - In-memory cache eliminates Docker API lookups on every call
  - Dedicated thread pool prevents thread starvation under load

Security model:
  - network_disabled=True        (no outbound networking)
  - mem_limit                    (hard memory cap)
  - nano_cpus=2_000_000_000      (max 2 CPU cores)
  - pids_limit=256               (blocks fork bombs)
  - security_opt no-new-privileges (prevents privilege escalation)
  - cap_drop ALL                 (removes all Linux capabilities)
  - tmpfs /tmp                   (ephemeral scratch space)
  - Timeout kill via `timeout` command wrapper
"""

from __future__ import annotations

import asyncio
import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import docker
import docker.errors
from docker.models.containers import Container

from app.engine.schemas import CompileResult, SandboxResult

logger = logging.getLogger(__name__)

# Output size guard — 10 MB max stdout/stderr
MAX_OUTPUT_BYTES = 10 * 1024 * 1024

# Dedicated thread pool for Docker calls (prevents starvation of the default pool)
_DOCKER_THREAD_POOL = ThreadPoolExecutor(max_workers=12, thread_name_prefix="docker-exec")

# Docker client (lazy singleton)
_docker_client: docker.DockerClient | None = None
_docker_client_lock = threading.Lock()

# ─── In-memory container cache ────────────────────────────────────────────
# Key: image name (e.g. "interleet-python:latest")
# Value: Container object
_container_cache: dict[str, Container] = {}
_container_cache_lock = threading.Lock()


def get_docker_client() -> docker.DockerClient:
    global _docker_client
    if _docker_client is None:
        with _docker_client_lock:
            if _docker_client is None:
                _docker_client = docker.from_env()
    return _docker_client


def _create_persistent_container(client: docker.DockerClient, image: str) -> Container:
    """Create a new persistent container for the given image.
    
    Handles race conditions when multiple PM2 instances start simultaneously
    and all try to create the same container. If container already exists (409),
    we simply reuse it instead of crashing.
    """
    container_name = f"interleet-engine-{image.replace(':', '-').replace('/', '-')}"
    workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
    os.makedirs(workspace_base, exist_ok=True)

    # Try to reuse existing container first (another PM2 instance may have created it)
    try:
        existing = client.containers.get(container_name)
        if existing.status == "running":
            logger.info("Reusing existing container: %s (image=%s)", container_name, image)
            return existing
        # Not running — try to start it
        existing.start()
        existing.reload()
        if existing.status == "running":
            logger.info("Restarted existing container: %s (image=%s)", container_name, image)
            return existing
        # Still not running — remove and recreate
        existing.remove(force=True)
    except docker.errors.NotFound:
        pass
    except Exception as exc:
        logger.warning("Failed to recover container %s: %s", container_name, exc)
        try:
            client.containers.get(container_name).remove(force=True)
        except Exception:
            pass

    try:
        container = client.containers.run(
            image=image,
            command=["sleep", "infinity"],
            name=container_name,
            volumes={
                workspace_base: {"bind": "/workspace", "mode": "rw"}
            },
            network_disabled=True,
            mem_limit="512m",
            memswap_limit="512m",
            nano_cpus=2_000_000_000,
            pids_limit=256,
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],
            detach=True,
            remove=False,
            tmpfs={"/tmp": "size=256m,noexec,nosuid"},
            restart_policy={"Name": "unless-stopped"},
        )
        logger.info("Created persistent container: %s (image=%s)", container_name, image)
        return container
    except docker.errors.APIError as exc:
        if exc.status_code == 409:
            # 409 Conflict: Another PM2 instance already created this container
            logger.info("Container created by another instance, reusing: %s", container_name)
            container = client.containers.get(container_name)
            if container.status != "running":
                container.start()
            return container
        raise


def get_container(image: str) -> Container:
    """
    Get the cached persistent container for this image.
    Creates one if it doesn't exist. Recreates if the container is dead.
    This is the HOT PATH — must be as fast as possible.
    """
    # Fast path: check cache without lock
    cached = _container_cache.get(image)
    if cached is not None:
        try:
            # Refresh status only if we suspect issues (reload is cheap, ~2ms)
            cached.reload()
            if cached.status == "running":
                return cached
        except Exception:
            pass
        # Container is dead or errored — evict from cache
        logger.warning("Cached container for %s is not running, recreating...", image)

    # Slow path: create or recover container (under lock)
    with _container_cache_lock:
        # Double-check after acquiring lock
        cached = _container_cache.get(image)
        if cached is not None:
            try:
                cached.reload()
                if cached.status == "running":
                    return cached
            except Exception:
                pass

        client = get_docker_client()

        # Try to find an existing container by name first
        container_name = f"interleet-engine-{image.replace(':', '-').replace('/', '-')}"
        try:
            existing = client.containers.get(container_name)
            if existing.status == "running":
                _container_cache[image] = existing
                logger.info("Recovered existing container: %s", container_name)
                return existing
            else:
                existing.start()
                existing.reload()
                if existing.status == "running":
                    _container_cache[image] = existing
                    logger.info("Restarted existing container: %s", container_name)
                    return existing
                # If it still won't start, remove and recreate
                existing.remove(force=True)
        except docker.errors.NotFound:
            pass
        except Exception as exc:
            logger.warning("Error recovering container %s: %s", container_name, exc)
            try:
                client.containers.get(container_name).remove(force=True)
            except Exception:
                pass

        # Create fresh container
        container = _create_persistent_container(client, image)
        _container_cache[image] = container
        return container


def prewarm_containers(images: list[str]) -> None:
    """
    Pre-warm containers for all language images at server startup.
    Called once during FastAPI lifespan startup.
    """
    client = get_docker_client()
    for image in images:
        try:
            # Check image exists first
            client.images.get(image)
            container = get_container(image)
            logger.info("Pre-warmed container for %s: %s", image, container.short_id)
        except docker.errors.ImageNotFound:
            logger.warning("Image not found (skipping pre-warm): %s", image)
        except Exception as exc:
            logger.error("Failed to pre-warm %s: %s", image, exc)


def invalidate_container(image: str) -> None:
    """Force-evict a container from cache (e.g., after image rebuild)."""
    with _container_cache_lock:
        container = _container_cache.pop(image, None)
        if container:
            try:
                container.remove(force=True)
            except Exception:
                pass
    logger.info("Invalidated container cache for: %s", image)


class DockerSandbox:
    """
    Utility class that executes user code inside persistent Docker containers via exec.
    Each language has ONE long-lived container — all execution happens via exec_run().
    """

    @staticmethod
    async def compile(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float = 30.0,
    ) -> CompileResult:
        """
        Run a compilation command inside the persistent container.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _DOCKER_THREAD_POOL,
            DockerSandbox._compile_sync,
            image,
            command,
            workspace,
            time_limit,
        )

    @staticmethod
    async def run(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
        memory_limit_mb: int,
    ) -> SandboxResult:
        """
        Run the execution command inside the persistent container.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _DOCKER_THREAD_POOL,
            DockerSandbox._run_sync,
            image,
            command,
            workspace,
            time_limit,
            memory_limit_mb,
        )

    @staticmethod
    async def run_isolated(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
        memory_limit_mb: int,
    ) -> SandboxResult:
        """
        Run the execution command inside a completely isolated, single-use container.
        This is required for DevOps challenges where side-effects must not leak.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _DOCKER_THREAD_POOL,
            DockerSandbox._run_isolated_sync,
            image,
            command,
            workspace,
            time_limit,
            memory_limit_mb,
        )

    # ─── Sync implementations (run in dedicated thread pool) ───────────────

    @staticmethod
    def _compile_sync(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
    ) -> CompileResult:
        start = time.monotonic()

        try:
            container = get_container(image)

            workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
            try:
                rel = workspace.relative_to(workspace_base)
                container_workspace = f"/workspace/{rel}"
            except Exception:
                container_workspace = "/workspace"

            # Wrap command in timeout
            wrapped_command = command.copy()
            if len(command) >= 3 and command[0] == "sh" and command[1] == "-c":
                wrapped_command[2] = f"timeout {time_limit} {command[2]}"
            else:
                cmd_str = " ".join(command)
                wrapped_command = ["sh", "-c", f"timeout {time_limit} {cmd_str}"]

            exec_res = container.exec_run(
                cmd=wrapped_command,
                workdir=container_workspace,
                stdout=True,
                stderr=True,
                demux=True,
            )

            exit_code = exec_res.exit_code
            stdout_bytes, stderr_bytes = exec_res.output or (b"", b"")
            output = _decode_output(stdout_bytes or b"") + _decode_output(stderr_bytes or b"")

            elapsed_ms = (time.monotonic() - start) * 1000

            return CompileResult(
                success=(exit_code == 0),
                output=output if exit_code == 0 else "",
                error=output if exit_code != 0 else "",
                time_ms=elapsed_ms,
            )

        except docker.errors.ImageNotFound:
            return CompileResult(
                success=False,
                error=f"Docker image not found: {image}. Run 'make build-sandboxes'.",
            )
        except Exception as exc:
            logger.exception("Docker compile error: %s", exc)
            # Invalidate cache on unexpected errors (container may be broken)
            _container_cache.pop(image, None)
            return CompileResult(success=False, error=str(exc))

    @staticmethod
    def _run_sync(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
        memory_limit_mb: int,
    ) -> SandboxResult:
        start = time.monotonic()

        try:
            container = get_container(image)

            workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
            try:
                rel = workspace.relative_to(workspace_base)
                container_workspace = f"/workspace/{rel}"
            except Exception:
                container_workspace = "/workspace"

            # Wrap command in timeout
            wrapped_command = command.copy()
            if len(command) >= 3 and command[0] == "sh" and command[1] == "-c":
                wrapped_command[2] = f"timeout {time_limit} {command[2]}"
            else:
                cmd_str = " ".join(command)
                wrapped_command = ["sh", "-c", f"timeout {time_limit} {cmd_str}"]

            exec_res = container.exec_run(
                cmd=wrapped_command,
                workdir=container_workspace,
                stdout=True,
                stderr=True,
                demux=True,
            )

            exit_code = exec_res.exit_code
            stdout_bytes, stderr_bytes = exec_res.output or (b"", b"")

            stdout = _decode_output(stdout_bytes or b"")
            stderr = _decode_output(stderr_bytes or b"")

            timed_out = (exit_code == 124)
            oom_killed = (exit_code == 137)

            wall_time_ms = (time.monotonic() - start) * 1000

            # Enforce output size limit
            if len(stdout.encode()) > MAX_OUTPUT_BYTES:
                stdout = stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
                stderr += "\n[Output truncated: exceeded 10MB limit]"

            return SandboxResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                wall_time_ms=round(wall_time_ms, 2),
                peak_memory_mb=0.0,
                timed_out=timed_out,
                oom_killed=oom_killed,
            )

        except docker.errors.ImageNotFound:
            return SandboxResult(
                stderr=f"Docker image not found: {image}. Run 'make build-sandboxes'.",
                exit_code=127,
            )
        except Exception as exc:
            logger.exception("Docker run error: %s", exc)
            # Invalidate cache on unexpected errors
            _container_cache.pop(image, None)
            return SandboxResult(stderr=str(exc), exit_code=1)

    @staticmethod
    def _run_isolated_sync(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
        memory_limit_mb: int,
    ) -> SandboxResult:
        start = time.monotonic()
        client = get_docker_client()

        workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
        try:
            rel = workspace.relative_to(workspace_base)
            container_workspace = f"/workspace/{rel}"
        except Exception:
            container_workspace = "/workspace"

        import shlex
        cmd_str = shlex.join(command)
        # Timeout at the docker run level is hard, we'll wrap the command in timeout
        wrapped_command = ["sh", "-c", f"timeout {time_limit} {cmd_str}"]

        try:
            container = client.containers.run(
                image=image,
                command=wrapped_command,
                volumes={
                    workspace_base: {"bind": "/workspace", "mode": "rw"}
                },
                working_dir=container_workspace,
                network_disabled=True,
                mem_limit=f"{memory_limit_mb}m",
                memswap_limit=f"{memory_limit_mb}m",
                nano_cpus=2_000_000_000,
                pids_limit=256,
                security_opt=["no-new-privileges"],
                cap_drop=["ALL"],
                detach=True,
                remove=False,
            )

            # Wait for completion or timeout
            try:
                # Docker timeout just to be safe, but sh -c timeout handles the real timeout
                result = container.wait(timeout=int(time_limit + 5))
                exit_code = result["StatusCode"]
            except Exception:
                # Fallback if wait throws
                container.kill()
                exit_code = 124

            stdout_bytes = container.logs(stdout=True, stderr=False)
            stderr_bytes = container.logs(stdout=False, stderr=True)
            
            container.remove(force=True)

            stdout = _decode_output(stdout_bytes)
            stderr = _decode_output(stderr_bytes)

            timed_out = (exit_code == 124)
            oom_killed = (exit_code == 137)
            wall_time_ms = (time.monotonic() - start) * 1000

            if len(stdout.encode()) > MAX_OUTPUT_BYTES:
                stdout = stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
                stderr += "\\n[Output truncated: exceeded 10MB limit]"

            return SandboxResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                wall_time_ms=round(wall_time_ms, 2),
                peak_memory_mb=0.0,
                timed_out=timed_out,
                oom_killed=oom_killed,
            )

        except docker.errors.ImageNotFound:
            return SandboxResult(
                stderr=f"Docker image not found: {image}. Run 'make build-sandboxes'.",
                exit_code=127,
            )
        except Exception as exc:
            logger.exception("Docker run_isolated error: %s", exc)
            return SandboxResult(stderr=str(exc), exit_code=1)

    @staticmethod
    async def image_exists(image: str) -> bool:
        """Check if a Docker image exists locally."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_DOCKER_THREAD_POOL, DockerSandbox._image_exists_sync, image)

    @staticmethod
    def _image_exists_sync(image: str) -> bool:
        try:
            get_docker_client().images.get(image)
            return True
        except docker.errors.ImageNotFound:
            return False
        except Exception:
            return False


def _decode_output(raw: bytes | str) -> str:
    """Safely decode Docker log output."""
    if isinstance(raw, str):
        return raw
    try:
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return ""
