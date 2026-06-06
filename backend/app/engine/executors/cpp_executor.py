"""C++ Executor — compiles with g++ -O2, runs native binary"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class CppExecutor(BaseExecutor):
    language = Language.CPP
    docker_image = "interleet-cpp:latest"
    filename = "solution.cpp"
    compile_command = ["sh", "-c", "g++ -O2 -std=c++17 -o solution solution.cpp 2>&1"]
    run_command = ["sh", "-c", "./solution < stdin.txt"]
    requires_compile = True
