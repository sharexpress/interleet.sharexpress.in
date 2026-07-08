"""
Browser Executor — runs generic frontend code (HTML, React, etc.) inside a Headless Chromium Sandbox
"""
import json
import logging
import aiofiles
from pathlib import Path
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor
from app.engine.schemas import SandboxResult, TestCaseSchema

logger = logging.getLogger(__name__)

class BrowserExecutor(BaseExecutor):
    language = Language.HTML
    docker_image = "interleet-browser:latest"
    filename = "index.html"
    compile_command = None
    run_command = ["node", "/app/runner.js"]
    requires_compile = False

    async def _write_code(self, workspace: Path, code: str) -> None:
        """Write workspace files and the runtime.json configuration."""
        html_content = ""
        css_content = ""
        js_content = ""

        try:
            # Check if code is a JSON string of multiple files (e.g. from editor)
            data = json.loads(code)
            if isinstance(data, dict):
                html_content = data.get("index.html", "")
                css_content = data.get("index.css", "")
                js_content = data.get("index.js", "")
            else:
                html_content = code
        except Exception:
            # Fallback for plain text single file
            html_content = code

        # Write index.html
        async with aiofiles.open(workspace / "index.html", "w", encoding="utf-8") as f:
            await f.write(html_content)
        (workspace / "index.html").chmod(0o644)

        # Write index.css (always write to avoid 404 resource requests)
        async with aiofiles.open(workspace / "index.css", "w", encoding="utf-8") as f:
            await f.write(css_content)
        (workspace / "index.css").chmod(0o644)

        # Write index.js (always write to avoid 404 resource requests)
        async with aiofiles.open(workspace / "index.js", "w", encoding="utf-8") as f:
            await f.write(js_content)
        (workspace / "index.js").chmod(0o644)

        # Build runtime.json configuration
        # The evaluationScript supports two modes:
        # 1. Per-testcase evaluation: stdin JSON contains an "evaluation" field with JS code
        #    that interacts with the DOM and returns a result string (e.g. "PASS" or "FAIL: ...")
        # 2. Legacy evaluator functions: checks for global window functions like processRatingEvents
        evaluationScript = """
        const stdinStr = window.STDIN_CONTENT || '';
        if (!stdinStr) return 'NO_TEST_DEFINED';
        
        try {
            const input = JSON.parse(stdinStr);
            
            // Mode 1: Per-testcase DOM evaluation script
            if (input.evaluation) {
                const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
                const fn = new AsyncFunction(input.evaluation);
                return await fn();
            }
            
            // Mode 2: Legacy evaluator functions on window
            const evaluators = [
              'processRatingEvents',
              'parseMarkdown',
              'starRatingWidget',
              'debouncedSuggestions',
              'customFormValidator',
              'responsiveBreakpoint',
              'nestedFileDirectory',
              'virtualScrollingList',
              'modalTransitions',
              'cssGridAutoplacement'
            ];
            
            for (const name of evaluators) {
              if (typeof window[name] === 'function') {
                try {
                    let result;
                    if (name === 'parseMarkdown') {
                      result = window[name](input.markdown);
                    } else if (name === 'processRatingEvents') {
                      result = window[name](input.events);
                    } else {
                      result = window[name](input);
                    }
                    return typeof result === 'object' ? JSON.stringify(result) : result;
                } catch(e) {
                    return 'Error executing custom evaluator: ' + e.message;
                }
              }
            }
            
            return 'NO_EVALUATOR_FOUND';
        } catch(e) {
            return 'Error: ' + e.message;
        }
        """

        runtime_config = {
            "entry": "index.html",
            "timeout": 5000,
            "captureScreenshot": False,  # Enable later or per-challenge
            "captureDOM": True,
            "captureConsole": True,
            "network": "enabled",
            "evaluationScript": evaluationScript
        }

        async with aiofiles.open(workspace / "runtime.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(runtime_config, indent=2))
        (workspace / "runtime.json").chmod(0o644)

    def _parse_runner_output(self, sandbox_result: SandboxResult) -> SandboxResult:
        # If exit_code != 0 and it doesn't look like JSON, return as is
        if sandbox_result.exit_code != 0 and not sandbox_result.stdout.strip().startswith('{'):
            return sandbox_result
        
        try:
            # Diagnostic dump
            try:
                with open("/tmp/last_runner_output.json", "w") as df:
                    df.write(sandbox_result.stdout)
            except Exception:
                pass
            data = json.loads(sandbox_result.stdout)
            status = data.get("status", "error")
            stdout_str = data.get("stdout", "")
            errors = data.get("errors", [])
            screenshot_base64 = data.get("screenshot", None)
            dom_content = data.get("dom", None)
            
            stderr = sandbox_result.stderr
            if errors:
                stderr += "\n" + "\n".join(errors)
            
            return SandboxResult(
                stdout=stdout_str,
                stderr=stderr.strip(),
                exit_code=1 if status == "error" else sandbox_result.exit_code,
                wall_time_ms=sandbox_result.wall_time_ms,
                peak_memory_mb=sandbox_result.peak_memory_mb,
                timed_out=sandbox_result.timed_out,
                oom_killed=sandbox_result.oom_killed,
                screenshot_base64=screenshot_base64,
                dom_content=dom_content,
            )
        except Exception as e:
            logger.error("Failed to parse runner output: %s", e)
            return sandbox_result

    async def run_batch_testcases(
        self,
        code: str,
        testcases: list[TestCaseSchema],
        time_limit: float,
        memory_limit: int,
    ) -> list[SandboxResult]:
        """Override to parse the structured JSON output from the browser runner."""
        results = await super().run_batch_testcases(code, testcases, time_limit, memory_limit)
        return [self._parse_runner_output(r) for r in results]

    async def run_testcase(
        self,
        code: str,
        testcase: TestCaseSchema,
        time_limit: float,
        memory_limit: int,
        comparison_mode,
    ):
        """Override to parse the structured JSON output for a single testcase."""
        sandbox_result, compile_result = await super().run_testcase(
            code, testcase, time_limit, memory_limit, comparison_mode
        )
        return self._parse_runner_output(sandbox_result), compile_result

