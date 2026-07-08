"""Runtime plugin metadata registry.

Runtime configuration is intentionally data-driven: API, worker, and editor all
consume the same document instead of maintaining domain-specific mappings.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Any


class RuntimeRegistry:
    _registry: dict[str, dict[str, Any]] = {}
    _lock = Lock()

    @classmethod
    def load_runtimes(cls, *, force: bool = False) -> None:
        with cls._lock:
            if cls._registry and not force:
                return

            configs_dir = Path(__file__).parent / "configs"
            runtimes: dict[str, dict[str, Any]] = {}
            for path in sorted(configs_dir.glob("*.json")):
                with path.open(encoding="utf-8") as config_file:
                    config = json.load(config_file)
                runtime_id = config.get("id")
                if not isinstance(runtime_id, str) or not runtime_id:
                    raise ValueError(f"Runtime config {path.name} has no valid id")
                if runtime_id in runtimes:
                    raise ValueError(f"Duplicate runtime id: {runtime_id}")
                config.setdefault("executionMode", "cli")
                config.setdefault("capabilities", {})
                config.setdefault("services", [])
                config.setdefault("limits", {})
                config.setdefault("artifacts", [])
                runtimes[runtime_id] = config
            cls._registry = runtimes

    @classmethod
    def get_runtime(cls, runtime_id: str | None) -> dict[str, Any]:
        cls.load_runtimes()
        return deepcopy(cls._registry.get(runtime_id or "", {}))

    @classmethod
    def get_all(cls) -> list[dict[str, Any]]:
        cls.load_runtimes()
        return [deepcopy(config) for config in cls._registry.values()]

    @classmethod
    def execution_mode(cls, runtime_id: str | None, fallback: str = "cli") -> str:
        runtime = cls.get_runtime(runtime_id)
        return str(runtime.get("executionMode") or fallback)

    @classmethod
    def runtime_for_mode(cls, execution_mode: str) -> dict[str, Any]:
        cls.load_runtimes()
        for config in cls._registry.values():
            if config.get("executionMode") == execution_mode:
                return deepcopy(config)
        return {}
