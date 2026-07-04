"""HTML Executor — runs frontend HTML/CSS/JS code inside Alpine container with JSDOM"""
import json
import logging
import aiofiles
from pathlib import Path
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor

logger = logging.getLogger(__name__)

class HtmlExecutor(BaseExecutor):
    language = Language.HTML
    docker_image = "interleet-node:latest"
    filename = "index.html"
    compile_command = None
    run_command = ["sh", "-c", "node runner.js < stdin.txt"]
    requires_compile = False

    async def _write_code(self, workspace: Path, code: str) -> None:
        """Write HTML, CSS, JS and the runner script to the workspace."""
        html_content = ""
        css_content = ""
        js_content = ""

        try:
            # Check if code is a JSON string of multiple files
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

        # Write index.css
        async with aiofiles.open(workspace / "index.css", "w", encoding="utf-8") as f:
            await f.write(css_content)
        (workspace / "index.css").chmod(0o644)

        # Write index.js
        async with aiofiles.open(workspace / "index.js", "w", encoding="utf-8") as f:
            await f.write(js_content)
        (workspace / "index.js").chmod(0o644)

        # Define the runner.js wrapper
        runner_js = """
const fs = require('fs');
const path = require('path');
let JSDOM;
try {
  JSDOM = require('jsdom').JSDOM;
} catch (e) {
  // Fallback if jsdom is not available (mock minimal JSDOM mock-like window context)
  JSDOM = class {
    constructor(html) {
      this.window = {
        document: {
          createElement: () => ({ setAttribute: () => {}, appendChild: () => {}, style: {} }),
          head: { appendChild: () => {} },
          body: { appendChild: () => {} }
        }
      };
    }
    runVMScript() {}
  };
}

const stdin = fs.readFileSync(0, 'utf-8').trim();

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');
const css = fs.readFileSync(path.join(__dirname, 'index.css'), 'utf-8');
const js = fs.readFileSync(path.join(__dirname, 'index.js'), 'utf-8');

const dom = new JSDOM(html, {
  runScripts: "outside-only",
  resources: "usable"
});
const { window } = dom;

window.JSON = JSON;
window.console = console;
window.STDIN_CONTENT = stdin;

// Expose common DOM interaction methods if needed
try {
  dom.runVMScript(new (require('vm').Script)(js));
} catch (err) {
  console.error("Runtime error in index.js:", err);
  process.exit(1);
}

// Legacy problem function evaluators
let foundEvaluator = false;
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
    foundEvaluator = true;
    const input = JSON.parse(stdin);
    let result;
    if (name === 'parseMarkdown') {
      result = window[name](input.markdown);
      console.log(result);
    } else if (name === 'processRatingEvents') {
      result = window[name](input.events);
      console.log(JSON.stringify(result));
    } else {
      result = window[name](input);
      console.log(typeof result === 'object' ? JSON.stringify(result) : result);
    }
    break;
  }
}
"""

        # Write runner.js
        async with aiofiles.open(workspace / "runner.js", "w", encoding="utf-8") as f:
            await f.write(runner_js)
        (workspace / "runner.js").chmod(0o644)
