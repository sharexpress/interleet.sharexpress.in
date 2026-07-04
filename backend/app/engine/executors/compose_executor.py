import asyncio
import os
import time
import subprocess
from pathlib import Path
import aiofiles

from app.engine.enums import Language, Verdict
from app.engine.schemas import SandboxResult, TestCaseSchema, TestCaseResult
from app.engine.executors.base import BaseExecutor

class ComposeExecutor(BaseExecutor):
    """
    Executor for docker-compose based multi-container environments.
    """
    def __init__(self, language: Language = Language.PYTHON):
        self.language = language
        self.filename = "docker-compose.yml"
        self.docker_image = "" # Not used directly
        self.run_command = [] # Not used directly
        self.requires_compile = False
        self.compile_command = None

    async def execute(
        self,
        request,
        testcase = None,
    ):
        from app.engine.schemas import ExecutionResult, ExecutionStatus
        import datetime
        import uuid
        submission_id = str(uuid.uuid4())
        
        tc = testcase
        if not tc:
            from app.engine.schemas import TestCaseSchema
            tc = TestCaseSchema(
                stdin=request.stdin,
                expected_output=request.expected_output or "",
            )
            
        results = await self.run_batch_testcases(request.code, [tc], request.time_limit, request.memory_limit)
        sandbox_res = results[0]
        
        from app.engine.judge import JudgeEngine
        tc_result = JudgeEngine.evaluate(sandbox_res, tc, "", request.comparison_mode)
        
        scoring = JudgeEngine.score([tc_result])
        return ExecutionResult(
            success=tc_result.passed,
            submission_id=submission_id,
            status=ExecutionStatus.COMPLETED,
            verdict=scoring.verdict,
            stdout=sandbox_res.stdout,
            stderr=sandbox_res.stderr,
            compile_output="",
            memory=sandbox_res.peak_memory_mb,
            time=sandbox_res.wall_time_ms / 1000,
            exit_code=sandbox_res.exit_code,
            testcase_results=[tc_result],
            passed_testcases=scoring.passed,
            total_testcases=scoring.total,
            score=scoring.score,
            completed_at=datetime.datetime.utcnow(),
        )

    async def run_batch_testcases(
        self,
        code: str,
        testcases: list[TestCaseSchema],
        time_limit: float,
        memory_limit: int,
    ) -> list[SandboxResult]:
        workspace = await self._create_workspace()
        results: list[SandboxResult] = []

        try:
            # Code is assumed to be the docker-compose.yml content
            async with aiofiles.open(workspace / self.filename, "w", encoding="utf-8") as f:
                await f.write(code)

            for tc in testcases:
                # Write supplementary files (e.g. server.js, requirements.txt, init.sql)
                if hasattr(tc, 'files') and tc.files:
                    for fname, content in tc.files.items():
                        safe_name = os.path.basename(fname)
                        async with aiofiles.open(workspace / safe_name, "w", encoding="utf-8") as f:
                            await f.write(content)
                        (workspace / safe_name).chmod(0o644)
                
                # Write verification script
                verification_script = getattr(tc, "verification_script", None)
                if verification_script:
                    async with aiofiles.open(workspace / "verify.sh", "w", encoding="utf-8") as f:
                        await f.write(verification_script)
                    (workspace / "verify.sh").chmod(0o755)

                start_time = time.time()
                
                # Bring up docker-compose stack
                up_proc = await asyncio.create_subprocess_exec(
                    "docker", "compose", "up", "-d", "--build",
                    cwd=str(workspace),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                up_stdout, up_stderr = await up_proc.communicate()

                exit_code = 0
                stdout_result = ""
                stderr_result = up_stderr.decode('utf-8', errors='replace')

                if up_proc.returncode != 0:
                    exit_code = up_proc.returncode
                    stdout_result = "docker compose up failed:\n" + up_stdout.decode('utf-8', errors='replace')
                else:
                    # Give services a buffer to initialize
                    await asyncio.sleep(2)
                    
                    if verification_script:
                        # Run verification script on the host, targeting exposed ports or using docker exec
                        verify_proc = await asyncio.create_subprocess_exec(
                            "bash", "verify.sh",
                            cwd=str(workspace),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        tc_time_limit = tc.time_limit or time_limit
                        try:
                            v_stdout, v_stderr = await asyncio.wait_for(verify_proc.communicate(), timeout=tc_time_limit)
                            exit_code = verify_proc.returncode
                            stdout_result = v_stdout.decode('utf-8', errors='replace')
                            stderr_result += "\n" + v_stderr.decode('utf-8', errors='replace')
                        except asyncio.TimeoutError:
                            verify_proc.kill()
                            exit_code = 124
                            stdout_result = "Verification script timed out."
                    else:
                        stdout_result = "OK"

                # ALWAYS bring down the stack
                down_proc = await asyncio.create_subprocess_exec(
                    "docker", "compose", "down", "-v", "--remove-orphans",
                    cwd=str(workspace),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                await down_proc.communicate()

                wall_time_ms = int((time.time() - start_time) * 1000)

                results.append(
                    SandboxResult(
                        stdout=stdout_result,
                        stderr=stderr_result,
                        exit_code=exit_code,
                        wall_time_ms=wall_time_ms,
                        peak_memory_mb=0,  # Not tracked for compose yet
                        timed_out=(exit_code == 124),
                        oom_killed=False
                    )
                )

        finally:
            await self._cleanup_workspace(workspace)

        return results
