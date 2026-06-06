"""Python Executor — runs Python 3.12 via Alpine container"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class PythonExecutor(BaseExecutor):
    language = Language.PYTHON
    docker_image = "interleet-python:latest"
    filename = "solution.py"
    compile_command = None
    run_command = ["sh", "-c", "python3 solution.py < stdin.txt"]
    requires_compile = False
