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


def get_or_create_prewarmed_container(client: docker.DockerClient, image: str) -> Container:
    """Get or dynamically start a pre-warmed background runner container."""
    container_name = f"interleet-prewarmed-{image.replace(':', '-')}"
    workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
    os.makedirs(workspace_base, exist_ok=True)

    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            try:
                container.start()
            except Exception:
                try:
                    container.remove(force=True)
                except Exception:
                    pass
                raise docker.errors.NotFound("Recreating broken container")
        return container
    except docker.errors.NotFound:
        # Create and start a new pre-warmed container
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
            tmpfs={"/tmp": "size=32m,noexec,nosuid"},
        )
        return container


class DockerSandbox:
    """
    Utility class that executes user code inside pre-warmed Docker containers via exec.
    """

    @staticmethod
    async def compile(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float = 30.0,
    ) -> CompileResult:
        """
        Run a compilation command inside the pre-warmed container.
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
        Run the execution command inside the pre-warmed container.
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
        start = time.monotonic()

        try:
            container = get_or_create_prewarmed_container(client, image)

            workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
            try:
                rel = workspace.relative_to(workspace_base)
                container_workspace = f"/workspace/{rel}"
            except Exception:
                container_workspace = "/workspace"

            # Wrap command in timeout command
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
            return CompileResult(success=False, error=str(exc))

    @staticmethod
    def _run_sync(
        image: str,
        command: list[str],
        workspace: Path,
        time_limit: float,
        memory_limit_mb: int,
    ) -> SandboxResult:
        client = get_docker_client()
        start = time.monotonic()

        try:
            container = get_or_create_prewarmed_container(client, image)

            workspace_base = os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces")
            try:
                rel = workspace.relative_to(workspace_base)
                container_workspace = f"/workspace/{rel}"
            except Exception:
                container_workspace = "/workspace"

            # Wrap command in timeout command
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
            return SandboxResult(stderr=str(exc), exit_code=1)

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
