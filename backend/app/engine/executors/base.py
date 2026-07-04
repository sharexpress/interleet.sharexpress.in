"""
Interleet Judge Engine — Base Executor
Abstract base class for all language-specific executors.

Performance optimizations:
  - Batch testcase execution: ONE workspace for interpreted languages
  - Hardlinks instead of file copies for compiled binaries
  - Shared compile workspace avoids redundant compilations
"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import aiofiles

from app.engine.enums import ComparisonMode, Language, Verdict
from app.engine.schemas import (
    CompileResult,
    ExecuteRequest,
    ExecutionResult,
    ExecutionStatus,
    SandboxResult,
    TestCaseResult,
    TestCaseSchema,
)

logger = logging.getLogger(__name__)


class BaseExecutor(ABC):
    """
    Abstract base for all language executors.

    Subclasses define image, filenames, compile/run commands.
    The execute() method handles:
      1. Workspace creation
      2. Code + stdin file writes
      3. Compilation (if needed)
      4. Execution via Docker sandbox
      5. Result collection
    """

    language: Language
    docker_image: str
    filename: str                        # e.g., "solution.py"
    compile_command: Optional[list[str]] = None  # None = interpreted
    run_command: list[str]               # e.g., ["python3", "solution.py"]
    requires_compile: bool = False

    # ─── Public Entry Point ────────────────────────────────────────────────

    async def execute(
        self,
        request: ExecuteRequest,
        testcase: Optional[TestCaseSchema] = None,
    ) -> ExecutionResult:
        """
        Full execution pipeline for a single request + optional testcase.
        Used for one-shot /execute calls. For multi-testcase submissions,
        the worker calls run_testcase() directly.
        """
        from app.engine.docker.sandbox import DockerSandbox
        from app.engine.judge import JudgeEngine

        submission_id = str(__import__("uuid").uuid4())
        workspace = None

        try:
            workspace = await self._create_workspace()
            await self._write_code(workspace, request.code)
            stdin_data = testcase.stdin if testcase else request.stdin
            await self._write_stdin(workspace, stdin_data)

            # Compile phase
            compile_output = ""
            if self.requires_compile and self.compile_command:
                compile_result = await DockerSandbox.compile(
                    image=self.docker_image,
                    command=self.compile_command,
                    workspace=workspace,
                    time_limit=30.0,  # generous compile timeout
                )
                compile_output = compile_result.output or compile_result.error
                if not compile_result.success:
                    return ExecutionResult(
                        success=False,
                        submission_id=submission_id,
                        status=ExecutionStatus.COMPLETED,
                        verdict=Verdict.COMPILATION_ERROR,
                        compile_output=compile_output,
                        completed_at=__import__("datetime").datetime.utcnow(),
                    )

            # Run phase
            time_limit = testcase.time_limit if (testcase and testcase.time_limit) else request.time_limit
            memory_limit = testcase.memory_limit if (testcase and testcase.memory_limit) else request.memory_limit

            sandbox_result = await DockerSandbox.run(
                image=self.docker_image,
                command=self.run_command,
                workspace=workspace,
                time_limit=time_limit,
                memory_limit_mb=memory_limit,
            )

            # Judge
            if testcase:
                tc_result = JudgeEngine.evaluate(
                    sandbox_result=sandbox_result,
                    testcase=testcase,
                    compile_output=compile_output,
                    comparison_mode=request.comparison_mode,
                )
                scoring = JudgeEngine.score([tc_result])
                return ExecutionResult(
                    success=tc_result.passed,
                    submission_id=submission_id,
                    status=ExecutionStatus.COMPLETED,
                    verdict=scoring.verdict,
                    stdout=sandbox_result.stdout,
                    stderr=sandbox_result.stderr,
                    compile_output=compile_output,
                    memory=sandbox_result.peak_memory_mb,
                    time=sandbox_result.wall_time_ms / 1000,
                    exit_code=sandbox_result.exit_code,
                    testcase_results=[tc_result],
                    passed_testcases=scoring.passed,
                    total_testcases=scoring.total,
                    score=scoring.score,
                    completed_at=__import__("datetime").datetime.utcnow(),
                )
            else:
                # No expected output — just return raw output
                verdict = Verdict.RUNTIME_ERROR if sandbox_result.exit_code != 0 else Verdict.ACCEPTED
                if sandbox_result.timed_out:
                    verdict = Verdict.TIME_LIMIT_EXCEEDED
                if sandbox_result.oom_killed:
                    verdict = Verdict.MEMORY_LIMIT_EXCEEDED
                return ExecutionResult(
                    success=(verdict == Verdict.ACCEPTED),
                    submission_id=submission_id,
                    status=ExecutionStatus.COMPLETED,
                    verdict=verdict,
                    stdout=sandbox_result.stdout,
                    stderr=sandbox_result.stderr,
                    compile_output=compile_output,
                    memory=sandbox_result.peak_memory_mb,
                    time=sandbox_result.wall_time_ms / 1000,
                    exit_code=sandbox_result.exit_code,
                    completed_at=__import__("datetime").datetime.utcnow(),
                )

        except Exception as exc:
            logger.exception("Executor error for language=%s: %s", self.language, exc)
            return ExecutionResult(
                success=False,
                submission_id=submission_id,
                status=ExecutionStatus.FAILED,
                verdict=Verdict.INTERNAL_ERROR,
                error=str(exc),
                completed_at=__import__("datetime").datetime.utcnow(),
            )
        finally:
            if workspace:
                await self._cleanup_workspace(workspace)

    async def run_testcase(
        self,
        code: str,
        testcase: TestCaseSchema,
        time_limit: float,
        memory_limit: int,
        comparison_mode: ComparisonMode,
    ) -> tuple[SandboxResult, CompileResult | None]:
        """
        Low-level: run a single testcase, return (sandbox_result, compile_result).
        Called by the worker for multi-testcase submissions.
        Returns the raw sandbox result for the worker to judge.
        """
        from app.engine.docker.sandbox import DockerSandbox

        workspace = await self._create_workspace()
        try:
            await self._write_code(workspace, code)
            await self._write_stdin(workspace, testcase.stdin)

            compile_result = None
            if self.requires_compile and self.compile_command:
                compile_result = await DockerSandbox.compile(
                    image=self.docker_image,
                    command=self.compile_command,
                    workspace=workspace,
                    time_limit=30.0,
                )
                if not compile_result.success:
                    return SandboxResult(exit_code=1), compile_result

            tc_time_limit = testcase.time_limit or time_limit
            tc_memory = testcase.memory_limit or memory_limit

            sandbox_result = await DockerSandbox.run(
                image=self.docker_image,
                command=self.run_command,
                workspace=workspace,
                time_limit=tc_time_limit,
                memory_limit_mb=tc_memory,
            )
            return sandbox_result, compile_result
        finally:
            await self._cleanup_workspace(workspace)

    async def compile_code(self, code: str) -> tuple[bool, str, Path | None]:
        """
        Compile code once in a shared compile workspace.
        Returns (success, compile_output, compile_workspace_path).
        """
        from app.engine.docker.sandbox import DockerSandbox
        workspace = await self._create_workspace()
        try:
            await self._write_code(workspace, code)
            compile_result = await DockerSandbox.compile(
                image=self.docker_image,
                command=self.compile_command,
                workspace=workspace,
                time_limit=30.0,
            )
            compile_output = compile_result.output or compile_result.error
            if not compile_result.success:
                await self._cleanup_workspace(workspace)
                return False, compile_output, None
            return True, compile_output, workspace
        except Exception as exc:
            logger.exception("Compile error: %s", exc)
            if workspace:
                await self._cleanup_workspace(workspace)
            return False, str(exc), None

    async def run_testcase_with_compile_workspace(
        self,
        code: str,
        testcase: TestCaseSchema,
        time_limit: float,
        memory_limit: int,
        compile_workspace: Path | None = None,
    ) -> SandboxResult:
        """
        Run a testcase in its own isolated workspace, using hardlinks for
        pre-compiled files (avoids multi-MB file copies per testcase).
        """
        from app.engine.docker.sandbox import DockerSandbox

        workspace = await self._create_workspace()
        try:
            if compile_workspace:
                # Use hardlinks instead of copies — much faster for large binaries
                await self._link_compiled_files(compile_workspace, workspace)
            else:
                # Interpreted languages: write the source code directly
                await self._write_code(workspace, code)

            # Write testcase stdin
            await self._write_stdin(workspace, testcase.stdin)

            tc_time_limit = testcase.time_limit or time_limit
            tc_memory = testcase.memory_limit or memory_limit

            sandbox_result = await DockerSandbox.run(
                image=self.docker_image,
                command=self.run_command,
                workspace=workspace,
                time_limit=tc_time_limit,
                memory_limit_mb=tc_memory,
            )
            return sandbox_result
        finally:
            await self._cleanup_workspace(workspace)

    # ─── Batch Execution (Interpreted Languages) ───────────────────────────

    async def run_batch_testcases(
        self,
        code: str,
        testcases: list[TestCaseSchema],
        time_limit: float,
        memory_limit: int,
    ) -> list[SandboxResult]:
        """
        Run multiple testcases in a SINGLE workspace (interpreted languages only).
        
        Instead of:  create-workspace → write-code → write-stdin → run → cleanup  (per TC)
        We do:       create-workspace → write-code → [write-stdin → run] × N → cleanup
        
        This saves ~20-30ms per testcase by avoiding redundant workspace I/O.
        Testcases run sequentially in the same workspace (safe for interpreted langs).
        """
        from app.engine.docker.sandbox import DockerSandbox

        workspace = await self._create_workspace()
        results: list[SandboxResult] = []

        try:
            # Write code ONCE
            await self._write_code(workspace, code)

            # Run each testcase in sequence, swapping stdin and writing specific files
            for tc in testcases:
                await self._write_stdin(workspace, tc.stdin)
                
                if hasattr(tc, 'files') and tc.files:
                    for fname, content in tc.files.items():
                        # Ensure no directory traversal exploits
                        safe_name = os.path.basename(fname)
                        async with aiofiles.open(workspace / safe_name, "w", encoding="utf-8") as f:
                            await f.write(content)
                        (workspace / safe_name).chmod(0o644)

                tc_time_limit = tc.time_limit or time_limit
                tc_memory = tc.memory_limit or memory_limit

                sandbox_result = await DockerSandbox.run(
                    image=self.docker_image,
                    command=self.run_command,
                    workspace=workspace,
                    time_limit=tc_time_limit,
                    memory_limit_mb=tc_memory,
                )
                results.append(sandbox_result)

            return results
        except Exception as exc:
            logger.exception("Batch execution error: %s", exc)
            # Fill remaining results with error
            while len(results) < len(testcases):
                results.append(SandboxResult(stderr=str(exc), exit_code=1))
            return results
        finally:
            await self._cleanup_workspace(workspace)

    # ─── Workspace Helpers ─────────────────────────────────────────────────

    @staticmethod
    async def _create_workspace() -> Path:
        """Create an isolated temp directory for this execution."""
        base = Path(os.environ.get("EXECUTION_WORKSPACE_DIR", "/tmp/interleet_workspaces"))
        base.mkdir(parents=True, exist_ok=True)
        tmp_dir = Path(tempfile.mkdtemp(dir=base, prefix="exec_"))
        tmp_dir.chmod(0o777)
        return tmp_dir

    async def _write_code(self, workspace: Path, code: str) -> None:
        """Write source code to workspace."""
        code_path = workspace / self.filename
        async with aiofiles.open(code_path, "w", encoding="utf-8") as f:
            await f.write(code)
        code_path.chmod(0o644)

    @staticmethod
    async def _write_stdin(workspace: Path, stdin: str) -> None:
        """Write stdin to workspace/stdin.txt."""
        stdin_path = workspace / "stdin.txt"
        async with aiofiles.open(stdin_path, "w", encoding="utf-8") as f:
            await f.write(stdin)
        stdin_path.chmod(0o644)

    @staticmethod
    async def _link_compiled_files(src_workspace: Path, dst_workspace: Path) -> None:
        """
        Link compiled files from compile workspace to run workspace.
        Uses hardlinks (instant, zero-copy) with fallback to regular copy.
        """
        import shutil

        loop = asyncio.get_event_loop()

        def _do_link():
            for item in src_workspace.iterdir():
                if item.name == "stdin.txt" or not item.is_file():
                    continue
                dst = dst_workspace / item.name
                try:
                    # Hardlink: instant, no data copy, same inode
                    os.link(item, dst)
                except OSError:
                    # Fallback: regular copy (cross-device, etc.)
                    shutil.copy2(item, dst)

        await loop.run_in_executor(None, _do_link)

    @staticmethod
    async def _cleanup_workspace(workspace: Path) -> None:
        """Recursively remove the workspace directory."""
        try:
            import shutil
            await asyncio.get_event_loop().run_in_executor(
                None, shutil.rmtree, workspace, True
            )
        except Exception as exc:
            logger.warning("Failed to cleanup workspace %s: %s", workspace, exc)
