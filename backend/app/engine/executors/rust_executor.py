"""Rust Executor — compiles with rustc -O, runs native binary"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class RustExecutor(BaseExecutor):
    language = Language.RUST
    docker_image = "interleet-rust:latest"
    filename = "solution.rs"
    compile_command = ["sh", "-c", "rustc -O -o solution solution.rs 2>&1"]
    run_command = ["sh", "-c", "./solution < stdin.txt"]
    requires_compile = True
