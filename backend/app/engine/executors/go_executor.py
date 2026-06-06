"""Go Executor — compiles with go build, runs native binary"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class GoExecutor(BaseExecutor):
    language = Language.GO
    docker_image = "interleet-go:latest"
    filename = "solution.go"
    compile_command = ["sh", "-c", "go build -o solution solution.go 2>&1"]
    run_command = ["sh", "-c", "./solution < stdin.txt"]
    requires_compile = True
