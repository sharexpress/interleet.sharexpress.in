import json
import logging
from pathlib import Path
import aiofiles

from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor
from app.engine.executors.factory import _REGISTRY

logger = logging.getLogger(__name__)

class ServiceExecutor(BaseExecutor):
    """
    Executes backend API servers by wrapping the user's code in a service runner.
    The runner dynamically allocates a port, spawns the server, tests it via HTTP,
    and returns a structured JSON payload of the HTTP responses.
    """

    def __init__(self, language: Language):
        # Steal configuration from the CLI executor
        cli_exec = _REGISTRY[language]()
        self.language = language
        self.docker_image = cli_exec.docker_image
        self.filename = cli_exec.filename
        self.requires_compile = cli_exec.requires_compile
        self.compile_command = cli_exec.compile_command
        
        # The user command to actually start the server
        self.user_run_command = cli_exec.run_command

        # The command to start the service runner (baked into the container)
        if language in (Language.JAVASCRIPT, Language.TYPESCRIPT):
            self.run_command = ["node", "/app/service_runner.js"]
        elif language == Language.PYTHON:
            self.run_command = ["python3", "/app/service_runner.py"]
        elif language == Language.GO:
            self.run_command = ["python3", "/app/service_runner.py"]
        else:
            self.run_command = ["python3", "/app/service_runner.py"]

    async def _write_code(self, workspace: Path, code: str, time_limit: float = 5.0) -> None:
        """Write the user's code, package.json (if any), and runtime.json."""
        # Check if code is a dictionary representing multiple files
        if code.strip().startswith("{"):
            try:
                data = json.loads(code)
                if isinstance(data, dict):
                    # Write all files
                    for fname, content in data.items():
                        async with aiofiles.open(workspace / fname, "w", encoding="utf-8") as f:
                            await f.write(content)
                        (workspace / fname).chmod(0o644)
                else:
                    await super()._write_code(workspace, code, time_limit=time_limit)
            except Exception:
                await super()._write_code(workspace, code, time_limit=time_limit)
        else:
            # Plain code string
            await super()._write_code(workspace, code, time_limit=time_limit)

        # Build runtime.json configuration
        # Extract the user command array into a string or pass as array
        runtime_config = {
            "command": self.user_run_command,
            "health": {
                "type": "http",
                "path": "/health"
            }
        }

        async with aiofiles.open(workspace / "runtime.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(runtime_config, indent=2))
        (workspace / "runtime.json").chmod(0o644)

    async def run_batch_testcases(self, code, testcases, time_limit, memory_limit):
        # Override to parse the JSON output from the service runner
        sandbox_results = await super().run_batch_testcases(code, testcases, time_limit, memory_limit)
        
        parsed_results = []
        for sr, tc in zip(sandbox_results, testcases):
            if sr.exit_code != 0 and not sr.stdout.strip().startswith("{"):
                parsed_results.append(sr)
                continue
            
            try:
                data = json.loads(sr.stdout)
                status = data.get("status", "error")
                responses = data.get("responses", [])
                
                # Filter headers case-insensitively based on expected testcase config
                try:
                    expected_data = json.loads(tc.expected_output.strip())
                except Exception:
                    expected_data = None

                if isinstance(responses, list) and isinstance(expected_data, list):
                    for act_res, exp_res in zip(responses, expected_data):
                        exp_headers = exp_res.get("response", {}).get("headers", {})
                        act_headers = act_res.get("response", {}).get("headers", {})
                        
                        filtered_headers = {}
                        for k in exp_headers.keys():
                            val = next((act_headers[ah] for ah in act_headers if ah.lower() == k.lower()), None)
                            if val is not None:
                                filtered_headers[k] = val
                        
                        if "response" in act_res:
                            act_res["response"]["headers"] = filtered_headers

                # We format the 'stdout' as a JSON string of the responses so JudgeEngine can compare it semantically
                sr.stdout = json.dumps(responses)
                
                # Append user logs to stderr for debugging
                user_stdout = data.get("stdout", [])
                user_stderr = data.get("stderr", [])
                runner_logs = data.get("logs", [])
                
                debug_info = []
                if runner_logs:
                    debug_info.append("=== RUNNER LOGS ===")
                    debug_info.extend(runner_logs)
                if user_stdout:
                    debug_info.append("=== SERVER STDOUT ===")
                    debug_info.extend(user_stdout)
                if user_stderr:
                    debug_info.append("=== SERVER STDERR ===")
                    debug_info.extend(user_stderr)
                    
                if debug_info:
                    sr.stderr = "\n".join(debug_info) + "\n" + sr.stderr
                
                if status == "error":
                    sr.exit_code = 1
                    
                parsed_results.append(sr)
            except Exception as e:
                logger.error("Failed to parse service runner output: %s", e)
                parsed_results.append(sr)
                
        return parsed_results
