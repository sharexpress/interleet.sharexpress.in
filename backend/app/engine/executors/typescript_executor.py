"""TypeScript Executor — compiles with tsc, runs with Node.js"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class TypeScriptExecutor(BaseExecutor):
    language = Language.TYPESCRIPT
    docker_image = "interleet-typescript:latest"
    filename = "solution.ts"
    compile_command = ["sh", "-c", "tsc --target ES2020 --module commonjs solution.ts 2>&1"]
    run_command = ["sh", "-c", "node solution.js < stdin.txt"]
    requires_compile = True
