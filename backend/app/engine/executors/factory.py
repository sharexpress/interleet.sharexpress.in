"""
Interleet Judge Engine — Executor Factory
Registry-based factory that returns the correct executor for a language.
"""

from __future__ import annotations

from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor
from app.engine.executors.cpp_executor import CppExecutor
from app.engine.executors.go_executor import GoExecutor
from app.engine.executors.java_executor import JavaExecutor
from app.engine.executors.javascript_executor import JavaScriptExecutor
from app.engine.executors.python_executor import PythonExecutor
from app.engine.executors.rust_executor import RustExecutor
from app.engine.executors.typescript_executor import TypeScriptExecutor

_REGISTRY: dict[Language, type[BaseExecutor]] = {
    Language.PYTHON: PythonExecutor,
    Language.JAVASCRIPT: JavaScriptExecutor,
    Language.TYPESCRIPT: TypeScriptExecutor,
    Language.GO: GoExecutor,
    Language.CPP: CppExecutor,
    Language.RUST: RustExecutor,
    Language.JAVA: JavaExecutor,
}

# Language metadata for API responses / UI
LANGUAGE_META: dict[Language, dict] = {
    Language.PYTHON: {"name": "Python 3.12", "extension": "py", "compiled": False},
    Language.JAVASCRIPT: {"name": "Node.js 20", "extension": "js", "compiled": False},
    Language.TYPESCRIPT: {"name": "TypeScript 5", "extension": "ts", "compiled": True},
    Language.GO: {"name": "Go 1.22", "extension": "go", "compiled": True},
    Language.CPP: {"name": "C++17 (g++)", "extension": "cpp", "compiled": True},
    Language.RUST: {"name": "Rust 1.78", "extension": "rs", "compiled": True},
    Language.JAVA: {"name": "Java 21 (JDK)", "extension": "java", "compiled": True},
}


class ExecutorFactory:
    """Registry-based factory for language executors."""

    @staticmethod
    def get(language: Language | str) -> BaseExecutor:
        """Return an executor instance for the given language."""
        if isinstance(language, str):
            try:
                language = Language(language.lower())
            except ValueError:
                raise ValueError(f"Unsupported language: {language!r}") from None

        executor_cls = _REGISTRY.get(language)
        if executor_cls is None:
            raise ValueError(f"No executor registered for language: {language}")

        return executor_cls()

    @staticmethod
    def supported_languages() -> list[str]:
        """Return list of supported language strings."""
        return [lang.value for lang in _REGISTRY]

    @staticmethod
    def language_info(language: Language | str) -> dict:
        """Return metadata for a language."""
        if isinstance(language, str):
            language = Language(language.lower())
        return LANGUAGE_META.get(language, {})
