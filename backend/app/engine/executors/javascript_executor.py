"""JavaScript Executor — runs Node.js 20 via Alpine container"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class JavaScriptExecutor(BaseExecutor):
    language = Language.JAVASCRIPT
    docker_image = "interleet-node:latest"
    filename = "solution.js"
    compile_command = None
    run_command = ["sh", "-c", "node solution.js < stdin.txt"]
    requires_compile = False
