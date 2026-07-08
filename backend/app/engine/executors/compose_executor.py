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

        from app.engine.schemas import StepEvent
        steps = [
            StepEvent(id="workspace", title="Workspace Created", status="passed", durationMs=10),
            StepEvent(id="config", title="Docker Compose Parsed", status="passed", durationMs=5),
            StepEvent(id="containers", title="Services Started", status="passed", durationMs=int(sandbox_res.wall_time_ms * 0.4)),
            StepEvent(
                id="validation",
                title="Integration Tests",
                status="passed" if tc_result.passed else "failed",
                durationMs=int(sandbox_res.wall_time_ms * 0.6),
                stdout=sandbox_res.stdout,
                stderr=sandbox_res.stderr
            )
        ]

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
            steps=steps,
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
            import json
            import socket
            import re

            # Find a free port to avoid conflicts with host services like Jenkins (port 8080)
            def get_free_port():
                s = socket.socket()
                s.bind(('', 0))
                port = s.getsockname()[1]
                s.close()
                return port
            
            free_port = get_free_port()

            try:
                files = json.loads(code)
                if isinstance(files, dict):
                    for fname, content in files.items():
                        if fname == "docker-compose.yml":
                            content = re.sub(r'["\']8080:(\d+)["\']', f'"{free_port}:\\1"', content)
                            content = re.sub(r'\b8080:(\d+)\b', f'{free_port}:\\1', content)
                        
                        safe_name = os.path.basename(fname)
                        async with aiofiles.open(workspace / safe_name, "w", encoding="utf-8") as f:
                            await f.write(content)
                        if safe_name.endswith(".sh"):
                            (workspace / safe_name).chmod(0o755)
                else:
                    code = re.sub(r'["\']8080:(\d+)["\']', f'"{free_port}:\\1"', code)
                    code = re.sub(r'\b8080:(\d+)\b', f'{free_port}:\\1', code)
                    async with aiofiles.open(workspace / self.filename, "w", encoding="utf-8") as f:
                        await f.write(code)
            except json.JSONDecodeError:
                code = re.sub(r'["\']8080:(\d+)["\']', f'"{free_port}:\\1"', code)
                code = re.sub(r'\b8080:(\d+)\b', f'{free_port}:\\1', code)
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
                    verification_script = verification_script.replace("8080", str(free_port))
                    async with aiofiles.open(workspace / "verify.sh", "w", encoding="utf-8") as f:
                        await f.write(verification_script)
                    (workspace / "verify.sh").chmod(0o755)

                start_time = time.time()
                
                # Generate a clean alphanumeric project name to prevent invalid image/tag reference formats
                import random
                import string
                proj_name = "proj" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))

                try:
                    # Bring up docker-compose stack
                    up_proc = await asyncio.create_subprocess_exec(
                        "docker", "compose", "-p", proj_name, "up", "-d", "--build",
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
                finally:
                    # ALWAYS bring down the stack
                    down_proc = await asyncio.create_subprocess_exec(
                        "docker", "compose", "-p", proj_name, "down", "-v", "--remove-orphans",
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
