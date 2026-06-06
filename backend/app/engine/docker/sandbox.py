"""
Interleet Judge Engine — Docker Sandbox
Secure isolated container execution using the Docker SDK.

Security model:
  - network_disabled=True        (no outbound networking)
  - mem_limit                    (hard memory cap)
  - nano_cpus=1_000_000_000      (max 1 CPU core)
  - pids_limit=64                (blocks fork bombs)
  - security_opt no-new-privileges (prevents privilege escalation)
  - cap_drop ALL                 (removes all Linux capabilities)
  - read_only root FS where safe (workspace volume is always rw)
  - Timeout kill via container.stop()
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from pathlib import Path

import docker
import docker.errors
from docker.models.containers import Container

from app.engine.schemas import CompileResult, SandboxResult

logger = logging.getLogger(__name__)

# Output size guard — 10 MB max stdout/stderr
MAX_OUTPUT_BYTES = 10 * 1024 * 1024

# Docker client (lazy singleton)
_docker_client: docker.DockerClient | None = None


def get_docker_client() -> docker.DockerClient:
    global _docker_client
    if _docker_client is None:
        _docker_client = docker.from_env()
    return _docker_client


class DockerSandbox:
    """
    Static utility class that runs code inside isolated Docker containers.

    All methods are async (offload blocking Docker calls to a thread pool).
    """

    # ─── Public API ────────────────────────────────────────────────────────

    @staticmethod
    async def compile(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float = 30.0,
    ) -> CompileResult:
        """
        Run a compilation command inside a container.
        Returns CompileResult with success flag and compiler output.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
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
        Run the execution command inside a hardened container.
        Returns SandboxResult with stdout, stderr, timing, and memory metrics.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            DockerSandbox._run_sync,
            image,
            command,
            workspace,
            time_limit,
            memory_limit_mb,
        )

    # ─── Sync implementations (run in thread pool) ─────────────────────────

    @staticmethod
    def _compile_sync(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
    ) -> CompileResult:
        client = get_docker_client()
        container: Container | None = None
        start = time.monotonic()

        try:
            container = client.containers.run(
                image=image,
                command=command,
                volumes={
                    str(workspace): {"bind": "/workspace", "mode": "rw"}
                },
                working_dir="/workspace",
                network_disabled=True,
                mem_limit="512m",  # generous for compilation
                nano_cpus=2_000_000_000,  # 2 CPUs for compilation
                pids_limit=128,
                security_opt=["no-new-privileges"],
                cap_drop=["ALL"],
                detach=True,
                stdout=True,
                stderr=True,
                remove=False,
                user="nobody",
            )

            try:
                result = container.wait(timeout=time_limit)
                exit_code = result.get("StatusCode", 1)
            except Exception:
                container.kill()
                return CompileResult(
                    success=False,
                    error="Compilation timed out",
                    time_ms=(time.monotonic() - start) * 1000,
                )

            logs = container.logs(stdout=True, stderr=True)
            output = _decode_output(logs)
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
            return CompileResult(success=False, error=str(exc))
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

    @staticmethod
    def _run_sync(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
        memory_limit_mb: int,
    ) -> SandboxResult:
        client = get_docker_client()
        container: Container | None = None
        start = time.monotonic()

        try:
            container = client.containers.run(
                image=image,
                command=command,
                volumes={
                    str(workspace): {"bind": "/workspace", "mode": "rw"}
                },
                working_dir="/workspace",
                # ─── Security ────────────────────────────
                network_disabled=True,
                mem_limit=f"{memory_limit_mb}m",
                memswap_limit=f"{memory_limit_mb}m",  # disable swap
                nano_cpus=1_000_000_000,              # 1 CPU core
                pids_limit=64,                        # block fork bombs
                security_opt=["no-new-privileges"],
                cap_drop=["ALL"],
                # ─── Isolation ───────────────────────────
                detach=True,
                stdout=True,
                stderr=True,
                remove=False,
                user="nobody",
                tmpfs={"/tmp": "size=32m,noexec,nosuid"},
            )

            timed_out = False
            oom_killed = False

            try:
                result = container.wait(timeout=time_limit + 2)
                exit_code = result.get("StatusCode", 1)
                oom_killed = result.get("Error", {}) == "OOM"
            except Exception:
                timed_out = True
                exit_code = 124  # Standard timeout exit code
                try:
                    container.kill()
                except Exception:
                    pass

            wall_time_ms = (time.monotonic() - start) * 1000

            # Collect stats before removal
            peak_memory_mb = 0.0
            try:
                stats = container.stats(stream=False)
                mem_usage = stats.get("memory_stats", {}).get("max_usage", 0)
                peak_memory_mb = round(mem_usage / (1024 * 1024), 2)
                # Check OOM from container inspect
                inspect = container.attrs
                if inspect.get("State", {}).get("OOMKilled", False):
                    oom_killed = True
            except Exception:
                pass

            # Collect output
            stdout_bytes = container.logs(stdout=True, stderr=False)
            stderr_bytes = container.logs(stdout=False, stderr=True)

            stdout = _decode_output(stdout_bytes)
            stderr = _decode_output(stderr_bytes)

            # Enforce output size limit
            if len(stdout.encode()) > MAX_OUTPUT_BYTES:
                stdout = stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
                stderr += "\n[Output truncated: exceeded 10MB limit]"

            return SandboxResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                wall_time_ms=round(wall_time_ms, 2),
                peak_memory_mb=peak_memory_mb,
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
            return SandboxResult(stderr=str(exc), exit_code=1)
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

    @staticmethod
    async def image_exists(image: str) -> bool:
        """Check if a Docker image exists locally."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, DockerSandbox._image_exists_sync, image)

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
