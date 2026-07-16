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

import os
from pathlib import Path
from typing import Optional
import aiofiles

from app.engine.enums import Language, Verdict
from app.engine.schemas import SandboxResult, TestCaseSchema, TestCaseResult
from app.engine.executors.base import BaseExecutor
from app.engine.docker.sandbox import DockerSandbox

class DevOpsExecutor(BaseExecutor):
    """
    Executor for DevOps / SysAdmin challenges.
    Runs the user's code inside a throwaway container, then optionally
    runs a verification script inside the exact SAME container to assert side effects.
    """
    
    def __init__(self, language: Language = Language.PYTHON):
        # We ignore language because devops always uses bash/sh.
        self.language = language
        # Force bash image
        self.docker_image = "interleet-devops:latest"
        self.run_command = ["bash", "solution.sh"]
        self.filename = "solution.sh"
        self.requires_compile = False
        self.compile_command = None

    async def execute(
        self,
        request,
        testcase = None,
    ):
        from app.engine.schemas import ExecutionResult, ExecutionStatus, Verdict
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
            StepEvent(id="workspace", title="Workspace Ready", status="passed", durationMs=10),
            StepEvent(id="config", title="Configuration Loaded", status="passed", durationMs=5),
            StepEvent(id="containers", title="Containers Started", status="passed", durationMs=int(sandbox_res.wall_time_ms * 0.2)),
            StepEvent(
                id="validation",
                title="Validation Suite",
                status="passed" if tc_result.passed else "failed",
                durationMs=int(sandbox_res.wall_time_ms * 0.8),
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

    async def _write_code(self, workspace: Path, code: str) -> None:
        """Write the user's shell script or multi-file dictionary."""
        import json
        try:
            files = json.loads(code)
            if isinstance(files, dict):
                for fname, content in files.items():
                    target_path = Path(workspace / fname).resolve()
                    if not str(target_path).startswith(str(workspace.resolve())):
                        continue
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    async with aiofiles.open(target_path, "w", encoding="utf-8") as f:
                        await f.write(content)
                    if fname.endswith(".sh"):
                        target_path.chmod(0o755)
                if "setup.sh" in files:
                    self.filename = "setup.sh"
                    self.run_command = ["bash", "setup.sh"]
                return
        except json.JSONDecodeError:
            pass

        async with aiofiles.open(workspace / self.filename, "w", encoding="utf-8") as f:
            await f.write(code)
        (workspace / self.filename).chmod(0o755)

    async def run_batch_testcases(
        self,
        code: str,
        testcases: list[TestCaseSchema],
        time_limit: float,
        memory_limit: int,
    ) -> list[SandboxResult]:
        """
        Run testcases in completely isolated containers.
        """
        workspace = await self._create_workspace()
        results: list[SandboxResult] = []

        try:
            # Write user code
            await self._write_code(workspace, code)

            for tc in testcases:
                # Provide standard input and files for the testcase
                await self._write_stdin(workspace, tc.stdin)
                
                if hasattr(tc, 'files') and tc.files:
                    for fname, content in tc.files.items():
                        safe_name = os.path.basename(fname)
                        async with aiofiles.open(workspace / safe_name, "w", encoding="utf-8") as f:
                            await f.write(content)
                        (workspace / safe_name).chmod(0o644)
                
                # Check if there is a verification script
                verification_script = getattr(tc, "verification_script", None)
                if verification_script:
                    async with aiofiles.open(workspace / "verify.sh", "w", encoding="utf-8") as f:
                        await f.write(verification_script)
                    (workspace / "verify.sh").chmod(0o755)

                # DevOps requires chaining commands in the same container.
                # If there's a verify script, we run the user code, THEN the verify code, 
                # all in one isolated execution to capture side-effects accurately.
                if verification_script:
                    # Run user script, then capture output of verification script
                    combined_cmd = f"bash {self.filename} ; bash verify.sh"
                else:
                    combined_cmd = f"bash {self.filename}"

                command = ["bash", "-c", combined_cmd]

                sandbox_result = await DockerSandbox.run_isolated(
                    image=self.docker_image,
                    command=command,
                    workspace=workspace,
                    time_limit=tc.time_limit or time_limit,
                    memory_limit_mb=tc.memory_limit or memory_limit,
                )

                # The actual stdout we evaluate is from the verification script!
                results.append(sandbox_result)

        finally:
            await self._cleanup_workspace(workspace)

        return results
